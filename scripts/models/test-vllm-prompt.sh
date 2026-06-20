#!/usr/bin/env sh
set -eu

VLLM_HOST="${VLLM_HOST:-127.0.0.1}"
VLLM_PORT="${VLLM_PORT:-8083}"
VLLM_MODEL_NAME="${VLLM_MODEL_NAME:-nexus-local}"
PROMPT="${*:-Say hello from the Nexus local model server in one sentence.}"
ENDPOINT="http://${VLLM_HOST}:${VLLM_PORT}/v1/chat/completions"

command -v curl >/dev/null 2>&1 || {
  echo "curl is required to run the vLLM test prompt." >&2
  exit 1
}

command -v python3 >/dev/null 2>&1 || {
  echo "python3 is required to parse the vLLM test response." >&2
  exit 1
}

PAYLOAD="$(PROMPT="$PROMPT" VLLM_MODEL_NAME="$VLLM_MODEL_NAME" python3 -c 'import json, os; print(json.dumps({"model": os.environ["VLLM_MODEL_NAME"], "messages": [{"role": "user", "content": os.environ["PROMPT"]}], "temperature": 0.2, "max_tokens": 128}))')"
RESPONSE="$(curl -fsS "$ENDPOINT" -H "Content-Type: application/json" -d "$PAYLOAD")"

printf '%s\n' "$RESPONSE" | python3 -c 'import json, sys; data=json.load(sys.stdin); print(data["choices"][0]["message"]["content"])'
