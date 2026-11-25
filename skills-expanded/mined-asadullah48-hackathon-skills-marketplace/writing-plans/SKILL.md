---
name: writing-plans
description: Use when implementation is needed - creates detailed implementation plans assuming the engineer has zero context for the codebase
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context.

**Core principle:** Document everything needed to implement - files, code samples, testing approaches, exact commands.

## Plan Structure

### Header Section

Include:
- Goal and objectives
- Architecture overview
- Technology stack
- Dependencies

### Task Sections

Organize by component, each with:
1. Task name
2. Five-step substeps:
   - Write test (if applicable)
   - Verify failure
   - Implement
   - Verify pass
   - Commit

### File Listings

- Files to create
- Files to modify
- Files to test

## Task Granularity

Each task represents a single 2-5 minute action:
- Write test
- Verify failure
- Implement
- Verify pass
- Commit

**Keep tasks small and focused.**

## Plan Content Requirements

For each task:
- Exact file paths
- Complete code snippets
- Precise commands with expected outputs
- Git commit instructions

## Best Practices

- Follow DRY, YAGNI, TDD principles
- Include frequent commits
- Assume skilled but unfamiliar engineer
- Don't skip verification steps

## After Plan Creation

Offer two execution paths:

1. **Subagent-Driven:** Fresh subagent per task in current session
2. **Parallel Session:** Execute in new session using executing-plans skill

## Documentation

Save plans to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Red Flags - STOP

- Missing file paths
- Incomplete code snippets
- Skipping verification steps
- Assuming context the reader doesn't have
- Tasks too large (should be 2-5 minutes each)
