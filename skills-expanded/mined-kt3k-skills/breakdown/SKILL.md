---
name: breakdown
description: |
  Break down a given task into subtasks with time estimates.
  Analyzes the codebase and task requirements to produce a structured plan
  with estimated effort for each step.
---

## Task Breakdown Skill

Given a task description (from the user or the current conversation context), perform the following:

1. **Understand the task**: Read relevant source files, configs, and documentation to fully understand the scope of the task.

2. **Identify subtasks**: Decompose the task into concrete, actionable subtasks. Each subtask should be:
   - Small enough to be completed in a single focused session
   - Independent where possible (minimize sequential dependencies)
   - Clearly scoped with a defined "done" state
   - Leaf nodes must be size **M or smaller**. If a leaf node would be L or XL, break it down further.

3. **Estimate effort**: For each subtask, assign a complexity size based on the scope of changes involved:
   - **XS**: Single location, obvious change — renaming, config tweak, one-line fix
   - **S**: A few locations in one file, well-understood — adding a field, writing a simple test
   - **M**: Multiple locations or files, some design decisions — new function, refactor a module, integration work
   - **L**: Cross-cutting across multiple modules, significant design decisions — new feature, major refactor
   - **XL**: New subsystem or architecture-level change, many unknowns — large migration, multi-file redesign

4. **Output format**: Present the breakdown as a tree structure that reflects the hierarchy and dependencies of the work:

   ```
   ## Task Breakdown: <task title>

   ## Specifications

   - <key requirement or behavior 1>
   - <key requirement or behavior 2>
   - <constraint or edge case>
   ...

   ## Subtasks

   - [ ] <high-level phase 1> [L]
     - [ ] <subtask 1.1> [S]
     - [ ] <subtask 1.2> [M]
       - [ ] <sub-subtask 1.2.1> [XS]
   - [ ] <high-level phase 2> [M]
     - [ ] <subtask 2.1> [S]
     - [ ] <subtask 2.2> [S]
   - [ ] <high-level phase 3> [S]

   ## Subtask Details

   ### 1. <high-level phase 1>
   <what this phase accomplishes and why>

   #### 1.1 <subtask 1.1>
   <what to do, which files/modules are involved, acceptance criteria>

   #### 1.2 <subtask 1.2>
   ...

   ### 2. <high-level phase 2>
   ...
   ```

   - Parent nodes represent phases or groups of related work; leaf nodes represent atomic tasks.
   - Estimates on parent nodes reflect the total effort of their children (not additional work).
   - Nesting depth should match the natural structure of the task

5. **Save option**: After presenting the breakdown, ask the user whether they want to save the plan as `plan.md` in the current working directory. If the user agrees, write the breakdown to `plan.md`.

### Guidelines

- If the task is unclear or underspecified, ask clarifying questions before producing the breakdown.
- Do NOT start implementing. This skill only produces the plan.
