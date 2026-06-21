import json
import os
import socket
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import error, request
from urllib.parse import urlparse

SERVICE_NAME = os.getenv("NEXUS_SERVICE_NAME", "open-webui-adapter")
SERVICE_VERSION = os.getenv("NEXUS_SERVICE_VERSION", "v0.5")
SERVICE_PORT = int(os.getenv("NEXUS_SERVICE_PORT", "8080"))
NEXUS_ENV = os.getenv("NEXUS_ENV", "development")
CREWAI_URL = os.getenv("CREWAI_INTERNAL_URL", "http://crewai:8080").rstrip("/")
CREWAI_TIMEOUT_SECONDS = float(os.getenv("CREWAI_TIMEOUT_SECONDS", "30"))
SYSTEM_LOG_DIR = Path(os.getenv("NEXUS_SYSTEM_LOG_DIR", "/var/log/nexus/system"))
MODEL_ID = os.getenv("OPEN_WEBUI_ADAPTER_MODEL_ID", "nexus-crewai")
STARTED_AT = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SYSTEM_LOG_DIR.mkdir(parents=True, exist_ok=True)
SYSTEM_LOG_FILE = SYSTEM_LOG_DIR / "open-webui-adapter.jsonl"


def utc_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_system_log(event, **fields):
    payload = {
        "timestamp": utc_timestamp(),
        "service": SERVICE_NAME,
        "event": event,
        **fields,
    }
    with SYSTEM_LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + "\n")


def make_request_id():
    return f"owui-{uuid.uuid4().hex[:12]}"


def extract_user_request(payload):
    messages = payload.get("messages", [])
    for message in reversed(messages):
        if message.get("role") == "user":
            content = message.get("content", "")
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                text_parts = [part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text"]
                return "\n".join(text_parts).strip()
    prompt = payload.get("prompt", "")
    if isinstance(prompt, str):
        return prompt.strip()
    return ""


def call_crewai(user_request, request_id):
    body = json.dumps({"request": user_request, "source": "open-webui", "request_id": request_id}).encode("utf-8")
    crewai_request = request.Request(
        f"{CREWAI_URL}/orchestrate",
        data=body,
        headers={"Content-Type": "application/json", "X-Nexus-Request-ID": request_id},
        method="POST",
    )
    with request.urlopen(crewai_request, timeout=CREWAI_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def format_orchestration_message(result, request_id):
    workflow_id = result.get("workflow_id", "unknown")
    status = result.get("status", "unknown")
    summary = result.get("response", {}).get("summary", "Nexus orchestration completed.")
    validation = result.get("validation", {})
    approved = validation.get("approved", False)
    return "\n".join(
        [
            "Nexus orchestration completed.",
            f"Request ID: {request_id}",
            f"Workflow ID: {workflow_id}",
            f"Status: {status}",
            f"Reviewer approved: {str(approved).lower()}",
            "",
            summary,
        ]
    )


def openai_chat_response(payload, request_id, result):
    content = format_orchestration_message(result, request_id)
    return {
        "id": f"chatcmpl-{request_id}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.get("model", MODEL_ID),
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "nexus": {"request_id": request_id, "workflow_id": result.get("workflow_id"), "status": result.get("status")},
    }


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        body = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            return {}
        return json.loads(self.rfile.read(content_length).decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path in {"/", "/health", "/status"}:
            health = {
                "status": "healthy",
                "service": SERVICE_NAME,
                "version": SERVICE_VERSION,
                "environment": NEXUS_ENV,
                "hostname": socket.gethostname(),
                "started_at": STARTED_AT,
                "crewai_url": CREWAI_URL,
            }
            try:
                with request.urlopen(f"{CREWAI_URL}/health", timeout=3) as response:
                    health["crewai_status"] = json.loads(response.read().decode("utf-8")).get("status", "unknown")
            except Exception as exc:
                health["status"] = "unhealthy"
                health["crewai_status"] = "unreachable"
                health["message"] = "CrewAI orchestration is unavailable. Confirm the crewai service is running and healthy."
                health["error"] = str(exc)
                self.send_json(503, health)
                return
            self.send_json(200, health)
            return
        if path == "/v1/models":
            self.send_json(200, {"object": "list", "data": [{"id": MODEL_ID, "object": "model", "owned_by": "nexus"}]})
            return
        self.send_json(404, {"status": "not_found", "service": SERVICE_NAME})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/v1/chat/completions":
            self.send_json(404, {"status": "not_found", "service": SERVICE_NAME})
            return
        request_id = self.headers.get("X-Request-ID") or make_request_id()
        try:
            payload = self.read_json()
            user_request = extract_user_request(payload)
            if not user_request:
                write_system_log("invalid_request", request_id=request_id, reason="empty_user_message")
                self.send_json(400, {"error": {"message": "Nexus needs a user message to start orchestration.", "type": "invalid_request_error"}})
                return
            write_system_log("open_webui_request_received", request_id=request_id, model=payload.get("model", MODEL_ID))
            result = call_crewai(user_request, request_id)
            workflow_id = result.get("workflow_id")
            write_system_log("open_webui_request_completed", request_id=request_id, workflow_id=workflow_id, status=result.get("status"))
            self.send_json(200, openai_chat_response(payload, request_id, result))
        except json.JSONDecodeError:
            write_system_log("invalid_request", request_id=request_id, reason="invalid_json")
            self.send_json(400, {"error": {"message": "The request body must be valid JSON.", "type": "invalid_request_error"}})
        except (error.URLError, TimeoutError) as exc:
            write_system_log("orchestration_unavailable", request_id=request_id, error=str(exc))
            self.send_json(503, {"error": {"message": "Nexus orchestration is unavailable. Confirm CrewAI is running and try again.", "type": "service_unavailable"}})
        except Exception as exc:
            write_system_log("adapter_error", request_id=request_id, error=str(exc))
            self.send_json(500, {"error": {"message": "Nexus could not complete orchestration for this request.", "type": "server_error"}})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    write_system_log("service_started", port=SERVICE_PORT, crewai_url=CREWAI_URL, version=SERVICE_VERSION)
    server = ThreadingHTTPServer(("0.0.0.0", SERVICE_PORT), Handler)
    server.serve_forever()
