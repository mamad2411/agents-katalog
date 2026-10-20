# AGENTS.md — src/providers/fetch/supadata/

## Purpose
Supadata YouTube transcript fetcher. Domain breaker for `youtube.com` / `youtu.be` URLs. Uses `mode=auto`: tries native captions first, falls back to AI-generated transcripts. Supports both sync and async (HTTP 202 + polling) responses depending on video length.

## Vendor

- **Vendor**: Supadata
- **Endpoint**: `https://api.supadata.ai/v1/transcript` (sync) and `/v1/transcript/{job_id}` (async polling)
- **Auth**: `x-api-key: <SUPADATA_API_KEY>`
- **Env var**: `SUPADATA_API_KEY`
- **Returns**: `FetchResult` — content is the full transcript text; metadata includes `lang`, `availableLangs`.
- **Per-provider timeout**: 60000ms (longer than default; transcripts can take a while).

## Conventions / Invariants

- Implements `FetchProvider`.
- `extract_video_id(url)` parses YouTube URL shapes: `youtu.be/<id>`, `youtube.com/watch?v=<id>`, `youtube.com/embed/<id>`, `youtube.com/shorts/<id>`, `youtube.com/live/<id>`.
- Sync path: response is `{ content, lang, availableLangs }`.
- Async path: HTTP 202 with `{ jobId }`; we poll `GET /v1/transcript/<jobId>` until `status === 'completed'` (or `'failed'`).
- `poll_job(api_key, job_id, timeout_ms)` enforces an overall deadline and exponential backoff between polls.
- API-native provider — exempt from the orchestrator's 200-char + challenge-pattern failure check (`API_NATIVE_PROVIDERS = ['github', 'supadata']`).

## Gotchas

- **Async polling**: long videos return HTTP 202 with a job ID. The provider polls until completion or timeout. The outer fetch deadline still applies.
- **`mode=auto`**: tries native captions first (free) and falls back to AI-generated (paid). No way to force one mode from this provider.

## Related

- Registered as `supadata` in `../../unified/fetch.ts`.
- Domain breaker in `../../../server/fetch_orchestrator.ts CONFIG.breakers.youtube` — runs BEFORE the social_media breaker.
