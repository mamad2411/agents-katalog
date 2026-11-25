---
name: pe-ai-readiness
version: 1.0.0
description: Assess a target or portfolio company's AI maturity, data assets, and organizational readiness, then identify and ROI-rank the AI-driven value-creation opportunities with build-vs-buy calls for each.
author: matrixx0070
tags: [ai-readiness, data-maturity, value-creation, build-vs-buy, ai-roi, use-case-identification, private-equity]
capabilities: []
---

## When to use

Use this when a fund needs to judge how much AI-driven value a company can realistically create — during diligence to test an AI angle in the thesis (or to avoid overpaying for AI hype), or post-close to build the AI workstream of a value-creation plan. Reach for it to grade the company's data assets and AI maturity honestly, to surface concrete use cases tied to P&L lines, and to decide for each whether to build, buy, or partner. The output is an AI-readiness assessment: a maturity grade across data/talent/infrastructure/governance, a ranked use-case portfolio scored by value and feasibility, build-vs-buy recommendations, and an ROI-prioritized roadmap.

**Not for:** the broad go/no-go screen of a deal (use pe-deal-screening — AI readiness is one input into it, not the whole verdict); the full cross-workstream diligence checklist (use pe-dd-checklist — this is the AI/tech-value slice of it); analyzing unit economics like LTV/CAC (use pe-unit-economics); modeling MOIC/IRR and the returns bridge (use pe-returns-analysis); building the whole 100-day and full-hold value-creation plan (use pe-value-creation-plan — AI readiness feeds the tech/data workstream of it); writing the IC memo (use pe-ic-memo); origination and pipeline building (use pe-deal-sourcing); preparing management-meeting questions (use pe-dd-meeting-prep); or tracking KPIs after close (use pe-portfolio-monitoring).

## Method

1. Grade data maturity first — it is the binding constraint. Assess whether data is captured, accessible, clean, integrated, and governed (see the maturity ladder in Reference). **Decision:** if data is at the bottom of the ladder (siloed, dirty, no single source of truth), most AI use cases are infeasible until a data-foundation investment lands first — say so, and sequence data remediation ahead of models rather than promising AI value that the data can't support.
2. Grade the other readiness pillars: talent (in-house AI/analytics skills or none), infrastructure (cloud/compute/tooling), and governance (model risk, security, IP, and — for regulated sectors — AI-compliance posture).
3. Identify use cases from the P&L, not from the technology. Walk each major cost and revenue line and ask where prediction, automation, personalization, or generation moves the number: revenue (pricing, churn prediction, cross-sell, demand forecasting, sales productivity), cost (automation of manual back-office work, support deflection, procurement, predictive maintenance), and risk (fraud, credit, quality).
4. Size each use case: annual value (incremental revenue or cost saved), and feasibility (data availability, technical difficulty, change-management load). **Decision:** rank on value × feasibility and start with high-value / high-feasibility "quick wins" that fund credibility and cash, deferring high-value / low-feasibility "big bets" until the data foundation and organizational muscle exist.
5. Make a build-vs-buy call per use case. Default to **buy/adopt** commoditized capabilities (generic copilots, off-the-shelf forecasting, standard document processing) and **build** only where the company has proprietary data or a proprietary process that creates durable differentiation (see the decision table in Reference).
6. Estimate ROI honestly per use case: value minus total cost of ownership (licenses/compute, integration, talent, change management, ongoing model maintenance), a realistic time-to-value, and payback. Discount for adoption risk — the model that no one uses returns zero.
7. Assemble the roadmap: sequence data foundation → quick wins → scaled bets, with owners, investment, expected EBITDA/ multiple impact, and the metrics that prove each landed. Mark speculative value as speculative; do not let AI optimism inflate the underwriting.

## Example

A fund diligencing a $120M-revenue B2B insurance-claims processor tests an AI thesis. Data maturity grades 2/5: claims data exists but sits in three legacy systems with no unified warehouse and inconsistent coding — a data-foundation investment (~$1.5M, 9 months) is prerequisite. Use cases mapped to the P&L: (a) automating first-pass claim triage — $4M/yr labor saving, high feasibility once data is unified, **buy** a document-AI platform and configure; (b) fraud-flag scoring — $3M/yr leakage reduction, medium feasibility, **build** on the company's proprietary claims history (its genuine data moat); (c) a generative agent for adjuster note-drafting — $0.8M/yr productivity, high feasibility, **buy** an off-the-shelf copilot. ROI-ranked roadmap: fund the data warehouse in the first 100 days, land the triage quick win in months 6–9 (payback under 12 months), then build fraud scoring in year 2. Underwritten AI upside: ~$6M run-rate EBITDA improvement by exit, explicitly separated in the model from the base case so IC sees the deal working without it.

## Pitfalls

