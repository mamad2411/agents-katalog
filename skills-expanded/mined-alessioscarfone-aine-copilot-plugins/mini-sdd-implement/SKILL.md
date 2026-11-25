---
name: mini-sdd-implement
description: 'Implement a feature from an existing spec file — write code, create tests, and update files to make a spec done. Use when executing development work defined in a spec, building or developing a feature, coding from a spec, or when asked to "implement the spec", "code this up", "develop the feature", or "follow the specification". Do not use for creating specs, updating project context, or proposing new features.'
disable-model-invocation: true
---
You are a Developer who has been dispatched to implement code, complete tasks, or resolving feedback based on an existing spec in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/`.

Reads the task list from the spec's `plan.md`, executes tasks one by one, tracks progress via checkboxes, and writes development notes into `spec.yaml` on completion. Supports resuming across sessions.

If you find that you've been going in circles or have a major question, it's OK to stop early and invite the reviewer for feedback. They can tell you what to do next.

> **Note:** Task generation is handled by `mini-sdd-plan`. This skill only executes tasks already written in `plan.md`.

---

## Hook execution

Check `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` for `hooks.implement.pre` and `hooks.implement.post` entries. Run pre-hooks before the Entry point; run post-hooks after the full workflow completes. See [references/hooks.md](./references/hooks.md) for the full execution rules.

---

## Entry point

1. Read `./{ARTIFACT_MAIN_FOLDER}/context.md` if it exists — use it as background for architecture decisions, tech stack, and conventions.
2. Determine which spec to implement:
   2.1 If a spec name is provided in the input (e.g., `/mini-sdd-implement user-authentication`), use it.
   2.2 If no name is provided, scan spec folders in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/` and read each `spec.yaml` `feature` block. 
      - Present all `ready` (with all `requires` dependencies satisfied) and `in-progress` specs: 
      > `<spec-name>` → `status` (ready/in-progress) and ask the user to choose which one to implement.
      - If no specs exist, inform the user:
      > "No specs found in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/`. Use `/mini-sdd-spec` to create one first."
3. Once a spec is selected, output:
   > "Selected spec: `<spec-name>`"
4. Read `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/spec.yaml` `feature` block (`status`, `requires`, `created`, `updated`) plus `components`/`constraints`, and `plan.md`.
5. Verify the spec status and decide the flow:
   - `draft` → the spec has no plan yet. Stop and inform the user:
     > "`<spec-name>` has no implementation plan yet (status: draft). Run `/mini-sdd-plan <spec-name>` to generate the plan first."
   - `ready` → verify `plan.md` exists and has unchecked tasks, then proceed to **Execute tasks**.
     - Evaluate `requires:`: if any dependency is not `done`, stop and list the unmet ones with their current statuses.
     - If `plan.md` is missing or has no tasks, inform the user:
       > "`plan.md` has no tasks for `<spec-name>`. Run `/mini-sdd-plan` to generate the plan first."
   - `in-progress` → proceed to **Resume implementation**.
   - `done` → ask: _"This spec is already marked as done. Do you want to re-run it?"_ If yes, proceed to **Execute tasks** (all tasks will be re-run if already checked).

---

## Resume implementation

1. Read `plan.md`, find the first unchecked task (`- [ ]`), and show progress:
   > "📊 Resuming `<spec-name>`: N/M tasks complete. Next: \<task description\>. Continue?"
2. On confirmation, proceed to **Execute tasks** from the first unchecked task.

---

## Execute tasks

> **Metadata convention**: always write `updated: <today's date>` to the `feature` block of `spec.yaml` whenever you modify it.

Before starting, set `feature.status` in `spec.yaml` to `in-progress`.

For each unchecked task in `plan.md` in order:

1. Announce which task is being worked on:
   > "🔨 Task N/M: \<task description\>"
2. Implement the code changes required for this task.
3. Keep changes minimal and focused on the task.
4. Mark the task complete **in `plan.md`**: `- [ ]` → `- [x]` right after the implementation of that task.

**Pause if:**
- Task is unclear → ask for clarification
- Implementation reveals an issue → report and wait for guidance
- User interrupts → keep `feature.status` as `in-progress`, summarize progress

---

## Completion

When all tasks are checked:

1. Review each requirement (every `components` and `constraints` entry) from `spec.yaml` and check that all are satisfied based on the implementation.
2. In the `feature` block of `spec.yaml` set: `status: done`.
3. Scan other specs whose `feature.requires:` contains `<spec-name>` and update them:
   - Remove `<spec-name>` from their `requires:` list.
   - If `requires` is now empty → set `status: ready`; otherwise keep it blocked (unmet `requires`).
   - Summarize any specs that became unblocked.
4. Fill the `development_notes` key in `spec.yaml`: summarize all tasks implemented (not just this session), list every changed file with a short description, and note any follow-ups.
5. Show a completion summary:

```
✅ Implementation complete: <spec-name>

Tasks: M/M done
Requirements: N/M satisfied

Changes made:
- <file 1>: <what changed>
- <file 2>: <what changed>
```

## After completion

Follow [references/after-completion.md](./references/after-completion.md) for the `context.md` update flow. This step must run every time implementation ends — including after post-completion fixes.

---

## Error handling

- **Spec not found**: List available specs and ask the user to choose.
- **Dependency gate**: Stop, list unmet dependencies from `requires`, and tell the user to complete those specs first.
- **Unclear requirement**: Ask for clarification before implementing.
- **Implementation paused**: Keep status as `in-progress`, tasks preserve progress for the next run.

---

## Output rules

{SKILL_ASSETS_NOTICE}
- Follow the tech stack and conventions from `context.md`.
- Write clean, idiomatic code — no unnecessary abstractions.
- All progress tracking lives in `plan.md` located alongside `spec.yaml` in the spec folder.
- Update task status after each completed task, not all at the end of the implementation. 
- Do not modify unrelated specs or unrelated files.
