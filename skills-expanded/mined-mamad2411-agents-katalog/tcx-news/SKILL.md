---
name: tcx-news
description: "Analyze news, filings, events, management commentary, policy changes, and market narrative. Use for source-quality review and fact-versus-inference timelines."
---

# News Analysis

Use this skill for news, filings, events, policy, macro, management commentary, market narrative, and source-quality review across supported investment universes.

Universe method:

- Public equity: use issuer filings, exchange/regulator records, earnings materials, transcripts, company news, sector/peer read-throughs, and market events.
- Crypto, macro, rates, FX, commodities, ETF/index, and credit-signal workflows need universe-specific sources and event taxonomies; label any missing route or unavailable connector honestly.
- Separate confirmed dates from inferred windows and unscheduled monitoring items.
- Treat rumors, social narratives, and single-source reports as unresolved evidence unless independently confirmed.

Expected output:

- Universe and event taxonomy
- Verified events
- Source list
- Timeline
- Market narrative change
- Fact versus inference separation
- Open questions
- Source/as-of posture and missing or stale event evidence

Decision quality fields when applicable:

- `evidence_grade`, `source_freshness`, `source_quality`
- `conflict_status`, `decision_readiness`, `confidence`
- `scenario_cases`, `contrary_evidence`, `update_triggers`
- `invalidation_conditions` and forecast permission fields when relevant

Role-specific quality:

- Put events in chronological order with dates.
- Separate source claims from analyst interpretation.
- Flag rumors, single-source claims, and stale events.
- State whether each event changes thesis, timing, valuation, risk, liquidity,
  policy, or only background context.
- Do not fabricate headlines, publication dates, filing dates, source claims, or retrieval timestamps.

Write outputs under `trading/reports/news/`.
