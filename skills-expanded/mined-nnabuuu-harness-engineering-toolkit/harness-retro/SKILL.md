---
name: harness-retro
version: 1.1.0
description: "Retrospective on completed harness tasks. Analyzes run data (scores, eval reports, changelogs) to identify convergence issues, bottleneck dimensions, repeated work, and cost inefficiency. Generates concrete prompt/rubric improvements. Optionally archives completed tasks. Standalone archive mode available — skip analysis, go straight to workspace cleanup. Triggers: 'retro', 'retrospective', 'review harness', 'analyze harness', '复盘', '回顾', '总结harness', 'archive harness', 'archive task', 'clean up workspace', '归档harness', '归档'."
---

# Harness Retrospective

Analyze completed harness runs to extract patterns and generate concrete improvements to prompts, rubrics, and exit conditions. This is L4 — the evaluation loop applied to the harness system itself.

## Self-Review Checklist (read BEFORE and AFTER every phase)

### Discovery Guards
- [ ] Scanned ALL task directories in `.harness-workspace/`, not just first match
- [ ] Verified each task has enough data to analyze (at minimum: state.json or progress.md)
- [ ] Confirmed scope with user before starting analysis

### Analysis Guards
- [ ] Read ALL eval reports and changelogs for selected tasks
- [ ] Did not skip any dimension — marked "insufficient data" if data missing
- [ ] All findings cite specific evidence (iteration numbers, scores, file paths)
- [ ] Cross-task analysis (D6) only when 2+ tasks selected

### Report Guards
- [ ] Improvement suggestions include concrete diffs, not just descriptions
- [ ] Suggestions reference specific dimension names from EVAL_CRITERIA.md
- [ ] Report saved to RETRO.md in the task directory (single-task) or `.harness-workspace/RETRO-{date}.md` (multi-task)

### Archive Guards
- [ ] Archive only after retro report is complete (Entry A) OR after user acknowledges no RETRO.md (Entry B)
- [ ] User explicitly confirmed before any file operations
- [ ] Entire task directory moved to `_archive/`, not left split across two locations
- [ ] DAGU symlink updated to point to new `_archive/` path (execution history preserved)

---

## Entry Point Detection

Determine which entry point the user needs before starting any phase.

- **Entry A — Full Retro**: Phases 1 → 2 → 3 → 4 (archive optional at end). The complete retrospective flow.
- **Entry B — Standalone Archive**: Skip directly to Phase 4A. Archive completed/failed tasks without running analysis.

### Detection Rules

| User says | Entry |
|-----------|-------|
| "archive harness", "archive task", "clean up workspace", "归档harness", "归档" | **Entry B** |
| "retro", "retrospective", "review harness", "analyze harness", "复盘", "回顾", "总结harness" | **Entry A** |
| Unclear or ambiguous | Ask: "Do you want a full retrospective (analysis + improvements), or just archive completed tasks?" |

---

## Phase 1: Discovery

### Step 1.1: Scan Workspace

Scan `.harness-workspace/` for all task directories. For each directory, extract:

- Task name (directory name)
- Status (from `state.json` → `status` field, or infer from progress.md)
- Mode (document / code / investigation — from `state.json` or SPEC.md)
- Iteration count (from `state.json` → `current_iteration`, or count eval reports)
- Final score (from progress.md last entry, or last eval report)
- Date range (from `state.json` timestamps, or file modification dates)

If `.harness-workspace/` doesn't exist or is empty, inform the user:
> "No harness workspace found. Run `/harness-create` to create a harness first."

### Step 1.2: Present Summary

Show the user a table of all discovered tasks:

```
| # | Task | Mode | Status | Iterations | Final Score | Date |
|---|------|------|--------|-----------|-------------|------|
| 1 | api-docs | document | completed | 8 | 82/100 | Apr 10 |
| 2 | auth-refactor | code | completed | 12 | 71/100 | Apr 14 |
| 3 | perf-bug | investigation | completed | 5 | — | Apr 15 |
```

### Step 1.3: Select Scope

Ask the user:
> "Which tasks should I analyze? Options: a single task (deep dive), multiple tasks (cross-task patterns), or all."

- **Single task**: Deep dive with all 6 dimensions (D6 marked N/A)
- **Multiple tasks / all**: All 6 dimensions including cross-task patterns (D6)

### Step 1.4: Load Data

For each selected task, read:
1. `state.json` — iteration tracking, timestamps, status
2. `progress.md` — score history
3. `SPEC.md` — the frozen target
4. `EVAL_CRITERIA.md` — rubric definitions (if present)
5. All files in `eval-reports/` — per-iteration evaluator output
6. All files in `changelogs/` — per-iteration change descriptions
7. All files in `prompts/` — agent prompt files

