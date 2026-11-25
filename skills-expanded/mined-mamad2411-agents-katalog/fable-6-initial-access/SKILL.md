---
name: fable-6-initial-access
description: >-
  Initial access v6 — audit stack, CVE map, methodology plan. NOT exploit delivery.
version: 6.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch]
---

# Initial Access (v6)

**Playbook:** `Workflow/initial-access/PLAYBOOK.md`

## This phase is audit + planning

You verify recon, map CVEs, rank tracks. **Exploit delivery is execution phase.**

## Reason first

1. Confirm product+version per PRIMARY host
2. Map CVE candidates or document exhaustion
3. Rank cred vs CVE vs upload vs config tracks

## Optional utilities

- `tools/utilities/cve_lookup.py` when version confirmed
- `tools/utilities/credential_spray.py` only if methodology selects cred track

## Artifacts

attack_surface_audit.json, cve_candidates.json, methodology_plan.json

## FORBIDDEN

- curl/sqlmap/shell upload delivery here
- Blind spray without plan
