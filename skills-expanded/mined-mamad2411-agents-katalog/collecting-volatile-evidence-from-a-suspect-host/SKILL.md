---
name: collecting-volatile-evidence-from-a-suspect-host
description: 'Collects volatile evidence from a potentially compromised host in correct order of
  volatility: memory, network state, running processes, logged-on users, and open handles, while
  preserving integrity and minimizing footprint. Activates for requests to collect volatile
  evidence, perform live response, or capture host state before shutdown.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - live-response
  - volatile-evidence
  - forensics
  - incident-response
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1057
  - T1049
d3fend:
  - D3-PSA
  - D3-SFA
references:
  - 'RFC 3227 Guidelines for Evidence Collection and Archiving — https://www.rfc-editor.org/rfc/rfc3227'
  - 'NIST SP 800-86 forensic techniques — https://csrc.nist.gov/pubs/sp/800/86/final'
---

# Collecting Volatile Evidence from a Suspect Host

## When to Use

- A host is suspected of compromise and you must capture state that disappears on reboot.
- You are performing live response before isolating or imaging the machine.
- You need an ordered, integrity-preserving collection for later analysis.

**Do not use** this as a substitute for full disk imaging when persistence matters — volatile
collection complements, not replaces, a forensic image. And do not reboot before collecting.

## Prerequisites

- Trusted, statically linked collection tools run from external media (not host binaries).
- Authorization to collect, and a destination on external/write-once media.

## Safety & Handling

- Assume host tools are compromised; use your own trusted binaries to avoid rootkit deception.
- Hash every artifact at collection time and record actions for chain of custody; minimize
  changes to the host.

## Workflow

### Step 1: Follow the order of volatility

Collect most-volatile first (RFC 3227): CPU/registers and cache → RAM → network state and
connections → running processes → logged-on users/sessions → open files/handles → then disk.

### Step 2: Capture memory first

Acquire a full RAM image with a trusted acquisition tool before anything that alters memory; it
is the richest and most perishable source.

### Step 3: Snapshot network and process state

Record active connections, listening ports, ARP/DNS cache, running processes with command lines
and parent links, and loaded modules.

```bash
python scripts/analyst.py manifest ./collection --case IR-42 --host WS01
```

### Step 4: Record users and handles

Capture logged-on users, sessions, scheduled tasks, and open handles/files.

### Step 5: Hash, log, and hand off

Hash each artifact, write a collection manifest with timestamps, and transfer to the analysis
environment preserving integrity.

## Validation

- Artifacts are collected in order of volatility, memory first, before any reboot.
- Every artifact has a recorded hash and collection timestamp in the manifest.
- Trusted external tools were used; host changes are documented.

## Pitfalls

- Rebooting or shutting down before capturing RAM, destroying the best evidence.
- Using the host's own (possibly trojaned) tools and trusting their output.
- No hashing/manifest, undermining evidentiary integrity.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the manifest helper.
- RFC 3227 and NIST SP 800-86 (linked in frontmatter).
