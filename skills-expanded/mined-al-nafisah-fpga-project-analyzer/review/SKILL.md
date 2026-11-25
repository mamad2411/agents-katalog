---
name: review
description: Review an FPGA project for hardware bugs - clock-domain crossings, pins, resets, address map, PYNQ overlay mistakes.
argument-hint: "[project folder]"
disable-model-invocation: true
---
Review the FPGA project in the folder given as arguments ($ARGUMENTS); if none, use the current folder.
Read `../fpga-project-analyzer/SKILL.md` (relative to this file's directory) and follow its workflow, including
`references/review.md`. Confirm each lint finding against the source, add what lint cannot see, and put every
confirmed finding (with file:line and fix) in the overlay. Reply with the diagram link (`?issues=1`) and the
findings ranked by severity.
