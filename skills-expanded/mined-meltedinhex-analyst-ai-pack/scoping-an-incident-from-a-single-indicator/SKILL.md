---
name: scoping-an-incident-from-a-single-indicator
description: 'Expands one indicator into the full scope of an incident: pivoting across data
  sources to find related hosts, accounts, and infrastructure, building a timeline, and bounding
  what is and is not affected. Activates for requests to scope an incident, pivot from a single
  IOC, or determine the blast radius of a detection.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - incident-response
  - scoping
  - pivoting
  - timeline
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
  - T1078
d3fend:
  - D3-DA
references:
  - 'NIST SP 800-61 Computer Security Incident Handling Guide — https://csrc.nist.gov/pubs/sp/800/61/r2/final'
  - 'MITRE ATT&CK — https://attack.mitre.org/'
---

# Scoping an Incident from a Single Indicator

## When to Use

- A detection fired on one indicator (a hash, IP, domain, or account) and you must find the full
  extent of the activity.
- You need to bound the incident — which hosts, accounts, and infrastructure are involved — before
  containment.
- You are building an investigative timeline from a single starting point.

**Do not use** premature containment on the first indicator alone — acting before scoping can tip
off the adversary and leave footholds you have not yet found.

## Prerequisites

- Access to relevant data sources (EDR, proxy, DNS, auth logs) and the pivoting/enrichment skills.

## Workflow

### Step 1: Characterize the seed indicator

Establish what the indicator is, when it was first/last seen, and on which host/account it
appeared.

### Step 2: Pivot to related artifacts

Expand outward: the file's other hosts, the IP's other connections, the account's other logons,
the domain's other resolvers. Each pivot yields new indicators to pivot again.

```bash
python scripts/analyst.py scope events.json --seed <sha256-or-ip>
```

### Step 3: Build the timeline

Order all discovered events chronologically to reconstruct the activity and find the earliest
sign (candidate patient zero / initial access).

### Step 4: Bound the scope

Define affected vs. unaffected explicitly: list involved hosts/accounts/infrastructure and the
evidence for inclusion, and note what was checked and cleared.

### Step 5: Hand off to containment

Produce the scoped picture (entities, timeline, indicators) so containment is coordinated and
complete rather than piecemeal.

## Validation

- Every included entity has explicit evidence tying it to the incident.
- The timeline has a defensible earliest event (initial access candidate).
- Cleared entities are documented, so scope is bounded, not open-ended.

## Pitfalls

- Containing the first host before pivoting, alerting the adversary and missing other footholds.
- Pivoting only one hop and missing second-order related entities.
- No timeline, so initial access and dwell time stay unknown.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the pivot/scope helper.
- NIST SP 800-61 and MITRE ATT&CK (linked in frontmatter).
