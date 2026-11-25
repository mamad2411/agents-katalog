---
name: rollback-manager
description: Revert uncommitted file edits, undo database migrations, and clean up temporary scratch files on abort.
category: execution
domain: computer-science
subdomain: runtime-execution
version: 1.0.0
level: intermediate
risk: low
tools:
  - terminal
  - file_write
capabilities:
  - state-rollback
  - atomic-cleanup
inputs:
  - text
  - code
outputs:
  - text
  - structured-data
side_effects:
  - filesystem-read
---

# Rollback Manager

## Overview
Revert uncommitted file edits, undo database migrations, and clean up temporary scratch files on abort.

## Operating Workflow
1. **Precheck**: Verify prerequisites and current environment state.
2. **Execute**: Perform designated rollback-manager operations adhering to least-privilege standards.
3. **Verify**: Assert outcome correctness and log structured telemetry.

## Progressive References
- See `references/guide.md` for in-depth operational protocols.
- See `examples/example.md` for standard execution patterns.
