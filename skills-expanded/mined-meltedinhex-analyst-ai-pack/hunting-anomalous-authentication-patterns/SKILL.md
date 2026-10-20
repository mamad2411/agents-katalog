---
name: hunting-anomalous-authentication-patterns
description: 'Hunts for anomalous authentication such as password spraying, brute force, and
  impossible-travel logons by aggregating Windows logon success/failure events per account and
  source over time. Activates for requests to hunt anomalous logons, detect password spraying or
  brute force, or find suspicious authentication patterns.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - authentication
  - password-spraying
  - brute-force
  - credential-access
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1110.003
  - T1110
  - T1078
d3fend:
  - D3-UA
  - D3-ANET
car:
  - CAR-2013-07-001
references:
  - 'MITRE ATT&CK T1110.003 Password Spraying — https://attack.mitre.org/techniques/T1110/003/'
  - 'Windows Security Event 4625/4624 — https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4625'
---

# Hunting Anomalous Authentication Patterns

## When to Use

- You have Windows logon success (4624) and failure (4625) events and want to detect password
  spraying (one password across many accounts), brute force (many failures per account), and
  suspicious source concentration.
- You are investigating credential-access attempts against accounts.

**Do not use** this for a single failed logon — it relies on aggregation across accounts/sources
to find patterns, not individual events.

## Prerequisites

- Logon events with account, source IP/host, status, and timestamp.

## Workflow

### Step 1: Aggregate auth outcomes

```bash
python scripts/analyst.py hunt logons.csv
```

Computes failures per account, distinct accounts targeted per source (spray signal), and
failure→success transitions per account (possible compromise).

### Step 2: Surface patterns

- Spray: one source failing against many distinct accounts.
- Brute force: many failures against one account from a source.
- Breakthrough: a burst of failures followed by a success.

### Step 3: Confirm

Correlate sources with known infrastructure; check whether successes are legitimate.

### Step 4: Operationalize

Set thresholds and write a detection (e.g., source touching ≥ N accounts within a window).

## Validation

- Spray detection keys on distinct-account breadth per source, not raw failure count.
- Brute force keys on per-account failure concentration.
- Failure-then-success transitions are reported for follow-up.

## Pitfalls

- Service accounts/misconfigured apps generating benign failure storms.
- NAT/proxy collapsing many users behind one source IP, mimicking spray.
- Time-window choice: too wide hides bursts, too narrow misses slow sprays.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1110.003 and Event 4625/4624 docs (linked in frontmatter).
