---
name: tax-ops-dashboard-brief
description: Draft a dashboard brief that defines the metric model, layout, filters, and validation for a recurring tax-ops monitoring view.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: communicate
tier: 1
adaptation: adapt
source: "OpenAI Data Analytics plugin, build-dashboard skill"
core_function: >
  Define a monitoring surface around the audience question, metric model,
  source checks, layout, filters, validation, and handoff.
domain_fit: >
  Priority 2, strongly. A dashboard brief helps turn recurring break, close,
  withholding, cost-basis, and client-impact tracking into a repeatable view.
domain_gap: >
  The source dashboard skill needs desk-specific metrics, source authority,
  close cadence, follow-up dimensions, and tax-risk thresholds. The domain fill
  decides what belongs in the default view and what must remain a drill-down.
maturity: >
  First-party OpenAI plugin skill available in this Codex environment. The
  source skill is a dashboard-building specification, adapted here as a
  prompt-only brief for whichever assistant or reporting surface is available.
notes: >
  Use when a recurring queue view or close-monitoring page is needed, even if
  the final surface is a spreadsheet, offline HTML file, internal BI page, or
  pasted management pack.
---
You are assisting a prime brokerage tax-operations analyst. Draft a dashboard brief for a recurring tax-ops monitoring view. The brief must be usable by an analyst, manager, or report builder.

Inputs I may provide:
- Business question or recurring meeting
- Audience: analyst, manager, field team, leadership, or control owner
- Available extracts or named sources
- Metrics, targets, service expectations, and refresh cadence
- Known filters or dimensions

Step 1, state the dashboard purpose. Name the audience, operating question, decision the view supports, refresh cadence, and latest complete data rule.

Step 2, define the metric model. Pick the smallest useful set of metrics across:
- status: open breaks, aged breaks, close readiness, completed remediation
- movement: new, cleared, reopened, amended, or reclassed items
- risk: withholding exposure, corrected-form exposure, client-impact count, high-value accounts
- drivers: cause, form, income type, product, issuer, account documentation status, remediation path
- quality: source freshness, duplicate rate, missing documentation, unmatched identifiers

Step 3, define filters. Include only filters that change action: period, form, regime, client, account, desk, product, break cause, age bucket, remediation path, and owner.

Step 4, lay out the view. Put the default view in this order:
1. KPI strip with status and latest complete date.
2. Trend showing movement over the selected period.
3. Driver breakdown showing where attention is needed.
4. Aging or risk table for follow-up.
5. Source quality and caveat strip.

Step 5, define validation. State how the dashboard ties to the authoritative source, how freshness is checked, which totals must reconcile, and which caveats must be visible.

Output:
- Dashboard title.
- Audience and decision.
- Metric definitions table.
- Required filters.
- View layout.
- Source and validation checklist.
- Open questions before build.

[INSERT: break-cause taxonomy]
[INSERT: remediation routing rules]
[INSERT: income-type to tax-form mapping]
