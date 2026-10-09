---
name: tcx-instrument
description: "Analyze instrument mechanics, universe support, liquidity, contract terms, ETF/index methodology, options/derivatives context, crypto market structure, and credit-signal boundaries."
---

# Instrument Analysis

Use this skill when the workflow depends on instrument mechanics or support boundaries rather than only issuer fundamentals, price action, news, valuation, portfolio fit, or risk.

Universe method:

- Public equity and ETFs: review share class, ADR/ordinary mapping, index/ETF methodology, corporate actions, float, liquidity, borrow/crowding inputs when available, and settlement or market-structure issues.
- Options and derivatives context: review contract terms, expiry, Greeks, implied move, skew, liquidity, exercise/assignment, and margin/readiness gaps when data exists.
- Crypto public markets: review venue fragmentation, spot/futures distinction, funding, custody/account gaps, liquidity, and public market data limits.
- Credit signals, convertibles, preferreds, rates, FX, commodities, and other instruments: identify what can be used as research/risk evidence and what requires a dedicated installed workflow.

Expected output:

- Universe, instrument, and support status
- Instrument identifiers, venue/market convention, contract or methodology facts
- Liquidity, borrow/funding/options/settlement/market-structure evidence when relevant
- Unsupported instrument or underwriting gaps
- Source/as-of posture and stale or missing inputs
- Readiness label: `factual-baseline`, `screen-grade`, `not-decision-ready`, `ready-for-portfolio-risk`, or `blocked`
- Open instrument questions and missing support

Decision quality fields when applicable:

- `evidence_grade`, `source_freshness`, `source_quality`
- `conflict_status`, `decision_readiness`, `confidence`
- `scenario_cases`, `contrary_evidence`, `update_triggers`
- `invalidation_conditions` and forecast permission fields when relevant

Role-specific quality:

- Distinguish source-backed instrument facts from analyst assumptions and PM judgment.
- Never infer execution eligibility from research data availability.
- Do not fabricate contract terms, borrow, funding, Greeks, market levels, index weights, credit spreads, settlement terms, or source timestamps.
- If the installed schema, policy, or adapter cannot represent the instrument, label execution as `blocked` or `not-decision-ready`.

Write outputs under `trading/reports/instrument/`.
