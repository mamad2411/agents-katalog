---
name: free-llm-rotation
description: >
  Configure and use free LLM providers with intelligent rotation and fallback. USE when:
  setting up ZeroClaw with free tiers, hitting rate limits, switching providers dynamically,
  comparing free model quality, configuring Ollama local fallback, or when the user says
  "use a free model", "I hit the rate limit", "switch to a cheaper model", "configure Ollama".
  Covers OpenRouter (26+ free), Groq (free tier), Ollama (local), Cerebras.
metadata:
  version: "1.0.0"
  category: "AI/Infrastructure"
  sources: ["openrouter.ai/models?q=free", "console.groq.com/docs/models", "ollama.com"]
---

# Skill: Free LLM Provider Rotation

## Free Provider Landscape (March 2026)

| Provider | Free Models | Speed | Rate Limit | Best For |
|----------|------------|-------|-----------|----------|
| **OpenRouter** | 26+ free models | Varies | Per-model | Variety, fallback |
| **Groq** | llama-3.1-8b, llama-3.3-70b | ~560-280 tps | 1K RPM | Speed, daily use |
| **Ollama** | Any local model | CPU: ~10 tps | None | Always-on fallback |
| **Cerebras** | Llama 3.3 70B | Very fast | Free tier | Quick tasks |

## Top Free Models on OpenRouter (March 2026)

| Model | Context | Speed | Best For |
|-------|---------|-------|----------|
| `openai/gpt-oss-120b:free` | 131K | ~500 tps | General, reasoning |
| `meta-llama/llama-4-scout-17b-16e-instruct:free` | 131K | ~750 tps | Fast tasks |
| `nvidia/nemotron-3-nano-30b-a3b:free` | 256K | Fast | Agent tasks |
| `arcee-ai/trinity-large-preview:free` | 128K | Medium | Creative, agent |
| `openai/gpt-oss-20b:free` | 131K | ~1000 tps | Ultra-fast |

## ZeroClaw Free Tier Configuration

```toml
# ~/.zeroclaw/config.toml

# Primary: OpenRouter (free tier)
# Set ZEROCLAW_API_KEY=<openrouter-key>
default_provider = "openrouter"
default_model    = "openai/gpt-oss-120b:free"

# Fallback chain: Groq → Ollama
[reliability]
fallback_providers = ["groq", "ollama"]
provider_retries   = 2

# Groq provider (set GROQ_API_KEY env var)
[model_providers.groq]
name     = "groq"
base_url = "https://api.groq.com/openai/v1"

# Ollama local (no API key, always free)
[model_providers.ollama]
name     = "ollama"
base_url = "http://127.0.0.1:11434"

# Model routes for manual control
[[model_routes]]
hint     = "fast"
provider = "groq"
model    = "llama-3.1-8b-instant"

[[model_routes]]
hint     = "local"
provider = "ollama"
model    = "llama3.2:3b"

[[model_routes]]
hint     = "smart"
provider = "openrouter"
model    = "openai/gpt-oss-120b:free"
```

## How to Get Free API Keys

### OpenRouter (primary — 26+ free models)
1. Go to https://openrouter.ai/
2. Sign up (GitHub login OK)
3. API Keys → Create key
4. Free models: filter by `$0/M tokens`
5. Usage: generous free tier, no credit card

### Groq (ultra-fast, free tier)
1. Go to https://console.groq.com/
2. Sign up → API Keys → Create
3. Free: 1K RPM, 30K RPD for most models
4. Set `GROQ_API_KEY=gsk_...`

### Cerebras (optional, very fast)
1. https://cloud.cerebras.ai/ → Sign up
2. Free tier available
3. Set `CEREBRAS_API_KEY=...`

## Ollama Management (local, always free)

```bash
# List installed models
ollama list

# Pull models (GPU-first, CPU fallback configured)
ollama pull llama3.2:3b      # 2GB — fast, good for general tasks
ollama pull qwen2.5-coder:7b # 4.7GB — best free code model
ollama pull nomic-embed-text # 274MB — embeddings (free!)

# Test GPU or CPU usage
ollama run llama3.2:3b "test" 2>&1 | head -5
journalctl -u ollama | grep "inference compute"
# GPU: "id=gpu0 library=cuda ..."
# CPU: "id=cpu library=cpu ..."

# Ollama API
curl http://127.0.0.1:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello",
  "stream": false
}'
```

## Rate Limit Handling

When you hit a rate limit (429 error):
1. ZeroClaw auto-falls to next provider in `fallback_providers`
2. If all cloud providers rate-limited → Ollama (local, no limit)

Manual routing:
```bash
# Force local model
zeroclaw agent -m "hint:local explain this code: ..."

# Force fast model  
zeroclaw agent -m "hint:fast summarize this document: ..."
```

## Inject API Keys via Infisical

```bash
# Store keys in Infisical (self-hosted)
infisical secrets set ZEROCLAW_API_KEY="or-..." --env=dev
infisical secrets set GROQ_API_KEY="gsk_..." --env=dev

# Run daemon with injected secrets
infisical run --env=dev -- zeroclaw daemon

# Verify
infisical secrets list --env=dev
```

## Model Selection Guide

```
Task type → Recommended model (free)

Code generation/review → openai/gpt-oss-120b:free OR groq:llama-3.1-8b-instant
Quick Q&A / routing → groq:llama-3.1-8b-instant (fastest)
Long document analysis → openai/gpt-oss-120b:free (131K context)
Always-available / offline → ollama:llama3.2:3b
Embeddings (RAG) → ollama:nomic-embed-text (free, local)
```
