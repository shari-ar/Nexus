#!/usr/bin/env sh
set -eu

CREWAI_URL="${CREWAI_URL:-http://127.0.0.1:8081}"
REQUEST_TEXT="${1:-Plan a simple Nexus v0.4 orchestration smoke test.}"
REQUEST_JSON=$(python3 -c 'import json,sys; print(json.dumps({"request": sys.argv[1]}))' "$REQUEST_TEXT")

curl --fail --silent --show-error \
  --header 'Content-Type: application/json' \
  --data "$REQUEST_JSON" \
  "$CREWAI_URL/orchestrate"
printf '\n'
