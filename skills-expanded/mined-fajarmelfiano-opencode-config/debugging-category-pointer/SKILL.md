---
name: debugging-category-pointer
description: "Pointer to a library of 4 specialized Debugging skills. Use when working on debugging-related tasks."
risk: none
---

# Debugging Capability Library 🎯

This is a **pointer skill**. The 4 specialized Debugging skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **bug-hunt-swarm** — Parallel read-only multi-agent root-cause investigation for bugs, regressions, crashes, flaky behavior, or unexplained failures.
- **diagnose-android-overheating** — Use when diagnosing Android overheating, idle heat, thermal throttling, charging or radio heat, or abnormal battery drain with read-only ADB evidence and approval gates.
- **logic-locate** — Locate the root cause of a CONFIRMED failure via backward-then-forward semi-formal tracing.
- **phase-gated-debugging** — Use when debugging any bug. Enforces a 5-phase protocol where code edits are blocked until root cause is confirmed. Prevents premature fix attempts.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/debugging/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/debugging`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
