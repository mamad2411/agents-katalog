---
name: ship-first
description: |
  Final task completion protocol: report → user-note → deploy → smoke test → close? → guide?
  → routing.db → propagate → STATUS → sessions. Invoked from fast-track and pipeline flows
  after task execution, not directly by the user.

  Use when: invoked after the execute step of a fast-track or pipeline task
---

# Ship-First Protocol

Final protocol after task execution. Receives context from the calling skill:

- `{task_id}` — slug or task id
- `{artifact_type}` — `fast-track` or `task`
- `{log_dir}` — path to the log folder
- `{task_file}` — path to the original task file
- `{project}`, `{project_path}` — from projects config
- `{title}` — task name (one line)
- `{date}` — current date
- `{arch_ref}` — arch-map result (string or null)
- `{block_num}` — current block number (per-block mode only)

## Input

Complete block or task execution context — the report artifacts from `plan-first`, block-num or "final" marker, `task_id`, `log_dir`, project metadata.

## Output

`report-*.md` + `user-note-*.md` per block; task-level aggregate `user-note.md`; `STATUS.md` in project root; `routing.db` row updated (status / arch_ref / closed_at); block or task marked done.

## Hands off to

`flow-first` for the next open block (per-block mode), or `— (terminal)` when all blocks are done.

---

## ship-first Modes

ship-first operates in **two modes**:

### Per-block mode

**Trigger:** `{block_num}` is in context. **Called by:** plan-first after block execute. **Does:** writes `report-N.M.md` + `user-note-N.M.md`, deploys the block, runs smoke test, closes the block in `task_blocks`, then moves to the next block or switches to task-level mode.

### Task-level mode

**Trigger:** `{block_num}` not passed or equals `'final'`. **Called by:** decomposition orchestrators after all blocks are closed, or per-block ship-first when it sees no open blocks. **Does:** artifact completeness check, ui-ai-first if needed, aggregate final user-note, "close?" question, guide?, arch-map, routing.db update, propagate arch_ref, parent chain check, STATUS + sessions.

### Mode determination

If `{block_num}` in context → per-block. Otherwise → task-level. Modes are mutually exclusive.

---

# Per-block mode

## Step B1 — Write report-N.M.md

Determine round `{R}`. Create `{log_dir}/report-{N.M}.{R}.md` with sections: What was done / What was notable / Next. Register in `task_artifacts` with `artifact_type='report'`.

## Step B2 — Write user-note-N.M.md

