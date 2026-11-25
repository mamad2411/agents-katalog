---
name: todo-verify
description: Use when the user invokes /todo-verify, says "verify this project", "did the e2e pass", "run the verification layer", or names a project and wants its verification result reconciled into the todo. Detection only — reads results, ticks tasks/flips status, opens Revisions on gaps; never edits code.
---

# Project Verify Skill

You are the **check** gate in the hub's `plan → do → check → revise` loop. `todo-execute`
*builds*; you *verify* — reading the project's result from its **verification MCP** (the
user's verification layer) and reconciling it into todo state. You **detect and record**;
you never edit code, never run repair. Failures and coverage gaps become structured
`## Revisions` entries that `todo-revise` then consumes and fixes.

Division of labor: **the verification MCP attests; you transcribe its verdict into
`tasks.md` plus the owning registry row.** The run is the hard gate that flips status;
coverage only emits Revisions.

This involves real judgment — driving the run, handling collisions, and interpreting the
result. Use the **balanced** tier at **high** effort from
[`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md). The final mechanical `tasks.md`/`index.md`
checkbox and status edits may be delegated to the **fast** tier exactly as
`todo-state` does. If the host cannot select a dispatch model, keep the work in
the current session.

## The verification MCP (pluggable)

This skill is **not tied to any specific test harness**. It assumes a verification MCP
server that exposes, in some form, this small contract:

- **start a run** against a named feature/target (returns a run id)
- **wait for / poll** until the run reaches a terminal verdict (`passed` / `failed`), and
  ideally streams progress rather than requiring a busy-poll
- **read the result** — which tests/specs passed, which failed
- **(optional) read coverage** — a gap list + a grounded coverage %

The tool names used below (`start_run`, `wait_for_result`, `get_result`, `get_coverage`)
are placeholders for that contract — map them to your server's actual tools. If a project
has no verification MCP, it simply omits the `## Verification` block in `plan.md` and this
skill is a no-op for it; the `plan → do → revise` loop still runs without the check gate.
See the README for how to point this at a concrete server.

## Hub location

The hub repo root is `$TODO_HUB` — an environment variable pointing at your hub folder
(default `~/todo`). Resolve **every** hub path against this root — active `index.md`,
cold `archive.md`, and each project's files — regardless of the current working directory.
This skill may be invoked from another repo; never assume cwd is the hub. Pass this root
to the edit sub-agent so it writes there, not into the cwd. (Same convention as `todo-refer`.)

## How the user invokes this

```
/todo-verify api-token-mgmt          ← drive the run + coverage, reconcile state
/todo-verify api-token-mgmt 7cvh     ← rerun an existing run by its id instead of a fresh run
/todo-verify                         ← ask which project, or act on context
```

Plain language counts too: "verify the token feature", "did the lifecycle spec pass",
"run the verification layer on this".

## Step 1 — Resolve the project

Resolve the short-name in `$TODO_HUB/index.md` first, then `$TODO_HUB/archive.md` only
on an exact active miss. Record the owning registry, section, full path, and status.

- Short name → look it up active-first; a duplicate across registries stops the run.
- Not found in either registry → tell the user and stop.
- Full path → use as-is.
- No project named and not obvious from context → ask which project before doing anything.

## Step 2 — Read the `## Verification` block

Extract the `## Verification` section from `plan.md` — **don't ingest the whole plan**
(hub plans can run large; the binding block is all this skill needs, plus the `## Goal`
line for the report):

```bash
awk '/^## Verification/{f=1} f&&/^## /&&!/^## Verification/{exit} f' plan.md
grep -m1 -A1 '^## Goal' plan.md
```

This is the binding to the verification MCP:

```markdown
## Verification
- **Feature:** api-token-mgmt
- **Run:** start_run (session reuse); rerun by run id
- **Gate covers:** Phase 5 tasks (e2e / integration / deploy-smoke)
- **Coverage source:** get_coverage(api-token-mgmt)                 # optional
- **Task↔test map:**                                                # optional
  - "Deploy + smoke-test full lifecycle" ⟶ spec: token-lifecycle.spec.ts
```

- **No `## Verification` block, or `Feature` unfilled** → stop and report:
  "<project> has no verification binding — add a `## Verification` block to plan.md
  (feature name + gate-covered tasks) before running /todo-verify." Do not guess a feature.
- Note the **`Gate covers`** set — the *only* tasks you may ever auto-tick. Anything outside
  it is never ticked by this skill.
- Note whether **`Coverage source`** is set (enables the coverage-gap → Revisions path).
- Read the **`Task↔test map`** if present — it sharpens which task ticks on which passing
  spec and which task a failure backlinks to. Absent → map coarsely (see Step 5).

## Step 3 — Drive the gate run (record-only)

Drive the verification MCP in **record-only** mode — you observe, you do not repair. If the
server has an auto-repair / "heal" mode, turn it OFF:

1. Start the run for the feature, reusing a stable session/conversation handle if the
   server supports it. For a rerun (a run id was passed, e.g. `7cvh`), start from that id.
2. If starting the run reports a **collision** (another run is using the same repo/app) →
   **ask the user** whether to run isolated (a per-run worktree, if the server offers it)
   or to queue behind the other run, then retry. Do not guess.
3. Wait for the terminal verdict using the server's wait/stream tool; if it returns a
   "still running" signal, call it again — loop until terminal (`passed` / `failed`).
   Prefer the wait/stream tool over busy-polling a status endpoint.
4. Pull the verdict from the result tool: which tests passed (ids / names) and which failed.

**Degradation rule (important):** if the app can't boot — no creds, blocked deploy,
health-check timeout — do **not** hard-fail. Set the run result to `blocked`, capture the
blocker reason verbatim, and continue to Step 4 (coverage-only). Report the blocker
prominently in Step 6.

## Step 4 — Read coverage (if `Coverage source` is set)

Call the coverage tool for the feature. Collect the gap list (e.g. `untested`,
`unverified`, `shallow-verified`, `path-incomplete`) plus the grounded coverage %. These
never flip status — they only become Revisions in Step 5.

If `Coverage source` is not set, skip this step.

## Step 5 — Reconcile and write back

Apply these rules. Mechanical `tasks.md` / registry edits may be delegated to a
fast-tier subagent (as `todo-state` does); the interpretation is yours.

Before any green result can flip the project to `done`, run:

```bash
python3 <todo-graph-skill-dir>/scripts/graph-report.py context \
  "$TODO_HUB" "<short-name>"
```

Passed tests may still tick their covered tasks, but an unsatisfied hard dependency or
incident graph identity/cycle issue keeps status `in-progress`. Report the exact graph
blocker and point at `/todo-graph why <short-name>` or `/todo-graph audit`. If the helper
is unavailable, do not cross the `done` gate. Context and lineage edges never gate.

| Verification result | tasks.md | owning registry status | Revisions |
|---|---|---|---|
| Run green, all gate-covered tasks pass | tick covered `[ ]`→`[x]` | → `done` **iff** every task in the project is `[x]`, else stays `in-progress` (a flip to `done` also stamps `completed` = today and `elapsed (days)` = `completed − started`, per `todo-state` § Date stamping — never overwrite an existing real `started`) | — |
| Run fails | no tick | stays `in-progress` | one entry per failing area, backlinked `⟵ Task N` |
| Coverage gap (even if run green) | no change | unchanged | one informational entry per gap (gap type named) |
| Run blocked (boot/creds) | no tick | unchanged | report blocker; coverage path still runs |
| No verification block | — | — | (handled in Step 2 — stop) |

**Mapping tasks ↔ tests:**
- With a `Task↔test map`: tick the mapped task only when its mapped spec/test passes;
  backlink a failure to the mapped task.
- Without a map (coarse fallback): an **all-green** run ticks the entire `Gate covers` set
  at once; a **partial** pass ticks nothing (you can't tell which task each test proves) —
  open a Revision noting which tests failed and that a `Task↔test map` would sharpen this.

**Revisions format** — reuse the exact `## Revisions` schema `todo-revise` consumes, so the
two skills interlock. Append to (or create) the `## Revisions` block at the bottom of
`tasks.md`, numbering `R<n>` continuing from any existing entries (never reuse a number):

```markdown
### R7 ⟵ Task 5.7 — beta deploy + lifecycle smoke        [open]
- Gap: token-lifecycle.spec.ts failed at the exchange step
- Expected: full lifecycle green (author → exchange → resolve-scoped → rotate → revoke)
- Actual: exchange returned 401 — run 7cvh, exchange step
- Fix: (leave for /todo-revise unless the cause is obvious)
- Source: verification run 7cvh / feature api-token-mgmt
- [ ] implement + re-verify
```

**Invariants:**
- Never tick a task outside `Gate covers`. Never edit code. Never run repair.
- The **run** is the only signal that flips `index.md` status; **coverage** never flips
  status, only emits Revisions.
- **Idempotent:** before appending a Revision, scan existing entries — if one already
  covers the same failing area/test, update it rather than adding a duplicate. Scan by
  extraction, not a full read: `grep -niA1 '^### R[0-9]\+[A-Za-z]*' tasks.md` gives every entry's
  heading + Gap line; read a specific entry's body by line range only if you need it.
  Likewise, find the `Gate covers` task lines to tick via `grep -n '\- \[ \]' tasks.md`
  filtered to the covered phase — hand the edit subagent the exact line text as
  its anchor, never the whole file.
- Leave `plan.md`, `research/`, `artifacts/` untouched — this skill edits `tasks.md`
  plus the owning registry row.
- If a failure or coverage gap opens a Revision for an archived project, atomically move
  its row back to the same section in `index.md`, set `in-progress`, and clear
  `completed` / `elapsed (days)` per `todo-state`. A passing re-verification that
  leaves an archived project `done` updates its `archive.md` row in place.

## Step 6 — Reconcile status honesty, then report

**Status honesty** (mirror `todo-state` / `todo-revise`): open Revisions on a
project marked `done` mean it isn't done. If archived, move the row back to `index.md`;
set `in-progress` and clear `completed` / `elapsed (days)` (Step 3.5). All tasks `[x]`
and no case-insensitive open Revisions, with a clean project-graph gate → offer `done`,
stamping `completed` = today and `elapsed (days)` when accepted.

**Report** status-first, terse:
- ✅ / ❌ / ⚠️ run verdict (or ⚠️ blocked + the blocker reason).
- Grounded coverage % and gap counts, if coverage ran.
- Exactly what was written: which tasks ticked, status before → after (plus any
  `started`/`completed`/`elapsed (days)` stamped or cleared), which `R<n>` Revisions opened.
- If Revisions were opened: "Run `/todo-revise <short-name>` to fix now — or
  `/todo-refer <short-name> resume` when picking this up in a later session." Direct work
  commands are act-now pointers; `/todo-refer … resume` is the entry point for deferred pickup.

## Notes
- This is the producer half of the Revisions loop; `todo-revise` is the consumer. Keep the
  schema identical so they interlock — same `### R<n> ⟵ Task N … [open]` + `- [ ]` shape.
- Record-only by design: you transcribe the verification MCP's verdict, you don't repair.
  If the server defaults to auto-repair, disabling it here is deliberate.
- Reconciled state feeds the infographic: the Stop hook (`infographic-staleness.sh`)
  regenerates `artifacts/infographic.html` after the tasks.md/index.md edits land.
- If a run keeps blocking on the same missing prerequisite (e.g. a deploy that never
  happened), say so plainly — that's a project blocker for `/todo-revise` or the user, not
  something verify can clear.
