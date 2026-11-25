---
name: multi-agent-runner
description: Run a manually-invoked workflow where multiple agents, optionally with user-specified models, attempt the same task and compare results. Use only when the user explicitly invokes this skill or asks to run a task with N models, best-of-N agents, multiple agent attempts, parallel proposals, competing implementations, or multi-agent task runs.
disable-model-invocation: true
---

# Multi Agent Runner

This skill is manual-only. Do not use it from ambient context. Use it only when the user explicitly invokes `multi-agent-runner` or clearly asks to run the same task through multiple agents.

## Primary Invocation

Optimize for this simple command shape:

```text
/multi-agent-runner fai la task seguente con questi N modelli: model-1, model-2, ...

[Task]
```

When the user provides both the model list and the task, do not ask for additional confirmation unless the request is unsafe, impossible, or missing a detail required to run the agents.

## Goal

Run one task through multiple agents, collect distinct attempts, compare them against the user's criteria, and help the user choose the best result.

Support two task modes:

- **General mode**: agents produce answers, plans, proposals, analyses, designs, or trade-off reviews without editing files.
- **Code mode**: agents implement or modify code in isolated worktrees so attempts remain separate and comparable.

## Start Checklist

Before launching agents, determine:

- The exact task.
- The expected output format.
- Whether this is **general mode** or **code mode**.
- The number of attempts. If the user lists models, the number of attempts equals the number of models.
- The decision criteria. Default to correctness, simplicity, maintainability, testability, and fit with the existing project.
- Any constraints: files to avoid, style requirements, time budget, models requested, or tests that must pass.

If the task and model list are clear, launch the agents. If something materially required is missing, ask one short clarification before launching agents.

## Agent Instructions

When the user lists models, give every model the same task, instructions, constraints, and success criteria. Do not assign artificial strategies by default. The goal is to compare model outputs under equivalent conditions.

Use varied strategies only when the user explicitly asks for different approaches, or when the user does not list models and wants multiple attempts from the same model.

Optional strategy set:

- **Conservative**: minimal, low-risk answer or implementation.
- **Pragmatic**: balanced solution optimized for clarity and maintainability.
- **Ambitious**: more comprehensive solution that may improve structure or UX if justified.

For more than 3 strategy-based attempts, add focused variants such as test-first, performance-focused, architecture-focused, UX-focused, or compatibility-focused.

## Model Selection

If the user names specific models, create one attempt per listed model and use exactly those models when they are available. Do not substitute a different model silently; if a requested model is unavailable, tell the user which model was unavailable and ask how to proceed.

If the user does not name models, default to the current model for all attempts. Use varied strategies only if multiple attempts would otherwise be identical.

If the user names models but not strategies, do not assign strategies. Run the same prompt against each model.

When the user does not name models and model choice matters, ask a short clarification before launching agents. Model choice matters when the user requests a high-cost code implementation, wants to compare model families, needs a specific style of reasoning, or asks for more than 3 attempts.

Recommended model assignment:

- **Claude**: architecture, trade-offs, refactors, reviews, and careful reasoning.
- **GPT/Codex**: implementation-heavy work, focused fixes, tests, and patch generation.
- **Gemini**: broad exploration, alternative perspectives, and second opinions.
- **Composer**: quick variants, lightweight attempts, and fast proposal generation.

Use this request format only when asking the user to choose models:

```text
Which models should I use for the attempts?

Default: use the current model for all attempts.
Optional: specify assignments like:
- Attempt 1: Claude, conservative
- Attempt 2: GPT/Codex, pragmatic
- Attempt 3: Gemini, alternative
```

## General Mode Workflow

Use this mode when the task is a question, proposal, plan, architecture option, review, explanation, or other non-editing work.

1. Launch multiple agents in parallel with read-only instructions when possible.
2. Ask each agent to return:
   - Short answer or proposal.
   - Key reasoning.
   - Assumptions.
   - Risks or weak points.
   - When this option is best.
3. Compare the results.
4. Present the best options clearly and recommend one if there is a clear winner.
5. Ask the user which direction to continue with when no option clearly dominates.

## Code Mode Workflow

Use this mode when agents need to create, modify, refactor, or test code.

1. Use isolated worktrees/branches for each attempt. Prefer the `best-of-n-runner` subagent type when available.
2. Give every attempt the same task, constraints, and success criteria.
3. Require each agent to return:
   - Summary of the implementation.
   - Changed files.
   - Tests or checks run.
   - Known risks.
   - Why this attempt should be chosen.
4. Do not merge or apply any attempt automatically.
5. Compare attempts by diff size, correctness, project fit, tests, maintainability, and risk.
6. Present the comparison and recommend the strongest attempt.
7. Apply or port the chosen implementation only after explicit user approval.

## Prompt Template For Agents

Use this shape when launching each agent:

```text
Task: [same task for every agent]

Mode: [general or code]
Model: [assigned model]
Success criteria:
- [criterion 1]
- [criterion 2]
- [criterion 3]

Constraints:
- [constraint 1]
- [constraint 2]

Return:
- Summary
- Main decisions
- Output or implementation notes
- Tests/checks run, if applicable
- Risks and trade-offs
- Recommendation
```

## Comparison Output

After all agents finish, respond with:

```markdown
## Recommendation
[One concise recommendation, or say there is no clear winner.]

## Comparison
- Attempt 1: [strengths, weaknesses, best use case]
- Attempt 2: [strengths, weaknesses, best use case]
- Attempt 3: [strengths, weaknesses, best use case]

## Next Step
[Ask which attempt to apply/continue with, or state the recommended next action.]
```

For code mode, include tests/checks run and any attempt that failed to build or pass tests.

## Guardrails

- Do not use this skill unless manually invoked.
- Do not launch code-writing attempts directly in the user's active branch.
- Do not apply, merge, or port an implementation without explicit user approval.
- Do not hide failed attempts; summarize why they failed.
- Keep the final comparison concise unless the user asks for detailed analysis.