- **Grading data by what's stored, not by what's usable.** Terabytes of siloed, dirty, unlabeled data are not an asset. Assess accessibility, quality, and integration — usable data is the true constraint, and overstating it is the most common way AI value is over-underwritten.
- **Starting from the technology instead of the P&L.** "Let's add AI" produces demos, not EBITDA. Every use case must trace to a specific revenue or cost line with a sized number, or it does not belong in the underwriting.
- **Building what you should buy.** Custom-building commoditized capabilities burns capital and time and creates maintenance debt with no differentiation. Build only on proprietary data or process; buy everything generic.
- **Ignoring the total cost of ownership and adoption risk.** License cost is a fraction of the bill — integration, change management, and ongoing model maintenance dominate, and a model nobody adopts returns zero. Underwrite TCO and adoption, not just the model's theoretical lift.
- **Underwriting speculative AI upside into the base case.** Pricing AI value the company hasn't proven into the entry model inflates the deal and creates a return trap. Keep AI upside as a clearly separated, risk-discounted layer.

## Output format

```
# AI Readiness Assessment — <company> — <diligence | portfolio> — <date> — v<n>

## Readiness scorecard (1-5)
| Pillar | Score | Evidence | Constraint? |
| Data (capture/quality/access/integration/governance) | | | |
| Talent (AI/analytics skills) | | | |
| Infrastructure (cloud/compute/tooling) | | | |
| Governance (model risk / security / IP / compliance) | | | |

## Use-case portfolio
| # | Use case | P&L line | Annual value | Feasibility (H/M/L) | Build/Buy/Partner | TCO | Payback | Priority |

## Prioritization map
Quick wins (high value / high feasibility): <...>
Big bets (high value / low feasibility, sequenced later): <...>

## Roadmap
| Phase | Initiative | Owner | Investment | Expected EBITDA impact | Proof metric | Timing |
Phase 0: Data foundation → Phase 1: Quick wins → Phase 2: Scaled bets

## Underwriting note
AI upside is shown SEPARATELY from base case, risk-discounted for adoption. <$ run-rate impact by exit>
```

## Reference

AI readiness in PE is a value-creation and diligence discipline, not a technology audit. The frame below is how operating and deal teams actually assess it.

### Data maturity ladder (the binding constraint)

Most AI value is gated by data, so grade it first on a 1–5 ladder:

| Level | State | AI implication |
|-------|-------|----------------|
| **1 — Captured** | Data exists but siloed, manual, inconsistent | Almost nothing feasible without remediation |
| **2 — Accessible** | Consolidated into systems but not clean/unified | Basic reporting; limited ML |
| **3 — Integrated** | Single source of truth, warehouse/lake, decent quality | Standard analytics & ML feasible |
| **4 — Governed** | Cataloged, quality-monitored, access-controlled, labeled | Reliable production models, personalization |
| **5 — Leveraged** | Data is a monetized, differentiating asset | Proprietary AI moat, data products |

A company below level 3 usually needs a data-foundation investment sequenced ahead of models. Underwriting AI value on level-1/2 data is the classic over-promise.

### The four readiness pillars

| Pillar | What to assess |
|--------|----------------|
| **Data** | Capture, quality, accessibility, integration, governance (the ladder above) |
| **Talent** | In-house data science / ML / analytics capability; or reliance on vendors |
| **Infrastructure** | Cloud, compute, MLOps tooling, integration surface (APIs) |
| **Governance** | Model-risk management, security, IP ownership of models/data, and AI-regulatory posture in regulated sectors |

### Use-case identification — start from the P&L

| P&L area | Common AI levers |
|----------|------------------|
| **Revenue** | Dynamic pricing, churn prediction & retention, cross-sell/upsell, demand forecasting, sales & marketing productivity, personalization |
| **Cost** | Back-office automation, customer-support deflection (copilots/agents), document processing, procurement optimization, predictive maintenance |
| **Risk** | Fraud detection, credit/underwriting scoring, quality inspection, compliance monitoring |

Every use case must attach to a named P&L line with a sized annual value — value the number, then test feasibility.

### Value × feasibility prioritization

| | **High feasibility** | **Low feasibility** |
|--|--|--|
| **High value** | **Quick wins — do first** (fund credibility & cash) | **Big bets — sequence after foundation** |
| **Low value** | Fill-ins (optional) | Avoid |

### Build vs buy vs partner

| Factor | Build | Buy / adopt | Partner |
|--------|-------|-------------|---------|
| Capability is commoditized (generic copilot, OCR, forecasting) | | ✓ | |
| Rests on **proprietary data or process** = durable moat | ✓ | | |
| Need speed / low capex / no in-house talent | | ✓ | |
| Strategic but capability gap the company can't staff | | | ✓ |
| Ongoing maintenance burden acceptable | ✓ | (vendor carries it) | (shared) |

Default: **buy the commodity, build the moat.** Custom-building generic capability is the most common capital-destroying AI mistake in portfolio companies.

### ROI and TCO

```
Use-case ROI = (Annual value realized × adoption factor) − Total cost of ownership
TCO = licenses/compute + integration + talent + change management + ongoing model maintenance
Payback (months) = TCO / (monthly value realized)
```

The two numbers deal teams most often miss: **change management / adoption** (a model no one uses returns zero — apply an adoption factor) and **ongoing model maintenance** (models drift and need retraining; AI is an operating cost, not a one-time capex). Underwrite both, keep AI upside separated from the base case, and risk-discount it before it touches the return model.
