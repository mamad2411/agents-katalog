---
name: kanban-meta-triage
description: Supervise a hermes kanban board where agents do the implementation — monitor for stalls and failures, triage blocked cards, preserve card work, and push cards from create to done. Use when running an autonomous kanban loop, when a card is blocked or crashlooping, when board work is not reaching main, or when asked to babysit/triage/unstick a kanban board.
allowed-tools: Bash(hermes kanban:*), Bash(python3:*)
---

# Kanban Meta-Triage

You are not doing the implementation. Workers are. Your job is to keep the board
moving and to catch what the board's own machinery cannot see.

**Before you hand-roll anything, check whether hermes already does it.** The
board is much larger than the four verbs (`list`/`show`/`create`/`comment`) most
sessions use. Reaching for raw SQL or a bespoke script when a first-class
command exists is the most common failure in this loop — and it produces
confidently wrong supervision, because the hand-rolled version encodes
assumptions the real system does not share.

## The live surface (injected at read time — do not trust any hardcoded list)

Everything below this heading is generated when you read this skill, so it
cannot go stale. If it is empty or errors, hermes is not reachable — say so
rather than falling back to remembered flags.

**Command inventory:**

!`hermes kanban --help 2>&1 | grep -v "1Password" | sed -n '/positional arguments:/,$p'`

**`create` flags** (workspace kind, goal loop, retry/runtime caps, skills):

!`hermes kanban create --help 2>&1 | grep -v "1Password" | sed -n '/^options:/,$p'`

**Real `task_events` kinds on the current board** — filter on these, never on
remembered names:

!`"${HERMES_PYTHON:-$HERMES_HOME/hermes-agent/venv/bin/python}" -c "import hermes_cli.kanban_db as kb; conn=kb.connect(); print(' '.join(r[0] for r in conn.execute('select kind, count(*) c from task_events group by kind order by c desc')))" 2>&1 | tail -3`

**Board state right now:**

!`hermes kanban stats 2>&1 | grep -v "1Password" | head -25`

Run `hermes kanban <subcommand> --help` for anything above before you
approximate it by hand.

## Which parts of that surface change how you supervise

The injected help tells you *what exists*; this table is the judgment about
*when it matters*:

| Need | Use | Why it matters |
|---|---|---|
| Watch the board live | `watch --kinds completed,blocked,gave_up,crashed,timed_out,protocol_violation` | Native event stream with kind filtering. Do not poll SQL for this. |
| Health problems the board already knows about | `diagnostics --severity warning\|error\|critical [--json]` | Hermes has its own diagnostics engine. Read it before declaring a diagnosis. |
| Why a card keeps failing | `runs <id> [--json]` then `log <id> --tail N` | Per-attempt history (profile, outcome, elapsed, summary) plus the worker's actual log. |
| What the worker actually saw | `context <id>` | Title + body + parent results + comments, exactly as the worker receives it. |
| Board-level counts | `stats --json` | Per-status/per-assignee counts + oldest-ready age. |
| Open-ended card one shot cannot finish | `create --goal --goal-max-turns N` | Judge loop: after each turn a judge checks the response against the card and lets the worker continue in-session. This is the fix for repeated budget exhaustion. |
| Card that crashloops | `create --max-retries N` / `--max-runtime 30m` | Per-card circuit breaker and runtime cap; the dispatcher SIGTERMs then SIGKILLs and requeues. |
| Force a skill into the worker | `create --skill <name>` (repeatable) | Kanban lifecycle is injected automatically; this adds domain skills. |
| Send a card to a reviewer | `request-review --reviewer <profile> --summary ... --metadata '{...}'` | Reassigns to the reviewer profile on the way in. `--force` overrides the live-claim guard. |
| Reviewer verdicts | `request-changes <id> <reason>` / `reopen-review <ids>` | `request-changes` needs an active review run; `reopen-review` pushes review → ready/todo without one. |
| Recover a stuck card | `promote --dry-run` then `promote [--force]` | `--dry-run` validates without mutating. `--force` promotes past unfinished parents. |
| Zombie/stale worker | `reclaim --reason ...`, `reassign --reclaim <id> <profile>` | Release a claim without waiting for TTL. |
| Structured completion | `complete --summary ... --metadata '{"changed_files":[...],"tests_run":12}'` | Metadata lands on the closing run; summary is the downstream handoff. |
| Backfill a finished card | `edit --result ... --summary ... --metadata ...` | Recovery for cards completed with an empty result. |
| Fan out | `swarm --worker PROFILE:TITLE[:SKILL,...] --verifier P --synthesizer P <goal>` | Parallel workers → verifier → synthesizer graph in one command. |
| Triage column | `specify [--all]` / `decompose [--all]` | Auxiliary-LLM spec fleshing and fan-out. |
| DB looks corrupt | `repair [--json]` | Quarantines and REINDEXes index-only corruption; fail-closed on anything else. |

