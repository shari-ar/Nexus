import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SERVICE_NAME = os.getenv("NEXUS_SERVICE_NAME", "nexus-service")
SERVICE_ROLE = os.getenv("NEXUS_SERVICE_ROLE", "Nexus development service")
SERVICE_VERSION = os.getenv("NEXUS_SERVICE_VERSION", "v0.1")
SERVICE_PORT = int(os.getenv("NEXUS_SERVICE_PORT", "8080"))
LOG_DIR = Path(os.getenv("NEXUS_LOG_DIR", "/var/log/nexus/system"))
STARTED_AT = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"{SERVICE_NAME}.log"


def write_log(event, **fields):
    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "service": SERVICE_NAME,
        "event": event,
        **fields,
    }
    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + "\n")


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if SERVICE_NAME == "vllm" and self.path == "/v1/models":
            payload = {"object": "list", "data": [{"id": "nexus-dev-placeholder", "object": "model", "owned_by": "nexus"}]}
            write_log("models_list", path=self.path, status="ok")
            self._send_json(200, payload)
            return

        if self.path in {"/", "/status", "/health"}:
            payload = {
                "status": "healthy",
                "service": SERVICE_NAME,
                "role": SERVICE_ROLE,
                "version": SERVICE_VERSION,
                "environment": os.getenv("NEXUS_ENV", "development"),
                "hostname": socket.gethostname(),
                "started_at": STARTED_AT,
            }
            write_log("health_check", path=self.path, status="healthy")
            self._send_json(200, payload)
            return

        write_log("not_found", path=self.path)
        self._send_json(404, {"status": "not_found", "service": SERVICE_NAME})


    def do_POST(self):
        if SERVICE_NAME == "vllm" and self.path == "/v1/chat/completions":
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length:
                self.rfile.read(content_length)
            payload = {
                "id": "chatcmpl-nexus-dev",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "nexus-dev-placeholder",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Nexus development mode is running. Open WebUI is connected to the local placeholder model endpoint.",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            }
            write_log("chat_completion", path=self.path, status="ok")
            self._send_json(200, payload)
            return

        write_log("post_not_found", path=self.path)
        self._send_json(404, {"status": "not_found", "service": SERVICE_NAME})

    def log_message(self, format, *args):
        write_log("http_access", message=format % args)


if __name__ == "__main__":
    write_log("service_started", role=SERVICE_ROLE, port=SERVICE_PORT, version=SERVICE_VERSION)
    server = ThreadingHTTPServer(("0.0.0.0", SERVICE_PORT), Handler)
    server.serve_forever()
