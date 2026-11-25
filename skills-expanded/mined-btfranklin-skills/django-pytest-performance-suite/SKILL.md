---
name: django-pytest-performance-suite
description: >-
  Build Django performance regression tests with pytest-benchmark. Use for ORM, views, schema, transactions, or database backend behavior. Match the production database engine and topology. Do not use for one-time profiling, browser rendering, application performance monitoring, or non-Django services.
---

# Django Pytest Performance Suite

## Workflow

1. Inspect the existing Django, database, pytest, command, and CI conventions. Record the production backend, driver, engine version, topology, relevant options, and workload scale.
2. Choose important uncached work. It can include ORM queries, builders, read models, request wrappers, and serializers. It can also include admin paths, migrations, schema operations, transactions, or database backend behavior.
3. Define the database-fidelity contract before you implement tests. Reproduce the applicable production engine and access mode. Document each deliberate approximation. Do not use an approximation to make claims about production latency.
4. Create a separate performance test group. Give it dedicated settings, a marker, commands, and on-demand CI. Keep it out of the default unit-test run.
5. Seed realistic scenarios in a deterministic way. Fix time, identifiers, random values, ordering, and external side effects. Build expensive data outside benchmark rounds.
6. Check correctness before you measure time. Use direct assertions, normalized snapshots, or summary hashes to check the required results. Then enforce a query or operation limit for the measured layer.
7. Benchmark stable work with `pytest-benchmark`. Exclude setup and instrumentation unless their cost is the explicit subject of the case.
8. Calibrate time limits only from repeated clean runs on a stable, representative runner. If that runner is not available, record timing results without enforcement. Continue to enforce deterministic correctness checks and query or operation limits. Report the unavailable runner and each deliberate approximation.
9. Keep correctness updates and time-baseline acceptance as separate maintenance actions. Add a coverage registry only for a limited family of interfaces where missing coverage is a known risk.

Use the repository's package manager and task runner. Preserve existing test conventions unless they prevent an isolated, reproducible performance test group.

## Decisions

- Never choose PostgreSQL, Turso, SQLite, or another database because this skill prefers it. Follow the target project's production contract.
- For an embedded production database, use the real Django backend and driver. Use an isolated local file or memory mode only when that mode matches the contract.
- For client-server or remote databases, preserve the relevant protocol and topology. Measure managed-network latency separately when CI cannot reproduce it faithfully.
- Prefer `RequestFactory` only when the test measures a request interface and excludes middleware from the contract.
- Prefer direct assertions for specific properties. Use normalized snapshots when comparison of the full result helps review. Use summaries and hashes for very large payloads.
- Use query or operation limits to identify regressions early. Use runner-specific time limits for time measurements.
- Never update snapshots or budgets automatically after a failure.

## Verify Current Information

When instrumentation or configuration depends on version-specific behavior, verify that behavior. Use the target repository and primary documentation. Record the checked Django, pytest, pytest-benchmark, database backend, and driver versions in reports. Do not store current package or database versions in this skill.

## Validation

Run correctness and query or operation checks before you measure time. Use multiple independent clean processes on the intended runner to measure variation. Enforce a time limit only when the variation is low enough to identify a product regression. Do not increase a tolerance only to make an unstable case pass.

Verify that ordinary tests exclude the performance marker. Verify that reports identify every case and environment. Keep correctness updates and time-limit acceptance as separate maintenance commands.

## Resources

- Read [references/patterns.md](references/patterns.md) when you implement database fidelity, deterministic data, snapshots, limits, or reports.
- Also read it when you implement optional coverage registration.
- Read [examples/performance-suite-plan.md](examples/performance-suite-plan.md) when preparing a concrete suite plan or handoff.
