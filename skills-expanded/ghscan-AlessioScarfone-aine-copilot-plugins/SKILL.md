---
name: mini-sdd-guide
description: >-
  Autonomous knowledge base for the mini-SDD framework. Always read this skill
  when working on a mini-SDD project or when any message mentions mini-SDD,
  mini-sdd-context, mini-sdd-spec, mini-sdd-plan, mini-sdd-implement,
  mini-sdd-init-config, context.md, spec.yaml, plan.md, ARTIFACT_MAIN_FOLDER,
  SPECS_SUBFOLDER, hooks config, or spec-driven development. Do not use for
  creating context files, writing specs, planning, or implementing features —
  those have their own skills.
user-invocable: false
---

This file is the complete reference for the mini-SDD framework. Read it in full whenever a mini-SDD topic arises. Do not create or modify any project files based on this skill alone.

---

## What mini-SDD is

**mini-SDD** is a lightweight spec-driven development framework for GitHub Copilot. It enforces one rule: **specs before code**.

```
context → spec → plan → implement → repeat
```

| Skill | Command | Purpose |
|-------|---------|---------|
| Project Context | `/mini-sdd-context` | Capture the project foundation; update when architecture changes |
| Feature Spec | `/mini-sdd-spec` | Define a requirement contract (`spec.yaml`) |
| Implementation Plan | `/mini-sdd-plan` | Turn a spec into an ordered, testable task plan (`plan.md`) |
| Implement | `/mini-sdd-implement` | Execute the task plan for a spec |
| Hook Config | `/mini-sdd-init-config` | Configure custom pre/post hooks for any workflow step |

The **mini-sdd** agent orchestrates these skills — it reads project state and routes the user to the correct next action.

---

## Workflow

```
1. /mini-sdd-context  — Create or update context.md (once; re-run on stack changes)
         ↓
2. /mini-sdd-spec <feature>  — Create spec.yaml contract (status: draft)
         ↓
3. /mini-sdd-plan <spec>  — Generate plan.md from the spec (status: draft → ready)
         ↓
4. /mini-sdd-implement <spec>  — Execute plan.md tasks (resume-safe across sessions)
         ↓
   spec status → done → dependent specs unlocked
         ↓
   Repeat from step 2 for the next feature
```

**Step 1 — Context:** Inspects the codebase (README, manifests, CI, source dirs), asks targeted questions for gaps, writes `./{ARTIFACT_MAIN_FOLDER}/context.md`. Re-run after architectural changes.

**Step 2 — Spec:** Asks clarifying questions (feature, user, functional requirements, cross-cutting constraints, tech notes), infers dependencies from existing specs, writes `spec.yaml` (acai `feature.yaml` format — `feature` + `components` + `constraints`). Sets `feature.status: draft`.

**Step 3 — Plan:** Reads `spec.yaml`, breaks its requirements into ordered, testable tasks following the task rules, writes `plan.md`. Advances the spec to `status: ready`.

**Step 4 — Implement:** Reads tasks from `plan.md` one by one, marks checkboxes, updates `feature.status` (`in-progress` → `done`). On completion: unlocks dependent specs, fills `development_notes` in `spec.yaml`.

---

## File structure

```
./{ARTIFACT_MAIN_FOLDER}/               # Root folder (default: mini-sdd/)
├── context.md                          # Project foundation — written by mini-sdd-context
├── mini-sdd.config.yml                 # Hook configuration — written by mini-sdd-init-config
└── {SPECS_SUBFOLDER}/                  # Specs folder (default: specs/)
    └── <spec-name>/                    # One folder per feature
        ├── spec.yaml                    # Requirement contract (acai feature.yaml format)
        └── plan.md                     # Ordered implementation task checklist
```

**Variables** (resolved at build time from `config.json`):

| Variable | Default | Meaning |
|----------|---------|---------|
| `{ARTIFACT_MAIN_FOLDER}` | `mini-sdd` | Root folder for all mini-SDD artifacts |
| `{SPECS_SUBFOLDER}` | `specs` | Subfolder for spec folders inside `ARTIFACT_MAIN_FOLDER` |

