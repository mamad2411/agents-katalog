---
name: rp-new-project
description: Initialize a new project or new section with the RepoPlanner planning structure. Use this skill when the user wants to start a new project, set up planning docs for a repo that doesn't have them yet, add a new section to a monorepo, or scaffold requirements/roadmap/state/task-registry. Creates the full .planning/ structure and 5-doc loop, asks the right questions about scope and goals, generates requirements with stable IDs, and produces a phased roadmap. Works for simple repos and monorepos.
---

# New Project Init

Sets up the full RepoPlanner planning structure for a new project or new monorepo section. The goal is a system where both agents and humans always know exactly what to work on next.

## Before starting

Check if a planning structure already exists:

```bash
ls .planning/ 2>/dev/null && echo "EXISTS" || echo "NEW"
```

If `.planning/` already exists, use the existing structure instead of overwriting — run `repo-planner` skill to read the current state.

If the user has an existing codebase with no planning docs, offer to map the codebase first:
- "I see existing code without planning docs. Want me to map the architecture before we define requirements?"

## Step 1: Gather project context

Ask these questions (inline, conversational — not a form):

1. **What are you building?** Wait for their response, then follow threads.
2. **Who is it for?** (end users, internal teams, operators)
3. **What's the single most important thing it must do?** (the core value)
4. **What's explicitly not in scope for the first version?**
5. **What tech stack?** (framework, database, deployment — or "I'll figure that out")
6. **Is this greenfield or does existing code exist?**

For each answer, ask one follow-up that digs deeper. Don't rush to requirements until you understand what they're building and why.

When you have enough to write a PROJECT.md, ask: "I think I have a clear picture. Ready to create the planning docs?"

## Step 2: Create PROJECT.md

Write `.planning/PROJECT.md`:

```markdown
# <Project Name>

## What we're building

[One paragraph: what it is, who it's for, why it exists]

## Core value

[The single thing that must work for this to be worth shipping]

## Tech stack

[Framework, database, deployment — or TBD]

## Constraints

[Timeline, budget, team, or technical constraints that shape decisions]

## Out of scope (v1)

- [Exclusion 1] — why
- [Exclusion 2] — why

## Key decisions

| Decision | Rationale |
|----------|-----------|
| [Any choices already made] | [Why] |

---
*Last updated: [date] after initialization*
```

## Step 3: Define requirements

Group capabilities by category. For each category, identify:
- **Must have (v1)** — product fails without this
- **Should have (v1)** — strong user expectation
- **Defer (v2+)** — nice-to-have, explicit deferral

Requirement quality:
- Specific and testable: "User can reset password via email link" (not "handle password reset")
- User-centric: "User can X" (not "System does Y")
- Atomic: one capability per requirement

REQ-ID format: `<CATEGORY>-<NUMBER>` (e.g. `AUTH-01`, `CONTENT-02`)

Write `.planning/REQUIREMENTS.md`:

```markdown
# Requirements

## v1 Requirements

### <Category 1>
- [ ] **<CAT>-01**: [User-centric requirement]
- [ ] **<CAT>-02**: [User-centric requirement]

### <Category 2>
- [ ] **<CAT2>-01**: [User-centric requirement]

## v2 (Deferred)

| Id | Requirement | Why deferred |
|----|-------------|--------------|
| `<CAT>-10` | [Requirement] | [Reason] |

## Out of scope

| Exclusion | Reason |
|-----------|--------|
| [Thing] | [Why it's excluded] |
```

Show the full requirements list and ask: "Does this capture what you're building? Anything to adjust?"

## Step 4: Create the roadmap

Derive phases from requirements — don't impose a framework. Each phase should:
- Be independently shippable
- Map to 2–8 requirements
- Have a clear goal someone can verify
- Have 2–5 observable success criteria

Write `.planning/ROADMAP.md`:

```markdown
# Roadmap

## Overview

| # | Phase | Goal | Requirements | Status |
|---|-------|------|--------------|--------|
| 1 | [Name] | [Goal] | <CAT>-01, <CAT>-02 | `planned` |
| 2 | [Name] | [Goal] | <CAT>-03, <CAT2>-01 | `planned` |

## Phase 1: <Name>

**Goal:** [One sentence goal]

**Requirements:** <CAT>-01, <CAT>-02

**Success criteria:**
1. [Observable user behavior that shows this works]
2. [Observable user behavior]
3. [Observable user behavior]

## Phase 2: <Name>

...
```

Coverage check: every v1 requirement must appear in exactly one phase.

## Step 5: Initialize state and task registry

Write `.planning/STATE.md`:

```markdown
# State

| Field | Value |
|-------|-------|
| `status` | `planning` |
| `updated` | [date] |

## Current cycle

| Field | Value |
|-------|-------|
| `phase` | Phase 1 planned — kickoff next |
| `focus` | define approach and tasks for Phase 1 before starting execution |
| `constraint` | — |

## Next queue

| Priority | Action | Type |
|----------|--------|------|
| `1` | run `rp-plan-phase` for Phase 1 to create KICKOFF.md and task list | `planning` |
```

Write `.planning/TASK-REGISTRY.md` (empty header):

```markdown
# Task Registry

*(Tasks will be added as phases are planned — run `rp-plan-phase` to start)*
```

## Step 6: Create supporting files

Write `.planning/DECISIONS.md` (empty with template):

```markdown
# Decisions

*(Stable decisions will be added as they emerge during planning and execution)*
```

Write `.planning/ERRORS-AND-ATTEMPTS.md`:

```markdown
# Errors and Attempts

*(Failed approaches will be recorded here to prevent repeating them)*
```

Write `planning-config.toml` (minimal):

```toml
[project]
name = "<project-name>"
created = "<date>"
namespace = "<namespace>"  # used as prefix for all phase IDs
```

## Step 7: Commit and show next steps

```bash
git add .planning/
git commit -m "docs: initialize planning structure"
```

Present the summary:

```
Planning initialized.

| File | Purpose |
|------|---------|
| .planning/PROJECT.md | project context |
| .planning/REQUIREMENTS.md | [N] v1 requirements |
| .planning/ROADMAP.md | [N] phases |
| .planning/STATE.md | current cycle |
| .planning/TASK-REGISTRY.md | tasks (empty — fill via plan-phase) |

Next: run rp-plan-phase for Phase 1 to create a KICKOFF and task list.
```

## For monorepos: adding a section

If adding a new section to an existing monorepo, create the MDX structure instead:

```
docs/<section>/
  requirements.mdx
  planning/
    planning-docs.mdx
    roadmap.mdx
    state.mdx
    task-registry.mdx
    decisions.mdx
    errors-and-attempts.mdx
```

Use the same section name as the namespace for all phase IDs (`<section>-<stream>-<phase>`). Read `repo-planner/references/monorepo-setup.md` for cross-section conventions.
