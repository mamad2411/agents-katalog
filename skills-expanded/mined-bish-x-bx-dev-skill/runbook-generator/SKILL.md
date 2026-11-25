---
name: "runbook-generator"
description: "Runbook Generator"
---

# Runbook Generator

**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** DevOps / Site Reliability Engineering

---

## Overview

Generate operational runbooks from bundled templates, then customize for deployment, incident response, maintenance, and rollback workflows.

## Core Capabilities

- Template-first runbook scaffolding
- Standard sections for start/stop/health/rollback
- Structured escalation and incident handling placeholders
- Reference templates for deployment and incident playbooks

---

## When to Use

- A service has no runbook and needs a baseline immediately
- Existing runbooks are inconsistent across teams
- On-call onboarding requires standardized operations docs
- You need repeatable runbook scaffolding for new services

---

## Quick Start

1. Open `references/runbook-templates.md`.
2. Choose the deployment, incident, maintenance, or rollback template.
3. Copy the selected template into the service repository's runbook location.
4. Replace placeholders with service-specific owners, commands, dashboards, health checks, and escalation contacts.

---

## Recommended Workflow

1. Start from the closest template in `references/runbook-templates.md`.
2. Fill in service-specific commands and URLs.
3. Add verification checks and rollback triggers.
4. Dry-run in staging.
5. Store runbook in version control near service code.

---

## Reference Docs

- `references/runbook-templates.md`

---

## Common Pitfalls

- Missing rollback triggers or rollback commands
- Steps without expected output checks
- Stale ownership/escalation contacts
- Runbooks never tested outside of incidents

## Best Practices

1. Keep every command copy-pasteable.
2. Include health checks after every critical step.
3. Validate runbooks on a fixed review cadence.
4. Update runbook content after incidents and postmortems.
