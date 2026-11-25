---
name: clickup-cli
description: "Manage ClickUp tasks, lists, spaces, checklists, comments, custom fields, docs and time tracking through the configured clickup-cli. Use for ClickUp, 클릭업, task lookup, deadlines, priorities, completion and workspace organization; preserve existing authentication and verify writes. Use morgen instead for Morgen calendars and tasks."
---

# ClickUp CLI

Use the installed `clickup-cli`, not a guessed `clickup` binary or a new API integration. This skill manages ClickUp only; do not migrate or synchronize Morgen tasks unless explicitly requested.

## Preflight and credentials

- Run `clickup-cli --version` and `clickup-cli auth check` when needed. On v0.18.0 auth check succeeds silently with exit 0.
- Existing credentials live in `~/.config/clickup-cli/config.toml`; project overrides may live in `.clickup.toml`. Use configured authentication. Never print/copy the token, read the credential file unnecessarily, or run setup to repair a transient request failure.
- `clickup-cli status` prints a masked token and configured workspace; avoid including this output in deliverables.
- Discover live syntax with `clickup-cli RESOURCE ACTION --help`; `clickup-cli agent-config show` provides the installed version's compact full reference without modifying files. Do not use agent-config inject/init unless requested.
- Use explicit task IDs for every operation. Omitted IDs can resolve from CLICKUP_TASK_ID or the git branch. Disable git detection with CLICKUP_GIT_DETECT=0 where appropriate, but still pass IDs.

## Discover hierarchy and targets

```sh
clickup-cli --output json workspace list
clickup-cli --output json space list
clickup-cli --output json folder list --space SPACE_ID
clickup-cli --output json list list --folder FOLDER_ID
clickup-cli --output json list list --space SPACE_ID
clickup-cli --output json list get LIST_ID
clickup-cli --output json --all task list --list LIST_ID --include-closed --subtasks
clickup-cli --output json --all task search --space SPACE_ID --include-closed --subtasks
clickup-cli --output json task get TASK_ID --markdown
```

List the folderless lists via --space as well as folder-contained lists. Resolve names to returned IDs. Do not choose a target merely because it is first in the response. Existing tasks, list metadata and the user's wording usually resolve ambiguity; ask only if materially distinct candidates remain.

`task search` is filtered workspace enumeration, NOT free-text search: v0.18.0 has no query/name flag. Supported filters include --space, --folder, --list, --status, --assignee and --tag. Filter returned task names/descriptions locally for textual matching. Include closed tasks when checking duplicates or historical completion; include subtasks when claiming full coverage.

## JSON and pagination traps

- Prefer --output json; inspect the actual shape. Verified v0.18.0 space list, task search, task get and list get return arrays, including singleton get responses. Do not assume `.id` at the root.
- Verified --fields does not project JSON fields. Use local JSON projection (jq or Python) rather than exposing full descriptions, emails and custom fields unnecessarily.
- Example after checking command success: `jq 'map({id,name,status:.status.status,list:.list.id,url})'` for task arrays.
- Check CLI exit status and structured error payloads BEFORE processing. A pipeline can mask the CLI failure; shell workflows should enable pipefail. Never interpret a request-error JSON object as an empty result.
- --all walks pages but the installed reference documents a hard cap of 100 pages. --limit N deliberately caps total returned items. Do not describe limited results as exhaustive. v2 uses --page; v3 docs/chat use --cursor; comments use --start and --start-id. Check endpoint help before continuing pagination.
- Timestamps are Unix milliseconds, often JSON strings. Handle null before conversion; preserve date-only versus timed semantics.

## Task writes

Inspect target task and target list statuses first; deduplicate creates by list, title and intent. Existing descriptions must not be overwritten unless requested; read and preserve their content when adding information.

```sh
clickup-cli --output json task create --list LIST_ID --name 'TITLE' --description 'BODY' --priority 3 --due-date '2026-10-01' --assignee USER_ID
clickup-cli --output json task create --list LIST_ID --name 'SUBTASK' --parent PARENT_ID --assignee USER_ID
clickup-cli --output json task update TASK_ID --parent PARENT_ID --name 'CLEAN_NAME'
clickup-cli --output json task update TASK_ID --status 'EXACT_LIST_STATUS'
clickup-cli --output json task update TASK_ID --due-date '2026-10-01T17:00:00+09:00' --priority 2
clickup-cli --output json task update TASK_ID --add-assignee USER_ID
clickup-cli --output json task update TASK_ID --rem-assignee USER_ID
clickup-cli --output json task update TASK_ID --description @/absolute/path/body.txt
clickup-cli task delete TASK_ID
```

