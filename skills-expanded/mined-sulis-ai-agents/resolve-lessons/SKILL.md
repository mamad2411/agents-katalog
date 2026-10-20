---
name: resolve-lessons
description: "Proactively drains the lesson backlog — drafts, schedules, and ships a fix per actionable lesson, collision-aware, with a plan-then-approve gate."
---

# /sulis:resolve-lessons — drain the lesson backlog, safely

## Conclusion (lead with the answer)

`/sulis:resolve-lessons` turns the **open `lesson` backlog into shipped
fixes**, proactively. It reads the open lesson issues, drafts a change
per actionable one, **schedules them so no two workers ever touch the
same file at once**, and ships each through the normal pipeline — spec →
tests → implement → **review gate** → merge → close the issue.

It is **plan-then-approve in v1**: it ALWAYS shows you the computed
schedule + the drafted spec for every lesson and **waits for your "go"**
before dispatching any worker. It never decides scope or ships code
behind your back.

It is structurally a **sibling of `/sulis:run-all`** — the same inline
dispatch loop, a different backlog (open lessons vs the WP INDEX) and a
different unit (a fix-change vs a WP).

## The load-bearing rule (MUST — same as run-all)

**Run the loop INLINE in this (the calling) session. Do NOT spawn an
orchestrator subagent.** The harness treats spawned subagents as leaves
of the agent tree, so an orchestrator-subagent could not itself spawn the
per-lesson executor subagents. YOU (the session that loaded this skill)
execute the loop directly and spawn one executor per scheduled lesson via
the Agent tool.

## Resolving tool paths (MUST — first action)

```bash
# Resolve from the ACTIVE plugin version (its bin/ is on PATH) — avoids the
# lexical-sort cache pick that mis-ranks 0.98.0 above 0.126.0 (#49).
SCRIPTS_DIR=""
_sulis_bin=$(printf '%s\n' "$PATH" | tr ':' '\n' | grep -E 'sulis-ai-agents/sulis/[^/]+/bin$' | head -1)
[ -n "$_sulis_bin" ] && [ -d "$(dirname "$_sulis_bin")/scripts" ] \
  && SCRIPTS_DIR="$(dirname "$_sulis_bin")/scripts"
# Dev fallback: marketplace repo cwd.
if [ -z "$SCRIPTS_DIR" ] && [ -f "plugins/sulis/scripts/sulis-issues" ]; then
  SCRIPTS_DIR="$(pwd)/plugins/sulis/scripts"
fi
# Last-resort: PORTABLE numeric (NOT lexical, NOT `sort -V`) cache pick.
[ -z "$SCRIPTS_DIR" ] && SCRIPTS_DIR=$(find ~/.claude/plugins/cache -name sulis-issues -type f \
  -path '*/sulis/*/scripts/*' 2>/dev/null \
  | sed -E 's#(.*/sulis/)([^/]+)(/scripts/.*)#\2 &#' \
  | sort -t. -k1,1n -k2,2n -k3,3n | tail -1 | cut -d' ' -f2- | xargs -I{} dirname {} 2>/dev/null)
[ -z "$SCRIPTS_DIR" ] && { echo "ERROR: cannot find sulis-issues" >&2; exit 1; }
```

The deterministic pieces are: `sulis-issues list` (the backlog read),
`_collision_schedule.schedule_collision_waves` (the scheduler),
`_change_context._locate_code_areas` (file-touch prediction). Invoke the
Python helpers via `python3 -c` with `sys.path` pointed at `$SCRIPTS_DIR`.

## The loop

### Step 1 — Read the backlog

```bash
python3 "$SCRIPTS_DIR/sulis-issues" list --descriptor lesson \
  [--repo OWNER/REPO]
```

Returns open lessons with `number`, `title`, `body`, `disposition`,
`labels`, `url`. If `degraded: true` (no `gh`), say so plainly and stop —
there's no backlog to drain.

### Step 2 — Triage into three buckets (MUST)

For each lesson, by disposition:

- **In-scope (mechanical)** — `disposition` is `task`, or `sea` **with a
  clear fix in the body** (the issue names the files + the change). These
  are auto-resolve candidates.
