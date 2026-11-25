---
name: post-execution-audit
description: Perform a comprehensive post-execution security, code quality, and documentation audit before completion.
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
  - post-audit
  - compliance-verification
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Post Execution Audit

## Overview
Perform a comprehensive post-execution security, code quality, and documentation audit before completion.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated post-execution-audit operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
