---
name: blue-ir
description: Incident response triage and coordination — build timelines, separate facts from hypotheses, guide containment decisions, and prepare handoff from approved logs, tickets, and redacted artifacts.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, blue-team, forensic]
authorization-required: conditional
evidence-outputs: [incident-notes, timeline, redacted-evidence]
---

# Blue-team incident response — triage and coordination

Use this skill to triage security incidents, build evidence-backed timelines, separate confirmed facts from working hypotheses, and guide containment decisions. Work exclusively from approved logs, tickets, host artifacts, and redacted evidence. Never execute attacker tools, exploit replay, destructive containment, or credential attacks from this skill.

## Required inputs

- Incident ticket or report with initial detection details: what was detected, when, by whom, which systems are affected, and initial severity assessment.
- Approved evidence: log extracts, alert details, EDR telemetry, network flow summaries, forensic artifact summaries, user reports, change records. All must be pre-collected and redacted.
- Asset inventory: affected hosts, their role (workstation, server, domain controller, cloud instance), owner, criticality, and whether they can be isolated.
- Incident response plan or runbook: escalation contacts, communication templates, containment authority, evidence-handling procedures, and regulatory notification requirements.
- Current authorization cache if live query or containment action is needed; otherwise, authorization is conditional on environment access.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when scope, asset, or evidence boundaries exist.
3. `pentest_agent_validate_target` before any target contact or live query.
4. `pentest_agent_check_authorization` before any active validation or environment contact.
5. `pentest_agent_build_command` and `pentest_agent_execute_tool` only for approved defensive read-only tooling.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — incident intake and scope confirmation

1. Review the initial detection: what triggered the incident (alert, user report, external notification, threat-intel), who detected it, and the initial scope (single host, multiple hosts, user account, data exposure).
2. Confirm incident validity: could this be a false positive? Check for known benign triggers (scheduled maintenance, software deployment, penetration test, vulnerability scan, authorized admin activity). If the incident is likely a false positive, document the evidence and close — no further IR workflow needed.
3. Determine the incident severity: critical (active data exfiltration, ransomware execution, domain admin compromise), high (confirmed compromise without data loss yet, privilege escalation detected), medium (suspicious activity requiring investigation, malware on isolated system), low (policy violation, failed attack attempt, phishing email reported by user).
4. Identify the incident commander and communication channel. All further findings go to the incident commander; do not broadcast incident details broadly from this skill.
5. Confirm what is NOT in scope: which systems, data types, or actions are off-limits for IR. Do not exceed scope even for containment.

### Phase 2 — evidence collection and timeline construction

Build a chronological timeline from all available evidence:

1. Start from the earliest known event and extend to the present. For each event, record: timestamp (UTC, normalized from source timezone), event type (log entry, alert, user report, forensic artifact), source system, description, and evidence reference.
2. Separate events into:
   - **Confirmed facts**: events with corroborating evidence from multiple independent sources.
   - **Reported observations**: events from a single source that is considered reliable (EDR alert, SIEM correlation, user report with screenshots).
   - **Working hypotheses**: plausible but unconfirmed inferences. E.g., "attacker likely used credential X to move from Host-A to Host-B because timestamp-A precedes timestamp-B and same user agent was observed."
   - **Unknowns**: gaps in the timeline where evidence is missing or contradictory.
3. Identify the attack phases (per MITRE ATT&CK or similar): Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact.
4. Map each event to the attack phase it belongs to. Identify where phases are missing (e.g., we see Initial Access and Persistence but no Execution — either evidence is missing or the access vector left no logs).

### Phase 3 — scope of compromise assessment

Determine the blast radius:

1. From the timeline, identify all affected systems: hosts with confirmed attacker activity, accounts used by the attacker, data accessed or exfiltrated, cloud resources accessed, and network segments traversed.
2. For each affected system, classify: confirmed compromise (attacker executed commands), suspected compromise (suspicious activity without confirmation), potentially exposed (same network segment or shared credentials), and not affected.
3. Trace credential exposure: which accounts were used? Were those accounts local, domain, or cloud? Were any of them privileged? If a privileged account was compromised, assume all systems that account can access are affected.
4. Trace data exposure: which files, databases, mailboxes, or cloud storage were accessed? Was the access read-only or read-write? Was data exfiltrated (check outbound network flows, cloud audit logs, email forwarding rules)?
5. Document the scope assessment with confidence levels per system. If scope is uncertain, note the uncertainty and what additional evidence would resolve it.

### Phase 4 — containment guidance

Draft containment recommendations for the incident commander. Do NOT execute containment actions from this skill — containment requires authority and operational approval.

