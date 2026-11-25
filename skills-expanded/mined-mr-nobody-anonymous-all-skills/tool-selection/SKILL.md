---
name: tool-selection
description: Select the minimal, safest, and most effective tool or MCP server for a given operational task.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - file_read
capabilities:
  - tool-optimization
  - least-privilege-selection
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Tool Selection

## Overview
Select the minimal, safest, and most effective tool or MCP server for a given operational task.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated tool-selection operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
