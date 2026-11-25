---
name: coordination
version: 1.0.0
description: Decide what to delegate, to whom, and how to aggregate results across agents
uses:
  - planning/strategic-planning
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - coordination:execute
    - delegation:decide
  requires_approval: true
---

# Coordination

Decide what to delegate, to whom, and how to aggregate results across agents. This skill provides the cognitive layer for multi-agent collaboration — the decision-making about delegation, not the message-passing mechanics.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `coordinate` is invoked, you (the agent) apply the methodology below to make delegation and coordination decisions using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `collaboration/coordination` in its skill list.

**Important**: This skill provides the cognitive framework for coordination decisions. The actual message passing, task claiming, and agent discovery happen through the bus and HTTP server infrastructure. This skill is about WHAT to delegate and HOW to structure the collaboration, not the transport.

## When to Use

- A task is too large or complex for a single agent to handle efficiently
- Specialized skills are needed that the current agent doesn't have
- Parallel execution would significantly reduce total time
- Multiple perspectives or expertise areas need to contribute to a result
- Work needs to be handed off to another agent with proper context
- Results from multiple agents need to be combined into a coherent output

## Methodology

### 1. Assess Delegation Need

Not everything should be delegated. Evaluate:

| Factor | Delegate | Keep |
|--------|----------|------|
| **Skill match** | Requires skill you don't have | Within your skill set |
| **Parallelism** | Independent work that can run concurrently | Sequential dependency on your context |
| **Complexity** | Subtask is self-contained and well-defined | Subtask requires your ongoing context |
| **Context cost** | Context can be transferred cheaply | Transferring context would be expensive or lossy |
| **Quality** | Specialist would produce better results | You can produce equivalent quality |

**Decision rule**: Delegate when the task is self-contained, the delegatee has better skills, and the context transfer cost is low relative to the quality or speed gain.

### 2. Decompose for Delegation

Break work into delegatable units:
- Each unit must be **self-contained** — the delegatee can complete it without ongoing context from you
- Each unit must have **clear inputs** — what the delegatee receives
- Each unit must have **clear outputs** — what the delegatee returns
- Each unit must have **acceptance criteria** — how you verify the result
- Dependencies between units must be explicit

**Anti-patterns:**
- Units that require back-and-forth during execution (too coupled)
- Units where the output format is ambiguous (will cause integration failures)
- Units that share mutable state (will cause conflicts)

### 3. Select Delegatees

Match tasks to agents based on:
- **Skill match**: Which agents have the required skills in their skill list?
- **Availability**: Which agents are currently idle or have capacity?
- **Track record**: Have you delegated to this agent before? How did it go?
- **Cost**: What's the resource cost of delegation vs. doing it yourself?

Don't select based on:
- Agent name or identity (capability-based, not identity-based)
- Assumptions about agent quality (verify through skills, not labels)

### 4. Prepare Delegation Package

For each delegated task, prepare:

```
- Task: [Clear description of what to do]
- Input: [All data/context the delegatee needs]
- Output format: [Exactly what to return and in what structure]
- Acceptance criteria: [How the result will be evaluated]
- Constraints: [Time box, quality bar, scope limits]
- Priority: [Critical / High / Medium / Low]
- Dependencies: [What must complete before this starts, what this blocks]
```

**Context transfer rule**: Include everything the delegatee needs, nothing they don't. Too little context → the delegatee wastes time discovering it. Too much context → the delegatee wastes time filtering it.

### 5. Monitor Delegated Work

While work is delegated:
- Track which tasks are assigned, in progress, and complete
- Watch for blockers — agents stuck on delegated tasks need timely unblocking
- Don't micromanage — check progress at defined intervals, not continuously
- Be available for clarification requests

### 6. Aggregate Results

When delegated work returns:
- **Verify against acceptance criteria**: Does each result meet its criteria?
- **Check consistency**: Do results from different agents contradict each other?
- **Resolve conflicts**: Where results disagree, determine which is correct or synthesize
- **Integrate**: Combine results into a coherent whole, filling gaps at seams
- **Attribute**: Track which agent produced which contribution

### 7. Handle Failures

When delegated work fails or doesn't meet criteria:
- **Clarify and retry**: If the issue was unclear instructions, refine the delegation package and retry
- **Reassign**: If the agent lacks capability, route to a different agent
- **Absorb**: If delegation overhead exceeds the task cost, do it yourself
- **Escalate**: If the failure indicates a systemic issue, escalate to the orchestrator

## Output Format

```
## Coordination: [Overall Task]

### Delegation Assessment
- Total subtasks: [N]
- Delegated: [X] (reason: [skill gap / parallelism / specialization])
- Kept: [Y] (reason: [context-heavy / sequential / simple])

### Delegated Tasks

| # | Task | Delegatee | Skills Required | Status | Priority |
|---|------|-----------|-----------------|--------|----------|
| 1 | [Description] | [Agent/skill] | [Skills] | [Pending/Active/Done] | [H/M/L] |
| 2 | [Description] | [Agent/skill] | [Skills] | [Pending/Active/Done] | [H/M/L] |

### Integration Plan
- Aggregation strategy: [Merge / Synthesize / Select best / Combine]
- Conflict resolution: [How to handle disagreements]
- Gap coverage: [How to fill seams between delegated work]

### Results
- [Task 1]: [Status] — [Accepted / Rejected (reason) / Pending]
- [Task 2]: [Status] — [Accepted / Rejected (reason) / Pending]

### Final Output
[Integrated result or reference to it]
```

## Quality Criteria

- Delegation decision is justified (not arbitrary)
- Each delegated task is self-contained with clear inputs, outputs, and criteria
- Context transfer is sufficient but not excessive
- Results are verified against acceptance criteria before integration
- Conflicts between results are identified and resolved
- The integrated output is coherent (no gaps at seams)
- Failed delegations are handled through the escalation levels

## Common Mistakes

- **Delegating context-heavy work**: If transferring the context costs more than doing the work, don't delegate
- **Vague delegation**: "Research this topic" without specifying what output you need, in what format, by when. The delegation package must be complete.
- **Assuming skill from identity**: Don't assume "the developer agent" can code. Check its skill list. Delegate based on capabilities, not names.
- **No acceptance criteria**: Without criteria, you can't verify results. Every delegation needs explicit criteria defined upfront.
- **Micromanaging**: Checking delegated work every minute wastes both agents' time. Set intervals and trust the delegatee to work within them.
- **Ignoring integration**: Getting results from 3 agents and concatenating them produces an incoherent document. Budget time and effort for integration.
- **Delegating everything**: Some tasks are faster to do yourself than to package, delegate, wait, verify, and integrate. The delegation overhead must be less than the delegation benefit.
- **Not verifying results**: Accepting delegated work without checking it against criteria. Delegation is not abdication.

## Completion

Coordination is complete when:
- Delegation decisions are justified with explicit criteria
- Each delegated task has a complete delegation package
- All delegated results are received and verified against acceptance criteria
- Conflicts between results are resolved
- Results are integrated into a coherent output
- Failed delegations are handled (retried, reassigned, or absorbed)
