---
name: coff0xc-detection-response
description: "Use when the user requests SOC, security operations, detection engineering, threat hunting/intel, incident response/IR, forensics, malware, or phishing: SIEM, Sigma, YARA, IOC, logs, alerts, EDR, timeline, alert tuning, false positives, and detection logic. Manual trigger: Use coff0xc-detection-response."
---

# coff0xc-detection-response

<!-- skill-id: cs-drs-6c1f90e4 -->

## Quick Rules (read this first for everyday tasks)
> **[Timeline first]** Define log sources, fields, time range, entities, alert context, and known IOCs first.
> **[Detection gate]** Sigma/YARA/queries must state field mappings, samples, false-positive sources, ATT&CK mapping, and test method.
> **[Response boundary]** Triage, preservation, and containment recommendations by default; confirm first for real isolation, blocking, deletion, account suspension, or production handling.
> **[Delivery standard]** Output timeline, evidence level, rules, tuning recommendations, missing logs, and review items.

Follow this section first for ordinary detection/response tasks; expand the full workflow only for incident command, real containment, or cross-team exercises.

## Capability
Defensive-operations capability for SOC, detection engineering, threat hunting, forensics, and incident response. It turns logs, sample leads, and alert problems into verifiable detections, timelines, and response recommendations.

## What It Can Deliver
- Sigma/YARA/query rule drafts and field mappings
- IOCs, timelines, attack stages, and ATT&CK mapping
- False-positive analysis, test samples, and tuning recommendations
- Incident handling, forensic preservation, and review/improvement checklists

## What Input It Can Take
- EDR/SIEM/cloud logs, alerts, IOCs, sample summaries
- Forensic notes, mail headers, network-traffic summaries, incident timelines
- Existing Sigma/YARA/query rules and false-positive feedback

## Safe-Use Boundaries
- Defensive detection, incident response, forensics, and reporting only
- Do not provide unauthorized attack, persistence, detection-evasion, or malicious-sample delivery steps
- When handling real logs, avoid leaking personal information and sensitive asset details
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Detection rules must state data sources, fields, test samples, and false-positive risk
- IR output separates observed facts from inference
- Prioritizes executable handling and verification steps

## Typical Usage
```text
Use coff0xc-detection-response to write Sigma and YARA detection rules from these EDR logs.
Use coff0xc-detection-response for a threat-hunting hypothesis, log queries, and alert tuning.
Use coff0xc-detection-response to build an incident timeline from these forensics notes.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
