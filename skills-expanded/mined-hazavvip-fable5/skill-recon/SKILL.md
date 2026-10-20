---
name: fable-6-recon
description: >-
  Recon v6.1 — primary vs chain triage; exact artifact paths; fable-util check after run.
version: 6.1.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch]
---

# Reconnaissance (v6.1)

**Playbook:** `Workflow/reconnaissance/PLAYBOOK.md`

## Reason first

1. Read intake brief + dead_ends
2. Decide if bulk recon utility helps
3. After pipeline output, **you** write triage + fingerprint at exact paths

## Optional utility (recommended)

```bash
bin/fable-util recon --target {domain} --campaign campaigns/{domain} --stage all
bin/fable-util check campaigns/{domain} --phase reconnaissance --strict
```

## Mandatory agent outputs (exact paths)

| File | Path |
|------|------|
| triage | `reconnaissance/triage_decision.json` |
| fingerprint | `reconnaissance/fingerprint.json` |

**NOT** `reconnaissance/intel/` — forbidden.

### triage_decision.json

- **primary_targets:** ONLY from `verified_signals.json` (with `signal_ref`)
- **chain_targets:** cred leaks, unverified login surfaces, high-value unverified hosts

Cred leak → **chain_targets**, never primary.

## FORBIDDEN

- `reconnaissance/intel/*` paths
- PRIMARY from cred leak or unverified candidates
- Scaffold JSON from scripts
- CVE exploit in recon phase
