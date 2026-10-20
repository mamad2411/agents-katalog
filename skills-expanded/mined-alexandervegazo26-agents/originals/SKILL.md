---
name: dependency-management
description: Evaluating, auditing, and maintaining third-party dependencies — vulnerability scanning, maintenance health signals, and when to add vs. avoid a dependency. Load before adding a new dependency, or when auditing existing ones.
---

# Dependency Management

## Before adding a dependency

Check first whether the standard library or an existing project dependency already solves the problem. Every dependency added is long-term maintenance the team now owns indirectly — weigh: maintenance health (recent commits, responsive maintainers, issue backlog), security history (past CVEs, how fast they were patched), bundle/footprint size, license compatibility, and how hard it would be to replace later.

## Auditing existing dependencies

Run the ecosystem's audit tool (`npm audit`, `pip-audit`, `bundler-audit`, language-native equivalent) regularly, not just when prompted. Distinguish a vulnerability that's actually reachable in this codebase's usage from one in an unused code path of the dependency — reachability changes urgency, though an unreachable-today vulnerability can become reachable after an unrelated change.

## Updating

Prefer frequent small updates over rare large ones — a large version jump bundles breaking changes together and makes root-causing a regression harder. Read changelogs for breaking changes before bumping a major version; don't bump blindly because a bot opened a PR.

## Removing

If a dependency is confirmed unused, remove it rather than leaving it as latent attack surface and audit noise.

## License compatibility

Check license compatibility with the project's own licensing/distribution model before adding anything — a permissive-looking package can have a copyleft transitive dependency.
