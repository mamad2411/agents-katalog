---
name: execution-planner
description: Synthesize atomic execution plans with discrete verification gates and failure checkpoints.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - file_read
  - file_write
capabilities:
  - execution-planning
  - task-decomposition
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Execution Planner

## Overview
Synthesize atomic execution plans with discrete verification gates and failure checkpoints.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated execution-planner operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
