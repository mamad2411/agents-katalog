---
name: audit-codebase-integrity
description: "Structured 19-area integrity audit for subtle bugs, design flaws and operational correctness risks. Run after incidents or refactors, before merging large branches or as a periodic health check."
---

# Codebase Integrity Audit

- If the user names files or directories, use that scope. Otherwise review the entire codebase.

## References

1. [Data Representation](./references/data-representation.md)
2. [Contract Invariants](./references/contract-invariants.md)
3. [Leaky Abstractions](./references/leaky-abstractions.md)
4. [Timing Correctness](./references/timing-correctness.md)
5. [Concurrency](./references/concurrency.md)
6. [Build Reproducibility](./references/build-reproducibility.md)
7. [Fake Coverage](./references/fake-coverage.md)
8. [Flag Debt](./references/flag-debt.md)
9. [Global State](./references/global-state.md)
10. [Idempotency](./references/idempotency.md)
11. [Reliability](./references/reliability.md)
12. [Silent Failure](./references/silent-failure.md)
13. [Observability Gaps](./references/observability-gaps.md)
14. [Security & Trust Boundaries](./references/security-boundaries.md)
15. [Cache & Freshness](./references/cache-freshness.md)
16. [Single Source of Truth](./references/single-source-of-truth.md)
17. [Schema Evolution](./references/schema-evolution.md)
18. [Online Migrations](./references/online-migrations.md)
19. [Time & Locale](./references/time-locale.md)

## Process

1. Read one reference file.
2. Review the chosen scope against that reference.
3. Repeat for every reference in order.

## Output

- Emit one section per reference.

### For each section, include:

- `Reference:` the reference title.
- `Scope checked:` files and directories reviewed for that reference.
- `Result:` the findings or "No findings".

### For each finding, include:

- what is wrong
- evidence
- impact
- recommended fix
