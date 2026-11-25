---
name: mobile-app-product-systems
description: Design and review mobile app and mobile game product systems including refunds, promotions, subscriptions, in-app purchases, in-app ads, notifications, daily check-ins, rewards, entitlement states, retention loops, and store-compliant monetization UX. Use when building or auditing iOS/Android apps, mobile games, consumer apps, app-store monetization flows, or lifecycle engagement systems.
---

# Mobile App Product Systems

Use this skill to design mobile app systems that monetize and retain without becoming manipulative, brittle, or store-policy risky.

## Resolve the surface

Classify the request into one or more surfaces:

- **Commerce**: refunds, subscriptions, IAP, entitlements, restore purchases, receipts.
- **Promotion**: discounts, bundles, limited-time offers, win-back, campaign targeting.
- **Ads**: IAA placement, rewarded ads, frequency, mediation, ad fatigue.
- **Retention**: daily check-in, streaks, missions, rewards, lifecycle messaging.
- **Notifications**: push permission, transactional, lifecycle, promotional, quiet hours.
- **Trust**: receipts, support, cancel flow, refund clarity, parental/age-sensitive UX.

Then read only the relevant references:

- General systems: `references/mobile-systems-rules.md`
- Refunds, revocation, repurchase, and abuse handling: `references/refund-and-entitlement-patterns.md`
- Promotions, offers, eligibility, placement, and campaign measurement: `references/promotion-system-patterns.md`

## Workflow

1. Identify the user state: new, activated, payer, subscriber, lapsed, refunded, churn-risk, or high-value.
2. Identify the business model: paid app, subscription, consumable IAP, non-consumable IAP, ads, hybrid, or game economy.
3. Apply the trust gate before recommending monetization or engagement tactics.
4. Design the state machine, not just the screen: eligibility, entitlement, cooldown, failure, restore, refund, and support states.
5. Produce UX, events, edge cases, and policy/trust guardrails together.
6. For refund or promotion work, include a decision table or state machine rather than generic advice.

## Trust gate

Do not propose a tactic unless it passes all checks:

- The user can understand the cost, benefit, and renewal/expiry state.
- The system has a clear path for restore, refund help, cancellation, and support.
- Promotions do not fake scarcity or hide material terms.
- Notifications are permission-aware, relevant, and rate-limited.
- Rewards and streaks do not punish healthy breaks or exploit compulsion.
- Ads do not interrupt critical tasks or degrade first-run trust.

## Output format

```text
System: <commerce | promotion | ads | retention | notifications | trust>
User states: <states>

Recommended design:
- <flow/state/rule>

Events to track:
- <event_name> { properties }

Edge cases:
- <case and expected behavior>

Risks:
- <policy/trust/product risk and mitigation>
```
