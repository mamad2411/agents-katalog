---
name: pr-unresolved-solutions
description: Draft and track fixes for unresolved PR review threads. Use when you need to generate a solution draft markdown for the latest/current PR unresolved threads and keep `.pr/<pr_number>/review_checklist.md` plus `.pr/<pr_number>/unresolved_checklist.md` checkbox states synchronized as issues are fixed.
---

# PR Unresolved Solutions

Create a scaffold document for unresolved threads, then require the agent to immediately replace placeholders with executable solutions thread-by-thread (without asking for confirmation) and keep checklist states updated while implementing fixes.

## Files

- Proposal generator:
  - `scripts/generate_unresolved_solutions.py`
- Checklist state sync:
  - `scripts/sync_checklist_status.py`
- Resolved section pruner:
  - `scripts/prune_unresolved_solutions.py`
- Upstream review thread collector:
  - `../pr-review-checklist/scripts/generate_pr_review_checklists.py`

## Prerequisites

1. Run commands from this skill directory (the directory containing this `SKILL.md`).
2. Set `PYTHONPATH` to repo root.
3. Ensure `.pr/<pr_number>/unresolved_checklist.md` exists. If missing, generate it first.

## Commands

1. Refresh checklist files from GitHub (optional but recommended):

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 ../pr-review-checklist/scripts/generate_pr_review_checklists.py
```

2. Generate proposal scaffold markdown for unresolved threads (default: current branch PR; fallback: latest `.pr/*`):

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/generate_unresolved_solutions.py
```

The generator only creates scaffolding placeholders for each thread:
- `Initial Solution Proposal`
- `Planned Changes`
- `Validation`

The agent must replace all `AGENT_REQUIRED` placeholders with concrete content.

## Autonomous Execution Policy (Mandatory)

1. After running `generate_unresolved_solutions.py`, immediately edit `unresolved_solutions.md` and fill every `AGENT_REQUIRED` placeholder.
2. Do not ask the user whether to continue this filling step.
3. Ask the user only when a thread is truly blocked by missing product direction, missing access, or conflicting requirements.
4. If some threads are blocked, continue filling all other threads first, then report only the blocked `TH-*` IDs with clear unblock questions.

Overwrite behavior:
- When `--overwrite` is used, existing thread proposals in `unresolved_solutions.md` are preserved by default (matched by `TH-*`).
- New unresolved threads are scaffold-only.
- Use `--reset-all` together with `--overwrite` only when you intentionally want to discard all existing proposal content.

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/generate_unresolved_solutions.py --overwrite

export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/generate_unresolved_solutions.py --overwrite --reset-all
```

Optional classification overrides:

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/generate_unresolved_solutions.py \
  --decision-thread-ids TH-2773815990 TH-2773840027 \
  --direct-close-thread-ids TH-2754216760
```

3. After implementing fixes, mark resolved thread IDs in both checklists:

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/sync_checklist_status.py \
  --thread-ids TH-2773735433 TH-2780379352 \
  --state resolved
```

4. If rollback is needed, revert checkbox state:

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/sync_checklist_status.py \
  --thread-ids TH-2773735433 \
  --state unresolved
```

5. Remove resolved sections from `unresolved_solutions.md` without resetting unresolved proposal content:

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/prune_unresolved_solutions.py --pr-number 122
```

Optional targeted prune:

```bash
export PYTHONPATH=/path/to/browseruse_bench
python3 scripts/prune_unresolved_solutions.py \
  --pr-number 122 \
  --thread-ids TH-2773840027 TH-2773794870
```

## Workflow

1. Refresh `review_checklist.md` and `unresolved_checklist.md`.
2. Generate `unresolved_solutions.md`.
3. Agent immediately writes concrete solution content for every thread (no confirmation gate):
   - exact file paths/symbols to edit
   - concrete change intent and expected behavior impact
   - executable validation commands and acceptance criteria
4. If the user request includes fixing threads, continue to implement fixes in code/docs; otherwise stop after a complete solutions document is produced.
5. After each verified thread fix, run cleanup with default combined mode `1+2`:
   - `sync_checklist_status.py --state resolved` for solved `TH-*` IDs
   - `prune_unresolved_solutions.py` to remove solved sections
6. Re-run `generate_pr_review_checklists.py` when needed to reconcile with latest GitHub thread states.

## Quality Bar (Mandatory)

1. No generic statements such as "按评论意图修改" or "通过基本验证".
2. Each thread proposal must include:
   - at least one concrete file path
   - at least one concrete change action
   - at least one concrete validation command
3. Any unresolved `AGENT_REQUIRED` placeholder means the proposal is incomplete.

## Classification & Color Rules

1. Default thread classification:
   - `outdated=yes` -> direct close (red mark)
   - otherwise -> code/docs change
2. Force category with flags:
   - `--decision-thread-ids`: mark as "need direction"
   - `--direct-close-thread-ids`: force direct close
3. Output style:
   - Summary shows red-highlight count for direct-close threads
   - Each direct-close thread includes a red "分类标记" and red "建议处理"
