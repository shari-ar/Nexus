#!/usr/bin/env sh
set -eu

ADAPTER_URL="${OPEN_WEBUI_ADAPTER_URL:-http://127.0.0.1:8084}"
MODEL_ID="${OPEN_WEBUI_ADAPTER_MODEL_ID:-nexus-crewai}"
PROMPT="${1:-Run the documented Nexus v0.5 Open WebUI to CrewAI smoke test.}"
PAYLOAD=$(PROMPT="$PROMPT" MODEL_ID="$MODEL_ID" python3 -c 'import json, os; print(json.dumps({"model": os.environ["MODEL_ID"], "messages": [{"role": "user", "content": os.environ["PROMPT"]}]}))')

curl --fail --silent --show-error \
  --header 'Content-Type: application/json' \
  --data "$PAYLOAD" \
  "$ADAPTER_URL/v1/chat/completions"
printf '\n'