If a file is missing, note it — do not abort. Some dimensions can still run with partial data.

---

## Phase 2: Analysis

Run all 6 dimensions. Read `references/analysis-playbook.md` for detailed procedures.

| # | Dimension | What it detects | Key data source |
|---|-----------|----------------|-----------------|
| 1 | Convergence | Plateaus, regressions, oscillation, slow/fast convergence | progress.md, state.json |
| 2 | Bottleneck Dimensions | Eval dimensions that never improved | eval-reports/ + EVAL_CRITERIA.md |
| 3 | Repeated Work | Same fix attempted 3+ times — evaluator feedback not actionable | changelogs/ cross-referenced with eval-reports/ |
| 4 | Cost Efficiency | Wasted iterations, useful-iteration ratio, diminishing returns | state.json + progress.md |
| 5 | Prompt Quality | Spec drift, missing fresh context, non-actionable evaluator feedback | prompts/ + eval-reports/ + SPEC.md |
| 6 | Cross-Task Patterns | Systemic template issues across multiple tasks | All of the above, across tasks |

### Analysis Rules

- **Never skip a dimension.** If data is insufficient, classify as "insufficient data" with an explanation of what's missing, not as "healthy".
- **Always cite evidence.** Every finding must reference specific iteration numbers, scores, dimension names, or file paths.
- **D6 gate**: Only run Dimension 6 when 2+ tasks are selected. For single-task retros, mark as "N/A — single task selected".
- **Investigation mode**: Tasks in investigation mode don't have numeric scores. Adapt D1 (convergence) to track hypothesis status changes instead (ACTIVE → ELIMINATED/CONFIRMED). D2 and D4 adapt to hypothesis count and evidence quality.

---

## Phase 3: Report & Recommendations

### Step 3.1: Generate Report

Read `references/retro-report-template.md` for the output format.

- **Single-task**: Save as `RETRO.md` in the task directory (e.g., `.harness-workspace/{task-name}/RETRO.md`)
- **Multi-task**: Save as `.harness-workspace/RETRO-{date}.md`

The report must include:
1. Score trajectory (or hypothesis timeline for investigation mode)
2. All 6 dimension findings with status, evidence, and impact
3. "What Went Well" section — always include positive findings
4. Recommended actions, prioritized by impact

### Step 3.2: Generate Improvement Suggestions

For each finding with status "concern" or "problem", generate a **concrete improvement suggestion**. Each suggestion must be one of:

**Prompt patch** — a before/after diff for a specific prompt file:
```diff
# prompts/generator.md
- Improve the code quality based on the evaluator feedback.
+ Improve the code quality based on the evaluator feedback.
+ IMPORTANT: Do not undo improvements from previous iterations.
+ Read the changelog from the previous iteration before making changes.
```

**Rubric adjustment** — a specific weight or detection method change to EVAL_CRITERIA.md:
```diff
# EVAL_CRITERIA.md
- Error Handling: 2/5 weight — checks for try/catch blocks
+ Error Handling: 2/5 weight — checks for try/catch blocks, specific error types, and user-facing error messages. Evaluator must cite specific functions missing error handling.
```

**Exit condition change** — threshold or max_iterations adjustment:
```diff
# harness.sh or state.json
- EXIT_THRESHOLD=80
+ EXIT_THRESHOLD=75
+ PLATEAU_EXIT=3  # Exit if score unchanged for 3 consecutive iterations
```

**Template improvement** — change to `harness-create/references/` for future harness creation:
```diff
# harness-create/references/prompt-templates.md
- ## Generator Prompt Base
+ ## Generator Prompt Base
+ > IMPORTANT: Include a "do not undo previous improvements" constraint in every generator prompt.
```

### Step 3.3: Present Suggestions

Present each suggestion **one at a time** to the user. For each:

1. State the dimension and finding that motivates it
2. Show the concrete diff
3. Ask: "Apply this change?" (yes / skip / modify)
4. If yes: apply the change to the file
5. If modify: let the user adjust, then apply
6. Move to next suggestion

This mirrors the audit skill's "one fix at a time" interaction pattern.

### Step 3.4: Self-Review

Re-read the Self-Review Checklist at the top of this file. Verify every applicable item. Fix any violations before presenting the output to the user.

---

## Phase 4: Archive (optional)

### Step 4.1: Offer Archive

After the retro report is complete, ask:
> "Would you like to archive the completed task(s)? This moves the task directory to `_archive/` and updates the DAGU symlink so execution history stays visible."

Only proceed if the user confirms.

### Step 4.2: Execute Archive

