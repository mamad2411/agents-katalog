---
name: development-and-testing-category-pointer
description: "Pointer to a library of 6 specialized Development And Testing skills. Use when working on development-and-testing-related tasks."
risk: none
---

# Development And Testing Capability Library 🎯

This is a **pointer skill**. The 6 specialized Development And Testing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **bug-hunter** — Systematically finds and fixes bugs using proven debugging techniques. Traces from symptoms to root cause, implements fixes, and prevents regression.
- **debugger** — Debugging specialist for errors, test failures, and unexpected
behavior. Use proactively when encountering any issues.

- **debugging-strategies** — Transform debugging from frustrating guesswork into systematic problem-solving with proven strategies, powerful tools, and methodical approaches.
- **openclaw-github-repo-commander** — 7-stage super workflow for GitHub repo audit, cleanup, PR review, and competitor analysis
- **systematic-debugging** — Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- **test-fixing** — Systematically identify and fix all failing tests using smart grouping strategies. Use when explicitly asks to fix tests ("fix these tests", "make tests pass"), reports test failures ("tests are failing", "test suite is broken"), or completes implementation and wants tests passing.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/development-and-testing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/development-and-testing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
