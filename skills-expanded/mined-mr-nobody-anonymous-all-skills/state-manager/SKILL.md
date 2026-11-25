---
name: state-manager
description: Synchronize session state, workflow contexts, and active stack definitions across agent transitions.
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
  - session-state-sync
  - context-tracking
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# State Manager

## Overview
Synchronize session state, workflow contexts, and active stack definitions across agent transitions.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated state-manager operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
