---
name: cfo-briefing
description: Use when preparing a concise CFO-ready operating brief from finance data, KPIs, risks, cash, revenue, AR, forecast, and close-status inputs.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/cfo-briefing/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# CFO Briefing

Use this skill to turn messy finance inputs into an executive-ready operating brief.

## Inputs

- KPI exports, financial statements, forecast, pipeline, cash position, AR/AP aging, close status, and board or investor questions.
- Prior-period comparisons, budget, forecast, and materiality threshold.
- Known risks, decisions needed, and audience.

## Workflow

1. Identify the briefing audience and time horizon: weekly operator update, board prep, investor update, lender update, or internal leadership meeting.
2. Extract the most decision-relevant changes in cash, revenue, margin, burn, runway, collections, bookings, churn, forecast, and close status.
3. Separate facts, interpretations, risks, and asks.
4. Call out what changed since the prior period and why it matters.
5. Keep the brief short enough for an executive to scan before a meeting.

## Output

Return:

- Headline: one sentence on the state of the business.
- Metrics table with current value, prior value, plan/forecast, variance, and note.
- Key risks and mitigations.
- Decisions needed.
- Appendix items or data gaps.

## Guardrails

- Do not overstate precision when inputs are preliminary.
- Do not bury cash, runway, covenant, or collection risks.
- Do not invent causal explanations. Mark them as hypotheses if not proven.
- Keep customer-sensitive and employee-sensitive details out of general executive summaries unless needed.
