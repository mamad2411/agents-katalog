---
name: performance-dependency
description: Use for performance problems, slow builds, memory/CPU issues, dependency updates, security advisories, migrations, or package risk.
---

# Performance And Dependency Work

Measure before changing and verify after.

## Performance Loop

1. Define the user-visible or system metric.
2. Measure baseline.
3. Profile to locate the bottleneck.
4. Change one meaningful factor.
5. Re-measure with the same method.
6. Check correctness did not regress.

Avoid speculative optimizations. Do not trade correctness or accessibility for speed without explicit approval.

## Dependency Loop

1. Read current package manager, lockfile, runtime, and framework versions.
2. Identify why the dependency changes: security, compatibility, feature, maintenance.
3. Check changelog/migration notes from primary sources when current facts matter.
4. Update incrementally.
5. Run focused tests and build/type checks.
6. Inspect call sites for breaking behavior.

## Risk Flags

- Auth, crypto, payments, database drivers, ORMs, build tools, AI SDKs, browsers, and test runners deserve extra verification.
- Never silence vulnerability checks or tests as the fix.
- For migrations, plan rollback and production data impact.

