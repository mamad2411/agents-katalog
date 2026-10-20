# Eval Set Stratified Sampling Recipe

## Summary

**One-sentence:** Produces a stratified sampling recipe (per-cohort × per-tool × per-intent quotas) for daily LLM eval-set drift checks so the slice is representative without paying full-eval cost.

**One-paragraph:** Daily drift checks cannot run the full eval set — too slow, too expensive. A naive random subsample misses tails (low-volume intents, new cohorts, rare tools). This methodology produces a written sampling recipe: declared strata (cohort × tool × intent × difficulty), per-stratum quota (proportional-with-floor, never raw-proportional), seed-locked sampler, fixed daily N, and a drift comparator that triggers re-sample only when the prod traffic distribution shifts >10%. Output is a `sampling-recipe.json` that the eval harness reads each morning.

**Ефективно для:** daily eval-suite triage, p7-llm-agent-developer drift monitoring, ML-ops on-call who needs a fixed-cost slice that still covers the long tail, teams whose eval bill 10x'd after they added cohorts.

## Applies If (ALL must hold)

- Production LLM workload has ≥3 named cohorts, tools, or intents.
- A full eval set ≥500 cases exists and is too expensive to run daily.
- Traffic distribution per stratum is known (analytics or trace logs).
- A daily slice budget (cases-per-day or $/day) is fixed.

## Skip If (ANY kills it)

- Full eval set ≤500 cases — run it whole, sampling adds noise without saving money.
- No traffic distribution data — fix observability before designing strata.
- Single cohort/intent — random subsample is equivalent, no stratification needed.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval set manifest | JSONL with `cohort`, `tool`, `intent`, `difficulty` fields | eval repo |
| Production traffic distribution | CSV `stratum,count_30d,share_pct` | analytics warehouse |
| Daily slice budget | int (cases/day) or float ($/day with $/case rate) | finops / on-call lead |
| Prior recipe (if exists) | `sampling-recipe.json` | eval repo `eval/` dir |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[llm-drift-daily-triage]]` | Consumer of the daily slice; recipe must match its cadence. |
| `geek/ai/llm-integration/AGENTS.md` | Parent group vocabulary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: proportional-with-floor, seed lock, drift trigger, stratum max-share cap, tail-floor 5 cases, recipe versioning | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for `sampling-recipe.json` + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: head-only sample, no floor, unchanged recipe under drift, no seed | ~600 |
| `content/04-procedure.xml` | recommended | 6 steps: enumerate strata → fetch traffic → set N → apply proportional+floor → seed → diff vs prior | ~700 |
| `content/05-examples.xml` | recommended | One full worked recipe for a 4-cohort × 3-tool agent | ~600 |
| `content/06-decision-tree.xml` | essential | Apply-or-skip + recipe-shape branches | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Enumerate strata from manifest | haiku | Mechanical group-by. |
| Compute per-stratum quotas | sonnet | Arithmetic + floor/cap judgment. |
| Diff vs prior recipe + decide refresh | sonnet | Bounded comparison. |
| Recipe rationale write-up | opus | Synthesis for human reviewer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sampling-recipe.schema.json` | JSON Schema for the recipe artefact. |
| `templates/sampling-recipe.example.json` | Reference filled recipe for a 4×3×2 grid. |
| `templates/strata-quota.py` | Proportional-with-floor quota calculator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eval-set-stratified-sampling-recipe.py` | Validate a recipe JSON against the schema + rule checks. | After recipe write, before eval harness consumes. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[llm-drift-daily-triage]]` — downstream consumer
- `[[judge-calibration-protocol]]` — orthogonal eval-quality lever

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: eval-set size ≥500, multi-stratum, traffic data available, then chooses between fresh-recipe or carry-forward branches based on traffic drift vs prior recipe.
