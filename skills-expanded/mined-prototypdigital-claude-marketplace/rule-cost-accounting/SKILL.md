---
name: cost-accounting
description: Measure LLM cost from the authoritative usage object and the provider's cost API — never from your own token estimates.
---

# Cost accounting

If an LLM feature has unit economics, measure them from the **authoritative numbers the provider returns**, not from estimates you compute yourself. Self-counted token estimates routinely miss what actually drives the bill: prompt-cache reads and writes, tool-use tokens, system-prompt overhead, and per-model rate differences.

## Rules

- Read cost inputs from the **`usage` object on each response** (input tokens, output tokens, and cache-read / cache-write tokens) rather than re-tokenizing the prompt to guess. The provider's count is the one you're billed on.
- For aggregate spend, pull from the provider's **organization Usage / Cost Admin API**, not a hand-rolled tally. Reconcile per-feature attribution against it.
- Track **cost per task / per resolved outcome**, not just cost per token — a cheaper-per-token model that needs more turns or retries can cost more per finished task.
- Attribute cost to a feature or request id at capture time; retrofitting attribution from logs after the fact is lossy.

## Examples

```ts
// BAD — self-counting tokens; misses cache reads, tool tokens, system-prompt overhead
const inputTokens = prompt.split(' ').length  // rough estimate
const cost = inputTokens * MODEL_INPUT_PRICE_PER_TOKEN

// GOOD — read authoritative usage object from the response
const response = await client.messages.create({ ... })
const { input_tokens, output_tokens, cache_read_input_tokens } = response.usage
const cost = (
  input_tokens * INPUT_PRICE +
  output_tokens * OUTPUT_PRICE +
  (cache_read_input_tokens ?? 0) * CACHE_READ_PRICE
)
```

## Source

Anthropic, "Usage and Cost API," 2026-02 — <https://platform.claude.com/docs/en/build-with-claude/usage-cost-api>. Per-response `usage` fields and the org-level Usage/Cost Admin API are the authoritative basis for cost measurement; estimates omit cache and tool token accounting.
