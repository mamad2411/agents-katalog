---
name: hermes-kanban
description: Manage the Hermes-native kanban board via the `hermes kanban` CLB (SQLite-backed at ~/.hermes/kanban.db and per-board ~/.hermes/kanban/boards/<slug>/kanban.db). Use when the user asks to "add to kanban", "put this on the kanban board", "create a kanban board", track action items / TODOs / triage items on a Hermes board, or manage cards/columns there. NOT for the `bd`/beads project issue tracker (see beads-setup) and NOT for the `triage` issue-tracker state machine — those are separate systems.
version: 0.1.0
triggers:
  - hermes kanban
  - kanban board
  - add to kanban
  - kanban triage
  - kanban card
---

# Hermes Kanban

The Hermes kanban is a durable SQLite-backed task board, shared across Hermes profiles, driven by the `hermes kanban` CLI. Cards can be executed autonomously by worker agents OR parked as human-action items.

## Three tracking systems — don't confuse them

When the user says "kanban", they mean THIS (the Hermes board). But two other trackers commonly coexist on the same machine:

- **Hermes kanban** (`hermes kanban`, `~/.hermes/kanban.db`) — agent task-execution board. The dispatcher can spawn worker agents to *do* cards. THIS skill.
- **`bd` / beads** (`~/darwin` and other repos) — git-tracked project issue tracker (Dolt-backed). See `beads-setup`. Topically scoped to a repo; don't put personal/email items here.
- **`triage` skill** — a state-machine workflow for triaging *issues* on an issue tracker (labels/roles). Unrelated to the Hermes board.

If the user says "kanban" plainly, default to the Hermes board. If they're inside a repo and mean issue tracking, ask or use `bd`.

## Key fact: tables are `tasks`, not `cards`

The schema uses a `tasks` table (plus `task_comments`, `task_links`, `task_events`, `task_runs`, `task_attachments`, `kanban_notify_subs`). There is NO `cards` table — querying `SELECT ... FROM cards` errors with "no such table: cards". Prefer the CLI over raw SQL.

## CLI quick reference

```bash
hermes kanban boards                       # list boards, show current
hermes kanban boards create <slug> --name "Display Name"   # new board
hermes kanban boards switch <slug>         # set current board
hermes kanban --board <slug> create "Title" --body "..." [flags]  # add a card to a specific board
hermes kanban --board <slug> list          # list cards on a board
hermes kanban --board <slug> show <id>     # full card + comments + events
hermes kanban --board <slug> comment <id> "note"
hermes kanban --board <slug> complete <id> # mark done
hermes kanban --board <slug> block <id>    # mark blocked
hermes kanban --board <slug> unblock <id>  # blocked/scheduled -> ready
hermes kanban --board <slug> archive <id>
```

Always pass `--board <slug>` explicitly when not on the current board — it's cleaner than relying on `switch`.

## Creating cards — the flags that matter

```bash
hermes kanban --board <slug> create "Title" \
  --body "Full description with context/source" \
  --priority <int> \            # tiebreaker, higher = sooner
  --created-by "Cooper Maruyama" \
  --json                         # emit JSON (returns the task id, e.g. t_4aabd479)
```

Other useful flags: `--assignee <profile>` (who executes it), `--triage` (park in triage; a specifier fleshes out the spec then promotes to todo), `--skill <name>` (force-load a skill into the worker, repeatable), `--max-runtime 30m`, `--goal` + `--goal-max-turns N` (run worker in a judged goal loop), `--idempotency-key <key>` (dedup — returns the existing id instead of duplicating).

Task ids look like `t_<hex>` (e.g. `t_4aabd479`).

## Human-action items vs agent-executable cards — CRITICAL

The Hermes kanban dispatcher can auto-spawn worker agents to EXECUTE cards. When the cards are really TODO / triage / review items meant for a HUMAN (deadlines, replies, decisions, "verify X was intentional"), you do NOT want a worker blindly running them.

Safe parking, in order of reliability:
1. **Leave `--assignee` unset.** Unassigned cards do not auto-dispatch — the dispatcher needs an assignee profile (and a running daemon) to pick a card up. This alone keeps human-action cards inert.
2. Use a dedicated board (e.g. `email-triage`) so they don't mix with executable work.

PITFALL — `--initial-status blocked` does NOT stick for unassigned cards: passing `--initial-status blocked` on `create` is intended for the running->blocked R3-gate transition; freshly-created unassigned cards still land in `ready`. That's fine because unassigned `ready` cards don't dispatch anyway. If you truly need them blocked, run `hermes kanban --board <slug> block <id>` after creation. Don't assume `--initial-status blocked` produced a blocked card — verify with `list`.

## Workflow: dumping a list of action items onto a board

1. `hermes kanban boards create <slug> --name "..."` (e.g. `email-triage`).
2. Script the card creation with the CLI (one `create` per item) — loop in execute_code, shlex-quote titles/bodies, capture the returned `t_...` id from `--json`.
3. Put real context in `--body`: source, date, deadline, sender — so the card is self-contained.
4. Set `--priority` higher for deadline/urgent items.
5. Leave `--assignee` unset for human-action items.
6. Verify with `hermes kanban --board <slug> list` and report the ids grouped by urgency.

Reusable helper: `scripts/bulk_create_cards.py` — edit `BOARD` + `CARDS` (list of `(title, body, priority)`), run it, and it creates each card (assignee left unset) and prints the `t_<hex>` ids. Works inside execute_code via `hermes_tools.terminal` or standalone via subprocess.

## Pitfalls

- **No `cards` table** — schema uses `tasks`. Raw SQL against `cards` fails. Use the CLI.
- **Per-board DBs** — the default board lives in `~/.hermes/kanban.db`; named boards live at `~/.hermes/kanban/boards/<slug>/kanban.db`. `boards create` prints the path.
- **`--initial-status blocked` ≠ blocked for unassigned cards** (see above). Verify; `block <id>` after creation if needed.
- **Don't auto-assign human TODOs** — leaving `--assignee` unset is what keeps them from being executed by a worker agent.
- **`hermes kanban create` requires a current board or `--board`** — set/confirm the board first.

## Cross-references

- `bd` / beads project issue tracker → `beads-setup` skill.
- Issue-triage state machine → `triage` skill.
