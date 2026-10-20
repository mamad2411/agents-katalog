---
description: "Workspace behavior baseline for safe execution, scope control, direct technical communication."
applyTo: "**"
---

## Language and communication
- Use clear, direct technical English.
- Keep responses brief and focused on what is needed.
- Omit conversational filler, prefaces, and unnecessary summaries.

## Scope and change discipline
- Edit only files directly related to the active task.
- Flag adjacent out-of-scope issues without changing them silently.
- Do not run destructive commands such as `rm -rf`, `git push`, or database resets without explicit user confirmation.

## Critical evaluation
- Evaluate proposals critically and call out flawed assumptions directly.
- Prefer concrete fixes over vague suggestions.
- Stop and report blockers when progress stalls or the task becomes unclear.

## Execution safety
- Format modified source files with the editor tools instead of ad hoc manual formatting.
- Use command-line tools only when they are necessary for the task.
- Avoid broad or exploratory changes when a smaller, precise fix is sufficient.

## Workflow macros
- Interpret the following prompt modifiers when present:
  - `#DMS`: The user wants to know if the proposed idea makes sense or not.
  - `#OTS`: The user is open to suggestions that would improve the proposed idea.
  - `#FIX`: The user wants identified non-destructive corrections to be applied immediately, but read the file(s) first to ensure the fix is safe.

## Clarification requests
- When a blocking question is required, provide explicit fixed choices.
- Mark exactly one fixed choice as recommended.
- Provide exactly one free-text answer path using the form's open-text / custom-answer
  field. Do not also add a fixed choice labeled `Other`, `Other (type your answer)`,
  or similar—that creates two free-text options.
- Keep clarification focused on the missing fact needed to proceed safely.
- Do not ask for approval of a spec, ADR, or override until the full text has already
  been shown in the same response.
