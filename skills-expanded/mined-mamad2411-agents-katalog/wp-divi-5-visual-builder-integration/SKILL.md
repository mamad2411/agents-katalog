---
name: wp-divi-5-visual-builder-integration
description: Implements or repairs Divi 5 Visual Builder registration, edit components, settings UI, icons, placeholders, custom CSS fields, styles, data loading, and optional custom editor UI while preserving public-API discipline and frontend parity.
---

# wp-divi-5-visual-builder-integration

Use this skill when the task is primarily inside the Divi 5 editor rather than the WordPress plugin bootstrap or PHP renderer.

## Required Inputs

- Exact Divi version and extension package versions.
- Module metadata and attribute contract.
- Current editor entry points and registration.
- Required settings panels, conditional controls, icons, placeholders, and inline editing.
- Data sources and permission model.
- Expected frontend semantics and styles.
- Performance budget and test setup.

## Principles

- Keep the saved attribute contract independent from transient editor state.
- Use supported Divi packages and registration patterns.
- Avoid direct DOM mutation and undocumented global state.
- Make loading, empty, error, unauthorized, and selected states explicit.
- Cancel, deduplicate, or cache repeated requests where appropriate.
- Keep private data and secrets out of browser bundles.
- Preserve keyboard operation and meaningful control labels.
- Verify frontend parity after every editor-only change.

## Workflow

Use [`workflows/integrate-visual-builder-workflow.md`](workflows/integrate-visual-builder-workflow.md).

## Resource

Use [`resources/editor-integration-checklist.md`](resources/editor-integration-checklist.md).

## Completion Evidence

Record package versions, registration points, metadata changes, editor states, request behavior, accessibility checks, tests, production build, and frontend parity results.
