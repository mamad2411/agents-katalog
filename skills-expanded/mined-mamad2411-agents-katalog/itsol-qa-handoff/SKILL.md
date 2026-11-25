---
name: itsol-qa-handoff
description: "Prepare QA handoff with coverage, evidence, defects, gaps, risks, and release readiness."
---

# ITSOL QA Handoff

Make QA testable: provide scope, data, environments, risks, scenarios, and a clear pass/fail outcome.

## Process

1. Confirm QA has the story, acceptance criteria, PR, tech notes, environment, data, roles, accounts, config, and known limitations.
2. Build scenarios from risk: happy path, negative path, edge cases, regression, permissions, data boundaries, integrations, retries, and security smoke.
3. Use test-design techniques where useful: equivalence classes, boundary values, decision tables, state transitions, and exploratory testing.
4. For bugs, require environment, reproducible steps, actual versus expected result, data, attachments, impact, severity, priority, and release-blocking status.
5. Select the real interaction surface: agent-browser for web UI, supported CDP/browser automation for Electron, interactive command execution for CLI, contract/integration/security tests for API/backend, device/runtime checks for mobile, integrity/migration/rollback for data, and readiness/observability/rollback for infrastructure.
6. In Initiative Delivery, use the harness-native QA plan/verdict capability. Execute every required packet, bind the verdict to the implementation fingerprint, and never infer PASS from a planned check or agent completion label.
7. Route failed QA to `implementation-fix`, `plan-revision`, or `user-decision`. After remediation, rerun applicable plan review and code review and then fresh QA. Do not close the phase until QA passes.
8. For release readiness, check QA result, regression, support notes, monitoring, feature flags, rollback, and production verification needs.

## Execution Policy

After resolving `itsol-workflow-mode`, load `itsol-execution-policy` whenever resource, stop, or completion state matters; it owns the full execution state and evidence validation. Never use `maxTurns` or termination as completion; preserve `partial`, `blocked`, and `failed` outcomes.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Definition of Done
- [02-qa-i-testowanie.md](./references/02-qa-i-testowanie.md) - QA i testowanie
- [03-bug-report.md](./references/03-bug-report.md) - Bug report; Jak wymyślać edge case'y
- [04-statusy-w-issue-trackerze.md](./references/04-statusy-w-issue-trackerze.md) - Statusy w issue trackerze; Handoffy między rolami; Release i wdrożenie; Metryki procesu
- [05-szablony.md](./references/05-szablony.md) - Szablony
- [06-checklist-dla-developera.md](./references/06-checklist-dla-developera.md) - Checklist dla developera; Checklist dla QA
