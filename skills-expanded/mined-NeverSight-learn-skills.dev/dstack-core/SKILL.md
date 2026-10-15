---
name: dstack-core
description: Shared dstack workflow contracts and conventions. Installed as support for the other dstack skills; use directly when reviewing workflow authority, trust boundaries, or naming conventions.
metadata:
  version: "0.5.9"
allowed-tools: Read Bash
---

# dstack Core Contracts

This support skill contains the shared contracts used by the dstack workflows.

Before executing a dstack workflow that links to a reference in this directory, read that reference completely. The
calling skill remains responsible for its workflow-specific authority and completion rules.

## Feature resolution

`<core-dir>/scripts/resolve-feature.py` resolves feature epics through Beads by canonical slug, exact or unique human
name, or ID. Use `--next` to select the next ready feature epic. Workflow commands should expose the canonical `<slug>`
reference and retain the Beads ID only for mutations and audit evidence.
