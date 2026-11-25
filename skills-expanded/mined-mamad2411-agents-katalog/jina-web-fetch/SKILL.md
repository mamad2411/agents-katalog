---
name: jina-web-fetch
version: 1.0.0
license: MIT
description: Fetch webpage text with a normal HTTP request first, then automatically fall back to jina.ai proxy when direct access fails or returns login/JS-blocked content. Use when extracting content from X (Twitter) or other pages that are hard to read directly.
---

# Jina Web Fetch

Use this skill to capture content from hard-to-fetch pages while keeping a deterministic workflow:

1. Try direct fetch first.
2. If direct fetch fails or looks blocked, retry via `jina.ai`.

## Quick Start

```bash
bash "<path-to-skill>/scripts/fetch_with_jina_fallback.sh" "<url>" "<output_file>"
```

Example:

```bash
bash "<path-to-skill>/scripts/fetch_with_jina_fallback.sh" \
  "https://x.com/trq212/status/2027463795355095314" \
  "raw/x-status.txt"
```

The script prints `source=direct` or `source=jina` to `stderr` so you can see which path was used.

If `output_file` is omitted, content is printed to `stdout`.

## Default Workflow

1. Run the script with the target URL.
2. Save raw output under a traceable path like `raw/<slug>.txt`.
3. Parse extracted text/markdown for:
   - main body
   - media links (images/videos)
   - referenced URLs
4. Keep original URL + raw capture together for auditability.

## Blocking Heuristics

The script auto-falls back to `jina.ai` when direct content looks like:

- login wall / sign-up prompt
- JS-required page
- anti-bot / captcha / access denied page
- very small shell-like HTML page (default threshold `< 800` bytes)

## Environment Knobs

- `FETCH_TIMEOUT` (default `25`)
- `FETCH_CONNECT_TIMEOUT` (default `10`)
- `FETCH_MIN_BYTES` (default `800`)
- `JINA_FORCE=1` to skip direct fetch and always use `jina.ai`

## URL Format Note

Fallback URL is built as:
`https://r.jina.ai/http://<original-host-and-path>`
