---
name: anthropic-api-troubleshooting
description: Diagnose failing Claude API requests — classify the error, explain the likely cause, and route to the fix. Use when an Anthropic API call errors, rate-limits, refuses, or behaves unexpectedly.
---

# Anthropic API Troubleshooting

Classify first, then fix. Use the SDK's typed exceptions
(`anthropic.BadRequestError`, `RateLimitError`, `APIStatusError`,
`APIConnectionError`) — never string-match messages.

## Error table

| Code | Type | Retryable | Usual cause |
|---|---|---|---|
| 400 | invalid_request_error | No | Bad params — see model-specific 400s below |
| 401 | authentication_error | No | Missing/invalid key; OAuth token on the wrong header; BOTH `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` set |
| 403 | permission_error | No | Key lacks model/feature access |
| 404 | not_found_error | No | Typo'd model ID (e.g. dot instead of dash, invented date suffix) |
| 413 | request_too_large | No | Oversized body — chunk or use the Files API |
| 429 | rate_limit_error | Yes | RPM/TPM/TPD — honor `retry-after`; SDK retries automatically |
| 500 | api_error | Yes | Transient — backoff; check status.anthropic.com |
| 529 | overloaded_error | Yes | Capacity — backoff, or try a less-loaded model |

## Model-specific 400s (the most common modern failures)

- `budget_tokens` sent to Opus 4.7/4.8, Sonnet 5, or Fable 5 → removed; use
  `thinking: {type: "adaptive"}`.
- `temperature` / `top_p` / `top_k` on those models → removed; delete them.
- `thinking: {type: "disabled"}` on Fable 5 → 400; omit the param entirely.
- Assistant-turn prefill on any 4.6+ model → 400; use structured outputs.
- Fable 5 under a zero-data-retention org → every request 400s; the payload
  is not the problem, the org's retention configuration is.
- First message not `user`, or `budget_tokens >= max_tokens` on old models.

## Not-an-HTTP-error failures

- **`stop_reason: "refusal"`** (HTTP 200): safety classifiers declined —
  check `stop_details.category`; content may be empty or partial. For Fable 5
  code, opt into server-side fallbacks
  (`betas: ["server-side-fallback-2026-06-01"]`,
  `fallbacks: [{"model": "claude-opus-4-8"}]`).
- **`stop_reason: "max_tokens"`**: raise `max_tokens` and stream.
- **`pause_turn`** on server-tool turns: re-send the conversation with the
  paused assistant turn appended — the server resumes; don't inject
  "Continue" text.
- **Silent cache misses**: `cache_read_input_tokens` stuck at 0 → a byte-level
  prefix invalidator (timestamp/UUID in the system prompt, unsorted JSON,
  varying tool set).

## Auth resolution gotcha

Credentials resolve: `ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → `ant auth
login` profile → WIF env. A stale exported API key silently shadows a
profile; an empty-string key still wins its slot. `ant auth status` shows
which source won.

Escalation: include the response `request_id` when reporting to Anthropic.
Current error docs: https://platform.claude.com/docs/en/api/errors
