---
name: ios-clean
description: Remove GStack iOS debug bridge artifacts from an iOS app after live-device QA work is done.
---

# iOS Clean

Use this skill when the user wants to remove StateServer, DebugBridge, debug overlays, accessors, or GStack iOS QA wiring from an iOS project.

## Workflow

1. Inspect the project for GStack iOS artifacts:
   - Swift Package references
   - `StateServer.swift`
   - debug overlays
   - generated state accessors
   - `#if DEBUG` hooks
2. Build a removal plan with exact files and project settings.
3. Remove only generated/debug bridge artifacts.
4. Rebuild or run the available iOS tests.
5. Report what remains if any manual cleanup is needed.

## Guardrails

- Do not remove app-owned debug tools unless clearly installed by the GStack iOS QA flow.
- Do not edit project signing, bundle IDs, or production runtime code unnecessarily.
- Prefer XcodeBuildMCP or existing Apple build tools when available.