Read `references/archive-policy.md` for the detailed policy.

For each task to archive:
1. Verify RETRO.md exists (it will always be present — Phase 3 just created it)
2. Clear stale lock fields in state.json
3. Move `.harness-workspace/{task-name}/` → `.harness-workspace/_archive/{task-name}/`
4. Write `archived-at.txt` with current timestamp
5. Update DAGU symlink to point to new `_archive/{task-name}/dag.yaml` path (if symlink existed)

### Step 4.3: Confirm

Show the user what was archived. The task directory is now under `_archive/` and DAGU execution history remains accessible.

---

## Phase 4A: Standalone Archive (Entry B)

This phase runs when the user enters via Entry B — they want to archive without running a full retro.

### Step 4A.1: Scan Workspace

Scan `.harness-workspace/` for all task directories (reuse Phase 1 scanning logic). For each directory, extract:

- Task name (directory name)
- Status (from `state.json` → `status` field, or infer from progress.md)
- Whether `RETRO.md` exists
- Iteration count (from `state.json` → `current_iteration`, or count eval reports)
- Final score (from progress.md last entry, or last eval report)

If `.harness-workspace/` doesn't exist or is empty, inform the user:
> "No harness workspace found. Run `/harness-create` to create a harness first."

### Step 4A.2: Present Archivable Tasks

Show a table of tasks with status `completed` or `failed` only — these are archivable:

```
| # | Task | Status | Iterations | Final Score | RETRO.md |
|---|------|--------|-----------|-------------|----------|
| 1 | api-docs | completed | 8 | 82/100 | Yes |
| 2 | auth-refactor | completed | 12 | 71/100 | No ⚠️ |
| 3 | perf-bug | failed | 5 | — | No ⚠️ |
```

- Tasks **without RETRO.md** get a ⚠️ warning
- For each flagged task, show: "⚠️ No RETRO.md — running `/harness-retro` first would capture learnings before archiving. Proceed anyway?"
- Recommend retro but **do not block** — let the user decide

If no tasks are archivable (all `in_progress` or `pending`), inform the user:
> "No completed or failed tasks found to archive."

### Step 4A.3: Confirm Archive

Ask the user to select which tasks to archive from the table. For each selected task, show what will happen:

- **Entire task directory** moved to `_archive/{task-name}/` — all files preserved intact
- **DAGU symlink** updated to point to new path — execution history stays visible
- **Original location** cleared from workspace

Only proceed after the user confirms.

### Step 4A.4: Execute Archive

Read `references/archive-policy.md` for the detailed policy, then for each confirmed task:

1. Check for RETRO.md — if missing, warn (standalone path allows this); if present, keep
2. Clear stale lock fields in state.json
3. Move `.harness-workspace/{task-name}/` → `.harness-workspace/_archive/{task-name}/`
4. Write `archived-at.txt` with current timestamp
5. Update DAGU symlink to point to new `_archive/{task-name}/dag.yaml` path (if symlink existed)

### Step 4A.5: Summary

Show a summary table of archived tasks:

```
| Task | Files | New Location | DAGU History |
|------|-------|-------------|--------------|
| api-docs | 21 | _archive/api-docs/ | Preserved |
| auth-refactor | 34 | _archive/auth-refactor/ | Preserved |
```

---

## Language & Adaptation Rules

- Match the user's language throughout (analysis, report, suggestions)
- Dimension names and structural labels stay in English for cross-tool compatibility
- If the user switches language mid-conversation, follow the switch
- Investigation mode tasks: adapt score-based analysis to hypothesis-based analysis

---

## 4-Layer Model Connection

The retro skill is L4 — the evaluation loop applied to the harness system:

| Dimension | Measures | Layer Connection |
|-----------|----------|-----------------|
| D1 Convergence | Did the loop drive improvement? | L4 effectiveness |
| D2 Bottleneck Dimensions | Are constraints well-calibrated? | L3 constraint quality |
| D3 Repeated Work | Is evaluator feedback actionable? | L3 constraint quality |
| D4 Cost Efficiency | Was effort well-spent? | L4 effectiveness |
| D5 Prompt Quality | Are goals and context correct? | L1 goal alignment + L2 context engineering |
| D6 Cross-Task Patterns | Are templates systemically sound? | All layers |

---

## Reference File Index

| Phase | Reference File | Load When |
|-------|---------------|-----------|
| 2 | `references/analysis-playbook.md` | Starting analysis on any dimension |
| 3.1 | `references/retro-report-template.md` | Generating RETRO.md |
| 4.2 | `references/archive-policy.md` | User confirms archive |
| 4A.4 | `references/archive-policy.md` | User confirms standalone archive |
