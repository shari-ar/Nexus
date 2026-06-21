#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

mkdir -p \
  "$ROOT_DIR/data/uploads" \
  "$ROOT_DIR/data/projects" \
  "$ROOT_DIR/data/workspaces" \
  "$ROOT_DIR/data/generated/code" \
  "$ROOT_DIR/data/generated/documents" \
  "$ROOT_DIR/data/generated/images" \
  "$ROOT_DIR/data/generated/videos" \
  "$ROOT_DIR/data/generated/audio" \
  "$ROOT_DIR/data/archives" \
  "$ROOT_DIR/memory/knowledge" \
  "$ROOT_DIR/memory/embeddings" \
  "$ROOT_DIR/memory/conversations" \
  "$ROOT_DIR/memory/artifacts" \
  "$ROOT_DIR/logs/agents" \
  "$ROOT_DIR/logs/workflows" \
  "$ROOT_DIR/logs/models" \
  "$ROOT_DIR/logs/system"

printf 'Nexus development directories are ready.\n'
printf 'Data: %s\n' "$ROOT_DIR/data"
printf 'Memory: %s\n' "$ROOT_DIR/memory"
printf 'Logs: %s\n' "$ROOT_DIR/logs"

if [ "${NEXUS_SKIP_CONFIG_VALIDATION:-0}" != "1" ]; then
  python3 "$ROOT_DIR/scripts/validation/validate-agent-configs.py"
fi
