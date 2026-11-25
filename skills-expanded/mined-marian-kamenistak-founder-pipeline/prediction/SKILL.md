---
name: prediction
description: "Use when the owner wants demand or opportunity predictions for a product, service or idea, including ideas that do not exist yet: \"predict demand\", \"will this sell\", \"is there a market for\", \"which niche should I pick\", \"what will be a hit\". Also runs inside `/founder-pipeline:founder` (P1.S4 hypothesis run, P5.S4 cadence wiring). NOT for a stream whose recurring prediction already runs on your scheduler, current-state SEO gap analysis, or market segment mapping (`/founder-pipeline:scout`)."
---

# Prediction — falsifiable demand bets for any product, service, or idea

> **Model: always your top-tier reasoning model** for synthesis, scoring, and gate steps; the research fan-out (steps 3A-3D) can run on a mid-tier model. Never downgrade steps 4-7. Tiers, never codenames — model names age out, the tier requirement doesn't.

Turns an idea (existing or hypothetical) into a **scored, probability-weighted, falsifiable prediction ledger** plus a money model and an execution plan. Every re-run grades the previous run's predictions with Brier scores before making new ones — the skill measurably gets more trustworthy or gets caught.

**Boundary.** If you already run a recurring, scheduled prediction cadence for a given stream (see P5.S4, which wires one up), let that cadence own the stream and don't duplicate it here. `/founder-pipeline:prediction` is the generic engine for everything else — above all **ideation-time runs where the product does not exist yet**. It is also not a current-state SEO gap analysis: "which keywords do live competitors already beat me on" is a today question answered by SERP data; this skill answers "what will be true in 6-24 months, and how will we know if we were wrong". Don't mix them.

## Two modes

| | `hypothesis` mode | `live` mode |
|---|---|---|
| When | Idea stage — no site, no competitor folder, no ledger. Invoked by `/founder-pipeline:founder` P1.S4 or directly on any "should I build X?" idea | Existing stream with a folder. Invoked by `/founder-pipeline:founder` P5.S4 (cadence wiring) or ad-hoc |
| Competitor set | Derived live in step 3: `/founder-pipeline:scout` sweep + live SERP + LLM-citation scan. No tracked set required | Stream's competitors folder / profile if present, else derived live |
| Kill-list | None — the first run establishes it | Stream's execution-plan kill-list if present (binding) |
| Primary output | **Niche verdict**: which sub-niche/angle wins, which keywords/queries/content angles to pursue, which to drop — shaped to steer ideation | Ledger update + execution plan for the live stream |
| Execution plan | Greenfield variant: everything is a "new page/asset" — no renames, no cannibalization sections | Live variant: extend-existing beats new; renames allowed |
| Output root | Caller names it (founder passes the stream folder; ad-hoc runs ask) — `<root>/predictions/` | `<stream folder>/predictions/` |

## Required inputs (gate before step 1 — every mode, every invocation)

No candidate bet may be framed until three inputs are explicit and written into the workspace
config block:

- **Problem(s)** — the specific pain(s) being validated, not the product category. "Demand for
  a therapist in a given city" is not a problem; "affluent urban professionals with
  high-functioning depression underserved by insurance-pay therapy" is.
- **Target persona** — who specifically. A named ICP/segment, not "everyone" or "people
  interested in X." Multiple personas are fine if the run genuinely spans them, but each must be
  named, not implied.
- **Territory** — the geographic/market scope (country, region, city-tier, or explicitly
  "global"). Every keyword/SERP/labor pull in steps 3A-3D inherits this scope; a run with no
  territory silently drifts to whatever locale the research tools default to.

**How to satisfy the gate:** pull from already-established project context (a brief, an approved
plan, prior workspace files) when available — do not re-ask what's already on record. Where any
of the three is missing or ambiguous, ask the owner directly, one at a time, before step 1 starts.
Silently assuming a persona or territory from a product description is the failure mode this gate
exists to prevent — a "local-language therapist" idea with no territory input can drift into pricing
US keyword volumes without anyone deciding that. Record all three in the workspace config block
(below) so step 0's future grading run and any resumed/merged cycle inherit them.

## Pipeline

DAG: `0 → 1 → 2 → (3A ∥ 3B ∥ 3C ∥ 3D) → 4 → 5 → 6 → 7`. Read only the reference file the current step names.