Examples show syntax, not real requested dates/targets. Only pass fields the user asked to change.
- **Assignee access**: Always resolve user IDs from `clickup-cli member list --list LIST_ID`. Do not infer IDs from task creator fields (which may belong to inactive accounts). Adding an assignee without list access fails with HTTP 400 (`All assignees must have access to this task`). Multiple assignees can be added by repeating `--add-assignee USER_ID`.
- **Subtask hierarchy & reparenting**: Use `--parent PARENT_ID` on `task create` or `task update` to nest tasks. Subtasks maintain independent statuses, due dates, and assignees. When grouping existing tasks, strip bracket prefixes (e.g., `[Project] Name` -> `Name`) via `--name`. If subtasks appear scattered across the UI ("flying around"), the ClickUp view setting is set to "As separate tasks"; switch to "Collapse all" or "Expand all" via the `Subtasks` button in the top-right toolbar.
- Priority: 1 urgent, 2 high, 3 normal, 4 low. Do not invent 0 or 9 to clear priority; inspect installed support for clearing fields.
- --due-date YYYY-MM-DD means a date in the machine's local timezone; the CLI sends local noon for date-only handling. A time without offset is local wall time; Z or ±HH:MM specifies an instant. A time sets due_date_time=true. Check local timezone before ambiguous relative dates and re-read the saved date.
- Free-form --description/--text/--content support @path, @- stdin and @@ for literal leading @. Use files for multiline payloads. A literal @everyone needs @@everyone to avoid file lookup.
- Status names belong to the LIST, not merely its space. Completion may mean done or closed depending on that list; distinguish cancellation from completion, and never bulk-map all done-type statuses into success.

## Other supported resources

Read action help before using less common flags:

```sh
clickup-cli checklist create --task TASK_ID --name 'Checklist'
clickup-cli checklist add-item CHECKLIST_ID --name 'Item'
clickup-cli checklist update-item CHECKLIST_ID ITEM_ID --resolved
clickup-cli comment list --task TASK_ID
clickup-cli comment create --task TASK_ID --text @/absolute/path/comment.txt --markdown
clickup-cli field list --list LIST_ID
clickup-cli field set FIELD_ID --value OPTION_ID TASK_ID
clickup-cli tag list --space SPACE_ID
clickup-cli tag create --space SPACE_ID --name 'Tag' --bg-color '#03A2FD' --fg-color '#03A2FD'
clickup-cli task add-tag TASK_ID 'Tag'
clickup-cli task remove-tag TASK_ID 'Tag'
clickup-cli tag delete --space SPACE_ID --tag 'Tag'
clickup-cli attachment list --task TASK_ID
clickup-cli attachment upload /absolute/path/file --task TASK_ID
clickup-cli doc list
clickup-cli doc pages DOC_ID --content
clickup-cli time current
```

- **Tags & color traps**: Create tags with `--bg-color` and `--fg-color` (hex codes with `#`). Note: `clickup-cli tag update` silently returns `{}` without updating colors on existing tags due to API limitations. To change a tag's color via CLI, delete and re-create it, create a distinct tag name (e.g. `kebab-case`), or edit it directly in the ClickUp UI.
- **Custom fields**: For `drop_down` fields, pass the specific `option_id` (not the index or string label) to `--value`. Verify options via `field list`.

For custom fields, inspect type and allowed options; do not assume the displayed dropdown name, index and option ID are interchangeable. `task get --markdown` requests markdown_description with inline URLs preserved. Markdown comment mentions such as [@Name](user:123) notify users; do not add mentions or --notify-all gratuitously. Time tracking, chat sends, doc edits, sharing, invites and webhooks modify remote state too.

## Safety and write verification

1. A request to inspect or create this skill does not authorize remote test tasks or mutations.
2. Execute explicit, unambiguous requested ordinary writes without extra ceremony. Require clear user authorization for deletion, broad bulk changes, access changes, invitations, sharing and destructive replacement. Do not infer these from 'organize'.
3. Re-read every changed object independently: task get for task fields and checklists, comment list for comments, field values on task get, doc page for document changes. Compare requested fields against saved values; API success alone is insufficient. For deletions, verify with `task get TASK_ID` which must return exit code 3 (`Task not found, deleted`).
4. If a write times out or loses its response, reconcile by read/search before retrying; avoid duplicate tasks/comments or repeated notifications.
5. Read-only requests may receive a bounded retry on transient network errors. Verified local session had intermittent request-send errors followed by successful reads. Do not change authentication or network profiles based on these errors.
6. CLI reference exit codes: 0 success, 1 client error, 2 authentication, 3 not found, 4 rate limited, 5 server error. Respect rate-limit guidance; distinguish an inaccessible ID from a genuinely nonexistent task.
7. Report changed task names, IDs/URLs, saved status and due dates succinctly. Say when verification is blocked; never claim completion from an unverified mutation.

## Verification scope

The command reference was checked against clickup-cli v0.18.0. Authentication, space and task enumeration, task detail and list metadata were verified with read-only API calls. Mutation syntax was checked against installed help, not by creating test data; verify each first authorized write by re-reading the changed object. No wrapper or installer is bundled: use an already installed and authenticated clickup-cli.
