---
name: sdd-parallel
description: Build a blast-radius-safe parallel wave plan across SDD roadmaps (BMAD, Spec Kit, GSD, OpenSpec, Beads), provision isolated git worktrees with non-invasive context boundaries, and orchestrate parallel tracks via Two-Stage Assisted (Interactive IDE Slots) or Multi-Window Autopilot.
---

# ⚡ SDD-Parallel — Multi-Track Orchestration Skill

## Overview

Use this skill whenever the user wants to:
1. Parallelize an SDD backlog or roadmap (`sprint-status.yaml`, `stories.yaml`, `epics.md`, `.scratch/**/issues/*.md`, `.specify/specs/*/tasks.md`, `.planning/ROADMAP.md`, `openspec/changes/*/tasks.md`, `.beads/issues.jsonl`).
2. Calculate file/AST/CRG blast-radius collisions and pack stories into barrier-synchronized waves ($K=2$ or $3$ tracks) with Model Effort routing (`high` / `medium` / `low`).
3. Provision clean `git worktree` environments with `.tmp/track-context.md` and `.parallel-lock.json` (`100% clean git status --porcelain`).
4. Execute waves via **Mode A: Two-Stage Assisted (Interactive IDE Slots — Spec Kit / GSD / OpenSpec / Beads / BMAD) (Recommended)** or **Mode B: Multi-Window Autopilot**, followed by deterministic checkpoint merges and quality gates.
5. Manage transactional wave safety via `abort-wave` and LIFO `rollback-wave` with automatic safety backup branches.

---

## Step 1: Discovery, Pre-Flight Gate & Wave Planning

1. Run the deterministic planner to inspect the repository, detect Wave 0 blockers (`git status --porcelain`, uncommitted `in-progress` stories), scan AST imports (`Spine Locks` vs `Additive Registries`), and compute impact radius via `code-review-graph` (optionally specify `--kit {auto,bmad,spec-kit,gsd,openspec,beads}` and `--routing-file <routing-overrides.json>`):
   ```powershell
   uv run sdd-parallel plan --repo <target-repo-path> --max-tracks 3 [--kit <kit>] [--routing-file <path>]
   ```
2. For BMAD repositories, the Pre-Flight Context Gate automatically validates the existence of `epic-<N>-context.md` in `implementation-artifacts` or `planning-artifacts` before wave execution to avoid add/add merge conflicts.
3. If multiple SDD ecosystems coexist in the same repository, `diagnose_multi_kit_coexistence()` warns the operator, automatically picks the kit with active backlog tasks, and isolates inactive kit directories.
4. When coupled with an external Cognitive Router (e.g. `Cloudflare Clef`, `Jev`, `Clairic`, `GLiClass`), pass `--routing-file <routing-overrides.json>` to `plan`, `prepare`, `run-guide`, or `autopilot` to override `effort`, `model`, and `execution_mode` per task without LLM calls in the core engine.

---

## Step 2: Operator Confirmation (`ask_question`)

Present the computed wave plan to the operator and prompt for execution flow:
1. **Execution Workflow:**
   - `(Recommended) Mode A: Two-Stage Assisted (Native SDD)` — Orchestrator provisions worktrees (`Depth 0`), operator opens independent Antigravity windows and launches native worker commands (`/bmad-build`, `/speckit.implement`, etc.) with full review lenses, then orchestrator verifies and merges.
   - `Mode B: Multi-Conversation Autopilot` — Automated Depth-0 launch across separate sessions via `sdd-parallel autopilot` (`--execute`, `--auto-merge`, `--policy`, `--timeout`).
   - `Mode C: In-Session Flat Dispatch (Deprecated / Fallback Only)` — Monolithic subagent dispatch inside single chat session (warning: lacks worktree directory isolation (`CWD`) and causes context window exhaustion in the orchestrator).

---

## Step 3: Wave Provisioning & Assisted Execution

### 3.1. Provision Worktrees for Wave $K$
```powershell
uv run sdd-parallel prepare --repo <target-repo-path> --wave <K> --antigravity-layout --headless [--kit <kit>]
```
This provisions or reuses fixed track slots in `~/.gemini/antigravity/worktrees/<Project>/track-<id>` ($K = \text{max\_tracks}$, e.g. `track-a`, `track-b`, ...) with Git 2.48 guard (`-c worktree.useRelativePaths=false`), performs an atomic in-place reset (`git checkout -B`, `git clean -fd`), injects `.tmp/track-context.md`, `.parallel-lock.json`, configures Claude Code sandbox settings (`.claude/settings.local.json` with `blockWritesOutsideWorkingDirectories`), and applies OS read-only locks (`chmod a-w` on forbidden files with `core.fileMode false`), keeping `git status --porcelain` **100% clean**.
*(Pass `--dynamic-worktrees` if legacy per-wave worktree directories `wave-<K>-track-<id>` are desired).*

