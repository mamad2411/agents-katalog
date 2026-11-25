---
name: clickup-task-breakdown
description: Turn scope documents (data model/UML, functional proposal, execution plan) into structured ClickUp tasks — modules as parent tasks, subtasks with "how to" descriptions, dependencies and CSV import. Use whenever you need to create tasks, break scope into activities, organize a backlog, plan a sprint or structure an execution plan in a project management tool.
---

# From scope documents to ClickUp tasks

Process for converting a project's planning documents into an executable backlog, without inventing scope.

## Rule number one: source of truth

Tasks are born **exclusively** from the project's source documents — typically three:

1. **Data model** (UML/entity diagram)
2. **Functional proposal** (what the system does, from the product view)
3. **Execution plan** (modules, hours, sequence)

If something isn't in any document, it doesn't become a task — it becomes a **question** for the tech lead. Generating tasks from imagined scope is the most expensive mistake in this process.

## Structure

- **Parent task = module from the execution plan.** One to one. If the plan has 7 modules, there are 7 parent tasks.
- **Subtask = verifiable deliverable within the module** (3–6 per module is normal). "Verifiable" = you can look at it and say whether it's done.
- Each subtask carries:
  - **Title**: infinitive verb + object ("Implement task CRUD", "Set up CI pipeline")
  - **"How to" description**: 3–8 lines grounded in the project's locked technical decisions — not a generic tutorial
  - **Estimate** inherited/apportioned from the module's hours in the plan
  - **Assignee** when team allocation is already known

## Sequencing and dependencies

Build the dependency graph between modules BEFORE distributing work (e.g. `Setup → Auth → domains in parallel → dashboards → QA`). In ClickUp, use *waiting on* relations between parent tasks; within a module, the subtask order already expresses the sequence.

Deliver alongside it a half-page **sequencing guide**: the order, the why, and where the team can parallelize.

## Import

For volume (20+ tasks), generate a CSV in ClickUp's Spreadsheet Importer format:

```csv
Task Name,Parent Task,Description,Time Estimate,Assignee
"Module A — Authentication and org structure",,"...",30h,
"Implement JWT login","Module A — Authentication and org structure","How to: ...",8h,John
```

Gotchas that have already caused rework:
- `Parent Task` references the **exact name** of the parent task (case-sensitive)
- Descriptions containing commas/line breaks go inside double quotes
- Estimates in the format the importer accepts (`8h`, not `8 hours`)
- No decorative Unicode characters (borders, emoji overload) — they break rendering in several places

## Quality checklist before delivering

- [ ] Every task traces back to a passage in a source document
- [ ] No module from the plan is missing a parent task
- [ ] Every subtask has a "how to" grounded in the project's decisions
- [ ] The sum of estimates matches the execution plan's hours (divergence = flag it, don't hide it)
- [ ] Sequencing guide delivered alongside
