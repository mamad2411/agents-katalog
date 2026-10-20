---
name: security-finding-backlog-triage
description: >
  Guides ongoing triage and prioritization of the accumulated SAST/DAST/
  SCA finding queue — scoring severity against real exploitability and a
  tool's known false-positive rate, and routing findings to a fix-now,
  scheduled, or won't-fix lane instead of a single undifferentiated
  backlog. Use when the user asks to "triage our security finding
  backlog", "why do we have 4,000 open Snyk/Semgrep findings and no plan
  to fix them", "prioritize which vulnerabilities to fix first", "set up
  a severity/exploitability scoring model", or "reduce our security
  finding backlog without ignoring real risk". Distinct from designing
  the pipeline gates that produce findings in the first place (see
  secure-cicd-gates) and from the single-CVE fire-drill response covered
  in critical-vulnerability-emergency-response.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Security Finding Backlog Triage

## Purpose

Every SAST, DAST, and SCA tool a team runs produces a steady stream of
findings, and left unmanaged that stream becomes an unbounded backlog —
thousands of open items with no consistent ranking, no owner, and no
realistic path to zero. A raw severity label (`CRITICAL`/`HIGH`/`MEDIUM`/
`LOW`) from a single tool is a poor sole ranking signal: it says nothing
about whether the vulnerable code path is actually reachable by an
attacker, whether the finding is one of a scanner's known
false-positive-prone rule classes, or whether it sits in a system that
faces the internet versus an isolated internal batch job. This skill
covers the ongoing, steady-state discipline of triaging an existing
finding backlog — scoring severity, exploitability, and false-positive
likelihood together to produce a defensible fix-order, and routing each
finding to a lane (fix now, scheduled remediation, accepted risk,
false positive) with an owner and a re-review date. It is the day-to-day
counterpart to [secure-cicd-gates](../secure-cicd-gates/SKILL.md), which
designs where findings enter the pipeline in the first place, and to
[security-gate-exception-management](../security-gate-exception-management/SKILL.md),
which governs how an individual accepted-risk decision is recorded and
expires.

## When to use

- The user has an existing SAST/DAST/SCA finding backlog (from
  SonarQube, Semgrep, Snyk, Trivy, a DefectDojo/AppSec dashboard, etc.)
  numbering in the hundreds or thousands, with no working prioritization
  scheme.
- The user asks "what should we fix first" across findings from multiple
  tools with different, incompatible native severity scales.
- A security or platform team wants to design (or revise) a
  severity-times-exploitability scoring model to replace raw tool
  severity as the sole ranking signal.
- The user wants to distinguish "real, exploitable, fix now" findings
  from "technically true but not reachable/not exploitable in context"
  findings without simply ignoring the latter category.
- A backlog review cadence (weekly/monthly triage meeting) needs a
  repeatable process and a scoring rubric instead of ad hoc discussion.
- The user wants to measure and reduce a tool's false-positive rate as
  input to how much weight its findings should carry in prioritization.

## Prerequisites & environment

- At least one operating scanner producing findings in a
  queryable/exportable form (SARIF, tool-native JSON/API, or a
  centralized AppSec dashboard such as DefectDojo, GitHub code scanning,
  or a SIEM ingesting scan output). This skill triages what scanners
  already produce; if no scanning exists yet, start with
  [sast-integration](../sast-integration/SKILL.md),
  [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md),
  or [dast-integration](../dast-integration/SKILL.md) first.
- Enough system/architecture context to assess reachability and exposure
  per finding — which services are internet-facing, which run with
  elevated privileges, which process untrusted input — typically an
  asset inventory or service catalog, even an informal one.
- A ticketing system (Jira, GitHub Issues, Linear) to assign owners and
  due dates per triage lane, rather than tracking decisions only inside
  the scanner's own UI comment field.
