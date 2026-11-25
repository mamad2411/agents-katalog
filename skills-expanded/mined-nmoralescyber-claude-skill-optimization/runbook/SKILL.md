---
name: runbook
description: Creates or updates operational runbooks — step-by-step procedures any operator (human or AI) can execute reliably under pressure, including at 3 AM during an incident. Use when the user says document this process, write a runbook for [task], turn this into a runbook, build an incident response procedure, create a playbook for [scenario], document the steps for [recurring task], write the IR procedure, build the cert rotation playbook, or describes any procedure that needs to be repeatable, auditable, executable by someone other than the original author, or survivable under cognitive load. Specializes in cybersecurity operations: incident response (with Puerto Rico-specific notification — DACO for consumer data, OCIF for financial customer data, Ley Núm. 111-2005 timing), security automation, compliance evidence collection (SOC 2, ISO 27001, HIPAA, GDPR, PCI-DSS), access provisioning/deprovisioning, certificate and secret rotation, vulnerability triage, backup restoration, breach notification (with bilingual Spanish/English customer-facing comms for Puerto Rico audience). Includes trigger conditions, prerequisites, exact commands (not vague descriptions), validation checks between every destructive step, rollback per step, escalation chains with names + phone + Slack, time annotations, MTTR/RTO/RPO targets, and audit trail. Do NOT use for process documentation that needs RACI/swimlane flowchart formality (use operations:process-doc), one-off informal notes (just write them), legal/compliance program tracking over time (use operations:compliance-tracking), templated outbound communications like breach notification letters or DSR responses (use legal:legal-response), or quick how-to questions (just answer them). Defining characteristic: "executable procedure with exact commands, validation, rollback, and escalation — works at 3 AM under stress."
---

# Runbook

Creates step-by-step operational procedures executable under pressure by anyone with appropriate access. Tuned for cybersecurity operations and Puerto Rico regulatory context.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Writing a procedure for IR, security ops, ITGC | Documenting a business process with RACI + swimlane flowchart → `operations:process-doc` |
| Procedure must be executable at 3 AM by on-call | Procedure is informal one-off → just write notes |
| Procedure needs validation, rollback, escalation | Tracking ongoing compliance program over time (evidence inventory, control status) → `operations:compliance-tracking` |
| Procedure is operational (you DO things) | Templated outbound communication (breach notice letter, DSR reply, NDA decline) → `legal:legal-response` |
| Procedure runs dozens/hundreds of times | Question is conceptual ("how does X work?") → answer directly |
| Procedure needs auditable execution log | Decision needs risk classification, not steps → `legal:legal-risk-assessment` or `operations:risk-assessment` |

