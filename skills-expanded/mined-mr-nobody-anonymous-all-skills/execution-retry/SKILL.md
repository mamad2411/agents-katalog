---
name: execution-retry
description: Apply exponential backoff, jitter, and adaptive error analysis to recover from transient execution failures.
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
  - error-recovery
  - adaptive-retry
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Execution Retry

## Overview
Apply exponential backoff, jitter, and adaptive error analysis to recover from transient execution failures.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated execution-retry operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