Same `{R}` as B1. Contents: What changed (1-3 lines from the user's perspective) + Where it affects. Purely technical block → `Nothing changes for the user.` Register with `artifact_type='user-note'`.

## Step B3 — Deploy block

Read block types from library-first artifact. For `ai-skill` type:

```bash
cd {skills_project_path} && git add .claude/ && git commit -m "block-{N.M}" && git push origin main
bash {skills_project_path}/.claude/shared/scripts/sync-agents.sh
```

For application code — additionally push in `{project_path}`. In any case sync tasks to the ops server. For sandbox projects — skip deploy. Remember `{last_commit_hash}` for Step B5.

## Step B4 — Smoke test by atom types

Get types via `SELECT atom_type FROM task_blocks WHERE task_id='{task_id}' AND block_num={NM}`. Where `{NM}` = `N*10+M`. If NULL — fallback: read library-first artifact.

| Type | What it does |
|---|---|
| `backend` | curl / command from plan, check status + response |
| `infra` | `nginx -t` / `systemctl status` / curl endpoint |
| `integration` | trigger webhook/API, check log |
| `ai-skill` | re-read changed SKILL.md, check logic for contradictions |
| `ui` / `manual` | skip — plan-first shows a UI test plan separately |

## Step B5 — Close block

First verify the block actually produced what its cadence required. On a runtime
with post-tool hooks this check can be automated; on one without them it is this
step, and skipping it closes a block whose artifacts were never written — silently,
because nothing else looks.

```bash
sqlite3 {routing_db} \
  "SELECT recommended_cadence,
          (SELECT group_concat(DISTINCT artifact_type) FROM task_artifacts
            WHERE task_id='{task_id}' AND block_num='{NM}') AS produced
     FROM task_blocks WHERE task_id='{task_id}' AND block_num={NM};"
```

`flow+lib+plan` expects `flow-first`, `library-first`, `plan-first` and `report`;
`lib+plan` expects the same without `flow-first`; `plan` expects `plan-first` and
`report`. A missing artifact means the chain was cut — say which one is absent and
stop, rather than closing the block.

```bash
sqlite3 {routing_db} \
  "UPDATE task_blocks SET status='done', commit_hash='{last_commit_hash}', closed_at='{date}'
   WHERE task_id='{task_id}' AND block_num={NM};"
```

Update the row in `## Blocks` in task.md: replace `⏳` with `✅` and `—` with `{last_commit_hash}`.

## Step B6 — Move to next block or task-level

Check for open blocks. Found → `$flow-first` with next block context. None → switch to task-level mode with `{block_num}` cleared.

---

# Task-level mode

## Step 0.5.0 — Hot-fix bypass

If all task blocks have `source='idea-first'` (hot-fix), the flow/library/plan/report/user-note artifacts were intentionally not created — skip Step 0.5. Otherwise execute standard Step 0.5.

## Step 0.5 — Check artifact completeness

For each block check for mandatory artifacts (`flow-first`, `library-first`, `plan-first`, `report`, `user-note`). All present → OK. Gaps → list them and ask "Restore? (go / skip)". On "go" — invoke the missing skill.

## Step 0.6 — Launch ui-ai-first (if needed)

Check `run_ui_ai_first` flag from session. `false` → skip. `true` → run full ui-ai-first protocol with `task_path={task_file}` and wait.

## Step 1.5 — Aggregate final user-note.md

From all block `user-note-NN.md` files, write `{log_dir}/user-note.md` with sections: What changed (by blocks) / Summary for the user / Where it affects. Purely technical refactor → `Nothing changes for the user.` Never skip creating the file. Register with `artifact_type='user-note-final'`.

## Step 4 — Close the task?

```
Close the task?
1. Close — everything accepted
2. More work — need to do more
```

If a prior step had "problems" — set status `open` immediately without asking.

## Step 4.5 — Create a guide?

**Only if** `artifact_type == fast-track` AND Step 4 answer was "1=close". Ask:

```
Create a full instruction for guides?
1. Create   2. Don't create
```

Answer "1" → invoke `/go-guide` with `mode='from-task'` and content_source = all block user-notes + final user-note.md + last report. The guide skill picks storage_mode automatically. Answer "2" → skip.

## Step 4.7 — arch-map (if arch_ref not passed)

`{arch_ref}` is null → automatically invoke `$arch-map`. Save result in `{arch_ref}` for Step 5. If unavailable → continue with null, not a blocker.

## Step 5 — Write to routing.db

Check if the record exists. UPDATE status / arch_ref / closed_at. Fallback INSERT if UPDATE affects no rows (task created before the go-fast Step 3 fix). Status: `done` if Step 4 answered "1", `open` otherwise.

After INSERT/UPDATE — write atoms from library-first: read `## Table`, for each row INSERT into `task_atoms`. Then aggregate counters (`cnt_ui`, `cnt_backend`, `cnt_integration`, `cnt_infra`, `cnt_ai_skill`, `cnt_manual`) via UPDATE on `artifacts`. Missing library-first → silently skip.

## Step 5.5 — Write-back linked improvement records (if any)

If task.md contains `linked_improv_artifact:` header → extract the linked slug. If task status = `done` → UPDATE the linked improvement rows and close the linked artifact. Otherwise skip — improvements stay open.

## Step 6 — Propagate arch_ref

If `arch_ref` not null → check for a related brief via `links` (`link_type='escalated_into'`). Found → merge-write arch_ref into the brief and its spec per `arch-map`.

## Step 6.5 — Check unclosed areas of parent task

If the current task is `part_of` a chain — find sibling tasks with status ≠ `done`. Any → warn:

```
⚠️ This task is part of chain {parent_id}. Unclosed:
- {id}: {title}

1. Close this — handle the rest separately
2. Open the next unclosed one now
```

## Step 7 — Update STATUS.md

Create/overwrite `{project_path}/STATUS.md` with: Last task / Pending / Next step.

## Step 7.5 — Close open/pending task blocks

Bulk-close any remaining blocks with `commit_hash='task-completed'` marker (distinguishes bulk-close from real per-block commits).

## Step 8 — Append to sessions.md

Append one line via Edit tool:

```
{date} {time} | {project}--{slug} | {✅ / ⚠️ / ❌} | {one-line summary}
```

Never overwrite — only append.

---

## Anti-patterns

### ❌ Inlining the skill instead of using the Skill() tool

Started executing the protocol manually from memory — outdated version, no accuracy guarantee. Always via `$ship-first`.

### ❌ Skipping Step 0.5 artifact check silently

Missing flow/library/plan/report/user-note artifacts left ungated — task closes with holes. Always check and prompt "Restore? (go / skip)".

### ❌ Executing both modes in one run

Per-block mode and task-level mode are mutually exclusive. Per-block does B1-B6 only. Task-level does 0.5-8 only.

### ❌ Overwriting sessions.md

The sessions log is append-only. Overwriting destroys history. Always Edit append, never Write.

---

## Related skills

- **plan-first** — invokes per-block ship-first after execute
- **arch-first / audit-first** — invoke task-level ship-first after all blocks close
- **ui-ai-first** — invoked at Step 0.6 if flag is set
- **go-guide** — invoked at Step 4.5 to create a guide
- **arch-map** — invoked at Step 4.7 to compute arch_ref

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'ship-first', datetime('now'))" 2>/dev/null || true
```
