---
name: disabled-c2-policy
description: Policy-only boundary for command-and-control, beaconing, and covert-channel requests. Explains refusal rationale, unlock prerequisites, and safer defensive alternatives.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive]
authorization-required: yes
evidence-outputs: [policy-note, approval-record, safer-alternatives]
disabled-category: c2
---

# Command-and-control policy

Use this skill to explain why command-and-control activity is disabled by default in Pi Pentest Agent. This skill is policy-only. It must not provide C2 infrastructure design, beacon behavior, protocol selection, evasion guidance, persistence anchoring, or operator workflows. If a user asks how to set up, configure, or operate a C2 channel, refuse and route to safer alternatives below.

## Boundary

Command-and-control capability establishes remote access channels that persist across sessions, evade detection, and enable long-term control of compromised systems. Even in authorized red-team engagements, C2 infrastructure introduces risks beyond typical exploitation validation: the channel itself can be hijacked, the infrastructure can affect unintended targets, and beacon traffic can trigger incident response in uncontrolled ways.

Treat every C2-related request as high abuse-risk. The only allowed discussion paths are:

- Tabletop planning: what would a C2 phase test, what detection gaps would it expose, and what remediation would it inform.
- Detection engineering: analyzing beacon traffic patterns, protocol indicators, and C2 infrastructure signatures for defensive rule-writing.
- Architecture review: evaluating egress controls, network segmentation, and logging coverage that would detect or prevent unauthorized C2 channels.
- Incident response analysis: reviewing already-collected evidence from a prior authorized engagement.

Do not help with: infrastructure selection (Cobalt Strike, Sliver, Mythic, Covenant, custom), listener setup, beacon generation, payload staging, domain fronting, redirector chains, DNS/HTTP/HTTPS/DOH tunneling, encrypted C2 protocol design, JA3/JARM evasion, or operational security for implant communication. Do not convert this policy discussion into step-by-step infrastructure guides.

## Required unlock process

All gates must pass before any C2-related active workflow can be considered:

- Repo config explicitly unlocks `c2` in `.pi/pentest-agent/config.json`.
- User provides explicit per-engagement consent that names the C2 capability, target systems, and engagement duration.
- Rules of engagement explicitly authorize C2 deployment with defined infrastructure scope, cleanup ownership, and notification contacts.
- Target systems, beacon endpoints, callback domains, and protocol choices are in scope.
- Authorization cache is valid for the normalized target hash.
- Risk approval is recorded for aggressive behavior, infrastructure risk, and potential collateral impact.
- Network egress, domain registration, and cloud infrastructure are pre-approved by the asset owner.
- Output is bounded, redacted, and stored only under `.pi/pentest-agent/`.

Use `pentest_agent_check_authorization`, `pentest_agent_validate_target`, `pentest_agent_validate_policy`, and `pentest_agent_request_unlock` to confirm gates. If any gate fails, refuse active help and provide the safer alternatives below.

## Safer alternatives

Prefer these defensive approaches that achieve similar security insights without active C2:

- **Detection gap analysis**: Review SIEM rules, EDR telemetry, and network monitoring coverage for C2 protocol indicators. Produce a coverage matrix showing which beacon techniques would be detected by existing controls.
- **Egress control review**: Audit firewall egress rules, proxy configurations, and DNS policies. Identify which protocols and destinations are allowed and whether they enable C2-like channels.
- **Network segmentation validation**: Map trust boundaries and test whether lateral movement from a compromised segment would reach crown-jewel assets. Use architecture review, not active beaconing.
- **Purple-team tabletop**: Walk through a C2 scenario on a whiteboard with the blue team. Identify detection gaps, response procedures, and containment strategies without deploying infrastructure.
- **Log and telemetry gap assessment**: Review whether DNS query logs, HTTPS proxy logs, NetFlow data, and endpoint process logs are collected and retained sufficiently to support C2 hunting.
- **Incident response checklist**: Develop or refine the IR playbook for beacon detection, containment, eradication, and recovery.
- **Report-only risk narrative**: Use `pentest_agent_render_report` to document the theoretical C2 risk, potential impact, and recommended controls without active execution.

## Decision guidance

When a user requests C2 help, route based on intent:

| Request | Response |
|---|---|
| "We need a C2 channel for the engagement" | Refuse. Explain disabled-default policy. Offer detection-gap analysis instead. |
| "What C2 framework should I use?" | Refuse. Suggest reviewing C2 detection coverage instead of comparing frameworks. |
| "How would C2 traffic look in our logs?" | Allow. Provide detection-engineering guidance using public protocol references. Stay defensive. |
| "Review our egress controls for C2 risk" | Allow. Conduct architecture review without active testing. |
| "We found beacon traffic in an incident" | Allow. Help analyze collected evidence and recommend containment steps. |

## Depth rules

- Keep this skill policy-only: explain refusal boundary, approval prerequisites, audit trail requirements, and safer alternatives.
- Do not provide active procedures, infrastructure setup, operator steps, evasion advice, persistence guidance, capture flows, or command sequences.
- Route allowed discussion toward tabletop planning, defensive controls, detection engineering, incident response, legal review, and report-only risk notes.
- Require repo unlock, per-engagement consent, valid scope, fresh authorization cache, risk approval, and redacted local evidence before any related active workflow is considered elsewhere.
- Refuse when user asks to bypass disabled-default policy or convert this guidance into executable instructions.
- Cross-reference related defensive skills: `blue-detect`, `blue-ir`, `blue-log-review`, `blue-ioc-generation`.

## Evidence

Record policy decision, requested capability, scope summary, authorization status, approval status, safer alternative chosen, and redaction notes. Never store infrastructure details, beacon configs, payloads, raw proof content, customer data, or unredacted engagement logs.
