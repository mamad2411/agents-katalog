---
name: dependency-governance
description: Guidelines for adding, updating, auditing, and removing dependencies while preserving lockfile integrity and supply chain safety
---

# Instructions

- **Use Existing Capabilities First:** Check the current standard library, framework utilities, and installed dependencies before adding a package.
- **Lockfile Alignment:** Use the package manager implied by the lockfile. Never mix npm, yarn, pnpm, and bun in the same project unless the repo already documents that strategy.
- **Package Selection Criteria:** Prefer actively maintained packages with recent releases, clear licenses, strong TypeScript support where relevant, low transitive dependency count, and documented security practices.
- **Minimal Version Changes:** Add or update only the dependency needed for the task. Avoid broad package upgrades unless the user requested a dependency refresh.
- **Vulnerability Handling:** For security updates, inspect whether the vulnerable path is reachable, apply the narrowest safe fix, and run the project test/build commands afterward.
- **Removal Hygiene:** When removing a dependency, delete unused imports, configuration, types, scripts, and documentation references.

# Gotchas

- **Transitive Risk:** A small package can pull in a large dependency tree. Inspect dependency impact before adopting it.
- **License Drift:** New packages can introduce licenses that are incompatible with the project or organization.
- **Install Script Risk:** Packages with postinstall scripts can execute code during installation. Treat them as higher risk.
- **Lockfile Churn:** Reinstalling with the wrong package manager can rewrite the lockfile and create noisy, risky diffs.

# Validation Loops

1.  **Manifest Check:** Confirm `package.json` and the relevant lockfile changed consistently.
2.  **Audit Check:** Run the project-appropriate audit command and document unresolved findings.
3.  **Build/Test Check:** Run the affected test, type, lint, and build commands.
4.  **Usage Check:** Search for old imports or stale docs after upgrades/removals.