**Python, not sqlite3.** `hermes_cli.kanban_db` is importable from the hermes
venv and exposes ~130 callables — `connect`, `list_tasks`, `get_task`,
`list_events`, `list_runs`, `board_stats`, `task_graph_context`,
`resolve_workspace`, `detect_crashed_workers`, `detect_stale_running`,
`reconcile_orphaned_running`, `release_stale_claims`, and the full mutation set.
Prefer it over hand-written SQL, which drifts from the schema:

```python
# "${HERMES_PYTHON:-$HERMES_HOME/hermes-agent/venv/bin/python}"
import hermes_cli.kanban_db as kb
with kb.connect_closing(board="sellie-emdash") as conn:
    for t in kb.list_tasks(conn, status="running"):
        print(t.id, t.workspace_kind, t.workspace_path)
```

If you must read the DB directly, use
`sqlite3.connect(f"file:{db}?mode=ro", uri=True)` from Python — the `sqlite3`
CLI returns `unable to open database file (14)` on any JOIN against the live WAL
database while workers hold it, while `SELECT COUNT(*)` succeeds, so it reads as
intermittent. Board DBs are per-board at
`~/.hermes/kanban/boards/<slug>/kanban.db`; the root `~/.hermes/kanban/kanban.db`
has zero tables and looks like a schema problem.

## Workspace kind is the operator's choice, not an anomaly

Every card declares where it runs. This is a first-class field
(`tasks.workspace_kind`), set at creation with `--workspace`:

| `--workspace` | `workspace_kind` | Where it runs |
|---|---|---|
| `scratch` *(CLI default)* | `scratch` | Fresh dir under `<board-root>/workspaces/<id>/` |
| `worktree` / `worktree:<path>` | `worktree` | A real linked git worktree, its own branch |
| `dir:<abs path>` | `dir` | An existing directory — **including the repo itself** |

A board can also set a default: `hermes kanban boards set-default-workdir`.
Note the MCP `kanban_create` tool and the CLI do **not** share a default — the
CLI defaults to `scratch`, and MCP-created cards on this board come out as
`worktree`. Check, don't assume.

**`dir:` is deliberate and supported.** `resolve_workspace` requires it to be
absolute specifically to prevent confused-deputy traversal. Sometimes you *want*
a card to execute in the repository directory, and a card configured that way is
correctly configured. Worktree is the right default for parallel work; it is not
a correctness requirement, and tooling must not treat `dir` as damage.

What `dir` *does* change is how you preserve work — see below.

## What actually deletes work (verified, not assumed)

Both deletion paths — `_cleanup_workspace` on completion and `kanban gc` on
archived tasks — **skip `worktree` and `dir` entirely**. From `kanban_db.py`:

> Only `scratch` workspaces are removed; `worktree` and `dir` workspaces are
> intentionally preserved.

| kind | deleted on complete? | deleted by `gc`? | how work survives |
|---|---|---|---|
| `scratch` | **yes**, if inside the managed workspaces root | **yes**, when archived | declare `artifacts=[...]` on `kanban_complete` — hermes copies them out before cleanup (`_persist_scratch_completion_artifacts`) |
| `worktree` | no | no | commit to the card's branch |
| `dir` | no | no | it is the operator's own directory; nothing to rescue |

