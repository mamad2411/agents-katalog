---
name: todo-execute
description: >-
  Use when the user invokes /todo-execute, says "execute this project", "work through
  tasks", or names a hub project and wants work done, including concurrently with
  phrases such as "execute these tasks in parallel", "work multiple features of the
  same repo at once", or "fan this out with worktrees". Sequential by default; parallel
  mode fans file-disjoint tasks out to worktree agents.
---

# Project Execution Skill

You execute planned projects stored in a hub repo.

Two modes, one skill:

- **Sequential (default)** — work `tasks.md` top to bottom yourself, inline. Steps 1–7 below.
- **Parallel** — fan file-disjoint task groups out to agents in git worktrees, land PRs via a serial merge queue. See [Parallel mode](#parallel-mode) at the end; it reuses steps 1–2 for orientation, then follows its own steps P1–P7.

This involves real judgment and code work. Run it inline on the current session model;
use at least the **balanced** tier from [`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md).

## Hub location

The hub repo root is `$TODO_HUB` — an environment variable pointing at your hub folder (default `~/todo`). Resolve **every** path against this absolute root — active `index.md`, cold `archive.md`, and each project's files — regardless of the current working directory. This skill may be invoked from another repo; never assume cwd is the hub. (Same convention as `todo-refer`.)

## How the user invokes this

```
/todo-execute queue-migration
/todo-execute projects/work/queue-migration   ← full path also works
/todo-execute queue-migration parallel        ← parallel mode
/todo-execute queue-migration parallel tasks 3,5,7   ← parallel, explicit task subset
```

## Step 1 — Resolve the project path

Resolve the short-name in `$TODO_HUB/index.md` first, then `$TODO_HUB/archive.md` only
on an exact active miss.

- Short name → get the full `path`, status, owning registry, and section
- Duplicate across registries → stop; do not choose one
- Not found in either registry → tell the user and stop
- Full path passed directly → use as-is

Check the project status:
- `ready` or `in-progress` → proceed
- `planning` → warn the user that plan.md/tasks.md may be empty, ask if they want to continue anyway
- archived `done` → invocation is intent to resume execution; say that you will reopen it,
  then apply Step 3 atomically before doing work

## Step 1.5 — Enforce the project-graph gate

Before loading full project context, run the bounded graph query:

```bash
python3 <todo-graph-skill-dir>/scripts/graph-report.py context \
  "$TODO_HUB" "<short-name>"
```

- Any unsatisfied `depends-on` edge → stop before changing status or creating a worktree.
  Name the exact blockers and point at `/todo-graph why <short-name>`.
- An identity, edge, or cycle issue incident to this project → stop and point at
  `/todo-graph audit`; graph corruption makes execution order untrustworthy.
- An `in-progress` project whose dependency regressed is **at risk**. Do not silently
  demote it or continue.
- `related-to`, `supersedes`, and legacy registry `related` hints never block.

If the graph helper is unavailable, say so and stop rather than guessing dependencies
from prose. This cheap gate exists to avoid loading and executing a blocked project.

## Step 2 — Orient yourself

Read these files in order:
1. `plan.md` — goal, context, constraints, scope, and the repo path
2. `tasks.md` — full scope of work before touching anything
3. `research/findings.md` if it exists — prior research already done
4. `research/superpowers-docs.md` if it exists, then `<repo>/docs/superpowers/plans/` and
   `<repo>/docs/superpowers/specs/` in the target repo — superpowers skills (brainstorming,
   writing-plans) drop design docs there during target-repo sessions. List them; read the
   ones relevant to this project's tasks. Any relevant doc not yet listed in
   `research/superpowers-docs.md` → add a pointer bullet now (absolute path + one-line
   summary).

Do not start executing until you've read all of them. If `plan.md` is missing critical info (goal unclear, no repo path, no context), state exactly what's missing and stop — suggest running `/todo-plan <name>` first.

**Parallel mode branches off here** — jump to [Parallel mode](#parallel-mode).

## Step 3 — Activate the project and update status

If the row came from `archive.md`, move it verbatim back to the same section in
`index.md`. Set status to `in-progress` there and apply `todo-state` § Date stamping in
the same atomic edit: clear `completed` / `elapsed (days)`, preserve the original
`started`, and never leave a non-done row in `archive.md`.

For an already-active row, set status to `in-progress`. If the prior status was `ready`
or `planning`, stamp/overwrite `started` = today; otherwise preserve it.

## Step 4 — Isolate target-repo work in a worktree

Before editing any **target-repo** code, give this run its own git worktree, so a
concurrent session (another `/todo-execute`, another chat) sharing the same repo can't
overwrite your working tree — the usual cause of "my changes vanished."

- Scope: this applies **only** to code in the target repo (the `path`/repo named in
  `plan.md`). Hub files under `$TODO_HUB` — `artifacts/`, `tasks.md`, `index.md`,
  `research/` — are ALWAYS edited in the hub, never in the worktree.
- If the project produces only hub artifacts (analysis, docs) and touches no target-repo
  code, skip this step and note that you did.
- Create it off the base branch, named from the project short-name:
  ```
  git -C <repo> fetch origin
  git -C <repo> worktree add <repo>-wt/<short-name> -b todo/<short-name> origin/<base>
  ```
  `<base>` is the repo's default branch (usually main, occasionally master — confirm with
  `git -C <repo> symbolic-ref refs/remotes/origin/HEAD`). All target-repo code, builds,
  tests, and preview for this run happen inside `<repo>-wt/<short-name>`.
- Resumed run: if that worktree/branch already exists, reuse it — don't recreate.
- Do NOT push or merge here. Shipping is a separate, deliberate `/todo-push` the user runs
  when ready (see Step 7) — never auto-ship from this skill.

## Step 5 — Execute tasks top to bottom

Work through `tasks.md` one task at a time, running this **per-task loop for every
task, no exceptions** — it is what keeps execution quality independent of the model
running it:

1. **Define done first**: read the task line + the plan.md section it belongs to, and
   state in one line what evidence will prove THIS task is done (a passing test, a file
   existing, an output matching). If you can't state it, the task is ambiguous → Step 6.
2. **Do the work.**
3. **Verify with evidence**: run the proof you named in 1 and look at the output. Code
   → run the test/build. Doc/artifact → open it and check it answers the task. No
   runnable proof and no observable output → it is NOT done; treat as blocked.
4. **Only now tick the checkbox.** Ticking before step 3 is the failure mode this loop
   exists to prevent — a checked box is a claim, and claims need evidence first.
5. **One-line record** of what changed and where (worktree file, artifacts path).

Never batch steps 2–4 across multiple tasks. Rules of the road:

- **Front-load installed process skills per task** — this skill organizes the work;
  the craft comes from skills the user already has. A code feature/bugfix task →
  invoke `superpowers:test-driven-development` if installed; a task that hits
  unexpected failures or a bug with unknown cause → `superpowers:systematic-debugging`
  before proposing fixes (the per-task evidence loop above is
  verification-before-completion applied per task — if that skill is installed, its
  discipline governs step 3). Only invoke skills present in the session's listing —
  never invent one; if none fits, the loop above is the complete fallback.
- Complete each task fully before moving to the next
- Target-repo code changes go in the Step 4 worktree; hub outputs (docs, analysis,
  scripts) go to `artifacts/`
- **Follow the artifact conventions** (hub AGENTS.md → "Artifact conventions"): name a
  dated output `YYYY-MM-DD-<kind>-<slug>.md` (`kind` ∈ analysis/finding/handoff/session/design),
  open it with the backlink header blockquote (`> **Kind:** … · **Source:** tasks.md#R7 · **Date:** … · **Index:** [README.md](README.md)`),
  and add a row to `artifacts/README.md` — create that manifest from
  `$TODO_HUB/templates/artifacts-README.md` if it doesn't exist yet. Living docs
  (`journal.md`, `blockers.md`) keep their stable names.
- Keep artifacts self-contained — another agent session should be able to read them cold
- Drop research notes or discoveries in `research/` if relevant
- **Superpowers docs get a hub pointer immediately**: whenever a superpowers skill
  (brainstorming → `docs/superpowers/specs/`, writing-plans → `docs/superpowers/plans/`)
  writes a doc into the target repo, add a row to the table in the project's
  `research/superpowers-docs.md` in the same task — doc path + source + one-line summary.
  A plan/spec that exists only in the target repo is invisible to the hub; the hub's
  Stop hook flags unreferenced docs, but record the pointer yourself, don't rely on it
- When plan.md doesn't answer a question, that IS the answer — record the ambiguity
  (Step 6), don't improvise a decision the plan never made

After completing each task, check it off in `tasks.md`:
```
- [x] Task name
```

When checking off, **don't append findings or prose to the task line** — a task stays
one line. Discoveries go to `research/`, outcomes to `artifacts/`, with at most a short
pointer suffix (`— see research/findings.md § X`). `tasks.md` is read whole by several
skills; keeping it a bare checklist is what keeps every other skill cheap.

## Step 6 — Handle blockers

If a task requires external access you don't have (credentials, running services, live APIs):
- Document the blocker in `artifacts/blockers.md` with enough detail to unblock later
- Skip to the next task
- Never silently skip

If a task is ambiguous and `plan.md` doesn't resolve it:
- State the ambiguity clearly
- Ask the user before proceeding

## Step 7 — Report when done

Re-run the Step 1.5 graph context immediately before any status flip to `done`.
Dependencies can regress during a long execution session; a newly unsatisfied hard edge
keeps the project `in-progress` and is reported as at risk.

Update the active `index.md` row:

- Blockers remain or tasks are open → stay `in-progress`.
- All tasks complete and `plan.md` has a `## Verification` block → stay `in-progress` and point the user at `/todo-verify <short-name>` — the verification run is the gate that flips `done`, not your own assessment. Code-complete + unit tests ≠ done.
- All tasks complete, no `## Verification` block, **but the Step 4 worktree has unmerged changes** → stay `in-progress`; the work isn't landed until it's shipped. Point the user at `/todo-push` (run from `<repo>-wt/<short-name>`).
- All tasks complete, no `## Verification` block, and nothing to ship (hub-only project) → set `done`, and stamp `completed` = today plus `elapsed (days)` = `completed − started` (`todo-state` § Date stamping).

Summarize:
- What was completed
- The worktree path + branch (`todo/<short-name>`) if one was created, and that shipping is a separate `/todo-push` run — left separate on purpose
- What's in `artifacts/` and what each file contains
- Any blockers in `artifacts/blockers.md`

Keep it short. The artifacts speak for themselves.

**Session handoff:** a command named in this report is an *act-now* pointer for the
current session. When the remaining work is for a later session, recommend
`/todo-refer <short-name> resume` instead — it re-orients on current tasks/revisions/git
state and routes to the right work command itself.

---

# Parallel mode

You fan a hub project's independent tasks out to parallel agents, each in its own
git worktree of the target repo, and land the results on main through a serial
merge queue. You are the orchestrator: agents build and open PRs; only you merge,
only you touch hub files.

Entry: steps 1–2 above (resolve + orient), plus: `plan.md` must name the target repo
path; verify it exists locally and `gh auth status` succeeds there — stop and report if
not. Set the active row's status to `in-progress`, applying the same Step 3 date rule
above.

## Step P1 — Partition tasks into features

Group the unchecked tasks into **file-disjoint features**: tasks that touch the same
files, or depend on each other's output, go in the SAME feature (they run sequentially
inside one agent). Judge overlap from plan.md scope notes and a quick read of the repo.

- 1 feature after grouping → parallelism buys nothing; say so and run the sequential
  mode (steps 3–7) instead.
- State the grouping (feature → task lines) before spawning so it's on record.

**Gate A — before spawning (every box checked, literally, or don't spawn):**

- [ ] For each feature, the expected file/dir set is WRITTEN OUT (from plan.md scope +
  a grep of the repo), and every pairwise intersection between features is empty. Two
  features sharing even one file → merge them into one feature now.
- [ ] Every agent prompt contains all four slots from step P3 (intent verbatim,
  workspace commands, implement instruction, return contract) — reread each prompt and
  point at the four slots before sending.
- [ ] `gh auth status` succeeded in the target repo THIS session (output seen, not
  assumed).

## Step P2 — Inherit the session model

Parallel mode does not override models for either wave. Implement and review agents run
on the inherited session model. The `todo-push` sub-step uses its own **fast**-tier
routing; do not override it.

## Step P3 — Implement wave (one agent per feature, all in one message, in parallel)

Start one background implementation subagent per feature on the inherited session model;
do not request a model override. Each prompt is self-contained — subagents may start
with zero history.
Every prompt MUST contain these slots:

1. **Intent** — plan.md `## Goal` + relevant context/constraints, and the exact task
   lines this feature covers, verbatim. This grounds the code review later.
2. **Workspace** — create an isolated worktree of the TARGET repo (never the hub):
   ```
   git -C <repo> fetch origin
   git -C <repo> worktree add <repo>-wt/<feat> -b feat/<name> origin/<base>
   cd <repo>-wt/<feat>   ← all work happens here
   ```
   Then install dependencies the way the repo does (check its AGENTS.md, CLAUDE.md,
   README, and build files).
3. **Implement** the feature's tasks, with unit tests, committed in the worktree.
   Tell the agent to use installed process skills for the craft
   (`superpowers:test-driven-development` for the code, `systematic-debugging` on
   unexpected failures) when they appear in its session listing.
4. **Return contract** — branch name, worktree path, files added/changed, blockers.
   Implement agents NEVER edit hub files, NEVER open PRs, NEVER merge — review and
   shipping belong to step P4.

Agents that hit an external blocker (creds, live services) report it in their return
and stop that feature — same rule as sequential Step 6, but the blocker lands in
`artifacts/blockers.md` via YOU, not the agent.

## Step P4 — Review wave (no model pin — inherited session model)

The moment a feature's implement agent returns, spawn its review agent — pipeline,
don't wait for the other features. Spawn review subagents yourself on the inherited
session model without a model override, same as the implement wave. Review prompt
slots:

1. **Intent** — the same intent block from step P3, verbatim.
2. **Workspace** — `cd <repo>-wt/<feat>` (the existing worktree; create nothing).
3. **Review** — invoke the `code-review` skill at **high** effort on the worktree
   diff, with the intent restated. Apply the fixes.
4. **Coverage gate** — for every file the diff ADDS: find all its call sites
   (grep the repo for imports/usages of its exported symbols), then run the repo's
   coverage tooling scoped to the added files and those call-site files. Require 100%
   line coverage on all of them; write unit tests and re-run until green. Report the
   final coverage numbers — never claim the gate passed without the run output.
5. **Ship to PR only** — invoke the `todo-push` skill with the instruction: "You are in a
   linked worktree. Stop at the PR — do not merge; the orchestrator owns the merge
   queue." (todo-push's worktree mode handles the rest.)
6. **Return contract** — PR URL, branch name, worktree path, review findings applied,
   coverage output, blockers. Review agents NEVER edit hub files and NEVER merge.

## Step P5 — Serial merge queue

Parallel until PR; **serial at merge**. When agents return, merge PRs one at a time:

```
git -C <repo>-wt/<feat> fetch origin
git -C <repo>-wt/<feat> rebase origin/<base>      ← replay on latest main
git -C <repo>-wt/<feat> push --force-with-lease
gh pr merge <url> --merge                          ← never --delete-branch here
```

- Rebase conflict → resolve it in that worktree if the resolution is mechanical;
  otherwise skip the PR, finish the queue, and open a Revisions entry in tasks.md.
- Never merge two PRs concurrently, and never merge before its rebase + push.

**Gate B — before EACH merge (re-run per PR, not once for the queue):**

- [ ] The previous PR in the queue is confirmed merged (`gh pr view <prev> --json state`
  shows `MERGED` — output seen).
- [ ] This PR's branch was rebased onto latest `origin/<base>` in THIS queue round —
  a rebase from before the previous merge doesn't count; redo it.
- [ ] Tests/CI are green on the post-rebase commit, with the run output in hand. No
  output → run them now; red → this PR skips the queue and gets a Revisions entry.

## Step P6 — Cleanup

From the PRIMARY repo copy (first path in `git worktree list`), for each feature:

```
git -C <repo> worktree remove <repo>-wt/<feat>
git -C <repo> branch -d feat/<name>
git -C <repo> worktree prune
git -C <repo> pull --ff-only        ← once, if primary sits on <base> and is clean
```

## Step P7 — Reconcile hub state and report

Only now, and only you: tick the completed task lines in `tasks.md`, write blockers to
`artifacts/blockers.md`, and set the active registry status per sequential Step 7 (a
`## Verification` block in plan.md means stay `in-progress` and point at
`/todo-verify` — merged PRs + unit tests ≠ done).

Report per feature: PR link, merge result, coverage numbers, blockers. Keep it short.
The sequential Step 7 session-handoff rule applies here too: work left for a later
session gets `/todo-refer <short-name> resume`, not a direct work command.

## Parallel-mode rules

- Parallel until PR, serial at merge — no exceptions, races corrupt main.
- Review always runs as a separate agent from implementation, but neither wave pins
  a model — both inherit the session model.
- Agents never write hub files; the orchestrator is the only hub writer.
- A feature = file-disjoint task group; overlapping tasks share one agent.
- Worktrees are of the target repo. Do not use host-managed isolation that creates a
  worktree for the current repo, which is usually the hub. Subagents run the explicit
  `git worktree add` command inside the target repo.
