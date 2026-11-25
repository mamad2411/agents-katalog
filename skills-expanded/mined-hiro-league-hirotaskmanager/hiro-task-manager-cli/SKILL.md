---
name: hiro-task-manager-cli
description: Use this skill when working with Hiro Task Manager through the `hirotm` CLI to manage tasks, task lists and task boards.
---

# Hiro Task Manager CLI

Use this skill when the user wants to work with Hiro Task Manager through the `hirotm` CLI to manage tasks, task lists and task boards.

## Use this skill for
- Creating, updating and deleting tasks.
- Creating, updating and deleting task lists.
- Managing boards.
- Listing, searching and filtering tasks, lists and boards.
- Managing Hiro Task Manager server, to be able to operate on tasks, lists and boards.
- Delete, purge or restore tasks, lists and boards (see [Destructive operations](#destructive-operations)).

## Destructive operations

The following commands are **destructive** and must NEVER be invoked without an explicit, unambiguous user request in the current turn:

- `tasks purge`, `lists purge`, `boards purge` — permanent deletion, not recoverable.

Soft-deletes (`tasks delete`, `lists delete`, `boards delete`) are allowed only after:
1. The agent has shown the target entity to the user (via `show`, `describe`, or `list`) and confirmed it is the right one.
2. The user's intent to delete that specific entity is unambiguous.

Always prefer `trash` inspection and `restore` over re-creating an entity that was deleted by mistake.

For any destructive command that supports it, run with `--dry-run` first, then rerun with `--yes` only after the user confirms.

## Default operating workflow
1. Navigate to intended workspace root.
2. Initially make sure Hiro Task Manager server is running.
3. Discover the boards, lists or tasks you need to work with.
4. Narrow down to the entity you need to work with, using search or list/filter.
5. Use (Identification) to identify yourself in all commands.
6. Perform the smallest safe mutation using all the available data, 
7. Show the resulting state after the change.

## Core rules
- Use `hirotm` cli command for all operations.
- use `--help` to get help on any command or sub command `boards --help`, `boards describe --help`.
- prefer `hirotm --help` and subcommand help when you need examples or docs links.
- Run commands from the intended workspace root.
- Inspect current state before making mutations.
- For paginated reads or search, prefer `--count-only` when you only need cardinality first.
- Use `--client-name` on mutating commands so changes are attributable.
- Treat delete, purge, and structural changes as sensitive.
- Prefer `--dry-run` first for delete, purge, and board structure changes, then rerun with `--yes` only when ready.
- Use `--no-color` when plain output is easier to inspect for one run.

# Identification

Identify yourself in all commands with `--client-name <your-name>`. Your name should reflect the Agent Name, ex: Cursor Agent, Github Copilot Agent, Claude Code Agent, Open Code Agent.
If you are not sure, use a generic name "AI Agent"


# Discovery

- use `boards list` to list all boards.
- use `boards describe <id-or-slug>` to describe all or some board details.
- use `tasks list --board <board-id-or-slug>` to list and filter tasks in a board.
- use `tasks show <task-id>` or `lists show <list-id>` to print one row by global id when you already know the id.

# Finding/Adding/Updating Tasks

- When a user refers to an existing task, use `tasks list` with filters, `tasks show`, or `query search` to find it.
- If convenient, use limit, offset, fields, or quiet options to manage and the output shape.
- When adding a task
  - use any available information such as priority, task group, release, etc...
  - Add proper title (80 characters max) and Emoji if relevant only.
  - use Organized Markdown description if the task body is detailed.
  - use mermaid diagrams if the task includes design diagrams or if the user requests it.
  - If linking to a larger documents in the workspace, make sure to use a proper link from the workspace root.

# Access

If you are not allowed to access an entity or perform an operation due to CLI Access Control, explain the situation and suggest the user to give you the necessary permissions. Never attempt to bypass the CLI Access Control.

# Errors

- Prefer the machine-readable stderr `code` over parsing the `error` text.
- If stderr includes a `hint`, use it as the next recovery step.
- HTTP/API failures usually include better `hint` guidance than local argument-validation failures.

# Server Operations

- Check Server Status with `server status`
- Start Server with `server start --background`
- Stop Server with `server stop`

## References

- Server Commands - Start, stop, and check the server status.
- [Boards Commands](reference/boards.md) - Create, update, delete, list, describe, and configure boards.
- [Lists Commands](reference/lists.md) - List, show, add, update, move, delete, restore, and purge board lists.
- [Tasks Commands](reference/tasks.md) - List, show, add, update, move, delete, restore, and purge tasks.
- [Releases Commands](reference/releases.md) - List, show, add, update, delete, and set-default releases.
- [Trash Commands](reference/trash.md) - Inspect trashed boards, lists, and tasks.
- [Status Commands](reference/statuses.md) - List workflow statuses and their meanings.
- [Search Commands](reference/search.md) - Full-text task search with `query search`.
- [CLI Access Policy](reference/cli-access-policy.md) - Map commands to `cliPolicy` requirements and read/write permissions.
- [Errors and Exit Codes](reference/errors.md) - Exit codes, stderr fields, and common machine-readable codes.

**Safety notes**

- Prefer inspect-first workflows.
- Search before create when overlap is likely.
- Do not bypass the CLI by any other means than the `hirotm` CLI.
- Respect permission and policy failures instead of working around them unsafely.
- For destructive commands, see [Destructive operations](#destructive-operations).

**References**

- [Online Documentation](https://docs.hiroleague.com/task-manager/get-started/quickstart)
