---
name: task-generation-mode
description: Generates tasks by analyzing the PRD and breaking it into actionable work items.
---

## Context

- Current branch: `git branch --show-current`
- Current git status: `git status --short`
- Project AGENTS.md: `cat AGENTS.md 2>/dev/null | head -50`

**Description:** Assistant instructions for converting a Product Requirements Document (PRD) into a structured, actionable implementation task list for developers.

---

### **Guardrails**

- Convert ambiguity into explicit assumptions, open questions, or user checkpoints.
- Prefer the smallest task breakdown that can deliver the PRD. Do not add speculative features, abstractions, or future-proofing.
- Every task should have a verifiable outcome: a test, command, review step, or observable behavior.
- Mark out-of-scope work explicitly instead of silently including it.

---

### **Required Companion Skill**

Use `/interrogate-me` before finalizing the task list. Let it stress-test the PRD, assumptions, dependencies, sequencing, risks, and implementation boundaries one question at a time. Incorporate the resulting assumptions, decisions, risks, and unresolved issues into parent tasks, sub-tasks, Relevant Files, Notes, and checkpoint prompts.

---

### **The Two-Phase Process**

#### **Phase 1: Parent Tasks (High-Level)**

1. **Analyze PRD:** Read functional requirements, user stories, and technical constraints.
2. **Generate Roadmap:** Identify the fewest high-level parent tasks that cover the PRD, usually 3-6.
3. **Checkpoint:** Present these parent tasks to the user and wait for approval.

- _Required Message:_ "I have generated the high-level tasks based on the PRD. Ready to generate the sub-tasks? Respond with 'Go' to proceed."

#### **Phase 2: Sub-Tasks & Finalization**

1. **Breakdown:** Once "Go" is received, expand each parent task into granular, actionable sub-tasks.
2. **Mapping:** Identify all files to be created or modified, including unit tests.
3. **Documentation:** Compile the final Markdown file.

---

### **Output Specification**

- **Format:** Markdown (`.md`)
- **Path:** `.planning/tasks/tasks-[prd-file-name].md`
- **Structure:**
  - **Task List:** Hierarchical checkboxes (`- [ ] 1.0 ...`, `- [ ] 1.1 ...`).
  - **Relevant Files:** Potential code and test files involved.
  - **Notes:** Testing commands and architectural reminders tied to the PRD.

---

### **Developer Guidelines**

- **Test Placement:** Unit tests must be co-located with their respective source files (e.g., `feature.ts` and `feature.test.ts`).
- **Context:** Use `codebase` and `usages` to ensure task descriptions align with existing patterns in the repository.

---

### **Example Task Entry**

```markdown
- [ ] 1.0 Data Model Implementation
  - [ ] 1.1 Define Zod schema for [Entity]
  - [ ] 1.2 Create Prisma migration for [Table Name]
  - [ ] 1.3 Implement repository pattern for CRUD operations
```

**Ask the user whether each task or subtask should be committed to git, and keep the work sequential.**

---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill task-generation-mode``
