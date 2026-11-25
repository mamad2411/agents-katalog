---
name: repo-accessibility-dom-inspection
description: Inspects DOM and accessibility evidence for browser interaction bugs. Use when debugging labels, focus, keyboard navigation, roles, forms, modals, hidden content, or screen-reader-relevant behavior.
---


# Accessibility and DOM Inspection

Use this skill when the issue concerns how users interact with elements or how the browser represents the page.

## Focus Areas

- accessible names and labels
- focus order and focus trapping
- keyboard behavior
- buttons vs links
- form validation and error association
- modal/dialog semantics
- hidden/disabled/inert content
- landmark and heading structure
- element state: selected, expanded, checked, invalid, busy
- dynamic content announcements

## Required Behavior

- Prefer accessibility tree and DOM evidence over visual guesses.
- Note whether a problem is semantic, interaction, visual, or state-management related.
- Avoid framework-specific advice unless paired with a framework plugin.
- Do not capture private page text unless required and approved.

## Workflow

Use `workflows/accessibility-dom-inspection-workflow.md`.

