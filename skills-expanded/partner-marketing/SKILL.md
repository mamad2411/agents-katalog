---
name: partner-marketing
description: When the user wants to plan a GTM partnership, joint launch, co-marketing, ecosystem, channel, referral, or co-sell motion. For joint events, coordinate with events; for partnership operations, corporate development, or M&A, use the appropriate non-PMM owner.
metadata:
  version: 1.0.0
---

# Partner Marketing

Plan GTM partnerships and co-marketing. Own the joint audience/value hypothesis,
narrative brief, contribution and approval map, activation plan, and learning.
Do not expand into corporate development, M&A, or generic partnership
operations.

## Integration marketplace presence

For approved integration listings read [marketplace brief](references/integration-marketplaces.md). Keep bilateral GTM and partner approval separate from referral incentive mechanics.


## Before planning

Read `../_shared/evidence-gaps.md` and `../_shared/ssot-consumption.md`.
Load the project manifest's relevant approved context and record sources used.
Read `../_shared/segment-selection.md` only when choosing audiences; inherit
accepted segment decisions without redefining canonical ICP.

## Workflow

Distinguish partner participants from end buyers when defining joint value
and handing audience intelligence to asset owners.

1. Define the business objective and partnership type: technology/integration,
   ecosystem, channel, strategic alliance, referral/co-sell, or joint launch.
2. Establish evidence for audience overlap, mutual customer value, partner
   capability, and each party's contribution. Mark unsupported assumptions.
3. Develop a joint narrative that preserves our approved canon. Label separately
   our approved claims, partner-approved claims, jointly approved claims, and
   unverified assumptions. Obtain explicit approval from both parties for joint
   claims and quotes.
4. Define offer/CTA, distribution, sales/co-sell motion, owners, approvals,
   dependencies, dates, measurement, and learning. Separate sourced outcomes
   from influence claims.
5. Route execution to channel owners and coordinate approval before publication.

## Required output

Inputs and assumptions; objective and audience overlap; mutual value; party
contributions; joint narrative and claim-status table; offer/CTA; distribution
and sales motion; asset/approval owners; measurement; risks and evidence gaps.
**Output quality:** `output-quality-check` can verify the required plan, claim
provenance/status, bilateral approvals, ownership, measures, and no fabricated
partner facts or proof.

## Handoffs and governance

This skill owns partner fit, mutual value, co-sell coordination, and joint
approvals. `referral-program` owns referral/affiliate mechanics, incentives,
and tracking. For a joint product release, `launch-strategy` owns release phases
and sequencing; this skill owns partner contributions and bilateral approvals.

Route joint event strategy to `events`; co-sell material to
`sales-enablement`; copy to `marketing-copy`; email to `email-sequence` or
`cold-email`; social activation to `social-content`; tracking to
`analytics-tracking`. This skill does not write final channel assets. Joint
market-facing messaging should pass `messaging-consistency-audit` and partner
approval. Any conflict with company canon goes to `ssot-context-loop` for
review; never change canon. A proposed quote remains `DRAFT / REQUIRES APPROVAL`
until approved by the named speaker and relevant parties.

## Related skills

`referral-program`, `launch-strategy`, `events`, `sales-enablement`, `marketing-copy`, `email-sequence`, `cold-email`,
`social-content`, `analytics-tracking`, `messaging-consistency-audit`,
`ssot-context-loop`, `output-quality-check`.
