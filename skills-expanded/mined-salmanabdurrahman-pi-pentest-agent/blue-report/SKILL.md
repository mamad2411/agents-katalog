---
name: blue-report
description: Defensive and incident report drafting — produce structured, redacted reports from findings, detections, IOC summaries, timelines, and containment logs with executive, technical, and regulatory audience variants.
disable-model-invocation: true
risk: report-only
allowed-modes: [auto, blue-team, forensic]
authorization-required: no
evidence-outputs: [report, finding-summary, redaction-notes]
---

# Blue-team report — defensive and incident reporting

Use this skill to draft structured, redacted defensive and incident reports from existing findings, detection summaries, IOC ledgers, incident timelines, and containment logs. Produce audience-appropriate variants: executive summary for leadership, technical deep-dive for engineering, regulatory notification for compliance, and post-incident review for the IR team. Never draft reports from unredacted data, run active validation, or post reports externally.

## Required inputs

- Completed findings: `pentest_agent_list_findings` output for the engagement or incident. Each finding must have: title, severity, confidence, affected assets, evidence references, impact, and remediation.
- Evidence inventory: `pentest_agent_list_evidence` output with redacted evidence records and hashes.
- Incident timeline (if applicable): from the `blue-ir` skill or an incident commander. Chronological events with confidence annotations.
- IOC ledger (if applicable): from the `blue-ioc-generation` skill or threat-intel team. IOCs with type, confidence, and expiry.
- Detection posture summary (if applicable): from the `blue-detect` skill or detection engineering team.
- Scope context: engagement scope, affected systems, time window, and any reporting constraints (redaction requirements, audience restrictions, regulatory requirements).
- Authorization cache not required for drafting from static findings and evidence. Authorization needed only if accessing live data or posting externally.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when scope, asset, or evidence boundaries exist.
3. `pentest_agent_validate_target` before any target contact or live query.
4. `pentest_agent_check_authorization` before any active validation or environment contact.
5. `pentest_agent_build_command` and `pentest_agent_execute_tool` only for approved defensive read-only tooling.
6. `pentest_agent_append_evidence` and `pentest_agent_record_finding` before report rendering.
7. `pentest_agent_render_report` or `pentest_agent_export_report` for final output.

## Workflow

### Phase 1 — audience and format selection

Determine report variants needed:

1. **Executive summary** (1-2 pages): for CISO, CTO, board, or executive leadership. Focus on business impact, risk posture, resource needs, and high-level timeline. Use plain language — no SIEM query syntax or raw log fields. Include: what happened, what was the impact (data, financial, reputational, operational), is the incident contained, what resources are needed, and what is the remediation timeline.
2. **Technical report** (5-20 pages): for security engineering, detection engineering, IT operations, and incident response teams. Include: full timeline with evidence references, attack chain analysis (MITRE ATT&CK mapping), IOC summary, log review findings, detection gap analysis, containment actions taken, and detailed remediation steps per system.
3. **Regulatory notification draft**: for legal/compliance team review. Include: incident date, discovery date, notification date, data types potentially exposed, number of individuals potentially affected, containment status, and remediation actions. Never include raw evidence, IOCs, or attacker TTPs in regulatory drafts.
4. **Post-incident review (PIR)**: for the IR team after incident closure. Include: incident timeline, what went well, what went poorly, detection time vs dwell time, containment time, gaps in tools/processes/training, and actionable improvements.

### Phase 2 — executive summary drafting

1. **Incident/engagement overview**: one paragraph. State what was assessed or what incident occurred, when, the scope, and the outcome in business terms.
   - Example: "Between 2024-03-10 and 2024-03-14, a threat actor gained unauthorized access to the customer-support application via a compromised third-party integration. The actor accessed support-ticket data for approximately 1,200 customers. The incident was detected on 2024-03-12, contained on 2024-03-13, and remediation was completed on 2024-03-14."
2. **Impact summary**: bullet points. Data exposed (type, not raw data), systems affected, services disrupted, financial impact (if known), regulatory implications.
3. **Current status**: is the incident contained? Is the threat actor still active? Have affected systems been remediated? Have affected parties been notified?
4. **Key findings** (3-5 maximum): the most important security observations. Prioritize by severity and business impact.
5. **Recommendations** (3-5 maximum): the most critical remediation actions needed. Focus on strategic improvements, not individual system patches.
6. **Risk posture statement**: after remediation, what is the residual risk? What compensating controls are in place while permanent fixes are being deployed?

### Phase 3 — technical report drafting

1. **Scope and methodology**: what was reviewed, which systems and time windows were in scope, which tools and techniques were used (defensive only), and any limitations.
2. **Timeline**: chronological table with timestamp (UTC), event description, source system, evidence reference, and confidence. Use timezone-consistent timestamps. Mark the detection time and containment time on the timeline.
3. **Attack chain analysis**: for each attack phase observed (per MITRE ATT&CK):
   - Technique used (T-code), how it was executed, which systems were involved.
   - How the technique was detected (or why it was missed).
   - IOCs associated with the technique.
   - Remediation applied or recommended.
