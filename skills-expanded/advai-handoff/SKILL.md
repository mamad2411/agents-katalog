---
name: "advai-handoff"
description: "Persists session handoff notes in `.advai/HANDOFF.md` and restores prior context from that file. Invoke when user wants to record current session progress or resume work in a new session."
---

# Advai Handoff

Use this skill to persist a compact session handoff in the current project and restore that context later from `.advai/HANDOFF.md`.

## When to Invoke

Invoke this skill when the user wants to:

- Record what has been done in the current conversation for the next agent session
- Save the current task goal, progress, changed files, validation status, and next step
- Resume work in a new conversation by reading the previous handoff note first
- Maintain a lightweight project-local state file instead of relying on long chat history

Do not use this skill for general documentation, changelogs, or long-form project notes.

## Handoff File

- Use exactly one file: `.advai/HANDOFF.md`
- Treat the current project directory as the storage scope
- Create the `.advai/` directory if it does not already exist
- Do not introduce extra handoff files, dated snapshots, or nested handoff directories unless the user explicitly asks for them

## Operating Flow

### In an active conversation

When the user asks to record or update handoff state:

1. Read the current `.advai/HANDOFF.md` if it exists.
2. Refresh the file with the latest state of the current task.
3. Keep the note concise, factual, and easy for the next session to scan.

### In a new conversation

When the user asks to resume from a previous handoff:

1. Check whether `.advai/HANDOFF.md` exists in the current project.
2. Read it before making assumptions about prior progress.
3. Summarize the handoff back to the user and continue from the recorded next step.
4. If the file is missing, say that no prior handoff note was found and continue with normal discovery.

## Recommended Template

Use this structure unless the user requests a different format:

```markdown
# Handoff

## Goal
- <current objective>

## Completed
- <finished work>

## Changed Files
- `<path>`: <what changed>

## Validation
- <tests run, checks performed, or not run yet>

## Open Issues
- <known gaps, blockers, or follow-ups>

## Next Step
- <the most useful next action>
```

## Writing Guidelines

- Prefer updating the existing handoff file in place instead of appending repeated session logs.
- Keep entries specific enough that a new agent can continue without rereading the whole conversation.
- Include concrete file paths when code or docs changed.
- Be explicit about validation status, including when checks were not run.
- Capture unresolved questions only when they materially affect the next step.
- If the current task direction changed, overwrite stale goals so the file reflects the latest agreed intent.

## Reading Guidelines

- Treat the handoff as working context, not as guaranteed truth.
- Cross-check the repository state when the handoff mentions changed files, tests, or pending work.
- If the handoff conflicts with the current user request, follow the newest user instruction and then refresh the handoff file if appropriate.

## Example Prompts

- "Record a handoff for this session."
- "Update the handoff before we stop."
- "Read the previous handoff and continue."
- "Resume from `.advai/HANDOFF.md`."
