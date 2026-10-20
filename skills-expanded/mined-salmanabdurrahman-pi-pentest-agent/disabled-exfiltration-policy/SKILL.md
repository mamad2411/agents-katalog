---
name: disabled-exfiltration-policy
description: Policy-only boundary for data-exfiltration, staging, and covert-transfer requests. Explains refusal rationale, unlock prerequisites, and safer defensive alternatives.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive]
authorization-required: yes
evidence-outputs: [policy-note, approval-record, safer-alternatives]
disabled-category: exfiltration
---

# Exfiltration policy

Use this skill to explain why data-exfiltration workflows are disabled by default. This skill is policy-only. It must not provide data collection, staging, transfer-channel design, covert transport, compression/encryption workflows, evasion guidance, or command sequences.

## Boundary

Exfiltration simulates what an attacker does after gaining access: identify valuable data, stage it, and transfer it outside the organization. Even in authorized testing, this activity risks exposing regulated data, personally identifiable information, intellectual property, or credentials to test infrastructure. A misconfigured staging directory or an overly broad collection filter can create a real data breach during a simulation.

Treat every exfiltration request as high abuse-risk. The only allowed discussion paths are:

- Data-loss prevention (DLP) review: assessing DLP tool coverage, egress filtering, and data-classification enforcement.
- Tabletop planning: designing a synthetic-data exfiltration exercise without transfer steps.
- Incident response analysis: reviewing already-collected evidence from a prior authorized engagement.
- Architecture review: evaluating network segmentation, egress controls, and data-access audit trails.

Do not help with: identifying valuable data on live systems, staging data in preparation for transfer, selecting exfiltration protocols (DNS, HTTPS, ICMP, cloud storage), designing covert channels, evading DLP detection, compressing or encrypting data for transfer, or moving data to external infrastructure. Do not process or store files, database contents, source code, credentials, or customer records.

## Required unlock process

All gates must pass before any exfiltration-related workflow can be considered:

- Repo config explicitly unlocks `exfiltration` in `.pi/pentest-agent/config.json`.
- User provides explicit per-engagement consent that defines data classes, volume limits, synthetic-data rules, and transfer-channel constraints.
- Rules of engagement explicitly define the data scope: synthetic only, named datasets, or specific record counts. Real production data must never be exfiltrated without documented authorization from the data owner and legal review.
- Target systems, data repositories, transfer methods, and destination infrastructure are in scope.
- DLP and monitoring teams are notified before the exercise to avoid incident-response mobilization.
- Authorization cache is valid for the normalized target hash.
- Risk approval is recorded for data-sensitive behavior and potential regulatory impact.
- Output is bounded, redacted, and stored only under `.pi/pentest-agent/`.

Use `pentest_agent_check_authorization`, `pentest_agent_validate_target`, `pentest_agent_validate_policy`, and `pentest_agent_request_unlock` to confirm gates. If any gate fails, refuse active help.

## Safer alternatives

Prefer these data-protection assessments that do not require moving data:

- **DLP control review**: Evaluate DLP tool deployment, policy coverage, and detection rules. Test DLP detection with synthetic canary tokens or test files that contain no real data.
- **Egress policy audit**: Review firewall egress rules, proxy allowlists, and DNS filtering. Identify gaps that could permit unauthorized data transfer.
- **Data classification and minimization review**: Assess whether data is appropriately classified, whether access controls match classification, and whether data minimization practices reduce exfiltration impact.
- **Log and alert coverage analysis**: Review whether file-access audit logs, database query logs, and network flow data are collected, retained, and monitored for exfiltration patterns.
- **Synthetic-data exercise design**: Create a tabletop or walkthrough plan that maps exfiltration paths using synthetic markers. Document the detection gaps without executing real transfers.
- **Access review for sensitive repositories**: Audit which users and services can read sensitive data stores. Identify over-privileged access without touching the data.
- **Report-only risk narrative**: Use `pentest_agent_render_report` to document the exfiltration risk, crown-jewel data locations, potential egress paths, and recommended controls.

## Decision guidance

| Request | Response |
|---|---|
| "Exfiltrate data from our file server" | Refuse unless all unlock gates pass and data scope is synthetic-only. Offer DLP review instead. |
| "Test if our DLP detects data leaving" | Allow DLP configuration review and canary-token testing. Do not move real data. |
| "Map our egress points" | Allow. Review firewall rules and proxy configurations. Stay read-only. |
| "We had a data breach; analyze the logs" | Allow. Help review collected evidence for exfiltration indicators. |
| "Stage these files for transfer" | Refuse. Do not process real files or stage data for movement. |

## Depth rules

- Keep this skill policy-only: explain refusal boundary, approval prerequisites, audit trail requirements, and safer alternatives.
- Do not provide data-collection, staging, transfer-channel, covert-transport, compression, encryption-for-exfil, or command sequences.
- Route allowed discussion toward DLP review, egress auditing, data-classification assessment, and report-only risk documentation.
- Require repo unlock, per-engagement consent, synthetic-data scope, fresh authorization cache, risk approval, DLP team notification, and redacted local evidence before any active workflow.
- Refuse when user asks to bypass disabled-default policy, process real data, or transfer files outside authorized infrastructure.
- Cross-reference related skills: `blue-ir`, `blue-log-review`, `blue-detect`, `forensic-metadata`, `forensic-chain-of-custody`.

## Evidence

Record policy decision, requested activity, synthetic-data constraints if defined, scope summary, approval status, safer alternative chosen, and redaction notes. Never store file contents, database extracts, source code, credentials, customer data, regulated data, or unredacted transfer logs.
