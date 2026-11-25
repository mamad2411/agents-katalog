---
name: cross-functional-alignment
description: "Bring engineering, design, research, marketing, and sales onto the same page and keep them there. Covers alignment levels, RACI clarity, and continuous maintenance. Use when teams have different understandings of what's being built, cross-team dependencies are causing problems, or alignment keeps breaking down."
---

# Cross-Functional Alignment

Get multiple teams with different incentives to agree on what to build, why, and when.

## How to use

- `/cross-functional-alignment` Apply alignment constraints to this conversation.
- `/cross-functional-alignment <initiative>` Build an alignment plan for the described initiative.

## Constraints

### Alignment Levels
Misalignment at a higher level poisons everything below it:
1. Vision alignment: do we agree on where we're going? (Check quarterly)
2. Strategy alignment: do we agree on how we'll get there? (Check monthly)
3. Execution alignment: do we agree on what we're doing this sprint? (Check weekly)
4. Tactical alignment: do we agree on today's priorities? (Check daily/async)
- MUST diagnose which level is broken before trying to fix execution details

### Decision Clarity
- Every key decision MUST have clear RACI: Responsible (does the work), Accountable (makes the call), Consulted (provides input), Informed (needs to know)
- MUST document alignment decisions in writing and make them accessible
- NEVER assume silence means agreement. Confirm explicitly.
- SHOULD end every cross-functional meeting with: what we agreed, what's unresolved, who owns next step

### Incentive Awareness
- MUST acknowledge that different teams have different incentives
- Engineering wants to reduce debt. Sales wants features. Marketing wants launches. These tensions are real.
- SHOULD surface incentive conflicts early rather than discovering them at deadline
- NEVER pretend tension doesn't exist. Name it and work through it.

### Communication Rhythm
- MUST establish predictable cadence for cross-functional check-ins
- Cadence should match project complexity: daily standups for launch sprints, weekly syncs for ongoing work
- SHOULD use async updates for status, sync meetings for decisions
- NEVER hold meetings that could be an email, or send emails that need to be a meeting

### Anti-Patterns
- Assumed Alignment: everyone nods in the meeting, everyone leaves with a different understanding
- Alignment by Email: sending a doc and assuming silence means buy-in
- Over-Alignment: meeting constantly about things that don't need group discussion
- Alignment Theater: running rituals without actually resolving disagreements
- Ignoring Incentive Conflicts: pretending engineering and sales want the same thing
