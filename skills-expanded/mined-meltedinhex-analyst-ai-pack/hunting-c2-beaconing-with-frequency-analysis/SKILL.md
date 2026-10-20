---
name: hunting-c2-beaconing-with-frequency-analysis
description: 'Detects command-and-control beacons in network logs by analyzing connection
  timing: measuring inter-arrival intervals, accounting for jitter, and scoring regularity per
  source/destination pair to surface periodic callbacks. Activates for requests to hunt C2
  beaconing, find periodic callbacks, or analyze connection-interval regularity.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - command-and-control
  - beaconing
  - network
  - frequency-analysis
  - jitter
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071.001
  - T1071
  - T1573
d3fend:
  - D3-NTA
  - D3-CA
references:
  - 'MITRE ATT&CK T1071 Application Layer Protocol — https://attack.mitre.org/techniques/T1071/'
  - 'Beaconing detection via inter-arrival timing — https://www.activecountermeasures.com/'
---

# Hunting C2 Beaconing with Frequency Analysis

## When to Use

- You have connection logs (proxy, firewall, Zeek/`conn.log`, NetFlow) and want to find implants
  that call home on a schedule.
- You are testing a hypothesis that a beacon is hiding in normal-looking web traffic.
- You need to rank source→destination pairs by timing regularity, allowing for jitter.

**Do not use** pure interval regularity as a verdict — software update checks, telemetry, and
keep-alives also beacon; combine timing with destination reputation and data volume.

## Prerequisites

- Connection records with timestamp, source, destination (IP/domain), and ideally bytes, over a
  window long enough to capture many callbacks (hours to days).
- A way to enrich destinations (reputation, age, rarity) for follow-up.

## Workflow

### Step 1: Group and order by pair

Bucket connections by (source, destination) and sort timestamps. Require a minimum count so the
interval statistics are meaningful.

### Step 2: Compute inter-arrival intervals

Derive deltas between consecutive connections per pair; the interval distribution reveals
periodicity.

### Step 3: Score regularity with jitter tolerance

A low coefficient of variation (std/mean) of intervals indicates a steady beacon; modern beacons
add jitter, so score on tolerance rather than requiring identical intervals.

```bash
python scripts/analyst.py beacon conn.json --min-events 8
```

### Step 4: Reduce false positives

Down-rank known update/telemetry destinations and CDNs; up-rank rare/young domains, small fixed
payload sizes, and odd ports.

### Step 5: Triage and confirm

For top pairs, pull payloads/JA3, destination intel, and host context; confirm via the C2/beacon
config skills and escalate.

## Validation

- Top candidates show consistently spaced callbacks (low CV) over many events, not a handful.
- Known-benign periodic services are filtered or explained.
- Confirmed beacons corroborate with destination reputation or payload analysis.

## Pitfalls

- Too few events per pair, making the interval statistics noise.
- Requiring perfect periodicity and missing jittered beacons.
- Ignoring data-volume regularity, a strong secondary beacon signal.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the beacon scorer.
- ATT&CK T1071 and inter-arrival timing analysis (linked in frontmatter).
