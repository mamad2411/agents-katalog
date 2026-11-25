# TDD Workflow Orchestration

This skill orchestrates full-cycle TDD development by integrating multiple specialized plugins into a cohesive workflow.

## When to Use This Skill

Use this skill when the user wants to:
- Develop a feature "from scratch to production"
- Follow strict TDD methodology (Red-Green-Refactor)
- Get help with the complete development cycle
- Orchestrate multiple development tools automatically
- Create a development plan with test cases

**Trigger phrases:**
- "Develop feature X end-to-end"
- "Full TDD cycle for..."
- "Create complete implementation of..."
- "Help me build X from start to finish"
- "Plan and implement..."

## Core Principles

### 1. Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────┐
│                    TDD CYCLE                            │
│                                                         │
│   ┌─────────┐    ┌─────────┐    ┌───────────┐          │
│   │   RED   │───▶│  GREEN  │───▶│ REFACTOR  │──┐       │
│   │  Write  │    │  Make   │    │  Improve  │  │       │
│   │  Failing│    │  Test   │    │  Code     │  │       │
│   │  Test   │    │  Pass   │    │  Quality  │  │       │
│   └─────────┘    └─────────┘    └───────────┘  │       │
│        ▲                                        │       │
│        └────────────────────────────────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. Three-Phase Orchestration

| Phase | Agent | Model | Purpose |
|-------|-------|-------|---------|
| **Explore** | codebase-explorer | sonnet | Fast module discovery |
| **Plan** | planning-agent | opus | Deep analysis, user questions |
| **Execute** | execution-agent | opus | TDD implementation |

### 3. Plugin Integration

This workflow integrates with existing plugins:

- **pytest-assistant** — Creating failing tests first (Red phase)
- **clean-code** — Code review and refactoring suggestions
- **ruff-lint** — Auto-formatting via hooks
- **python-typing** — Type checking via hooks
- **software-architect** — Architecture decisions during planning

## Workflow Overview

```
User Prompt
    │
    ▼
┌─────────────────┐
│ Codebase        │  Find relevant modules
│ Explorer        │  Understand project structure
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Planning        │  Ask clarifying questions
│ Agent           │  Create development plan
└────────┬────────┘  Define test cases
         │
         ▼
┌─────────────────┐
│ EnterPlanMode   │  User reviews and approves
│ (Claude Code)   │  the development plan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execution       │  TDD cycle for each test
│ Agent           │  Quality gates
└────────┬────────┘  Documentation
         │
         ▼
    Completed Feature
```

## Memory Anchors

Plans include Memory Anchors — structured context that persists across sessions:

```yaml
---
id: dev-{uuid}
feature: {name}
status: draft | approved | in_progress | completed
---
```

Anchors capture:
- **TASK**: The end goal
- **APPROACH**: Chosen implementation strategy
- **CONSTRAINTS**: Technical limitations

## Explicit Phase Separation

Each TDD phase should be tracked explicitly. Use TaskCreate to make phase transitions visible:

```
TaskCreate: "RED — Write failing test for <feature>"
  → Write test, verify it fails
  → TaskUpdate: completed

TaskCreate: "GREEN — Minimal implementation for <feature>"
  → Write just enough code to pass
  → TaskUpdate: completed

TaskCreate: "REFACTOR — Clean up <feature> implementation"
  → Improve code quality, tests stay green
  → TaskUpdate: completed
```

**Why:** Without explicit separation, phases blur together. Developers skip Red (writing tests after code) or skip Refactor (moving on too quickly). Tracking forces discipline.

## References

- [Plan Format](references/plan-format.md) — Development plan structure
- [Context Handoff](references/context-handoff.md) — How context flows between agents
- [Plugin Integration](references/plugin-integration.md) — How plugins work together
