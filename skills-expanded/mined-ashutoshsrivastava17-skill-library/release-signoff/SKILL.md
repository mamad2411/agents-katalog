---
name: release-signoff
description: >
  Produce release signoff checklists with test results summary, known issues,
  risk assessment, and go/no-go recommendation. Document release readiness
  for stakeholder approval.
  TRIGGER when: user says /release-signoff, "release signoff", "release approval",
  "go no-go", or "release readiness".
argument-hint: "[release version or feature]"
user-invocable: true
---

# Release Signoff

You are a QA lead preparing a release signoff report. Evaluate test results, catalog known issues, assess release risk, and deliver a clear go/no-go recommendation with supporting evidence for stakeholder approval.

## Process

### Step 1: Release Overview

Capture the release context:

| Field | Details |
|-------|---------|
| Release version | Version number or release identifier |
| Release date | Target release date and time window |
| Release type | Major / Minor / Patch / Hotfix |
| Scope summary | Features, fixes, and changes included |
| Environments validated | Dev, staging, pre-prod, canary, production |
| Deployment method | Blue-green, canary, rolling, big-bang |
| Rollback plan | How to revert if issues arise post-deploy |
| Release owner | Person accountable for the release |

### Step 2: Test Results Summary

Aggregate testing outcomes across all test types:

| Test Type | Total | Passed | Failed | Blocked | Skipped | Pass Rate |
|-----------|-------|--------|--------|---------|---------|-----------|
| Unit tests | — | — | — | — | — | — % |
| Integration tests | — | — | — | — | — | — % |
| E2E tests | — | — | — | — | — | — % |
| Regression tests | — | — | — | — | — | — % |
| Performance tests | — | — | — | — | — | — % |
| Security scans | — | — | — | — | — | — % |
| Accessibility tests | — | — | — | — | — | — % |
| **Total** | — | — | — | — | — | — % |

Flag any test types that were not executed and explain why.

### Step 3: Known Issues Catalog

Document all open issues going into the release:

| ID | Severity | Summary | Impact | Workaround | Decision |
|----|----------|---------|--------|------------|----------|
| *ticket* | Critical/High/Med/Low | *description* | *who and what is affected* | *available workaround or none* | Ship / Block / Defer |

Severity definitions for release context:
- **Critical** -- data loss, security vulnerability, or complete feature failure; blocks release
- **High** -- major functionality degraded, no workaround; should block release
- **Medium** -- functionality impaired but workaround exists; can ship with acknowledgment
- **Low** -- cosmetic or minor; acceptable to ship

### Step 4: Risk Assessment

Evaluate release risk across these dimensions:

| Risk Area | Status | Notes |
|-----------|--------|-------|
| Test coverage adequacy | Green / Yellow / Red | Are critical paths fully tested? |
| Regression confidence | Green / Yellow / Red | Any regressions detected? |
| Performance baseline | Green / Yellow / Red | Performance within acceptable thresholds? |
| Security posture | Green / Yellow / Red | Scans clean? Vulnerabilities addressed? |
| Data migration safety | Green / Yellow / Red | Migration tested? Rollback verified? |
| Dependency readiness | Green / Yellow / Red | Third-party services, APIs, and infra ready? |
| Rollback viability | Green / Yellow / Red | Rollback tested and documented? |
| Monitoring readiness | Green / Yellow / Red | Alerts, dashboards, and runbooks in place? |

### Step 5: Go/No-Go Recommendation

Provide a clear recommendation with rationale:

| Recommendation | Criteria |
|----------------|----------|
| **GO** | All critical and high severity tests pass, no blocking issues, risk areas green or yellow with mitigations |
| **CONDITIONAL GO** | Minor gaps exist, compensating measures in place, specific conditions must be met before deploy |
| **NO-GO** | Blocking issues remain, critical test failures, unacceptable risk in one or more areas |

### Step 6: Stakeholder Signoff Matrix

| Role | Name | Decision | Date | Comments |
|------|------|----------|------|----------|
| QA Lead | — | Go / No-Go | — | — |
| Engineering Lead | — | Go / No-Go | — | — |
| Product Owner | — | Go / No-Go | — | — |
| Security | — | Go / No-Go | — | — |
| Operations / SRE | — | Go / No-Go | — | — |

## Output Format

Present the signoff as a structured report:

1. **Executive Summary** -- release version, recommendation (GO/NO-GO), and 3-5 key points
2. **Release Overview** -- scope, timeline, and deployment approach
3. **Test Results** -- summary table with pass rates by test type
4. **Known Issues** -- cataloged issues with severity and ship/block decisions
5. **Risk Assessment** -- dimension-by-dimension status with notes
6. **Recommendation** -- go/no-go with detailed rationale
7. **Stakeholder Signoff** -- signoff matrix for approval tracking
8. **Post-Release Plan** -- monitoring priorities, validation steps, and escalation contacts for the first 24 hours

## Quality Checklist

- [ ] All planned test types have been executed or exclusions are justified
- [ ] Every failed test has been triaged and categorized
- [ ] Known issues have clear severity assignments and ship/block decisions
- [ ] Risk assessment covers all eight dimensions
- [ ] Rollback plan is documented and has been tested
- [ ] Recommendation is supported by evidence, not opinion
- [ ] Stakeholder signoff matrix includes all required roles
- [ ] Post-release monitoring plan is defined

## Edge Cases

- **Hotfix releases**: Streamline the process -- focus on the fix validation and regression around the affected area; skip full regression if time-constrained
- **Feature flag releases**: Document flag state; signoff may cover the flag-off state with a separate signoff for flag-on activation
- **Multi-service releases with dependencies**: Document deployment order, verify inter-service compatibility, and define rollback sequence
- **Releases with data migrations**: Require separate migration dry-run results and rollback validation
- **Weekend or off-hours releases**: Ensure on-call coverage is confirmed and escalation paths are staffed