- Organizational agreement on who has authority to move a finding into
  the "accepted risk" lane — see
  [security-gate-exception-management](../security-gate-exception-management/SKILL.md)
  for the exception-approval workflow this hands off to.
- A defined remediation SLA by severity tier (e.g. from
  [secure-cicd-gates](../secure-cicd-gates/SKILL.md)'s severity-to-action
  table) that triage scoring feeds into — triage without an SLA produces
  a ranked list nobody is accountable for actually working through.

## Step-by-step guidance

1. **Normalize findings from all tools into one schema** before scoring
   anything — a common cause of "which of these three CRITICALs do I fix
   first" confusion is that each tool's severity scale isn't directly
   comparable:
   ```
   finding_id, tool, native_severity, cve_or_rule_id, component,
   file_or_endpoint, first_seen, age_days, internet_facing (bool),
   requires_auth (bool), known_exploit_available (bool)
   ```
   Export via SARIF (SAST/DAST tools generally support it) or each
   tool's API/JSON export, and land it in one place — a spreadsheet is a
   legitimate starting point; a dashboard like DefectDojo is the
   steady-state target once volume justifies it.

2. **Score each finding on three independent axes**, not raw severity
   alone:
   - **Severity** — the tool's own rating (CVSS base score for
     CVE-based SCA findings; `ERROR`/`WARNING` or similar for SAST/DAST
     rule findings), kept as one input, not the final answer.
   - **Exploitability** — is the vulnerable code path actually
     reachable? A SQL-injection finding in a function only ever called
     with hardcoded, non-user-controlled arguments scores materially
     lower than the identical rule firing on a public API handler. For
     SCA specifically, check whether the vulnerable function in the
     dependency is actually invoked by the application (`grype` and
     several SCA tools support call-graph-aware "reachability"
     analysis) rather than assuming every CVE in an installed package
     is equally live.
   - **Exposure** — does this run on an internet-facing service, with
     elevated privileges, or process untrusted/external input? A
     `CRITICAL` CVE in a library used only by an internal offline batch
     job is a different risk than the same CVE in a public API
     gateway.
   Combine as a simple weighted score rather than a black box, so the
   ranking is explainable to an engineer who disagrees with it:
   ```
   priority_score = severity_weight * exploitability_weight * exposure_weight
   # e.g. severity(1-4) * exploitability(0.25/0.5/0.75/1.0) * exposure(1.0/1.5/2.0)
   ```

3. **Fold in per-tool/per-rule false-positive rate as a discount
   factor**, tracked over time (see
   [security-posture-metrics-and-trend-analysis](../security-posture-metrics-and-trend-analysis/SKILL.md)
   for how to measure it). A specific SAST rule with a historical 80%
   dismissal rate on this codebase should not carry the same weight in
   the initial ranking as a rule that has never once been marked a false
   positive — but a high false-positive *rate* is a signal to fix the
   rule/tuning, not a license to permanently deprioritize everything it
   finds.

4. **Route every finding to exactly one lane** as the outcome of triage,
   not left un-lane-d in a general backlog:
   - **Fix now** — high score, within current sprint/SLA window, ticket
     created with an owner.
   - **Scheduled** — real finding, lower urgency; ticket created with a
     due date consistent with its severity's SLA, tracked against that
     date.
   - **Accepted risk / exception** — real finding, deliberately not
     fixed for a documented reason (compensating control, low
     exploitability confirmed, cost disproportionate to risk); hand off
     to
     [security-gate-exception-management](../security-gate-exception-management/SKILL.md)
     for the formal expiring-exception record — never leave this as an
     informal "we decided not to fix it" comment with no expiry.
   - **False positive** — confirmed non-issue; suppress in the scanner
     with a justification comment (per the suppression guidance in
     [sast-integration](../sast-integration/SKILL.md) and
     [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)),
     and log it so the tool/rule's false-positive rate metric reflects
     it.

