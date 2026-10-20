# Codex Workspace Guide

## Overview
This directory contains Codex-specific operating guidance for this repository. Use it as the adapter layer for Codex, similar to how `.claude/CLAUDE.md` serves Claude.

The root `AGENTS.md` remains the repo-wide contract. This file explains how to use the `.cortex` structure when a task needs deeper workflow guidance.

---

## Development Workflow

Follow this workflow for feature development and non-trivial fixes:

```
spec -> plan -> build -> test -> review -> ship
```

| Phase | Command Guide | Purpose |
|-------|---------------|---------|
| Define | `commands/spec.md` | Capture scope, boundaries, and acceptance criteria |
| Plan | `commands/plan.md` | Break work into small vertical slices |
| Build | `commands/build.md` | Implement incrementally |
| Verify | `commands/test.md` | Prove behavior with tests and validation |
| Review | `commands/review.md` | Check correctness, readability, architecture, security, and performance |
| Ship | `commands/deploy.md` | Final deployment and verification guidance |

### Supporting Command Guides

| Guide | Purpose |
|-------|---------|
| `commands/debug.md` | Systematic diagnosis and root-cause analysis |
| `commands/simplify.md` | Reduce complexity without changing behavior |
| `commands/fix-issue.md` | Analyze and fix reported issues |

---

## Core Principles

### Code Quality
- Test first when practical, especially for bug fixes and behavior changes.
- Implement in small, reviewable increments.
- Review work across five axes: correctness, readability, architecture, security, and performance.

### Philosophy
- Progress over perfection
- Fix root causes, not symptoms
- Prefer the simplest change that fully solves the problem
- Tests are evidence, not decoration

---

## Rule Priority

Apply guidance in this order:

1. Direct user instructions
2. Root `AGENTS.md`
3. `.cortex/rules/*`
4. Existing repository patterns and code reality
5. `.cortex/references/*` and `.cortex/commands/*` as supporting material

All rules in `.cortex/rules/` should be treated as mandatory unless they clearly conflict with the actual repository stack or higher-priority instructions.

---

## Rules

Use `.cortex/rules/` as the main standards library:

### Code Quality
- `clean-code.md`
- `code-style.md`
- `error-handling.md`

### Architecture & Design
- `tech-stack.md`
- `system-design.md`
- `project-structure.md`
- `api-conventions.md`

### Data & Naming
- `naming-conventions.md`
- `database.md`

### Operations
- `security.md`
- `monitoring.md`
- `testing.md`
- `git-workflow.md`

When rules are generic or Node-oriented, adapt them to this repo's Python/FastAPI backend instead of copying them literally.

---

## Agents

Use the right guide from `.cortex/agents/` for the task:

### Development
- `backend.md`: APIs, services, repositories, database work
- `frontend.md`: UI, components, routing, state, rendering behavior
- `systems-architect.md`: architecture decisions and system boundaries

### Quality
- `code-reviewer.md`: structured review and findings
- `test-engineer.md`: test strategy and regression coverage
- `security-auditor.md`: threat modeling and security review
- `qa.md`: test plans, bug reproduction, and quality verification

### Product & Design
- `project-manager.md`: scope, milestones, and task shaping
- `ui-ux-designer.md`: UX, accessibility, and design direction
- `copywriter-seo.md`: copy and SEO guidance

---

## Skills

Use `.cortex/skills/` for reusable workflows:

- `tdd`
- `code-review`
- `incremental-implementation`
- `deploy`
- `security-review`
- linked shared skills such as `fastapi-templates`, `python-testing-patterns`, and `vercel-react-best-practices`

Prefer skills when the task matches a repeatable workflow instead of inventing a new process each time.

---

## References

Use `.cortex/references/` as checklists and quick reminders:

- `security-checklist.md`
- `testing-patterns.md`
- `performance-checklist.md`
- `accessibility-checklist.md`

References support decisions; they do not override the repo's actual code, tests, or root `AGENTS.md`.

---

## Behavior Guidelines

1. Follow the workflow for non-trivial work.
2. Apply root `AGENTS.md` first, then `.cortex/rules`.
3. Prefer small, verifiable changes.
4. Explain intent before substantial edits.
5. Use the most relevant agent, command guide, skill, or reference instead of mixing everything at once.
