---
name: sable-execute
description: |
  Flip SABLE into EXECUTION mode — drain the bead pool. Writes the
  mode-state file via `sable-mode set execution`, then stands up the manager
  fleet on demand: `sable-spawn-manager --all` opens optimus, tarzan, and
  chuck as warm claude panes in their own hidden windows and kicks their
  operating loops (the session itself is Lincoln-only until now —
  sable-launch is mode-neutral). Managers spawn a worker pane per bead;
  workers self-push their worktree branches; Chuck merges. In execution mode
  the interlock hook blocks spawning planning-only producers — you are
  draining the pool, not filling it.
  Use when asked to "/sable-execute", "enter execution mode", "start executing", or
  "drain the backlog".
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# /sable-execute — enter EXECUTION mode

You are **Lincoln**, the orchestrator main session (see `roles/lincoln.md`). This skill
flips you into **execution mode**, whose single job is to **drain the bead
pool**.

## 0. Require the approved handoff (hard gate)

Planning's final human gate records a tier-appropriate receipt in the atomic mode
state:

- **Quick** binds the one consolidated approval to its explicit 1–3 beads.
- **Full** binds final decomposition approval to all five dossier artifacts, the
  epic's live children, fresh `bd swarm validate --json`, and a ready front.
- **Both** prove zero unresolved `open-question` beads across open, in-progress,
  blocked, and deferred states, and bind the current integration-base SHA.

Do not reproduce these checks manually. The mode transition below revalidates
the receipt and carries it into execution under the same state lock. If evidence
changed after approval, it refuses without altering planning state; return to
`/sable-plan`, resolve the drift, and ask for the single final approval again.

## 0.5 Docker Supabase preflight (hard gate, SABLE-n5rb)

Before any lane touches Docker Supabase, run:

```bash
sable-docker-preflight
```

This detects the dockerd/containerd ghost-container desync class that
corrupted a shared pgdata volume after the 2026-07-07 WSL hard reboot
(forensics + recovery runbook: market-brief-package-9scm) — containerd can
revive pre-crash containers as tasks dockerd no longer tracks while dockerd
separately starts its own visible generation, and both postgres processes end
up writing the SAME volume. This recurs on every hard reboot/freeze, so it
must be caught here, before `sable-spawn-manager --all` lets any worker near
the db.

- **Exit 0 — clean.** Proceed to step 1.
- **Nonzero because docker/Supabase isn't part of this project** (stderr/JSON
  errors say `docker not found` or `no supabase_db_* container found`) — not
  applicable here, proceed to step 1.
- **Any other nonzero — HARD STOP.** Do not flip the mode-state, do not spawn
  managers. Paste the diagnosis to the operator (which of phantom
  containers / ghost cgroup tasks / dual postmaster fired, and the specific
  IDs/timestamps reported) and point at the runbook the tool prints
  (market-brief-package-9scm). Wait for the operator to run recovery before
  retrying this step.

## 1. Flip the mode-state

Choose the provider map once for this execution session, then run exactly one
mode transition. It succeeds only from a fresh approved planning receipt. A
Claude-only install uses the backwards-compatible default:

```bash
sable-mode set execution --fleet optimus,tarzan,chuck
```

When both Claude and Codex are installed, record the operator's session choice
explicitly:

```bash
sable-mode set execution --fleet optimus,tarzan,chuck \
  --providers optimus=claude,tarzan=codex,chuck=claude,worker=codex
```

The three manager roles may use different providers, but `worker` is one
provider shared by every worker pane for the whole execution session. Missing
entries default to Claude. The map is immutable while execution mode is active:
do not switch providers per bead or per dispatch. To change it, stand down the
fleet and return to planning/clear the ended session before starting a new
execution session.

There is one explicit emergency bypass, owned by the human operator:

```bash
sable-mode set execution --break-glass \
  --reason "operator-provided reason" --fleet optimus,tarzan,chuck
```

