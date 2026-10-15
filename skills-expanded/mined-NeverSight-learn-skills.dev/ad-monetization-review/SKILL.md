---
name: ad-monetization-review
description: Design and audit in-app advertising monetization for mobile apps, games, web apps, and content products including rewarded ads, interstitials, banners, native ads, offerwalls, mediation, frequency caps, payer suppression, privacy consent, UX placement, revenue analytics, and ad fatigue. Use when adding ads, improving ARPDAU, balancing IAA with IAP/subscriptions, or reducing churn from ads.
---

# Ad Monetization Review

Use this skill to make ads a measured monetization system rather than an interruption tax.

## Workflow

1. Identify product type, session loop, monetization mix, audience age/privacy constraints, and ad formats.
2. Read `references/ad-monetization-systems.md`.
3. Map ad placements to user intent, natural breaks, reward value, and fatigue risk.
4. Define segmentation: new users, engaged users, payers, subscribers, lapsed users, children-sensitive contexts, and high-frustration states.
5. Produce a revenue plan with caps, consent, analytics, suppression rules, support cases, and experiment guardrails.

## Guardrails

- Do not place interstitials during critical tasks, payment, onboarding trust-building, or error recovery.
- Do not make rewards ambiguous before an ad starts.
- Do not optimize ad impressions without retention, payer conversion, privacy, and complaint guardrails.

## Output format

```text
Ad context:
Monetization mix:

Placement map:
- <placement> -> format, trigger, user state, cap, reward, risk

Policy/trust constraints:
- <constraint> -> product response

Experiment plan:
- hypothesis, variants, success metric, guardrail metric, stop rule

Instrumentation:
- <event> with key properties
```