5. **Batch triage by pattern, not one finding at a time**, when volume is
   high. Group findings by rule ID/CVE and by component — 200 instances
   of the same low-context-risk rule across test fixtures can be
   triaged as one decision rather than 200 individual reviews; genuinely
   distinct high-severity findings in production code paths still need
   individual review.

6. **Run a recurring triage cadence** (weekly for new criticals/highs,
   monthly for the broader backlog) with a fixed, small standing agenda:
   new findings since last review, SLA-breaching items, and exceptions
   nearing expiry. A triage meeting with no fixed cadence degrades into
   "whenever someone has time," and the backlog grows faster than it's
   worked down.

7. **Report backlog size and age distribution, not just a raw count**,
   to leadership — "4,200 open findings" is not actionable; "180 exceed
   their SLA, oldest is 340 days, concentrated in three legacy services"
   points at where to actually intervene. See
   [security-posture-metrics-and-trend-analysis](../security-posture-metrics-and-trend-analysis/SKILL.md)
   for the trend-tracking this feeds.

## Best practices

- Score exploitability and exposure alongside severity as a matter of
  process, not only for a handful of contested findings — a scoring
  model applied inconsistently just relocates the argument from "is this
  really critical" to "why did this one get the special treatment."
- Batch-triage by rule/CVE pattern for volume; reserve individual review
  for genuinely high-stakes findings — triaging 3,000 items one at a
  time is itself the reason backlogs never get worked down.
- Track false-positive rate per rule/tool as a first-class metric and
  feed it back into tuning (fewer default rules, better exclusions) —
  discounting priority is a triage workaround, not a fix for a
  consistently noisy rule.
- Give every finding exactly one lane and one owner at the end of
  triage — a finding left in "still deciding" indefinitely is
  functionally the same as ignored, just with extra bookkeeping.
- Re-triage on new information, not just on a schedule — a finding
  scored low-exploitability because a code path was believed unreachable
  needs immediate re-scoring the moment that code path becomes reachable
  (e.g. a new caller is added), independent of the next scheduled
  review.
- Keep the scoring model simple enough to explain in one sentence to an
  engineer questioning a ranking — an opaque scoring formula erodes
  trust in triage decisions just as much as no scoring at all.

## Common pitfalls

- **Symptom:** The backlog has thousands of open findings, all nominally
  "in triage," and nobody can say what the team is actually working on
  this week.
  **Fix:** Force every finding into one of the four lanes (fix now,
  scheduled, accepted risk, false positive) as the definition of "triaged" —
  a finding with no lane assignment isn't triaged yet, regardless of how
  long it's been open.

- **Symptom:** Prioritization is entirely driven by each tool's native
  severity label, so a `HIGH` SCA finding in an unreachable internal
  utility outranks a `MEDIUM` SAST finding in a public-facing auth
  handler.
  **Fix:** Apply the severity × exploitability × exposure scoring model
  consistently, and use dependency reachability analysis (where the SCA
  tool supports it) rather than assuming every listed CVE in an
  installed package is equally live.

- **Symptom:** A team marks a large batch of findings "false positive" to
  clear the backlog dashboard before a leadership review, without
  individually verifying each one.
  **Fix:** Require a specific justification per suppression (or per
  batch of genuinely identical findings), and periodically audit a
  sample of "false positive" dispositions — a backlog that looks clean
  because of unverified mass-dismissal is worse than a visibly large,
  honestly-triaged one.

- **Symptom:** The same handful of "accepted risk" findings have been
  carried forward in every triage meeting for over a year with no
  formal record of who approved the acceptance or when it expires.
  **Fix:** Every accepted-risk disposition must go through
  [security-gate-exception-management](../security-gate-exception-management/SKILL.md)'s
  exception process with an explicit owner and expiry — an informal
  "we've always just left this one" is exactly the unbounded waiver list
  that process exists to prevent.

