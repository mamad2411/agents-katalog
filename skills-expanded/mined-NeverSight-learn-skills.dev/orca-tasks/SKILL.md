---
name: orca-tasks
description: >-
  Turn an approved plan (docs/agents/plan.md) into an Orca Run and its Tasks with
  dependency edges, plus the tracker issue mirrors (github or linear). Creates the
  orchestration namespace only — never launches a worker. Orchestrator sessions only.
  Invoke with /orca-tasks.
disable-model-invocation: true
argument-hint: "Path to the plan doc?"
---

# Cut an approved plan into Orca tasks

Materialize an approved plan into the Orca orchestration namespace: one Run, one Task per plan
task, dependency edges preserved. This is the middle step of the pipeline (`/orca-setup` →
`/orca-plan` → `/orca-tasks` → `/orca-orchestrate`). It creates state only — no worker is
launched here; the Run and its Tasks are the source of truth the orchestrator drives next.

## Gates

- `docs/agents/setup.md` must exist (else route to `/orca-setup`).
- `docs/agents/plan.md` must exist **and** be approved (`Status: approved`). Refuse otherwise —
  never cut tasks from a draft plan.

## Load the guides before any command

```text
orca skills get orchestration
orca skills get orca-cli
```

Read them before running anything. Prefer `--json`. Never guess subcommands or flags from
memory.

## Steps

1. Read `docs/agents/plan.md`; verify the approval. Confirm the objective and the task list with
   the user in one line before creating anything.
2. Create the Run:
   ```bash
   orca orchestration run-create --objective "<plan objective>" --json
   ```
   Record the returned `run.id`.
3. Create one Task per plan task, 1:1, in dependency-safe order (tasks whose blockers exist
   first). Carry the plan id into the spec so `/orca-orchestrate` and the worker can reconcile:
   ```bash
   orca orchestration task-create --spec "<plan task id>: <spec>" --json
   # with dependency edges, referencing the created task ids:
   orca orchestration task-create --spec "<plan task id>: <spec>" --deps '<["<blocker_task_id>", ...]>' --json
   ```
   Keep `--deps` to the plan's `blocked-by` edges verbatim. Chains should stay ≤ 3-4 steps (the
   plan promised this).
4. Verify the graph: `orca orchestration task-list --run <run_id> --json` — every task exists,
   every dependency edge references a real task, and there are no cycles.
5. Issue mirror (required by the tracker choice — there is no markdown tracker): read the
   tracker from `docs/agents/setup.md` (the `## Issue tracker` section). Create one issue per
   task with the plan id in the title and blocking links mirroring the edges:
   - **github** → `gh issue create --title "<plan id>: <title>" --body "<spec>"`. Dependency
     edges are carried by the **Orca DAG (`--deps`) as the single source of truth**; the issue
     mirror documents them in the body — after all issues exist, append `Blocked by: #<num>` /
     `Blocks: #<num>` lines using the captured issue numbers. Optionally add real blocking links
     via `--depends-on` **only when the installed `gh` supports it** — runtime-detect support;
     do not assume it (on this project's toolchain `gh issue create` has no `--depends-on` flag
     and the REST dependencies endpoint 404s, so the body documentation + Orca DAG is the
     fallback that must always work). Note: `gh issue create` has **no `--json` flag** — it
     prints the new issue URL to stdout; capture the issue number from that URL. Then link the
     task worktree:
     `orca worktree set --worktree <task_worktree_selector> --issue <num> --json`.
   - **linear** → native
     `orca linear create --title "<plan id>: <title>" --body-file <spec-file> --team <key> --workspace <id> --json`
     (workspace + team from the setup marker), mirror dependency edges with
     `orca linear relation add --related <issue> --type blocks`, then link the task worktree:
     `orca worktree set --worktree <task_worktree_selector> --linear-issue <issue_key> --json`.
   The worktree link is what surfaces the task in Orca's Tasks tab under the chosen tracker.
   The two trackers are exclusive: mirror to the tracker recorded in setup, never both. With a
   `linear` tracker, no GitHub issue is created (and vice versa) — the setup chose one.
   A tracker whose CLI is missing or unauthenticated must be surfaced to the user, not silently
   skipped — the setup promised that tracker.
6. Report the Run id and task ids to the user. Point the card at the plan:
   `orca worktree set --worktree <primary-selector> --comment "tasks cut from docs/agents/plan.md"`.

## Done when

- The Run exists and every plan task is an Orca Task with its `blocked-by` edges as `--deps`.
- `task-list --run` shows the same graph as the plan; the user has the run + task ids.
- No worker has been started. Launching them is `/orca-orchestrate`'s job.
