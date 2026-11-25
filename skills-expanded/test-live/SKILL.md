---
name: test-live
description: Test a tg-cli change against the real Telegram before it ships — pick the live scenarios the change touches, get the owner's yes, run them through bin/tg in Saved Messages, the test group and the test dialog only, snapshot and restore what they change, record the shape of every answer and never its content. Use when asked to test live, check a branch on the real account, run the live scenarios, «проверить вживую», «прогнать живые сценарии».
---

# Test a change live

The rules are shared with max-cli: cli-core's
[RELEASING.md, "Live checks"](https://github.com/WireCatLabs/cli-core/blob/main/docs/dev/RELEASING.md#live-checks).
Read them first. **This is the owner's real Telegram account**: a mistake sends a message to a
person ([CLAUDE.md](../../../../CLAUDE.md), rule 1).

The scenarios are public, by role:
[docs/dev/live-scenarios.md](../../live-scenarios.md). The cast is private and never goes
into this repository: the real test group, the second account, their ids and the profile names. It
lives in `docs_ai/live-cast.md` of the main checkout, which git ignores. Without it, only the Saved
Messages scenarios can run. Say so, and do not guess a chat.

Nothing here sends, marks read, deletes or changes a setting without the owner's yes in this session.

## 1. Pick the scenarios

```sh
git diff --stat origin/main...HEAD
git diff origin/main...HEAD -- docs/commands.md        # generated: the commands and options that changed
grep '⛔' docs/dev/test-matrix.md                      # commands only a live run checks
```

Map each changed command to the scenario ids that exercise it. Every changed command with a ⛔ row is
in the list. Drop what the page's "Not run" table rules out, and name what you dropped.

## 2. Show the list and wait for yes

One line per scenario: its id, the commands, the role (Saved Messages, test group, test dialog), what
it changes and how that is put back. Wait for the owner's yes. A scenario not on the approved list
is not run.

## 3. Build, seed, run through `bin/tg`

```sh
pnpm build
node --experimental-strip-types scripts/seed-worktree.ts <main checkout> "$PWD"   # a worktree, once
bin/tg account show --json
```

**Always `bin/tg`, never `node dist/bin/tg.js`.** The bare build opens the owner's real store, and a
branch build can migrate it. **Never `session start`**: that is a new device on the real account.
From an agent inside this repository's sandbox, only a **plain** `bin/tg …` call reaches Telegram.
`bin/tg … | jq` and a script that starts `bin/tg` run inside the sandbox and get `ENETUNREACH`
([agents.md](../../agents.md#what-an-agent-may-do-and-what-stops-it)). Run the call on its
own and read the shape from its output, or ask the owner to run a script from a terminal.

Pace the writes: Telegram answers a burst with `FLOOD_WAIT`, and three sessions share one account's
budget. Keep reads small (`--limit 3`).

## 4. Record and report

Append a dated row per scenario to the Results table in `docs_ai/live-cast.md`: the branch or
version, the id, PASS/FAIL, the exit codes and shapes. No content, no names, no ids of real people.
A FAIL caused by the account's state rather than the change is still a FAIL until the owner rules
on it.

Report to the owner what ran, what failed (the command and exit code), what was dropped and why, and
anything that could not be restored exactly.
