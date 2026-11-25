---
name: task-execution
version: 1.0.0
description: Meta-cognitive methodology for selecting actions, monitoring progress, and adapting plans during execution
uses:
  - planning/strategic-planning
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - execution:manage
  requires_approval: false
---

# Task Execution

Meta-cognitive methodology for selecting actions, monitoring progress, and adapting plans during execution. This skill governs HOW to think about execution, not the execution machinery itself.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `execute_task` is invoked, you (the agent) apply the methodology below to manage task execution using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `execution/task-execution` in its skill list.

**Important**: This skill provides the cognitive framework for execution management. It does NOT replace the agentic execution loop (agent_runner), tool dispatching, or message handling infrastructure. Those are system concerns. This skill is about decision-making during execution.

## When to Use

- Multiple valid next actions exist and you need to choose which to pursue
- A plan is being executed and progress needs to be assessed against expectations
- An assumption in the plan has proven wrong and the approach needs adaptation
- Execution is stuck and you need a structured way to diagnose and unblock
- A task has unclear completion criteria and you need to determine when to stop
- Resource constraints require trade-off decisions during execution

## Methodology

### 1. Assess Current State

Before selecting any action, understand where you are:
- **Plan position**: Which step in the plan are you on? What's done, what's remaining?
- **Assumptions check**: Are the assumptions that informed the plan still valid?
- **Resource state**: What resources remain? (time, tokens, API calls, budget)
- **Blockers**: Is anything preventing forward progress?
- **Changed conditions**: Has anything changed since the plan was made?

### 2. Select Next Action

When multiple valid next actions exist, evaluate using these criteria:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Dependency** | Does anything else depend on this completing first? | Highest — always do blocking work first |
| **Risk reduction** | Does this action reduce uncertainty or validate an assumption? | High — early risk reduction prevents wasted effort |
| **Effort vs. impact** | What's the ratio of effort required to value delivered? | Medium — prefer high-impact, low-effort actions |
| **Reversibility** | Can this action be undone if it's wrong? | Medium — prefer reversible actions when uncertain |
| **Information gain** | Will completing this reveal information needed for other decisions? | Medium — information-gathering actions enable better future decisions |

**Decision rule**: When in doubt, choose the action that reduces the most uncertainty with the least effort. Uncertainty is the enemy of good execution.

### 3. Define Done

Before starting an action, state explicitly:
- **Completion criteria**: What specific outcome means this action is done?
- **Time box**: How long should this take? When should you stop and reassess?
- **Quality bar**: What's the minimum acceptable quality? (perfect is the enemy of done)
- **Abort criteria**: Under what conditions should you stop this action and try something else?

### 4. Monitor Progress

During execution, periodically assess:
- **Am I making progress?** Is the gap between current state and completion criteria shrinking?
- **Am I on track?** Is effort matching expectations, or is this taking longer than expected?
- **Are assumptions holding?** Is the information I based my approach on still valid?
- **Should I continue?** Has new information emerged that changes whether this action is worth completing?

**Progress signals:**
- Positive: Intermediate results match expectations, dependencies are resolving, confidence is increasing
- Negative: Same error recurring, effort exceeding time box, new blockers emerging, scope expanding
- Neutral: Steady progress but slow — consider whether the approach is right or just needs more time

### 5. Adapt When Needed

When progress stalls or assumptions fail, follow this escalation:

**Level 1 — Adjust tactic** (stay on same action, change approach):
- Try a different method to achieve the same goal
- Reduce scope to get a partial result
- Seek more information before continuing

**Level 2 — Skip and return** (move to next action, come back later):
- Park the blocked action with notes on what's needed
- Pick up a non-blocked action to maintain progress
- Set a trigger for when to revisit ("return when X is resolved")

**Level 3 — Replan** (revise the plan):
- An assumption was fundamentally wrong
- A new constraint has emerged
- The goal itself has changed
- Use `create_plan` to revise the approach

**Level 4 — Escalate** (seek help):
- You've exhausted approaches at your level
- A decision requires authority you don't have
- The task is blocked on an external dependency you can't resolve

### 6. Know When to Stop

Execution is complete when ANY of these conditions are met:
- **Success**: All completion criteria are satisfied
- **Good enough**: The output meets the minimum quality bar and further refinement has diminishing returns
- **Time box expired**: The allocated time is consumed — deliver what you have with a status report
- **Blocked**: All remaining actions are blocked on external dependencies — report the blockers
- **Abort**: Abort criteria are met — stop, report why, and recommend next steps

**Danger signals that you should stop:**
- You're polishing something that's already done (perfectionism trap)
- You're repeating the same approach hoping for different results (insanity loop)
- You've exceeded the time box by 2x with no completion in sight
- New information has made the original goal irrelevant

## Output Format

```
## Execution: [Task]

### Current State
- Plan position: Step [X] of [Y]
- Assumptions: [Valid / Invalidated — which ones]
- Resources remaining: [Time, budget, etc.]
- Blockers: [None / List]

### Action Selected
- Action: [What to do next]
- Rationale: [Why this action, using selection criteria]
- Completion criteria: [Specific outcome]
- Time box: [Duration]
- Abort criteria: [When to stop]

### Progress Assessment
- Status: [On track / At risk / Blocked / Complete]
- Adaptation: [None needed / Level 1-4 — description]

### Outcome
- Result: [What was achieved]
- Completion: [Met criteria / Partial / Aborted]
- Next action: [What follows]
```

## Quality Criteria

- Action selection uses explicit criteria, not gut feeling
- Completion criteria are defined before execution starts
- Time boxes are set and respected
- Progress is assessed against expectations, not just activity
- Adaptation follows the escalation levels in order
- Stop conditions are recognized and acted on
- Reasoning for decisions is documented

## Common Mistakes

- **Acting without assessing**: Jumping to the first action that comes to mind without checking current state or evaluating alternatives
- **No completion criteria**: Starting an action without defining what "done" looks like leads to endless polishing or premature stopping
- **Ignoring time boxes**: Running over time without reassessing whether the approach is right. If it's taking 3x longer than expected, the approach is likely wrong.
- **Escalating too fast**: Jumping to Level 3 (replan) when a Level 1 (adjust tactic) would suffice. Try simpler adaptations first.
- **Not escalating soon enough**: Spending hours on a blocked action when escalating to Level 4 would unblock in minutes
- **Confusing activity with progress**: "I've been working on this for 2 hours" is activity. "I've completed 3 of 5 acceptance criteria" is progress.
- **Sunk cost fallacy**: Continuing an approach because of time already invested, even though a different approach would be faster from here
- **Perfectionism trap**: Refining an output that already meets criteria. If it passes the quality bar, ship it.

## Completion

Task execution management is complete when:
- Current state is assessed against the plan
- Next action is selected using explicit criteria
- Completion criteria are defined before execution
- Progress is monitored against expectations
- Adaptations follow the escalation levels when needed
- Stop conditions are recognized and the appropriate action is taken
