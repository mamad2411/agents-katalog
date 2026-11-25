---
name: fpga-project-analyzer
description: Analyze and explain existing AMD/Xilinx FPGA projects visually - Vivado block designs (.xpr, .bd, .hwh, .xsa, BD Tcl), Verilog/SystemVerilog/VHDL, PYNQ overlays and notebooks, HLS/bare-metal C, device trees, timing/DRC reports and build logs. Builds a drill-down Vivado-style diagram (block design -> IP -> RTL -> registers) and finds bugs - clock-domain crossings, unconstrained I/O, reset polarity, address map, interrupts, PYNQ overlay mistakes. Use when asked to understand, review, document or debug an FPGA, Zynq, MPSoC or PYNQ project, or a failed Vivado build.
---

# FPGA Project Analyzer

Scripts read the project; you read their compact output. Do not open .bd/.hwh/.xpr/report files directly.
`FPA` below stands for `python3 <this skill's directory>/scripts/fpa.py`; type the full command each time
(a shell variable does not word-split in zsh). Outputs go to `<project>/.fpa/`.

## Workflow
1. `FPA build <project>` - extracts everything, runs the checks, prints a ~40-line summary
   (blocks, clock domains, streams, AXI-MM, IRQ -> GIC/DT numbers, address map, software refs, reports, findings).
   Repo with several boards/builds or a Makefile flow: point it at the build's own lists instead of scanning,
   e.g. `--src sim/plps.d --src sim/psbd.d` (make .d / .f / .lst files, dirs or globs; repeatable).
2. Drill into what matters, never the whole tree:
   - `FPA show <project> <block>` one block (`/` = top, `/stream_proc/scaler_0` = nested): pins, peers,
     net names, clock domains, address, registers, software refs, src file:line; add `--nets` to list the
     nets inside the block as `level|net` keys
   - `FPA findings <project>` all findings with detail and fix
   - `FPA logs <file>` failed build: grouped errors (Vivado, HLS, PetaLinux/Yocto task logs, gcc)
   - `FPA reports <dir>` timing / utilization / DRC / methodology facts from existing .rpt files
3. Open source files only at the file:line that `show` gives, only to confirm a finding or a block's role.
4. Write `<project>/.fpa/overlay.json` (schema below): a role note for each key block, 1-2 flows, and review findings.
5. `FPA view <project>` -> `.fpa/design.html` (offline, single file); it warns about overlay paths or nets that do
   not resolve. Deep links: `design.html#/hier/block`, `?issues=1` (issue list), `?sel=/hier/block` (block panel),
   `?theme=dark`. The viewer's Export menu saves the current level as SVG/PNG.
6. For documentation requests: `FPA doc <project>` -> `.fpa/design.md` with SVG diagrams and tables.

## How to answer
- Visual first: give the file:// link and deep links, then at most 6 short bullets. No pasted reports or long prose.
- "Explain the design" = overlay notes (3-8 words per block) + flows, so the diagram carries the explanation.
- Each finding: what, where (path, file:line), why it breaks hardware, the fix (exact code/Tcl/XDC when short).
- Lint findings (`"by":"lint"`) are candidates; confirm with `show` and the source before calling them bugs.
  Lint is structural; it cannot see functional bugs such as pipeline misalignment or protocol violations.
- For any "what's wrong" or review request, read `references/review.md` once and check the RTL it points to.

## Overlay schema (.fpa/overlay.json)
```json
{"notes": {"/axi_dma_0": "DDR <-> stream mover"},
 "flows": [{"name": "sample path", "nets": ["|axi_dma_0_M_AXIS_MM2S", "/stream_proc|S_AXIS_1"]}],
 "findings": [{"sev": "high|med|low|info", "path": "/stream_proc/stream_scaler_0", "title": "...",
               "detail": "...", "fix": "...", "src": {"file": "rtl/x.v", "line": 19},
               "net": "gain_q", "level": "/stream_proc/stream_scaler_0"}]}
```
Flow nets are `<level path>|<net name>` exactly as `show <project> <level> --nets` prints them; the top level is
the empty path (`|net`). `net` + `level` on a finding draws that wire red.

## Vivado (optional, auto-detected)
- `FPA deep <project> --top <module>`: Vivado-elaborated netlist (RTL_REG, RTL_MUX, operators) for the
  lowest level; merged on the next build. Use when the user wants gate/RTL-cell detail.
- `FPA vivado-reports <run.dcp|project.xpr>`: runs report_cdc, clock interaction, timing, DRC, methodology.
- `FPA build <project> --vivado on`: sources the project's BD Tcl in Vivado for exact pins. This executes
  project code - ask the user before using it on a repository they did not write.

## Limits
Light RTL parsing (no Vivado) evaluates VHDL generics and `if`/`case ... generate` conditions (a
condition it cannot evaluate keeps its branch), draws a `for ... generate` once, and does not evaluate
Verilog generates; when hierarchy looks wrong, say so and offer `deep`. BD Tcl that relies on apply_bd_automation is only partly readable
without Vivado (the summary says so).
