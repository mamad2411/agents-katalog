---
name: daily-reward-and-streak-review
description: Design and audit daily rewards, check-ins, streaks, missions, calendars, streak repair, lifecycle notifications, retention loops, live events, game economies, habit formation, and anti-abuse controls for apps and games. Use when building daily login rewards, streak mechanics, reward calendars, return rituals, or retention systems that should increase engagement without coercion.
---

# Daily Reward And Streak Review

Use this skill to make daily retention loops motivating, fair, and economy-safe.

## Workflow

1. Identify the core behavior the product wants to reinforce and the user value of returning.
2. Read `references/daily-reward-streak-systems.md`.
3. Map reward cadence, streak state, missed-day handling, notifications, economy impact, and abuse controls.
4. Separate healthy habit reinforcement from punishment, pressure, or low-value farming.
5. Produce a loop design with state model, reward table, metrics, and experiment guardrails.

## Guardrails

- Do not make the product depend on anxiety or loss aversion as the main value.
- Do not create rewards that undermine pricing, progression, or marketplace fairness.
- Provide recovery paths for missed days when long-term trust matters more than strict streak purity.

## Output format

```text
Core return behavior:
Reward promise:

Loop design:
- cadence, trigger, reward, recovery, cap

State model:
- <state> -> entry, exit, user message

Economy/support risks:
- <risk> -> mitigation

Metrics:
- activation, repeat, long-term retention, fatigue, economy impact
```
