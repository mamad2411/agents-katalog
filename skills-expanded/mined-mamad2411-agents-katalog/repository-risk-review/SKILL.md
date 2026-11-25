---
name: repository-risk-review
description: Reviews repository state before large or risky changes. Use when assessing dirty working tree state, high-risk files, migrations, lockfiles, infrastructure, deployment config, secrets-like files, or generated outputs before editing.
---

# Repository Risk Review

Use this skill to inspect repository risk before making broad, destructive, production-adjacent, or security-sensitive changes.

## When to Use This Skill

Use this skill before:

- large refactors
- dependency upgrades
- lockfile changes
- migration work
- deployment or infrastructure edits
- deleting or moving files
- modifying authentication, authorization, cryptography, or secrets handling
- touching generated files
- changing CI/CD workflows
- working in an unfamiliar repository

## Review Checklist

1. Check whether the working tree has uncommitted user changes.
2. Identify high-risk directories and files.
3. Identify generated files and lockfiles.
4. Identify migrations and schema files.
5. Identify infrastructure and deployment config.
6. Identify CI/CD config.
7. Identify files that may contain secrets or private data.
8. Identify test/build commands from repository conventions.
9. Recommend a safe plan before editing.

## Script

This skill owns:

```text
scripts/repository_risk_scan.py
```

Run with `--help` first:

```bash
python3 .agents/plugins/repo-agent-safety/skills/repository-risk-review/scripts/repository_risk_scan.py --help
```

The script is read-only and uses standard library commands to inspect common repository risk indicators.
