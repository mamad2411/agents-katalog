---
name: table-persistence-implementation
description: Implements or migrates MRT table view persistence into a generic useViewPersistence architecture on any Material React Table page.
category: General-Development
---

# Table Persistence Implementation

## When to use

Use this skill to implement or migrate MRT table view persistence into a generic System Memory / `useViewPersistence` architecture on any Material React Table page. This includes:

- switching from direct browser storage (`localStorage` / `sessionStorage`) to a shared persistence hook
- preserving global metadata and tab-specific metadata separately
- ensuring reset/clear behavior only affects the current active tab
- adding a drop-in DnD toolbar or table-level persistence UI when the page has tabbed or multi-view state
- creating a consistent Jira-ticket / PR description template for the feature
- announcing tests and verifying persistence behavior in code reviews

## What the skill owns

- identifying table page persistence state without assuming a single `localStorage` key
- recognizing the `useViewPersistence` / `useTablePersistence` hook pattern
- ensuring `handleReset()`/clear actions only clear the intended tab-scoped payload
- preserving shared global metadata separately from active-tab metadata
- advising on a generic `table-persistence-implementation` migration path across repo-specific table pages
- referencing Git-level validation when the migration spans multiple commits or file-focused persistence changes:
  - use [`git-commit-comparison-audit`](../git-commit-comparison-audit/SKILL.md) for full commit-level before/after comparison
  - use [`git-cross-ref-file-parity`](../git-cross-ref-file-parity/SKILL.md) to verify the same file change was preserved exactly

## Recommended structure

1. Audit the table page for browser storage usage and existing persistence keys.
2. Identify global metadata vs active-tab metadata and pin them to separate persistence keys.
3. Use a generic persistence hook such as `useViewPersistence` instead of ad hoc storage logic.
4. Update reset handlers so they clear only the current tab's persistence state.
5. Keep navigation/tabs metadata and page metadata separate for multi-tab views.
6. Document the migration and, when needed, create a Jira ticket / PR description covering the user-visible persistence behavior.
