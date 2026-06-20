---
permalink: /docs/deployment/vllm-local-model-serving/
title: vLLM Local Model Serving
---

# vLLM Local Model Serving

Nexus uses vLLM as the local OpenAI-compatible model server. The development stack exposes the vLLM API on `http://localhost:${VLLM_PORT:-8083}` and connects Open WebUI to `http://vllm:8000/v1` inside Docker.

## Configuration

Set these values in `.env` before starting the model service:

| Variable | Purpose | Default |
| --- | --- | --- |
| `VLLM_IMAGE` | vLLM Docker image repository. | `vllm/vllm-openai-cpu` |
| `VLLM_IMAGE_TAG` | vLLM Docker image tag. | `latest-x86_64` |
| `VLLM_PORT` | Host port for the OpenAI-compatible API. | `8083` |
| `VLLM_MODEL_NAME` | Served model name returned by `/v1/models`. | `nexus-local` |
| `VLLM_MODEL_PATH` | Hugging Face model ID or local model path. | `Qwen/Qwen2.5-0.5B-Instruct` |
| `VLLM_TENSOR_PARALLEL_SIZE` | Number of GPU partitions for tensor parallel serving. | `1` |
| `VLLM_MAX_MODEL_LEN` | Maximum model context length used in development. | `2048` |
| `VLLM_DTYPE` | Runtime dtype used by the selected vLLM image. | `auto` |
| `VLLM_CPU_KVCACHE_SPACE` | CPU KV cache size in GiB for CPU images. | `4` |
| `VLLM_GPU_MEMORY_UTILIZATION` | Fraction of GPU memory available to vLLM. | `0.90` |

## CPU And GPU Expectations

The default profile uses the official vLLM CPU image with a small instruction model to keep local development practical. GPU execution is the preferred path for higher throughput. Use a CUDA-capable NVIDIA GPU with enough VRAM for the selected model, installed NVIDIA drivers, and the NVIDIA Container Toolkit when enabling the GPU override.

For GPU development, start Compose with the GPU file:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  -f docker/compose/docker-compose.gpu.yml \
  --profile models up -d vllm
```

CPU-only development uses `vllm/vllm-openai-cpu:latest-x86_64` by default on x86_64 hosts. Set `VLLM_IMAGE` and `VLLM_IMAGE_TAG` for another CPU architecture or a custom CPU build.

## Model Profiles

Model profiles live in `configs/models/`:

| File | Capability |
| --- | --- |
| `configs/models/reasoning.yaml` | Planning, analysis, summarization, and general chat. |
| `configs/models/coding.yaml` | Code generation, code review, test generation, and debugging. |
| `configs/models/routing.yaml` | Capability-to-profile routing contract. |

## Verification

Start the model service and check health:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile models up -d vllm

docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  ps vllm

curl -fsS http://localhost:${VLLM_PORT:-8083}/health
curl -fsS http://localhost:${VLLM_PORT:-8083}/v1/models
```

Run a test prompt:

```bash
./scripts/models/test-vllm-prompt.sh "Reply with one sentence confirming Nexus vLLM is ready."
```

Confirm startup and request logs:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  logs vllm > logs/models/vllm-startup.log

ls -la logs/models/
```

## Official References

- vLLM OpenAI-compatible server documentation: `https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html`
- vLLM Docker deployment documentation: `https://docs.vllm.ai/en/latest/deployment/docker.html`
- vLLM CPU installation documentation: `https://docs.vllm.ai/en/latest/getting_started/installation/cpu.html`
