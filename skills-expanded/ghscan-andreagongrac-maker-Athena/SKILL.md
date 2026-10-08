---
name: visual-verify-ui
description: Wraps the browser tool into a dedicated visual QA testing skill for frontend work.
argument-hint: "test <url> | snap"
allowed-tools:
  - Bash
  - Read
auto-invoke: false
model: default
---

# Visual QA & UI Verification

Automates visual regression testing and responsive design checks by formally deploying browser tools to capture DOM states and screenshots.

## Triggers

"check the UI", "does this look right", "take a screenshot"

## Core Mechanics

1. Boots local server if not running.
2. Uses Browser tool to navigate to target URL.
3. Captures full-page screenshots across Mobile, Tablet, and Desktop viewports.
4. Returns visual evidence to the main protocol loop.

## Reference Paths

- `.context/memories/protocols/engineering/99-visual-verification.md`
