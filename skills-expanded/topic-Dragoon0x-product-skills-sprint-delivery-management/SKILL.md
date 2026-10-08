---
name: sprint-delivery-management
description: "Drive predictable delivery without micromanaging the engineering team. Covers sprint planning, blocker removal, scope negotiation, and knowing when to cut vs. push. Use when sprints consistently miss commitments, scope keeps creeping, or delivery feels chaotic."
---

# Sprint Delivery Management

Drive predictable delivery through clarity, not control.

## How to use

- `/sprint-delivery-management` Apply sprint delivery constraints to this conversation.
- `/sprint-delivery-management <situation>` Diagnose delivery issues for the described context.

## Constraints

### Sprint Planning
- MUST ensure every sprint item has clear acceptance criteria before committing
- MUST protect capacity: never plan 100% of available time. Leave buffer for bugs and surprises.
- SHOULD limit work in progress — too many things in flight means nothing gets finished
- NEVER commit to scope without engineering input on effort
- MUST prioritize ruthlessly: if everything is P0, nothing is P0

### Scope Management
- MUST define the minimum shippable version before starting work
- When scope needs to change mid-sprint, MUST trade: adding something means removing something
- SHOULD have a clear escalation path for scope disagreements
- NEVER silently expand scope. Make the trade-off visible.
- MUST distinguish between "nice to have in v1" and "actually required for v1"

### Blocker Removal
- PM's primary execution job is removing blockers, not tracking tickets
- MUST check for blockers daily, not just at standup
- SHOULD resolve cross-team dependencies before they become blockers
- NEVER let a blocked engineer sit idle when you could be escalating or finding alternatives
- MUST own unblocking even when the blocker isn't in your control

### Delivery Judgment
- MUST know when to cut scope to hit a deadline vs. when to slip to maintain quality
- SHOULD ask: "if we ship without this, will users notice?" If no, cut it.
- MUST communicate delays early with root cause and revised timeline
- NEVER surprise stakeholders with a miss at the end of the sprint

### Anti-Patterns
- The Ticket Manager: tracking JIRA instead of removing blockers and making decisions
- Scope Inflation: "just one more thing" every sprint until nothing ships on time
- The 100% Sprint: planning to capacity with zero buffer, then wondering why you miss
- Micromanaging: asking engineers for hourly updates instead of trusting the process
- Ignoring Velocity: planning the same amount of work every sprint regardless of team capacity trends
