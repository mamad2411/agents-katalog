---
name: ios-fix
description: Fix an iOS bug found during QA, rebuild, redeploy or rerun, and verify the behavior.
---

# iOS Fix

Use this skill when the user asks to fix an iOS issue found by `ios-qa`, tests, screenshots, or device exploration.

## Workflow

1. Reproduce or read the evidence for the bug.
2. Locate the relevant Swift, SwiftUI, or project configuration.
3. Make the smallest safe fix.
4. Build with the available Apple workflow.
5. Re-run the specific failing flow.
6. Summarize the cause, fix, and verification.

## Guardrails

- Do not do blind fixes without a reproduction or evidence trail.
- Do not change signing or deployment settings unless the bug is actually there.
- Preserve user edits and unrelated local changes.
