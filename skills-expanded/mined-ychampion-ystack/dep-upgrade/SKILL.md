---
name: dep-upgrade
description: >-
  Upgrade dependencies safely, one at a time: list what is outdated, read each changelog for breaking
  changes, bump one package (or one tight group), run the build and tests, fix or roll back, and commit
  before the next. Use for "update dependencies", "bump packages", "upgrade X to v5", "fix the
  outdated/vulnerable packages", "Dependabot PRs pile", or a framework major-version upgrade.
---

# Dependency upgrade

Bumping everything at once turns ten small breakages into one knot nobody can untangle. Upgrade one
thing, prove it, keep it, move on.

## When it applies

- Several outdated or vulnerable packages to bring up to date.
- A single major-version upgrade (a framework, a compiler, a runtime).
- Merging a backlog of automated bump PRs.

## Procedure

### 1. Baseline

On a clean branch, run install, build, type check, lint and tests. Record what passes now. A test that
already fails is not the upgrade's fault; note it and keep it out of the verdicts.

### 2. List and order

Use the ecosystem's own tool (`bun outdated`, `pnpm outdated`, `pip list --outdated`,
`cargo outdated`, `go list -m -u all`, `npm audit` / `pip-audit` for vulnerabilities). Order:

1. security fixes;
2. patch and minor bumps, batched only if they're in the same family;
3. majors, one per step, low-level ones (runtime, compiler, test runner) before the things on top.

Packages that must move together (a framework and its plugins, a type package and its library) are
one step.

### 3. Read before you bump

For each major, read the changelog or migration guide between the current and target version. Note
every breaking change, then search the code for each removed or renamed API. If the list is long,
split the upgrade into a prep step (adapt the code on the old version where possible) and the bump.

### 4. Bump one step

Change the one version, install, and let the lockfile update. Check the lockfile diff for surprise
changes to other packages.

### 5. Prove it

Run the same checks as the baseline. Then exercise the code that uses the package: its tests, or a
short real run of the feature. "It compiles" is not enough for a library with runtime behaviour.

### 6. Keep or roll back

- Green: commit with the package, old -> new version, and anything you adapted. One commit per step.
- Red and the fix is small and clear: fix, re-run, commit.
- Red after two fix attempts: roll back that step, note why, and move to the next package.

### 7. Report

```
| Package | From -> To | Result | Notes |
| lib-a   | 2.1 -> 2.4 | kept   | -     |
| lib-b   | 4 -> 5     | kept   | adapted 3 call sites to new API |
| lib-c   | 1 -> 2     | held   | breaks X; needs <decision or work> |
Baseline failures (not caused by upgrades): <list>
```

## Rules

- One step per commit, so any later breakage bisects to one bump.
- Never delete the lockfile to "fix" an install. Resolve the conflict.
- Don't add new packages during an upgrade run.
- Pin and note a package you hold back; don't leave a range that will drift.
