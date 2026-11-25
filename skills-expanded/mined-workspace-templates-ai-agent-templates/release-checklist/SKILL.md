---
name: release-checklist
description: "Runs a release step by step: verifies the branch, tests and changelog, tags the version, builds artifacts and writes a rollback note before shipping."
---

# Release checklist

Work the gates in order. A failed gate stops the release.

## Gates

1. **Branch**: on the release branch, `git status` clean, up to date with its remote (`git fetch` then compare). Nothing unmerged that should be in.
2. **CI**: the latest run for this exact commit passed. If you cannot see CI, run the full local suite: lint, typecheck, tests, build.
3. **Version**: decide it from the changes (major for breaking), update every file that holds it, and confirm they agree.
4. **Changelog**: an entry for this version with date, grouped as Added, Changed, Fixed, Removed, each item written for a user. Breaking changes get a migration line.
5. **Dependencies and security**: run the audit command for the ecosystem (`npm audit --omit=dev`, `pip-audit`, `cargo audit`); list anything high or critical.
6. **Artifacts**: build from a clean checkout, record file names and sizes, and run a smoke test of the built output (import it, start it, hit the health endpoint).
7. **Tag**: annotated, on the release commit: `git tag -a vX.Y.Z -m "..."`. Verify with `git show vX.Y.Z --stat`.
8. **Rollback note**: write down the previous version, the exact command to deploy or reinstall it, any database migration that is not reversible, and who to tell.

## Rules

- Do not push tags, publish packages or deploy until the user says "ship it" after seeing the summary.
- Never skip a gate silently. A skipped gate is listed with the reason.

## Report

A table of gate, status and evidence, then the rollback note, then the exact commands left for the user to run.
