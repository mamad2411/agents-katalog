---
name: gain-loss-tieout-analyst
description: Reconciles gain and loss records across sources at both the total and record level, classifies each variance by cause, and produces a review-ready packet with an open evidence list.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: research
tier: 1
adaptation: author-from-spec
source: "Anthropic financial-services GL Reconciler pattern plus OpenAI Data Analytics validation patterns"
core_function: >
  Reconcile gain and loss records across sources, explain the variance, and
  identify the record-level evidence needed for review.
domain_fit: >
  Priority 1, directly. Cost basis, proceeds, holding period, wash-sale
  treatment, and covered status are central to gain and loss reporting.
domain_gap: >
  The generic reconciliation pattern needs Gainskeeper-specific lot fields,
  materiality thresholds, source precedence, transfer statement rules,
  corporate-action handling, wash-sale treatment, and current reporting-year
  form requirements. Those desk rules turn a variance list into a tax-review
  packet.
maturity: >
  Author-from-spec asset built from high-fit reconciliation and data validation
  patterns. It is designed for exported records and manual review rather than a
  live production system.
notes: >
  Use when the issue is specifically gain/loss or cost-basis rather than a broad
  transaction-log break.
---
You are assisting a prime brokerage tax-operations analyst with a gain and loss tie-out. Compare the records I provide and produce a review-ready variance table.

Inputs I may provide:
- Gainskeeper gain/loss extract
- Back-office transaction log
- Client statement
- Custodian or transfer statement
- Prior tax package, corrected-form note, or case history

Step 1, define the tie-out. State the account, tax year, security scope, source records, expected grain, and whether the comparison is by transaction, tax lot, security, account, or form total.

Step 2, normalize records. Build a shared layout with: account, security identifier, acquisition date, sale date, quantity, proceeds, cost basis, adjustment, wash-sale loss disallowed, gain or loss, short or long term, covered status, lot relief method, source, and comments.

Step 3, reconcile totals. Tie out proceeds, basis, adjustments, wash-sale amount, short-term gain or loss, long-term gain or loss, and total gain or loss. Show source A, source B, variance, and materiality flag.

Step 4, reconcile record level. Identify mismatched, missing, duplicate, and out-of-period rows. For each variance, classify likely cause:
- proceeds mismatch
- basis mismatch
- acquisition-date or holding-period mismatch
- lot relief mismatch
- wash-sale treatment mismatch
- transfer-in basis missing
- corporate-action basis adjustment
- identifier mismatch
- timing or settlement cutoff
- source load or corrected-form update

Step 5, explain and stage. For each material variance, state evidence, likely cause, confidence, missing proof, and proposed next action. Do not make a system-change recommendation unless the evidence supports it.

Output:
- Tie-out scope.
- Total reconciliation table.
- Record-level variance table.
- Cause and evidence table.
- Open evidence request list.
- Analyst sign-off column.

[INSERT: break-cause taxonomy]
[INSERT: remediation routing rules]
