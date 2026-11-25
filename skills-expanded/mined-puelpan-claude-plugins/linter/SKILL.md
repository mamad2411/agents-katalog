---
name: linter
description: >-
  Detect the project's linter / formatter / type-checker, run it, and fix all
  reported issues. Use only when the user explicitly asks to lint, run the
  linter, fix lint errors, or fix formatting/type errors for the project.
---

# Linter

Run the project's linter and fix all the issues found.

## When to Use This Skill

Use this skill only when the user explicitly asks to lint, run the linter, or
fix lint / formatting / type errors.

## Instructions

- Find out what the linter tool is for this project. Check these files:
  `Makefile`, `pyproject.toml`, `package.json`.
- Run the linter tool command.
- Fix the reported linter or type errors.
