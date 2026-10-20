---
name: task-master-planner
description: "Interactive Taskmaster planning protocol that produces 70–80+ granular tasks, organized into phases/waves/swarms, with verification gates and GitHub issue synchronization (including dispatch-friendly orchestration). USE WHEN turning a spec or architecture doc into a schema-complete, GitHub-synced task plan you can hand to an orchestrator; ships JSON blueprints and a context-collection + plan-generation script set."
origin: community
cluster: ai-agents-meta
version: 1.0.0
---

# Task Master Planner

Use this skill to design execution-ready engineering plans from specs, architecture docs, and repo context.

This is not a lightweight checklist generator. It is a full orchestration workflow.

---

## 1) Session Start: Interactive Discovery (Mandatory)

Before generating tasks, run a short discovery dialogue to lock planning depth and delivery constraints.

Capture at minimum:
- Planning depth: **lean / standard / deeply detailed**
- Delivery mode: prototype, production, or hardening
- CI/CD expectations: none / basic / production-grade
- Release model: single milestone or phased rollout
- Quality bar: testing depth, observability, performance, security requirements
- Team topology: solo / small squad / multi-squad
- External constraints: deadline, compliance, platform constraints

Do not skip discovery unless all values are explicitly provided in the request.

---

## 2) Inputs to Load

Load all available planning context, prioritizing:
- `DesignSpec.md`
- `ProjectArchitecture.md`
- `.context/architecture/overview.md`
- `.context/architecture/patterns.md`
- `.context/auth/overview.md`
- `.context/testing.md`
- `.context/workflows.md`
- `.context/errors.md`
- `.context/api/headers.md`
- `.context/feature-flags.md`
- `.context/performance.md`
- `.context/monitoring.md`
- `.context/ui/patterns.md`

If user asks to process all context docs, enumerate and include all `.context/**` files relevant to requirements and constraints.

---

## 3) Plan Size and Structure Rules

### Minimum granularity
- Minimum total tasks: **70**
- Default target: **80 tasks**
- Expand beyond 80 for large scope; never compress by hiding complexity

### Required hierarchy
- Top-level: **Phases**
- **Phase 1 must be split into multiple Waves**
- Each Wave must include **multiple Swarms** (parallel work clusters)
- Swarms should be dependency-aware and independently executable where possible

### Dependency discipline
- Define explicit dependencies across tasks
- Preserve execution order where needed (schema → API → UI, auth → protected routes, etc.)
- Maximize parallelism only when dependencies permit

---

## 4) Required Task Schema (Per Task)

Each task must include:
- `id` (stable string)
- `title` (short, action-oriented)
- `area` (`frontend` | `backend` | `data` | `infra` | `qa` | `product`)
- `owner_role` (e.g., Frontend Eng, Backend Eng, DevOps, QA)
- `est_hours` (numeric)
- `dependencies` (array of task IDs)
- `deliverable` (one sentence)
- `acceptance` (testable one sentence)
- `validation` (how completion is proven: tests/logs/metrics/checks)

Recommended effort range: **4–16 hours** for most tasks.

---

## 5) Orchestration Policy (Enforced)

### A. Plan-node default
- Any non-trivial work (3+ steps or architecture decisions) starts in planning mode
- If execution drifts or fails, stop and re-plan
- Include verification work in plan scope, not just build work

### B. Parallel/swarm strategy
- Use independent swarms for independent tracks
- One tactical focus per swarm (avoid mixed-goal swarms)
- Keep cross-swarm dependency contracts explicit

### C. Verification before done
- Never mark done without evidence
- Require concrete proof: tests, logs, status checks, metrics, or diff validation

### D. Elegance gate (balanced)
- For non-trivial changes, challenge the design for cleaner alternatives
- Replace brittle hacks with robust solutions when justified
- Avoid over-engineering simple fixes

### E. Autonomous bug-fix behavior
- For bug reports: diagnose from failing evidence, fix root cause, verify, then close

---

## 6) GitHub Issue Synchronization + Dispatch Compatibility

When task planning completes (or when waves advance):
- Create/update GitHub issues mapped to phase/wave/swarm and task IDs
- Preserve task dependencies in issue relationships/comments/checklists
- Update issue states as execution progresses

When dispatch-based orchestration is requested:
- Use dispatch-compatible flows to create/update issue batches
- Confirm repo scope and branch/reference context before dispatch
- Post concise completion summaries back to linked issues/PRs

---

## 7) Planning Artifacts

Maintain these artifacts throughout planning/execution:
- `tasks/todo.md` → checklist grouped by Phase → Wave → Swarm
- `tasks/lessons.md` → user-correction-derived guardrails to prevent repeat mistakes

Execution tracking protocol:
1. Write plan checklist first
2. Confirm/align with user
3. Mark items complete progressively
4. Summarize milestone progress
5. Add wave-level review notes
6. Persist lessons from feedback

---

## 8) Output Contract

When presenting a Taskmaster plan, include in order:
1. Discovery summary
2. Assumptions and constraints
3. Phase map
4. Detailed Phase 1 Wave/Swarm layout
5. Full task list (70–80+)
6. Dependency rationale
7. Verification strategy
8. GitHub sync + dispatch strategy
9. Risks and fallback plan

---

## 9) Mini Cookbook References

Use these quick recipes when available in the active runtime:
- `dispatching-parallel-agents` for swarm-level parallelization
- `using-superpowers` for skill-selection discipline before action
- GitHub issue/PR workflow recipes for synchronization and status transitions

---

## 10) Definition of Done

A Taskmaster plan is done only when:
- discovery is complete,
- structure includes phases/waves/swarms,
- tasks are 70–80+ and schema-complete,
- dependencies are coherent,
- verification strategy is explicit,
- and GitHub synchronization approach is defined.
