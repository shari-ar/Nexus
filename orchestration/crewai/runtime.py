import json
import os
import socket
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

SERVICE_NAME = os.getenv("NEXUS_SERVICE_NAME", "crewai")
SERVICE_ROLE = os.getenv("NEXUS_SERVICE_ROLE", "Orchestration runtime")
SERVICE_VERSION = os.getenv("NEXUS_SERVICE_VERSION", "v0.4")
SERVICE_PORT = int(os.getenv("NEXUS_SERVICE_PORT", "8080"))
NEXUS_ENV = os.getenv("NEXUS_ENV", "development")
CONFIG_DIR = Path(os.getenv("NEXUS_CONFIG_DIR", "/app/configs"))
PROMPT_DIR = Path(os.getenv("NEXUS_PROMPT_DIR", "/app/prompts"))
WORKFLOW_LOG_DIR = Path(os.getenv("NEXUS_WORKFLOW_LOG_DIR", "/var/log/nexus/workflows"))
AGENT_LOG_DIR = Path(os.getenv("NEXUS_AGENT_LOG_DIR", "/var/log/nexus/agents"))
WORKSPACE_DIR = Path(os.getenv("NEXUS_WORKSPACE_DIR", "/workspaces"))
STARTED_AT = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

for runtime_dir in (WORKFLOW_LOG_DIR, AGENT_LOG_DIR, WORKSPACE_DIR):
    runtime_dir.mkdir(parents=True, exist_ok=True)



def load_agent_config(agent_id):
    config_path = CONFIG_DIR / "agents" / f"{agent_id}.yaml"
    if not config_path.exists():
        return {"id": agent_id, "config_path": str(config_path), "loaded": False}
    role = "unknown"
    model_profile = "unknown"
    permission_policy = "unknown"
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("role:"):
            role = stripped.split(":", 1)[1].strip()
        if stripped.startswith("model_profile:"):
            model_profile = stripped.split(":", 1)[1].strip()
        if stripped.startswith("permission_policy:"):
            permission_policy = stripped.split(":", 1)[1].strip()
    return {
        "id": agent_id,
        "config_path": str(config_path),
        "loaded": True,
        "role": role,
        "model_profile": model_profile,
        "permission_policy": permission_policy,
    }


def load_core_agent_configs():
    return {agent_id: load_agent_config(agent_id) for agent_id in ["supervisor", "planner", "reviewer"]}

def utc_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_jsonl(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + "\n")


def log_workflow(workflow_id, event, **fields):
    write_jsonl(
        WORKFLOW_LOG_DIR / f"{workflow_id}.jsonl",
        {
            "timestamp": utc_timestamp(),
            "service": SERVICE_NAME,
            "workflow_id": workflow_id,
            "event": event,
            **fields,
        },
    )


def log_agent(agent_id, event, workflow_id, **fields):
    write_jsonl(
        AGENT_LOG_DIR / f"{agent_id}.jsonl",
        {
            "timestamp": utc_timestamp(),
            "service": SERVICE_NAME,
            "agent": agent_id,
            "workflow_id": workflow_id,
            "event": event,
            **fields,
        },
    )


def build_plan():
    return [
        {
            "step": 1,
            "stage": "intake",
            "owner": "supervisor",
            "action": "Accept and summarize the user request.",
            "observable_result": "The orchestration response includes the accepted request summary.",
        },
        {
            "step": 2,
            "stage": "plan",
            "owner": "planner",
            "action": "Create a short measurable execution plan.",
            "observable_result": "The orchestration response includes ordered plan items.",
        },
        {
            "step": 3,
            "stage": "delegate",
            "owner": "placeholder_delegate",
            "action": "Complete a placeholder delegated task for v0.4 runtime verification.",
            "observable_result": "The response includes delegated task status and a workspace artifact path.",
        },
        {
            "step": 4,
            "stage": "validate",
            "owner": "reviewer",
            "action": "Validate lifecycle events, delegation boundary, and response readiness.",
            "observable_result": "The response includes reviewer approval and structured check results.",
        },
        {
            "step": 5,
            "stage": "respond",
            "owner": "supervisor",
            "action": "Return the final orchestration response.",
            "observable_result": "The terminal output shows a completed workflow response.",
        },
    ]


def create_placeholder_artifact(workflow_id, request_summary):
    workspace = WORKSPACE_DIR / workflow_id
    workspace.mkdir(parents=True, exist_ok=True)
    artifact = workspace / "placeholder-result.json"
    payload = {
        "workflow_id": workflow_id,
        "status": "completed",
        "request_summary": request_summary,
        "message": "The placeholder delegate completed the v0.4 orchestration runtime check.",
    }
    artifact.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return artifact


