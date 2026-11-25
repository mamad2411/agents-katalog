---
name: preflight-check
description: Execute rigorous preflight validation before running commands, checking working tree, network, and disk space.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - terminal
  - file_read
capabilities:
  - preflight-validation
  - system-readiness-check
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Preflight Check

## Overview
Execute rigorous preflight validation before running commands, checking working tree, network, and disk space.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated preflight-check operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
