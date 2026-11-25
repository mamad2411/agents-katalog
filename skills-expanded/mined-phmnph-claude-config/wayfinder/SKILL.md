---
name: wayfinder
description: Map unresolved decisions for a large initiative and work through their dependencies until a plan is actionable.
---

# Resolve a large initiative's unknowns

Use this when the route to a significant outcome is still unclear. Establish the
destination and whether the request covers planning only or also execution.
Reuse existing context and decisions. If the route is already clear, complete
the requested planning or implementation directly without inventing a map.

## Maintain the map

Use [MAP.md](MAP.md) as a starting shape when there is no existing convention.
The map names the destination, links decisions and their evidence, records
in-scope questions not yet precise enough to resolve, and marks exclusions.
Create decision records for questions that can be phrased now. Link prerequisites
so the next unblocked question is visible. Do not invent a complete task tree
before enough evidence exists.

Read tracker conventions from project instructions when available. Without a
configured tracker, local Markdown is sufficient. Use $setup-matt-pocock-skills
only if needed conventions remain unclear. External creation, assignment,
comments, and transitions require the user's authorization for those actions;
use existing authorization rather than asking again for every ticket. In a
shared tracker, claim work through the existing ownership mechanism and check
for concurrent changes before updating records. Refer to decisions by title.

## Resolve questions with the appropriate method

- **Research:** load $research when outside evidence is needed. Answer small
  questions directly; delegate independent investigations only when beneficial
  and permitted. Give delegated researchers a stopping rule and no further
  delegation. Do not create one worker automatically for every open question.
- **Prototype:** load $prototype when an observation or small artifact can settle
  a question. Human taste or preference requires the user's input; measurable
  technical observations can be assessed by the agent.
- **Discussion:** load $grilling for unresolved goals or material tradeoffs, and
  $domain-modeling when terminology or durable design decisions change. Choose
  routine engineering details from evidence instead of forwarding every choice.
- **Prerequisite task:** perform only the authorized work needed to unlock a
  decision, such as inspecting a data sample or obtaining environment facts.

Record the resolution and supporting artifact once, then update the map's index.
Add questions made concrete by the new evidence and revise dependencies. Preserve
the history of superseded or out-of-scope decisions according to project rules.

## Continue until the requested outcome is reached

Work through further unblocked questions while there is authorization, useful
progress, and budget. There is no one-ticket-per-session limit. If asked only to
chart the map, deliver the map. If asked to resolve it, continue until the plan is
actionable, a material human decision blocks progress, or the budget is reached.
At a blocker, record what is known and the next required decision; do independent
work that remains useful. Planning does not automatically authorize product
implementation, paid experiments, or deployment.
