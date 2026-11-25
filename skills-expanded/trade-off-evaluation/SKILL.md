---
name: trade-off-evaluation
description: "Make product trade-offs explicitly and defend them clearly. Covers scope vs. quality, speed vs. polish, and knowing what to sacrifice without destroying value. Use when facing competing priorities, deciding what to cut, or when stakeholders want everything without acknowledging constraints."
---

# Trade-Off Evaluation

Make trade-offs explicit so the team can disagree with the decision, not discover it by accident.

## How to use

- `/trade-off-evaluation` Apply trade-off constraints to this conversation.
- `/trade-off-evaluation <trade-off>` Evaluate a specific product trade-off.

## Constraints

### Making Trade-Offs Visible
- MUST name the trade-off explicitly: "We're choosing X at the cost of Y because Z"
- MUST document trade-offs in writing so the team knows what was sacrificed and why
- SHOULD present trade-offs to stakeholders as options with consequences, not decisions already made
- NEVER make trade-offs silently and hope nobody notices
- MUST revisit trade-offs when the context that drove them changes

### Common Trade-Off Dimensions
- Scope vs. timeline: ship less on time or ship more late?
- Quality vs. speed: polish now or iterate after launch?
- Flexibility vs. simplicity: support every use case or nail the primary one?
- Short-term vs. long-term: quick fix now or proper solution later?
- One segment vs. another: optimize for power users or new users?
- MUST identify which dimension is actually in tension. Often the real trade-off isn't obvious.

### Evaluation Framework
- MUST define what you're optimizing for before evaluating the trade-off
- SHOULD ask: what's the worst case if we choose option A vs. option B?
- MUST consider reversibility: prefer reversible decisions. Be more careful with irreversible ones.
- SHOULD estimate the cost of being wrong for each option
- NEVER evaluate trade-offs in a vacuum — context determines which side is better

### Communicating Trade-Offs
- MUST frame trade-offs in terms of user and business impact, not technical details
- SHOULD present options with clear pros, cons, and your recommendation
- MUST own the trade-off you chose — don't blame constraints or other teams
- NEVER present a trade-off as having no downsides. Everything has a cost.

### Anti-Patterns
- The False Dichotomy: presenting two options when more exist
- The Hidden Trade-Off: making cuts without telling stakeholders what was sacrificed
- Analysis Paralysis: spending more time evaluating the trade-off than it would take to try both
- The Everything Approach: refusing to make trade-offs and ending up with a bloated, unfocused product
- Retroactive Justification: making the decision on gut then constructing the rationale after
