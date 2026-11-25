---
name: do-subtasks
description: Executes exactly one approved subtask at a time, then returns a conventional commit message suggestion for human review and commit. Use when the user wants strict one-task-at-a-time implementation with manual commit control and explicit "next task" prompts.
---

# Do Subtasks

## Workflow

1. Implement exactly one subtask at a time.
2. Do not begin additional subtasks in the same response.
3. When that subtask is complete, stop implementation and return only a conventional commit message suggestion.
4. The commit message must have no scope and no body.
5. The human reviews and commits; do not commit automatically.
6. Wait for the human to tell you to move to the next task.

## Next-task behavior

- When the human tells you to continue, begin work immediately.
- Do not ask for confirmation.
- Do not restate or confirm which task you are starting.
- If the human asks for the next subtask and there are no remaining agreed-upon subtasks, do not implement anything.
- In that case, tell the human that all agreed-upon subtasks have already been implemented.

## Output Rules

- At subtask completion, output a single-line conventional commit message only.
- Allowed format: `<type>: <short description>`
- No scope section like `feat(api): ...`
- No body text, bullets, or extra commentary.
