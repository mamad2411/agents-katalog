---
name: gemini-cli-session
description: Use when the user wants the primary agent to call Gemini CLI directly while preserving an existing Gemini conversation history. Read the session ID from a project-root `.gemini-cli-session-id` file when available; otherwise recover the latest project session from local Gemini history or create a new session, then persist that ID. Use `--approval-mode auto_edit` by default so Gemini CLI can write files with its own edit tools. Covers `-r <session-id>`, `-p`, `-m gemini-3-flash-preview`, and `stream-json` output handling.
---

# Gemini CLI Session

Use this skill when the user wants the primary agent to send a prompt to Gemini CLI against an existing Gemini session, so Gemini keeps the prior conversation history.

Do not use wrapper scripts. Run Gemini CLI directly.

Default to `--approval-mode auto_edit` so Gemini CLI can use its own `write_file` and `replace` tools without interactive approval.

Use the project-root `.gemini-cli-session-id` file as the primary source of truth for the session to resume.

The main user task must never run without an active session ID.

If `.gemini-cli-session-id` does not exist, first look up the current project's local Gemini history under `~/.gemini/tmp/<project_hash>/logs.json` and recover the latest `sessionId`. Write that value into `.gemini-cli-session-id`.

If the project has no local Gemini session history yet, start a fresh headless run only for session bootstrap, capture the `session_id` from the `init` event in `stream-json`, and immediately persist it into `.gemini-cli-session-id`. After that, run the real user task by reading the session ID from `.gemini-cli-session-id` and using `gemini -r`.

## Workflow

1. Read `<project-root>/.gemini-cli-session-id` first.
2. If the file exists and contains a valid session ID, use that value for the real Gemini command.
3. If the file is missing or empty, inspect `~/.gemini/projects.json` to get the current project's hash, then inspect `~/.gemini/tmp/<project_hash>/logs.json` for the latest `sessionId`.
4. If a local project `sessionId` is found, write it to `.gemini-cli-session-id`.
5. If no session can be recovered locally, start a fresh bootstrap session, capture the new `session_id` from the `init` event, and write it to `.gemini-cli-session-id`.
6. When bootstrapping a brand-new session, use a short bootstrap prompt that tells Gemini CLI to inspect the current directory, for example: `Inspect the current directory and get ready to continue work in this project.`
7. If session creation or recovery fails and `.gemini-cli-session-id` still does not contain an active session ID, do not run the main user prompt. Report the failure and stop.
8. Only after `.gemini-cli-session-id` contains an active session ID, run the real user task with `gemini -r`.
9. Always include `-m "gemini-3-flash-preview"` unless the user explicitly asks for another model.
10. Always include `--approval-mode auto_edit` unless the user explicitly asks for another approval behavior.
11. Default to `stream-json` output unless the user explicitly asks for plain text or another Gemini output mode.
12. For file creation or edits, let Gemini CLI perform the write through its own `write_file` or `replace` tools.
13. Do not manually write the file yourself as a fallback. If Gemini CLI does not have the required edit tool registered, report that clearly and stop.
14. If the user wants the exact Gemini output, relay it faithfully. Otherwise, summarize the relevant answer from the command output.

## Command Pattern

Use:

```bash
gemini -r "<session-id>" -p "<prompt>" -m "gemini-3-flash-preview" -o "stream-json" --approval-mode auto_edit
```

If there is no session yet, use this only as a bootstrap step:

```bash
gemini -p "Inspect the current directory and get ready to continue work in this project." -m "gemini-3-flash-preview" -o "stream-json" --approval-mode auto_edit
```

The first `init` event contains the new `session_id`. Save that value into `.gemini-cli-session-id`. Then run the real task by reading the session ID from `.gemini-cli-session-id` and using `gemini -r`.

## File Rules

- The session file must live at `<project-root>/.gemini-cli-session-id`.
- The file should contain only the session ID string and a trailing newline.
- Treat the file as the project's pinned Gemini conversation.
- The real user prompt must be executed only after this file contains an active session ID.
- If the user gives a different explicit session ID, update `.gemini-cli-session-id` to that value before running the next Gemini command.

## Notes

- Treat the resume ID as required whenever the user expects Gemini to remember earlier context.
- `-r` cannot create a missing session. It only resumes an existing one.
- Local Gemini session history is project-scoped; prefer the current project's own history before falling back to a brand new session.
- No main task execution without a session ID. Recovery or bootstrap comes first; if neither works, stop.
- Prefer Gemini CLI's own edit tools for file writes. Successful `write_file` or `replace` calls mean Gemini itself performed the modification.
- If Gemini CLI reports that `write_file` or `replace` is not registered, do not patch the file manually as a substitute unless the user explicitly changes the requirement.
- Keep the user's prompt text exact unless they explicitly ask you to rewrite it.
- If `gemini` is missing, report that clearly and stop.
- If Gemini returns streaming JSON events, inspect them and extract the meaningful assistant response for the user unless the user asked for the raw event stream.
- If the user asks what Gemini previously saw or said, use the active session ID with a direct prompt such as `What was my last message to you?`
