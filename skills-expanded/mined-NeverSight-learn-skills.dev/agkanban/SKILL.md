---
name: agkanban
description: Use when coordinating multi-agent tasks across Claude Code / Codex with a kanban-style board that pairs with agmsg. Manage cards, claim work, move cards between todo/doing/review/done, and auto-notify teammates via agmsg on transitions. Triggers include "show my tasks", "claim a card", "move card to review", "add a task to the board", or any multi-agent task hand-off.
---

# agkanban

Kanban-style task state management designed to pair with agmsg. State is persisted in
`~/.agkanban/board.db`; card column transitions auto-notify stakeholders via agmsg.
Identity (team/agent) is borrowed from agmsg.

## Prerequisites

- agmsg installed and the project joined to a team (`/agmsg` to verify).
- Board operations work without joining / without agmsg, but notifications are skipped.

## Usage

Use the platform entrypoint for the current session:

- **Windows / PowerShell / Codex:** run `agkanban <subcommand>` from the project directory.
  This is a PowerShell profile function that delegates to
  `~/.agents/skills/agkanban/scripts/windows/agkanban.ps1`, which then uses Git Bash.
  Do not call WSL `bash`, and do not call `bash scripts/agkanban.sh` from the project root.
  If the `agkanban` function is missing, use the explicit launcher:
  `& "$HOME\.agents\skills\agkanban\scripts\windows\agkanban.ps1" <subcommand>`.
- **Unix / Git Bash:** run
  `bash "$HOME/.agents/skills/agkanban/scripts/agkanban.sh" <subcommand>` (or
  `bash scripts/agkanban.sh <subcommand>` only when your working directory is the
  installed skill directory).

**No arguments shows your open cards — todo/doing/review assigned to you (everything but
done)** (there is no separate `mine` command).

**Viewing your cards is a call to act, not just to report** (like agmsg's "read and
respond"). When you run `agkanban` with no args — or when the SessionStart hook surfaces
your cards — work them: for each card read `show <id>` for the `--body` (target files +
acceptance criteria), then start. **Always `claim` a todo card before doing any work on
it** — claim moves it to `doing` and notifies the team that it is in progress; never work
a todo card unclaimed. Move `doing → review` when ready, and as reviewer do the review and
`done` it (or report a blocker to the requester via agmsg). Do not stop at listing or
summarizing them.

| Command | Action |
|---|---|
| `agkanban` | Your open cards (todo/doing/review assigned to you) |
| `agkanban board` | Full team board |
| `agkanban add "<title>" [--assignee X] [--reviewer Y] [--body "..."]` | Add card (todo) |
| `agkanban claim <id> [--agent A]` | Claim (doing, assign to self, atomic) |
| `agkanban review <id>` | Request review (move to review) |
| `agkanban done <id>` | Mark done |
| `agkanban reopen <id>` | Reopen (back to todo) |
| `agkanban move <id> <todo\|doing\|review\|done>` | Generic: move to any column (fallback for the above verbs) |
| `agkanban show <id>` | Card detail + event history |
| `agkanban block <id> --by <id2> [--by <id3> …]` | Add dependency(ies) — `--by` is repeatable for multiple prerequisites |
| `agkanban edit <id> [--title T] [--assignee X] [--reviewer Y] [--body "..."] [--agent A]` | Edit card fields — **creator or assignee only** (empty value clears; title can't be empty) |
| `agkanban delete <id> [--agent A]` | Permanently delete a card (alias `rm`) — **creator only**; also clears dangling `blocked_by` |

`claim`/`review`/`done`/`reopen` are intent-specific transition verbs; internally they
perform the same column move + agmsg auto-notification as `move`. Use `move` only when
you need to target an arbitrary column.

**Write actionable cards.** The agmsg notification carries only the card *title*, so for a
card that represents real work, put the target files/paths and acceptance criteria in
`--body`. Without a body the assignee/reviewer cannot tell what to act on. Read it with
`agkanban show <id>` on Windows/PowerShell, or with the Bash entrypoint on Unix/Git Bash.

Pass `--team <name>` on each command when you belong to multiple teams.

Pass `--agent <name>` on `agkanban` (no-arg), `claim`, `edit`, and `delete` when multiple
agents share one project directory and identity cannot be auto-resolved (`agent unresolved`
error). This mirrors `--team` and takes priority over `agmsg whoami` output.

In a team, `--assignee` / `--reviewer` are agmsg agent names (list them with `/agmsg team`),
and the board + notifications are shared with teammate agents on the same machine. Run
agkanban from the project you joined so `whoami` can resolve your identity.

## Codex sandbox setup

agkanban writes outside the project (`~/.agkanban`) and notifies through agmsg
(`~/.agents/skills/agmsg`). In Codex `workspace-write` sessions, run this once so those
paths are added to `~/.codex/config.toml` as absolute writable roots:

```bash
bash ~/.agents/skills/agkanban/scripts/setup-codex-sandbox.sh
```

Use `--check` to verify without writing, or `--print` to print the TOML block. Restart or
respawn Codex after changing sandbox configuration.

## Delivery (awareness)

agkanban has no dedicated monitor. Notifications fired on transitions are delivered by
**agmsg's delivery mechanism (turn/monitor/hook)**. Because state is persistent, running
`agkanban` / `board` on demand is sufficient to catch up without missing anything.

### SessionStart auto-pull (optional)

Register `hooks/session-start.sh` as a Claude Code SessionStart hook to automatically
surface your assigned cards in context at every session start (silent when identity is
unresolved or there are no cards). Example config (`~/.claude/settings.json`):

```json
"hooks": {
  "SessionStart": [
    { "hooks": [ { "type": "command",
      "command": "bash ~/.agents/skills/agkanban/hooks/session-start.sh" } ] }
  ]
}
```

## Notification mapping

| Transition | Recipient |
|---|---|
| → doing | assignee |
| → review | reviewer (falls back to creator) |
| → done | creator (+ assignee if different) |
| all deps done | assignee of the waiting card (fires only once *every* dependency is done) |

Notifications to yourself are suppressed.
