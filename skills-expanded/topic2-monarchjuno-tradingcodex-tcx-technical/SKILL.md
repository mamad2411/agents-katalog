---
name: tcx-technical
description: "Analyze price action for an investment workflow. Use for trend, momentum, support/resistance, volatility, liquidity, drawdown, invalidation, and setup-quality reports."
---

# Technical Analysis

Use this skill for price, volume, trend, volatility, liquidity, drawdown, market-structure, and setup-quality analysis across supported traded instruments.

Universe method:

- Public equity, ETF/index, listed options context, crypto public market data, FX/rates/commodity proxies, and other traded instruments may be reviewed when source data is available and read-only.
- State the data venue/provider, instrument identifier, timeframe, session/market convention, and as-of timestamp.
- For non-equity instruments, identify unsupported specialist fields such as funding, roll yield, duration, Greeks, borrow, margin, custody, or venue fragmentation rather than pretending they are covered.
- Technical observations are evidence inputs, not trade instructions.

Expected output:

- Universe, instrument, timeframe, and data source
- Trend and momentum
- Support, resistance, and invalidation levels
- Volatility and liquidity notes
- Technical risk
- Setup quality
- Readiness label and missing market-structure inputs

Decision quality fields when applicable:

- `evidence_grade`, `source_freshness`, `source_quality`
- `conflict_status`, `decision_readiness`, `confidence`
- `contrary_evidence`, `update_triggers`, `invalidation_conditions`
- anti-overfit checks when backtest, signal, or model-performance claims appear

Role-specific quality:

- State data date, timeframe, and whether price data is missing or stale.
- State raw-versus-adjusted posture and the adjustment or corporate-action
  policy when it can change the result.
- Distinguish observation from trade recommendation.
- Include invalidation or uncertainty instead of a one-way setup call.
- Label stale or partial market data `screen-grade` or `not-decision-ready`
  only when the affected interval, venue, adjustment, liquidity, or market
  anchor could materially change the setup. Provider-derived data is not an
  automatic downgrade when its identity, timeframe, units, and freshness are
  adequate.
- State when evidence is suggestive rather than conclusive, especially when sample size or regime coverage is thin.
- Explicitly note when live implementation friction may erase paper alpha.
- Explain what the setup does and does not support.

Write outputs under `trading/reports/technical/`.
