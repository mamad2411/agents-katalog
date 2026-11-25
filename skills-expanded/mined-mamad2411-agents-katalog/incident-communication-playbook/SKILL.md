---
name: incident-communication-playbook
description: Create incident communication playbooks for outages, data issues, payment failures, store launch problems, privacy incidents, game economy issues, support backlogs, and degraded product experiences. Use when planning status updates, customer notices, internal coordination, postmortems, support macros, incident timelines, or trust-recovery communication.
---

# Incident Communication Playbook

Use this skill to communicate incidents clearly, quickly, and proportionately.

## Workflow

1. Identify incident type, user impact, blast radius, uncertainty, legal/privacy risk, and channels.
2. Read `references/incident-communication-patterns.md`.
3. Draft internal coordination, customer-facing updates, support macros, and post-incident follow-up.
4. Separate known facts, unknowns, actions, next update time, and user workaround.
5. Produce a communication timeline and approval/risk gates.

## Guardrails

- Do not speculate beyond verified facts.
- Do not hide material user impact.
- Route privacy/security/legal-sensitive incidents through the required review path.

## Output format

```text
Incident type:
Impact:
Channels:

Timeline:
- <time> <audience> <message/update>

Customer update:
- <draft>

Support macro:
- <draft>

Post-incident follow-up:
- <items>
```
