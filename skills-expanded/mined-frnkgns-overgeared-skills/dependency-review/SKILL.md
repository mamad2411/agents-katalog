---
name: dependency-review
description: Safely evaluate dependency additions, upgrades, and replacements. Use when adding a package, upgrading dependencies, replacing a library, responding to an audit finding, or changing framework and runtime versions.
---
# Dependency Review

## Purpose

Understand the cost and risk of a dependency change before it lands in the project.

## Check

- Why the dependency is needed, and whether the project already has an alternative.
- Package health: maintenance activity, release cadence, ownership, and issue responsiveness.
- Version compatibility with the project's runtime, framework, and other dependencies.
- Breaking changes and the required migration steps.
- Transitive dependency footprint and new install or build scripts.
- Security advisories for the package and its resolved tree.
- Runtime and environment requirements, including Node, runtime, and platform constraints.
- Bundle, build-time, and memory impact where relevant.
- Licensing when the project or repository tracks licenses.
- Alternatives considered, including doing nothing.

## Rules

- Do not run broad or automatic upgrades. Upgrade only what the request covers.
- Do not perform a major-version upgrade without explicit authorization.
- Do not run install scripts, postinstall hooks, or unfamiliar packages' code merely to inspect them; review the code first.
- Never apply audit auto-fix commands automatically.
- Never commit secrets, private registries, or credentials introduced by a registry change.
- Keep lockfile changes scoped to the requested dependency change and verify the resolved tree afterward.
- Prefer the smallest version change that fixes the actual problem.