**`spec.yaml` structure** (the file begins with `feature` and may contain `components` and `constraints`):

```yaml
feature:
  name: my-feature        # dash-case feature name
  version: 0.1.0          # optional, SemVer
  description: >-
    What the feature does, who benefits, why it matters.
  prerequisites: []       # optional external dependencies
  # mini-sdd tracking extension:
  status: draft           # draft | ready | in-progress | done
  requires: []            # spec names that must be done first
  created: YYYY-MM-DD
  updated: YYYY-MM-DD

components:               # functional requirements, grouped by UPPER_SNAKE keys
  LOGIN:
    description: ...
    requirements:
      1: Observable, testable behavior
      1-1: Optional sub-requirement (max 1 level)

constraints:              # cross-cutting / non-functional requirements (optional)
  AUTH:
    requirements:
      1: ...

# mini-sdd extensions: non_goals, technical_notes, open_questions, development_notes
```

A requirement is referenced by its **ACID**: `<feature-name>.<GROUP_KEY>.<ID>` (e.g. `my-feature.LOGIN.1-1`).

---

## Spec lifecycle

### Status values

| Status | Set by | Meaning |
|--------|--------|---------|
| `draft` | `mini-sdd-spec` | Spec contract written, no implementation plan yet |
| `ready` | `mini-sdd-plan` | Plan generated; spec is ready to implement |
| `in-progress` | `mini-sdd-implement` | Implementation has started |
| `done` | `mini-sdd-implement` | Implementation is complete |

### Dependency rules

- `requires:` lists spec names that must reach `done` before this spec is implementable.
- Dependencies are inferred automatically by `mini-sdd-spec`; the user is asked only when the relationship is ambiguous.
- A spec with unmet `requires` entries **cannot be implemented** even if `status` is `ready`.
- When a spec reaches `done`, `mini-sdd-implement` removes it from the `requires:` field of every spec that listed it and re-evaluates which specs are now unblocked.

### Task format (in `plan.md`)
```
- [ ] 1. Top-level task _(LOGIN.1)_
- [ ] 1.1 Sub-task _(LOGIN.1)_
- [x] 2. Completed task _(AUTH.2)_
- [ ]* 3. Optional task _(EXPORT.3)_    ← nice-to-have, not blocking
```

**Task rules:** Maximum 2 nesting levels. Every task references a requirement by its ACID: `_(<GROUP_KEY>.<ID>)_`. Parent tasks with sub-tasks are group headers — mark done only when all sub-tasks are checked. Coding tasks only — no deployment, docs, or manual testing.

---

## Skill behaviors

### `/mini-sdd-context`

- If `context.md` exists → summarises it, asks: update or overwrite?
- **Creation:** runs codebase reconnaissance (README, manifests, CI, source dirs), asks up to 5 targeted questions in one message, fills and writes `context.md`.
- **Update:** reads current file, applies only confirmed changes, refreshes `Last updated`.
- Reads `hooks.context.pre` before entry and `hooks.context.post` after completion.

### `/mini-sdd-spec`

- Reads `context.md` for background. Derives a dash-case spec name. Checks for an existing spec and asks to update or create new if found.
- **Creation:** single clarification message (feature description, user, functional requirements, cross-cutting constraints, technical notes). Infers `requires:` from existing specs. Writes `spec.yaml` (`feature` + `components` + `constraints`) and sets `feature.status: draft`. Hands off to `/mini-sdd-plan`.
- **Update:** edits `spec.yaml` requirements, refreshes `feature.updated`, and resets `feature.status: draft` so the plan can be regenerated. Never touches `plan.md`.
- Reads `hooks.spec.pre` before entry and `hooks.spec.post` after completion.

### `/mini-sdd-plan`

- Reads `context.md` and the selected spec's `spec.yaml`. If no spec name given, lists `draft` specs (and specs whose plan is out of date) and asks the user to choose.
- **Creation:** breaks the spec requirements into ordered tasks (per the task rules), tags each task with the requirement ACID, presents them for confirmation, writes `plan.md`, and advances the spec to `feature.status: ready`.
- **Update:** regenerates or appends tasks to an existing `plan.md` (preserving history when appending), then re-confirms `status: ready`.
- Never modifies the requirements in `spec.yaml` — only its `feature.status` and `feature.updated` fields.
- Reads `hooks.plan.pre` before entry and `hooks.plan.post` after completion.

