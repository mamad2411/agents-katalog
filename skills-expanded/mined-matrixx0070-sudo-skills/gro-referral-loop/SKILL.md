---
name: gro-referral-loop
version: 1.0.0
description: Design a referral or viral loop and compute its k-factor, cycle time, and amplification honestly.
author: matrixx0070
tags: [growth, referral, viral, k-factor, loops]
capabilities: []
---

## When to use

Use this when you want users to bring users — a referral program, invite flow, or content/collaboration loop. Reach for it to model whether a loop can meaningfully lower CAC and to design the incentive, trigger, and mechanics.

**Not for:** paid acquisition, one-off launch campaigns, or brand/content marketing (that's the marketing role). Also not a rescue for a product people don't like — viral loops amplify retention, they don't create it; fix retention first via gro-retention-analysis.

## Method

1. Map the loop as a cycle: user reaches a share trigger → sends invites → invitees land → invitees activate → become senders. Every stage is a multiplier you can measure and improve.
2. Compute k-factor = (invites sent per user) × (conversion rate per invite). k = i × c. Decision point: k ≥ 1 means self-sustaining exponential growth (rare); 0 < k < 1 still amplifies acquisition by 1/(1−k) — a k of 0.5 doubles every acquired user's downstream reach.
3. Measure cycle time (trigger → invitee becomes a sender). Two loops with equal k but different cycle time grow wildly differently; halving cycle time beats a small k bump.
4. Choose the incentive: one-sided (reward inviter), two-sided (reward both — usually best), or intrinsic (the product is better shared). Decision point: match the reward to real value and cap it against fraud/abuse economics.
5. Place the trigger at a moment of realized value (just after the aha-moment), not at signup. Reduce invite friction (prefilled message, native share, minimal fields).
6. Instrument every stage, model the amplification, and A/B the incentive and trigger placement via gro-ab-test-design. Watch payback: reward cost per activated referral must be < LTV.

## Example

Each activated user sends 4 invites (i=4); 12.5% convert (c=0.125). k = 4 × 0.125 = 0.5. Amplification = 1/(1−0.5) = 2×: every 1,000 paid signups yield ~2,000 total. Cycle time 6 days. Two-sided reward: $10 credit each, paid only on invitee activation. Payback fine if LTV > $20 per referred user.

## Pitfalls

- Reporting invites *sent* as success while conversion is near zero — k is what matters, not volume.
- Bolting a loop onto a product with weak retention; churned invitees never re-invite, so k collapses.
- Uncapped or pre-activation rewards inviting fraud and burning cash on fake accounts.
- Placing the invite prompt at signup, before the user has felt any value to share.

## Output format

```
Loop: <name>
Stages:      trigger → invites (i=<>) → landed → converted (c=<>) → sender
k-factor:    k = i × c = <> × <> = <>
Amplification: 1/(1−k) = <>×  | Cycle time: <days>
Incentive:   <one/two-sided/intrinsic>, reward=<>, paid on <activation>
Trigger:     <post-aha moment>
Economics:   reward cost/referral <$> < LTV <$>
Fraud cap:   <limit>
Validation:  A/B incentive + trigger via gro-ab-test-design
```
