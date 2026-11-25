---
name: checkpoint-manager
description: Record intermediate execution checkpoints and memory state to enable resumable long-running agent jobs.
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
  - state-checkpointing
  - resumable-execution
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Checkpoint Manager

## Overview
Record intermediate execution checkpoints and memory state to enable resumable long-running agent jobs.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated checkpoint-manager operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
