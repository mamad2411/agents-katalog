---
name: ai-spend-report
description: Produce a report of AI and token spend for this project from real metrics — per-agent and per-feature attribution, retry waste, prompt-cache economics, token budgets, and the measured saving from the Foundry memory system. Use when asked what Claude Code is costing, which agent is expensive, whether a model downgrade is safe, or whether the memory system pays for itself. Reads prices only from pricing.json and reports token counts with no money when it is absent.
user-invocable: true
argument-hint: "[--since YYYY-MM-DD] [--until YYYY-MM-DD] [--model <id>]"
context: fork
agent: foundry-economics:ai-cost-controller
background: false
model: sonnet
effort: medium
metadata:
  foundry.vertical: economics
  foundry.io: "events.jsonl + pricing.json -> estimate.v1"
license: Apache-2.0
---

# AI spend report

Measures what the AI system costs **from files that exist in this repository**. Nothing in
this skill estimates, extrapolates or recalls a price.

**Not financial advice.** Analytical decision support only.

## Step 0 — Locate prices, or declare their absence

Look in order:

1. `.foundry/economics/pricing.json`
2. `<project root>/pricing.json`
3. the path in `.foundry/config.json` under `economics.pricingPath`

**If none exists**, the report opens with exactly this and then continues in tokens:

> No `pricing.json` found in this project. All figures below are **token counts only**;
> monetary values are shown as `<<UNPRICED>>`. Create `.foundry/economics/pricing.json` from
> `references/pricing.template.json` and fill it from your provider's current published
> pricing to get costs.

Never guess a rate, not even "to illustrate". A token report without prices is honest and
useful; one with invented prices is a liability. Check `pricing.asOf`: if it is more than
90 days before today, warn that prices may be stale. Schema and rules in `references/pricing.md`.

## Step 1 — Aggregate the metrics

```
node ${CLAUDE_SKILL_DIR}/scripts/aggregate-events.mjs --root "$CLAUDE_PROJECT_DIR" --format md
node ${CLAUDE_SKILL_DIR}/scripts/aggregate-events.mjs --root "$CLAUDE_PROJECT_DIR" \
  --since 2026-07-01 --until 2026-07-31 --model <model-id> --format json
```

Zero dependencies, Node ≥ 20, read-only, cross-platform. Exit code `2` means there is no
metrics file yet — report that as a fact, not as a failure.

Then call the `token_report` tool of the `foundry` MCP server for index size, stored-fact
size and blackboard size. Use the tool, not file reads: reading `.foundry/memory/` into
context to write a report about token economy would be self-refuting.

### Be explicit about what the data cannot tell you

`.foundry/metrics/events.jsonl` is a **gate-and-memory ledger, not a token ledger**. The only
token-bearing event is `subagent_return`. Prompt, cache and output tokens for the main
conversation are simply not in the file. Whole-session totals must come from a provider usage
export or `/cost` output supplied by a human.

State this in the report. Do not scale up `subagent_return` totals and present the result as
measured. Event-kind reference: `references/metrics-schema.md`.

## Step 2 — Attribute

```
cost(call)    = (input×inputPerMTok + cacheWrite×cacheWritePerMTok
               + cacheRead×cacheReadPerMTok + output×outputPerMTok) / 1e6
cost(agent)   = Σ over that agent's calls
cost(session) = Σ over the session's calls
cost(feature) = Σ over sessions attributed to the feature
```

Reliability ladder — state which rung each figure sits on:

| Rung | Method | Status |
|---|---|---|
| 1 | Per-agent, from `subagent_return.tokens` | measured |
| 2 | Per-session, split on `session_end.session`, joined to a usage export by time window | measured if an export exists |
| 3 | Per-feature, joined on branch name from `git reflog` against the session's time window | **heuristic** — label it, give a confidence |

Rung 3 has no support in `events.jsonl`: no event kind carries a branch or a feature tag, so the
only join available is `git reflog` against session timestamps, and it is a guess whenever two
branches were touched in one session. If it cannot be done reliably, report rungs 1 and 2 and
recommend adding an explicit feature tag rather than producing an attractive but unfounded
feature breakdown.

## Step 3 — Compute the operating metrics

```
cost_per_session       = total_cost / sessions
cost_per_merged_change = total_cost / merged PRs in the window
tokens_per_agent_run   = Σ subagent_return.tokens / count(subagent_return)     (report p80 too)
retry_waste_rate       = contract_violation ÷ (contract_valid + contract_violation)
zero_hit_rate          = memory_search with hits=0 ÷ all memory_search
```

`retry_waste_rate` is a **rejected-artifact rate, not a token share**: `contract_violation`
carries only `{schema, count}` and no token count, and no event ties a violation to a run or a
session, so a token-weighted figure cannot be computed from this file. Never present it as one.
It is still the most actionable single number, because a contract violation means an artifact was
produced, rejected and produced again — spend with zero output, fixable by correcting the agent's
output-contract handling rather than by changing any model. The aggregation script reports the
same ratio as `contractViolationRate`; if the two disagree, the script is right.

