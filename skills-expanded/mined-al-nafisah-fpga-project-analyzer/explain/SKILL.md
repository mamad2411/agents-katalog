---
name: explain
description: Explain an FPGA project (Vivado, Zynq, PYNQ) with an interactive drill-down diagram.
argument-hint: "[project folder]"
disable-model-invocation: true
---
Explain the FPGA project in the folder given as arguments ($ARGUMENTS); if none, use the current folder.
Read `../fpga-project-analyzer/SKILL.md` (relative to this file's directory) and follow its workflow.
Focus on how the design works: a 3-8 word role note for every key block and 1-2 data-flow paths in the
overlay, then render the view. Reply with the diagram link and at most 6 short bullets.
