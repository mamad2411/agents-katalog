---
name: game-economy-review
description: Review and design game economy systems for mobile, PC, casual, live-service, and app-like games including currencies, sources/sinks, progression, rewards, daily check-ins, battle passes, IAP, ads, events, refunds, anti-abuse, fairness, and live-ops measurement. Use when building or auditing monetization and retention loops in games.
---

# Game Economy Review

Use this skill to make game economies sustainable, fair, and measurable.

## Workflow

1. Identify genre, session loop, audience, monetization model, and progression horizon.
2. Read `references/game-economy-patterns.md`.
3. Map sources, sinks, pacing, scarcity, offers, ads, events, refunds, and abuse vectors.
4. Check player trust, fairness, support recovery, and live-ops observability.
5. Produce economy risks, tuning levers, and event schema.

## Guardrails

- Do not recommend exploitative dark patterns, hidden odds, or coercive spend pressure.
- Separate ordinary refunds from abuse enforcement.
- Design for fun first; monetization should amplify value, not repair weak gameplay.

## Output format

```text
Game loop:
Monetization model:

Economy map:
- Sources:
- Sinks:
- Progression gates:
- Offers/events:

Risks and fixes:
- <rule id> <risk> -> <fix>

Events:
- <event>
```