- **Defer (design-heavy)** — `disposition` is `sea` but the body poses a
  design question with competing approaches (e.g. "should we use SQLite
  vs the file store?"). v1 does NOT resolve these — flag for the founder
  to handle deliberately. (The agent-teams design-debate slot is a v2
  extension; do not invoke it here.)
- **Defer (unknown disposition)** — `disposition` is `""` (no parseable
  footer). Never auto-run; flag for founder triage.

Judging "clear fix vs design question" is a reading task: a lesson with a
"Suggested fix" section naming files + a concrete change is mechanical; a
lesson asking "which approach?" is design-heavy.

### Step 3 — Predict file-touch per in-scope lesson

For each in-scope lesson, predict the files its fix will touch from the
backticked tokens in the issue body:

```bash
python3 -c "
import sys; sys.path.insert(0, '$SCRIPTS_DIR')
from _change_context import _locate_code_areas
from pathlib import Path
print('\n'.join(_locate_code_areas(open('/tmp/lesson-NNN-body.txt').read(),
                                   Path('<repo-root>'))))
"
```

Treat the result as a **lower bound** — a lesson may touch files it
didn't name. That's fine: if a worker's actual diff collides anyway,
branch-ci / the merge surfaces it (fail-safe), and that lesson re-queues.

### Step 4 — Schedule collision-free waves

```bash
python3 -c "
import sys; sys.path.insert(0, '$SCRIPTS_DIR')
from _collision_schedule import schedule_collision_waves
import json
item_files = json.load(open('/tmp/lesson-files.json'))  # {num: [files]}
item_files = {k: set(v) for k, v in item_files.items()}
print(json.dumps(schedule_collision_waves(item_files, max_parallel=3)))
"
```

Each wave is a list of lesson numbers that can run **in parallel** (no
shared files). Lessons that share a file land in **different** waves
(serialised, oldest-first).

### Step 5 — PLAN-THEN-APPROVE (MUST — the v1 gate)

Present the plan and **wait for the founder's explicit "go"**. Use the
AAF-06 three-list shape — never "I found N, shall I do them?":

> *Lesson backlog plan:*
>
> *Will resolve (N): #53 (git-stash audit), #52 (CI pre-flight), …*
> *Deferred — design-heavy, your call (M): #30 (SQLite store) …*
> *Skipped — unknown disposition (K): #99 …*
>
> *Schedule (collision-aware):*
> *  Wave 1 (parallel): #53, <other disjoint>*
> *  Wave 2: #52  (serialised after #53 — both touch the git-workflow standard)*
>
> *Drafted spec for each — [show the per-lesson one-paragraph spec].*
>
> *Go?*

Do NOT dispatch anything until the founder confirms. If they trim the
list ("skip #52 for now"), re-schedule and re-present.

### Step 6 — Dispatch, wave by wave (on "go")

For each wave, for each lesson in it (parallel within a wave):

1. `sulis-change start --slug <lesson-slug> --primitive <fix|...> --intent
   "<from the issue body>"` — opens the change branch + worktree.
2. Write `.changes/{slug}.SPEC.md` from the issue body (the drafted spec).
3. Spawn the executor (Agent tool) to implement it through Steps 1-7
   (RGB → commit → push).
4. Drive Steps 8+: branch-ci, **the step-4.5 `/sulis:review` gate**,
   squash-merge **only on green CI + PASS review**.
5. PR body carries `Closes #<lesson-number>` so the merge closes the
   issue (#34 trailer rule — one keyword per issue).
6. `sulis-change mark-shipped`.

**Between waves**, rebase any remaining change branches onto the latest
`main` (the trunk) so later lessons build off the latest.

### Step 7 — Batch-report (AAF-06)

> *Resolved (N): #53 → shipped (PR #…, issue closed), …*
> *Paused on review (P): #… — CRITICAL finding: [plain English]*
> *Deferred (M+K): #30, #99 — [why]*

## Guardrails (MUST — never bypass)

1. **The step-4.5 review gate stays.** A CRITICAL finding pauses that
   lesson and surfaces it; never auto-merge past it. (It caught a real
   silent-fail-open this session.)
2. **Founder disposition gates scope.** The plan-then-approve step (5) is
   mandatory in v1. Never auto-decide which lessons are in scope.
3. **Collision-aware, never naive-parallel.** Only dispatch a wave the
   scheduler produced. Two in-flight workers never touch the same
   predicted file.
4. **Supervised in v1.** Report per lesson; the founder watches. There is
   no fully-autonomous mode in v1 (that's a later, separate opt-in).
5. **No `git stash` in change worktrees** (lesson #53) — the stash stack
   is shared per-repo; park transient state as a WIP commit instead.

## Gotchas

- **Don't run as a subagent.** This loop must run inline (the run-all
  constraint). If you find yourself spawned as `Agent(resolve-lessons)`,
  you can't dispatch executors — surface that and have the calling
  session run it instead.
- **Prediction is a lower bound, not a guarantee.** The collision
  schedule is computed from backticked tokens in issue bodies; treat a
  real merge conflict as the fail-safe and re-queue the lesson.
- **Empty / degraded backlog is normal** — say so plainly, don't
  manufacture work.
- **Design-heavy SEA lessons are NOT in v1 scope.** Defer them; do not
  route to an agent-teams debate (v2).
- **Unknown-disposition lessons defer to founder triage** — never
  auto-run a lesson whose disposition you couldn't parse.

## When to invoke

- The founder wants to clear the lesson backlog ("resolve the open
  lessons", "drain the backlog", "work through what we've captured").
- After a `/sulis:capture-lessons` run has filed a batch of actionable
  lessons.

## When NOT to invoke

- A single specific lesson the founder wants fixed now — that's a normal
  `/sulis:change start` (the orchestrator is for *batches*; n=1 has
  nothing to schedule).
- Design-heavy lessons needing a decision first — those want a
  deliberate design pass, not the resolution loop.
- An empty backlog — nothing to do.

## See also

- `../run-all/SKILL.md` — the inline-loop template this mirrors
- `../../scripts/sulis-issues` — `list` (backlog read) + `capture`
- `../../scripts/_collision_schedule.py` — `schedule_collision_waves`
- `../../scripts/_change_context.py` — `_locate_code_areas` (prediction)
- `../review/SKILL.md` — the step-4.5 gate; `../change/SKILL.md` — the
  per-lesson ship flow
- `.changes/create-resolve-lessons.SPEC.md` — the full design + locked
  decisions