### 3.2. Generate Operator Run Guide
```powershell
uv run sdd-parallel run-guide --repo <target-repo-path> --wave <K> --antigravity-layout [--kit <kit>]
```
This outputs a ready-to-copy Markdown matrix with worktree paths and framework-specific worker launch commands:
```text
| Track | Stories | Effort | Worktree Directory | Worker Command |
| :--- | :--- | :--- | :--- | :--- |
| track-a | 11-2 | high | .../track-a | `/speckit.implement 11-2` (or `/bmad-build`, `/gsd-execute-phase`, `/opsx:apply`, `bd update`) |
| track-b | 11-3 | medium | .../track-b | `/speckit.implement 11-3` (or `/bmad-build`, `/gsd-execute-phase`, `/opsx:apply`, `bd update`) |
```

### 3.3. Execute Native Workers (Depth 0)
Operator opens each worktree in an independent Antigravity window and triggers the worker:
- **GitHub Spec Kit:** `/speckit.implement <task-id>`
- **GSD:** `/gsd-execute-phase <phase-num>`
- **OpenSpec:** `/opsx:apply <task-id>`
- **Beads:** `bd update <task-id> --status in-progress`
- **BMAD:** `/bmad-build <task-id>` (full workflow: spec generation, TDD implementation, and Code Quality / Edge Cases / Test Coverage lenses).

### 3.4. (Deprecated / Fallback Only) Mode C: In-Session Flat Dispatch
> [!WARNING]
> While subagents support nesting up to 10 levels, `invoke_subagent` cannot bind subagents to separate `git worktree` working directories (`CWD`) or isolate Scope Guard locks. Running parallel story mutations inside a single chat session leads to shared directory conflicts and rapid context window exhaustion. Flat Dispatch should only be used as an emergency fallback when multi-window or CLI execution is impossible.

---

## Step 4: Verification & Barrier Checkpoint Merge

1. **Verify Lock Invariants & Scope Guard:**
   Verify that generated specs and code in worktrees did not touch forbidden blast-radius files (PreToolUse lock check, Terminal Guard validation, and clean git diff):
   ```powershell
   uv run sdd-parallel verify-wave --repo <target-repo-path> --wave <K> [--kit <kit>]
   ```
2. **Barrier Checkpoint Merge:**
   Merge all track branches into the base branch with polymorphic 3-way status resolution (`sprint-status.yaml`, `tasks.md`, `issues.jsonl`) and run mandatory quality gates:
   ```powershell
   uv run sdd-parallel merge --repo <target-repo-path> --wave <K> --cleanup [--kit <kit>]
   ```
   Quality gates executed automatically:
   - `uv run pytest`
   - `uv run ruff check src/ tests/`
   - `uv run mypy --strict src/`

---

## Step 5: Transactional Safety & Rollback Engine

If a wave fails verification, quality gates, or requirements during development:

1. **Abort Before Merge (Clean Worktrees & Branches):**
   ```powershell
   uv run sdd-parallel abort-wave --repo <target-repo-path> --wave <K>
   ```
   Removes active worktrees, prunes git metadata, and deletes temporary `parallel/wave-<K>-*` branches.

2. **Rollback After Merge (Strict LIFO Order with Backup):**
   ```powershell
   uv run sdd-parallel rollback-wave --repo <target-repo-path> --wave <K> --save-backup
   ```
   - Enforces strict LIFO invariant (only the latest merged wave can be rolled back).
   - Creates immutable safety branch: `backup/wave-<K>-before-rollback-<timestamp>`.
   - Resets repository `HEAD` to pre-merge commit.
   - Polymorphically resets task statuses in SDD artifacts (e.g. `sprint-status.yaml` $\to$ `ready-for-dev`) and cleans specs.

---

## Complete CLI Command Reference

All subcommands exposed by `sdd-parallel`:
- `plan`: Analyze SDD roadmap, AST/CRG graph, and construct wave plan (supports `--routing-file`).
- `prepare`: Provision isolated git worktree slots with boundary locks (supports `--routing-file`).
- `claim-track`: Attach boundary locks to an existing interactive IDE worktree slot.
- `run-guide`: Display operator execution instructions and native worker launch commands (supports `--routing-file`).
- `autopilot`: Generate and execute multi-conversation worker launch commands (supports `--routing-file`, `--execute`, `--auto-merge`, `--policy`, `--timeout`).
- `check-lock`: Validate if modifying a file is permitted by `.parallel-lock.json`.
- `verify-wave`: Validate that track commits strictly adhere to lock boundaries.
- `merge`: Checkpoint merge of parallel track branches with quality gates.
- `merge-status`: Monotonic 3-way deterministic merge for sprint and task status files.
- `abort-wave`: Transactionally discard in-flight wave worktrees and parallel branches.
- `rollback-wave`: Revert merged wave in strict LIFO order with safety backup branch.
- `install-plugin`: Package and deploy portable Antigravity IDE plugin.
- `demo`: Run standalone 5-second Merge-Bomb demo and multi-kit verification.
- `bench`: Run retrospective benchmark & confusion matrix evaluation on git history or synthetic demo.
- `inspect`: Launch or generate standalone interactive HTML Wave Inspector for wave plans and slot status.
- `init-custom`: Interactive onboarding wizard to configure custom SDD roadmap (.parallel/custom-kit.yaml).
