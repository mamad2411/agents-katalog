---
name: better-openclaw
description: "Generate and manage Docker Compose stacks via the better-openclaw API"
metadata:
  openclaw:
    emoji: "🦞"
---

# better-openclaw Skill

Use this skill to generate Docker Compose stacks via the better-openclaw API. The API returns complete `docker-compose.yml`, `.env`, reverse proxy configs, and OpenClaw skill files ready to deploy.

## API Base URL

- **Web API**: `https://better-openclaw.dev/api`
- **Standalone API**: `https://api.better-openclaw.dev/api/v1` (or configured `API_URL`)

## Generate a Stack

POST to `/generate` (web) or `/api/v1/generate` (standalone):

```bash
curl -X POST "https://better-openclaw.dev/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "my-stack",
    "services": ["ollama", "qdrant", "n8n"],
    "skillPacks": ["ollama-local-llm", "qdrant-memory", "n8n-trigger"],
    "proxy": "caddy",
    "domain": "example.local",
    "monitoring": true
  }'
```

## List Services

GET available services (standalone API only):

```bash
curl "https://api.better-openclaw.dev/api/v1/services"
curl "https://api.better-openclaw.dev/api/v1/services?category=ai"
```

## List Skill Packs

```bash
curl "https://api.better-openclaw.dev/api/v1/skills"
curl "https://api.better-openclaw.dev/api/v1/skills?services=ollama,qdrant"
```

## Validate Before Generation

Validate a stack configuration without generating files:

```bash
curl -X POST "https://api.better-openclaw.dev/api/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "services": ["ollama", "qdrant"],
    "skillPacks": ["ollama-local-llm"],
    "gpu": false
  }'
```

## Generate Request Schema

| Field | Type | Description |
|-------|------|-------------|
| projectName | string | Output directory / project name |
| services | string[] | Service IDs (e.g. ollama, qdrant, n8n, minio) |
| skillPacks | string[] | Skill pack IDs (optional) |
| proxy | string | none, caddy, traefik |
| domain | string | Domain for auto-SSL (optional) |
| gpu | boolean | Enable GPU for AI services |
| monitoring | boolean | Add Grafana + Prometheus |
| platform | string | linux/amd64 or linux/arm64 |
| deployment | string | local, vps, homelab |

## Common Service IDs

- **AI**: ollama, whisper
- **Vector DB**: qdrant, chromadb, weaviate
- **Automation**: n8n
- **Storage**: minio, redis, postgresql
- **Proxy**: caddy, traefik
- **Media**: ffmpeg, remotion

## Tips for AI Agents

- Always include required dependencies: e.g. n8n adds postgresql automatically.
- Use `validate` before `generate` to catch port conflicts and config errors.
- The response contains a `files` object: keys are paths, values are file contents.
- Skill packs require their backing services (e.g. ollama-local-llm requires ollama).
- For homelab/VPS deployments, set `proxy: "caddy"` or `traefik` and provide `domain`.
