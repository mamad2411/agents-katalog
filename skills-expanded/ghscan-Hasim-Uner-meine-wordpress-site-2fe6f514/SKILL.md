---
name: revenue-learning-loop
description: "Plan or evaluate a release against qualified, progressed and won inquiries. Use for measurement readiness and keep/revert decisions, not analytics implementation."
---

# Revenue Learning Loop

Name the route, decision and evidence needed. Use the selected local context;
read only the relevant route in `llms.txt` and the matching mode below.

## Select one mode

- Instrument: missing or uncertain measurement → [instrument](references/instrument.md).
- Plan: define one change and freeze outcomes/windows → [plan](references/plan.md).
- Review: compare declared windows → [review](references/review.md).

The mode links to required measurement-contract sections. Do not load all modes.

## Implementation ownership

Hand a distinct implementation phase to its primary owner:
- Cockpit code → `seo-cockpit-dev`; REST/CRM/attribution → `wordpress-growth-architecture`.
- Broad website audit → `performance-marketing`; offer diagnosis → `offer-funnel-intelligence`.
- Page architecture → `conversion-architecture`; copy → `conversion-copy`.
- Visual implementation → `frontend-system`; search demand/regression → `seo-intelligence`.

## Invariants

- Qualified, progressed, and won outcomes outrank clicks, CTR, and raw request
  volume. A click lift cannot win while lead quality falls.
- Never infer causality from a simple pre/post comparison. Name seasonality,
  traffic-mix, sales-process, campaign, and tracking changes as confounders.
- Do not call a low-volume rollout an A/B test. Use a directional observation
  and return `INSUFFICIENT` when the predeclared data gate is not met.
- Never change two funnel layers in one learning cycle.
- Never choose the metric, window, guardrail, or threshold after seeing the
  result.
- Never put names, email addresses, phone numbers, free text, click IDs, or raw
  CRM records into analytics events, committed files, or reports.
- Do not add pixels, analytics libraries, consent banners, GTM/GA4 changes, or
  external configuration unless explicitly requested.
- Never auto-revert. A revert candidate is a recommendation requiring an
  authorized implementation step.

Deliver: Keep candidate, Revert candidate or Insufficient; windows, volume,
freshness, primary outcome and guardrails; confounders; one next action and its
owner (Repo, Manual WP, Sales or External). Never call a candidate causal proof.
