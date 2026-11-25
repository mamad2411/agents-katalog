---
name: swarm-orchestrate
description: Optional autonomy control plane — configure, plan, launch, monitor, recover, or stop local CLI-agent workers through SwarmVault's durable supervisor. Use for fit/budget-aware platform + model + reasoning-effort routing; a consistent pre-start/live/boundary/on-demand board with ticket drill-down; TOLD/MEASURED/EST usage and run accounting; bounded event-driven waits; stale-worker and possible-quota recovery; safe context compaction; launch adapters; and consent-gated continuation across provider resets.
---

# swarm-orchestrate — optional local autonomy

**Gate:** this add-on is disabled by default. Do not enable it, configure write access, or
start workers unless the user explicitly asks. Tickets and atomic claims remain the source of
truth; signals and controls never override a healthy claim.

## What this is for (read before configuring anything)

The goal is **the right model on the right task, at the lowest token cost** — parallelism is
only one means to that end, and often not the right one. So orchestration has two separate
decisions, and conflating them is the classic mistake:

1. **Fit — always on, at every level.** Which platform, model, and reasoning effort each task deserves,
   from its kind (design / planning / coding / review / docs), its size, and each platform's
   remaining usage. A docs ticket never burns a flagship model; a design ticket never gets a
   cheap one. This is not something the user buys by going slower.
2. **Acceleration — the speed level, and the *only* thing the user chooses.** How eagerly
   work is handed to *other* agents instead of done in the current session.

## Enable — two design questions, then the numbers only they can see

1. Confirm the project is registered and has dependency-ready tickets.
2. Ask the two **design** questions:
   - **"Which agentic platforms do you have?"** — the tools installed on their machine:
     `claude-code`, `codex` (verified), `gemini`, `opencode`, `droid`, `cursor`, `copilot`,
     `amp` (best-effort), or any other agent CLI by name. Offer the list *and* an "other"
     option; a platform with no adapter still works as a cooperative worker, or gets a
     `--launch-cmd` template.
   - **"How much acceleration is allowed?"** — `slow` | `standard` | `fast` (below). Plus:
     *may these workers edit code?*
3. **Never ask for a worker count, a concurrency ceiling, or a model name.** Those are not the
   user's decisions: ceilings derive from the level, and the platform+model per task come
   from fit. Asking for a model produces exactly the wrong answer — one model cannot be
   right for both a large design task and a docs chore.
4. **Do ask for the usage numbers — you cannot read them.** Per platform: *which plan are you
   on · what limits does it show (per session/day, per week, both) · when do they reset · are
   any other sessions running I can't see · may I schedule a continuation automatically if a
   limit is about to run out?* Look up per-model costs yourself first; ask only if the lookup
   fails. See **Usage — you are blind without the user** below; the full interview and the
   per-platform notes are in `references/usage-limits.md`.
5. One command:

```bash
python3 /path/to/swarmvault.py supervisor setup --project MyApp \
  --platforms claude-code,codex --speed standard --start
# --read-only            workers may read/plan but never edit code
# --isolation worktree   each worker gets its own git worktree + branch (see below)
# --launch-cmd 'kiro=kiro run --dir {cwd} {prompt}'   wire an agent with no built-in adapter
# --self-platform codex  which platform THIS session is (else $SWARMVAULT_PLATFORM)
```

`--project` may be omitted when you are in the project directory. The supervisor runs
locally, never uses a shell to launch workers, and logs every spawned process in the vault.

Read what `setup` prints back. Two of its lines are about this machine rather than your
choices, and both change what actually happens:

- **`host`** — how many concurrent workers this machine holds. A worker is not just an agent
  process; it also runs the ticket's tests and build, which dominate. The ceiling is
  `(available memory − reserve) ÷ per-worker footprint`, measured from `/proc/meminfo` and any
  cgroup limit, and it **overrides the speed level's ceiling when it is lower**. Over-subscribing
  memory does not degrade gracefully: the host kills the guest, and every worker, the lead
  session and the supervisor die at once with nothing recorded. Tune the footprint with
  `supervisor configure --platform <p> --worker-memory-mb N` if your suite is heavier or
  lighter than the 1200 MB default (that number is an EST, and it says so).
- **`tree`** — whether workers share one working tree. See below.

## Working-tree isolation

`shared` is the default because it is the only mode that works for every project shape — no
git, whole-file generated artefacts, uncommittable local state. Above one worker it is
genuinely unsafe, and the board says so rather than letting you find out:

