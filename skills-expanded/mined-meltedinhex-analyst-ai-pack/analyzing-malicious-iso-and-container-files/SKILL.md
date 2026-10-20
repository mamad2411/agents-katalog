---
name: analyzing-malicious-iso-and-container-files
description: 'Analyzes malicious ISO, IMG, VHD, and similar container files used to smuggle payloads
  past email and mark-of-the-web defenses by enumerating contents and flagging hidden executables,
  LNKs, and scripts. Activates for requests to analyze a malicious ISO/IMG, inspect a container
  delivery file, or find payloads hidden inside a disk image attachment.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - iso
  - container
  - delivery
  - mark-of-the-web
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1553.005
  - T1204.002
  - T1027
d3fend:
  - D3-FCR
  - D3-FA
references:
  - 'MITRE ATT&CK T1553.005 Mark-of-the-Web Bypass — https://attack.mitre.org/techniques/T1553/005/'
  - 'ISO 9660 file system — https://wiki.osdev.org/ISO_9660'
---

# Analyzing Malicious ISO and Container Files

## When to Use

- You have an ISO/IMG/VHD attachment suspected of smuggling a payload (LNK + hidden DLL/EXE/script)
  past MOTW and scanners.
- You need to enumerate contents and flag hidden/executable entries without mounting the image.

**Do not use** mounting/auto-run to inspect — that can trigger the lure. Parse the container's
directory records statically.

## Prerequisites

- The container file (read inertly). Optional: `pycdlib` for full ISO parsing (the script falls
  back to signature/string carving if absent).

## Safety & Handling

- Never mount or open the container interactively; carve statically. Defang any URLs found.

## Workflow

### Step 1: Identify the container type

```bash
python scripts/analyst.py inspect sample.iso
```

Detects ISO 9660 (`CD001`), UDF, FAT/VHD signatures and reports the format.

### Step 2: Enumerate entries and flag payloads

Lists embedded file signatures (`MZ`, `PK`, LNK `\x4C\x00\x00\x00`, script headers) and flags
hidden/executable/decoy entries.

### Step 3: Assess the lure chain

A typical chain is a visible LNK pointing at a hidden DLL/EXE/script in the same image — document
the relationship.

### Step 4: Extract and route

Carve the hidden payload and route it to the appropriate analysis workflow; defang URLs.

## Validation

- The container format is identified by signature.
- Hidden executables/LNKs/scripts are enumerated with offsets.
- The lure→payload relationship is documented.

## Pitfalls

- Mounting the image and triggering the lure.
- Missing payloads in less-common container formats (VHDX, UDF) without the right parser.
- Overlooking hidden-attribute files that the file manager would not show.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the inspector.
- ATT&CK T1553.005 and ISO 9660 references (linked in frontmatter).
