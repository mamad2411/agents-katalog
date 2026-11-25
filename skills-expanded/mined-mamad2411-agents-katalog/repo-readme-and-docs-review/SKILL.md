---
name: repo-readme-and-docs-review
description: Reviews and updates repository documentation such as READMEs, setup guides, contribution docs, troubleshooting pages, and examples. Use when documentation must reflect repository behavior, commands, configuration, or user-facing workflows.
---

# README and Documentation Review

Use this skill when creating, updating, or reviewing repository documentation.

## When to Use This Skill

Use for README updates, setup docs, contribution docs, troubleshooting docs, examples, usage docs, and validating docs for placeholders, stale paths, and unsupported claims.

## Process

1. Identify the intended audience.
2. Inspect relevant repository files before writing technical claims.
3. Compare docs against actual scripts, configs, commands, and file paths.
4. Check that prerequisites and environment variables are explicit.
5. Check that examples are safe and use placeholders for secrets.
6. Separate verified facts from assumptions.
7. Keep the update scoped to the requested change.
8. State validation performed and remaining uncertainty.

## Workflows

- Use `workflows/docs-review-workflow.md` to review existing documentation.
- Use `workflows/docs-update-workflow.md` to update docs after code or config changes.

## Resources

- `resources/docs-quality-checklist.md`

## Examples

- `examples/readme-review-notes-example.md`

## Scripts

This skill owns:

```text
scripts/docs-link-and-placeholder-scan.py
scripts/docs-stop-reminder.py
```

Run scripts with `--help` before manual use.
