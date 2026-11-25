---
name: subagent-driven-development
description: Use when executing implementation plans - dispatches fresh subagent per task with two-stage review process (spec compliance then code quality)
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching independent subagents for each task, with a two-stage review process.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) ensures quality and speed.

## The Process

### Step 1: Extract Tasks

Load plan file and extract all tasks into TodoWrite tracker.

### Step 2: For Each Task

1. **Implementation**: Dispatch an implementer subagent who:
   - Codes the solution
   - Tests the implementation
   - Self-reviews

2. **Spec Review**: A separate subagent verifies:
   - Code matches requirements
   - All acceptance criteria met
   - No over/under-building

3. **Quality Review**: Another subagent assesses:
   - Code quality
   - Best practices
   - Maintainability

4. **Iterations**: If either review identifies gaps:
   - Implementer fixes issues
   - Both reviewers re-check

## Key Principles

- **Fresh subagent per task** - prevents context pollution
- **Two-stage review** - spec compliance before code quality
- **Same session** - eliminates context switching
- **Surface questions early** - before implementation begins

## Critical Safeguards

- Never skip reviews
- Never accept "close enough" on spec compliance
- Spec compliance must be verified BEFORE code quality review
- Order matters: spec then quality

## Why This Approach

**Rather than:**
- Manual execution (slow, error-prone)
- Parallel sessions (context loss)

**This provides:**
- Parallelization via independent task execution
- Fresh context per task
- Systematic verification at each stage

## Common Mistakes

- Skipping spec review
- Reviewing quality before spec compliance
- Using same subagent for implementation and review
- Batching multiple tasks without per-task review

## Red Flags - STOP

- "This task is simple, skip review"
- "Quality review first, spec later"
- Same subagent does implementation and review
- "Close enough" on requirements
