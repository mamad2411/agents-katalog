---
name: lcs-task-slicer
description: Use this skill whenever the user asks to split a reviewed PRD into executable tasks. Trigger on "slice prd", "break down prd", "create tasks", or similar. Produce small, dependency-aware tracer-bullet vertical slices. Classify tasks into AFK (autonomous) or HITL (requires human input). Present the proposed breakdown to the user for feedback before writing tasks. Write each task into its own file task-###.md under .lcs/work-items/<timestamp>-<slug-work-item>/task/.
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Task Slicer Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Convert `prd-enhanced.md` (or `prd.md`) into individual executable task files (`task-001.md`, `task-002.md`, etc.) under `.lcs/work-items/<timestamp>-<slug-work-item>/task/`.
- Ensure tasks are small, dependency-aware, and session-friendly (<2 hours human time or one agent session).

Trigger
- Activate when user requests to "slice prd", "break down prd", "slice prd-enhanced.md", "create tasks", or similar.

Behavior Checklist

1. **Gather Context**:
   - Read `.lcs/state.md` to identify the active work-item directory: `.lcs/work-items/<timestamp>-<slug-work-item>/`. 
   - Read `prd-enhanced.md` (fallback to `prd.md` if enhanced version is missing).
   - Verify PRD has clear acceptance criteria and test strategy. If missing or weak, suggest running `lcs-prd-reviewer` first.

2. **Draft Tracer-Bullet Vertical Slices**:
   - Break the plan into **tracer bullet** tasks. Each task must be a thin vertical slice cutting through all integration layers end-to-end (schema, API, UI, tests), NOT a horizontal slice of one layer.
   - Slices should deliver a narrow but COMPLETE path that is demoable/verifiable.
   - Classify tasks into:
     - `AFK` (Away From Keyboard): Can be fully implemented and merged by autonomous agents.
     - `HITL` (Human In The Loop): Requires human interaction, architectural decisions, or design reviews. Prefer AFK over HITL.

3. **Quiz/Confirm with the User**:
   - Present the proposed breakdown to the user as a numbered list:
     - **Title**: Short descriptive name
     - **Type**: AFK / HITL
     - **Blocked by**: Which other tasks must complete first
     - **User stories covered**: Associated stories (if any)
   - Ask the user:
     - Does the granularity feel right (too coarse / too fine)?
     - Are the dependency relationships correct?
     - Should any slices be merged or split further?
     - Are the correct slices marked as HITL and AFK?
   - Iterate and refine based on feedback until the user approves.

4. **Create Task Files**:
   - Create the output directory: `.lcs/work-items/<timestamp>-<slug-work-item>/task/` if it does not exist.
   - Write each approved task into `.lcs/work-items/<timestamp>-<slug-work-item>/task/task-###.md` (sequential 3-digit number starting at `001`).

5. **Update State & Handoff**:
   - Update `.lcs/state.md` with:
     - `current_phase: tasks`
     - `timestamp: <current-ISO-timestamp>`
   - Output the structured task list summary.
   - End with a Handoff pointing to the next logical step (e.g. `lcs-task-executer` and `task-001.md`).

Prompt Templates
- Starter: "Slice prd-enhanced.md menjadi task-###.md"
- Slicing rule: "Prefer thin tracer-bullet vertical slices that take <2 hours or one agent session. Clearly partition AFK vs HITL slices."

Task File Structure
Each `task-###.md` must adhere to this exact structure:

```markdown
# TASK-###: <task-name>

* **Status**: pending
* **Type**: <AFK / HITL>
* **Depends on**: <TASK-### or None>
* **Priority**: <high/medium/low>
* **Scope**: <vertical slice behavior, avoiding extremely stale specific details unless from verified prototypes>
* **Files likely touched**:
  - <file-path-1>
  - <file-path-2>
* **Implementation notes**:
  - <step-by-step logic, API changes, or structures>
* **Acceptance criteria**:
  - [ ] <AC 1 (falsifiable)>
  - [ ] <AC 2 (falsifiable)>
* **Test plan**:
  - <Unit test spec or manual verification steps>

## Handoff
Next recommended skill: lcs-task-executer
Next file to read: .lcs/work-items/<timestamp>-<slug-work-item>/task/task-###.md
Current phase: tasks
Current confidence: high
Blocking questions: None
Risks to carry forward: <risks>
Suggested next command: Eksekusi task-###.md
```