1. For each affected system, propose containment actions based on severity and operational impact:
   - **Network isolation**: move the host to a restricted VLAN or apply host-based firewall rules to block all except IR management traffic. This is the safest option but disrupts the service.
   - **Account disable**: disable compromised user and service accounts. If the account is critical for operations, coordinate with the service owner first.
   - **Credential rotation**: force password reset for all accounts that were active on compromised systems during the attack window. Rotate Kerberos tickets, API keys, and OAuth tokens.
   - **Service suspension**: if a compromised service cannot be isolated (cloud function, SaaS integration), suspend it until investigation is complete.
2. For each containment action, assess the operational impact: which services will be disrupted, which users will be affected, what is the expected downtime, and is there a rollback plan.
3. Prioritize containment by risk: active exfiltration or ransomware execution → immediate containment. Historical compromise with no active attacker presence → coordinated containment during maintenance window.
4. Document the containment decision log: action taken, timestamp, authority, affected systems, operational impact observed, and rollback status.

### Phase 5 — evidence preservation for investigation

While containment is ongoing, preserve evidence:

1. For each affected host (before reimaging or isolation), ensure: memory dump (if feasible and authorized), disk image or key forensic artifacts (prefetch, event logs, registry hives, browser history, scheduled tasks, service configurations), and network flow logs for the attack window.
2. Hash all collected evidence immediately after acquisition (SHA256). Record the hash, acquisition method, timestamp, and collector identity in the chain-of-custody log.
3. Preserve logs from all affected systems for at least the full attack window plus 30 days before for baseline. Ensure logs are not rotated or deleted during the investigation.
4. Do not modify, clean, or remediate affected systems until evidence is preserved and the incident commander authorizes remediation. Early remediation destroys forensic evidence.

## Decision points

- **Escalate to incident commander immediately**: active ransomware execution, confirmed data exfiltration, domain admin compromise, or any situation where delay increases damage.
- **Confirm false positive and close**: if all evidence points to benign activity and no anomalous behavior remains unexplained, document and recommend closing the incident.
- **Expand scope cautiously**: if investigation suggests additional systems or accounts are affected, expand the scope but do not exceed authorization boundaries.
- **Request external support**: if the incident exceeds team expertise, involves legal/regulatory notification, or requires law enforcement contact, escalate through the incident commander.

## Prohibited behavior

- Executing attacker tools, exploit code, malware, or offensive pentest tools during IR.
- Running destructive containment (disk wipe, system shutdown, firewall block of critical services) without explicit incident commander authorization.
- Credential attacks (password spraying, hash cracking, token replay) against compromised or production accounts.
- Modifying or deleting evidence on affected systems before preservation.
- Communicating incident details outside the authorized IR team.
- Storing unredacted incident data, PII, credentials, or forensic artifacts in evidence.

## Stop conditions

- Incident commander requests halt or scope change → stop and follow direction.
- Active attacker detected (interactive session, ongoing exfiltration) → escalate immediately, do not alert the attacker through IR activity.
- Containment would cause production outage exceeding approved threshold → escalate to incident commander.
- Evidence preservation requires credentials or access beyond current authorization → stop and escalate.

## Evidence — incident triage ledger

Record per incident:

```text
Incident ID: <unique ID>
Status: <triage | investigation | containment | recovery | closed>
Severity: <critical | high | medium | low>
Affected systems: <count and classification: confirmed / suspected / exposed>
Timeline events: <count: confirmed facts / reported observations / hypotheses / unknowns>
Attack phases identified: <Initial Access, Execution, Persistence, ...>
Scope confidence: <high — all affected systems identified | medium — some uncertainty | low — scope unknown>
Containment status: <not started | proposed | approved | in progress | completed>
Evidence preservation: <complete — all hosts preserved | partial — N hosts not preserved | not started>
Commander: <incident commander name/role>
```

Aggregate into an incident triage report:
- executive summary (what happened, what's affected, what's being done);
- full timeline with confidence annotations;
- scope of compromise assessment per system;
- containment proposal with operational impact per action;
- evidence preservation status;
- open questions and next investigation steps.

Never store: raw forensic artifacts, memory dumps, disk images, unredacted logs, credentials, PII, internal hostnames, or unredacted incident communications.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed compromise vector, credential exposure, data exposure, and persistence mechanism discovered. Include: affected system, attack technique, evidence references, and remediation recommendation.
2. Package the incident triage report for the incident commander and IR team.
3. Recommend: after incident closure, conduct a post-incident review (lessons learned), update detection rules for the attack techniques used, close the specific security gaps exploited, improve log coverage for blind spots identified, and update the IR runbook with this incident's timeline for faster future triage.