Never choose this on the operator's behalf. It records the operator identity,
time, reason, base SHA, and failed readiness checks as `kind=break-glass`.
Generic hook force flags do not create execution authority.

For an approved receipt, its `scope` array is also the exact execution work
set. Quick scope is the explicit 1–3 approved beads; Full scope is the exact
child-ID snapshot approved at decomposition. New descendants and unrelated
ready work are not added implicitly: return to planning and record a new final
approval. Only a carried `kind=break-glass` receipt is unbounded, and
`sable-spawn-worker` announces that bypass on every dispatch.

This writes the **per-repo** mode-state file — `<repo>/.claude/sable/state/mode-state.json`
when inside a git repo (resolved from the git common-dir, so all of the repo's
worktrees share one mode), or `~/.claude/sable/state/mode-state.json` outside a
git repo. Because the mode lives in the repo, you can run a separate SABLE
session in **another** repo at the same time — e.g. plan project B while project
A executes — without the two clobbering each other's mode. From this point the
`mode-interlock.sh` hook is in execution posture: spawning planning-only
producers (sherlock / victor / columbo) is blocked on both the Agent and Bash
legs (soft — `SABLE_ORCHESTRATION_FORCE=1` / `--force` overrides). Mode flips are
mid-conversation; no restart.

## 1.5 Seed the active-contracts surface (SABLE-9ozz)

The mode flip alone is invisible to a manager pane that **restarts** mid-drain
(`/clear`, crash, session limit): the pane re-boots on its STATIC role card and
loses every conversation-state convention this fleet is running under — the
merge-gate sole-path contract, any interim worker cap, the manual-relay rule
while a hook is dark. That was the 2026-07-13 gah9 bypass: a restarted chuck
merged with bare `git merge --no-ff` because his static identity still described
the old manual flow. Persist the live contracts to disk so `session-role-anchor.sh`
surfaces them into every fresh boot's identity:

**Use `add` for every line — never `set`.** The surface ACCUMULATES across shifts:
most of what a booting pane needs was written by earlier shifts, not by this flip.
`set` REPLACES the whole surface, and this choreography used to lead with it —
on 2026-07-30 one flip destroyed 25 of 29 committed lines of operator doctrine,
including an entry marked BINDING ON EVERY INCOMING LINCOLN and the ruling naming
the run's integration branch. They survived only because this one file is
git-tracked (SABLE-ztks1), which is luck the mechanism must not depend on.
`sable-contract set` now REFUSES (exit 3) against a non-empty surface for exactly
this reason (SABLE-wx048); `set --force` is the deliberate reset.

```bash
sable-contract add  "Merges go ONLY through sable-merge-gate. NO bare git merge/push on any integration branch."
sable-contract add  "Workers self-push their worktree branch; Chuck's PRIMARY handoff is a direct tmux message; a durable for-chuck bead is created only if delivery fails, so its absence is healthy; Chuck merges via the gate."
# add any interim fleet rule live this shift, e.g.:
# sable-contract add "Interim worker cap: 2 per manager until SABLE-p8rf lands."
```

Adding a line that already says the same thing is cheap and safe; erasing one that
a previous shift is relying on is not — so when in doubt, `add`.

`sable-contract` writes `<repo>/.claude/sable/state/active-contracts.md`, colocated
with the mode-state (same per-repo resolution). Update it the moment a protocol
flips — a contract change that lives only in this conversation dies with the next
restart. Retire a single rule with `sable-contract clear` (removes the surface) or
`sable-contract set --force` (deliberate full reset) — both destroy accumulated
history, so read the surface first and re-add what still applies.

## 2. Bring up the warm-pane session

Execution runs on the **tmux warm-pane topology** — the only execution topology
(see `TMUX-AGENTS-DESIGN.md`): every role is a real, persistent interactive
Claude or Codex session
in its own tmux pane with a provider-neutral identity (`SABLE_AGENT_NAME`),
in the role→pane registry (`@sable_role` pane option) that `sable-msg` and the
worker-spawn tooling resolve against.