### `/mini-sdd-implement`

- Reads `context.md` for architecture context. If no spec name given, lists `ready` (unblocked) and `in-progress` specs and asks the user to choose.
- **Execute:** sets status to `in-progress`; for each unchecked task: announces it, implements the code, marks `- [ ]` → `- [x]`, updates `updated` date. Pauses on unclear tasks or discovered issues.
- **Resume:** when `status` is `in-progress`, finds first unchecked task, shows progress (N/M done), asks for confirmation.
- **Completion:** marks satisfied requirements, sets `feature.status: done`, removes the spec from `requires:` of dependent specs (unlocking them), fills `development_notes` in `spec.yaml` (files changed, follow-ups), shows a summary.
- Reads `hooks.implement.pre` before entry and `hooks.implement.post` after completion.

### `/mini-sdd-init-config`

- If `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` exists → shows configured hooks, asks: update or reset?
- Runs the hook interview: all eight events in one message, pre-filled with current values.
- Writes (or overwrites) the config; shows the final file content. Never writes empty hook lists.

---

## Hook system

Hooks inject plain-text instructions before or after any skill's workflow. No shell scripts — the AI executes them as instructions.

**Supported events:**

| Step | Pre hook key | Post hook key |
|------|-------------|--------------|
| context | `hooks.context.pre` | `hooks.context.post` |
| spec | `hooks.spec.pre` | `hooks.spec.post` |
| plan | `hooks.plan.pre` | `hooks.plan.post` |
| implement | `hooks.implement.pre` | `hooks.implement.post` |

**Execution:** pre-hooks run before the skill's entry point; post-hooks run after the full workflow. Each instruction is announced: `"⚙️ Pre-hook: <instruction>"`. If a hook is ambiguous or cannot be executed, skip it without blocking the main workflow.

**Config format** (`./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml`):

```yaml
hooks:
  context:
    post:
      - "Update the CHANGELOG with a summary of context changes"
  implement:
    pre:
      - "Check git status and confirm the working tree is clean before starting"
    post:
      - "Run the test suite and report any failures"
```

**Hook writing rules:** imperative sentences; one atomic action per item; pre hooks are non-destructive; omit empty events entirely.

---

## Assessing project state

When determining the current state of a mini-SDD project or deciding what to do next:

1. Check whether `./{ARTIFACT_MAIN_FOLDER}/context.md` exists. If missing, the first action is always `/mini-sdd-context`.
2. Scan `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/` for spec folders. For each, read the `spec.yaml` `feature` block to get `status` and `requires`. Classify:
   - `in-progress` specs — highest priority to resume
   - `draft` specs — spec written but no plan yet; next action is `/mini-sdd-plan`
   - `ready` specs where all `requires` entries are `done` — implementable next
   - `ready` specs with unmet `requires` — blocked, not yet implementable
   - `done` specs — complete
3. Check whether `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` exists.

**Decision table:**

| Situation | Recommended action |
|-----------|-------------------|
| `context.md` missing | `/mini-sdd-context` |
| No specs exist | `/mini-sdd-spec <feature-name>` |
| A spec is `draft` (no plan) | `/mini-sdd-plan <spec-name>` |
| A spec is `in-progress` | `/mini-sdd-implement <spec-name>` to resume |
| Unblocked `ready` specs exist | `/mini-sdd-implement <spec-name>` |
| All specs `done`, nothing in-progress | `/mini-sdd-spec <next-feature>` |
| Hooks not configured and user wants customisation | `/mini-sdd-init-config` |

**State summary format** (use when reporting state to the user):

```
📊 Project state:
- Context: ✅ exists (last updated: YYYY-MM-DD) | ❌ missing
- Specs:   N total — D draft, X ready (Y implementable, Z blocked), A in-progress, B done
- Hooks:   ✅ configured (N events) | ❌ not configured
- Next recommended action: <action>
```

{SKILL_ASSETS_NOTICE}
