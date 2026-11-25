---
name: printer-job
description: Execute Commodore and Epson printing workflows through c64bridge.
---

## Intent

Use this skill for printer text output, bitmap output, and custom character definition.

## Inputs

- Printer family: Commodore or Epson.
- Desired output type: text, bitmap row, or custom character definition.
- Any device or secondary-address requirements.

## Execution

1. Use `c64_printer` with `op: "print_text"` for text workflows.
2. Use `c64_printer` with `op: "print_bitmap"` for bitmap row workflows.
3. Use `c64_printer` with `op: "define_chars"` for custom character definitions.
4. Surface any generated BASIC or payload details the user must keep or reuse.

## Validation

1. Confirm which printer family and operation ran.
2. Summarize any generated program text or printer control assumptions.

## Safety

- Confirm printer family before issuing printer-specific control sequences.
