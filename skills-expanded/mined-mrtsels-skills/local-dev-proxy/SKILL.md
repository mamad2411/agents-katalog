---
name: local-dev-proxy
description: Set up a local development reverse proxy for a static frontend SPA that needs to proxy /api/ calls to a separate backend server (Spring Boot, Express, etc.)
---

# Local Dev Proxy Setup

Use when the frontend (served by a simple static file server) needs to call a backend API on a different port, and you need same-origin requests without CORS complications.

## The Problem

- Frontend served by `python3 -m http.server :3000`
- Backend API on `:8080`
- Frontend makes `fetch('/api/...')` → hits the static server (501 Unsupported Method)
- Setting `API='http://localhost:8080/api'` requires CORS and adds preflight overhead

## The Solution: Python Reverse Proxy

A single Python script replaces the plain http.server and proxies `/api/` requests to the backend.

### Step-by-step

1. Create `dev_proxy.py` in the project root (template below)
2. Kill any old `python3 -m http.server` on the port
3. Run: `python3 dev_proxy.py`
4. Access the app at `http://localhost:3000/`

### Key Behaviors

- **GET** requests for non-`/api/` paths → served as static files from the project root (same as `http.server`)
- **Any method** (GET/POST/PUT/DELETE/PATCH) on `/api/` paths → forwarded to `BACKEND` URL
- **OPTIONS** on `/api/` → returns 204 with CORS headers (for preflight when needed)
- **HTTP errors** from backend (4xx/5xx) → proxied through, not swallowed
- **Root path** → serves `index.html` automatically

### Pitfalls

- **Empty database**: Docker MySQL containers may restart without persisting data. If tables exist but are empty, import init.sql in-place (DO NOT restart the container): `docker exec -i <container> bash -c "mysql -uroot -p<PASS> --default-character-set=utf8mb4 <DB>" < init.sql`
- **Port already in use**: Kill stale processes with `lsof -ti:3000 | xargs kill -9`
- **Background process**: Use `terminal(background=true)` to start the proxy, then verify with `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/index.html`
- **Default credentials**: Not documented in README — test with curl against the login endpoint to discover them if unknown. Common patterns: `admin/admin123`, `jinpeng/jinpeng123`
- **Script encoding**: Ensure init.sql uses `utf8mb4` — MySQL Chinese import may garble without `--default-character-set=utf8mb4`
- **`docker-compose` vs `docker compose`**: macOS may have both installed. `docker compose version` succeeds but lifecycle commands (stop, rm, up) may fail with "unknown command: docker compose". Prefer `docker-compose` (with hyphen) on systems where the compose plugin is not registered as a docker subcommand.
**⚠️ `ai-config.json` overrides env vars**: If the backend container has an `uploads/ai-config.json` with empty strings (like `"baseUrl": ""`), those override correctly-set environment variables. Fix: write correct values to the file in-container, then `docker restart backend` to re-trigger `@PostConstruct init()`.

**⚠️ `ai-config.json` fields must stay in sync**: The file has three critical fields — `baseUrl`, `model`, `apiKey` — and all three must match the env vars in docker-compose.yml. A stale `model` in the JSON file will override the env var even when URL and key are correct. After updating docker-compose.yml, always update the in-container `ai-config.json` (via `docker cp` or `docker exec`) and restart.

### Spring Boot AI Vision Config for OCR

When the dev proxy backend is a Spring Boot app that needs OCR (vision LLM calls), add these env vars to `docker-compose.yml` under the backend service:

```yaml
environment:
  AI_VISION_URL: https://dashscope.aliyuncs.com/compatible-mode/v1
  AI_VISION_MODEL: qwen3-vl-plus  # or qwen-vl-max, but prefer qwen3-vl-plus for better OCR accuracy
  AI_VISION_APIKEY: your-dashscope-api-key
```

**⚠️ CRITICAL: Use the RIGHT provider for OCR.** DeepSeek does NOT support document/vision OCR. The OCR system expects a vision-capable LLM API that accepts base64 images in OpenAI-compatible format. Always use **DashScope (Alibaba Cloud Qwen-VL)** for document OCR. The service sends `POST {baseUrl}/chat/completions` with `type: image_url` payloads — DashScope's compatible-mode endpoint is `https://dashscope.aliyuncs.com/compatible-mode/v1`.

**⚠️ Env var name mismatch pitfall:** The deployment docker-compose at `deployment/docker/docker-compose.yml` uses `AI_VISION_KEY` as the env var name, but Spring Boot's `@ConfigurationProperties(prefix = "ai.vision")` with field `apiKey` expects `AI_VISION_APIKEY` (relaxed binding from `ai.vision.api-key`). `AI_VISION_KEY` does NOT match. Always use `AI_VISION_APIKEY` in root docker-compose.yml.

The `application.yml` maps these as:
- `AI_VISION_URL` → `ai.vision.base-url`
- `AI_VISION_MODEL` → `ai.vision.model`
- `AI_VISION_APIKEY` → `ai.vision.api-key`

The OCR service calls `POST {baseUrl}/chat/completions` with a standard OpenAI-compatible request (system prompt + base64 image). Any vision-capable LLM API that follows OpenAI's chat completions format works.

**To apply new env vars to a running Docker container:**
```bash
docker-compose stop backend
docker-compose rm -f backend    # removes the container (not the image)
docker-compose up -d backend    # creates a new container with new env vars
```

**If `ai-config.json` exists in the container:** After writing correct values to it, restart the backend to trigger `@PostConstruct init()` which re-reads the file:
```bash
docker restart enterprise-mvp-backend
```

## Template

Use the template at `templates/dev_proxy.py` — copy it to the project root, adjust `BACKEND` and `FRONTEND_DIR` as needed.
