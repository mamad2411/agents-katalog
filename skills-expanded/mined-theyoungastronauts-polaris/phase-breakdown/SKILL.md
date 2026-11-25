---
name: phase-breakdown
description: "Breaking an implementation plan into small, independently reviewable phases with parallel groups and sync points. Apply when structuring or sizing the phases of a plan."
---

# Skill: Phase Breakdown

## Purpose
Break a plan into executable phases, each suitable for a single git worktree, branch, and PR.

## Phase Structure

Each phase should include:

```markdown
## Phase N: [Descriptive Name]

### Objective
One sentence — what does "done" look like?

### Input
- What context/files/APIs does this phase need?
- Link to integration summary if cross-repo

### Tasks
1. [ ] Specific task with clear completion criteria
2. [ ] ...

### Output
- What artifacts does this phase produce?
- Any integration summary updates needed?

### Suggested Skills
- List relevant execution skills (e.g., django-patterns, nextjs-patterns)
- List relevant verification skill (e.g., verify-django)

### Branch
feature/[plan-name]-phase-N
(See the `/worktrees` skill for worktree setup)

### Verification Checklist
- [ ] All tasks completed
- [ ] Tests written and passing
- [ ] Linting clean
- [ ] Phase objective met
- [ ] Integration summary updated (if applicable)
```

## Guidelines

### Sizing
- Each phase should be reviewable in a single PR
- Target: 1-3 hours of focused Claude execution time
- If a phase feels too big, split it

### Ordering
- Dependencies flow forward — Phase N should not depend on Phase N+1
- Put foundational work (models, schemas, types) early
- Put integration/glue work late
- API contract definition should come before both backend implementation and frontend consumption

### Parallel Phases

Phases targeting different sub-projects with no cross-repo dependency can run in parallel.
Use a parallel group notation to mark these:

```markdown
## Parallel Group A (Phases 1-2)

### Phase 1: Backend — Models and API [server/]
...

### Phase 2: Frontend — Layout and Routing [web/]
...

## Sync Point: Integration Summary
Backend generates integration summary → frontend consumes it

## Parallel Group B (Phases 3-4)

### Phase 3: Backend — Business Logic [server/]
...

### Phase 4: Frontend — API Integration [web/]
Depends on: Integration summary from Phase 1
...
```

**Rules for parallel phases:**
- Phases in a parallel group target different sub-projects (different directories/repos)
- No phase in a group may depend on another phase in the same group
- Sync points between groups are where cross-repo handoff happens (integration summaries)
- The `[directory/]` suffix on phase names makes the target sub-project explicit

**When phases can NOT be parallel:**
- Frontend phase consumes an API defined in a backend phase in the same group
- Both phases modify shared configuration or documentation
- One phase's output is another phase's input

### Cross-Repo Phases
When a feature spans repos:
1. Phase for backend API + integration summary generation
2. Phase for frontend consumption (starts from integration summary)
3. Phase for integration testing (if applicable)

Never have a single phase spanning both repos — keep them separate and use the integration summary as the handoff.
