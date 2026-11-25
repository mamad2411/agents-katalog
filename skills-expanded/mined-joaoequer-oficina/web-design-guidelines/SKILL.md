---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
argument-hint: <file-or-pattern>
---

> Provenance: github.com/vercel-labs/agent-skills (skills/web-design-guidelines), rules from vercel-labs/web-interface-guidelines command.md snapshot 2026-10-13, audited 2026-10-13 (SKILL.md read in full, instruction-only, no scripts). Why: front-end review of personal projects. Modified: upstream fetches the rules from raw.githubusercontent.com at every run; here they are vendored in references/rules.md so the skill makes no network call. Refresh the file by hand when updating.

# Web Interface Guidelines

Review files for compliance with the rules in `references/rules.md` (read it first; it holds the rules and the output format).

1. Read `references/rules.md`.
2. Read the files given as argument (or ask which files or pattern to review).
3. Check every rule. These rules assume React or HTML: for React Native or vanilla JS, skip the ones that do not apply and say so.
4. Output findings in the terse `file:line` format the rules define.
