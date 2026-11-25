# Implementer Subagent Prompt Template for Codex

Use this when dispatching a bounded implementation subagent with `spawn_agent`.

## Recommended Agent Type

- `worker` for code changes

## Required Inputs

- `{TASK_NAME}` — short task label
- `{TASK_DESCRIPTION}` — full task description from the controller
- `{CONTEXT}` — architectural or dependency context
- `{WORKDIR}` — repo path
- `{WRITE_SCOPE}` — files or modules this worker owns
- `{VERIFY_COMMAND}` — the most specific verification command for the task

## Template

```text
You are implementing `{TASK_NAME}`.

You are not alone in the codebase. Other agents may be working in parallel. Do not revert edits you did not make. Adjust to existing changes when needed.

## Task Description

{TASK_DESCRIPTION}

## Context

{CONTEXT}

## Ownership

You own changes in:
{WRITE_SCOPE}

Work from: `{WORKDIR}`

## Requirements

Before you begin, read the task carefully and raise any ambiguity immediately.
Do not guess about missing requirements.

Your job is to:
1. Implement exactly what the task specifies.
2. Follow existing code patterns in the repo.
3. Add or update tests when the task warrants them.
4. Run this verification before reporting back:
   `{VERIFY_COMMAND}`
5. Self-review your work before finishing.

## Self-Review Checklist

- Did I implement the requested behavior fully?
- Did I avoid overbuilding?
- Did I follow repo conventions and nearby patterns?
- Did I keep the change scoped to my owned files?
- Did I run the requested verification and read the output?

## Report Format

Return:
- what you changed,
- verification run and result,
- files changed,
- any follow-up concerns or limitations.
```
