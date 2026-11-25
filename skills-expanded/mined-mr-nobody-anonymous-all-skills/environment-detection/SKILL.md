---
name: environment-detection
description: Detect OS, CPU architecture, installed runtimes, shell environments, and container runtimes dynamically.
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
  - environment-discovery
  - runtime-detection
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Environment Detection

## Overview
Detect OS, CPU architecture, installed runtimes, shell environments, and container runtimes dynamically.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated environment-detection operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
