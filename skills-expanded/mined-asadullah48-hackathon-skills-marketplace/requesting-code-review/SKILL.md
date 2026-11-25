---
name: requesting-code-review
description: Use when code review is needed - after each task in subagent-driven development, before merging to main, or after completing major features
---

# Requesting Code Review

## Overview

Code review should happen systematically throughout development.

**Core principle:** Review after each task in subagent-driven development, before merging, and after major features.

## When to Request Review

1. **After each task** in subagent-driven development
2. **Before merging** to main branch
3. **After completing** major features
4. **When uncertain** about implementation approach

## The Process

### Step 1: Get Commit Hashes

Identify the commits or changes to be reviewed.

### Step 2: Dispatch Code Reviewer

Use the code-reviewer subagent with:
- Commit range or diff
- Specific focus areas if needed
- Context about the task

### Step 3: Address Feedback

Respond to feedback based on severity:

- **Critical:** Fix immediately
- **Important:** Resolve before proceeding
- **Minor:** Note for later

## Integration Points

- **Subagent-driven development:** Review after each task implementation
- **Plan execution:** Review between batches or after completion
- **Ad-hoc features:** Review before committing

## Common Mistakes

- Skipping reviews for "simple" changes
- Waiting too long to request review
- Not addressing critical feedback
- Batching too many changes for review

## Red Flags - STOP

- "This change is simple, skip review"
- "I'll request review later"
- Ignoring critical feedback without justification
