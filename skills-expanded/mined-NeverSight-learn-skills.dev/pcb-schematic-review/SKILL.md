---
name: pcb-schematic-review
description: Review schematics, PCB planning, board-level interfaces, power trees, clocks, reset networks, and layout-sensitive risks. Use when checking a board design, preparing bring-up, auditing connector or peripheral choices, or debugging a hardware-software integration issue rooted in the board itself.
---
# PCB Schematic Review

Use this skill when the board may be the hidden source of the system bug.

## Core Workflow

1. Identify the board purpose, power domains, clocks, and external interfaces.
2. Review the power tree and reset behavior first.
3. Check signal direction, voltage compatibility, pull-ups, termination, and protection.
4. Map critical peripherals to firmware expectations.
5. End with bring-up order and measurement points.

## Execution Rules

1. Power, clock, and reset deserve priority over secondary peripherals.
2. Be explicit about what requires layout review versus what is visible from the schematic.
3. Separate likely board issues from likely firmware issues.
4. Highlight components with long lead time or substitution risk when relevant.

## Output Contract

Return:

1. Board summary.
2. Critical risks.
3. Bring-up sequence.
4. Measurement points.
5. Open electrical questions.
