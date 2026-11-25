---
name: autoreview
description: Run an explicitly requested structured second-model code review and verify findings before changes.
category: development
aliases: []
triggers:
- use autoreview
- run autoreview
keywords:
- autoreview
- development
- explicitly
- requested
- structured
- second
- model
dependencies:
- optional:codex-or-claude-cli
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- autoreview
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- autoreview
- development
- explicitly
- requested
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Autoreview

## Purpose
Run an explicitly requested structured second-model code review and verify findings before changes.

## When to Use
Use when you need to run an explicitly requested structured second-model code review and verify findings before changes. or trigger commands matching use autoreview, run autoreview.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Run an explicitly requested structured second-model code review and verify findings before changes.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
optional:codex-or-claude-cli

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use autoreview"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical development category.
