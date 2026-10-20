---
description: "SWYP Issue Quick-Create — instantly create an issue when a bug, blocker, or split task occurs during development"
---

<!-- AI-PROTECTED-FILE v1.0 -->
<!-- DO NOT MODIFY: Admin-only. Contact @Woo-JongHo for changes. -->

# SWYP Issue Quick-Create

Entry point for quickly creating a GitHub issue when something comes up during development.

## When to Use

- Discovered a **bug** while developing
- An unexpected **blocker** has occurred
- Found a **separate task** needed outside the current work
- Want to record **technical debt**

## Execution

Load and follow the workflow below:

@_wood/workflows/03-todo.md

**Entry hint:** When entering the workflow, select the "Create new issue" option.
Providing the currently active issue number and branch as context will create a linked issue.

## Quick Issue Type Selection

| Situation | Type Label |
|-----------|-----------|
| Bug found during feature development | `유형:버그` |
| New task derived from current work | `유형:작업` |
| New screen-level task | `유형:페이지` |
| Improvement to existing feature | `유형:개선` |
