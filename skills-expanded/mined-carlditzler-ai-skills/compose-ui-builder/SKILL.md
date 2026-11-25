---
name: compose-ui-builder
description: Use for Android UI work that is primarily Jetpack Compose: screens, components, Material 3 polish, state ownership, adaptive layout, accessibility, and lifecycle-aware rendering in Kotlin codebases.
---

# Compose UI Builder

## Use when
- the task is mainly an Android Compose screen, component, form, flow, or UI-state change
- the repo is Compose-first or the changed surface is already implemented in Compose
- the job requires Material 3 decisions, state hoisting, or Compose-specific behavior

## Do not use when
- the affected surface is strictly Views/XML and there is no good reason to introduce Compose
- the task is mostly backend, data, or architecture work with minimal UI impact

## Working rules
- Respect the repo's actual UI stack before introducing new patterns.
- Keep composables focused on rendering state and user interaction.
- Use ViewModel-owned screen state for meaningful screens and collect streams with lifecycle awareness.
- Treat accessibility, adaptive layouts, edge-to-edge behavior, long text, and error states as baseline quality.
- Customize Material 3 with purpose; do not scatter one-off values through the tree.

## Workflow
1. Identify the primary user task, the key states, and the existing Compose patterns in the repo.
2. Choose the right state owner and rendering structure before editing.
3. Implement the smallest complete UI slice with loading, empty, success, error, and disabled states as needed.
4. Add or update targeted tests, previews, or equivalent repo-supported validation.
5. Validate recomposition-sensitive behavior, focus, IME, insets, and configuration resilience where relevant.

## Quality bar
- Clear primary action and information hierarchy.
- Stable state ownership and no duplicate sources of truth.
- No business logic or IO in composables.
- Layout survives font scaling, width changes, and realistic content.
- Accessibility semantics and touch targets are present by default.

## Reference routing
- Read `references/compose-docs.md` for Compose APIs and state guidance.
- Read `references/material3-checklist.md` for UI, theming, and Material 3 decisions.
- Read `references/release-quality-gates.md` when the surface is user-facing or release-critical.

## Output contract
Provide:
- files changed
- state and UI decisions made
- tests or validation added
- any real remaining risk
