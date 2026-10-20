---
name: plc
domain: automation
level: domain
description: Vendor-agnostic PLC methodology — scan cycles, IO addressing conventions, and safety-relevant state — before any vendor-specific detail.
tags: [plc, ladder-logic, automation, "scan cycle"]
triggers: [plc, "ladder logic", "programmable logic controller", "scan cycle"]
version: "1.0.0"
requires: []
recommends: []
capabilities: []
conflicts: []
when_to_use: Any task involving a PLC, regardless of vendor — load this before a vendor-specific skill like automation/siemens-s7.
when_not_to_use: A microcontroller-only project with no PLC in the loop.
---

# Skill: plc

## Purpose

The methodology every PLC shares, independent of Siemens/Allen-Bradley/Delta/etc. — load
this first, then a vendor skill for the specifics.

## Method

1. **Scan cycle** — a PLC repeatedly reads inputs, executes the whole program, then writes
   outputs, in that order, every cycle. Code that assumes an output changes mid-cycle
   (instead of at the next scan) is a common source of confusing behavior.
2. **Addressing conventions are not universal** — the same physical register can be
   addressed differently across vendors and even across protocol layers on the same
   vendor's own hardware (see automation/modbus's PDU-vs-reference-number gotcha). Never
   assume an address maps directly without checking the specific vendor/protocol
   convention in use.
3. **Safety-relevant state** (E-stops, interlocks, watchdog outputs) is generally
   fail-safe-by-design at the hardware level — don't "fix" a safety circuit in software
   without understanding why it was wired the way it was.
4. **IO simulation before hardware** — when available, test logic changes against simulated
   IO before writing to a live process; a PLC output can move real machinery.

## Anti-patterns

- Assuming an output takes effect immediately rather than at the next scan boundary.
- Copy-pasting a register address from one project to another without re-verifying the
  addressing convention for the new vendor/protocol.
