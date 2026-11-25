---
name: automating-orcad-capture-tcl
description: Use when the user mentions OrCAD, OrCAD Capture, Cadence SPB, .DSN, .OLB, design cache, schematic part placement, PlacePart, PlaceWire, PlacePort, NetAlias, footprint write-back, CIS, ODBC parts database, library recovery, inherited design, or any schematic-side TCL automation request. Covers Cadence SPB 23.1+. Does NOT cover PCB-side / Allegro, PSpice, Constraint Manager, or netlist export.
author: redstone39 <jacky9152@gmail.com>
---

# OrCAD Capture Toolkit — Skill Entry Point

AI agents: read this file and [references/ai-usage.md](references/ai-usage.md).

## When to Trigger This Skill

Load and use this skill whenever a user request falls into any of the following scenarios:

- Writing, modifying, or debugging any OrCAD Capture TCL script
- Mentions of .DSN / .OLB / design cache / Capture automation
- Placing parts / wires / ports, editing properties, or reading schematic structure with PlacePart / PlaceWire / PlacePort
- Recovering a part from an inherited design into a standalone library
- Probing whether the CIS Tcl surface is available, or deciding between Unified CIS / Legacy CapCIS
- Any TCL-related question on the Cadence SPB schematic side

## Out-of-Scope (Do Not Force This Skill)

- **PCB-side / Allegro-side** TCL (routing, constraints, shapes, padstacks) — that is a separate API set
- **PSpice simulation** — simulation commands, profile configuration, waveform analysis
- **Constraint Manager** rule editing
- **Netlist export** to other formats (Allegro / Verilog / Spice / EDIF)
- **Project Manager file-level operations** — e.g., archive, tar/zip project
- **OrCAD X / Cloud** API specifics (some surfaces may differ)
- **Skill / library-level schematic editing** (inherits / sub-circuit hierarchy editing)
- **Batch merging multiple parts** into one .OLB (this toolkit's design cache recovery handles only a single part)

When these topics arise, inform the user that this toolkit does not cover them and suggest they look for dedicated PCB / PSpice / Constraint Manager resources.

## Workflow for AI Agents

1. **Read [`references/ai-usage.md`](references/ai-usage.md)** — decision tree + output specification + composable idiom building blocks (primary entry point)
2. **Read the relevant [`references/`](references/) module** — verify viable APIs, known pitfalls, and version dependencies
3. **Check [`references/anti-patterns.md`](references/anti-patterns.md)** — confirm the APIs you intend to use are not on the DO NOT list
4. **Build on the §5 idiom blocks in ai-usage.md** — do not generate from scratch; do not omit `$lStatus` / `_Resolve` / iterator-delete conventions
5. **Assemble using the user's specific refdes / paths / package names**, and return a single **self-contained `.tcl` tailored to this request**
6. **Include execution steps**: which .DSN to open → which page to navigate to → which snippet to paste into the Command Window → expected log signals

AI does not need to run TCL itself. OrCAD Capture must be open on the user's machine; the user pastes the AI-generated script into `View > Command Window` and executes it.

## Three Content Modules

| Module | Document | Contents |
|--------|----------|----------|
| API Reference | [`references/api-reference.md`](references/api-reference.md) | Verified / pending / infeasible API quick-reference; common pitfalls |
| CIS Probe | [`references/cis-probe.md`](references/cis-probe.md) | Logic specs for 17 probes + Tcl example patterns + 5-step flow |
| Design Cache Recovery | [`references/design-cache-recovery.md`](references/design-cache-recovery.md) | G1/G2/G3 three-stage canonical TCL chain (inline code skeleton) |

Cross-cutting documents (should be consulted for any task):

- [`references/ai-usage.md`](references/ai-usage.md) — AI decision tree, output specification, **composable idiom building blocks** (setup / iter / property / placepart / save / alias / composition example)
- [`references/anti-patterns.md`](references/anti-patterns.md) — centralized DO NOT list
