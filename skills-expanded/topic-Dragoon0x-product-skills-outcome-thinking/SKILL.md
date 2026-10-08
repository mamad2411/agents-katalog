---
name: outcome-thinking
description: "Focus product work on outcomes rather than output. Covers defining success, connecting features to results, and knowing the difference between shipping and impact. Use when the team ships lots of features but metrics don't move, when success is defined by delivery dates, or when nobody can say what a feature accomplished."
---

# Outcome Thinking

Measure success by what changed, not what shipped.

## How to use

- `/outcome-thinking` Apply outcome thinking constraints to this conversation.
- `/outcome-thinking <initiative>` Define outcomes for the described initiative.

## Constraints

### Outcome Definition
- MUST define the desired outcome before defining the solution
- Outcomes MUST be measurable: "users are happier" is not an outcome. "NPS improves from 30 to 40" is.
- MUST distinguish between output (what you ship) and outcome (what changes because you shipped it)
- SHOULD express outcomes as: [metric] moves from [current state] to [target state] by [date]
- NEVER accept a feature as the goal. The feature is the hypothesis about how to achieve the goal.

### Connecting Work to Outcomes
- Every initiative MUST have a clear hypothesis: "If we build X, metric Y will improve because Z"
- MUST be able to draw a line from any team's current work to a measurable outcome
- If you can't connect work to an outcome, question whether it should be on the roadmap
- SHOULD break large outcomes into leading indicators the team can track weekly
- NEVER let "we shipped it" be the end of the story. Measure what happened next.

### Outcome Accountability
- MUST review outcomes after launching, not just celebrate the launch
- SHOULD set a review date at the beginning of every initiative
- MUST be honest when outcomes aren't met — understand why and adjust
- SHOULD distinguish between "the feature didn't work" and "we measured too early"
- NEVER move on to the next project without understanding if the last one achieved its goals

### Balancing Outcomes with Discovery
- Not everything can have a pre-defined outcome. Exploration and learning are valid goals.
- SHOULD set learning outcomes for discovery work: "We'll know X by the end of this"
- MUST still define what "done" looks like for exploratory work
- NEVER use "we're exploring" as an excuse for directionless work indefinitely

### Anti-Patterns
- Output Obsession: measuring success by features shipped, not impact created
- Outcome Theater: defining outcomes but never measuring them after launch
- Metric Fixation: optimizing a metric while the user experience degrades
- The Perpetual MVP: shipping minimum versions and never measuring if they worked
- Moving the Goalposts: changing the success criteria after the results are in
