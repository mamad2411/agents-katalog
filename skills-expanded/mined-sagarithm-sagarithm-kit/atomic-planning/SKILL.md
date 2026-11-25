---
id: "lifecycle.planning-and-task-breakdown"
name: "Atomic Planning & Task Breakdown"
version: "1.2.0"
domain: "lifecycle"
description: "Deconstructs complex specifications into hermetic, sequentially verifiable implementation slices. Enforces blast-radius containment and rollback checkpoints."
triggers:
  - "Decomposing a feature into implementation steps"
  - "Planning a multi-file refactoring or migration"
  - "User asks for a roadmap or implementation plan"
---

# 📋 Atomic Planning & Task Breakdown

> **"A plan is not a wishlist; it is a DAG (Directed Acyclic Graph) of verifiable transitions where every node leaves the codebase in a compilable, passing state."**

Large, unpartitioned code generations are the #1 cause of agentic failure. When an AI attempts to edit 15 files simultaneously, cognitive load exceeds context limits, syntax errors multiply, and recovery becomes impossible.

This skill mandates that all engineering tasks be broken down into **atomic, hermetic slices** that can be developed, tested, and verified independently.

---

## 🔬 The Anatomy of an Atomic Task Slice

Every task in a Sagarithm implementation plan must satisfy the **INVEST** principle:
1. **Independent**: Can be merged and executed without depending on unmerged future steps.
2. **Negotiable**: Has clear boundaries between mandatory core and optional enhancements.
3. **Valuable / Verifiable**: Leaves the codebase in a green, working, test-covered state.
4. **Estimable**: Clear scope of files touched (typically $\le 3$ files per slice).
5. **Small**: Can be reviewed and verified in a single mental pass.
6. **Testable**: Accompanied by dedicated automated test assertions.

---

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Architectural Reality | Mandatory Requirement |
|---|---|---|
| *"I will implement the entire feature in one giant edit."* | Monolithic edits blow past context limits and make git bisect/rollbacks impossible. | Break work into discrete, commits that pass tests independently. |
| *"Step 1 doesn't need tests; we will test everything at the end."* | Untested intermediate states hide compounding architectural errors. | Every intermediate task slice must compile and pass tests (`npm test`). |
| *"I'll create the schema, API, and UI all at once."* | Cross-cutting vertical spikes bypass contract validation and domain isolation. | Build inside-out: Domain Models -> Core Business Logic -> Public API -> UI. |
| *"The plan is self-evident; writing it down wastes tokens."* | Unrecorded plans cause agents to drift off-target mid-session. | Write the task plan to `.sagarithm/tasks.md` with explicit checkmarks before building. |

---

## 🔄 Task Execution Lifecycle

```
  [1. Task Selected] ──► [2. Red Test Written] ──► [3. Minimal Implementation]
                                                             │
                                                             ▼
                                                    [4. Green Verification]
                                                             │
                                                             ▼
                                                    [5. Git Checkpoint Commit]
```
