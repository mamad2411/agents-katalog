---
name: market-research-pro
description: |
  Production-grade market research: evidence and sizing system model, failure modes (single-source TAM, spurious precision, stale data), decision trade-offs (top-down vs bottom-up, breadth vs depth, speed vs rigor), quality guardrails (no fabricated market sizes; cite source+date+geo).

  Use when the user asks to validate market opportunity, compare competitors, estimate market size with assumptions, identify ICP segments, prioritize expansion, or produce an executive market brief with citations and confidence levels.

  Pair with `web-research-pro` for official current sources, `business-analysis-pro` to turn findings into requirements or roadmaps, and `data-analysis-pro` for numeric analysis of survey or tabular data. This skill owns research framing and synthesis quality; the others own implementation and analytics.

  Triggers: "market research", "TAM", "SAM", "SOM", "competitive analysis", "market sizing", "ICP segments", "market brief", "competitor landscape", "expansion".
---

> Adapted from [truongnat/aix](https://github.com/truongnat/aix), licensed under MIT.
> See [ATTRIBUTION.md](ATTRIBUTION.md) for source and license details.

# Market research (professional)

Skill text is **English**; answer in the user's preferred language when rules or the conversation specify it.

Use official company sources, regulatory filings, and high-quality industry reports as preferred evidence; this skill encodes **assumption-driven sizing**, **source reliability ranking**, and **decision-ready** synthesis. Confirm **market definition**, **geography**, **time horizon**, and **decision context** (invest, build, expand, price).

## Boundary

**`market-research-pro`** owns **what market signals mean for decisions**, **sizing methods**, **competitive framing**, and **evidence quality**. **`web-research-pro`** owns **how** to gather and verify external sources. **`business-analysis-pro`** owns **requirements and delivery** artifacts from decisions.

## Related skills (this repo)

| Skill | When to combine with `market-research-pro` |
|-------|--------------------------------------------|
| **`web-research-pro`** | Collect and verify external sources, changelogs, and citation quality |
| **`business-analysis-pro`** | Convert findings into initiative scope, requirements, and priority |
| **`data-analysis-pro`** | Analyze survey/usage/exported datasets numerically |
| **`seo-pro`** | Search-demand and organic visibility angle for web-first products |

## When to use

- Market sizing with transparent assumptions (TAM/SAM/SOM).
- Competitor landscape and differentiated positioning.
- ICP/segment prioritization and expansion hypotheses.
- Pricing and packaging hypothesis framing (not final finance model).
- Trend scan for strategic direction with citation discipline.

## When not to use

- **Legal or investment advice** as binding opinion — surface evidence and defer to counsel/investors.
- **Primary survey design** as the main topic — pair **`data-analysis-pro`** for instrument and stats.

## Required inputs

- **Decision** the research supports (or explicit "exploratory").
- **Market boundary** draft (category, geo, timeframe) when sizing.

## Expected output

Follow **Suggested response format (STRICT)** — eight sections including explicit confidence.

## Workflow

Apply **Karpathy principles** throughout: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution.

1. **Confirm** decision to support (go/no-go, segment priority, pricing hypothesis), market boundaries, and timeframe. → verify: [context documented].
2. **State assumptions** about requirements, constraints (**Think Before Coding**).
3. **Apply** minimum solution first; escalate only when justified (**Simplicity First**).
4. **Make surgical changes** — only touch code directly related to the request (**Surgical Changes**).
5. **Define success criteria**; loop until verified (**Goal-Driven Execution**).
6. **Respond** using **Suggested response format**; note main risks.

### Operating principles

1. **Think Before Coding** — Confirm the decision, market boundary, geography, and time horizon before sizing or comparing anything. Ask when the category itself is unstable or ambiguous.
2. **Simplicity First** — Use the smallest defensible evidence set and sizing method that answers the decision. Do not fabricate precision or build heavyweight market models without need.
3. **Surgical Changes** — Analyze only the relevant market slice, segment, or competitor frame. Do not expand into broad industry theory unless it changes the decision.
4. **Goal-Driven Execution** — Done = the research supports a decision with explicit assumptions, source dates, and confidence.
5. **Evidence quality is part of the result** — A weak source should weaken the claim, not be hidden behind polished prose.
6. **Sizing is assumption math** — TAM/SAM/SOM outputs are only as good as the boundary and denominator logic behind them.
7. **Competitors are contextual** — Substitute, adjacent, and direct competitors should not be flattened into one category.
8. **Market research is not prophecy** — Uncertainty and outdated or conflicting signals should remain visible.

## Default recommendations by scenario

- **Exploratory market scan** — Start with category definition, key segments, and a small competitor map.
- **Sizing request** — State the method and assumptions before quoting any market number.
- **Expansion decision** — Compare geographies or verticals on the few criteria that drive the actual choice.
- **Positioning question** — Clarify substitute and direct competitor sets before claiming differentiation.

## Decision trees

Summary: choose top-down, bottom-up, competitor-first, or segment-first research paths based on the decision and available evidence.

Details: [references/decision-tree.md](references/decision-tree.md)

## Anti-patterns

Summary: single-source TAM, stale benchmark reuse, spurious precision, and competitor sets that do not match buyer reality.

Details: [references/anti-patterns.md](references/anti-patterns.md)

### Market signal and evidence system model (summary)

How sources, market signals, and synthesis quality should interact so research stays decision-relevant.

Details: [references/market-signal-and-evidence-system-model.md](references/market-signal-and-evidence-system-model.md)

### Market sizing and assumptions (summary)

How to bound TAM/SAM/SOM and keep assumption math visible instead of implied.

Details: [references/market-sizing-and-assumptions.md](references/market-sizing-and-assumptions.md)

### Competitor and positioning (summary)

How to compare categories, substitutes, and direct players without collapsing them into shallow feature grids.

Details: [references/competitor-and-positioning.md](references/competitor-and-positioning.md)

### Segment prioritization and GTM (summary)

How to reason about ICPs, wedges, and go-to-market sequencing from evidence rather than preference.

Details: [references/segment-prioritization-and-gtm.md](references/segment-prioritization-and-gtm.md)

### Reporting and evidence quality (summary)

How to present findings with source/date/geo context and honest confidence levels.

Details: [references/reporting-and-evidence-quality.md](references/reporting-and-evidence-quality.md)

## Suggested response format (STRICT)

1. **Context** — Decision, market boundary, geography, timeframe, and confidence needs.
2. **Research model** — Explain the sizing or competitor frame and why it fits the decision.
3. **Findings** — Evidence-backed market, segment, or competitor conclusions with assumptions visible.
4. **Verification** — Source/date/geo anchors and what would need refreshing later.
5. **Residual risks** — Weak evidence, category ambiguity, or stale-data exposure.

## Resources in this skill

| Topic | File |
|-------|------|
| Market signal and evidence system model | [references/market-signal-and-evidence-system-model.md](references/market-signal-and-evidence-system-model.md) |
| Market sizing and assumptions | [references/market-sizing-and-assumptions.md](references/market-sizing-and-assumptions.md) |
| Competitor and positioning | [references/competitor-and-positioning.md](references/competitor-and-positioning.md) |
| Segment prioritization and GTM | [references/segment-prioritization-and-gtm.md](references/segment-prioritization-and-gtm.md) |
| Reporting and evidence quality | [references/reporting-and-evidence-quality.md](references/reporting-and-evidence-quality.md) |
| Failure modes and mitigation | [references/failure-modes-detection-mitigation.md](references/failure-modes-detection-mitigation.md) |
| Decision framework and trade-offs | [references/decision-framework-and-trade-offs.md](references/decision-framework-and-trade-offs.md) |
| Decision tree | [references/decision-tree.md](references/decision-tree.md) |
| Anti-patterns | [references/anti-patterns.md](references/anti-patterns.md) |
| Tips and tricks | [references/tips-and-tricks.md](references/tips-and-tricks.md) |
| Edge cases | [references/edge-cases.md](references/edge-cases.md) |
| Quality validation and guardrails | [references/quality-validation-and-guardrails.md](references/quality-validation-and-guardrails.md) |
| Integration map | [references/integration-map.md](references/integration-map.md) |
| Version notes | [references/versions.md](references/versions.md) |

## Quick example

**Input:** "Estimate the market for a developer tool in Southeast Asia."
- Define the category and geography before computing any size estimate.
- Use transparent assumptions instead of quoting a single magic TAM number.
- **Verify:** The output shows the method, source dates, and the assumption chain.

**Input (tricky):** "This competitor report gives contradictory market sizes."
- Compare source scope, year, and category definition before choosing a number.
- Preserve uncertainty instead of reconciling by guesswork.
- **Verify:** The report explains why the figures differ and which one is more decision-usable.

**Input (cross-skill):** "Research the market, then turn it into a product wedge."
- Pair **`web-research-pro`** for source gathering and **`business-analysis-pro`** or **`strategic-consulting-pro`** for decision conversion.
- Keep evidence collection and strategy framing distinct.
- **Verify:** The wedge recommendation is traceable back to segment evidence rather than intuition alone.

## Checklist before calling the skill done

- [ ] Decision, market boundary, geography, and timeframe confirmed first (Think Before Coding)
- [ ] Minimum defensible research path chosen; no fake precision added (Simplicity First)
- [ ] Only the relevant market slice or competitor set was analyzed (Surgical Changes)
- [ ] Success criteria, assumptions, and evidence anchors are explicit (Goal-Driven Execution)
- [ ] Sizing logic is transparent
- [ ] Competitor framing matches the actual buyer/use case context
- [ ] Source date and geography are stated where they matter
- [ ] Residual uncertainty or stale-data risk is documented