- a half-written file from one ticket breaks an unrelated ticket's build;
- an in-flight edit (a widget arming a timer, a half-applied migration) can hang everybody's
  tests;
- whole-file generated output means any commit touching it carries other tickets' changes;
- **no worker can run the suite to check its own work**, because the suite reflects six other
  tickets' half-finished states.

`--isolation worktree` gives each worker its own `git worktree` on branch
`swarmvault/tk-nnn`, and the lead merges the branches. Nothing in a worktree is ever deleted
automatically — an uncommitted change there is somebody's unmerged work, and the board lists
each worktree with its dirty count so it can be dealt with deliberately.

## The speed levels — what each actually does

| level | hands a task to another agent when… | ceiling (per platform / total) | usage reserve | reconcile |
|---|---|---|---|---|
| `slow` | **only** when another platform's model fits the task better than this session | 1 / 1 | 35% | 180s |
| `standard` | better fit, **or** there is genuinely independent work worth overlapping | 2 / 4 | 15% | 60s |
| `fast` | anything runnable — spread as wide as capacity allows, independent tickets batched | 4 / 8 | 5% | 30s |

Every routing decision comes back marked `execute: dispatch` or `execute: in-session`:

- **`dispatch`** — launch/wake that platform's worker on that model.
- **`in-session`** — *you* take this ticket, now, on the `model` in the plan. This is not a
  fallback, it is the point of `slow`: quality routing without paying for a second context.
  The pre-plan shows it as an unclaimed recommendation. It becomes running only after an
  atomic claim or live signal.

If this calling session is already working, declare `--session-state busy`. The route becomes
`awaiting-session` and stays queued; do not describe it as assigned, claimed, or running.

So at `slow` a single session behaves like a well-run one-person team: it picks the right
model for each task, switches to it, `checkpoint`s and compacts when context grows
(*Self-management*, below), and only calls in another agent when that agent is genuinely
better at the task in front of it. At `fast` the same routing runs, but everything runnable
goes out at once.

