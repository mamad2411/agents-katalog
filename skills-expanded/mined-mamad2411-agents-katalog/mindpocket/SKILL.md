---
name: mindpocket
description: Use when a task requires operating the MindPocket CLI to inspect server readiness, authenticate, and retrieve or manage bookmarks, folders, or the current user through structured JSON commands.
---

# MindPocket CLI Skill

## When to Use

Use this skill when the user wants to operate a MindPocket server through the `mindpocket` CLI instead of manual browser actions or direct API calls.

Typical requests include:

- Inspecting CLI readiness or available commands
- Configuring the target server URL
- Logging in or checking auth status
- Reading the current user profile
- Listing, reading, creating, updating, or deleting bookmarks
- Listing or reading folders

## Preconditions

Check that the CLI is available before doing anything else:

```bash
command -v mindpocket
```

If the command is missing, tell the user the MindPocket CLI is not installed or not on `PATH`.

Only use a one-shot fallback such as `npx mindpocket@latest ...` when networked npm execution is acceptable in the current environment and the user has not prohibited it.

Never assume a default server URL. Never invent bookmark IDs or folder IDs.

## Standard Workflow

Follow this sequence unless the user explicitly asks for a narrower step:

1. Confirm the CLI exists with `command -v mindpocket`.
2. Discover the CLI surface with `mindpocket schema`.
3. If a command shape is uncertain, run `mindpocket <subcommand> --help`.
4. Run `mindpocket doctor` before protected operations or troubleshooting.
5. If the server is unset, ask the user for the MindPocket server URL and set it with `mindpocket config set server <url>`.
6. If auth is missing or expired, use `mindpocket auth login --no-open` unless the environment clearly supports opening a browser.
7. Prefer read-only inspection before mutation.
8. Parse normal command output as JSON and treat failures as structured error results.

## Command Selection Rules

Prefer these commands as the primary interface:

```bash
mindpocket version
mindpocket schema
mindpocket doctor
mindpocket config get
mindpocket config set server <url>
mindpocket auth login --no-open
mindpocket auth status
mindpocket auth logout
mindpocket user me
mindpocket bookmarks list --limit <n>
mindpocket bookmarks get <id>
mindpocket bookmarks create --url <url>
mindpocket bookmarks update <id> ...
mindpocket bookmarks delete <id>
mindpocket folders list
mindpocket folders get <id>
```

Selection rules:

- Use `schema` before guessing commands, arguments, or output fields.
- Use `--help` when a specific subcommand shape is uncertain.
- Use `doctor` before protected commands and before troubleshooting.
- Prefer `config get` before rewriting configuration.
- Prefer read-only commands before any create, update, or delete flow.

## Authentication Workflow

Use this order:

1. Run `mindpocket doctor`.
2. If the server is missing, ask for the correct URL and set it with `mindpocket config set server <url>`.
3. If auth is missing or expired, run `mindpocket auth login --no-open`.
4. If needed, confirm status with `mindpocket auth status`.
5. Only use `mindpocket auth logout` when the user explicitly wants to clear the current session.

Prefer `--no-open` for terminal, remote, and agent-driven environments. Only prefer browser opening when the environment clearly supports it and the user benefits from it.

## Bookmark Workflows

Use these patterns:

- To inspect recent bookmarks, start with `mindpocket bookmarks list --limit <n>`.
- To inspect a specific bookmark, use `mindpocket bookmarks get <id>`.
- To create a bookmark, require a concrete URL and use `mindpocket bookmarks create --url <url>`.
- To update a bookmark, first identify the bookmark ID from list or get results, then run `mindpocket bookmarks update <id> ...`.
- To delete a bookmark, confirm intent unless the user explicitly requested deletion, then run `mindpocket bookmarks delete <id>`.
- To inspect folders, use `mindpocket folders list` and `mindpocket folders get <id>`.
- To inspect the current account, use `mindpocket user me`.

Prefer structured, read-only inspection before mutation. Do not infer IDs from names when the CLI has not returned an ID.

## Failure Handling

Treat either of these as a failure:

- A non-zero process exit code
- A JSON payload with `ok: false`

When a command fails:

1. Surface the command that failed.
2. Surface the failure `code`, `message`, and relevant `details`.
3. Use `mindpocket doctor` if the failure might be caused by server config, auth state, or connectivity.
4. Ask for missing inputs instead of guessing them.

Common corrective paths:

- Missing CLI: tell the user to install `mindpocket` or approve a one-shot `npx mindpocket@latest ...` fallback.
- Missing server: ask for the server URL, then run `mindpocket config set server <url>`.
- Missing auth: run `mindpocket auth login --no-open`.
- Unknown arguments or flags: consult `mindpocket schema` or the relevant `--help`.

## Output and Parsing Rules

MindPocket CLI is JSON-first for normal command results. Parse stdout as JSON whenever possible.

For successful commands:

- Read the JSON payload instead of scraping terminal text.
- Keep the user-facing summary concise.
- Preserve enough structured detail to debug or continue the workflow.

For failed commands:

- Include `code`, `message`, and relevant `details` in the response.
- Do not hide the actual reason for failure behind generic wording.

## Escalation Rules

Ask the user before proceeding when:

- The server URL is unknown
- Authentication is required and the environment constraints are unclear
- A destructive action such as bookmark deletion is requested without clear intent
- The CLI is missing and using `npx mindpocket@latest ...` would require networked execution the user may not want

Do not silently switch to direct API calls, browser automation, or guessed parameters when the CLI flow is available but incomplete.
