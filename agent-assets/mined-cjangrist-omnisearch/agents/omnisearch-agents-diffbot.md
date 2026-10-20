# AGENTS.md — src/providers/fetch/diffbot/

## Purpose
Diffbot Article API URL fetcher. Returns structured article extraction with rich metadata (author, date, images). Tier 2 parallel race (with `olostep`).

## Vendor

- **Vendor**: Diffbot
- **Endpoint**: `POST https://api.diffbot.com/v3/article`
- **Auth**: query param `token=<DIFFBOT_TOKEN>`
- **Env var**: `DIFFBOT_TOKEN` (note: `DIFFBOT_TOKEN`, not `DIFFBOT_API_KEY`)
- **Returns**: `FetchResult`. Title from `objects[0].title`. Content is the article `text`. Metadata: `author`, `date`, `siteName`, `images`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ objects: [{ title, text, html, author, date, siteName, images }] }`. Single-element array; we take object 0.
- Returns `text` (not `html`) — already plain text, ready for LLM consumption.

## Related

- Registered as `diffbot` in `../../unified/fetch.ts`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
