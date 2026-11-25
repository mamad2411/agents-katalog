---
name: request-a-customer-referral
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Ask a satisfied customer for a referral in a respectful, specific, and compliant way.

## Preconditions

- A customer with positive outcome, relationship health, and permission to contact.
- Account owner or customer success alignment on timing.
- Approved referral messaging, incentive policy, and tracking process.

## Steps

1. **Confirm customer readiness.** Review health score, recent support issues, renewal risk, stakeholder sentiment, and value achieved. → *Expect:* the customer is an appropriate referral candidate.
2. **Coordinate internally.** Check with account owner, customer success manager, or partner owner before asking. → *Expect:* the request will not conflict with account strategy.
3. **Choose the referral ask.** Decide whether to request an introduction, named account referral, testimonial path, or permission to mention your company internally. → *Expect:* the ask is specific and low-friction.
4. **Draft the message.** Thank the customer, name the outcome, make one specific ask, and offer a simple way to decline. → *Expect:* the message is respectful and clear.
5. **Review incentives and compliance.** Confirm whether referral rewards, disclosures, or procurement restrictions apply. → *Expect:* the request follows policy.
6. **Send through an approved channel.** [BRANCH: Salesforce | HubSpot | generic] send and log email from Salesforce; send and log email from HubSpot; in another CRM, send through the approved email or task workflow. → *Expect:* the request is sent or logged on the account.
7. **Track the response.** Create a task or campaign status to follow up, thank, or close the loop. → *Expect:* the referral request has a visible status.

## Decision points

- If the customer has open escalations → wait until the issue is resolved.
- If incentives are involved → confirm disclosure and anti-bribery policy before sending.
- If the referral would reveal confidential usage → ask only for an introduction the customer is comfortable making.

## Failure modes & recovery

- **F1 Poor timing:** detect customer dissatisfaction or renewal risk → cancel the ask and notify the account team.
- **F2 Vague request:** detect the customer would not know whom to refer → rewrite with target role, company type, or introduction path.
- **F3 Policy conflict:** detect restricted incentives or procurement rules → remove incentive language and seek internal guidance.

## Verification

The CRM account shows a sent or scheduled referral request with internal alignment, specific ask, compliance review, and follow-up status.

## Variations

- Executive sponsor ask: keep the message short and route through the relationship owner.
- Post-success milestone: ask soon after measurable value is delivered.
- Partner referral: coordinate with partner rules and attribution process.

## Safety & privacy

Medium outreach and compliance risk. Follow CAN-SPAM, GDPR, consent, opt-out, anti-bribery, incentive disclosure, and confidentiality rules; never pressure customers or expose their private business results without permission.
