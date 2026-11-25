---
name: behavior-validator
description: Validate user-visible behavior against a written contract without inspecting implementation source.
category: development
aliases: []
triggers:
- use behavior-validator
- run behavior-validator
keywords:
- behavior-validator
- development
- validate
- user
- visible
- behavior
- against
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- behavior-validator
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
- behavior
- behavior-validator
- development
- user
- validate
- validator
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

# Behavior Validator

## Purpose
Validate user-visible behavior against a written contract without inspecting implementation source.

## When to Use
Use when you need to validate user-visible behavior against a written contract without inspecting implementation source. or trigger commands matching use behavior-validator, run behavior-validator.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Validate user-visible behavior against a written contract without inspecting implementation source.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse the contract into user tasks, expected behavior, anti-cheat probes, setup, and evidence requirements.
2. Prepare runtime access: target URL, CLI command, API endpoint, fixture data, credentials, or generated artifact path.
3. Exercise each user task as a real user or operator would.
4. Run anti-cheat probes: vary fixture data, refresh/retry, test empty and invalid inputs, verify persistence, inspect generated output, and confirm buttons/commands perform real work rather than only displaying success text.
5. Capture evidence as compact redacted notes, screenshots, terminal excerpts, response summaries, file summaries, or accessibility observations. Omit credentials, tokens, cookies, private user data, and unrelated log content.
6. Emit a structured report. Use `references/report-schema.md` when a machine-readable report is useful.
7. If the orchestrator fixes a finding, rerun only the affected contract clauses plus any nearby regression probes.

## Tools
None required (pure logic).

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use behavior-validator"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical development category.
