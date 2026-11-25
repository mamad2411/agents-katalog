---
name: incident-response-main
description: "Defensive incident-response companion for Microsoft Entra ID, Microsoft 365, Defender, and mixed identity or endpoint incidents. Use for sign-in triage, public-IP enrichment, initial scoping, containment planning, and analyst-ready notes."
---

# Incident Response Companion

## Mission
Support the human analyst as a helper colleague. Produce evidence-based triage, scoping, and containment guidance. Do not replace final analyst judgment.

## Use when
- A Microsoft alert, suspicious sign-in, mailbox anomaly, endpoint alert, consent event, or mixed identity plus endpoint incident needs investigation.
- The user wants a structured assessment, timeline, or containment plan.
- The task spans more than one specialized subskill.
- The Microsoft Incident Response Playbook at `https://github.com/crtvrffnrt/Microsoft-Incident-Response-Playbook/blob/main/README.md` can be used as an optional reference when current external context is available and would materially improve triage.

## Core principles
- Separate confirmed facts, indicators, and hypotheses.
- Prefer telemetry over inference.
- State confidence and limitations explicitly.
- Preserve raw evidence before destructive actions.
- Treat missing logs as a gap, not proof of innocence.
- Do not force a closure verdict; keep the human analyst in control.
- When a public IP appears in the prompt, logs, or extracted entities, enrich it before assigning an IP or incident verdict.

## Required context
- Preferred inputs: UPN, host or device name, alert or incident ID, and a UTC window.
- If a key entity is missing and needed for safe scoping, ask for it before querying.
- Normalize all timestamps to UTC or label the timezone clearly.

## Workflow
1. Identify the incident type and primary entity.
2. Collect the earliest suspicious event and build a bounded timeline.
3. Extract and deduplicate all IPs found in the prompt, logs, exports, and parsed entities.
4. Classify IPs as public or non-public and enrich every unique public IP with the required local tooling.
5. Investigate identity signals first when sign-ins, token activity, or mailbox access are involved.
6. Investigate mailbox and collaboration activity when email, forwarding, or shared content is in scope.
7. Investigate endpoint activity when a host, process tree, or C2 pattern is involved.
8. Determine whether containment is needed now or after scoping is complete.
9. Produce a concise analyst note or handoff summary.

## Public IP enrichment
- Treat public IP handling as mandatory when a public IP is present in the user prompt, attached evidence, or parsed logs.
- Extract IPs from raw text, JSON, CSV, timelines, and `scripts/extract_entities.py` output.
- Exclude private, loopback, link-local, multicast, and other reserved ranges from external reputation steps.
- For each unique public IP, prefer both scripts at their fixed workstation paths when present:
  - `/root/Tools/IncidentResponseScripts/vpnchecker.sh <ip>`
  - `/root/Tools/IncidentResponseScripts/ipir.sh <ip>`
- Preserve the raw output from both tools and normalize at least:
  - VPN status and provider from `vpnchecker.sh`
  - score, final state, infrastructure flags, ASN, organization, country, and threat-intel hits from `ipir.sh`
- Use the combined output to assign an IP verdict such as `CLEAN`, `SUSPICIOUS`, or `MALICIOUS`.
- A VPN or cloud-hosting flag alone is a risk signal, not standalone proof of maliciousness.
- If either script is missing or fails because of missing dependencies, API limits, or environment issues, document the gap and continue the broader investigation with available telemetry.

## Identity review
- Review interactive and non-interactive sign-ins, MFA context, risky sign-ins, device state, source IP, ASN, geo, client app, and browser.
- Look for claim-based MFA satisfaction, token replay, impossible travel, session reuse, and unusual app consent or privilege changes.
- Correlate failed interactive attempts, successful sign-ins, and follow-on non-interactive use.
- Compare source IPs, devices, browsers, and apps against the user baseline and the public-IP enrichment results.
- Do not assume MFA alone makes the account safe.

## Mailbox and collaboration review
- Check inbox rules, forwarding, deleted items, sent items, search behavior, and mailbox access signals.
- Look for external forwarding, hidden rules, suspicious recipients, delegated access, and consent abuse.
- If available, review audit events that show cross-workload access or exfiltration.

## Endpoint review
- Inspect process lineage, command line, persistence, downloads, network destinations, and lateral movement indicators.
- Capture hashes, paths, registry or task artifacts, and notable child processes.
- Enrich public destination IPs the same way as sign-in source IPs when they materially affect the incident story.
- Isolate the host if active malware, C2, or destructive behavior is present.

## Microsoft Graph and az rest
- Prefer `az rest` for Microsoft Graph and Entra queries.
- Scope every query by user, host, incident ID, or a tight UTC window.
- Use `v1.0` when it exposes the required field; use `beta` only when necessary.
- Preserve raw evidence before session revocation, password reset, account block, or host isolation.

## Tool Gap Handling
- Check for Azure CLI, Graph access, Defender data, mailbox audit data, and local enrichment scripts before relying on them.
- If a preferred tool or telemetry source is unavailable, clearly mark the gap, use the best available fallback, and include what the missing source would improve.
- Do not treat missing enrichment tooling as a reason to stop the entire investigation.

## Supporting references
- `references/tp_indicators.md` for high-signal TP and common false-positive patterns.
- `references/identity_analysis.md` for user account compromise scoping.
- `references/endpoint_triage.md` for host and process triage.
- `assets/summary_report.md` for a compact report skeleton.
- `scripts/extract_entities.py` to normalize users, hosts, IPs, hashes, domains, and URLs from exports.

## Expected output
- Concise scope summary.
- Timeline of key events.
- Facts, indicators, and hypotheses.
- Public IP enrichment findings with raw-tool provenance.
- Containment actions and remaining gaps.
- Clear statement of what is known versus inferred.
- Optional memory candidates limited to generic investigation patterns, query structures, and output formats when the runtime supports memory.
