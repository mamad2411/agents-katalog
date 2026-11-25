---
name: repo-package-script-audit
description: Audits package lifecycle scripts and package manifest scripts for risky behavior. Use when dependency changes, package installation, package scripts, postinstall hooks, publish/release scripts, or script execution are involved.
---

# Repository Package Script Audit

Use this skill to inspect lifecycle scripts and package manifest scripts before dependency install or script execution.

## When to Use This Skill

Use this skill when dependency changes add package lifecycle scripts, `package.json` scripts change, lifecycle hooks exist, scripts download remote code or binaries, scripts modify permissions or delete files, scripts access secrets or deployment tools, or package-manager scripts run in unfamiliar repositories.

## Workflow

Use `workflows/package-script-audit-workflow.md`.

## Scripts

This skill owns `scripts/package-script-scan.py`.
