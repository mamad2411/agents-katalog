---
name: ir-runbook
description: Incident Response runbook — NIST SP 800-61 phases (Preparation/Detection-Analysis/Containment-Eradication-Recovery/Lessons-Learned), per-scenario playbooks (ransomware, BEC, data exfil, credential compromise, cloud), regulatory reporting (NIS2 24h/72h, AVG breach 72h, DORA), comms templates, and post-incident review.
---

# IR Runbook

> **Operational discipline**: a runbook steers people under pressure; ambiguity costs time. Keep procedures concrete and testable — a step that cannot be executed at 03:00 without personal interpretation is not operational. Legal and regulatory aspects (breach notification, NIS2 incident reporting, contract clauses with customers/suppliers) are part of the runbook but require DPO/legal input for final decisions — this skill structures, it does not replace a lawyer during an incident.

## When to use

An incident is not the moment to design procedures. This skill helps in advance with runbook construction and during with scenario selection, phase transitions, and regulatory timelines.

Triggers on:

- A question like "write a ransomware runbook", "what do we do on a suspicious phishing report from a user", "is this a data breach under AVG", "design a BEC procedure", "post-incident review structure".
- An active incident response where phase determination or a regulatory question (NIS2 24h, AVG 72h, DORA 4h) needs clarity.
- A handoff from `secrets-scanner` (leak confirmed, escalating to IR), `cve-triage` (CVE with confirmed exploitation), `forensics-assist` (forensics running in parallel with IR).
- A tabletop exercise where you test the runbook.
- Periodic runbook review (at least annually or after every significant incident).

### When NOT (handoff)

- Policy-level IR policy itself (purpose, scope, roles at management level) → `policy-drafter`. An IRP policy is high-level requirements; this runbook is the operational execution.
- Forensic investigations (memory analysis, disk imaging, timeline reconstruction) → `forensics-assist`. Runs in parallel.
- Detection side: rule tuning, alert triage of the alarm that triggers the incident → `detection-engineer`, `alert-tuning`, `log-triage`.
- Threat intel + IOC enrichment → `ioc-hunter`.
- Malware analysis itself → `malware-triage`.
- Audit-evidence collection of the controls touching the incident → `audit-evidence`.
- Pentest context (planned) → pentest skills, not incident response.

## Approach

Six phases based on NIST SP 800-61 Rev. 2, with a regulatory layer (phase 5) as the NL/EU specific.

### 1. Preparation (before any incident)

What must be ready before things break:

- **Runbook portfolio**: scenarios identified from threat intel + risk register. Minimum: ransomware, business-email compromise (BEC), credential compromise (single-account), cloud credential compromise, data exfil, insider-threat report, supply-chain incident at a vendor.
- **IR team roster** with roles: incident commander, technical lead, forensics, comms lead, legal/DPO liaison, exec bridge. Per role primary + backup. 24/7 reachability via paging.
- **Communication channels**: out-of-band (avoid compromised email during an incident), Signal/Wire group, dedicated bridge link, status page for external communication.
- **Tools readiness**: SIEM access, EDR console access, jump hosts, tested backup-restore procedures, known evidence-storage destination.
- **Regulatory contact info on hand**: CSIRT-NL (NCSC-NL), AP for data-breach reporting, sector regulator (RDI/DNB/AFM), CERT-NL contacts. Phone numbers and web-form URLs in the runbook, not "we'll look it up".
- **Tabletop cadence**: at least annually per scenario, more frequently for high-impact (ransomware, cloud credential compromise).

### 2. Detection and Analysis

The first minutes/hours decide a lot.

