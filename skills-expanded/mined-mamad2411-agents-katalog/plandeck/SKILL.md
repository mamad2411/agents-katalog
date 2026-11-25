---
name: plandeck
description: A live visual Kanban board and continuity layer for long-running agentic tasks. Nobody wants to read a markdown plan or stare at raw HTML while an agent grinds for an hour, so Plandeck turns the plan into a board that organizes itself. Use it when a task is multi-step, long-running, or needs visual planning. Break the work into cards, declare which card depends on which, and Plandeck computes the critical path, auto-promotes cards to Ready as their dependencies clear, rolls up story-point estimates into an honest percent complete, and names the one next action. Plans, observed transitions, and last-known-good snapshots stay as plain files on disk, so they survive /clear and context resets. After a reset, run plandeck next to recover the single next move and its recent history. If the plan stops parsing, run plandeck doctor before using git. Renders a live board in the browser over SSE. Triggers on plan a project, break down a task, kanban board, task board, visual plan, long-running agent, agentic task, track dependencies, critical path, story-point estimates, what is next, mission journal, recover plan, plandeck.
---

# Plandeck

Plandeck keeps a plan on disk as `plan.yaml` and renders it as a live Kanban board that reorganizes itself as you edit. You author cards (id, estimate, dependencies, next action). Plandeck computes the rest: which cards are Ready, the critical path, progress rollups, and the single next move. It grows out of planning-with-files (crash-proof file plans plus a completion gate). What is new in Plandeck is the live visual board plus a deterministic intelligence layer over the yaml. It contains no AI and no LLM, only pure, tested functions.

## When to use it

Reach for Plandeck when the work is multi-step and worth tracking:

- A task that needs 5+ steps, spans a long session, or will outlive a `/clear`.
- Work with real dependencies, where order matters and one card unblocks others.
- Anything you want to see: a board with lanes, estimates, and a critical path.

## When not to use it

Skip it for one-shot work:

- A single edit, a quick answer, a two-step fix.
- Anything you will finish before the next context reset.

Do not build a board for work that does not need one. The overhead pays off only when the plan has to persist and coordinate.

## Files in a plan directory

| file | role |
|---|---|
| `plan.yaml` | The single source of truth (the board). You read and write it; the board re-renders live. |
| `archive.yaml` | Completed cards moved out of the live plan. Their ids still satisfy dependencies. |
| `plan.md` | The charter a human or agent reads first: north star, why, constraints. |
| `cards/*.md` | Optional long receipts. `plandeck check` warns about unreferenced files and missing card references. |
| `NEXT.md` | Generated re-entry breadcrumb. A running board refreshes it when the generated content changes. |
| `.plandeck/` | Derived continuity data: `journal.ndjson`, `last-state.json`, and the newest 20 valid plan snapshots. Gitignored. Never edit it by hand. |
| `plan.yaml.corrupt` | Content replaced by the most recent explicit doctor restore. Kept beside the plan for inspection and gitignored. |
| `.plandeck-board/` | Generated static board app. Gitignored, rebuilt on every `plandeck board`. |

## Card schema

Author these fields on each card in `plan.yaml`:

| field | required | shape | purpose |
|---|---|---|---|
| `id` | yes | `C001`, `C002` | Stable card id. |
| `title` | yes | short imperative | What the card delivers. |
| `column` | yes | `backlog` / `ready` / `doing` / `review` / `done` | The lane you place the card in. Never place a card in Ready by hand; Plandeck promotes it. |
| `status` | no | `queued` / `active` / `blocked` / `done` | `active` marks the ONE card in flight. Mark a blocker with `status: blocked` (or `column: blocked`); both route the card to the Blocked lane, and an unmet dependency lands it there on its own. |
| `role` | no | `scout` / `worker` / `judge` / `pm` | Who does the card. |
| `estimate` | no | story points `1/2/3/5/8/13` | Powers percent complete, velocity, and the critical path. No hours. An omitted estimate counts as one point everywhere. |
| `confidence` | no | `0..1` | How firm the estimate is. |
| `priority` | no | `P0..P4` | `P0` is drop everything. |
| `risk` | no | `low` / `med` / `high` | Risk band. |
| `depends_on` | no | `[ids]` | Plandeck promotes the card to Ready once every listed card is done. |
| `verify` | no | `[commands]` | Commands that prove the card is really finished. |
| `next_action` | no | one sentence | The single concrete next move on this card. |
| `tags` | no | `[..]` | Free labels. |
| `updated_at` | no | ISO timestamp | Powers aging and observed velocity for done cards. |
| `receipt` | no | `{result, summary, changed_files, commands, evidence, note}` | What happened when the card was finished or blocked. |

Derived fields are recomputed on every read. Never hand-set them. In the board payload they serialize as `ready`, `onCriticalPath`, `unblocks`, `unmetDeps`, `ageDays`, the rollups, and the single `next` pointer. You place a card in `backlog` with its `depends_on`, and Plandeck is the one that shows it in Ready the moment those dependencies are done.

A minimal `plan.yaml`:

