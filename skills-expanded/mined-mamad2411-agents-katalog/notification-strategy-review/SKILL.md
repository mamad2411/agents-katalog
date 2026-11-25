---
name: notification-strategy-review
description: Design or audit notification strategy across push, email, in-app messages, SMS, lifecycle messaging, reminders, games, SaaS, mobile apps, and desktop utilities. Use when planning permission prompts, notification taxonomy, user controls, retention campaigns, quiet hours, deliverability, fatigue, event triggers, or support-safe messaging.
---

# Notification Strategy Review

Use this skill to make notifications useful enough to deserve attention.

## Workflow

1. Identify channel, user lifecycle stage, product promise, and message objective.
2. Read `references/notification-strategy-patterns.md`.
3. Classify messages by utility, urgency, consent, frequency, and failure risk.
4. Design permission timing, preferences, fallback, measurement, and support recovery.
5. Produce a notification taxonomy and experiment plan.

## Guardrails

- Do not use notifications to compensate for weak product value.
- Do not mix transactional, security, marketing, and engagement consent.
- Give users controls, quiet hours, and clear unsubscribe paths.

## Output format

```text
Notification objective:
Channels:

Taxonomy:
- <message type> -> trigger, user value, channel, frequency, control

Risks and guardrails:
- <risk> -> <guardrail>

Events:
- <event>
```
