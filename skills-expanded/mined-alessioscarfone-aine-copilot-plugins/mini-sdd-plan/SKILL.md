---
name: mini-sdd-plan
description: 'Generate or update the implementation plan for an existing spec — read spec.yaml and break it into an ordered, testable task checklist. Use when creating a plan from a spec, generating tasks, planning how to implement a feature, or refreshing a plan after the spec changed. Do not use for writing the spec itself (use mini-sdd-spec) or implementing code (use mini-sdd-implement).'
disable-model-invocation: true
---

Generate or update the implementation plan (`plan.md`) for a spec in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/`.

The plan reads the `spec.yaml` contract and breaks it into concrete, ordered, testable tasks. It is the bridge between the spec (what to build) and `mini-sdd-implement` (which executes the tasks).

> **Note:** This skill never modifies `spec.yaml` requirements — it only reads them and advances the spec's `status`. The spec contract is owned by `mini-sdd-spec`.

---

## Hook execution

Check `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` for `hooks.plan.pre` and `hooks.plan.post` entries. Run pre-hooks before the Entry point; run post-hooks after the full workflow completes. See [references/hooks.md](./references/hooks.md) for the full execution rules.

---

## Entry point

1. Read `./{ARTIFACT_MAIN_FOLDER}/context.md` if it exists — use it as background for tech stack, architecture, and conventions.
2. Determine which spec to plan:
   2.1 If a spec name is provided in the input (e.g., `/mini-sdd-plan user-authentication`), use it.
   2.2 If no name is provided, scan spec folders in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/` and read each `spec.yaml` `feature` block.
      - Present specs whose `feature.status` is `draft` (spec written, no plan yet) and any whose spec was updated after their plan:
        > `<spec-name>` → status `<status>` and ask the user to choose which one to plan.
      - If no specs exist, inform the user:
        > "No specs found in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/`. Use `/mini-sdd-spec` to create one first."
3. Once a spec is selected, output:
   > "Selected spec: `<spec-name>`"
4. Read `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/spec.yaml`: the `feature` block (`status`, `requires`, `created`, `updated`, `name`) and full content (`components`, `constraints`, and extensions).
5. Check whether `plan.md` already exists in the spec folder:
   - **No `plan.md`** → proceed to **Creation flow**.
   - **`plan.md` exists** → show a brief summary and ask:
     > "A plan already exists for `<spec-name>`. Do you want to **regenerate it** (replace) or **append new tasks** (keep history)?"
     - **Regenerate / Append** → proceed to **Update flow**.

---

## Creation flow

1. Read the spec content: `feature.description`, `components` requirements, `constraints`, non-goals, prerequisites, technical notes.
2. Break the spec into tasks following the rules in [references/task-rules.md](./references/task-rules.md). Tag every task with the ACID(s) it satisfies, e.g. `_(LOGIN.1)_` (the `<GROUP_KEY>.<ID>` form; the full ACID is `<spec-name>.<GROUP_KEY>.<ID>`).
3. If any open questions or assumptions were noted in the spec, ask the user for clarification before finalizing the tasks.
4. Present the task list to the user:
   > "📋 Tasks for `<spec-name>`:"
   > 1. \<task 1\>
   > 2. \<task 2\>
5. Ask: _"Does this task breakdown look good? Any adjustments?"_
6. After confirmation, write `plan.md` using `assets/plan.template.md` as the base, filling all the sections. Write to `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/plan.md`.
7. Advance the spec: in the `feature` block set `status: ready` and `updated: YYYY-MM-DD`. Do not change any requirement content.
8. Confirm to the user:
   > "✅ Created `<spec-name>/plan.md` with N tasks and set `<spec-name>/spec.yaml` to status: ready.
   > Next: run `/mini-sdd-implement <spec-name>` to execute the plan."

---

## Update flow

Use this when a `plan.md` already exists for the spec.

1. Read the current `plan.md` and the (possibly updated) `spec.yaml`.
2. Re-read the spec content and break it into tasks following [references/task-rules.md](./references/task-rules.md).
3. Decide based on the user's choice in the Entry point:
   - **Regenerate** → replace the task list with a fresh breakdown derived from the current spec.
   - **Append** → **append** a new dated section to the existing `plan.md` using `assets/plan.template.md` as the base. Do **not** remove existing tasks — preserve the history of previous implementations.
4. Present the new/updated task list and ask: _"Does this look good? Any adjustments?"_
5. After confirmation, write `plan.md`.
6. Advance the spec: in the `feature` block set `status: ready` and `updated: YYYY-MM-DD`.
7. Confirm:
   > "✅ Updated `<spec-name>/plan.md` (N tasks) and set `<spec-name>/spec.yaml` to status: ready."

---

## Task Rules

See [references/task-rules.md](./references/task-rules.md) for the full format, numbering, and content guidelines.

---

## Status lifecycle

This skill advances a spec from `draft` → `ready` once a plan exists. It never sets `in-progress` or `done` (owned by `mini-sdd-implement`). Whether a `ready` spec is currently implementable is derived from `requires:` — if any dependency is not `done`, implementation must wait.

---

## Output rules

{SKILL_ASSETS_NOTICE}
- One plan per spec, located alongside `spec.yaml` in the spec folder.
- Coding tasks only — no deployment, documentation, or manual testing tasks.
- Every requirement (`components` and `constraints`) must be covered by at least one task, tagged with its ACID `_(<GROUP_KEY>.<ID>)_`.
- Keep tasks small and ordered so dependencies are satisfied bottom-up.
- Do **not** modify the requirements in `spec.yaml` — only its `feature.status` and `feature.updated` fields.

## Error handling

- **No spec selected / not found**: List available specs and ask the user to choose, or tell them to run `/mini-sdd-spec` first.
- **Spec has no content to plan**: If `spec.yaml` has no requirements or only placeholders, ask the user to complete it with `/mini-sdd-spec` before planning.
- **Open questions in the spec**: Ask for clarification before finalizing tasks; if unanswered, note the assumption in the plan and proceed with best effort.
- **Plan folder not writable / path missing**: Create the spec folder if it does not exist before writing.