| # | Step | Runs on | Gate |
|---|------|---------|------|
| 0 | **Grade past predictions** (re-runs only): for every ledger row past its check date, EXECUTE the row's recorded indicator command (fetch on the mid-tier model; hit/miss/partial verdicts on the top-tier one), compute the Brier score against the row's frozen base-rate column, update the calibration block. Grading re-query budget: $0.30 of paid keyword-data spend — one reason indicators should prefer free Tier-2 sources. **First run**: no ledger exists → create `PREDICTIONS.md` from the header block in `references/output-contract.md` with "cycle 1 — no calibration data yet" and skip to step 1 | mid-tier + top-tier | hard rule — no new predictions until old ones are graded |
| 1 | **Frame the questions + open the workspace.** Create `<output root>/predictions/<YYYY-MM-DD>/workspace.md` (same-day re-run: suffix `-2`) holding the config block — problem(s), target persona, and territory MUST already be filled in (see "Required inputs" gate above). Turn the idea into 3-10 candidate bets, each phrased as a **resolvable question**: background, resolution criterion, close date (Metaculus format — grading must never argue about what the prediction meant) | top-tier | workspace.md config block has problem/persona/territory filled before any bet is drafted |
| 2 | **Pre-register decision rules.** BEFORE any research runs, append to `workspace.md`: the survival cutoff (default: every rubric axis ≥ 2 AND all-axis product ≥ 24 AND confidence ≥ Medium — tighten per run, never loosen after scoring), per-bet kill/GO rules (structural is fine at zero data: "GO only if corroborated in ≥3 silos", "kill if a comparable failed for the same ICP"), and the money floor from the caller (founder passes the P1.S1 profit bar). The point is preventing post-hoc relaxation, not perfect priors. In hypothesis mode, the orchestrator also derives the competitor set HERE (one `/founder-pipeline:scout` + live-SERP pre-step) so the fan-out prompts carry it | top-tier | workspace.md with rules must exist before step 3 starts |
| 3A | **Papers/reports subagent** — academic + industry sources on the idea's domain | mid-tier | — |
| 3B | **Keyword/attention subagent** — keyword volumes + trends + AI-prompt volume from your keyword-data provider; Wikipedia pageviews + HN mention velocity for attention time series (`references/data-sources.md`). Balance check first; reuse cached `raw/*.json`; new paid spend cap $1 (hypothesis) / $0.60 (live) | mid-tier | — |
| 3C | **Labor/practitioner subagent** — job-posting counts (public jobs APIs), emerging role titles, community discourse (forums/newsletters) | mid-tier | — |
| 3D | **Contrarian subagent** — explicitly hunts evidence AGAINST each bet: failed comparable products, declining signals, "nobody pays for this" threads, substitute solutions | mid-tier | — |
| 4 | **Citation registry** — merge, dedupe, gate: ≥12 approved sources, ≥5 unique domains, ≥30% official/academic, single-source share ≤25%, **≥2 contrarian sources per candidate bet** (from 3D — applies to ALL bets; survival isn't decided until step 5). A trend claim counts as *signal* only when ≥3 unrelated silos corroborate it (e.g. search data + job postings + preprints) — otherwise it's *noise*, logged as Watch. Dropped sources never return | top-tier | auto-gate |
| 5 | **Score + calibrate** — per `references/rubric.md`: outside-view base rate FIRST, then 4-axis multiplicative score via an **ensemble of 3 parallel fresh-context subagents** (optimist / skeptic / base-rate-anchored — each blind to the others; orchestrator takes the per-axis median), then a granular probability (5% steps) per bet. A bet **survives** iff it clears the step-2 pre-registered cutoff. Any axis without evidence = **INSUFFICIENT DATA**, never a guessed midpoint — the bet becomes a Watch row (unscored, see hard rules) with a named manual-verification item | top-tier | `/founder-pipeline:critical` must surface ≥3 real issues (soft critique → one fresh-context re-run; still <3 → record and pass); blocking issues addressed before step 6 |
| 6 | **Money layer** — surviving bets only (Watch rows get none) — per `references/money-model.md`: Fermi-decompose into audience × problem incidence × conversion × price; every factor `[source: ...]` or `[assumption — validation: ...]`; name the factor that dominates uncertainty. Output = a 12-month revenue RANGE per bet vs the pre-registered money floor. INPUT to viability decisions, never proof | top-tier | — |
| 7 | **Outputs** — per `references/output-contract.md`: ledger rows (probability + indicator + threshold + check date + base-rate column + wild-card line), `prediction-report.md`, mode-appropriate `execution-plan.md`, and in hypothesis mode the **niche verdict** block. Cross-impact check: bets that rise and fall together are ONE bet — merge or mark correlated | top-tier | the owner reviews before anything downstream consumes the plan |

## Hard rules

- Every number carries `[source: <tool/URL>, <date>]` or `[assumption — validation: <test>]`. No invented URLs, volumes, or prices.
- A scored prediction enters the ledger only as a resolvable question with: probability (5% granularity), **executable leading indicator** — recorded as a runnable command in the ledger row (a curl-able URL, or a keyword-API call written out with its exact parameters) that step 0 can execute verbatim months later; the owner's own lead log or "session themes" never qualify as the sole indicator; **prefer free Tier-2 sources over paid Tier-1 when both discriminate** (grading budget is $0.30) — plus threshold picked at write time, check date, frozen base-rate column, and one wild-card line ("what breaks this" + its own watchable indicator).
- **Watch rows are unscored**: no probability, no Brier — they carry only indicator + graduation threshold + check date; when data arrives they graduate to scored bets. Forcing a probability onto a bet just declared unscoreable is the guess this rule exists to prevent.
- The base-rate column is **frozen at write time** and IS the naive forecaster's prediction at grading — never recomputed at grading time.
- Thresholds and survival cutoffs are pre-registered (step 2) — retro-fitting either to fit results is falsification of the record.
- INSUFFICIENT DATA is a legitimate rating. Filling an evidence gap with a plausible guess is not.
- API credentials for the research sources (jobs API, forum API, keyword-data provider) live in your secrets store, never in the workspace files. Paid keyword data runs through your provider's MCP server or REST client with a balance check before new spend. The worked example throughout the reference files is DataForSEO via its MCP server (`dfs-mcp`, an optional dependency you install separately) — any provider works as long as its calls are reproducible verbatim months later.
- Misses are never deleted; they are the calibration record. The ledger header carries the rolling mean Brier score vs the naive base-rate forecaster — if the skill isn't beating base rates after 3 cycles, say so in the report header.
- Step 0 before step 1 on every re-run.
- A hedge-everything ledger (all probabilities 45-55%) fails the resolution check in `references/rubric.md` — flag it, don't ship it.
- Reader-facing copy in outputs (titles, briefs) passes `/founder-pipeline:brand-voice` conventions.
- Prediction-market cross-check: where a related Metaculus/Polymarket/Manifold question exists, record its probability next to yours; divergence >20 points forces a written justification.
- Problem, target persona, and territory are gated inputs (see "Required inputs" above) — not optional framing color. A run missing any of the three does not proceed past step 1.

## Skill routing

| Need | Skill |
|------|-------|
| Adversarial pass at step 5 gate | `/founder-pipeline:critical` |
| Competitor set derivation (hypothesis mode step 3) | `/founder-pipeline:scout` + live SERP from your keyword-data provider |
| Deep domain research beyond the fan-out | No shipped skill — fan out extra research subagents on the domain, one question each, and register their sources through step 4's citation gate like any other |
| Execute a content brief into a post | `/founder-pipeline:blog-launch` (owner-triggered only) |
| Current-state SEO gap vs prediction | Different question — don't mix. Answer it inline from live SERP data, or with `/founder-pipeline:seo-audit` for the site's own side of it |

## Config block (per run, written into the workspace file)

```
mode: hypothesis | live
idea/stream: <one-liner or folder path>
problem: <the specific pain being validated — required, see "Required inputs" above>
target persona: <named ICP/segment — required, not "everyone">
territory: <geographic/market scope — required, or explicitly "global">
output root: <path>
horizon: default +24 months
budget: paid keyword-data new-spend cap (defaults above) + $0.30 grading reserve
money floor: <from caller; "none" allowed>
digest delivery: off by default (a scheduled cadence, if you run one, owns delivery)
```

**Founder hand-off contract (P1.S4):** founder passes idea one-liner + problem + target persona + territory + intake digest path + draft problem/ICP files (`P1-Ideation.S2-Problem.md`, `P1-Ideation.S3-ICP.md`) + the owner's asset list (for the founder-fit axis) + the P1.S1 profit bar as money floor + stream folder as output root. Ad-hoc runs ask exactly those inputs not already resolvable from project context, one at a time — problem/persona/territory are never skipped even when everything else is available.

## References

| File | Loaded by |
|------|-----------|
| `references/rubric.md` | step 5 — base rates, axes, ensemble, probabilities, Brier grading, resolution check |
| `references/data-sources.md` | steps 3A-3D — tiered source registry incl. free attention/labor/prediction-market APIs |
| `references/money-model.md` | step 6 — Fermi decomposition contract |
| `references/output-contract.md` | step 7 — ledger row format, report, execution-plan variants, niche verdict |
