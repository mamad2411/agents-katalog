---
name: sec-incident-response
version: 1.0.0
description: Drive a security incident through triage, contain, eradicate, recover, and blameless postmortem while preserving evidence.
author: matrixx0070
tags: [security, incident-response, forensics, containment, postmortem, defensive]
capabilities: []
---

## When to use

Use this when a security incident is suspected or confirmed — breach, malware, credential compromise, data exposure, or active intrusion. It structures a calm, evidence-preserving defensive response.

**Not for:** hacking back or retaliating against an attacker; destroying data before it is captured as evidence; or routine bug triage. Contain and recover — never counter-attack.

## Method

1. **Triage & declare.** Confirm the incident is real, classify severity, assign an incident lead, and open a timestamped log. Record scope: what systems, data, and accounts are involved.
2. **Preserve evidence.** Before changing anything, capture volatile state (logs, memory, connections, disk snapshots). *Decision point:* if the attacker is active, weigh evidence capture against stopping ongoing damage — capture what you can, then contain.
3. **Contain.** Isolate affected hosts, revoke compromised credentials and sessions, block malicious IPs/domains, and disable exploited paths. Prefer reversible short-term containment first.
4. **Eradicate.** Remove malware, close the entry vector, patch the exploited weakness, and rotate all potentially exposed secrets.
5. **Recover.** *Decision point:* when host integrity is in doubt, rebuild from known-good images rather than cleaning in place. Restore from verified backups, monitor for reinfection, and confirm integrity before reopening.
6. **Postmortem.** Write a blameless timeline, root cause, impact, what worked, and concrete action items with owners and dates.

## Example

Alert: a service account logs in from an unfamiliar country at 02:14. Triage confirms anomalous API calls (Sev 2). Preserve: snapshot the host, export auth logs. Contain: disable the service account, revoke its active tokens. Eradicate: rotate the leaked key found in a public gist, patch the pipeline that logged it. Recover: redeploy from a clean image, watch auth logs 48h. Postmortem action item: move CI secrets to a vault, owner @platform, due in 2 weeks.

## Pitfalls

- **Rebooting or "cleaning" before capturing state.** Volatile evidence (memory, connections) is gone forever once you do.
- **Containing loudly against an active intruder.** Premature, visible action can trigger data destruction; coordinate the cutoff.
- **Declaring recovery without watching for reinfection.** Attackers leave persistence; monitor before you call it closed.
- **Blame in the postmortem.** Naming a person instead of a process gap stops people from reporting the next incident.

## Output format

```
## Incident summary
Severity: <>. Scope: <>. Current status: <>.

## Timeline
| Time (UTC) | Event / action taken |
|------------|----------------------|

## Phase checklist
- Contain: [ ] ...
- Eradicate: [ ] ...
- Recover: [ ] ...

## IOCs
- <indicator of compromise>

## Postmortem
Root cause: <>. Impact: <>.
| Action item | Owner | Due |
|-------------|-------|-----|
```
