---
name: hopback
description: Search local coding-agent session history, page through the results, and resume or fork a session. Use when the user asks to find, inspect, continue, recover or fork earlier work from Claude Code, Codex, Antigravity, OpenCode, Kimi Code or another agent that hopback indexes.
compatibility: Requires the hb (or hopback) command with JSON output, version 0.2.0 or later.
---

# hopback

`hb` (the same program as `hopback`) indexes the session files that coding
agents keep on this machine. Use its JSON output as a local discovery tool. Do
not parse the human table, and do not start the TUI: it needs a terminal.

## Search

1. Start with a narrow query and a small page:

   ```bash
   hb --json --limit 10 "dir:project agent:codex authentication bug"
   ```

2. Read `sessions` and `meta` from the single JSON object on stdout. Notices
   and errors are on stderr; a failed command prints nothing on stdout and
   exits with status 1.
3. Prefer filters when the user gives the context: `agent:claude`,
   `dir:backend`, a date keyword, or the flags `--agent` and `--directory`.
4. Each session has `id`, `agent`, `title`, `original_title`, `directory`,
   `timestamp`, `message_count`, `pinned`, `hidden`, `forked_from` and
   `resume_command`. Add `--include-messages` to get the conversation text
   as `messages`, a list of `{role, text}`.

## Page through results

- `meta.state` is `more`, `complete` or `past_end`.
- While it is `more` and more candidates are needed, repeat the same command
  with `--offset` set to `meta.next_offset`.
- Stop on `complete` or `past_end`. Do not restart from the beginning or raise
  `--limit` without a reason. `--all` returns everything from the offset on;
  use it only when the full list is really needed.
- Add `--no-refresh` to answer from the existing index without scanning the
  agents' files, when speed matters more than freshness.
- Hidden sessions are left out unless `--include-hidden` is given.

## Continue the newest session of a folder

`hb . --print` prints two lines for the current folder: the folder to run in,
then the command that resumes its most recently used session, whatever the
agent. It exits with status 1 when the folder and its parents have no session.
Without `--print`, `hb .` starts the agent itself.

## Select and resume

- Compare `title`, `directory`, `timestamp`, `agent` and `id` to pick the
  session. When two look alike, show both to the user.
- Use `resume_command` as an argument array. Do not rebuild it by splitting or
  joining shell text.
- Run the command from the session's `directory`.
- `resume_command` already carries the agent's skip-permission flags when the
  session was started with them. `--yolo` adds them to every command.

## Fork and organise

- `hb fork --json --to codex <agent:id>` makes a translated fork (Claude Code
  to Codex or back); the result's `launch_command` opens it. With `--dry-run`
  it describes the fork without writing anything.
- `hb pin`, `hb unpin`, `hb rename <agent:id> "<title>"`, `hb hide` and
  `hb unhide` change hopback's own notes about a session. Add `--json` to get
  the session back after the change.
- Address a session as `agent:id`. A bare id works only when one agent has it.