```yaml
version: 1
plan:
  title: "Ship the onboarding flow"
  slug: ship-onboarding-flow
  north_star: "A new user signs up and lands on the dashboard, proven by the e2e test."
  velocity: null            # optional points/day override; otherwise observed from completion history
cards:
  - id: C001
    title: "Map the problem and the verification path"
    role: scout
    column: doing
    status: active
    estimate: 2
    priority: P1
    next_action: "Read the auth code, write the exact command that proves signup works."
  - id: C002
    title: "Build the signup API"
    role: worker
    column: backlog
    estimate: 5
    priority: P1
    depends_on: [C001]
    verify: ["npm test -- signup"]
```

## Commands

From the repo root, run each command with `node scripts/cli.mjs <cmd>`, or as `plandeck <cmd>` after `npm link` (a published `npx plandeck` release is planned). The commands below use the `plandeck` name for brevity.

- `plandeck init [dir]` scaffolds `plan.yaml` and `plan.md` in `dir` (default `.`).
- `plandeck board <dir> [--once] [--json] [--port N] [--host H] [--actor NAME]` starts or registers a live board. The first process becomes the hub and writes a temporary `plandeck-hub.json` breadcrumb. Later processes verify it through `GET /api/boards`, so they can find the hub on a fallback or ephemeral port, hand over their plan and actor, and exit. Every occupied ladder port is also probed for a compatible hub. Edit `plan.yaml` and the watcher records observed transitions, snapshots changed valid plans, refreshes `NEXT.md` only when its content changes, and streams the board plus hub index over SSE. `--once` generates the static app and exits.
- `plandeck archive <dir> [--json] [--actor NAME]` moves cards with `status: done` or `column: done` into `archive.yaml` and records lifecycle entries. It preserves all plan text outside the removed card ranges, writes each file through a temporary file plus rename, and refuses an id already present in the archive. Archived ids satisfy dependencies, and archived points remain in progress totals.
- `plandeck check <dir> [--json]` validates the plan and runs the completion gate. It exits `1` on a hard error (a parse error, a duplicate id, a dependency cycle, or a dangling dependency) and reports softer issues (more than one active card, aging, unreferenced note files, missing note files) as warnings without failing. Archived dependencies and note references count. It reports `COMPLETE` only when every live or archived card is done and the plan is structurally clean.
- `plandeck next <dir> [--write] [--json] [--since HASH] [--actor NAME]` observes the plan and prints the ONE next action. JSON includes `stateHash`; pass it back with `--since` to receive only an unchanged marker when no card id, effective column, or status changed. `--write` atomically emits `NEXT.md` with recent journal entries.
- `plandeck journal <dir> [--since ISO] [--limit N] [--json]` reads observed history newest-first. Without `--since`, it returns the newest 20 entries. A live hub exposes the same entries at `GET /<slug>/api/journal`.
- `plandeck doctor <dir> [--restore TIMESTAMP|latest] [--json] [--actor NAME]` reports plan health and last-known-good snapshots. Restore is never automatic. An explicit restore atomically replaces `plan.yaml` and saves the replaced content as `plan.yaml.corrupt`.

The hub binds to `127.0.0.1` by default. Its `POST /api/boards` and `DELETE /api/boards` endpoints accept only `application/json` sent with an exact Host header for `127.0.0.1`, `localhost`, or `plandeck.localhost` on the active port. A breadcrumb is only accepted after the hub handshake succeeds.

## Continuity contract for agents

Plandeck remembers observed changes, not only current state. `.plandeck/journal.ndjson` is an append-only mission journal for plan loads, cards added or removed, effective column changes, authored status changes, receipt fingerprints, archive lifecycle events, and doctor restores. `NEXT.md` carries the newest five entries under `Since you left` in chronological order. Never edit the journal or `.plandeck/last-state.json` by hand. They are derived data, like `NEXT.md`.

If you know which model or agent you are, set `PLANDECK_ACTOR` or pass `--actor` to `board`, `next`, `archive`, or `doctor`. Flag value wins over the environment, and the fallback is `unknown-agent`. Actor attribution is best-effort and session-scoped. A board attributes every transition it observes to the actor that registered that plan most recently, regardless of which process changed the file.

A successful board refresh or `plandeck next` snapshots changed, valid `plan.yaml` content into `.plandeck/snapshots/`. The newest 20 are retained. `plandeck check` deliberately remains read-only and creates neither journal state nor snapshots. If `plan.yaml` stops parsing, run `plandeck doctor <dir>` first. Review its parse error and snapshots, then use `--restore latest` or a compact snapshot timestamp only when rollback is warranted. Restore is explicit every time and keeps the replaced content in `plan.yaml.corrupt`.

Polling agents should retain `stateHash` from `plandeck next --json` and pass it to the next call as `--since <hash>`. A matching hash returns only `unchanged` plus the hash. This avoids repeatedly loading the full next-action result when no card id, effective column, or status changed.

Known limits are intentional. The journal grows without rotation. Journal appends have no lockfile, so concurrent processes can rarely duplicate, miss, or interleave a line. The last-state file is only a cache, so this cannot corrupt `plan.yaml`. Continuity write failures warn once and never block `board`, `next`, or `archive`.

