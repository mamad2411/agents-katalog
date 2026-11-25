---
name: result-validator
description: Audit execution output against intended success criteria, exit codes, and operational benchmarks.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - file_read
  - terminal
capabilities:
  - outcome-verification
  - benchmark-auditing
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Result Validator

## Overview
Audit execution output against intended success criteria, exit codes, and operational benchmarks.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated result-validator operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
