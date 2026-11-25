---
name: docker-model
description: >
  Use this skill when running local AI models with Docker Model Runner — the
  `docker model` CLI — e.g. "run an LLM locally with Docker", "pull a model
  from the ai/ namespace", "connect my app to a local model", "use a local
  model as backend for the Drupal AI module", or when wiring the `models:`
  top-level element into a compose.yaml. Covers pulling/running models,
  OpenAI-compatible endpoints, and Compose integration.
---

# Docker Model Runner Skill

Docker Model Runner (DMR) manages and serves AI models through Docker Desktop
or Docker Engine, exposing **OpenAI-compatible APIs**. Models are pulled as
OCI artifacts from Docker Hub (`ai/` namespace), any OCI registry, or
Hugging Face, and stored locally. For Drupal work it provides a free, local,
keyless backend for the AI module ecosystem during development.

---

## Enabling

- **Docker Desktop:** Settings → enable *Docker Model Runner* (Beta features).
- **Docker Engine (Linux):** supported without Desktop; models are served on
  the host. GPU support: NVIDIA (CUDA), AMD (ROCm), Vulkan; Apple Silicon on
  macOS; CPU everywhere.

---

## Core CLI

```bash
docker model status                      # is the runner active?
docker model pull ai/smollm2             # fetch a model (Docker Hub ai/ namespace)
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF  # from Hugging Face
docker model list                        # local models
docker model run ai/smollm2 "Hello"      # one-shot prompt
docker model run ai/smollm2              # interactive chat (exit with /bye)
docker model configure --context-size 8192 ai/smollm2   # adjust context window
docker model inspect ai/smollm2          # model metadata
docker model logs                        # runner logs
docker model rm ai/smollm2               # delete local model
```

Run `docker model --help` for the full, current command list — the CLI is
still evolving.

---

## OpenAI-compatible API

| Endpoint | Method |
|---|---|
| `/engines/v1/models` | GET |
| `/engines/v1/chat/completions` | POST |
| `/engines/v1/completions` | POST |
| `/engines/v1/embeddings` | POST |

Base URLs:

- **From the host:** `http://localhost:12434` (default TCP port)
- **From containers (Docker Desktop):** `http://model-runner.docker.internal`
- **From containers (Docker Engine):** `http://172.17.0.1:12434`

```bash
curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "ai/smollm2", "messages": [{"role": "user", "content": "Hi"}]}'
```

Any OpenAI SDK works by pointing `base_url` at
`http://localhost:12434/engines/v1` — no API key required.

---

## Compose integration — `models:` top-level element

Declare models next to services; Compose pulls and provisions them:

```yaml
services:
  app:
    image: my-app
    models:
      - llm                      # short syntax

models:
  llm:
    model: ai/smollm2
    context_size: 4096
    runtime_flags:
      - "--no-prefill-assistant"
```

Short syntax injects environment variables into the service container, named
after the model key: `LLM_URL` and `LLM_MODEL`. Long syntax picks your own
variable names:

```yaml
services:
  app:
    image: my-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME
```

---

## Using DMR as a Drupal AI backend

The Drupal **AI module** (`drupal/ai`) talks to providers over the OpenAI
API. Point an OpenAI-compatible provider (e.g. `drupal/ai_provider_openai`)
at the Model Runner endpoint to develop AI features without cloud keys:

- **Base URL** (Drupal in a container, Docker Desktop):
  `http://model-runner.docker.internal/engines/v1`
- **Base URL** (Drupal on the host): `http://localhost:12434/engines/v1`
- **API key:** any non-empty placeholder — DMR does not check it.
- **Model name:** exactly as listed by `docker model list` (e.g. `ai/smollm2`).

This gives local, reproducible AI development for content generation,
embeddings/search experiments, and automated tests without external costs.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `docker model: command not found` | Enable Model Runner in Docker Desktop settings, or install the plugin on Docker Engine |
| Connection refused on 12434 | Enable *host-side TCP support* in the Model Runner settings; check `docker model status` |
| Container cannot reach `model-runner.docker.internal` | On Docker Engine use `http://172.17.0.1:12434` instead |
| Responses truncated | Raise the context window: `docker model configure --context-size <n> <model>` |
| Model too slow / out of memory | Pull a smaller quantized variant from the `ai/` namespace; check GPU is actually used (`docker model logs`) |
