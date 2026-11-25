---
name: qa-release-signoff
version: 1.0.0
description: Run a release sign-off checklist that turns test results, open bugs, and risk into a defensible go/no-go call.
author: matrixx0070
tags: [qa, release, signoff, go-no-go, risk]
capabilities: []
---

## When to use

At the gate before a release ships — when someone must say "yes, this is safe to release" and own that call. Sign-off converts scattered signals (test runs, open bugs, coverage, known risks) into one recorded decision with rationale, so the choice is defensible and the accepted risk is explicit.

**Not for:** deciding what to test (see qa-test-plan), the deploy runbook mechanics itself, or mid-development status updates. Sign-off is the final quality gate, not the plan and not the deployment steps.

## Method

1. **Confirm exit criteria are met** — pull the release's planned exit criteria and check each. Decision point: if any is unmet, that's a blocker unless explicitly waived with rationale.
2. **Review open bugs by severity.** Decision point: any open Critical or High on a shipped path is a default no-go; Medium/Low with a documented workaround can ship as "known issues."
3. **Verify test execution:** required suites ran and passed on the release build (not an old build). Note coverage of High-risk areas specifically; a green suite that skipped the money path is not sign-off.
4. **Assess residual risk.** List what wasn't tested, what's shipping with known issues, and what could go wrong in production.
5. **Check rollback readiness** — is there a tested way back if it fails? A go with no rollback is a bigger risk than a no-go.
6. **Make the call and record it:** GO, NO-GO, or GO-WITH-CONDITIONS. Name the accepted risks, the owner, and the date. If NO-GO, list exactly what must change to flip it.

## Example

```
Release: mobile checkout v5.1, build 5.1.0-rc3.
Exit criteria: 5/6 met; perf test not run -> waived (no perf-sensitive change).
Open bugs: 0 Critical, 0 High, 3 Medium (all with workarounds -> known issues).
Suites: unit+integration green on rc3; e2e checkout journey pass. High-risk (payment) covered.
Residual risk: Apple Pay untested on iOS 26 (0.3% users) -> monitor.
Rollback: feature flag, tested off-switch.
CALL: GO-WITH-CONDITIONS — flag on for 10% first, watch payment error rate 24h. Owner: QA lead, 2026-07-11.
```

## Pitfalls

- **Rubber-stamp sign-off** — "tests are green" without checking they ran on THIS build or covered High-risk paths.
- **Silent waivers** — skipping an exit criterion with no recorded rationale.
- **No rollback plan** — saying GO with no tested way back.
- **Owner-less call** — a decision nobody's name is on; when it breaks, nobody accepts the risk they took.

## Output format

```
Release: <name + exact build/rc>
Exit criteria: <met / unmet — waivers with rationale>
Open bugs: Critical <n> | High <n> | Medium <n> (known issues listed)
Test execution: <suites run on this build, High-risk coverage confirmed>
Residual risk: <untested areas, known issues, prod what-ifs>
Rollback readiness: <mechanism + tested?>
DECISION: GO / NO-GO / GO-WITH-CONDITIONS
  Conditions/monitoring: <if conditional>
  Accepted risks: <explicit list>
  Owner + date: <name, date>
  If NO-GO: <what must change to flip>
```
