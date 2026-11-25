---
name: reflection
version: 1.0.0
description: Extract lessons, patterns, and improvement strategies from completed work
uses:
  - analysis/deep-analysis
  - validation/verification
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - memory:write
    - reflection:execute
  requires_approval: false
---

# Reflection

Extract lessons, patterns, and improvement strategies from completed work. Learn from both successes and failures to improve future performance.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `reflect` is invoked, you (the agent) analyze completed work to extract generalizable lessons using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `meta/reflection` in its skill list.

Persist learnings using the existing `memory_store` tool. Do not create a separate storage mechanism.

## When to Use

- After completing a significant task or project
- After a failure or unexpected outcome
- When the same type of mistake recurs
- At the end of a sprint, phase, or milestone
- Before starting similar work (reflect on last time first)
- When verification results reveal systematic gaps

## Methodology

### 1. Gather Evidence

Before reflecting, collect the raw material:
- **What was the goal?** Original objectives, success criteria, constraints
- **What happened?** Actual sequence of events, decisions made, actions taken
- **What was the outcome?** Final result vs. expected result
- **What did verification find?** Any verification reports, quality checks, test results
- **What was the timeline?** How long things took vs. estimates
- **What feedback was received?** User feedback, reviewer comments, stakeholder reactions

### 2. Identify What Worked

Explicitly acknowledge successes:
- What went better than expected? Why?
- What decisions turned out well? What made them good decisions?
- What processes or practices were effective?
- What would you repeat in similar future work?

Be specific. "The plan was good" is not a lesson. "Breaking the migration into 3 phases with rollback points prevented a production outage when Phase 2 failed" is a lesson.

### 3. Identify What Didn't Work

Examine failures and friction honestly:
- What went worse than expected? Why?
- Where were the bottlenecks or delays?
- What assumptions proved wrong?
- What risks materialized that weren't anticipated?
- What did verification catch that should have been caught earlier?

### 4. Extract Root Causes

For each significant failure or friction point, ask why:
- Use the 5 Whys or fishbone analysis (from `analysis/deep-analysis`)
- Distinguish between:
  - **Process failures**: The methodology was wrong
  - **Execution failures**: The methodology was right but wasn't followed
  - **Knowledge failures**: Missing information that wasn't sought
  - **Estimation failures**: Effort or risk was misjudged
  - **Communication failures**: Information didn't reach the right people

### 5. Formulate Lessons

Convert observations into generalizable principles:
- Each lesson should follow the pattern: **"When [context], [action] because [reason]"**
- Lessons must be actionable — they should change future behavior
- Lessons must be generalizable — they should apply beyond this specific case
- Classify each lesson:
  - **Strategy**: How to approach similar problems
  - **Process**: Steps to follow or avoid
  - **Estimation**: How to predict effort, risk, or outcomes
  - **Tool/technique**: Specific methods that work or don't

### 6. Define Improvements

For each lesson, specify a concrete change:
- **What to start doing**: New practices to adopt
- **What to stop doing**: Practices that hurt more than they help
- **What to change**: Existing practices that need adjustment
- Each improvement should be specific enough to act on immediately

### 7. Persist Learnings

Store lessons for future retrieval using `memory_store`:
- Use `memory_type: semantic` for generalizable lessons (facts and principles)
- Use `memory_type: procedural` for process improvements (how-to changes)
- Use `memory_type: episodic` for specific experiences to reference later
- Tag with relevant categories for retrieval (domain, skill, failure type)
- Include enough context that the lesson is useful without re-reading the full experience

## Output Format

```
## Reflection: [Subject/Project/Task]

### Context
- Goal: [What was intended]
- Outcome: [What actually happened]
- Duration: [Planned vs. actual]

### What Worked
1. **[Practice/Decision]**: [Why it was effective]
   Lesson: When [context], [action] because [reason].

2. **[Practice/Decision]**: [Why it was effective]
   Lesson: When [context], [action] because [reason].

### What Didn't Work
1. **[Issue]**: [What happened and impact]
   Root cause: [Category] — [Explanation]
   Lesson: When [context], [action] because [reason].

2. **[Issue]**: [What happened and impact]
   Root cause: [Category] — [Explanation]
   Lesson: When [context], [action] because [reason].

### Verification Insights
- [Patterns from verification results that inform future quality]

### Improvements
| Action | Type | Lesson Source |
|--------|------|--------------|
| Start: [new practice] | Process | [Which lesson] |
| Stop: [harmful practice] | Strategy | [Which lesson] |
| Change: [adjusted practice] | Estimation | [Which lesson] |

### Lessons Persisted
- [Lesson 1]: stored as [memory_type], tagged [tags]
- [Lesson 2]: stored as [memory_type], tagged [tags]
```

## Quality Criteria

- Both successes and failures are analyzed (not just failures)
- Root causes are identified, not just symptoms
- Lessons follow the "When [context], [action] because [reason]" pattern
- Lessons are generalizable beyond the specific case
- Improvements are concrete and immediately actionable (start/stop/change)
- Verification outputs are referenced when available
- Learnings are persisted via `memory_store` with appropriate types and tags

## Common Mistakes

- **Only reflecting on failures**: Successes contain equally valuable lessons. What worked and why is just as important as what failed.
- **Surface-level analysis**: "It took too long" is an observation, not a lesson. Ask why it took too long, and what would prevent it next time.
- **Non-actionable lessons**: "Be more careful" is not actionable. "Add a verification step before deploying database migrations" is actionable.
- **Non-generalizable lessons**: "Don't use library X" is too specific. "Evaluate library maturity before adopting — check release frequency, issue response time, and community size" is generalizable.
- **Skipping persistence**: Insights that aren't stored are lost. Always persist via `memory_store`.
- **Ignoring verification results**: If verification caught issues, those patterns should inform future quality practices. Reference verification outputs explicitly.
- **Blame over process**: Focus on process improvements, not individual blame. "The review step was skipped" is more useful than "person X didn't review."
- **Reflecting too late**: Reflect soon after completion while details are fresh. Delayed reflection produces vague, less useful lessons.

## Completion

Reflection is complete when:
- Both successes and failures are identified with specific evidence
- Root causes are classified (process, execution, knowledge, estimation, communication)
- Each lesson is generalizable and follows the "When/action/because" pattern
- Improvements are concrete (start/stop/change)
- Verification results are referenced where available
- Learnings are persisted via `memory_store` with appropriate types and tags
