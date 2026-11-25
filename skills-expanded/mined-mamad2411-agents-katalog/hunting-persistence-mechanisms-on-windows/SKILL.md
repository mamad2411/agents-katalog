---
name: hunting-persistence-mechanisms-on-windows
description: 'Hunts for Windows persistence across autostart locations: Run keys, services,
  scheduled tasks, WMI event subscriptions, and startup folders, baselining them to surface
  anomalous or recently added entries. Activates for requests to hunt persistence, audit
  autostart extensibility points, or find malware autoruns on Windows.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - persistence
  - windows
  - autoruns
  - registry
  - scheduled-tasks
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1547.001
  - T1543.003
  - T1053.005
  - T1546.003
d3fend:
  - D3-PSMD
  - D3-SFA
references:
  - 'MITRE ATT&CK TA0003 Persistence — https://attack.mitre.org/tactics/TA0003/'
  - 'Autoruns (Sysinternals) — https://learn.microsoft.com/sysinternals/downloads/autoruns'
---

# Hunting Persistence Mechanisms on Windows

## When to Use

- You are hunting for how an adversary maintains a foothold across reboots.
- You have autostart inventories (Autoruns exports, registry/scheduled-task/WMI dumps) from
  one or many hosts and want to surface anomalies.
- You want to baseline a fleet and flag entries that deviate or were recently added.

**Do not use** a single host's autoruns list as ground truth — many legitimate entries look
unusual; comparison against a fleet baseline is what makes anomalies meaningful.

## Prerequisites

- Autostart data per host: Run/RunOnce keys, services, scheduled tasks, WMI event
  subscriptions, startup folders, and (ideally) signing status.
- A baseline (golden image or fleet majority) to diff against.

## Workflow

### Step 1: Inventory the ASEPs

Collect the common Autostart Extensibility Points across hosts: Run keys (T1547.001), services
(T1543.003), scheduled tasks (T1053.005), and WMI subscriptions (T1546.003).

### Step 2: Baseline and diff

Compare each host's entries to the fleet baseline; entries appearing on few hosts, unsigned,
or pointing to user-writable/temp paths bubble up.

```bash
python scripts/analyst.py hunt autostart.json --baseline baseline.json
```

### Step 3: Score anomalies

Raise priority for: unsigned binaries, LOLBins launched with encoded args, paths in
`%TEMP%`/`%APPDATA%`, recently created tasks, and WMI consumers running scripts.

### Step 4: Triage candidates

For each high-score entry, pull the target binary's signing/hash, the creating user/time, and
correlate with process and network telemetry.

### Step 5: Confirm and respond

Validate suspicious entries (sandbox/RE the binary), escalate confirmed persistence to IR, and
turn the pattern into a detection.

## Validation

- Anomalies are ranked against a baseline, not flagged from one host in isolation.
- High-score entries map to concrete artifacts (path, hash, signer) for triage.
- Confirmed persistence ties back to a known intrusion timeline.

## Pitfalls

- Treating every unsigned entry as malicious; many legitimate tools are unsigned.
- Checking only Run keys and missing services/tasks/WMI subscriptions.
- No timestamps, so you cannot distinguish long-standing from newly planted entries.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the autostart hunter.
- ATT&CK Persistence tactic and Autoruns (linked in frontmatter).
