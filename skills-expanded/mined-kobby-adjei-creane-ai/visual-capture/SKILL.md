---
name: visual-capture
description: Use when the task needs desktop-level or app-window screenshots and tool-specific capture is unavailable or insufficient. Sanitized adaptation of upstream screenshot skills.
---

# Visual Capture

## When to use
- The user explicitly asks for a screenshot.
- You need a system-level capture of an app, window, or region.
- Browser- or tool-specific screenshot features are not enough.

## Workflow
1. Prefer tool-native capture when it already exists for the target.
2. Otherwise use the OS-level capture method appropriate for the environment.
3. For Codex self-inspection, keep captures in a temp or artifact directory.
4. For user-deliverable output, save to the requested path or a stable project output path.

## Guardrails
- Capture only what is necessary for the task.
- Avoid collecting unrelated windows or sensitive information.
- If OS permissions block capture, report the exact permission problem instead of retrying blindly.
- Keep filenames stable and descriptive.

## Repo conventions
- Use `analysis_artifacts/` for debugging captures.
- Use `output/` only if the task is explicitly about producing a deliverable artifact.
