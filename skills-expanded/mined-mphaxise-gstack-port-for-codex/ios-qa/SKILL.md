---
name: ios-qa
description: Perform structured QA for an iOS app using simulator or real-device tooling available to Codex.
---

# iOS QA

Use this skill when the user asks to QA a SwiftUI or iOS app.

## Workflow

1. Discover project, workspace, scheme, and target device/simulator.
2. Build and launch the app using XcodeBuildMCP or local Xcode tooling.
3. Map the major screens and user flows from source and UI evidence.
4. Exercise flows:
   - launch
   - navigation
   - forms
   - permissions
   - empty/error/loading states
   - orientation or size changes when relevant
5. Record findings with reproduction steps, severity, and screenshots when possible.
6. If the user asked for fixes, hand off to `ios-fix`.

## Guardrails

- Distinguish simulator QA from real-device QA.
- Do not claim hardware-specific coverage without a physical device run.
- Keep QA report-only when the user asks for no fixes.
