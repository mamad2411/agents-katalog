---
name: disabled-persistence-policy
description: Policy-only boundary for persistence, backdoor, and long-term-access requests. Explains refusal rationale, unlock prerequisites, and safer defensive alternatives.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive]
authorization-required: yes
evidence-outputs: [policy-note, approval-record, safer-alternatives]
disabled-category: persistence
---

# Persistence policy

Use this skill to explain why persistence workflows are disabled by default. This skill is policy-only. It must not provide persistence mechanisms, stealth guidance, autostart locations, implant behavior, bypass tactics, cleanup-resistant design, or command sequences.

## Boundary

Persistence establishes mechanisms that survive reboots, credential rotation, and user sessions — granting long-term access to a compromised system. Even in authorized red-team engagements, persistence artifacts can be missed during cleanup, create lingering backdoors that outlive the engagement, and confuse incident responders who discover them later without context.

Treat every persistence request as high abuse-risk. The only allowed discussion paths are:

- Hardening review: assessing which autostart mechanisms, scheduled tasks, and service configurations are exposed and how to lock them down.
- Detection engineering: designing rules that detect persistence installation via registry changes, scheduled-task creation, service modification, or startup-folder writes.
- Incident response analysis: reviewing already-collected evidence for persistence indicators.
- Tabletop planning: walking through persistence scenarios to identify detection gaps without implementing them.

Do not help with: creating scheduled tasks, registry Run keys, WMI event subscriptions, launch daemons/agents, systemd services, cron jobs, .bashrc/.profile modifications, SSH authorized_keys insertion, web shells, cloud backdoor roles, or any mechanism that survives reboots or credential changes. Do not convert this policy discussion into installation steps.

## Required unlock process

All gates must pass before any persistence-related workflow can be considered:

- Repo config explicitly unlocks `persistence` in `.pi/pentest-agent/config.json`.
- User provides explicit per-engagement consent that names the target systems, persistence mechanisms, and cleanup ownership.
- Rules of engagement explicitly authorize persistence simulation with defined duration, cleanup procedure, and notification contacts.
- Target systems, autostart mechanisms, and service configurations are in scope.
- Cleanup procedure is defined, tested, and assigned to a named owner with a deadline.
- Authorization cache is valid for the normalized target hash.
- Risk approval is recorded for integrity-impacting and cleanup-risk behavior.
- Incident response and system-owner teams are notified before and after the exercise.
- Output is bounded, redacted, and stored only under `.pi/pentest-agent/`.

Use `pentest_agent_check_authorization`, `pentest_agent_validate_target`, `pentest_agent_validate_policy`, and `pentest_agent_request_unlock` to confirm gates. If any gate fails, refuse active help.

## Safer alternatives

Prefer these persistence-focused defensive assessments:

- **Autostart hardening checklist**: Enumerate all autostart locations (registry Run keys, Startup folders, scheduled tasks, services, WMI subscriptions, launch daemons, systemd units, cron, shell profiles) and assess whether they are monitored and hardened against unauthorized modification.
- **Detection rule gap analysis**: Review SIEM and EDR rules for persistence-related events: new service creation, scheduled task registration, registry Run key modification, WMI event consumer creation, and shell-profile changes.
- **Cleanup and recovery drill**: Design and test a cleanup procedure against a synthetic persistence artifact in a lab environment. Measure time-to-detect and time-to-remediate.
- **Configuration audit**: Compare current autostart configurations against a known-good baseline. Identify unauthorized or unexplained entries without installing new ones.
- **Incident response containment checklist**: Develop or refine the IR playbook for persistence discovery, containment, and eradication.
- **Tabletop persistence scenario**: Walk through a persistence scenario on a whiteboard with system owners and incident responders. Identify detection gaps and response friction without deploying artifacts.
- **Report-only risk narrative**: Use `pentest_agent_render_report` to document persistence risks, exposed autostart surfaces, and recommended hardening steps.

## Decision guidance

| Request | Response |
|---|---|
| "Install persistence on this server" | Refuse unless all unlock gates pass and cleanup ownership is documented. Offer hardening review. |
| "What persistence methods evade EDR?" | Refuse. Offer detection-gap analysis that identifies which methods current rules would miss. Stay defensive. |
| "Audit our scheduled tasks for anomalies" | Allow. Conduct read-only configuration audit. |
| "We found a suspicious service" | Allow. Help analyze the collected artifact for persistence indicators. |
| "Write a cron job for recurring access" | Refuse. Do not create, configure, or advise on persistence mechanism installation. |

## Depth rules

- Keep this skill policy-only: explain refusal boundary, approval prerequisites, audit trail requirements, and safer alternatives.
- Do not provide active persistence procedures, stealth techniques, cleanup evasion, autostart mechanism details, or tool-specific command sequences.
- Route allowed discussion toward hardening review, detection engineering, configuration auditing, and report-only risk documentation.
- Require repo unlock, per-engagement consent, valid scope, documented cleanup ownership, fresh authorization cache, risk approval, team notification, and redacted local evidence before any active workflow.
- Refuse when user asks to bypass disabled-default policy or install persistence mechanisms.
- Cross-reference related skills: `ad-lateral-movement-policy`, `ad-enumeration`, `ad-bloodhound-review`, `blue-detect`, `blue-ir`, `blue-log-review`.

## Evidence

Record policy decision, requested capability, cleanup requirements if discussed, scope summary, approval status, safer alternative chosen, and redaction notes. Never store persistence scripts, autostart paths, implant configurations, raw proof content, or unredacted system logs.
