---
name: communicating-decisions
description: "Communicate product decisions so teams understand not just what was decided but why. Covers framing, transparency about trade-offs, and handling disagreement gracefully. Use when decisions aren't sticking, teams are relitigating past calls, or when stakeholders feel left out."
---

# Communicating Decisions

Tell people what you decided, why, and what it means for them.

## How to use

- `/communicating-decisions` Apply decision communication constraints to this conversation.
- `/communicating-decisions <decision>` Draft communication for the described product decision.

## Constraints

### Decision Framing
- MUST lead with the decision, then explain the reasoning. Don't bury the headline.
- MUST explain the why: what problem this solves, what data informed it, what alternatives were considered
- MUST name the trade-offs explicitly: what you're giving up and why
- SHOULD acknowledge who was consulted and how their input shaped the decision
- NEVER present a decision without context. Context turns compliance into buy-in.

### Audience Calibration
- Engineering needs: what changes, technical implications, timeline impact
- Design needs: scope boundaries, user flows affected, quality bar expectations
- Leadership needs: strategic rationale, business impact, resource implications
- Sales/CS needs: customer-facing changes, messaging guidance, timeline for enablement
- MUST tailor depth and framing to each audience. One announcement doesn't fit all.

### Handling Disagreement
- MUST create space for disagreement BEFORE the decision is final
- SHOULD actively seek out the strongest counterargument and address it
- Once decided: expect disagree and commit. The decision is the decision.
- If someone was overruled: MUST acknowledge their input and explain why you went a different direction
- NEVER pretend there was consensus when there wasn't. Be honest about the call.

### Documentation
- Every significant decision MUST be written down with: what, why, who was involved, date, alternatives considered
- SHOULD be stored somewhere the team can reference later
- MUST update documentation if the decision gets revisited or changed
- NEVER leave decisions in chat threads where they get lost

### Anti-Patterns
- The Mystery Decision: "we're doing X now" with no explanation
- The Consensus Illusion: pretending everyone agreed when someone was clearly overruled
- Decision Amnesia: no record of why a decision was made, leading to revisits months later
- The Drip: communicating a decision slowly through hallway conversations instead of a clear announcement
- Relitigating: allowing decided issues to be reopened without new information