4. **Finding details**: each confirmed finding with:
   - Finding ID and title.
   - Severity and CVSS score (if applicable).
   - Affected assets and scope status.
   - Technical description of the weakness or compromise.
   - Evidence references (redacted).
   - Reproduction steps or attack path.
   - Impact assessment.
   - Remediation: immediate fix, long-term fix, and compensating controls.
5. **Detection gap analysis** (if applicable): techniques that were not detected, why they were missed, and recommended detection rules.
6. **IOC summary** (if applicable): IOC count by type, confidence distribution, and integration status (deployed to SIEM/EDR/firewall or pending).

### Phase 4 — redaction and quality review

Before finalizing any report variant:
1. **PII scan**: does the report contain email addresses, usernames, customer names, IP addresses of customers, or any personal data? Redact or generalize (e.g., "customer from EU region" instead of specific name).
2. **Credential scan**: does the report contain passwords, API keys, tokens, cookies, or private keys? Remove immediately — these should never appear in any report.
3. **Infrastructure scan**: does the report contain internal hostnames, internal IP addresses, server names, or network topology details? For executive and regulatory reports, generalize. For technical reports, note that distribution should be restricted.
4. **IOC safety**: are IOCs suitable for the report's audience? Do not share active attacker infrastructure IOCs in widely-distributed reports — these may alert the attacker.
5. **Attribution caution**: do not attribute the attack to a specific threat actor or nation-state unless confirmed by a credible threat-intelligence source and approved by legal. Use descriptive names: "the threat actor" or "unauthorized third party."
6. **Readability**: can a non-technical reader understand the executive summary? Can a technical reader reproduce the findings from the technical report? Are acronyms expanded on first use?

### Phase 5 — distribution and access control

1. Classify each report variant by distribution scope: incident commander only, IR team, security leadership, executive leadership, board, legal, regulators, affected customers, or public.
2. Apply access controls: store sensitive reports in restricted locations. Do not email unencrypted reports containing technical findings.
3. Set review and expiry: reports should be reviewed by the incident commander or engagement lead before distribution. After the incident is closed or the engagement is complete, archive reports per retention policy.
4. Never post reports externally (GitHub, blog, social media, threat-intel sharing) without explicit authorization and heavy redaction.

## Decision points

- **Separate variants early**: executive summary, technical report, regulatory notification, and PIR should be separate documents. Do not mix audiences.
- **Escalate unclear findings**: if a finding lacks sufficient evidence, is based on a single unverified alert, or contradicts other evidence → mark as "needs investigation" and escalate back to the detection or IR team.
- **Defer regulatory notification**: never draft a final regulatory notification without legal review. Draft the technical facts only.
- **Redact aggressively**: when in doubt, redact. It is easier to add detail later than to recall a report that leaked PII or IOCs.

## Prohibited behavior

- Including raw log entries, forensic artifacts, or unredacted evidence in reports.
- Including PII, credentials, tokens, API keys, internal hostnames, or network topology in distributed reports.
- Attributing attacks to specific threat actors without confirmed intelligence and legal approval.
- Posting or sharing reports outside the authorized distribution scope.
- Running active validation, scanning, or exploitation to "confirm report findings" — reports document what was already found.
- Drafting reports from undocumented findings — every claim must trace to a stored finding or evidence record.

## Stop conditions

- Report contains PII or credentials → redact before continuing.
- Finding evidence is insufficient for report → escalate back to investigation team, do not fabricate.
- Distribution would exceed authorization → stop, escalate to incident commander or engagement lead.
- Regulatory notification requires legal review → stop, note for maintainer, do not draft final language.

## Evidence — report assembly ledger

Record per report variant:

```text
Report type: <executive summary | technical | regulatory draft | PIR>
Audience: <CISO | security engineering | legal | IR team>
Status: <draft | reviewed | approved | distributed>
Findings included: <count: critical / high / medium / low / info>
IOCs included: <count by type, redacted: yes/no>
Redaction notes: <fields redacted: hostnames, IPs, customer names, ...>
Distribution: <authorized recipients and channels>
Expiry/review date: <date>
```

Never store: unredacted reports, reports containing PII/credentials, distribution lists with external recipients, or regulatory drafts not yet reviewed by legal.

## Report handoff

1. Use `pentest_agent_render_report` to produce the final markdown report. Use `pentest_agent_export_report` for JSON or other formats.
2. After rendering, verify: all findings have evidence references, all IOCs are redacted or safe for the audience, all timelines are source-referenced, and the report passes the redaction scan.
3. Deliver per the distribution plan: executive summary to leadership, technical report to engineering, regulatory draft to legal, PIR to IR team.
4. Archive the final report and all evidence under the engagement or incident ID. Retain per the organization's data retention policy.
5. Recommend: establish a report template library with pre-approved language, automate redaction scanning in the report pipeline, and track report distribution and readership for compliance.
