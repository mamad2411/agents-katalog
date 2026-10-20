---
description: Workflow guidelines for starting and completing tasks
alwaysApply: true
---
# Workflow Guidelines

## First Step for Any Task

- Before starting work on any task, always check the `.cursor/rules` directory for relevant guidance
- These documents contain established workflows, conventions, and requirements for different aspects of the project
- Following these rule files will ensure consistency and reduce rework
- If multiple rule files seem relevant, review all of them before proceeding

## Last Step for Any Task

- If you've learned new concepts, workflows, or best practices during task completion, suggest updates to the relevant rules
- For new workflows that aren't covered by existing rules, suggest creating a new rule file
- Evaluate whether tests should be added for your changes:
  - For functional code, new features, API changes, or bug fixes, tests are essential
  - For content-only changes like documentation updates, tests are typically not required
- Always verify that no regressions are introduced by your changes
- Ensure documentation (README.md) is updated when adding or modifying services

## Available Rules

- [010-workflow.mdc](mdc:.cursor/rules/010-workflow.mdc) - Workflow guidelines
- [011-conventional-commits.mdc](mdc:.cursor/rules/011-conventional-commits.mdc) - Commit message format
- [012-minimal-code-changes.mdc](mdc:.cursor/rules/012-minimal-code-changes.mdc) - Minimal code changes principle
- [013-general-coding-principles.mdc](mdc:.cursor/rules/013-general-coding-principles.mdc) - General coding principles
- [020-codebase-structure.mdc](mdc:.cursor/rules/020-codebase-structure.mdc) - File organization
- [030-bug-handling.mdc](mdc:.cursor/rules/030-bug-handling.mdc) - Bug handling with TODO comments
- [040-python-style.mdc](mdc:.cursor/rules/040-python-style.mdc) - Python code style
- [050-docker-compose.mdc](mdc:.cursor/rules/050-docker-compose.mdc) - Docker Compose guidelines
- [060-shell-scripts.mdc](mdc:.cursor/rules/060-shell-scripts.mdc) - Shell script guidelines
- [070-best-practices.mdc](mdc:.cursor/rules/070-best-practices.mdc) - Best practices
- [080-common-tasks.mdc](mdc:.cursor/rules/080-common-tasks.mdc) - Common tasks
