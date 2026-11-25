---
name: break-backlog-kpi-readout
description: Turn measured tax-ops operating performance into a leadership-ready KPI readout with definitions, comparisons, validated drivers, caveats, and next actions.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: communicate
tier: 1
adaptation: adapt
source: "OpenAI Data Analytics plugin, kpi-reporting skill"
core_function: >
  Turn measured operating performance into a leadership-ready status readout
  with definitions, comparisons, validated drivers, caveats, and next actions.
domain_fit: >
  Priority 1, directly. This packages break backlog, aging, close readiness,
  client impact, withholding exposure, and corrected-form risk for field and
  leadership communication.
domain_gap: >
  The source KPI skill must be given tax-ops metric definitions, close
  milestones, service expectations, queue ownership, break taxonomy, and risk
  thresholds. Once supplied, the readout can say whether the operation is on
  track for filing, correction control, client response, or issue closure.
maturity: >
  First-party OpenAI plugin skill available in this Codex environment. The
  source skill gives a strong KPI-readout structure, adapted here to tax-ops
  queue management and close reporting.
notes: >
  Use for WBR or MBR-style updates, close checkpoints, queue health, or a quick
  leadership status note after research.
---
You are assisting a prime brokerage tax-operations analyst. Create a leadership-ready KPI readout for a tax-reporting operating queue or close milestone.

Inputs I may provide:
- KPI actuals, targets, comparison period, and latest complete date
- Break backlog by age, form, cause, client, account, desk, or remediation path
- Prior readout, close calendar, service-level expectation, or issue notes
- Driver analysis or source-quality findings

Step 1, define the readout. State the audience, period, cutoff date, primary KPI, supporting metrics, target or service expectation, and what decision the readout supports.

Step 2, lock definitions. For each KPI, state numerator, denominator, grain, exclusions, source, comparison period, and whether the metric is complete through the cutoff date. Do not present a KPI as final if the definition or source is unclear.

Step 3, report the topline. Provide current value, prior or target value, absolute variance, percent variance where useful, and status. Use on track, watch, or at risk only when the basis is stated.

Step 4, explain drivers. Include only validated drivers or explicitly labeled hypotheses. Useful drivers include:
- aged breaks by cause
- unresolved withholding discrepancies by regime
- cost-basis breaks by product or security
- issuer reclass or corporate-action concentration
- account documentation gaps
- remediation path bottlenecks
- client or field-impact concentration

Step 5, state risk and action. Connect the evidence to close risk, corrected-form risk, client communication risk, staffing need, or control risk. Recommend an action only when the evidence supports it. Otherwise name the next validation step.

Output:
- BLUF: current status and reason.
- KPI scorecard table.
- Driver table with evidence and confidence.
- Risks and mitigants.
- Field or leadership note in polished prose, ready to send.

[INSERT: break-cause taxonomy]
[INSERT: remediation routing rules]
[INSERT: income-type to tax-form mapping]
