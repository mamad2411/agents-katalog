---
name: codex-cli-session
description: Use when the user wants Codex CLI session continuity across repeated non-interactive runs. Read the session ID from a project-root `.codex-cli-session-id` file when available; otherwise bootstrap a new Codex session, persist the new session ID, and then run the real task with `codex exec resume`. Covers session continuity, `--json`, `-m`, and project-scoped session pinning.
---

# Codex CLI Session

Use this skill when the user wants Codex CLI to continue work through a pinned project session instead of starting a fresh session every time.

Use the project-root `.codex-cli-session-id` file as the primary source of truth for the session to resume.

The main user task must never run without an active session ID.

Do not use wrapper scripts. Run Codex CLI directly.

## Workflow

1. Read `<project-root>/.codex-cli-session-id` first.
2. If the file exists and contains a valid session ID, use that value for the real Codex command.
3. If the file is missing or empty, bootstrap a fresh Codex session with a short prompt that tells Codex to inspect the current directory and get ready to continue work in this project.
4. After bootstrapping, recover the newest session ID from `~/.codex/session_index.jsonl` and write it into `.codex-cli-session-id`.
5. If bootstrap fails and `.codex-cli-session-id` still does not contain an active session ID, do not run the main user prompt. Report the failure and stop.
6. Only after `.codex-cli-session-id` contains an active session ID, run the real user task with `codex exec resume`.
7. Keep the user's prompt text exact unless they explicitly ask you to rewrite it.
8. If the user explicitly provides a different Codex session ID, update `.codex-cli-session-id` to that value before running the next Codex command.
9. If the user wants the exact Codex output, relay it faithfully. Otherwise, summarize the relevant answer from the command output.

## Command Pattern

Use:

```bash
codex exec resume "<session-id>" "<prompt>" --json
```

If there is no session yet, use this only as a bootstrap step:

```bash
codex exec "Inspect the current directory and get ready to continue work in this project." --json
```

After bootstrapping, write the newest session ID into `.codex-cli-session-id`. Then run the real task by reading the session ID from `.codex-cli-session-id` and using `codex exec resume`.

## File Rules

- The session file must live at `<project-root>/.codex-cli-session-id`.
- The file should contain only the session ID string and a trailing newline.
- Treat the file as the project's pinned Codex conversation.
- The real user prompt must be executed only after this file contains an active session ID.

## Notes

- `codex exec resume` requires an existing session. If you do not have one yet, bootstrap first.
- No main task execution without a session ID. Bootstrap comes first; if it fails, stop.
- Prefer `--json` for machine-readable output and reliable session-oriented workflows.
- If the user asks what Codex previously saw or said, use the active session ID with a direct prompt such as `What was my last message to you?`
