---
name: compare-models
description: Compare specific AI models side by side, or browse the live model catalog, with Jev Model Router. Use when the user names models to weigh ("opus vs gpt-6-astra"), asks what a model costs or how fast it is, or wants a list of models filtered by provider, price, context, vision or tool support.
metadata:
  short-description: Compare named models or browse the catalog
---

# Compare or browse models

## Compare named models

1. Call `compare_models` with the names the user gave in `models`. Loose names work: "opus", "gpt 6 astra", "deepseek flash".
2. If the user has a task in mind, pass it as `task`. The result then adds a verdict per model (strong fit, fits, borderline, too weak, overkill), the best reasoning effort, and a per-call cost and time estimate, all scored together.
3. Show the table and name the best option for the user's priority. Point out overkill and too-weak options.

## Browse the catalog

1. Call `search_models` with the filters the user asked for: `query`, `provider`, `max_output_price_per_mtok`, `min_context`, `vision`, `tools`, `reasoning`, `sort` (intelligence, coding, price, speed, context or newest) and `limit`.
2. Show the table. Intelligence and coding scores are 0-100 relative to the strongest current model; `*` marks scores inferred from a model family and `?` marks unreviewed estimates.

To pick one model for a task without naming candidates, use the `route` skill instead.