def orchestrate(request_text, source="direct", request_id=None):
    workflow_id = f"wf-{uuid.uuid4().hex[:12]}"
    request_summary = " ".join(request_text.strip().split())[:500]
    if not request_summary:
        request_summary = "Run the Nexus v0.4 orchestration smoke test."

    selected_agents = load_core_agent_configs()
    log_workflow(workflow_id, "workflow_created", request=request_summary, environment=NEXUS_ENV, source=source, request_id=request_id, selected_agents=selected_agents)
    log_agent("supervisor", "intake_received", workflow_id, request=request_summary, source=source, request_id=request_id, config=selected_agents["supervisor"])

    plan = build_plan()
    acceptance_criteria = [
        "A workflow ID is returned to the caller.",
        "Workflow logs include created, planned, delegated, validated, and completed events.",
        "Agent logs include supervisor, planner, and reviewer events.",
        "The supervisor records delegation instead of executing the domain task directly.",
    ]
    log_workflow(workflow_id, "plan_created", plan=plan, acceptance_criteria=acceptance_criteria)
    log_agent("planner", "plan_created", workflow_id, steps=len(plan), acceptance_criteria=acceptance_criteria, config=selected_agents["planner"])

    delegation = {
        "delegated_by": "supervisor",
        "delegated_to": "placeholder_delegate",
        "task": "Return a measurable placeholder result for the orchestration lifecycle.",
        "reason": "v0.4 verifies orchestration boundaries before domain executors are connected.",
        "direct_domain_execution_by_supervisor": False,
    }
    log_workflow(workflow_id, "delegation_decision", delegation=delegation)
    log_agent("supervisor", "delegation_decision", workflow_id, delegation=delegation)

    artifact = create_placeholder_artifact(workflow_id, request_summary)
    placeholder_result = {
        "status": "completed",
        "artifact_path": str(artifact),
        "message": "Placeholder delegate completed successfully.",
    }
    log_workflow(workflow_id, "placeholder_task_completed", result=placeholder_result)

    validation = {
        "approved": True,
        "checks": {
            "workflow_id_present": True,
            "plan_present": True,
            "delegation_logged": True,
            "supervisor_direct_domain_execution": False,
            "response_ready": True,
        },
        "findings": [],
    }
    log_workflow(workflow_id, "validation_completed", validation=validation)
    log_agent("reviewer", "validation_completed", workflow_id, validation=validation, config=selected_agents["reviewer"])

    response = {
        "summary": "Nexus v0.4 accepted the request, created a plan, delegated a placeholder task, validated the result, and completed the workflow.",
        "verification": {
            "workflow_log": str(WORKFLOW_LOG_DIR / f"{workflow_id}.jsonl"),
            "agent_logs": [
                str(AGENT_LOG_DIR / "supervisor.jsonl"),
                str(AGENT_LOG_DIR / "planner.jsonl"),
                str(AGENT_LOG_DIR / "reviewer.jsonl"),
            ],
            "workspace_artifact": str(artifact),
        },
    }
    log_workflow(workflow_id, "workflow_completed", status="completed", response=response)
    log_agent("supervisor", "workflow_completed", workflow_id, status="completed")

    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "request": request_summary,
        "source": source,
        "request_id": request_id,
        "plan": plan,
        "acceptance_criteria": acceptance_criteria,
        "delegation": delegation,
        "placeholder_result": placeholder_result,
        "validation": validation,
        "selected_agents": selected_agents,
        "response": response,
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
        raw_body = self.rfile.read(content_length).decode("utf-8")
        return json.loads(raw_body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in {"/", "/health", "/status"}:
            self.send_json(
                200,
                {
                    "status": "healthy",
                    "service": SERVICE_NAME,
                    "role": SERVICE_ROLE,
                    "version": SERVICE_VERSION,
                    "environment": NEXUS_ENV,
                    "hostname": socket.gethostname(),
                    "started_at": STARTED_AT,
                    "config_dir_present": CONFIG_DIR.exists(),
                    "prompt_dir_present": PROMPT_DIR.exists(),
                    "workspace_dir_present": WORKSPACE_DIR.exists(),
                    "workflow_log_dir": str(WORKFLOW_LOG_DIR),
                    "agent_log_dir": str(AGENT_LOG_DIR),
                    "core_agents": load_core_agent_configs(),
                },
            )
            return
        self.send_json(404, {"status": "not_found", "service": SERVICE_NAME})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/orchestrate":
            self.send_json(404, {"status": "not_found", "service": SERVICE_NAME})
            return
        try:
            payload = self.read_json()
            result = orchestrate(payload.get("request", ""), payload.get("source", "direct"), payload.get("request_id") or self.headers.get("X-Nexus-Request-ID"))
            self.send_json(200, result)
        except json.JSONDecodeError:
            self.send_json(400, {"status": "invalid_json", "message": "Request body must be valid JSON."})
        except Exception as exc:
            self.send_json(500, {"status": "error", "message": str(exc)})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", SERVICE_PORT), Handler)
    server.serve_forever()
