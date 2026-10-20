---
name: cmd-debug
description: Command — Start systematic debugging on a bug, test failure, or unexpected behavior.
---

# /debug

Invokes `Skill(devkit:debugging)` and walks the four phases (root-cause investigation → pattern analysis → hypothesis → fix). No fix attempts until Phase 1 is complete.

If the issue is a cryptic error message, the `error-whisperer` agent may help interpret it before debugging proper begins.

Argument: short description of the symptom. The skill drives the rest.

## Arguments

`[symptom]`
