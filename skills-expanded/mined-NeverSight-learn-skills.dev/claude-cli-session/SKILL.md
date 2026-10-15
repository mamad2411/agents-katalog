---
name: claude-cli-session
description: Use when the user wants Claude Code session continuity across repeated CLI runs. Read the session ID from a project-root `.claude-cli-session-id` file when available; otherwise create a new UUID-backed Claude session, persist that ID, and then run the real task through the same pinned session. Covers `--resume`, `--session-id`, `-p`, `--output-format stream-json`, `--permission-mode acceptEdits`, and optional `ollama launch claude --model ...` integration.
---

# Claude CLI Session

Use this skill when the user wants Claude Code to continue work through a pinned project session instead of starting a fresh session every time.

Use the project-root `.claude-cli-session-id` file as the primary source of truth for the session to resume.

The main user task must never run without an active session ID.

Do not use wrapper scripts. Run Claude CLI directly.

Default to `--permission-mode acceptEdits` for edit-capable automated runs unless the user explicitly asks for a different permission mode.

## Workflow

1. Read `<project-root>/.claude-cli-session-id` first.
2. If the file exists and contains a valid UUID session ID, use that value for the real Claude command.
3. If the file is missing or empty, generate a new UUID, write it into `.claude-cli-session-id`, and use it to bootstrap a fresh Claude session with `--session-id`.
4. When bootstrapping a brand-new session, use a short bootstrap prompt that tells Claude to inspect the current directory and get ready to continue work in this project.
5. If bootstrap fails and `.claude-cli-session-id` still does not contain an active session ID, do not run the main user prompt. Report the failure and stop.
6. Only after `.claude-cli-session-id` contains an active session ID, run the real user task with `--resume`.
7. Keep the user's prompt text exact unless they explicitly ask you to rewrite it.
8. If the user explicitly provides a different Claude session ID, update `.claude-cli-session-id` to that value before running the next Claude command.
9. If the user wants the exact Claude output, relay it faithfully. Otherwise, summarize the relevant answer from the command output.

## Command Pattern

Use:

```bash
claude -p --resume "<session-id>" --output-format stream-json --permission-mode acceptEdits "<prompt>"
```

If there is no session yet, use this only as a bootstrap step:

```bash
claude -p --session-id "<uuid>" --output-format stream-json --permission-mode acceptEdits "Inspect the current directory and get ready to continue work in this project."
```

If the user explicitly wants to drive Claude Code through Ollama, use:

```bash
ollama launch claude --model "<model>" -- -p --resume "<session-id>" --output-format stream-json --permission-mode acceptEdits "<prompt>"
```

If there is no session yet in the Ollama-driven flow, generate a UUID, write it to `.claude-cli-session-id`, then bootstrap with:

```bash
ollama launch claude --model "<model>" -- -p --session-id "<uuid>" --output-format stream-json --permission-mode acceptEdits "Inspect the current directory and get ready to continue work in this project."
```

## File Rules

- The session file must live at `<project-root>/.claude-cli-session-id`.
- The file should contain only the session ID string and a trailing newline.
- Treat the file as the project's pinned Claude conversation.
- The real user prompt must be executed only after this file contains an active session ID.

## Notes

- `--resume` requires an existing session. If you do not have one yet, bootstrap first with `--session-id`.
- `--session-id` must be a valid UUID.
- No main task execution without a session ID. Bootstrap comes first; if it fails, stop.
- Prefer `--output-format stream-json` for machine-readable output and reliable session-oriented workflows.
- If the user asks what Claude previously saw or said, use the active session ID with a direct prompt such as `What was my last message to you?`
