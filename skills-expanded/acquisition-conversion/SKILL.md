---
name: acquisition-conversion
description: "Diagnose and improve acquisition conversion across landing pages, forms, popups and signup/account creation through registration or qualified handoff. Use for CRO, abandonment, demo requests and signup friction. Product activation and upgrades have separate owners."
metadata:
  version: 2.0.0
---

# Acquisition Conversion

## Approved context and evidence

Read `../_shared/evidence-gaps.md` and `../_shared/ssot-consumption.md`.
Load only relevant approved manifest context and record sources in Inputs and assumptions.
Read `../_shared/segment-selection.md` when an audience decision is needed; inherit accepted segments and ICP.
Separate sources, interpretation, and proposals. Missing evidence remains Assumed or Gap.
Do not edit SSOT. Route proposed canon changes to `ssot-context-loop` for human review and approval.

## Modes

Choose the journey bottleneck and load the relevant reference. Combine modes when the evidence spans steps.

| Mode | Decisions and reference |
|---|---|
| Landing/page | Message match, evaluation needs, proof, CTA hierarchy and traffic intent: [page](references/page.md). |
| Forms | Field justification, qualification versus completion, progressive profiling, errors, mobile and demo routing: [forms](references/forms.md). |
| Popups | Context, offer, trigger, suppression, frequency, dismissal and accessibility: [popups](references/popups.md). |
| Signup/account creation | Commitment expectations, authentication/SSO, verification, friction and abandonment: [signup](references/signup.md). |

## Workflow and output

1. Define the acquisition start, successful registration or qualified-handoff endpoint, audience, traffic source and denominator. Map each step and distinguish missing data from observed loss.
2. Diagnose message match, offer fit, buyer questions, trust and interaction friction. Justify every requested field and commitment. Do not optimize completion at the expense of qualified demand without showing the trade-off.
3. Produce Inputs and assumptions, journey/bottleneck diagnosis, Quick Wins, High-Impact Changes, prioritized Test Ideas, implementation acceptance criteria, and ranked Evidence gaps. Treat copy alternatives as proposals pending proof and canon checks.
4. Brief `marketing-copy` for final page/form/offer copy, `website-buyer-journey` for path changes, `email-sequence` for nurture/abandonment, and `revops` for qualified demo routing, SLA and recycling. Web/Product/Design own deployment and accessible interactions.
5. Define completion, qualification, downstream quality and customer-respect guardrails. Use `analytics-tracking` for measures and instrumentation requirements and `marketing-experimentation` for test design.

## Endpoint boundaries

Successful signup is the endpoint here. First value and stalled-user recovery route to `product-activation`; upgrade eligibility, timing and conversion route to `upgrade-conversion`.
Do not introduce deceptive urgency, impossible promises, involuntary opt-ins or blocked dismissal.
`output-quality-check` verifies the brief; `messaging-consistency-audit` independently reviews market-facing meaning. Launch clearance belongs to `launch-readiness-check`.

## Related skills

`marketing-copy`, `website-buyer-journey`, `product-activation`, `upgrade-conversion`, `revops`, `email-sequence`, `analytics-tracking`, `marketing-experimentation`.