Scratch deletion carries a containment guard (#28818): a board `default_workdir`
pointing at a real source tree paired with `scratch` would otherwise `rmtree`
user data, so anything outside the managed root is refused and logged.

**Correction to earlier versions of this skill:** the six cards (~30 files) lost
on 2026-08-12 were `scratch` cards, where removal is by design and the fix is
`artifacts=[...]`. Those losses were real, but they do **not** generalize to
worktree cards, and this skill previously claimed they did. Verify per kind.

## Preserve work — but for the right reason, per kind

- **scratch** — the workspace is genuinely destroyed. Declare deliverables via
  `kanban_complete(artifacts=[...])`, or copy them out before completing.
  This is the only kind with a hard deadline.
- **worktree** — nothing deletes it, so there is no race. Commit anyway, and
  commit *incrementally*: the branch is what gets reviewed and merged, it
  survives manual `git worktree prune`, and a run that dies at its iteration
  cap hands the next run nothing if the work was never committed. A card that
  requests review with an empty branch is asking a reviewer to review nothing.
- **dir** — never blanket-stage. The directory is shared with the human and
  other agents, so enumerating `status --porcelain` and staging every path is
  functionally `git add -A`. If a `dir` card must commit, it stages the specific
  files it wrote, the same rule the repo's CLAUDE.md sets for everyone.

## The loop

0. **Confirm which board you are on.** Every command without `--board` hits the
   *current* board, which is process-global state someone else may have moved.
1. **Arm the board monitor** (`scripts/kanban-monitor.py`, or
   `hermes kanban watch --kinds ...`) before anything else.
2. **Triage what it surfaces** — blocked, failed, stalled, review-requested.
3. **Preserve per workspace kind** (`scripts/preserve-cards.py`).
4. **Contribute evidence, not verdicts**, once the native review lane is working.
5. **Route residuals to the card that owns them** so findings survive scope
   boundaries.

## Always check the active board first

```bash
hermes kanban boards show      # which board am I on?
hermes kanban boards list      # what else exists, and their counts
```

Then **pass `--board <slug>` explicitly on every mutating command.** The current
board is shared mutable state: `boards switch` from any other session or worker
changes what your next unqualified command touches, and nothing in the output of
`create`/`block`/`complete` tells you which board it hit.

Two failure modes this prevents, both observed:

- **Creating a card on the wrong board.** It dispatches immediately and does real
  work in the wrong project's repo.
- **Reading a board by slug is a WRITE.** `connect(board=…)` does
  `mkdir(exist_ok=True)` and initializes a schema, so querying an archived or
  misspelled slug silently *creates an empty board* — which then reads as
  catastrophic data loss. A typo'd `--board` does not error; it manufactures a
  new empty board and answers your query from it. If a board suddenly looks
  empty, check `boards/_archived/` and your own recent commands before
  concluding anything was lost.

## Always tag cards with a project tenant

Boards are the hard isolation boundary; **tenants are the soft filter inside
one.** On any board that carries more than one project, a card without a tenant
is unfilterable and unroutable — it shows up in every query and belongs to
nothing.

```bash
hermes kanban --board <b> create "<title>" --tenant <repo>[:<package>][:<category>] ...
```

**Check the board's existing conventions before inventing a value:**

```bash
# NOTE: `list --json` returns a bare LIST, not {"tasks": [...]}.
hermes kanban --board <b> list --json | python3 -c "
import json,sys,collections
t=collections.Counter(x.get('tenant') or '(none)' for x in json.load(sys.stdin))
[print(f'  {n:>4}  {k}') for k,n in t.most_common()]"
```

Match what is already there. Only mint a new tenant when nothing fits.

**The convention:**

| shape | use | example |
|---|---|---|
| `<repo>` | single-repo project | `hindsight` |
| `<repo>:<package>` | monorepo — package name from its `package.json` | `sellie-emdash:@sellieai/omniroute` |
| `<repo>:<package>:<category>` | optional third segment when the board already uses one | `sellie-emdash:frank:seo` |

The third segment is optional and **must not be invented freshly** — if the
board has no category convention yet, stop at two. A one-off category nobody
else uses is worse than none, because it fragments the filter without adding a
grouping anyone can rely on.

Workers receive `$HERMES_TENANT` and namespace their memory writes by prefix, so
the tenant is not just a label — it scopes what a worker remembers.

## Always assign skills, and look them up before you do

`create --skill <name>` is repeatable and force-loads a skill into the worker.
The kanban lifecycle is injected automatically, so everything you add here is
**domain** knowledge the worker would otherwise have to rediscover — or, worse,
improvise.

**Never type a skill name from memory, and do not try to enumerate them by
hand.** The catalog changes with every `hermes update`, and every shortcut for
listing it is wrong in a different way — all three of these were tried and all
three produced false "missing" verdicts:

| shortcut | why it lies |
|---|---|
| `hermes skills list` + grep | the table **truncates names** (`test-driven-develop…`), so any name over ~19 chars fails an exact match |
| `ls ~/.hermes/skills` | skills are nested under **category dirs** (`skills/devops/sdlc-review/`), so a flat listing misses most of them |
| one skills root | hermes reads **several**: `~/.hermes/skills`, `~/.agents/skills`, the bundled builtins under `~/.hermes/hermes-agent/skills`, plus per-profile `skills/` dirs |

`skills_list()` / `skill_view()` resolve across all roots and return untruncated
names. **Use them; do not reimplement discovery.** A guessed or mis-typed skill
name is the exact failure mode this whole skill exists to prevent — it looks
like it worked.

**Required sequence before creating any card:**

1. `skills_list()` — the full catalog (name + description). `skills_list(category)`
   narrows it: `software-development`, `devops`, `github`, `quality-assurance`,
   `web-development`, `research`, `productivity`, …
2. `skill_view(name)` on each candidate — confirms it exists, shows the real
   content, and reports `readiness_status`. A skill whose status is
   `setup_needed` is missing env or credentials and will not help the worker
   until that is resolved (usually a 1Password item).
3. Pass the confirmed names: `--skill <a> --skill <b>`.

**Match skills to the card's actual work, not its title.** A few that recur on
this board:

| card is about | consider |
|---|---|
| reviewing a handoff / routing outcomes | `sdlc-review` |
| board health, stale or stuck cards | `kanban-board-triage` |
| a bug with unclear cause | `systematic-debugging` |
| a regression the user asked to lock in | `test-driven-development` |
| pre-commit or PR review | `requesting-code-review`, `adversarial-reviewer` |
| verifying another agent's delegated work | `delegated-code-verification` |
| any `.ts` / `.tsx` edit | `typescript-best-practices` |
| EmDash site, plugin, or CLI work | `building-emdash-site`, `creating-plugins`, `emdash-cli` |
| driving or QA-ing a web UI | `agent-browser`, `dogfood`, `web-quality-assurance` |
| a design or sequencing decision | the relevant `principle-*` skill |

Two or three well-matched skills beat a pile. Every skill is context the worker
pays for on every turn, and a card that loads ten of them has less room for the
work than one that loads two.

## Four rules

### 1. Monitor the board, not individual cards

Per-card monitors structurally cannot work. On a 30-card board, 23 cards were
created by `auto-decomposer`, 6 by workers, 1 by the dashboard — **zero** by the
supervising session. A "monitor each card I create" loop has 0% coverage. A
board-scoped cursor over `task_events` covers every card, including ones that do
not exist yet.

### 2. Verify against the artifact, not a proxy

Every wrong call in this loop came from checking something adjacent to the claim:

| Claimed | Checked (wrong) | Should have checked |
|---|---|---|
| "reviewer is working the queue" | a `code-reviewer` process is running | whether a **review-column card** was claimed |
| "the skill fix failed" | the latest run's outcome | whether that run **started after the fix** |
| "the guard fails builds" | piped output to `tail` | the guard's own **exit code**, unpiped |
| "the upgrade builds" | `bun run build` passes | that the new version was **actually installed** |
| "completion deletes the workspace" | the skill said so | `_cleanup_workspace` — it skips worktree/dir |
| "these commits are unsigned" | `git log --format=%G?` → `N` | `git cat-file commit <sha> \| grep gpgsig` (unverifiable ≠ unsigned) |

### 3. Contribute evidence, not verdicts

Hand-review only while the review lane is starved. Once it recovers, **stop** —
an approval that races a reviewer completes the card out from under them and
makes `request-changes` illegal, destroying a valid changes-requested verdict.
Check `has_spawnable_review` / whether a review-column card was claimed, not
whether a reviewer process exists.

Post findings as comments and let the lane decide. Both passes then happen, and
reviewers catch things you miss.

### 4. Park with `schedule`. Reserve `blocked` for things that need a human.

**Default to `schedule` for backlog.** `blocked` means *someone must act*; a
board where every parked card is `blocked` teaches the operator that blocked is
noise, and then a card that genuinely needs them gets skipped. `scheduled` says
"not now" without making a claim on anyone's attention.

```bash
hermes kanban --board <b> create "<title>" --body "..." --json   # capture the id
hermes kanban --board <b> schedule <id> "Backlog — parked pending <what>."
```

It holds unconditionally: `recompute_ready` promotes only from
`('todo','blocked')`, so a `scheduled` card is never even considered. Release
with `unblock <id>`, which accepts both `blocked` and `scheduled`.

Use `blocked` only when the reason names a person's decision:

| state | means | releases |
|---|---|---|
| `schedule` | not now; nobody is waiting on anybody | `unblock` |
| `blocked --kind needs_input` | a human must decide | `unblock` |
| `blocked --kind capability` | hard wall: no access, missing credential | `unblock` |
| `blocked --kind dependency` | waits in **todo**, auto-promotes when parents finish | automatic |
| `blocked --kind transient` | maybe-flaky failure | retry |

Repeated same-kind re-blocks after an unblock route the card to triage
automatically to break unblock loops (`block_loop_detected`) — another reason
not to use `blocked` as a parking lot.

**`schedule` on this build takes no time argument.** The docs describe
`create --scheduled-at <ISO8601>` and `schedule --at <ISO8601>`; neither exists
here, and there is no `scheduled_at` column — see `references/hazards.md` B6.
`schedule` parks; it does not wake anything up later. If a card must start at a
time, that is a cron job, not a card.

**Two states that do NOT park:**

- `--initial-status blocked` on `create` sets the status and the create response
  really does say `blocked` — then the dispatcher **promotes it within seconds**,
  because a block with no `block_kind` is not a human gate. Observed 2026-08-14:
  created blocked 16:51:38, `promoted` 16:52:01, spawned, ran the work to
  completion. This entry has now been wrong in both directions ("fails
  silently", then "works"); both readings came from checking the create response
  instead of the card a minute later. **Check the card, not the call.**
- `triage` — auto-decompose fans it into children, one of which reaches `ready`
  and dispatches.

## Detect absence, not just events

A hung worker emits nothing. Silence is indistinguishable from progress, so half
the monitor is absence-detection. Hermes already implements most of it — prefer
these over reinventing them:

- `detect_crashed_workers` — reclaims running tasks whose worker PID is dead;
  appends a `crashed` event. When the worker exited **rc=0** while the task was
  still running, it records `protocol_violation` — the worker answered
  conversationally without calling `kanban_complete`.
- `detect_stale_running` — reclaims on heartbeat gap; **disabled by default**
  (`stale_timeout_seconds=0`), so a board with it unset has no stall detection.
- `reconcile_orphaned_running` — requeues zombies whose claim bookkeeping broke
  (running with NULL `claim_lock`/`claim_expires`), which no other path touches.
- `release_stale_claims` — TTL-based claim expiry.

Two calibration rules learned the hard way:

- **Report the observation, not a guessed cause.** "Dispatcher likely dead" was
  emitted while the gateway was healthy; the real cause was a decomposer no-op.
- **Only flag work that could actually progress.** `todo` cards behind a blocked
  parent, `triage`, `scheduled`, and `blocked` are legitimate resting states.
  Flagging them trains the operator to ignore the monitor.

## `task_events` kinds

The authoritative list is injected at the top of this skill. Never filter on a
remembered name — a wrong kind matches zero rows and fails **silently**, which
is indistinguishable from "nothing went wrong".

**`crashed` IS a real kind.** An earlier version of this skill asserted it was
not, which would make a monitor drop every crash on the floor. `started` and
`failed` are genuinely absent. That error is exactly why this section no longer
hardcodes anything.

The terminal-failure set worth filtering on:
`gave_up, timed_out, protocol_violation, crashed, blocked, block_loop_detected,
changes_requested`.

`protocol_violation` deserves specific attention — it means the worker exited
**rc=0** while its card was still `running`, i.e. it answered conversationally
without ever calling `kanban_complete`. It is a worker-behaviour bug, not an
infrastructure failure, and retrying it unchanged reproduces it.

Re-derive at any time:

```sql
select kind, count(*) from task_events group by kind order by 2 desc;
```

## Scripts

```bash
# Board monitor — arm as a persistent background watcher.
python3 scripts/kanban-monitor.py           # BOARD=<slug> to target another board

# Preserve card work, dispatching on workspace_kind. Commits worktree cards to
# their own branch; reports scratch cards needing artifacts=[...]; never
# blanket-stages a dir card.
python3 scripts/preserve-cards.py
```

Monitor output is tagged `[ATTN]` (needs your decision), `[FLOW]` (pipeline
advanced), `[HEALTH]` (absence of progress), `[MON-ERR]` (the monitor itself
failed — so its silence can never be mistaken for success).

See `references/hazards.md` for the full failure catalog with reproductions.
