---
name: dead-dependency-cleanup
description: Finds unused and duplicated packages in your manifests and removes them one at a time, running the build and tests after each removal so nothing breaks.
---

# Dead dependency cleanup

Remove one package at a time. A green build after each removal is the only proof.

## Steps

1. Identify the ecosystem and manifests (package.json, requirements.txt, pyproject.toml, go.mod, Cargo.toml, Gemfile). Run the baseline build and tests; if they fail now, stop and report.
2. Find candidates with the ecosystem's tool when available: `npx depcheck`, `npx knip`, `deptry`, `go mod tidy`, `cargo machete`. Otherwise search the source for each package's import name; note that import names can differ from package names.
3. Check what scanners miss before deleting: use in config files (babel, eslint, jest, webpack plugins), CLI use in scripts and CI files, peer dependencies required by another package, dynamic `require`, and type-only `@types/*` packages.
4. Find duplicates: two packages for one purpose, the same package at several versions in the lockfile (`npm ls <name>`), and runtime dependencies that belong in dev dependencies.
5. For each candidate: remove it with the package manager (`npm uninstall`, `pip uninstall` plus manifest edit), then run build, lint and tests. If anything fails, restore it and mark it as used.
6. Keep one commit per removal or small group.

## Rules

- Never hand-edit a lockfile.
- Do not upgrade anything in the same change.
- Do not remove a package that only a script or config references without reading that file.

## Report

Removed packages with size saved, kept packages with the reason they are still needed, and duplicates that need a decision from the team.
