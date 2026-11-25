---
name: incident-response
description: "Guides hands-on incident handling through the NIST SP 800-61r3 and SANS PICERL phases, covering identification and scoping, containment trade-offs, evidence handling, eradication, recovery and lessons learned. Use when the user is handling an active compromise, ransomware or malware outbreak, needs containment steps, or wants an IR playbook. (Decision-maker view: incident-response-leadership.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Incident response (handler)

You are the analyst doing the work, not the commander making the calls; for the
declare/notify/escalate/comms decisions, `load_skill incident-response-leadership`.
This skill is the technical lifecycle. Two compatible maps:

- **NIST SP 800-61r3** (Apr 2025, first rev since 2012) folds IR into CSF 2.0:
  Govern/Identify/Protect (prepare, prevent) + Detect/Respond/Recover (handle).
  verify: https://csrc.nist.gov/pubs/sp/800/61/r3/final
- **SANS PICERL** is the operational checklist: Preparation → Identification →
  Containment → Eradication → Recovery → Lessons learned.

Work it iteratively, not strictly linearly: eradication that misses a foothold
loops you back to identification.

## Preparation (before the call)

- Tooling staged: EDR, IR collection scripts, jump kit, out-of-band comms.
- Know your assets + crown jewels and what "normal" looks like (you can't spot
  evil without a baseline). Logging coverage validated (`load_skill siem-soar`).
- Runbooks for top scenarios (ransomware, BEC, web compromise, stolen creds):
  `load_skill ransomware-response`, `load_skill bec-email-investigation`,
  `load_skill cloud-incident-response`.

## Identification (confirm + scope)

- Validate the alert is a real incident, not a benign/false positive.
- Build the timeline: first evidence, patient zero, dwell time. Pivot across
  identity, endpoint, network, cloud logs.
- Map observed actions to **ATT&CK** technique ids as you go; it makes scope and
  handoffs unambiguous and seeds the report. Pull related infra with
  `load_skill ioc-pivoting`.
- Determine: entry vector, accounts/hosts touched, data at risk, attacker still
  active? Set severity (drives the commander's clock; see leadership skill).
- **Scope before you contain.** Containing one node of a known-larger intrusion
  tips the attacker to burn the rest.

## Containment (stop the spread, mind the trade-offs)

Short-term (immediate) then long-term (durable). Decision rules:

- **Network-isolate, don't power off.** Quarantine the host (EDR contain / VLAN /
  switchport) so RAM and live state survive for forensics. Powering off destroys
  volatile evidence; reimaging destroys the case.
- **Disable, don't delete** compromised accounts (preserve the artifact); rotate
  creds/tokens/keys; revoke OAuth grants and active sessions.
- Block C2 at egress/DNS; preserve a copy of the indicator first.
- Trade-off: **stop-the-bleeding vs preserve-evidence.** When data is actively
  exfiltrating or ransomware is encrypting → contain now, evidence second. When
  scope is unknown and the attacker is dormant → consider monitored
  watch-and-learn (time-boxed, with exec air cover from the commander).
- Beware tripwires: mass simultaneous isolation can trigger destructive payloads.

## Evidence handling (do it before eradicating)

- **Order of volatility** (RFC 3227): CPU/cache → RAM → network state/ARP/routing
  → running procs/open files → disk → logs/archives → physical config. Capture
  the volatile end _first_. Full memory + targeted disk image.
- Hash on collection (sha256), write-protect, document **chain of custody**
  (who/what/when/where, every transfer); untracked evidence is inadmissible.
- Analyze the _copy_, never the only copy, on an isolated host. For the deep dig:
  `load_skill digital-forensics`. For a captured binary: `load_skill
malware-triage` / `malware-static`.

## Eradication (remove the foothold)

- Remove malware, backdoors, attacker accounts, web shells, persistence (services,
  scheduled tasks, run keys, cron, WMI subs, cloud roles/keys).
- Eradicate the **root cause**, not just the symptom: patch the entry vuln, close
  the misconfig. Use the ATT&CK map: every persistence/defense-evasion technique
  you logged is a thing to remove. Verify with a hunt (`load_skill threat-hunting`)
  before declaring clean.

## Recovery (return to operations)

- Rebuild from known-good (golden image), not by cleaning in place where possible.
- Restore from a backup _predating_ the compromise; verify integrity.
- Reset all credentials that were exposed. Stage the return; **monitor closely**
  with heightened detection for attacker return (they often come back).
- Define exit criteria: clean for N days, no recurring IOCs, vector closed.

## Lessons learned (close the loop)

- Blameless review within ~2 weeks: timeline, dwell time, what detection missed,
  what slowed response. Owned action items, not a doc that rots.
- Feed gaps back: new detections (`load_skill detection-engineering`), new hunts,
  control changes. This is the Govern/Protect feedback in 800-61r3.

## marq tie-in

`report_finding` every confirmed TTP with its ATT&CK id + affected asset as you
work, then `render_report` for the IR write-up. Stage artifacts/timeline under
`/work` (use the file tools; they are sandboxed). Analyse captured samples (copy only)
with YARA/capa/rabin2 in your own analysis sandbox; marq does not run them.
