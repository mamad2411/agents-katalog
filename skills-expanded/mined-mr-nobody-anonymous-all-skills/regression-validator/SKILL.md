---
name: regression-validator
description: Run regression suites and automated test suites to ensure modifications introduce no breaking changes.
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
  - regression-testing
  - test-suite-execution
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Regression Validator

## Overview
Run regression suites and automated test suites to ensure modifications introduce no breaking changes.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated regression-validator operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