## The deterministic brain (no AI)

Everything Plandeck computes is a pure function over the yaml. There is no model call anywhere in it, so the output is identical every run and safe to trust after a reset.

- Ready detection: a topological pass, cycle-guarded. A card whose dependencies are all done becomes Ready. A card inside a dependency cycle is never marked Ready; the cycle is flagged instead.
- Critical path: the longest points-weighted dependency chain, drawn in gold on the board. Unestimated cards use the same one-point default as rollups.
- Rollups: an honest percent complete from points, plus per-column point sums. Archived points remain in the done and total values.
- Velocity and ETA: a positive `plan.velocity` is the configured rate. When it is unset, Plandeck derives an observed rate after at least three dated done or archived cards span one day or more. The payload reports a `configured` or `observed` basis.
- Aging: cards are flagged from `updated_at` after one day blocked, two days in `doing` or `review`, or five days in `ready`.
- Receipt hygiene: `plandeck check` warns about note files with no live or archived reference and card references whose note file is missing.
- `next`: exactly one tie-broken id. It prefers the active card, then a Ready card on the critical path, then priority, then how many cards it unblocks.

## The working loop

Before the first observing command in a session, set `PLANDECK_ACTOR` to the current agent name when known.

1. Start the plan: run `plandeck init .`, or write `plan.yaml` by hand. Give `plan.md` a north star, the observable proof the work is done.
2. Open the board (optional, recommended): `plandeck board .`.
3. Work the ONE active card, the one at `column: doing`, `status: active`. Keep exactly one card active; `plandeck check` warns (it does not fail) if it finds more than one.
4. Record a receipt on that card: `result`, `summary`, `changed_files`, `commands`, `evidence`. For a large receipt, write `cards/<id>.md` and point `receipt.note` at it.
5. Move the card to `column: done`.
6. Run `plandeck next .`. It names the next card. Set that card `status: active`. Cards that were waiting on the finished one appear in Ready on their own.
7. When completed cards make the live plan noisy, run `plandeck archive .`. Dependencies and progress remain correct, and hand formatting outside the archived card ranges stays untouched.
8. Repeat from step 3.
9. Gate completion: `plandeck check .`. It reports `COMPLETE` only when the plan is clean and every live or archived card is done.

If a read fails because `plan.yaml` is malformed or missing, run `plandeck doctor .` before attempting a manual reconstruction or git rollback.

## After a /clear

This is the reason Plandeck exists. After any context reset, do not re-read the whole plan. Run:

```
plandeck next .
```

The terminal prints the single move: the card id, why it is next, and what is Ready now. The fuller breadcrumb (progress, what is blocked, the critical path, recent `Since you left` history, and the board URL) is written to `NEXT.md` by `plandeck next --write`. A running board refreshes it after every valid plan change and skips an unchanged write. Read `Since you left` before resuming so you see the transition sequence that led to the current card. `NEXT.md` is a tiny separate file, never an in-place rewrite of `plan.yaml`, so reading or writing it does not invalidate the model's prompt cache.

Example `NEXT.md`:

```
# ▸ NEXT
**C003 · Build the signup API**  `P1` `critical path` `5 pts` `unblocks 1`
Resume the card already in progress.
- Progress: 15% (5/34 pts, 2/10 cards)
- Ready now: C005, C010
- Blocked: C007
- Critical path: C001 → C002 → C003 → C004 → C008 → C009 (17 pts)

## Since you left
- C004 moved doing → blocked — claude-sonnet-4, 2026-07-13 14:02 UTC
- C004 moved blocked → doing — gpt-5, 2026-07-14 09:10 UTC

- Live board: http://plandeck.localhost:41747/ship-onboarding-flow/
```

## The board

The hub root lists every live board on one port, including archived cards in its done count. Its live dot changes state when SSE disconnects. Each board renders six lanes: Backlog, Ready, In Progress, Blocked, Review, Done. `In Progress` is your `doing` column. `Blocked` is derived from unmet dependencies and `status: blocked`, so you never place a card there by hand. A progress ring shows points done over total with the ETA and its configured or observed velocity basis, and the header shows an archive count when present. A gold "Do this next" banner names the one move. The critical path is drawn as a gold chain. Each card shows its id, estimate, role, priority, risk, and dependency indicators. If YAML stops parsing, a red banner explains that the lanes are the last good state. It is theme-aware (auto, light, dark), Notion and Linear clean, with zero dependencies.

## Where it runs

- Claude Code, as a skill and via the CLI, tested on Windows 11.
- Any agent that runs a shell and reads files can use the CLI (`plandeck board`, `archive`, `check`, `next`, `journal`, `doctor`).
- This file follows the open SKILL.md standard, so it loads anywhere that reads SKILL.md (Codex, Cursor, and others).

## Lineage

Plandeck grows out of planning-with-files (MIT): durable plans on disk that survive `/clear`, plus the deterministic completion gate. The live board, the YAML reader, and the intelligence layer (dependencies, critical path, estimation, velocity, the next-action picker) are Plandeck's own, with zero dependencies.
