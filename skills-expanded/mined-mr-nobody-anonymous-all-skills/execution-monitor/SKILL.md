---
name: execution-monitor
description: Continuously monitor streaming command output, process health, and memory consumption during tasks.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - terminal
  - manage_task
capabilities:
  - process-monitoring
  - telemetry-tracking
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Execution Monitor

## Overview
Continuously monitor streaming command output, process health, and memory consumption during tasks.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated execution-monitor operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
