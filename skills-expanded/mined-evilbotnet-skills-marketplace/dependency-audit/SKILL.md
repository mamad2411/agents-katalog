---
name: dependency-audit
description: Audit dependencies for vulnerabilities, staleness, duplication, and bloat, producing a prioritized action list. Use when the user asks to review, audit, clean up, or assess project dependencies.
---

# Dependency Audit

1. **Inventory.** Parse the manifest(s) and lockfile(s). Separate direct
   from transitive dependencies — recommendations target direct deps.
2. **Security.** Run the ecosystem's audit tool if available
   (`npm audit`, `pip-audit`, `govulncheck`, `cargo audit`) and summarize
   findings by severity. Report only vulnerabilities that are reachable
   from this project's usage when you can determine it.
3. **Staleness.** Flag deps that are archived, deprecated, or far behind
   their latest major version. Note which lag is risky vs. merely cosmetic.
4. **Bloat & duplication.** Flag heavyweight packages used for a single
   trivial function and multiple libraries covering the same concern
   (two HTTP clients, two date libs).
5. **Prioritize.** Output a ranked action list:
   - `now` — vulnerable or broken
   - `soon` — deprecated/unmaintained with a clear migration
   - `eventually` — bloat and consolidation opportunities
   Each entry: the dep, the problem, the concrete recommended action, and
   the estimated blast radius of the change.

Do not upgrade anything unless asked — this skill reports; the user
decides.
