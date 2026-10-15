---
name: flexibility-testing
description: >-
  Plan and implement flexibility tests: installability, environment adaptability,
  and replaceability — the ISO/IEC 25010:2023 Flexibility characteristic that
  replaced and absorbed the former Portability characteristic. Use when: "runs
  on-prem and cloud," "移植性," "portability," "flexibility," "Docker/K8s deployment
  testing," "install/upgrade/rollback testing," "does it work on ARM/Windows/
  air-gapped," or migrating between databases, clouds, or runtimes. Produces an
  adaptability test matrix (design mode) and CI matrix jobs / installation smoke
  tests (implementation mode). Not for: browser engine differences — use
  cross-browser-testing; scalability/load — use performance-efficiency skills.
  Related: cross-browser-testing, test-strategy-doc.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1 (test types: non-functional)"
  iso25010: [flexibility]
  mode: [design, implementation]
---

# Flexibility Testing

Verify the system installs, adapts, and can be replaced across its supported
environments — the ISO/IEC 25010:2023 characteristic almost every QA suite silently
skips. (In ISO 25010:2023, **Flexibility** replaced the 2011 **Portability**
characteristic and added *scalability* as a fourth sub-characteristic.)

## Scope note

This skill covers three of the four Flexibility sub-characteristics: **adaptability**,
**installability**, and **replaceability**. The fourth — **scalability** — is a
capacity/load concern; hand off to the performance-efficiency skills for it.

## Objective

An environment matrix with explicit pass criteria for the three sub-characteristics in
scope: **adaptability** (runs correctly across OS/arch/runtime/config variants),
**installability** (install, upgrade, rollback, uninstall succeed cleanly), and
**replaceability** (swaps in for the component it replaces without data loss).
The failure mode this prevents: "supported platforms" listed in the README that no
pipeline has ever exercised.

## Context Discovery

- What does the product *claim* to support? (README, sales docs, SLAs — the claim set
  is the test scope; untested claims are liabilities)
- Deployment modes: SaaS-only? on-prem? air-gapped? single binary? Helm chart?
- Upgrade path policy: N−1? N−2? Is rollback promised?
- What varies across environments: OS, CPU arch (x86/ARM), runtime versions, DB
  engines, locales/timezones, filesystem case-sensitivity.

## Instructions

1. **Build the claims-driven matrix**: one row per supported environment combination,
   pruned by risk — full test on the most-used and most-different combos, smoke on the
   rest. Every claimed platform appears at least once.

2. **Adaptability tests**: run the existing functional smoke suite across the matrix
   (CI matrix strategy). Add environment-sensitive cases: path separators, locale
   number/date formats, TZ handling, case-sensitive filesystems, ARM-specific native
   deps.

3. **Installability tests**: script fresh-install → verify → upgrade from N−1 →
   verify data intact → rollback → verify. Uninstall must leave no orphaned state.
   These are tests, not docs — automate them.

4. **Replaceability tests** (when applicable): migration from the predecessor/
   competitor component with a realistic dataset; assert row counts, checksums, and
   behavior parity on critical flows.

5. **Wire into CI**: matrix jobs (e.g. GitHub Actions `strategy.matrix` over
   `os: [ubuntu, windows, macos]` × arch) for adaptability; a scheduled pipeline for
   the install/upgrade/rollback cycle, which is too slow for every PR.

## Output Format

### design mode

| Env ID | OS/Arch | Runtime | DB | Depth (full/smoke) | Sub-characteristic | Pass Criteria |
|---|---|---|---|---|---|---|
| ENV-01 | ubuntu-22.04/x86 | Node 20 | PG 16 | full | adaptability | smoke suite 100% |
| ENV-05 | RHEL 9/ARM | Node 20 | PG 15 | smoke | adaptability + install | install+upgrade+rollback clean |

### implementation mode

GitHub Actions canonical shape:

```yaml
jobs:
  adaptability:
    strategy:
      matrix:
        os: [ubuntu-22.04, windows-2022, macos-14]
        node: [20, 22]
    runs-on: ${{ matrix.os }}
    steps: [ ... checkout, setup, run smoke suite ... ]
```

Plus `scripts/install-cycle-test.sh` implementing install → upgrade → rollback with
assertions after each phase.

## Anti-Patterns

- **Testing only the dev environment** — the matrix collapses to "Ubuntu x86 latest"
  because that's what CI runs by default. **Guard:** matrix rows come from the claims
  list, not from what's convenient.
- **Install docs instead of install tests** — a README paragraph is not verification.
  **Guard:** installability = executable script with assertions, run on schedule.
- **Upgrade tested, rollback assumed** — rollback fails exactly when you need it.
  **Guard:** rollback is a distinct scripted phase with data-integrity assertions.
- **Hallucinated runner labels/images** — CI configs referencing runner images that
  don't exist. **Guard:** verify runner labels against the CI provider's current
  documentation before committing.

## Related Skills

- `cross-browser-testing` — client-side compatibility; this skill covers server/
  install-side flexibility.
- `test-strategy-doc` — decides whether flexibility is in scope at all.

## References

- ISO/IEC 25010:2023 — Flexibility (adaptability, scalability, installability,
  replaceability); supersedes the 2011 Portability characteristic.
