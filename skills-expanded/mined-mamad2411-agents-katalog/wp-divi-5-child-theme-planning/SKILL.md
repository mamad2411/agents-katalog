---
name: wp-divi-5-child-theme-planning
description: Plans Divi 5 customization ownership and child-theme scope. Use when deciding whether work belongs in Divi native tools, Theme Builder, a child theme, a plugin, or an explicitly managed snippet solution.
---

# Divi 5 Child-Theme Planning

## Objective

Define the smallest defensible child-theme scope before implementation.

## Inputs

Collect:

- Exact Divi, WordPress, and PHP versions.
- Existing child theme, plugin, Theme Builder, Theme Options, and snippet customizations.
- Requirement, affected pages/templates, users, data, and environments.
- Whether behavior must survive a theme switch.
- Whether the work changes presentation, business behavior, storage, API access, scheduled tasks, or privileged actions.
- Update, rollback, ownership, and support constraints.

## Method

1. Describe the requirement without naming an implementation location.
2. Classify it as visual configuration, global visual template, theme-coupled presentation code, portable functionality, or operations.
3. Apply [customization-placement-matrix.md](resources/customization-placement-matrix.md).
4. Search existing project code and Divi configuration for an existing owner.
5. Prefer native Divi or a documented hook before a template copy.
6. Define files, interfaces, tests, owner, version baseline, and removal condition.
7. Identify data migration, security, accessibility, performance, and update risks.
8. Run [plan-divi-child-theme-workflow.md](workflows/plan-divi-child-theme-workflow.md) for a formal plan.

## Required Output

Produce:

- Placement decision and rejected alternatives.
- Exact compatibility baseline.
- Proposed child-theme file tree.
- Hook and template dependencies.
- Security and data-ownership notes.
- Test and rollback plan.
- List of existing customizations to consolidate or remove.

## Guardrails

- Do not create a child theme solely because custom code exists.
- Do not put portable functionality or durable data ownership in the theme.
- Do not recommend direct parent-theme edits.
- Do not copy templates without a source-version register.
- Do not present historical hook documentation as current proof without verification.