- **Triage criteria**: is it a real incident or a false positive? Initial severity assessment. Four severity levels are common: SEV1 (existential: ransomware in production, mass exfil, prod down), SEV2 (significant impact: single-system compromise, limited exfil), SEV3 (locally containable: phishing click without credential handover), SEV4 (informational, monitoring).
- **Initial scoping**: which systems are affected, which data classification, which users involved. Do not wait for 100% certainty — work with "best knowledge at time".
- **Clock starts**: for regulatory timelines (NIS2 24h from detection, AVG 72h from "becoming aware", DORA 4h from classification). Document the detection time because it starts the reporting clocks.
- **Communications trigger**: SEV1/SEV2 wakes the IC + technical lead immediately; SEV3 within office hours.
- **Evidence preservation**: snapshot logs, memory, disk images before containment (containment can destroy evidence). See `forensics-assist`.

Output of this phase: an incident ticket with scope, severity, IC, first hypotheses.

### 3. Containment

Short-term (stop the bleeding) plus long-term (sustainable).

**Short-term containment** (minutes to hours):

- **Network isolation**: affected hosts off-network (firewall/EDR network-isolate). Less destructive than power-off, preserves memory state.
- **Account disablement** for compromised credentials. Rotate keys via `secrets-scanner` phase 4.
- **Block rules** for C2 IOCs in firewall/DNS/SIEM.
- **Stop attack progression**: kill processes, stop services that are actively abused.

**Long-term containment** (hours to days):

- **Patch + reconfigure** before recovery. Otherwise it is a repeat incident within weeks.
- **Strengthen network segmentation** where it should have been.
- **Backup isolation** ensured if ransomware is in play — offline copies unreachable to the attacker.

Priority differs per scenario. Ransomware: isolate backups + stop payload spread; BEC: account revoke + email-rule cleanup; data exfil: egress block + identify uplevel paths.

### 4. Eradication and Recovery

- **Eradication**: remove attacker tools/persistence. Not just fixing the one compromised account — search-and-destroy all persistence (see `post-exploit` phase 5 for what attackers leave behind). EDR baseline rebuild, password reset where persistence is cred-based, image rebuilds where persistence is on disk.
- **Recovery**: phased return of services online, strengthened monitoring during come-back, validated clean state per restored system. No "we don't see anything happening, so all is well" — actively monitor with heightened detection.
- **Validation criteria** decided in advance: how do you know the threat is gone? Which detection rules must not fire for N days? Which logs must be clean?

### 5. Regulatory reporting and compliance layer

NL/EU-specific with several overlapping regimes:

- **AVG breach (Art 33)**: 72 hours after "becoming aware". To AP via the report form. Plus Art 34: notify data subjects on high risk (often overlaps with large incidents). See `gdpr-pia` for context.
- **NIS2 (Art 23)**: three phases 24h/72h/1-month for essential and important entities, to CSIRT-NL plus competent authority (often RDI). See `nis2`.
- **DORA (Art 17–23)**: for financial entities. Major-incident classification via RTS thresholds, then 4h initial / 72h intermediate / 1 month final to DNB/AFM. See `dora`.
- **Sector-specific rules**: healthcare (Wkkgz), critical-infra additions, telecoms requirement. Inventory per sector.
- **Contract clauses**: many B2B contracts require customer notification within X hours for security incidents touching their data. Inventory in phase-1 prep.

Discipline during the incident: one person (often the DPO or compliance lead) tracks the clock per regime. A late notification can on its own lead to enforcement action, separate from the incident impact.

### 6. Lessons Learned and post-incident review (PIR)

Within 1–2 weeks after recovery:

- **PIR meeting** with all involved plus management. No blame; focus on process learning.
- **Timeline reconstruction**: what happened when, who knew what, which decisions were made.
- **What went well**: detection trigger worked, comms channel was reachable, etc. Document deliberately — otherwise institutional knowledge disappears.
- **What did not go well**: missed detection, unclear role split, delayed regulatory notification.
- **Action items** with owners and deadlines. Not "we must improve x" but "DevOps lead implements offline backup validation within 6 weeks".
- **Update runbook AND policy** based on findings. The next incident must not produce the same lessons.
- **Threat intel out**: anonymized IOCs and TTPs shared via FI-ISAC/CSIRT-NL where appropriate (see `dora` Pillar 5 for financial; voluntary for others).

