---
name: QNEW
version: 1.0.0
description: Start new feature - understand best practices, follow them. Gathers requirements, analyzes codebase patterns, creates implementation plan, and snapshots requirements.lock.
trigger: QNEW
dependencies:
  agents:
    - planner
    - docs-writer
tools: []
claude_tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# QNEW - New Feature Initialization

## Purpose

Start a new feature by understanding existing codebase patterns and best practices, then creating a structured plan with locked requirements.

## Workflow

### 1. Gather Requirements
- Clarify user intent and acceptance criteria
- Identify similar features in codebase
- Extract non-functional requirements (performance, security, etc.)

### 2. Analyze Codebase Patterns
**Agent: planner**
- Search for similar implementations using Grep/Glob
- Identify naming conventions, file structure patterns
- Review existing types, interfaces, utilities
- Document patterns to follow for consistency

### 3. Create Implementation Plan
**Agent: planner**
- Break down feature into tasks
- Estimate story points (use Fibonacci scale for planning)
- Identify dependencies and risks
- Define interface contracts

### 4. Document Requirements
**Agent: docs-writer**
- Write `requirements/current.md` with REQ-IDs
- Include acceptance criteria per requirement
- Document assumptions and constraints
- List non-goals explicitly

### 5. Snapshot Requirements Lock
- Copy `requirements/current.md` → `requirements/requirements.lock.md`
- Lock prevents scope creep during implementation
- Tests will reference REQ-IDs from lock file

## Output Format

```markdown
# Feature: [Name]

## Requirements Analysis
- Found X similar patterns in codebase
- Key conventions: [list]
- Reusable components: [list]

## Implementation Plan
**Total Estimate: [X] SP**

### Task 1: [Name] ([Y] SP)
- REQ-ID references
- Acceptance criteria
- Dependencies

### Task 2: [Name] ([Z] SP)
...

## Requirements Lock
Created: requirements/requirements.lock.md
```

## Success Criteria

- requirements/current.md exists with clear REQ-IDs
- requirements/requirements.lock.md created
- Implementation plan with SP estimates
- Codebase patterns identified and documented
- No coding started yet (planning phase only)

## Related Skills

- **QPLAN**: For detailed implementation planning after QNEW
- **QCODET**: Write tests referencing REQ-IDs from lock file
- **QDOC**: Update documentation after implementation
