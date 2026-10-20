---
name: dev-review-orchestrator
description: "Orchestrates complete code review workflows using GSD/Ralph Loop pattern. Coordinates code analysis, documentation audit, architecture review, testing, and UI/UX validation in sequence. Use when: (1) analyzing existing codebases, (2) security audits, (3) code quality reviews, (4) user says 'review my code' or 'audit this project'. Triggers: '/gsd init code-review', 'review this code', 'audit codebase', 'security audit', 'analyze existing code'."
---

# Dev Review Orchestrator

Coordinates multiple development skills through 5 phases to thoroughly analyze and improve existing codebases using GSD + Ralph Loop pattern.

## Workflow Overview

```
Phase 1: Code Analysis
  └─> code-review-pro, regex-visual-debugger

Phase 2: Documentation Audit
  └─> technical-writer, api-documentation-writer

Phase 3: Architecture Review
  └─> database-schema-designer, technical-writer

Phase 4: Testing & Validation
  └─> webapp-testing

Phase 5: UI/UX Review
  └─> color-palette-extractor, screenshot-to-code
```

## Execution Protocol

### 1. Initialize Review

```bash
/gsd init code-review [project-name]
```

Creates review project structure with ROADMAP.md containing all 5 phases.

### 2. For Each Phase

```bash
/gsd discuss-phase [N]   # Determine review focus, skip irrelevant phases
/gsd plan-phase [N]      # Create PLAN.md with task breakdown
/gsd execute-phase [N]   # Run Ralph Loop on each task
/gsd verify-phase [N]    # UAT checklist verification
```

### 3. Focus-Based Phase Selection

**Security-focused:** Phase 1 (tasks 1.1, 1.2) only
**Documentation-focused:** Phase 2 only
**Performance-focused:** Phase 1 (task 1.2) + Phase 3
**Pre-launch (comprehensive):** All phases

### 4. Phase Discussion Questions

**Phase 1 (Code Analysis):**
- Primary concern? → Security / Performance / Quality / All
- Analysis depth? → Quick scan / Standard / Deep audit

**Phase 2 (Documentation):**
- Current doc state? → Minimal / Outdated / Incomplete / Good
- Target audience? → Developers / API consumers / End users / All

**Phase 3 (Architecture):**
- Database technology? → PostgreSQL / MySQL / MongoDB / Other
- Known architecture concerns? → Yes (describe) / General review

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
  name: "Security Analysis"
  skill: "code-review-pro"
  input_source:
    type: "file"
    location: "/path/to/codebase"
  max_iterations: 4
  completion_promise: "SECURITY_ANALYSIS_COMPLETE"
  verification_criteria:
    - SQL injection vulnerabilities checked
    - XSS vulnerabilities checked
```

## Output Structure

```
project-[name]-review/
├── phases/phase-[N]/PLAN.md, UAT.md, SUMMARY.md
├── handoffs/phase-[N]/task-[X.Y]-iter-[Z].json
└── outputs/
    ├── reports/        # Analysis reports
    ├── docs/           # Generated documentation
    ├── tests/          # Generated tests
    └── recommendations/# Fix guides
```

## Skill Routing

When these patterns appear, route to this orchestrator:

- "review.*code", "audit.*codebase"
- "security.*audit", "analyze.*existing"
- "improve.*project", "check.*quality"
- `/gsd init code-review`
