---
name: web-search
description: "Live web discovery via `web.search` and `web.fetch`. Use when the task needs current internet search results or readable page retrieval."
---

# web-search

Use this skill for live web discovery and page retrieval.

Tool methods:
- `web.search`
- `web.fetch`

Input checklist for `web.search`:
1. `query` (required)
2. optional `count` (1..20)
3. optional `lang` (for example `en`, `ru`)
4. optional `country` (for example `us`, `gb`)
5. optional `freshness` (`pd`, `pw`, `pm`, `py`)

Input checklist for `web.fetch`:
1. `url` (required, only http/https)
2. optional `format` (`text` or `markdown`)
3. optional limits: `max_chars`, `max_bytes`

API key:
- `web.search` requires `AFKBOT_BRAVE_API_KEY`.

Safety:
- Respect network allowlist policy.
- Prefer concise `count` and strict freshness filters to limit noisy results.
- Do not return secrets/tokens from fetched pages.
- Runtime routes the correct skill automatically; do not send `skill_name`.