Two guarantees hold at every level: a platform below the level's **usage reserve** is parked
unless nothing better is free (so no level eats a platform's last quota), and work over the
ceiling is never dropped — one ticket is routed to the calling session and the rest are
queued with a stated reason. A platform that is out of *usage* (not out of slots) defers
instead, which is what feeds usage-limit continuation.

`budget`/`balanced` are accepted as older names for `slow`/`standard`. The per-platform
`configure` action still exposes the raw knobs (`--max-workers`, `--model`, `--models`,
`--launch-cmd`) — reach for it only when the user asks for that level of control.

## Operate

- `supervisor status --project MyApp` — inspect enabled state, PID, workers, and status.
- `orchestrate --project MyApp` — print the full pre-dispatch board, reconcile once, then
  print the live/post-dispatch board (add `--json` for raw state).
- `orchestrate --project MyApp --plan` — read-only pre-dispatch plan; no launch/control/claim.
- `orchestrate --project MyApp --wait [seconds]` — return on one durable worker event or a
  bounded timeout (hard cap: five minutes), reconcile after an event, then return control.
  See *Waiting* below; this is the only way you may wait on a worker.
- `signal --project MyApp --agent <id> --event heartbeat` — worker health/progress.
- `inbox --project MyApp --agent <id>` — worker reads pending controls; acknowledge with
  `--ack <id>`.
- `control --project MyApp --agent <id> --action stop|wake|retry` — durable request; it is
  not a claim revocation or arbitrary process kill.
- `supervisor run --project MyApp --until-idle` (or `--max-seconds N`): a bounded foreground
  reconciliation loop. Plain `supervisor run` is the daemon's own loop and does not return;
  it is for systemd/launchd or a terminal, never for you.
- `supervisor stop --project MyApp` — stop only the supervisor. `disable` prevents restart.

## Waiting: the contract, and why you always get control back

`orchestrate --wait [seconds]` is bounded by construction. It returns on the **first** durable
event or at its deadline, and it always prints why it returned, from a closed set:

| Wake reason | What happened | What you do next |
|---|---|---|
| `progress` | a worker signalled progress | keep going; check the board if it names your ticket |
| `terminal` | a worker signalled `done` or `blocked` | reconciliation already ran; read the board, take the next ticket |
| `worker-exit` | a launched worker died without signalling | its log path is on the row; the slot is already free |
| `heartbeat-stale` | a worker went silent past its TTL | check health; reassignment goes through the stale-claim protocol |
| `quota-wait` | usage exhaustion was classified | see *Recovery and quota limits*; the platform or the ticket is parked |
| `control-ack` | a worker acknowledged a control request | expect work to start; wait again |
| `timeout` | nothing changed inside your window | do useful local work, then wait again |

Using it correctly:

1. **Dispatch, then wait, then act, once per turn.** Never chain waits back to back. If you
   have local work, do it and wait afterwards.
2. **Keep one identity.** The wait remembers its position in the signal stream, keyed by your
   agent id. That is what makes an event which landed *between* two waits wake the next one
   instead of being lost. Pass `--agent <id>` (or set `$SWARMVAULT_AGENT`) when two sessions
   drive the same project, so each keeps its own position; otherwise the project's stored
   identity is reused. Never invent a new id per invocation.
3. **`--reset-cursor`** is the deliberate way to start again from the present. Do not use a
   fresh identity for that.
4. **A timeout is information, not a failure.** It means no worker changed state in that
   window. Say so plainly and carry on.
5. **Never poll in a loop and never watch on a timer.** Between waits read
   `orchestration/status.md` (rewritten by every reconciliation, free to read) or `--brief`.

If an invocation reports that another healthy leader holds the lease, it planned nothing,
dispatched nothing and reaped nothing. Report that, rather than a completed cycle.

## Usage — you are blind without the user (FR-28)

**You cannot read your own usage limits. No agentic CLI exposes them.** Say where every number
came from: `TOLD` (provider UI/user), `MEASURED` (local signal/process/tool observation), or
`EST` (derived). A local measurement is not automatically a provider reading.

**Set it up once, per platform:**

```bash
usage setup --platform <platform> --plan "<provider-plan>" \
  --window <provider-window> --hours <hours> --resets-at <ISO>
usage setup --platform <platform> --window <provider-window> \
  --limit <displayed-limit> --resets-at <ISO>
usage sessions --note "<other sessions this process cannot see>"
usage consent --auto-schedule yes                                 # standing consent, revocable
```

If they only know percentages, skip `--limit` — the burn rate is learned from readings alone.
If they don't know a reset time, leave it out; you will not schedule against a guess.

**Count what you burn.** Every `release --done` estimates the ticket's cost from its `tier`,
`kind` and model and adds it to the ledger (pass `--model` so the estimate isn't assumed).
Log anything outside the ticket flow yourself:

```bash
usage spend --platform <platform> --tier <tier> --kind <kind> --model <model>
usage spend --platform <platform> --tokens <measured-token-count>
usage metrics --platform <platform> --model <model> \
  --input-tokens <n> --output-tokens <n> \
  --cache-read-tokens <n> --cache-write-tokens <n> \
  --cost <amount> --api-seconds <n> --wall-seconds <n> --provenance MEASURED
```

**Correct yourself — this is the part that matters.** Whenever the user pastes a real figure:

```bash
usage record --platform <platform> --window <provider-window> --used <displayed-percent>
```

The rate re-learns from the gap, so the next estimate is better. Ask for a reading whenever
the board says one is stale, and re-ask about invisible sessions after a day — someone else's
session on the same account is the single biggest source of drift, and only they can see it.

**Never** state a usage number without its provenance, never convert an estimate into a fact
by repeating it, and never let a missing answer become an assumed one — the board prints the
open question instead, and so should you.

**Keep meters separate.** Context/compaction capacity is `--meter context`, displayed as
`context, not quota`, and never parks a provider or schedules continuation. Provider allowance,
non-cache input/output, cache read/write, monetary cost, API time, and wall time are distinct
columns. Never infer one from another.

## Smart assignment — size, budget & model fit (runs at every speed level)

- **Budgets come from the usage ledger**, tightest window first, projected forward from the
  user's last reading. A platform you know nothing about stays *unknown* — and unknown never
  silently becomes zero. `signal --event budget` survives only as a relay for a figure the
  user gave a worker; prefer `usage record`.
- **Big tasks → the platform with the most remaining usage**, preferring one whose configured
  model fits the task kind; **small tasks / supervision → the least-budget platform**, so the
  big-budget ones stay free for big work. Empty/quota platforms are skipped (→ continuation).
- **Provision the model to the task kind** (design / planning / coding / review / docs) and
  **size** — flagship models only where `tier: top` or a demanding kind needs them; cheap+fast
  for docs/boilerplate. Route reasoning effort independently. Wire overrides with
  `configure --models 'design=…,coding=…' --efforts 'design=high,coding=high,docs=medium'`.
- Keep the picks current from [artificialanalysis.ai](https://artificialanalysis.ai). Full
  method and the kind→strength table: `references/model-routing.md`.

**This is level-independent.** `slow` does not mean "use a weaker model" and `fast` does not
mean "stop caring" — the same table decides the model either way. With one platform (or at
`slow`, where most work stays here) it is *you* switching models per task rather than a
worker being launched with one; see *Self-management* below.

## The board — one complete view at every trigger point

`board --project MyApp` renders every agent, **any platform, in the current CLI**. Use the
same full renderer:

- **Before start:** `orchestrate` must print `PRE-DISPATCH PLAN` before any launch.
- **While working:** every reconciliation shows running, queued, blocked, completed,
  platform usage, separate run metrics, forecast, signals, and open questions.
- **After finish/boundaries:** do not swallow the board emitted by `release --done`,
  `done`/`blocked`/`quota-wait`, and `checkpoint`; also print it for milestones, phase gates,
  validated specs, and other boundaries the CLI cannot see.
- **On demand:** full, brief, live, pre-plan, or ticket drill-down.

Every running/queued row includes ticket, description, tier/kind, platform, model, effort,
route rationale, ETA/provenance/confidence, estimated tokens, estimated window cost,
current→after usage, dependencies/unblocks, and executor/state. Blocked rows say exactly what
they wait on and the next action. Unknown values say what reading/configuration is needed.
Each ticket must occur in exactly one current-state section. Treat terminal ticket state as
authoritative over late signals/process records. A dependency-only `status: blocked` ticket
reopens when all `requires` edges are done; reserve `blocker_kind: manual` with a
`blocked_reason` for a real hold that must remain. A current claim is durable ownership:
render it as running/claimed and reserve its capacity even when a collaboration worker has no
OS-visible PID; say that liveness telemetry is unavailable rather than making it disappear.

```
board --project MyApp            # full report on demand
board --project MyApp --plan     # read-only pre-dispatch plan
board --project MyApp --ticket TK-NNN  # ticket body, claim, route, estimates, signals
board --project MyApp --brief    # ONE line — for frequent mid-work check-ins
board --project MyApp --verbose  # + each worker's dispatched prompt and recent log lines
board --project MyApp --html     # one self-contained page, written once, for a human to keep open
```

`--watch N` exists for a human at a real terminal. It is not yours: a command that redraws on
a timer spends a turn per redraw and, without a terminal or `--iterations N`, has no natural
end. Use `status.md` or `--brief` instead.

**And when you print it, close the loop:** if the board carries a CHECK MY ASSUMPTIONS block,
put those questions to the user in your own message — a stale reading, unknown limits, unseen
sessions, missing scheduling consent. One paste back and every estimate on the next board is
sharper.

**Monitoring must not cost what it monitors (FR-21).** The full report belongs at boundaries;
between them use `--brief` (one line), the `orchestration/status.md` snapshot every
reconciliation rewrites (free to read, no agent turn), or the one-line swarm summary already
in injected session context. A dynamic `board` always rereads the current ledger/tickets/signals;
do not repeat a stale status snapshot after a newer provider reading. Never spend an agent
turn on a timer or per heartbeat.

Workers make the board rich by signalling meaningfully:
`signal --event progress --reason "auth wired, tests green"`.

## Agent roster & launch adapters

Any agent can be a **cooperative worker** — run the swarm-implement worker loop
(claim → build → test → release) against the shared vault; claims are the referee. The
supervisor can also **launch** workers headlessly, via a declarative adapter registry with
three tiers:

- **Verified** — `claude-code`, `codex`. Spawned without a shell, exact flags known,
  ownership verified by the atomic claim. Both a `write` and a real read-only mode.
- **Best-effort** — `gemini`, `opencode`, `droid`, `cursor`, `copilot`. Sensible default
  invocations for fast-moving CLIs. **Confirm the flags for your installed version**, or
  override. These launch **only with `--allow-write`**: read-only headless launch is offered
  only where a genuine read/plan mode is known, so a read-only request can never accidentally
  start a writing agent. A wrong flag fails visibly (the exited process is logged as blocked),
  never silently.
- **Any other agent** (Windsurf, Kiro, Trae, Continue, Augment, Warp, …) — wire it with a
  command template you vouch for:

  ```bash
  supervisor configure --project MyApp --platform kiro --allow-write \
    --launch-cmd 'kiro run --dir {cwd} {prompt}'      # tokens: {cwd} {model} {prompt}
  ```

  With no adapter and no `--launch-cmd`, the supervisor records a **manual-action** request
  (start that agent yourself) rather than guessing a command.

Never assume one platform can command another (Claude Code cannot drive Codex, or vice versa);
each adapter only declares what it can do.

## Usage limits & continuation (FR-23)

Long projects outlast a single provider usage window. This works **with or without the
supervisor** — even a solo agent should offer it.

1. **Watch the estimate.** The board's USAGE LEFT is your signal — an estimate, so say so. When
   a window is projected past ~90%, stop at a safe point rather than dying mid-ticket. Don't
   wait for a tidy block boundary: an unfinished block is recoverable, a session killed
   mid-edit is not.
2. **Get consent.** Standing consent (`usage consent --auto-schedule yes`) means you may
   schedule without asking again — say that you're acting on it. Otherwise ask: *"My estimate
   says you're near the weekly limit. Continue automatically after it resets — until the whole
   project is finished, or until a point you name (e.g. end of M3)? Or stop here?"*
3. **Confirm the reset time.** Use the real datetime — told by the user, or rolled forward from
   a told reset. Never invent one. Unknown → schedule nothing, say so, leave a note.
4. **Schedule and record in one command:**

   ```bash
   python3 /path/to/swarmvault.py schedule set --project MyApp \
     --at 2026-07-29T09:00:00Z --scope until-finish --confirm
   ```

   Without `--confirm` (and without standing consent) it prints the exact command it *would*
   install and stops. With it, it installs a real one-shot wake — `at`, else a tagged crontab
   line, else printed manual instructions — and writes the durable continuation record, which
   surfaces in session context (`⏳ Scheduled continuation`) so no other session double-schedules.
   **Tell the user the device must stay on and awake**, or the wake cannot fire.
   `plan-continue set` still records intent without installing anything.
5. **Clean up.** The wake removes its own one-shot when it fires. When the project (or the named
   `--scope`) is finished, clear the rest: `schedule clear --project MyApp`. A resumed session
   that finds the work already complete clears it instead of looping. Leave nothing installed
   on their machine that outlives the work it was for.

**Scope, and it is not negotiable:** the only thing you may ever schedule on a user's machine
is *waking or supervising an agent on a registered project*. Not a fetch, not a build, not a
deploy, not a cleanup script — however helpful it would be, and even with full environment
access. `schedule` takes no shell command precisely so this cannot happen by accident.

For the supervisor path, a worker that hits a limit emits `quota-wait --retry-at <ISO>`; the
supervisor persists the wait, avoids relaunch loops, and retries only at/after that time, and
may choose another eligible provider only if the ticket policy permits.

## Self-management — one session, orchestrated (this IS `slow`)

At `slow` — and any time a plan entry comes back `execute: in-session` — orchestration means
managing *yourself* instead of spawning anyone:

1. **Switch model to the task.** Use the `model` in the plan entry (or the per-kind table in
   `references/model-routing.md`): strong model for design/planning/review or a `tier: top`
   ticket, cheap and fast for docs and boilerplate. On platforms where the user drives the
   model choice, say which model you want and why in one line rather than silently continuing
   on the wrong one.
2. **Compact at safe boundaries** rather than carrying a bloated context into the next ticket
   (below).
3. **Only then consider a second agent** — when the routing says another platform's model
   genuinely fits the next task better, dispatch that one ticket, not the whole queue.

This is the token-frugal path: one context, right-sized model per task, no re-establishing
project state in a fresh agent for work you could finish here.

On a long task, when your context grows large **and you are at a safe, resumable point**
(ticket done, phase boundary, a planning milestone recorded):

1. `checkpoint --project MyApp --did "…" --next "…"` — records a safe-state session note.
2. Make sure flow-state, tickets, and memory are current (they are your real state, J1).
3. Compact/clear your context (your platform's mechanism), then continue — the SessionStart
   context rebuilds from the vault.

**Quality outranks token-saving.** Never compact mid-reasoning, mid-edit, or when continuity is
carrying the task — if the work needs the tokens, keep them and finish well. Compaction is for
*safe* boundaries only.

## Recovery — when the board shows workers that are not there

**One command. Do not hand-clear files.**

```bash
python3 ~/.swarmvault/scripts/swarmvault.py recover --project P            # clear it
python3 ~/.swarmvault/scripts/swarmvault.py recover --project P --dry-run  # look first
```

"This worker is gone" lives in three places — the process record, the claim file, and the
signal stream — plus the leader lease and the sync lock. Clearing fewer than all of them
leaves a ticket undispatchable while every surface you check says it is free. `recover` finds
them together, clears them together, prints one line per record, and reconciles. The board's
BLOCKED table prints this same command as the next action, so the path forward is on the
screen that shows the problem.

`recover` deletes a record only when the worker is **provably** gone: a launched pid that is
not running on this host, or an agent whose last signal is terminal or past the retirement
horizon. "I cannot see it" is never "it died" — a worker launched on another host, or one that
is merely silent, keeps its claim.

**Do not use `pgrep` to check.** A shell command that mentions SwarmVault workers matches its
own command line, so `pgrep -af "SwarmVault worker"` reports live workers at a moment when
zero exist. `recover --dry-run` and `board` are the checks; they read process records and
`/proc`, not a pattern that can match the asker.

Reconciliation does the same work automatically each cycle: a claim behind a provably dead
worker is released, the ticket note records who held it and why it went, and the slot is
freed. Counting those claims as capacity is what let a board report seven running workers
against zero processes while dispatch queued nothing.

### Whose files were those?

Every launched worker records a `git status` snapshot before it starts. When it exits — cleanly
or not — the difference is written to `orchestration/attribution/TK-NNN.json` and appended to
the ticket. Work stranded by a dead worker is attributed instead of anonymous, so a relaunched
worker can tell its own prior output from another ticket's.

## Quota limits, and the failure that impersonates them

Workers signal `quota-wait --retry-at <ISO-8601>` rather than retrying blindly. `--retry-at` is
optional: without a real reset time the wait is still recorded, the work is parked, and the
board shows the open question. Nothing is ever scheduled against a guessed reset.

**Exhaustion arrives at one of five verdicts; say which one you have.**

| Level | Evidence | Effect |
|---|---|---|
| `confirmed` | a reading you were given that is at or over the limit, or a provider error the platform's profile records as exhaustion | that platform is parked for routing until its told reset; continuation (FR-23) may be offered |
| `inferred` | a worker log matching that platform's exhaustion patterns | the ticket is parked against a relaunch loop; ask for a confirming reading |
| `suspected` | repeated short-lived exits on one platform with no other explanation | stop dispatching there, show the pattern, ask |
| `ambiguous` | wording the platform emits for **both** a provider cap and a worker running out of its own context — "session limit" is the standard example | the ticket is parked; **no platform is parked**, because the log cannot tell the two apart. Ask for a reading to settle it |
| `context` | the worker's own window overflowed ("context length exceeded", "prompt is too long") | not a usage limit at all. No platform is parked and no reset is waited for: the ticket is too big for one worker context, so split it or re-dispatch on a bigger window |

The last two exist because they are opposite problems that read alike. Parking a healthy
platform on a worker's own context overflow leaves the platform idle and the ticket waiting on
a reset that was never going to help.

Common to all: exhaustion **parks**, it never prints a percentage. Everything below `confirmed`
is `INFERRED/low` and may not schedule a wake by itself. Detection patterns are per-platform
profile data, not hardcoded strings, so a vendor changing its error text is a data edit.

## Estimates that outran their reading

A window's usage is one reading you gave plus arithmetic. The arithmetic is capped at 100% —
"105% of an allowance used" is not a fact about any allowance, it is the projection announcing
it has outrun its own reading — and the overshoot is reported as a question rather than a
number.

Routing follows from that: a platform is taken out of the pool when **your reading** says the
window is spent, or when a projection calibrated on three or more samples says so. A low- or
medium-confidence projection reading 0% left does **not** defund a platform; it keeps its slot
and raises a question. Stopping the swarm on a number nobody supplied is worse than one more
dispatch against a window that turns out to be tight.

When you see one of those questions on the board, ask the user and record the answer:
`usage record --platform <p> --window <w> --used 5%`.

---
*Influences: SwarmVault's existing claim, checkpoint, and adapter contracts.*
