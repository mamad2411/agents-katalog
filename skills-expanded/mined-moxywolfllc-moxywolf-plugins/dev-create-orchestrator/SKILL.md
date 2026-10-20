---
name: dev-create-orchestrator
description: "Orchestrates complete code creation workflows using GSD/Ralph Loop pattern. Coordinates design, architecture, implementation, documentation, and testing skills in sequence. Use when: (1) creating new applications from scratch, (2) building new features, (3) starting development projects, (4) user says 'build me an app' or 'create new project'. Triggers: '/gsd init code-project', 'create new app', 'build new feature', 'start development'."
---

# Dev Create Orchestrator

Coordinates multiple development skills through 5 phases to create production-ready code using GSD + Ralph Loop pattern.

## Workflow Overview

```
Phase 1: Requirements & Design
  └─> screenshot-to-code, color-palette-extractor, canvas-design

Phase 2: Architecture
  └─> database-schema-designer, mcp-builder

Phase 3: Implementation
  └─> artifacts-builder, screenshot-to-code

Phase 4: Documentation
  └─> api-documentation-writer, technical-writer

Phase 5: Testing & QA
  └─> webapp-testing, code-review-pro
```

## Execution Protocol

### 1. Initialize Project

```bash
/gsd init code-project [project-name]
```

Creates project structure with ROADMAP.md containing all 5 phases.

### 2. For Each Phase

```bash
/gsd discuss-phase [N]   # Gather requirements, identify skippable tasks
/gsd plan-phase [N]      # Create PLAN.md with task breakdown
/gsd execute-phase [N]   # Run Ralph Loop on each task
/gsd verify-phase [N]    # UAT checklist verification
```

### 3. Phase Discussion Questions

**Phase 1 (Design):**
- Do you have UI mockups? → Skip task 1.1 if code-only
- Have existing brand guidelines? → Skip task 1.2
- Need visual assets created? → Skip task 1.3 if existing

**Phase 2 (Architecture):**
- Need persistent data? → Skip task 2.1 if no database
- External API integrations? → Skip task 2.2 if none

**Phase 3-5:** Proceed based on Phase 1-2 outputs.

## Task Execution

Each task follows Ralph Loop pattern:

1. Load bounded context (~3500 tokens max)
2. Execute skill with completion promise
3. Write handoff JSON for next task
4. Check promise met → advance or iterate

**For detailed task definitions:** See `references/phase-tasks.md`

**For completion promises:** See `references/completion-promises.md`

## PLAN.md Task Format

```yaml
- id: "1.1"
  name: "Extract UI Requirements"
  skill: "screenshot-to-code"
  input_source:
    type: "user_input"
    description: "UI mockups or descriptions"
  max_iterations: 3
  completion_promise: "UI_SPECS_COMPLETE"
  verification_criteria:
    - Component hierarchy documented
    - Layout structure defined
```

## Output Structure

```
project-[name]/
├── phases/phase-[N]/PLAN.md, UAT.md, SUMMARY.md
├── handoffs/phase-[N]/task-[X.Y]-iter-[Z].json
└── outputs/
    ├── app/          # Built application
    ├── docs/         # Documentation
    └── tests/        # Test suites
```

## Skill Routing

When these patterns appear, route to this orchestrator:

- "create.*app", "build.*application"
- "new.*project", "start.*development"
- "code.*from scratch"
- `/gsd init code-project`