- **Symptom:** Triage focuses entirely on the newest findings each week,
  and a long tail of old, unaddressed high-severity items quietly ages
  past its SLA without anyone noticing.
  **Fix:** Make SLA-breaching items a fixed line item in every triage
  meeting's agenda, sorted by age, not just a review of what's new since
  last time.

## Worked example

A platform team inherits a service with 1,150 open findings across
Semgrep (SAST), Trivy (SCA/container), and OWASP ZAP (DAST baseline),
and no prior triage process.

Normalized export (illustrative excerpt, from each tool's SARIF/JSON):
```
finding_id | tool    | native_sev | rule/cve            | component        | internet_facing | first_seen
F-0231     | trivy   | CRITICAL   | CVE-2024-EXAMPLE-1  | libfoo@2.3.0     | true             | 2026-02-11
F-0894     | semgrep | ERROR      | sqli-flask-orm      | app/admin/bulk.py| false            | 2025-11-03
F-1042     | trivy   | HIGH       | CVE-2023-EXAMPLE-2  | build-tool@1.1.0 | false (build-only)| 2025-09-22
F-1103     | zap     | Medium     | missing-csp-header  | /api/v1/*        | true             | 2026-01-04
```
(`CVE-2024-EXAMPLE-1` and `CVE-2023-EXAMPLE-2` are illustrative
placeholders, not real CVE identifiers.)

Scoring (severity 1-4, exploitability 0.25-1.0, exposure 1.0-2.0):
```
F-0231: 4 * 1.0 (public endpoint, no auth required to trigger) * 2.0 (internet-facing) = 8.0  -> Fix now
F-0894: 4 * 0.5 (admin-only route, requires authenticated staff session) * 1.5 = 3.0          -> Scheduled (SLA: 2 weeks)
F-1042: 3 * 0.25 (build-tool only, never shipped/runs in prod) * 1.0 (internal build env)= 0.75 -> Accepted risk (build-only exposure)
F-1103: 2 * 0.75 (real gap, low direct exploitability alone) * 2.0 = 3.0                        -> Scheduled (SLA: 90 days)
```

Triage outcome recorded in the tracking ticket system:
- F-0231 → JIRA-SEC-441, fix now, owner: payments-team, due in 48h
  (matches the critical-severity SLA).
- F-0894 → JIRA-SEC-442, scheduled, due in 2 weeks.
- F-1042 → routed to
  [security-gate-exception-management](../security-gate-exception-management/SKILL.md),
  exception granted with a 2026-12-01 expiry and owner recorded, not left
  as an unowned backlog item.
- F-1103 → JIRA-SEC-443, scheduled, due in 90 days per medium-severity
  SLA.

The remaining ~1,146 findings are batch-triaged by grouping on
`rule/cve` and `component`: 340 turn out to be the same `missing-csp-header`
ZAP finding repeated per endpoint (one scheduled fix at the framework
middleware level closes all of them at once), and roughly 200 Trivy
findings trace to a single outdated base image (one base-image bump
fix, see [container-image-hardening](../container-image-hardening/SKILL.md)),
rather than requiring 540 individual triage decisions.

## Cross-references

- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — designs where and
  when findings enter the pipeline and the severity-to-action table this
  skill's scoring model feeds into.
- [critical-vulnerability-emergency-response](../critical-vulnerability-emergency-response/SKILL.md) —
  the accelerated, out-of-band process for a single newly-disclosed
  critical CVE, versus this skill's steady-state ongoing backlog
  management.
- [security-gate-exception-management](../security-gate-exception-management/SKILL.md) —
  the formal, expiring-exception workflow that an "accepted risk" triage
  lane hands off to.
- [security-posture-metrics-and-trend-analysis](../security-posture-metrics-and-trend-analysis/SKILL.md) —
  tracking backlog age distribution, mean-time-to-remediate, and
  false-positive rate over time as inputs back into this triage process.
- [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md) —
  the SCA-specific finding source and reachability-analysis tooling
  referenced in the scoring step.
