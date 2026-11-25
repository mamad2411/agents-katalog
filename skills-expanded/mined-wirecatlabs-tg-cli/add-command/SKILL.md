---
name: add-command
description: Add a new `tg` command or option to tg-cli end to end — the shared command in cli-core or a Telegram-only one here, the adapter method, tests through run(), the MCP tool, the test matrix, docs, the parity manifest and the changelog. Use when asked to add, build or implement a command, subcommand or flag in this repository.
---

# Add a command to tg-cli

A command is done when the port, the adapter, the command, the guard, the tests, the MCP tool, the
matrix, the docs and the changelog all agree. Follow the steps in order and tick them in the pull
request description.

Before anything: `HANDOFF.md` §3c and §4 (the path a new method takes, and what
bites), and [CLAUDE.md](../../../../CLAUDE.md) (the five rules). Names, options and answer shapes follow
cli-core's
[STANDARD.md](https://github.com/WireCatLabs/cli-core/blob/main/docs/dev/STANDARD.md): tg and max
answer the same command the same way.

## 0. Where it goes

- **Messenger-neutral** (most commands: messages, chats, reactions, polls, the store): the command
  lives in **cli-core**, and tg only implements the adapter method. Max gets it too.
- **Telegram only** (`session`, a Telegram concept nothing else has): `src/commands/` here, and a
  line in [cli-core's `parity.json`](https://github.com/WireCatLabs/cli-core/blob/main/parity.json)
  saying it is one-sided, and why.

Work in a worktree off `origin/main`, one per repository you touch: `git switch -c feat/<name>
--no-track origin/main`, and push without `-u` (the sandbox masks `.git/config`).

## 1. The path of a new adapter method

1. `MessengerAdapter` in cli-core `src/ports/messenger.ts`. A new method is optional
   (`edit?`), and commands ask for it with `capability()`.
2. A line in `observed.ts` (which ids the run record names) and `stored.ts` (what is saved), and the
   store if it should work with `--offline`.
3. The command in cli-core `src/cli/messenger/`, in a file of its own. A write is resolve →
   guard check → write → guard record, as `sendText` does, so read-only profiles, the recipient list
   and the send journal apply.
4. Release cli-core (its `bin/release`), then `pnpm add @wirecat/cli-core@<v>` here and
   add the version to `pnpm-workspace.yaml` → `minimumReleaseAgeExclude`.
5. `TelegramAdapter` in `src/telegram/adapter.ts` — in the feature's own module beside it (`folders.ts`, `topics.ts`,
   `groups.ts` …) with a one-line method in the class when the feature has one — and its mapping
   in `src/telegram/map.ts`: the only file that knows mtcute's shapes. No mtcute type crosses
   `src/telegram/` (rule 4, a lint rule). Check that no new mtcute path prints to stdout.

## 2. The command's contract

- `annotate(command, { effects })` on every command, reads too: `REMOTE_WRITE`, `FETCH`, `REMOTE_READ`,
  `LOCAL_WRITE`, `LOCAL_READ` from `@wirecat/cli-core/cli`; one without counts as a write. Nothing sends, marks read or
  deletes unless the typed command asks for it (rule 1). Anything that cannot be undone gets the
  level `ask` in cli-core's built-in permission defaults, so it asks first; `--allow-dangerous`
  answers yes for a deletion, `--yes` for the rest.
- In machine mode, stdout carries one JSON value and nothing else (rule 2). A list is
  `{ items, limit, hasMore }`.
- Errors are a `CliError(<code>, <sentence that says what to do>)`. The code decides the exit code.
- The connection closes in a `finally` (rule 3). A retried write reuses its `--operation-id`, never a new
  one: Telegram deduplicates by `random_id` across connections.

## 3. Tests

Drive it **through `run()`** against the scripted adapter: the fakes in `src/program.test.ts`,
`src/runs.test.ts`, `src/send-guard.test.ts`, `src/offline.test.ts` and `src/contract.test.ts`, and
the adapter's own case in `src/telegram/adapter.test.ts`, where mtcute is a stand-in.

- Pass **every option** at least once. `pnpm test:matrix` shows ✅/❌ per option and fails on ❌, and so does full validation after the merge.
  A command that truly cannot run offline gets its reason in `scripts/test-matrix-untested.ts` and a
  row in [live-scenarios.md](../../live-scenarios.md).
- Assert behaviour, not only "exit 0": what the adapter received, the output shape, a refusal on a
  read-only profile with nothing sent, a journal entry with no text.

```sh
pnpm lint && pnpm typecheck && pnpm test:coverage && pnpm test:matrix && pnpm docs:check
```

## 4. Agents

**The MCP tool comes in the same pull request** (cli-core `src/mcp/tools/<resource>.ts`). A write
tool carries `permission` and goes through the same guard. If an agent should know the command, add
a line to [`skills/tg-cli/SKILL.md`](../../../../skills/tg-cli/SKILL.md), which `tg skill show` prints.

## 5. Docs

- `pnpm generate` rewrites `docs/commands.md`. Never edit it by hand; full validation fails on drift.
- The user page for the area (`README.md`, `docs/usage.md`, …): English, current facts only.
- A changelog fragment, `changes/<branch>.md`: what a user notices, under tg's headings
  ([CONVENTIONS.md](../../CONVENTIONS.md#the-changelog)).
- `parity.json` in cli-core: the command's row moves to `both`, or says why it is one-sided.

## 6. Live

A command that reaches Telegram gets checked live before it ships: the `test-live` skill, with the
owner's yes, in the scenarios of [live-scenarios.md](../../live-scenarios.md). Add a row
there if none covers it.
