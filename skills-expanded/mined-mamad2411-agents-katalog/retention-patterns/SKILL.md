---
name: retention-patterns
description: "Design for the second visit, not just the first. Habit loops, re-engagement triggers, and value reinforcement without dark patterns. Use when retention is low, when building engagement features, or when people stop coming back."
---

# Retention Patterns

Design for the second visit, not just the first.

## How to use

- `/retention-patterns` Apply retention constraints to this conversation.

## Constraints

### Habit Loop Design
- Trigger: what brings the user back (notification, routine, need)
- Action: what they do when they return (must be low-friction)
- Reward: what value they get (must be variable, not identical every time)
- Investment: what they put in that makes the product more valuable over time (data, content, connections)

### Retention Checkpoints
- Day 1: Did they experience core value?
- Day 7: Did they return without a prompt?
- Day 30: Has the product become part of a routine?
- For each checkpoint: what's the one thing that, if true, predicts long-term retention?

### Re-Engagement
- MUST bring value, not just reminders ("Your weekly summary" not "We miss you")
- SHOULD trigger based on user behavior, not calendar schedules
- MUST respect opt-out preferences absolutely
- NEVER use guilt or FOMO for re-engagement

### Anti-Patterns
- Streak mechanics that punish absence instead of rewarding presence
- Notifications designed to create anxiety
- Engagement features that benefit the platform but not the user
- Measuring DAU without measuring whether users got value from their visit
- Confusing addiction with loyalty
