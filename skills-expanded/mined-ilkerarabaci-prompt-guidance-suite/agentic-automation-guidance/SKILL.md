---
name: agentic-automation-guidance
description: specialize openai prompt guidance for agentic and automation-heavy work. use when the task involves multi-step execution, connector or tool orchestration, dependency-aware workflows, recurring procedures, status tracking, or semi-autonomous action with verification and safety checks.
---

# Agentic Automation Guidance

Use this skill for tasks that behave like workflows: discover, decide, act, verify, and report.

## Operating stance

- Treat the request as an execution graph, not a single response.
- Identify inputs, dependencies, side effects, and completion criteria before acting.
- Optimize for reliable follow-through with lightweight status visibility.
- Prefer reversible actions until preconditions are verified.

## Default workflow

1. Translate the request into a workflow with steps, dependencies, and outputs.
2. Resolve prerequisite discovery or retrieval before later actions.
3. Execute independent lookups in parallel when safe and useful.
4. Sequence dependent or irreversible actions carefully.
5. Track progress against a checklist of required deliverables.
6. Verify outcomes before declaring completion.
7. Report results, blockers, and remaining risk.

## Tool rules

- Use tools whenever they materially improve correctness, completion, or state awareness.
- Do not stop early when another tool call is likely to unlock or verify the task.
- Retry empty or partial results with a changed strategy before concluding failure.
- Do not parallelize steps when one result determines the next action.
- After parallel retrieval, synthesize before taking more actions.

## Safety and action rules

- Ask before destructive, irreversible, externally visible, or permission-sensitive actions.
- For reversible low-risk steps, proceed when the intent is clear.
- If a dependency is missing, state the blocker exactly.
- Keep an audit-friendly record of what was checked, executed, and verified.

## Output defaults

Unless the user requests another shape, return:

1. Goal
2. Status or outcome
3. Actions taken
4. Verification performed
5. Blockers or next step

## Style defaults

- Be operational, concise, and explicit.
- Prefer state-based reporting over narrative storytelling.
- Make it obvious what is done versus what remains.

For reusable templates, consult `references/automation_patterns.md`.
