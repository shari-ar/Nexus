import json
import os
import socket
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

SERVICE_NAME = os.getenv("NEXUS_SERVICE_NAME", "openhands")
SERVICE_VERSION = os.getenv("NEXUS_SERVICE_VERSION", "v0.7")
SERVICE_PORT = int(os.getenv("NEXUS_SERVICE_PORT", "8080"))
NEXUS_ENV = os.getenv("NEXUS_ENV", "development")
WORKSPACE_ROOT = Path(os.getenv("OPENHANDS_WORKSPACE_ROOT", "/workspaces")).resolve()
PROJECTS_ROOT = Path(os.getenv("OPENHANDS_PROJECTS_ROOT", "/projects")).resolve()
GENERATED_CODE_ROOT = Path(os.getenv("OPENHANDS_GENERATED_CODE_ROOT", "/generated/code")).resolve()
AGENT_LOG_DIR = Path(os.getenv("NEXUS_AGENT_LOG_DIR", "/var/log/nexus/agents"))
STARTED_AT = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

for runtime_dir in (WORKSPACE_ROOT, PROJECTS_ROOT, GENERATED_CODE_ROOT, AGENT_LOG_DIR):
    runtime_dir.mkdir(parents=True, exist_ok=True)


def utc_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_agent_log(event, **fields):
    payload = {
        "timestamp": utc_timestamp(),
        "service": SERVICE_NAME,
        "agent": "openhands",
        "event": event,
        **fields,
    }
    with (AGENT_LOG_DIR / "openhands.jsonl").open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + "\n")


def is_within(path, root):
    try:
        path.resolve().relative_to(root)
        return True
    except ValueError:
        return False


def validate_workspace(workspace):
    workspace_path = (WORKSPACE_ROOT / workspace).resolve()
    if not is_within(workspace_path, WORKSPACE_ROOT):
        raise ValueError("Workspace must stay inside the OpenHands workspace root.")
    workspace_path.mkdir(parents=True, exist_ok=True)
    return workspace_path


def delegate(payload):
    workflow_id = payload.get("workflow_id") or f"wf-{uuid.uuid4().hex[:12]}"
    task_id = payload.get("task_id") or f"task-{uuid.uuid4().hex[:12]}"
    instruction = str(payload.get("instruction") or payload.get("request") or "Prepare a coding task summary.").strip()
    repository = payload.get("repository", {})
    workspace_name = payload.get("workspace") or workflow_id
    workspace_path = validate_workspace(workspace_name)
    artifact_dir = (GENERATED_CODE_ROOT / workflow_id).resolve()
    if not is_within(artifact_dir, GENERATED_CODE_ROOT):
        raise ValueError("Generated code artifact path must stay inside the generated code root.")
    artifact_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "workflow_id": workflow_id,
        "task_id": task_id,
        "status": "completed",
        "subsystem": "openhands",
        "repository": repository,
        "workspace_path": str(workspace_path),
        "summary": "OpenHands received the delegated software-development task and prepared a controlled engineering handoff artifact.",
        "generated_diff": "No source diff generated in v0.7; this milestone verifies delegation boundaries and artifact flow.",
        "test_result": "not_run_v0.7_placeholder",
        "final_summary": f"Delegated coding instruction accepted: {instruction[:240]}",
    }
    artifact_path = artifact_dir / "openhands-result.json"
    artifact_path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    result["artifact_path"] = str(artifact_path)

    write_agent_log(
        "openhands_task_received",
        workflow_id=workflow_id,
        task_id=task_id,
        workspace_path=str(workspace_path),
        artifact_path=str(artifact_path),
    )
    write_agent_log("openhands_task_completed", workflow_id=workflow_id, task_id=task_id, status="completed")
    return result


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
            self.send_json(
                200,
                {
                    "status": "healthy",
                    "service": SERVICE_NAME,
                    "version": SERVICE_VERSION,
                    "environment": NEXUS_ENV,
                    "hostname": socket.gethostname(),
                    "started_at": STARTED_AT,
                    "workspace_root": str(WORKSPACE_ROOT),
                    "projects_root": str(PROJECTS_ROOT),
                    "generated_code_root": str(GENERATED_CODE_ROOT),
                },
            )
            return
        self.send_json(404, {"status": "not_found", "service": SERVICE_NAME})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/delegate":
            self.send_json(404, {"status": "not_found", "service": SERVICE_NAME})
            return
        try:
            self.send_json(200, delegate(self.read_json()))
        except json.JSONDecodeError:
            self.send_json(400, {"status": "invalid_json", "message": "Request body must be valid JSON."})
        except ValueError as exc:
            self.send_json(400, {"status": "invalid_request", "message": str(exc)})
        except Exception as exc:
            self.send_json(500, {"status": "error", "message": str(exc)})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    write_agent_log("service_started", port=SERVICE_PORT, version=SERVICE_VERSION)
    server = ThreadingHTTPServer(("0.0.0.0", SERVICE_PORT), Handler)
    server.serve_forever()
