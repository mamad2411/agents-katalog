---
name: readme-standard
description: Write and review concise, progressive READMEs with executable examples and verified links.
category: utilities
aliases: []
triggers:
- use readme-standard
- run readme-standard
keywords:
- readme-standard
- utilities
- write
- review
- concise
- progressive
- readmes
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- readme-standard
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- readme
- readme-standard
- review
- standard
- utilities
- write
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

# Readme Standard

## Purpose
Write and review concise, progressive READMEs with executable examples and verified links.

## When to Use
Use when you need to write and review concise, progressive readmes with executable examples and verified links. or trigger commands matching use readme-standard, run readme-standard.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Write and review concise, progressive READMEs with executable examples and verified links.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
None required (pure logic).

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use readme-standard"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical utilities category.
