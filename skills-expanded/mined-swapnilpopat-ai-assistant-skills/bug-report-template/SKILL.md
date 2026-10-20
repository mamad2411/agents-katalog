---
name: bug-report-template
description: Author high-signal bug reports — title, environment, steps, expected vs. actual, evidence, severity vs. priority, scope, regression status. Use when filing or coaching teams to file bugs that get triaged and fixed quickly.
source: self
date_added: 2026-05-01
---

# Bug Report Template

A bug report is the input to a triage decision. Quality of the report drives time-to-triage, time-to-fix, and the chance of a real fix vs. a "can't reproduce" close.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Tracker | Jira (Xray/Zephyr), Linear, GitHub Issues, Azure Boards |
| Evidence | Screenshot/Loom, HAR, console + network logs, traceparent → backend trace, Sentry/Datadog issue link |
| Schema | Title, env, repro steps, expected, actual, evidence, severity, priority, scope, frequency, regression, workaround |
| Templates | Issue templates in repo / Jira request types / Linear templates |

## When to Use

- Filing a defect from any source (test run, customer report, exploratory session, monitoring alert).
- Reviewing/triaging incoming reports.
- Coaching engineers / support / customers to file usable bugs.

## Template (paste-ready)

```markdown
## Title
<area> — <short, observable behavior>: <what's wrong>
e.g., Checkout — clicking "Place order" twice creates duplicate charges

## Environment
- Build / version: orders-api v3.14.0 (sha a1b2c3)
- Web build: web-shop @ deploy 2026-04-30T14:22Z
- URL: https://shop.example.com/checkout
- Browser / OS / device: Chrome 130 / macOS 15.4 / MacBook Pro M3
- Account / role / feature flags: std-merchant; flags=`fast-checkout=on`
- Region: eu-west-1
- Time of occurrence: 2026-04-30T15:08Z (±30s)

## Preconditions
- Logged in as merchant std-merchant
- Cart contains 1 × SKU-A (€42.00)
- Card ending 4242 saved

## Steps to reproduce
1. Open /cart
2. Click "Place order"
3. Within 200ms, click "Place order" again

## Expected
- Exactly 1 order created
- Second click is no-op (button disabled or idempotent server-side)

## Actual
- 2 orders created
- 2 charges visible in Stripe (`pi_3Pa...` and `pi_3Pb...`)

## Evidence
- Loom: <link>
- Screenshot: <link>
- HAR: <link>
- Server trace: <Tempo/Jaeger link with traceparent>
- Sentry issue: <link>

## Severity
S1 (data corruption: duplicate financial transaction)

## Priority
P1 (revenue impact, customer-facing)

## Scope
- Affects: ~0.4% of checkouts (estimated from rage-click metric)
- Versions: appears since v3.13 (2026-04-12)
- Regression: yes — v3.12 had button disable-on-submit

## Workaround
None usable; refunds processed manually

## Linked
- Requirement: REQ-PAY-7
- Related test: TC-PAY-0142
- Linked PR (if known): #4821
```

## Severity vs. Priority — keep them separate

| Severity | Definition | Examples |
| --- | --- | --- |
| S1 Critical | Data corruption, security, full outage | Duplicate charge, data loss, auth bypass |
| S2 High | Major function broken; no good workaround | Cart fails for 1 of 3 browsers |
| S3 Medium | Important defect, workaround exists | Filter X returns wrong order but searchable |
| S4 Low | Cosmetic / minor | Misaligned label |

| Priority | Definition |
| --- | --- |
| P1 | Fix now (block release) |
| P2 | Fix this sprint |
| P3 | Backlog, schedule |
| P4 | Nice to have |

A cosmetic issue on the marketing homepage during launch can be S4/P1. A data-corruption bug behind a flag turned off can be S1/P3.

## Triage Pass/Fail Heuristics

A report is **triageable** if a stranger can reproduce it without asking. If any of these is missing, push back:

- Steps reproducible from a clean session
- Expected vs. Actual both observable
- Evidence (one of: screencast, HAR, trace, log link)
- Build/version + environment
- Severity rationale (impact, scope, frequency)

## Issue Template (.github/ISSUE_TEMPLATE/bug.yml)

```yaml
name: 🐞 Bug
description: A defect report
title: "[bug] "
labels: ["bug","triage"]
body:
  - type: textarea
    id: env
    attributes: { label: Environment, value: "Build:\nURL:\nBrowser/OS:\nUser/Flags:" }
    validations: { required: true }
  - type: textarea
    id: steps
    attributes: { label: Steps to reproduce, render: markdown }
    validations: { required: true }
  - type: textarea
    id: expected
    attributes: { label: Expected }
  - type: textarea
    id: actual
    attributes: { label: Actual }
  - type: textarea
    id: evidence
    attributes: { label: Evidence (Loom, HAR, traceparent, Sentry) }
  - type: dropdown
    id: severity
    attributes: { label: Severity, options: [S1, S2, S3, S4] }
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Title is "doesn't work" | Title = area + observable behavior + what's wrong |
| Steps assume hidden state | List preconditions and start from clean session |
| Expected = "should be correct" | Expected must be observable and exact |
| No evidence | Loom screencast in 30s — non-negotiable |
| Severity = Priority | Keep separate; both required for triage |
| Filed against monolithic "bugs" project | Route by area for routing, but use a single template |
| Customer-paraphrased, no repro | Convert support tickets via QA before filing |

## Output Format

Use the template above; render it identically across Jira, Linear, GitHub. The triage decision belongs in the triage thread, not the bug body.

## References

- IEEE 1044 — Standard Classification for Software Anomalies
- Cem Kaner — *Lessons Learned in Software Testing* (defect reports)
- Atlassian — Severity vs. Priority guidance
- Linear / GitHub issue template docs