## Step 4 — Prompt-cache economics

With `w = cacheWritePerMTok/inputPerMTok − 1` and `r = cacheReadPerMTok/inputPerMTok`:

```
break-even reuses  N* = (1 + w − r) / (1 − r)
```

Derive `w` and `r` from `pricing.json`; never assert typical values. Then check what actually
governs whether `N*` is reached — prefix stability, TTL, and fan-out — and say whether caching
is currently paying. If cache token counts are absent from your data, say so rather than
modelling a cache you cannot see. Full treatment and the ordering rules in `references/levers.md`.

## Step 5 — Token budgets

```
budget(workflow) = Σ_agents ( expected_runs × p80_tokens_per_run ) × (1 + headroom)
```

Use the **p80** from step 3, not the mean, or half the runs breach on day one. State the
headroom and justify it. Enforcement points that already exist and cost nothing:
`handoffSummaryTokenBudget` (default 300) and `indexTokenBudget` (default 4000) in
`.foundry/config.json`, plus the `subagent-firewall` hook. Name the breach policy — warn,
degrade, or stop — and its owner. A budget with no consequence is a comment.

## Step 6 — Is the memory system paying for itself?

```
eager_baseline   = fact_tokens + blackboard_tokens          (counterfactual: load everything)
lazy_actual      = index_tokens + Σ retrieved_fact_tokens
saving_tokens    = eager_baseline − lazy_actual − memory_write_cost
saving_money     = saving_tokens × sessions × inputPerMTok / 1e6
```

All inputs from `token_report` and the aggregation script. Be scrupulous, because this is a
claim Foundry makes about itself:

- Label the eager baseline a **counterfactual**, not an observation.
- Subtract the write cost: `memory_write` calls and index rebuilds.
- Report the zero-hit rate; searches returning nothing are pure cost.
- Sessions that never queried memory get no credit.
- **If the net is negative, say so.** A cost controller that only ever validates its own
  system is not a control.

## Step 7 — Emit

Write `estimate.v1` via `blackboard_write`:

```
wave:   ai-spend
agent:  ai-cost-controller
schema: estimate.v1
```

- `scope` carries the window and its sources.
- One item per attribution unit, `unit: "eur"` — **only when priced**.
- Unpriced run: omit monetary items entirely and set
  `assumptions[0] = "UNPRICED: no pricing.json; monetary items omitted, token counts in companion report."`
  Do not misuse the `unit` enum to smuggle token counts into a money field.

Companion report from `references/templates/ai-spend-report.md`; per-agent table to
`.foundry/economics/ai-spend.csv` using `references/templates/ai-spend.csv`. Return only the
paths plus ≤ 300 tokens.

## Exit criteria

- [ ] Prices located or their absence declared in the first line
- [ ] `pricing.asOf` staleness checked against today
- [ ] Window stated with session count and events-in-window count
- [ ] Per-agent totals with runs, p50, p80, max
- [ ] The gap between `events.jsonl` and a true token ledger stated explicitly
- [ ] `retry_waste_rate` and `zero_hit_rate` computed, and `retry_waste_rate` labelled a
      rejected-artifact rate rather than a token share
- [ ] Cache `N*` computed from `pricing.json`, or its absence explained
- [ ] Token budget proposed per workflow from p80 values, with a breach policy and an owner
- [ ] Memory saving computed **net of write cost**, counterfactual labelled
- [ ] At least three levers, each with file to change, current measured value, expected delta,
      and the risk accepted
- [ ] No monetary figure without a `pricing.json` line behind it
- [ ] `blackboard_write` returned VALID

## What this skill deliberately does not cover

- **Price discovery.** It does not fetch, browse or recall prices.
- **Output quality.** It measures cost, never whether answers are good. A model downgrade must
  be quality-evaluated by whoever owns the workflow.
- **Model benchmarking** or capability claims about any model.
- **Cloud infrastructure cost** → `finops-analyst`. **Build cost** → `estimate-project`.
  **Whether the AI feature is worth building** → `business-plan`.
- **Per-person monitoring.** Attribution is to features and agents. Do not build individual
  productivity surveillance from this data; refuse if asked.
- **Provider contract negotiation and committed-spend tiers.**

## References

- `references/pricing.md` — pricing.json schema, sourcing rules, staleness policy
- `references/pricing.template.json` — copy to `.foundry/economics/pricing.json`
- `references/metrics-schema.md` — every event kind and what it can and cannot prove
- `references/levers.md` — the concrete levers, ranked, each with its risk
- `references/templates/ai-spend-report.md` · `references/templates/ai-spend.csv`
- `scripts/aggregate-events.mjs` — the aggregator

## Interop

Record measured baselines — cost per session, per-agent p80 tokens, cache reuse, zero-hit rate
— with `memory_write` as facts of type `metric`, so the next report has a reference class.
Hand any structural change with real implementation effort to `estimate-project`. If
`superpowers` is installed, use `superpowers:verification-before-completion` before claiming a
saving; otherwise run the exit criteria above.
