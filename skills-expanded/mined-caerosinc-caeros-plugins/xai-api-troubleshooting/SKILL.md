---
name: xai-api-troubleshooting
description: Diagnose failing xAI API requests — classify the error, explain the likely cause, route to the fix. Use when a Grok API call errors, rate-limits, or costs more than expected.
---

# xAI API Troubleshooting

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| 400 on a Grok 4.6 request setting `reasoning_effort: "none"` | Reasoning cannot be disabled on Grok 4.6 | Use `low` / `medium` / `high` (default) / `xhigh` |
| 404 model not found | Retired ID (`grok-4.3`) or a typo | Migrate to `grok-4.6`; use exact IDs/aliases |
| 401 | Missing/invalid `XAI_API_KEY`, or key on the wrong header | Bearer token in `Authorization`; regenerate at console.x.ai |
| 429 | Team rate limits | Backoff with `retry-after`; check limits in console.x.ai |
| Output truncated | Your client set an output cap; Grok 4.6 itself has no text output limit | Raise the app cap or chunk the task; stream |
| Context errors on huge prompts | 500K (Grok 4.6/4.5) / 256K (Grok Build) windows | Trim or summarize history |

## Cost surprises

- **The 200K cliff**: Grok 4.6 rates DOUBLE once prompts reach 200K tokens
  ($2→$4 in, $6→$12 out). A long-context agent that drifts past 200K silently
  doubles its bill — cap or compact history before the cliff.
- **grok-4.3 → grok-4.6 migration**: the `xai:default` style aliases moved to
  4.6, which costs $2/$6 vs 4.3's $1.25/$2.50 — alias-pinned configs changed
  price without a code change.
- Cached input is $0.50/M vs $2/M — unstable prompt prefixes forfeit it.

## Behavior notes

- Grok 4.6 always reasons; latency includes thinking time. Use
  `reasoning_effort: "low"` for latency-sensitive routes, or Grok Build for
  fast coding loops.
- Parallel tool calls are native: your executor must handle multiple calls
  in one response and return all results together.
- Server-side search failures usually surface as degraded answers rather
  than HTTP errors — check whether search actually fired (citations
  present) before blaming the model.

Current status and docs: https://docs.x.ai and console.x.ai.
