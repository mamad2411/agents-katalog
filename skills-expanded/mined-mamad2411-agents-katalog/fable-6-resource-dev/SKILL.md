---
name: fable-6-resource-dev
description: >-
  Resource development v6 — build exploit manifest from CVE candidates.
version: 6.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Resource Development (v6)

**Playbook:** `Workflow/resource-development/PLAYBOOK.md`

## Reason first

For each CVE candidate, find/adapt PoC from `arsenal/`. Document params and preauth.

## Output

`resource-development/exploit_manifest.json`

## FORBIDDEN

- Running exploits without manifest entry
- Blind CVE roulette
