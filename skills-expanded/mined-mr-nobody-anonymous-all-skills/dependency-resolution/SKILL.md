---
name: dependency-resolution
description: Resolve missing packages, tool dependencies, and version incompatibilities prior to execution.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - terminal
  - file_read
  - file_write
capabilities:
  - dependency-resolution
  - package-management
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Dependency Resolution

## Overview
Resolve missing packages, tool dependencies, and version incompatibilities prior to execution.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated dependency-resolution operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