**Cross-skill chains:**
- IR runbook references `legal:legal-response` for the templated breach notification text (don't re-implement legal text inside the runbook — link to it)
- Compliance evidence runbook updates `operations:compliance-tracking` records on completion (audit trail)
- IR runbook may chain FROM `customer-support:customer-research` (research the affected customer first) and TO `customer-support:customer-escalation` (notify CSM) and `legal:legal-response` (regulator notification text)

## Core principles for runbooks that don't fail under pressure

1. **Exact commands, not gestures.** "Restart the database" is gesture. `sudo systemctl restart postgresql-15` is a command. Runbooks fail at 3 AM because they're written for daytime brains.

2. **Validation between every destructive step.** After each state-changing step, the runbook checks the change took effect before proceeding. Otherwise you cascade failures.

3. **Rollback at every decision point.** If step 5 fails, what's the rollback for steps 1-4? Mandatory, not optional. If no rollback is possible, write `NO ROLLBACK — verify pre-flight extra carefully` explicitly.

4. **Pre-flight checks first.** Before doing anything: verify access, verify environment (prod vs. staging — fingerprint check, not assumption), verify dependencies UP, verify no concurrent conflicting operation.

5. **Escalation chain at the top.** Names + phone + Slack handle. "The team" doesn't get paged.

6. **Time annotations.** Each step has expected duration. If it takes 3x expected, that's a signal something is wrong. Whole-runbook MTTR target stated up top.

7. **Cognitive-load reduction.** At 3 AM the operator is at half capacity. Use copy-pasteable command blocks. Avoid embedded narrative in steps. One decision per step max.

8. **Dry-run path required for destructive procedures.** Every runbook that touches prod must have a `--dry-run` or staging equivalent documented.

9. **Bilingual customer-facing text where the audience is bilingual.** For Puerto Rico customer comms (breach notification, outage notice), provide both Spanish and English templates side-by-side OR explicitly link to `legal:legal-response` for the bilingual templated version.

10. **The runbook is the source of truth.** If reality differs from the runbook, fix the runbook before continuing — or stop.

11. **Blast radius declared per destructive step.** Each state-changing step states what it touches: "BLAST RADIUS: prod database `users` table — affects all logged-in sessions." Operators decide go/no-go with eyes open.

12. **Two-person rule for severity-Critical destructive steps.** If a step's failure would breach SLA or expose data, require a named second operator to confirm before execution. Written into the step.

## Standard runbook anatomy

Every runbook produced includes ALL of these sections. Skip none. Even when "not applicable," write `N/A — [reason]`.

```markdown
# Runbook: [Title]

**Owner:** [Named individual + named backup, with contact]
**Last validated:** YYYY-MM-DD by [name]
**Next validation due:** YYYY-MM-DD
**Severity if executed wrong:** Critical | High | Medium | Low
**MTTR target (whole runbook):** X minutes
**RTO / RPO (if recovery procedure):** X / Y
**Dry-run available:** Yes — see "Dry-run mode" section / No — explain why

## Trigger conditions
[Specific conditions that mean THIS runbook should run, not a different one.]

## Pre-flight checks (must all pass before starting)
- [ ] Access: [specific roles/permissions needed; how to verify you have them]
- [ ] Environment fingerprint: [prod URL hash, account ID, cluster name — not just "make sure it's prod"]
- [ ] Dependencies: [list services that must be UP; how to verify each]
- [ ] Conflicts: [list ongoing operations that block this runbook; how to check]
- [ ] Notification: [who must be paged BEFORE starting; with channel]
- [ ] Audit log: open the execution log entry now (so partial executions are still recorded)

## Escalation chain
1. Primary: [name + phone + Slack] — pager rotation link
2. Backup: [name + phone + Slack]
3. After 30 min unresolved: [escalation path]
4. After 2 hr unresolved: [executive escalation]
5. Legal/comms trigger: [when to loop in counsel + comms — e.g., suspected data exposure, customer impact >X, regulatory clock starting]

## Procedure

### Step 1: [Name]
**Action (copy-paste):**
```
exact command here
```
**Expected duration:** ~30 sec
**Validation:**
```
command to verify
```
Expected output: [what you should see]
**If validation fails:** [exact remediation OR rollback to step 0 OR escalate]
**Rollback for this step:** [exact reverse command, or N/A — explain]

### Step 2: ...

## Rollback procedure (whole runbook)
[Reverse-order steps to undo everything if you need to abort. Each with its own validation.]

## Post-execution verification
- [ ] [Outcome 1 confirmed — with check command]
- [ ] [Outcome 2 confirmed]
- [ ] Notification sent to [stakeholders + channel]
- [ ] Logged in [ticketing system / audit log location]
- [ ] Execution log closed with: started-at, finished-at, operator, outcome, deviations

## Known failure modes
| Symptom | Cause | Fix |
|---|---|---|
| ... | ... | ... |

## Dry-run mode (if applicable)
[Exact equivalent commands that exercise the procedure without state change — staging environment, --dry-run flags, etc.]

## Audit trail
- Where execution logs are stored (path / system)
- Retention period
- Who reviews logs and how often

## Change log
| Date | Author | Change | Validated by |
|---|---|---|---|
| ... | ... | ... | ... |
```

## Cybersecurity runbook templates

### Template 1 — Incident response (suspected intrusion)

Trigger: SIEM/EDR alert, anomaly detection, customer report, insider observation.

Required sections beyond standard anatomy:
- **Containment first** (isolate affected hosts/accounts BEFORE investigation — don't tip off the attacker; preserve evidence in the act of containing)
- **Evidence preservation** (snapshot disk, capture memory, preserve logs with hash; chain of custody log; do this BEFORE remediation)
- **Investigation triage** (what was accessed, what was exfiltrated, lateral movement check, persistence check)
- **Eradication** (remove persistence, rotate ALL potentially exposed credentials, patch entry vector)
- **Recovery** (restore from clean backup verified pre-incident, monitor heavily for re-infection 30+ days)
- **Notification (with regulatory clocks)** — see "Puerto Rico notification matrix" below; GDPR 72hr; varies by US state; SEC 4-day disclosure for material cyber incidents on public co's
- **Customer notification** — chain to `legal:legal-response` for the templated text; runbook handles WHEN/HOW/TO-WHOM
- **Post-incident review** (RCA, timeline, lessons, runbook updates) — separate runbook, scheduled within 7 days
- **MTTC (mean time to contain) target** stated up top alongside MTTR

### Puerto Rico notification matrix (bake into IR runbooks)

| Trigger | Regulator / law | Clock | Who notifies |
|---|---|---|---|
| Consumer PII compromised | DACO (Departamento de Asuntos del Consumidor) under Ley Núm. 111-2005 | "Most expedient time possible without unreasonable delay" — internal default 72hr | Legal counsel files; runbook flags |
| Financial-services customer data compromised | OCIF (Oficina del Comisionado de Instituciones Financieras) | Per OCIF guidance — typically immediate notification to regulator | Legal + CISO joint |
| Health data | HIPAA Breach Notification Rule | 60 days to affected individuals; >500 affected = HHS + media | Privacy officer |
| EU resident data | GDPR Art. 33 | 72 hr to supervisory authority | DPO |
| Public company material incident | SEC Form 8-K Item 1.05 | 4 business days from materiality determination | Legal + IR + CFO |

The runbook does NOT contain the legal text — it links to `legal:legal-response` (which has the bilingual Spanish/English templates). The runbook handles the operational trigger: "Notify legal counsel within 30 min of containment confirmation; legal initiates `legal:legal-response` for regulator + customer letters."

### Template 2 — Security automation (recurring scheduled task)

Trigger: cron, scheduled job, or manual execution per cadence.

Required sections:
- **Schedule** (cron expression + timezone + drift tolerance — e.g., "0 2 * * 1 America/Puerto_Rico, ±15 min acceptable")
- **Authentication** (which service account, which secret rotation pattern, where the secret lives)
- **Output destination** (logs, reports, dashboard updates)
- **Failure detection** (alerting on null output, malformed output, missed runs — name the alert + recipient)
- **Idempotency check** (safe to re-run if previous run partially completed?)
- **Backoff/retry** (exponential, max attempts, what happens after exhaustion)

Examples: weekly vulnerability scan triage, monthly access review, quarterly cert rotation, daily backup integrity check, hourly endpoint posture sync.

### Template 3 — Compliance evidence collection

Trigger: framework requirement (SOC 2 control, ISO 27001 control, GDPR Art., PCI-DSS req, HIPAA safeguard) on quarterly/annual cycle, or audit kickoff.

Required sections:
- **Control mapped** (framework + control ID + control wording)
- **Evidence type** (log export, screenshot with timestamp + URL bar visible, signed attestation, config dump)
- **Collection procedure** (exact commands or UI click-path with selectors)
- **Storage location** (GRC platform location, naming convention `YYYY-Q#-FRAMEWORK-CONTROL-EVIDENCE-TYPE`, retention period)
- **Reviewer** (who signs off the evidence is complete and current)
- **Mapping notes** (which other frameworks does this same evidence satisfy — avoid duplicate work)
- **Update to `operations:compliance-tracking`** (chain — once evidence collected, mark control as "fresh" in the tracking system)

### Template 4 — Access provisioning / deprovisioning

Trigger: new hire, contractor onboarding, role change, departure (voluntary/involuntary), contract end.

Required sections:
- **Identity creation** (IdP provisioning, MFA enrollment, access groups by role)
- **Application access** (per-app provisioning checklist, with named owner per app)
- **Hardware** (laptop, YubiKey/hardware token, badge — with serial-number capture)
- **Sensitive system access** (separate approval chain, time-bounded, justification logged, recertification cadence)
- **For deprovisioning specifically:** session revocation FIRST, data egress check, equipment return tracking, access log audit, archive vs delete decision per data class
- **Deadline** (most regulators expect access removal within 24 hours of termination; immediate for involuntary terminations — runbook differentiates)
- **Audit log entry** with start/end timestamps + named approver

### Template 5 — Certificate / secret rotation

Trigger: scheduled rotation date, breach suspicion, key compromise, departing employee with shared-secret access.

Required sections:
- **Inventory check** (where is this cert/secret used — every dependency listed; auto-discovery query if available)
- **Generation** (entropy source, length, algorithm — pinned to current best practice)
- **Distribution** (rolling deployment to dependencies; with verify-each)
- **Validation** (each dependency confirmed using the new value with a positive check)
- **Old-value revocation** (with verification window — don't revoke until ALL consumers confirmed switched; specify the window length)
- **Audit log entry** (who, when, why, old-value hash, new-value hash)
- **Dry-run** (rotation in staging environment first for any cert touching customer-facing systems)

### Template 6 — Backup restoration test

Trigger: monthly/quarterly DR test, audit requirement, real recovery scenario.

Required sections:
- **Restoration target** (test environment, NEVER prod for tests — fingerprint check)
- **Backup selection** (which date, which tier — full / incremental / snapshot; verify backup integrity hash before restore)
- **Restore command** (exact, with environment safety guards)
- **Integrity verification** (row counts, schema match, application boots, test data accessible, sample queries return expected)
- **Performance benchmark** (how long did it take vs. RTO commitment — record in audit log)
- **Findings** (any issues that would have blocked real recovery)
- **Update to `operations:compliance-tracking`** (DR test = evidence for BC/DR control)

### Template 7 — Vulnerability triage (added)

Trigger: new CVE published affecting your stack, scanner finding, customer-reported.

Required sections:
- **Exposure check** (which versions running where; query the asset inventory)
- **Exploitability assessment** (CVSS + EPSS + KEV check + your environment context)
- **Decision** (patch / mitigate / accept — with named approver for accept)
- **Patch deployment** (link to the patch-deployment runbook; do not duplicate)
- **Customer notification trigger** (does this affect customer data? → IR template)
- **Audit log** (CVE ID, decision, approver, timestamp)

## Writing pattern: command formatting

When the runbook includes shell commands:

```
**Step N:** Restart the application server

Command (copy-paste):
  sudo systemctl restart myapp.service

Expected duration: ~15 seconds

Validation:
  systemctl status myapp.service

Expected output:
  Active: active (running)

If validation fails:
  - Check logs: journalctl -u myapp.service -n 50
  - If "address already in use" → wait 60s and retry once
  - If "permission denied" → escalate to ops on-call (escalation §1)
  - If anything else → rollback to step 0 and escalate

Rollback for this step:
  sudo systemctl stop myapp.service && [restore prior state command]
```

This formatting matters. Operators copy-paste under pressure. Every command must be self-contained, complete, copy-pastable, and idempotent where possible.

## Anti-patterns that break runbooks

- **"Check the logs"** — which logs? where? what command? what to look for? what's normal vs. abnormal?
- **"Make sure everything is OK"** — define "OK" with a specific check
- **"You may want to..."** — make a decision; remove optionality during execution
- **"As needed"** — replace with a specific trigger condition
- **"The team will handle..."** — name the individual or role; "the team" doesn't get paged
- **Embedded narrative inside steps** — explain the why in a separate "Background" section, not in the procedure steps
- **Missing rollback** — every destructive step needs a rollback or an explicit `NO ROLLBACK — verify pre-flight extra carefully`
- **Outdated commands** — runbooks must be re-validated quarterly minimum; commands rust
- **No environment fingerprint** — "make sure it's prod" is not a check; provide the URL hash / account ID / cluster name to match
- **Legal text inside an IR runbook** — link to `legal:legal-response` instead; runbook handles WHEN/HOW, legal-response handles WHAT-TO-SAY
- **English-only customer comms for PR audience** — link to bilingual templates in `legal:legal-response`
- **No audit trail** — if the execution wasn't logged, the auditor will assume it didn't happen

## Validation cadence

Every runbook needs scheduled re-validation. Default cadences:

| Runbook category | Re-validate every | Trigger override |
|---|---|---|
| Incident response (active threats) | Quarterly minimum + after any incident execution | After any IR exercise OR real incident — same week |
| Compliance evidence | Before each audit cycle | Framework version change |
| Access provisioning | After any IdP/IAM change | New SaaS app added |
| Cert/secret rotation | Before each rotation | Algorithm deprecation |
| Backup restoration | Quarterly minimum (DR tests USE the runbook to validate it) | Backup tooling change |
| Routine ops (scheduled tasks) | Annually | Schedule change, dependency change |
| Vulnerability triage | Semi-annually | Major scanner/SBOM tooling change |

Re-validation = run through the runbook in a controlled context (dry-run if available, staging if not), fix any drift between runbook and reality, sign + date in the change log. Audit trail entries from real executions also count toward the next validation if they were clean.

### Drift detection between scheduled validations

A runbook is "drifting" — and needs ad-hoc re-validation BEFORE its scheduled date — when ANY of these signal:
- Underlying tooling version bumped (k8s upgrade, EDR major version, IdP migration)
- A step required improvisation during real execution (operator deviated)
- Audit log shows a step taking >2x expected duration repeatedly
- An incident postmortem references this runbook with a "fix the runbook" action item
- Quarterly chaos/fire-drill exercise surfaces a gap

### Sample audit-log entry format

```
runbook_id: ir-suspected-intrusion-v3.2
execution_id: 2026-04-25T03:14:22Z-amorales
operator_primary: amorales
operator_second: jruiz  (two-person rule satisfied)
trigger: SIEM alert SIEM-2026-04-25-0042
started_at: 2026-04-25T03:14:22Z
finished_at: 2026-04-25T04:47:19Z
mttr_target_min: 90
mttr_actual_min: 93
deviations:
  - step 4: validation took 12 min instead of expected 5 min (network latency)
outcome: contained; eradication continuing in followup ticket
followup_tickets:
  - INC-9182 (post-incident review)
  - INC-9183 (cred rotation)
```

## Output

Every runbook this skill produces includes:

1. The full runbook in the standard anatomy above (no skipped sections)
2. Pre-flight checklist as a copy-pastable block (so on-call can run it without re-reading whole runbook)
3. Markdown version + a one-page printable PDF candidate (for physical IR binders — useful in PR during outages)
4. Suggested location to store (path in runbook repo, GRC platform link)
5. Initial validation date scheduled + next validation date set
6. Audit-trail location identified
7. Suggested next runbook to write (chained — e.g., wrote IR runbook → suggest post-incident-review runbook; wrote cert rotation → suggest secret-inventory runbook)
8. Cross-skill chains noted (e.g., "this runbook chains TO `legal:legal-response` for breach text" or "this runbook chains FROM `customer-support:customer-research` for affected-customer context")
