---
name: audit-dependencies
description: Runs your package manager audit, explains which advisories really matter and proposes the smallest safe upgrade for each.
disable-model-invocation: true
---

Audit the dependencies of this project. Focus: $ARGUMENTS (all manifests if empty).

1. Detect the ecosystem from lockfiles and run the matching audit: `npm audit --json`, `pnpm audit`, `pip-audit`, `cargo audit`, `bundle audit`, `composer audit` or `govulncheck ./...`. If the tool is missing, say so and stop.
2. For every advisory, decide if it is real: is the package a production dependency or dev-only, is the vulnerable function actually called (search the code), and is the vulnerable version the one in the lockfile?
3. For each real one, find the smallest fixed version and classify the jump as patch, minor or major. Read the changelog for breaking changes if it is major.
4. Mention transitive packages with the parent that pulls them in, and whether an override or resolution would help.
5. Do not install, update or edit lockfiles yet.

Report a table: package, current, fixed in, severity, reachable (yes/no/unknown), upgrade size. Then list dismissed advisories with the reason. Ask which upgrades to apply, and run the tests after applying.
