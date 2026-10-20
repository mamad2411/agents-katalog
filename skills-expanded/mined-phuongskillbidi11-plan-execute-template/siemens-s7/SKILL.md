---
name: siemens-s7
domain: automation
level: technology
description: Siemens S7 (S7-1200/1500/300/400) specifics — DB/data-block addressing and the S7comm/S7comm-plus protocol split — layered on general PLC methodology.
tags: [siemens, s7, s7-1200, s7-1500, tia-portal]
triggers: [siemens, s7, "s7-1200", "s7-1500", "tia portal", s7comm]
version: "1.0.0"
requires: [automation/plc]
recommends: []
capabilities: []
conflicts: []
when_to_use: Any task targeting a Siemens S7-family PLC specifically.
when_not_to_use: A different PLC vendor — load automation/plc plus that vendor's own skill instead.
---

# Skill: siemens-s7

## Purpose

What's specific to Siemens S7 hardware, on top of the vendor-agnostic PLC methodology in
`automation/plc` (a hard dependency of this skill — always loaded alongside it).

## Specifics

1. **Data blocks (DBs) are the primary addressing unit** — a tag lives at `DBx.DBWy`/
   `DBx.DBXy.z` (block number, then byte/bit offset), not a flat global address space. Two
   different DB numbers with the same offset are unrelated memory.
2. **S7-1200/1500 default to "optimized" block access**, which hides absolute byte offsets
   unless the DB's optimized-access setting is explicitly disabled in TIA Portal — a
   symbolic tag name in optimized blocks has no fixed byte offset to hand to an external
   tool.
3. **Protocol split** — older S7-300/400 and S7-1200/1500 in compatible mode speak S7comm;
   newer S7-1500 (and S7-1200 by default since firmware V4) prefer S7comm-plus, which adds
   session-based authentication and isn't a drop-in wire-compatible replacement for tools
   built against S7comm.
4. **This is a real S7-family PLC** — everything in `automation/plc` (scan cycle,
   addressing conventions are not universal, safety-relevant state) still applies
   underneath.

## Anti-patterns

- Assuming a symbolic tag name maps to a fixed byte offset without checking the DB's
  optimized-access setting.
- Reusing an S7comm client library against an S7-1500 configured for S7comm-plus-only
  access and assuming a connection failure means the network is broken.
