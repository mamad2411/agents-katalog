---
name: scope-task
description: "This skill scopes and researches a single new task to insert into an existing project's ROADMAP.md. It should be used when a developer identifies a gap in the roadmap during the do-task/checkpoint loop and needs to properly scope a new action item before implementing it. Triggered by requests like '/scope-task 2.5 Integrate Research into SPEC.md', '/scope-task 3.3 Add WebSocket support', or 'scope task 1.4 Set up CI pipeline'. Works alongside project-init (which creates the roadmap) and do-task (which implements tasks)."
---

# Scope Task

## Overview

This skill researches and scopes a single new task, then inserts it into an existing ROADMAP.md at the specified position. It follows the same discovery depth as project-init — web research, self-reflection, and user interview — but focused on one task rather than an entire project. The output is a properly formatted action item inserted into the roadmap, ready for `do-task` to implement.

## Workflow

### Step 1: Parse Arguments

Extract two pieces from the user's input:

- **Task ID** — numeric identifier in `<phase>.<item>` format (e.g., `2.5`, `3.3`)
- **Task Title** — the descriptive title following the ID (e.g., "Integrate Research into SPEC.md")

If either is missing or malformed, ask the user to provide the full invocation: `/scope-task <phase.item> <Task Title>`.

### Step 2: Load Project Context

Read the following files from the current working directory (check `docs/` subdirectory first, then project root):

1. **ROADMAP.md** — to understand existing phases, task numbering, and what has already been scoped
2. **SPEC.md** — to understand the project's architecture, tech stack, data models, and key decisions

If ROADMAP.md does not exist, inform the user and stop — this skill requires an existing roadmap to insert into.

Validate the task ID:
- The phase number must correspond to an existing phase in the roadmap (Phases 1-4 for actionable tasks; Phase 5 for future directions)
- The item number must not already exist — scope-task always creates new insertions
- If the ID conflicts with an existing task, list nearby IDs and ask the user to pick an available slot

### Step 3: Research

Conduct targeted research using `WebSearch` to investigate:

- **Best practices** — established patterns and approaches for this type of task given the project's tech stack
- **Similar implementations** — how other projects have solved this problem
- **Libraries and tools** — relevant packages, APIs, or utilities that could aid implementation
- **Trade-offs** — alternative approaches with their pros and cons
- **Pitfalls** — common mistakes and gotchas specific to this task

Keep research focused on the single task — not the broader project. Use SPEC.md context to make searches specific to the project's stack and architecture.

### Step 4: Self-Reflection

Before interviewing the user, pause and reason through:

- How research findings connect to the project's existing architecture (from SPEC.md)
- What the task's requirements should be, based on research
- Gaps in understanding that only the user can fill
- Potential impacts on other roadmap tasks
- Scope boundaries — what this task should and should not include
- Questions where the answer is NOT obvious from SPEC.md, ROADMAP.md, or research

### Step 5: Interview

Use `AskUserQuestion` to clarify unresolved items from Steps 2-4. Topics may include:

- Technical implementation choices surfaced by research
- Scope boundaries — what exactly should be in vs. out
- Integration points with existing or planned roadmap tasks
- Acceptance criteria the user has in mind
- Priority or ordering relative to neighboring tasks

Rules for the interview:
- Do NOT ask questions whose answers are obvious from SPEC.md, ROADMAP.md, or research
- Do NOT re-ask information already present in the project documentation
- Each round should surface genuinely new information
- Keep it focused — this is one task, not a full project discovery
- 1-2 rounds of questions is typical; go deeper only if the task is genuinely complex

### Step 6: Write the Action Item

Compose the new task following the canonical roadmap format.

**For Phases 1-4**, use exactly 3 subsections:

```markdown
### <phase>.<item> <Task Title>

**Description**: What this task is and why it matters. Connect it to the project's goals and architecture.

**Requirements**:
- [ ] Concrete deliverable 1
- [ ] Concrete deliverable 2
- [ ] ...

**Implementation Notes**: Technical guidance, references to specific libraries or APIs discovered during research, trade-offs considered, gotchas to watch for. Reference relevant parts of SPEC.md where helpful.
```

**For Phase 5 (Future)**, use the alternative format:

```markdown
### <phase>.<item> <Task Title>

**Description**: What this direction is about.

**Features**:
- Potential feature or capability 1
- Potential feature or capability 2

**Rationale**: Why this direction is worth pursuing.
```

Quality guidelines for the action item:
- Requirements should be concrete, testable, and individually checkable
- Implementation Notes should contain genuinely useful technical guidance drawn from research — not generic advice
- Description should clearly explain *why* this task matters in the context of the project
- Target 4-10 requirement items depending on task complexity
- Reference specific libraries, APIs, or patterns by name when applicable

### Step 7: Insert into ROADMAP.md

Insert the new action item into ROADMAP.md at the correct position:

- Place it after the task with the preceding item number (e.g., `2.5` goes after `2.4`)
- If inserting at the end of a phase (e.g., `2.5` when the last task is `2.4`), place it before the next phase heading
- If inserting between existing tasks (e.g., `2.5` between `2.4` and `2.6`), place it in numerical order
- Do NOT renumber existing tasks — the new ID fills a gap or extends the sequence
- Preserve all existing content and formatting in the roadmap

Use the `Edit` tool to insert the new task. Verify the insertion by reading back the modified section of ROADMAP.md.

### Step 8: Summary

After insertion, present a brief summary to the user:

- The task ID and title
- A one-line description of what was scoped
- The number of requirements defined
- Any notable trade-offs or decisions made during scoping

The task is now ready for `/do-task <id>`.
