---
name: to-issues
description: Break a plan or PRD into vertical-slice issues on the project issue tracker.
disable-model-invocation: true
---

Break work into **tracer-bullet** vertical slices — each cuts all layers end-to-end, demoable alone.

Run `/aiops-setup` if tracker config is missing.

## Modes

- **Multi-session** (PRD exists): full issue decomposition → `issues/*.md` published to tracker.
- **Single-session** (no PRD, `task_breakdown` phase): lightweight → single `tasks.md` in `.scratch/<slug>/`, no tracker publish.

## Process

1. **Context** — conversation or fetched issue/PR from `docs/agents/issue-tracker.md`. For single-session, use `tech-spec.md` + `NOTES.md` as input.
2. **Explore** (optional) — codebase, domain vocabulary, prefactor opportunities.
3. **Draft slices** — title, blocked-by, user stories covered. Prefactor slices first.
4. **Quiz user** — granularity, dependencies, merge/split. Iterate until approved.
5. **Publish** — dependency order; `ready-for-agent` unless told otherwise. Don't close parent. For single-session, write `tasks.md` to `.scratch/<slug>/`.

### Single-session two-phase breakdown (task_breakdown phase)

When in `task_breakdown` phase (single-session), run as two sub-phases with a human checkpoint between:

**Phase 1 — parent tasks (3–5 items)**
- Draft coarse-grained parent tasks from `tech-spec.md` + `NOTES.md`
- Each parent task is one demoable vertical slice
- Present to user: confirm, reorder, merge, or split before proceeding

**Phase 2 — sub-task expansion** (only after user confirms parent tasks)
- Expand each parent task into concrete sub-tasks with explicit `blocked_by` dependencies
- Compute waves via topological sort
- Write `tasks.md` with YAML frontmatter

## Issue template

**Parent** — link if applicable.

**What to build** — end-to-end behavior, not layer checklist.

**Acceptance criteria** — checkboxes.

**Blocked by** — issue refs or "None".

## tasks.md template (single-session)

Include YAML frontmatter for structured dependency tracking:

```markdown
---
tasks:
  - id: t1
    title: "Add WorkspacePaths dataclass"
    blocked_by: []
  - id: t2
    title: "Wire workspace_paths() resolver"
    blocked_by: [t1]
  - id: t3
    title: "Update path helpers to use WorkspacePaths"
    blocked_by: [t1]
  - id: t4
    title: "Integration tests"
    blocked_by: [t2, t3]
waves:
  - [t1]
  - [t2, t3]
  - [t4]
---

# Tasks: <slug>

## Wave 1
- [ ] **t1**: Add WorkspacePaths dataclass — <end-to-end behavior>. Blocked by: None

## Wave 2
- [ ] **t2**: Wire workspace_paths() resolver — <end-to-end behavior>. Blocked by: t1
- [ ] **t3**: Update path helpers to use WorkspacePaths — <end-to-end behavior>. Blocked by: t1

## Wave 3
- [ ] **t4**: Integration tests — <end-to-end behavior>. Blocked by: t2, t3
```

Group tasks by wave in the body. Waves are computed from `blocked_by` via topological sort.
