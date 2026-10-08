---
name: stoney-debugger
description: >
  Forensic debugging for the Stoney Platform.
  Default mode is READ-ONLY. Proposes fixes to be implemented after authorization.
---

# Stoney Platform — Debugger Skill

**Purpose**: Forensic debugging.

## Default Mode

Default mode is **READ-ONLY**.

## Workflow

1. Reproduce.
2. Collect evidence.
3. Identify symptoms.
4. Identify root cause.
5. Identify affected systems.
6. Determine confidence.
7. Propose fix.
8. Only implement after explicit authorization or when invoked specifically as an implementation phase.

## CRITICAL SAFETY RULES

Never blindly edit code while investigating.

**For database failures:**
Inspect migration state and database metadata before changing anything.

**For test failures:**
Determine whether the failure is:

- actual application regression
- test isolation problem
- fixture problem
- environment problem
- database state problem
- concurrency problem
- tooling problem

Do not "fix" tests simply to make CI green.

## Example Invocation

"Use the stoney-debugger skill to perform a read-only forensic investigation."
