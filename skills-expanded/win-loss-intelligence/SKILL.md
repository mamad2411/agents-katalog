---
name: win-loss-intelligence
description: When the user wants to understand why opportunities are won or lost, analyze closed-won or closed-lost evidence, or find segment and competitor patterns. Use for win/loss synthesis and route resulting decisions to strategy owners; for sales collateral, see sales-enablement, and for research design, see customer-research.
metadata:
  version: 1.0.0
---

# Win/Loss Intelligence

Explain why the company wins or loses, for whom, against what alternatives,
under which conditions, and what the evidence suggests should be reviewed.
Produce evidence and implications, not revised positioning or sales copy.

## Context research handoffs

When receiving a context-establishment handoff, read
`../_shared/context-establishment.md`. Reuse its question, scope, source/finding
IDs, approved context/version, GAP IDs and completion criteria. Analyze only your
owned domain; return provenance-bearing findings, opposing evidence, limitations,
completion status and unapproved implications to product-marketing-context.
Use decision-specific evidence readiness; approval is separate. A hold affects
only its decision. Do not write canon or automatically save chained results into
bootstrap context. Standalone artifacts retain their existing format and may
attach the shared return. Preserve IDs and status without duplicating studies.

## Before analysis

- Read `../_shared/evidence-gaps.md`, `../_shared/ssot-consumption.md`, and
  `../_shared/segment-selection.md` when comparing segments.
- Use applicable SSOT as a comparison point, never as a file to edit. Record
  relevant canon version/files and route contradictions through
  `ssot-context-loop` for human review.
- Inventory available closed-won/lost interviews, CRM reason codes, calls, AE
  notes, opportunity data, competitor evidence, and research. Record date range,
  inclusion rules, counts, missingness, and known selection bias.
- Distinguish buyer-reported reason, seller-reported reason, directly observed
  evidence, and inferred hypothesis. CRM loss codes are seller-entered signals,
  not buyer truth.

## Analysis

1. Define the question, cohort, and denominator. Separate closed outcomes from
   open or disqualified opportunities.
2. Code supported themes across segment, persona, company size, use case,
   competitor/alternative, deal size, funnel stage, geography, capability,
   price, implementation, integration, security/compliance, procurement,
   timing, and status quo. Leave unsupported dimensions unscored.
3. Separate frequency, severity/materiality, and confidence. Show counts and
   denominators where available. A small or biased sample cannot establish a
   rate or broad pattern.
4. Identify win/loss drivers, competitor and segment patterns, product,
   positioning, messaging, proof, pricing/packaging, sales-process issues,
   false assumptions, and unresolved questions only where evidence supports
   them. Do not classify every loss as competitive.
5. Include representative source-linked evidence. Use verbatim quotes only
   when present in actual source material. Preserve conflicting reports.
6. Route implications to the owner. Do not automatically rewrite any artifact.

## Required output

1. Inputs and assumptions, using shared evidence labels.
2. Executive summary and analysis question.
3. Evidence base: sample, outcome counts, period, sources, exclusions, bias,
   and limitations.
4. Win themes and loss themes, each with frequency, severity, confidence, and
   representative evidence where available.
5. Supported breakdowns by relevant segment/persona/alternative/stage.
6. Implications and handoffs, with unresolved questions and ranked evidence
   gaps. Suggested routes: Voice of Customer to `customer-research`, recurring
   objections to `objection-intelligence`, competitive evidence to
   `competitor-profiling`, positioning to `positioning-strategy`, messaging to
   `messaging-framework`, proof gaps to the evidence owner, price to
   `pricing-strategy`, and sales process to `sales-enablement` or `revops`.

## Safety and quality checks

- Never invent reasons, quotes, counts, rates, outcomes, or competitor claims.
- Mark missing buyer evidence as Gap; never promote seller interpretation to
  customer truth. Keep Sourced / Assumed / Gap labels; identify derivations as interpretation
  with formulas/source inputs, not a fourth label.
- Do not imply causality from association or attribute a win/loss to one factor
  when evidence supports multiple conditions.
- New findings may request SSOT review. Only `ssot-context-loop` manages
  canonical changes and required human approval.
- Internal analysis normally does not go to `messaging-consistency-audit`.
- **Output quality:** `output-quality-check` can verify cohort/denominators,
  source/report type, frequency/severity/confidence separation, quotes,
  limitations, supported breakdowns, explicit handoffs, and no silent canon
  change.

## Related skills

`customer-research` (research design and VoC), `objection-intelligence`,
`competitor-profiling`, `positioning-strategy`, `messaging-framework`,
`pricing-strategy`, `sales-enablement`, `revops`, `ssot-context-loop`,
`output-quality-check`.
