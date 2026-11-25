---
name: phase-6-verify
description: Phase 6 of the development cycle. Verifies a milestone before release — full test suite, acceptance-criteria check by the qa-tester agent, security audit by the security-auditor agent, performance against the spec's NFRs, and an architecture check — and produces a go/no-go verification report.
disable-model-invocation: true
argument-hint: "[milestone, e.g. M2]"
---

# Phase 6 — Verify a milestone

Milestone: $ARGUMENTS. If none was given, use the latest milestone whose tasks are all `[x]`.

Goal: evidence, not opinion, that the milestone does what the spec says, safely and fast enough.

## Steps

```
Verification progress:
- [ ] 1. Full automated suite
- [ ] 2. Acceptance check          (qa-tester agent)
- [ ] 3. Security audit            (security-auditor agent)
- [ ] 4. Performance vs NFRs
- [ ] 5. Architecture drift check  (architecture-reviewer agent; for MVP and larger releases)
- [ ] 6. Fix, re-verify, report
```

**1. Suite.** Run every test (unit, integration, end-to-end), plus lint, type checks, and the build. Record the commands and the results, including coverage.

**2. Acceptance.** Use the **qa-tester** agent with the list of acceptance criteria covered by this milestone's tasks. It checks that every criterion has a passing test and tries the edge cases.

**3. Security.** Use the **security-auditor** agent on the whole codebase, scoped to what changed in this milestone. Include the dependency vulnerability scan. Also check that every mitigation in `docs/security/THREAT_MODEL.md` that is due in this milestone is in place.

**4. Performance.** For each performance NFR in the spec, measure it with the `optimizing-performance` skill, for example a short load test or page timings. If a target isn't met, open a task in the backlog.

**5. Architecture.** For MVP and larger releases, use the **architecture-reviewer** agent to compare the code with ARCHITECTURE.md and the ADRs. Fix any drift, or record the change in a new ADR.

**6. Fix and report.** Create a backlog task for every Blocker or High finding, and fix them with `/phase-5-build`. Then repeat the failed checks. Write the report:

```markdown
# Verification report — <milestone> — YYYY-MM-DD
Decision: GO | NO-GO

| Check | Result | Evidence |
|-------|--------|----------|
| Test suite | ✅ 214 passed, coverage 87% | `<command>` |
| Acceptance criteria | ✅ 23/23 | qa-tester report |
| Security | ✅ 0 high, 2 low (accepted) | security-auditor report |
| Performance NFR-1 | ✅ p95 1.4 s (target 2 s) | load test |
| Architecture | ✅ no drift | architecture-reviewer |

## Open issues accepted for release
## Follow-up tasks created
```

Save it to `docs/release/VERIFY-<milestone>.md`. If the decision is GO, finish with: "Next: `/phase-7-release`".
