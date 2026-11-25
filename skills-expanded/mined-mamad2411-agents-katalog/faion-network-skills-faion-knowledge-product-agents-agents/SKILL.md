# Product Manager Agents

## Summary

**One-sentence:** Two Claude subagents for product scoping work: `faion-mvp-scope-analyzer-agent` analyses competitor features to recommend a minimum feature set for a new product, and `faion-mlp-agent` upgrades an MVP to an MLP through a five-mode sequential pipeline (analyze → find-gaps → propose → update → plan) with a mandatory human checkpoint between `propose` and `update`.

**One-paragraph:** Two Claude subagents that turn MVP→MLP scoping into a traceable pipeline instead of a vibes-led roadmap session. `faion-mvp-scope-analyzer-agent` requires ≥3 named comparables, refusing to run without them so it cannot hallucinate a feature floor. `faion-mlp-agent` runs 5 modes in strict sequence — analyze the current state, find-gaps against MLP dimensions (Delight, Ease, Speed, Trust, Personality), propose WOW features, update spec files autonomously after human review, and plan implementation order. The mandatory checkpoint between `propose` and `update` plus a "VCS clean tree" precondition on `update` keep autonomous spec edits reviewable. B2B contexts down-weight Delight and Personality.

**Ефективно для:** PM, який скейлить продукт з MVP до "продукт, який клієнт любить" і втомився, що roadmap-сесії — це 4-годинна срачка про "wow-фічі".

## Applies If (ALL must hold)

- Defining MVP scope for a new product OR upgrading an MVP to an MLP.
- ≥3 comparable products exist (for MVP-scope-analyzer).
- Spec files are committed to version control (for MLP mode:update).
- A PM is available to approve mode:propose output before mode:update runs.
- The team is ready to act on spec updates (not mid-sprint / code freeze).

## Skip If (ANY kills it)

- Product at ideation stage with no existing specs — start with discovery methodology instead.
- Competitor landscape entirely novel, no comparables — the MVP scope analyzer needs comparables.
- Team not ready to act on spec updates — run analyze + find-gaps for prep, defer update.
- B2B enterprise with highly custom requirements where MLP dimensions don't apply — modify weights first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Target market + segment | text | product brief |
| ≥3 named comparables | list | competitive research |
| Existing spec files | markdown | product repo |
| Clean VCS state | git status output | local repo |
| PM available for review | role + person | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/product/product-manager/ai-native-product-development` | Product-positioning context this pipeline consumes. |
| `geek/product/product-manager/agentic-ai-product-development` | Sibling autonomous-agent methodology; shares VCS-state hygiene. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: strict-sequence, human-checkpoint-before-update, VCS-clean precondition, ≥3 comparables, B2B trust+ease weights | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (mode:plan as backlog, rigid 5-dim checklist, stale analyzer output, unapproved update, dirty tree) | ~950 |
| `content/06-decision-tree.xml` | essential | New-product-or-existing branch + B2B-or-B2C weight branch + clean-VCS gate | ~350 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scope-analyze` | sonnet | Competitor-grounded judgment; cites comparables. |
| `mlp-find-gaps` | sonnet | Per-dimension judgment from current state vs target. |
| `mlp-propose-wow-features` | opus | Strategic synthesis; surfaces non-obvious differentiators. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mlp-pipeline.py` | Sequential 5-mode pipeline coordinator with human-checkpoint pause. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents.py` | Validate a subagent run record (mode, vcs_state, comparables count, human_review_status). | After every subagent invocation. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[agentic-ai-product-development]] — sibling autonomous-agent product methodology.
- [[ai-feature-de-risking]] — peer methodology for shipping AI features safely.
- [[ai-native-product-development]] — provides positioning context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first asks whether this is a new-product scope or MVP→MLP upgrade. New-product branch checks ≥3 comparables → run scope-analyzer. MLP branch checks VCS clean + PM available → run sequential pipeline. B2B vs B2C decides dimension weights (B2B: trust+ease > delight+personality).
