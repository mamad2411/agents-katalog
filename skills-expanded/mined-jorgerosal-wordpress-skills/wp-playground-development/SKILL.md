---
name: wp-playground-development
description: WordPress Playground review for Codex. Use when reviewing Blueprints, Playground CLI usage, embedded Playground demos, reproducible WordPress setups, or zero-setup bug repro environments.
---

# Codex WordPress Playground Review

## Purpose

Use this skill when Codex should review WordPress Playground setups for reproducibility, Blueprint quality, local CLI workflows, and demo clarity.

## Focus Areas

- Blueprint structure and step selection
- `@wp-playground/cli` workflows
- Embedded demos and `blueprint-url` usage
- Reproducibility and version clarity

## Workflow

1. Identify the Blueprint, CLI entrypoint, or embed flow.
2. Check reproducibility and hidden setup first.
3. Review steps, versions, and landing page intent.
4. Load only the needed shared references from `../../claude-skills/wp-playground-development/references/`.
5. Report findings with severity, file references, impact, and fixes.

## References

- `../../claude-skills/wp-playground-development/references/blueprint-patterns.md`
- `../../claude-skills/wp-playground-development/references/cli-and-local-workflows.md`
- `../../claude-skills/wp-playground-development/references/embedding-and-repros.md`
