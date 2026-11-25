---
name: ui
description: Implements or refactors Flutter presentation layer using project design-system components and shared UI patterns. Use when building or updating feature screens and widgets.
argument-hint: "<screen-or-feature>"
---

# Implement Presentation Layer

Implement Flutter UI using the project's design system and shared screen-state patterns.

## Workflow

1. Confirm the screen or feature scope and identify the relevant existing UI patterns.
2. Reuse design-system components instead of raw `material` or `cupertino` widgets.
3. If local presentation state is needed, keep it in hooks.
4. Apply the project's shared loading and error patterns for the relevant scenario.
5. Keep user-facing text in the project's localization setup and resolve it in the presentation layer.
6. If shared UI is needed, place it in the app design system rather than `common`.
7. Before finishing, verify the work against the practical checklist in `reference.md` (alongside this skill).

## Guardrails

- Follow the existing project design system instead of introducing parallel UI primitives.
- Reuse the project's loading and error patterns instead of one-off screen-specific variants.
- Route state-management work to `flutter-bloc` and localization setup work to `flutter-localization`.
