---
name: artifact-validator
description: Verify generated documents, diagrams, and code artifacts against structural schemas and styling rules.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - file_read
capabilities:
  - artifact-verification
  - schema-validation
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Artifact Validator

## Overview
Verify generated documents, diagrams, and code artifacts against structural schemas and styling rules.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated artifact-validator operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
