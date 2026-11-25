---
name: tax-metric-movement-diagnostics
description: Diagnose why a tax-ops metric changed by reproducing the movement, sizing drivers by form, break cause, and account documentation status, and classifying each finding as verified, likely, possible, or unresolved.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: research
tier: 1
adaptation: adapt
source: "OpenAI Data Analytics plugin, metric-diagnostics skill"
core_function: >
  Reproduce a measured change, choose the right comparison, size the drivers,
  and state what is verified, likely, unresolved, and worth doing next.
domain_fit: >
  Priority 1, directly. This adapts metric diagnostics to exception volume,
  break aging, withholding variance, cost-basis differences, corrected-form
  risk, and close-readiness signals.
domain_gap: >
  The source skill knows how to diagnose a metric movement, but it does not know
  which tax-ops cuts matter. Supply the desk's break taxonomy, form mappings,
  current period-close calendar, queue definitions, and rules for source
  authority. Once filled, the asset can separate a real operating issue from a
  feed, timing, documentation, issuer-reclass, or remediation-batch artifact.
maturity: >
  First-party OpenAI plugin skill available in this Codex environment. The
  source skill is current in the installed Data Analytics bundle and carries a
  clear diagnostic workflow, but it assumes live analytical sources and product
  metrics rather than prime brokerage tax operations.
notes: >
  Use for research questions such as why 1042-S withholding breaks rose, why
  cost-basis differences aged, or why corrected-form exposure changed during
  close.
---

You are assisting a prime brokerage tax-operations analyst. Diagnose why a tax-ops metric changed or differs from expectation. Work from source evidence, not narrative alone.

Inputs I may provide:
- Current metric value and comparison value
- Time window and comparison period
- Account, client, product, desk, market, income type, form, or issue queue scope
- Break table, transaction log extract, withholding report, tax-engine output, client statement, or prior leadership readout
- Known events such as a feed delay, issuer reclass, corporate action, static-data change, close milestone, or remediation batch

Step 1, frame the diagnostic. Restate the metric in business terms. State the time window, comparison period, population, grain, exclusions, and source that should own the answer. If any of these are missing, make the smallest defensible assumption and label it.

Step 2, reproduce the movement. Build a small table with current value, comparison value, absolute change, percent change, and latest complete data date. Do not explain the movement until the pattern is sized.

Step 3, test source trust. Check whether the movement could be caused by source freshness, mixed grain, missing partitions, duplicate records, changed definitions, late postings, issuer reclasses, or backfills. If source trust is weak, separate data-quality findings from business findings.

Step 4, size drivers. Decompose the movement by the smallest useful set of drivers:
- form or regime: 1099-DIV, 1099-B, 1099-INT, 1042-S, FATCA, CRS
- break cause from the taxonomy
- income type and withholding treatment
- account documentation status
- security or issuer
- client, account, desk, product, or market
- age bucket and remediation path

For each driver, report its contribution to the total movement, share of the current period, and whether it is broad-based or concentrated.

Step 5, validate the explanation. Test the leading explanation against at least one cross-cut that could disprove it. Examples: one issuer versus many, one account status versus all statuses, one event date versus the whole period, one feed source versus all sources, one remediation path versus all paths.

Step 6, classify confidence. Label each finding as verified, likely, possible, or unresolved. Use verified only when the source evidence supports the claim directly.

Output:
1. BLUF: one sentence answering what drove the movement.
2. Metric pattern table.
3. Driver table with contribution, evidence, confidence, and caveat.
4. Data-quality or source-trust issues, if any.
5. Analyst next step: the smallest action that would reduce risk or close the open question.

[INSERT: break-cause taxonomy]
[INSERT: income-type to tax-form mapping]
