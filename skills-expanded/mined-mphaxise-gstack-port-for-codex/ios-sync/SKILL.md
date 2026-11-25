---
name: ios-sync
description: Refresh GStack iOS debug bridge artifacts against upstream templates or local app state.
---

# iOS Sync

Use this skill when the user asks to regenerate or refresh iOS QA/debug bridge support.

## Workflow

1. Identify existing debug bridge files and package references.
2. Compare them against upstream templates or current app structure.
3. Regenerate or update only bridge-owned files:
   - StateServer
   - DebugOverlay
   - package wiring
   - generated state accessors
4. Build the app and verify that bridge support still launches.
5. Report any app code that needs manual annotation or accessors.

## Guardrails

- Do not overwrite hand-written app code with generated bridge code.
- Do not leave debug bridge hooks enabled for production builds.
- Preserve signing and deployment settings.
