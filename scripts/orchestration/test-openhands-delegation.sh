#!/usr/bin/env sh
set -eu

OPENHANDS_URL="${OPENHANDS_URL:-http://127.0.0.1:8082}"
WORKFLOW_ID="${1:-wf-openhands-smoke}"
INSTRUCTION="${2:-Prepare a minimal coding handoff artifact for the Nexus v0.7 smoke test.}"
PAYLOAD=$(WORKFLOW_ID="$WORKFLOW_ID" INSTRUCTION="$INSTRUCTION" python3 -c 'import json, os; print(json.dumps({"workflow_id": os.environ["WORKFLOW_ID"], "task_id": "coding-smoke", "instruction": os.environ["INSTRUCTION"], "workspace": os.environ["WORKFLOW_ID"], "repository": {"repository_path": "/projects", "workspace": os.environ["WORKFLOW_ID"]}}))')

curl --fail --silent --show-error \
  --header 'Content-Type: application/json' \
  --data "$PAYLOAD" \
  "$OPENHANDS_URL/delegate"
printf '\n'
