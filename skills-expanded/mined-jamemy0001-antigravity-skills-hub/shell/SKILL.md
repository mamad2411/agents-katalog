---
name: shell
description: >-
  Runs the rest of a /shell request as a literal shell command. Use only when
  the user explicitly invokes /shell and wants the following text executed
  directly in the terminal.
disable-model-invocation: true
aliases:
  - shell
category: "07 - Codebase Exploration & Tooling"
tags:
  - agent-skill
  - developer-tools
  - stage-7
---

# Run Shell Commands

Use this skill only when the user explicitly invokes `/shell`.

## Behavior

1. Treat all user text after the `/shell` invocation as the literal shell command to run.
2. Execute that command immediately with the terminal tool.
3. Do not rewrite, explain, or "improve" the command before running it.
4. Do not inspect the repository first unless the command itself requires repository context.
5. If the user invokes `/shell` without any following text, ask them which command to run.

## Response

- Run the command first.
- Then briefly report the exit status and any important stdout or stderr.

---

## 🔗 Connected Skills
- [[Skills/sdk/SKILL|sdk]]
- [[Skills/automate/SKILL|automate]]

<!-- v1.1.0 synchronized: 2026-09-29 -->
