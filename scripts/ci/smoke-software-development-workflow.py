#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib import request

ROOT_DIR = Path(__file__).resolve().parents[2]
COMPOSE_FILES = ["-f", "docker/compose/docker-compose.yml", "-f", "docker/compose/docker-compose.dev.yml"]
PROMPT = "Implement a small code change for the Nexus software-development workflow smoke test."


def run(command):
    return subprocess.run(command, cwd=ROOT_DIR, check=True, text=True, capture_output=True)


def curl_json(url, payload=None):
    if payload is None:
        with request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    run(["docker", "compose", *COMPOSE_FILES, "--profile", "orchestration", "--profile", "engineering", "up", "-d", "--build", "crewai", "openhands"])
    try:
        for _ in range(20):
            try:
                crewai = curl_json("http://127.0.0.1:8081/health")
                openhands = curl_json("http://127.0.0.1:8082/health")
                if crewai.get("status") == "healthy" and openhands.get("status") == "healthy":
                    break
            except Exception:
                time.sleep(2)
        result = curl_json("http://127.0.0.1:8081/orchestrate", {"request": PROMPT, "source": "ci-smoke", "request_id": "ci-v0.8"})
        workflow_id = result["workflow_id"]
        artifact_path = result["delegated_result"].get("artifact_path")
        if result.get("workflow_type") != "software-development":
            raise AssertionError("workflow_type must be software-development")
        if result.get("delegation", {}).get("delegated_to") != "openhands":
            raise AssertionError("software-development workflow must delegate to OpenHands")
        checks = result.get("validation", {}).get("checks", {})
        for check_name in ["code_result_has_artifact", "code_result_has_generated_diff", "code_result_has_test_result", "code_result_has_final_summary"]:
            if checks.get(check_name) is not True:
                raise AssertionError(f"missing reviewer check: {check_name}")
        if not artifact_path:
            raise AssertionError("OpenHands artifact path missing")
        workflow_log = ROOT_DIR / "logs" / "workflows" / f"{workflow_id}.jsonl"
        aggregate_log = ROOT_DIR / "logs" / "workflows" / "aggregate" / "software-development.jsonl"
        host_artifact = ROOT_DIR / "data" / "generated" / "code" / workflow_id / "openhands-result.json"
        for expected_path in [workflow_log, aggregate_log, host_artifact]:
            if not expected_path.exists():
                raise AssertionError(f"expected path missing: {expected_path}")
        print(json.dumps({"status": "passed", "workflow_id": workflow_id, "artifact": str(host_artifact)}, sort_keys=True))
    finally:
        run(["docker", "compose", *COMPOSE_FILES, "stop", "crewai", "openhands"])


if __name__ == "__main__":
    raise SystemExit(main())