### 7. Verification-loop for runbook maintenance

Not for the incident itself, for runbook revision:

Layer 1: scope (all scenarios covered, or does our threat model have a gap?), assumptions (contact info current? backup procedure last tested when?), gaps (eviction procedures covered for cloud providers other than AWS?). Layer 2: regulatory timelines correct (NIS2/AVG/DORA hours not mixed up), CSIRT-NL/AP/RDI procedure steps current, no invented statutory references.

## Output

Two modes: a runbook document (in advance, a living document) or an incident log (during, real time).

**Runbook document** structure:

```
IR Runbook — version X.Y, valid until YYYY-MM-DD
Owner: <CISO/IRT lead> | Last tabletop: <date>

1. Preparation
   IR team roster (primary + backup)
   Comms channels (out-of-band)
   Regulatory contacts (CSIRT-NL, AP, sector)
   Tooling access (SIEM, EDR, jump hosts)

2. Per scenario (ransomware, BEC, data exfil, cred comp, cloud comp, etc.):
   Detection triggers
   Initial actions (first 30 min)
   Severity criteria
   Communication flow
   Containment steps (short + long term)
   Eradication checklist
   Recovery validation criteria
   Regulatory reporting trigger
   Per-step expected duration

3. Communication templates
   Internal: status update to IRT bridge
   Internal: comms to wider org
   External: status-page wording
   Customer notification (per contract)
   Regulator notification (AVG, NIS2, DORA)

4. Tabletop archive
   Per exercise: scenario, participants, lessons learned

Verification-loop: ...
```

**Incident log** (during):

```
Incident log — INC-YYYY-NNNN
IC: <name> | Detection time: <UTC> | Severity: <SEV1-4>

Timeline:
  HH:MM — action/decision — by whom

Scope:
  Affected systems: <list>
  Affected data: <classification>
  Affected users: <N>

Regulatory clocks:
  AVG breach (72h):    <start, deadline, status>
  NIS2 (24h/72h/1m):   <if essential/important>
  DORA (4h/72h/1m):    <if financial>
  Customer notification: <per contract>

Containment:
  Short-term: <steps + timestamp>
  Long-term:  <plan>

Eradication status:
  <persistence checks completed, status>

Recovery:
  Validation criteria: <which measured>
  Online phasing:      <order + times>

Open questions / blockers:
  - <...>

Verification-loop: ...
```

## References

- **NIST SP 800-61 Rev. 2** — [https://csrc.nist.gov/pubs/sp/800/61/r2/final](https://csrc.nist.gov/pubs/sp/800/61/r2/final). Computer Security Incident Handling Guide; canonical phases.
- **ENISA Incident Response Guidelines** — [https://www.enisa.europa.eu/topics/incident-response](https://www.enisa.europa.eu/topics/incident-response).
- **NCSC-NL** — [https://www.ncsc.nl/](https://www.ncsc.nl/). NL CSIRT procedures plus playbooks.
- **AP — Datalek melden** — [https://www.autoriteitpersoonsgegevens.nl/themas/beveiliging/datalekken](https://www.autoriteitpersoonsgegevens.nl/themas/beveiliging/datalekken). AVG Art 33/34 procedure.
- **EU Directive 2022/2555 (NIS2) Art 23** — [https://eur-lex.europa.eu/eli/dir/2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555). Incident-reporting timeline.
- **EU Regulation 2022/2554 (DORA) Art 17–23** — [https://eur-lex.europa.eu/eli/reg/2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554). Major-incident reporting.
- **MITRE ATT&CK** — [https://attack.mitre.org/](https://attack.mitre.org/). For TTP classification during analysis.
- **SANS Reading Room — IR** — [https://www.sans.org/reading-room/](https://www.sans.org/reading-room/). Per-scenario playbook templates.

## Categories

- blue
