---
name: problem-articulation
description: "Define user problems with enough clarity and specificity that the team can evaluate solutions against them. Covers problem framing, user evidence, and the gap between stated and real problems. Use when the team can't agree on what problem they're solving, solutions aren't landing, or feature requests are mistaken for problems."
---

# Problem Articulation

Define the problem so clearly that the right solution becomes obvious.

## How to use

- `/problem-articulation` Apply problem articulation constraints to this conversation.
- `/problem-articulation <context>` Sharpen the problem definition for the described situation.

## Constraints

### Problem Statement Structure
- MUST name the specific person experiencing the problem (role, context, situation)
- MUST describe what they're trying to accomplish and what prevents them
- MUST state the impact: what happens when this problem isn't solved?
- SHOULD express the problem in the user's language, not internal jargon
- NEVER include a solution in the problem statement. "We need a dashboard" is a solution, not a problem.

### Depth
- MUST distinguish between the stated problem and the root problem
- "I need a way to export data" might really be "I need to report to my boss weekly and I can't get the numbers I need"
- SHOULD ask "why?" at least 3 times to get to the underlying need
- MUST validate problem statements with actual user evidence (quotes, data, observed behavior)
- NEVER assume you understand the problem without talking to people who have it

### Scoping
- MUST define the boundaries: whose problem is this? In what context? How often?
- SHOULD quantify when possible: how many users, how often, how severe
- MUST separate the problem worth solving from adjacent problems that are tempting to include
- NEVER define the problem so broadly it can justify building anything
- NEVER define it so narrowly it can only justify one specific solution

### Validation
- MUST check: can the team read this problem statement and agree it's worth solving?
- SHOULD ask: if we solved this perfectly, would users notice and care?
- MUST compare against alternatives: how do users solve this problem today?
- NEVER build for a problem only one user has without checking if it's widespread

### Anti-Patterns
- Solution Masquerading as Problem: "we need a notification system" isn't a problem
- The Assumed Problem: the PM thinks users have a problem they've never actually expressed
- The Vague Problem: "users find it hard to use" — which users? Which part? How hard?
- Problem by Proxy: the stakeholder's problem ("sales needs this feature") confused with the user's problem
- Problem Drift: starting with one problem and gradually shifting to a different one mid-project
