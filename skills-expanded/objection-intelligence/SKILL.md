---
name: objection-intelligence
description: When the user wants to discover, classify, prioritize, trace, or maintain recurring buyer objections from sales and customer evidence. For final rep responses and handling materials, see sales-enablement; for research design, see customer-research.
metadata:
  version: 1.0.0
---

# Objection Intelligence

Maintain an evidence-based library of buyer objections. Own discovery,
classification, prioritization, traceability, and refresh. `sales-enablement`
owns final talk tracks and objection-handling collateral.

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

## Inputs and evidence

Read `../_shared/evidence-gaps.md` and `../_shared/ssot-consumption.md` when
using canonical messages or approved responses. Use sales calls, win/loss work,
customer research/VoC, CRM notes, security reviews, procurement feedback, and
seller reports. Label the reporter/source type; seller feedback is not buyer
evidence. Never invent customer wording or proof.

## Workflow

1. Define scope and period. Deduplicate records without erasing distinct
   personas, stages, or contexts.
2. Capture objection text, source and date, persona, segment, funnel stage,
   category, frequency and denominator, severity/deal impact, current response,
   supporting proof, confidence, and unresolved gap where available.
3. Classify as useful into capability, competitor, status quo, price, ROI,
   security, compliance, implementation, integration, procurement, trust/proof,
   timing, or organizational change. Keep a distinct category when needed.
4. Prioritize frequency, severity, and confidence separately. Rare deal blockers
   can outrank frequent low-impact concerns. Do not infer deal impact from
   mention count alone.
5. Compare contexts only when evidence supports it. Preserve conflicting
   evidence and note whether the same phrase represents different concerns.
6. Maintain version/date and evidence links so future reviews can confirm,
   merge, split, retire, or reopen entries.

## Required output: objection library

Include Inputs and assumptions; scope and sample; then a reusable table:

| ID | Objection / exact language | Source type and evidence | Persona / segment / stage | Category | Frequency | Severity / impact | Confidence | Current approved response / proof | Gap / owner |
|---|---|---|---|---|---|---|---|---|---|

Include prioritization rationale, unresolved disagreements, evidence gaps, and
handoffs. Route response creation to `sales-enablement`. Route repeated
positioning or messaging concerns to `positioning-strategy` or
`messaging-framework`; possible canon revisions go through `ssot-context-loop`
with human approval. VoC language may be consolidated in `customer-research`.

## Safety and quality checks

- Keep frequency, severity/materiality, and confidence distinct.
- Mark unsupported responses or proof as Gap; never imply an unapproved response
  is canonical. Do not silently change the SSOT.
- This evidence library is normally internal, not a market-facing artifact for
  `messaging-consistency-audit`.
- **Output quality:** `output-quality-check` can independently verify source
  traceability, required fields, separation of frequency/severity/confidence,
  persona/stage differences, evidence gaps, correct routing, and no invented
  proof or canon changes.

## Related skills

`customer-research`, `win-loss-intelligence`, `sales-enablement`,
`positioning-strategy`, `messaging-framework`, `ssot-context-loop`,
`output-quality-check`.