Determine which of two states you are in:

- **You are the lincoln pane** of a running sable session (check:
  `SABLE_AGENT_NAME` is `lincoln` and `$TMUX` is set (legacy Claude sessions
  also carry `CLAUDE_AGENT_NAME`);
  `tmux display-message -p '#{@sable_role}'` prints `lincoln`). This is the
  normal case — `sable-launch` creates a Lincoln-only session. **Stand up the
  fleet now**: run `sable-spawn-manager --all` — each manager (optimus,
  tarzan, chuck) opens as a persistent interactive Claude or Codex session in
  its OWN detached window
  (your window is not disturbed), launched with a bypass permission posture
  and kicked into its operating loop. Idempotent: already-running managers are
  skipped. The interlock allows this only in execution mode — which you just
  set in step 1. The spawn tool independently checks the carried handoff before
  any manager pane is created; a legacy or statusless execution file cannot
  start the fleet.
- **No sable session exists yet** (`tmux has-session -t sable` fails). Tell the
  operator to run `sable-launch` from a plain terminal (it wraps `sable-tmux`,
  creates the Lincoln-only session, and attaches — `tmux attach -t sable`),
  continue this conversation in the **lincoln pane**, then stand up the fleet
  as above.

How the drain works (all of it happens in the panes, not in your context):

- **Managers (optimus, tarzan)** read `sable-mode handoff show` and drain only
  ready IDs from that receipt's exact scope, partitioned by their normal
  parented/orphan lanes. They verify each bead and **dispatch their own workers**
  — one ephemeral worker pane per bead via the worker-spawn helper,
  which checks receipt scope and then owns the claim (worktree = pane CWD,
  model pinned from the bead's `model:` label, pre-dispatch governance runs
  inside the helper). Managers do not pre-claim normal dispatches. The helper
  mechanically rejects a lead or bundle member outside the receipt before any
  claim.
  Managers review results through the bead pool; they do **not** push worker
  code.
- **Workers** do TDD in their own worktree, pass the gates, **self-push** their
  own worktree branch from their pane CWD, close their bead with gate evidence,
  and flag `@sable_status=done`.
- **Chuck** is the merge-queue **pane**. A manager's push notifies him
  message-first (`sable-msg chuck`, sent by the post-push hook), with a durable
  `for-chuck` bead as the fallback when his pane is unreachable; he merges,
  replies, and idles. There is no second terminal to open.
- **Reap** finished worker panes with `sable-worker-status --reap`.
- **Peek** at any pane or hidden worker window with `sable-view` (status
  table), `sable-view <role>` (focus), or `sable-view <role> --tail` (read
  without switching).

## 3. Talk to the managers (sable-msg)

Lead↔manager conversation is low-volume, direct, and message-first:

```bash
sable-msg optimus "status?"                      # queued behind the current turn
sable-msg tarzan  "drop the auth epic, API is urgent now" --interrupt
```

`--interrupt` sends Escape first so the message lands mid-turn instead of
queueing. Every injected turn opens with the fixed header
`⟦SABLE-MSG⟧ from=<sender>` — the framing rule that lets every pane distinguish
agent traffic from the operator. Replies from managers arrive in your pane the
same way; treat any turn without that header as the human.

## 4. Oversee

- Give the operator scoped status: managers report over `sable-msg`; work state
  and worker results live in the bead pool (`bd show`, `bd list
  --status=in_progress`) — synthesize, don't enumerate.
- Broker arbitration: when a manager messages you with a conflict or a
  priority question, decide (or relay to the operator) and reply via
  `sable-msg`.
- You do **not** write application code, claim beads, dispatch workers, or
  push. The managers plan, dispatch, review; the workers build and self-push;
  Chuck merges. You keep the session coherent.

## 5. Hand back to planning

When the pool runs dry or needs regrooming, tell the operator to run `/sable-plan`.
Do not spawn producers yourself from execution mode — the interlock will block
it, and that is correct.
