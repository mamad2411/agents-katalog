---
name: hand-off-a-closed-deal-to-onboarding
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Transfer a closed-won deal to onboarding with the customer context, commitments, and owners needed for a clean start.

## Preconditions

- The deal is closed won or otherwise approved for onboarding.
- Contract, order form, products, start date, and customer contacts are available.
- A defined onboarding handoff process or intake form.

## Steps

1. **Open the closed deal.** Review account, contacts, products, amount, terms, and close notes. → *Expect:* the sold scope and customer context are visible.
2. **Confirm commercial completeness.** Check signature, billing details, products, implementation services, special terms, and start date. → *Expect:* onboarding will not start from an incomplete sale.
3. **Prepare handoff summary.** Capture customer goals, success criteria, stakeholders, risks, promised timelines, integrations, and support needs. → *Expect:* onboarding receives practical context.
4. **Create the handoff record.** [BRANCH: Salesforce | HubSpot | generic] create a case, task, project, or onboarding request from Salesforce; create a ticket, task, or workflow in HubSpot; in another CRM, use the approved onboarding intake object. → *Expect:* an onboarding-owned record exists.
5. **Attach or link documents.** Add contract, order form, proposal, security notes, and relevant meeting notes using approved storage links. → *Expect:* onboarding can access source documents.
6. **Assign owners and due dates.** Set onboarding owner, sales owner, kickoff target date, and first internal task. → *Expect:* ownership and timing are clear.
7. **Notify the onboarding team.** Send the handoff through the approved channel with the CRM link. → *Expect:* onboarding receives the handoff and can acknowledge it.

## Decision points

- If contract or billing details are missing → hold handoff and resolve with sales ops or finance.
- If special promises were made → escalate them clearly before kickoff.
- If the customer needs immediate contact → coordinate the first message with onboarding owner.

## Failure modes & recovery

- **F1 Missing scope:** detect onboarding asking what was sold → add products, quantities, terms, and proposal link.
- **F2 Unassigned handoff:** detect no onboarding owner → assign the correct queue or manager.
- **F3 Hidden commitment:** detect a promise only in email or call notes → add it to the handoff summary and flag risk.

## Verification

An onboarding-owned record exists with sold scope, documents, stakeholders, commitments, risks, owner, due dates, and notification to the onboarding team.

## Variations

- Enterprise implementation: include technical discovery, integrations, security, and project milestones.
- Self-serve onboarding: trigger automated welcome and internal monitoring instead of a full handoff.
- Partner-led onboarding: include partner owner and division of responsibilities.

## Safety & privacy

Customer contracts and implementation details are confidential. Share links only with authorized onboarding, finance, legal, and account team members.
