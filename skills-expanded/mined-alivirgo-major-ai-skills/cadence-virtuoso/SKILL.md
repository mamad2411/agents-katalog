---
name: cadence-virtuoso
description: "Automate Cadence Virtuoso design and simulation with SKILL, OCEAN, and Spectre; inspect DRC and LVS verification results."
category: eda
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["cadence-virtuoso", "ic-design", "spectre", "ocean-scripting", "cadence-skill", "drc-lvs", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Cadence Virtuoso IC Design AI Skill Guide (Claude)

## Overview & Engine Architecture
Cadence Virtuoso is the premier analog, RF, and mixed-signal integrated circuit (IC) design environment, built on the **OpenAccess (OA) database standard**. Virtuoso integrates transistor-level schematic capture, full-custom polygon layout, physical verification (DRC/LVS via **Pegasus / PVS / Assura**), parasitic extraction (**Quantus QRC**), and SPICE simulation via the **Spectre Circuit Simulator**. Automation is driven by the Lisp-based **Cadence SKILL** programming language and the **OCEAN (Open Command Environment for Analysis)** batch simulation framework. Claude operates as a Principal Analog IC Design Lead and Tapeout Verification Architect, specializing in **SKILL layout automation**, **OCEAN PVT corner & Monte Carlo characterization**, **DRC/LVS debug**, and **OA database concurrency**.

### Cadence Virtuoso & Spectre Execution Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Cadence Virtuoso Architecture               │
│                                                             │
│  Design Entry & OpenAccess Database                         │
│  ├── `cds.lib` Library Registry & OpenAccess (OA) Hierarchies│
│  ├── Virtuoso Schematic Editor (Transistor-Level Composer)  │
│  └── Virtuoso Layout Suite (Full-Custom Sub-Micron Polygon) │
│                                                             │
│  Simulation & Physical Verification Stack                   │
│  ├── Spectre / Spectre X FastSPICE Multi-Threaded Engine    │
│  ├── OCEAN Batch Simulation Framework & SKILL API           │
│  └── Pegasus / PVS Physical Verification (DRC, LVS, QRC)    │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **OCEAN Batch Simulation Automation**: Author robust OCEAN scripts (`.ocn`) to execute multi-corner PVT sweeps (Process: TT/FF/SS/FS/SF, Voltage $\pm 10\%$, Temperature $-40^\circ\text{C}$ to $125^\circ\text{C}$) and export bandwidth, phase margin, and slew rate metrics.
2. **Cadence SKILL Programming**: Write clean SKILL functions (`procedure()`, `dbCreateRect()`, `dbOpenCellViewByType()`) for procedural layout generation, guard ring placement, and pin placement.
3. **DRC / LVS Physical Verification Triage**: Resolve complex layout-versus-schematic mismatches, short circuits, soft-check substrate taps, and antenna ratio violations.
4. **OpenAccess Lock & Environment Management**: Diagnose and clean stale `.cdslck` file locks, configure `~/.cdsinit` startup scripts, and resolve technology display definitions (`display.drf`).

---

## Production OCEAN Automation: Automated PVT Corner & AC Stability Characterization

Save this script as `run_pvt_ac_corners.ocn` and execute via `ocean -replay run_pvt_ac_corners.ocn`:

```lisp
;; ==============================================================================
;; OCEAN Automation Script: Op-Amp AC Gain, Bandwidth & Phase Margin Sweep
;; Sweeps Process Corners (TT, FF, SS), Voltages, and Temperatures
;; ==============================================================================

simulator('spectre)
design("/home/engineer/simulation/OpAmp_TB/spectre/schematic/netlist/netlist")
resultsDir("/home/engineer/simulation/OpAmp_TB/spectre/results")

;; Define Simulation Analyses
analysis('dc ?saveOppoint t)
analysis('ac ?start "1" ?stop "10G" ?dec "20")

;; Define Design Variables
desVar("Vin_cm" 0.9)
desVar("Rload" 100k)
desVar("Cload" 1p)

;; Corner Definitions
corners = list(
    list("TT" "/pdk/models/spectre/corners.scs" "tt_lib" 27 1.8)
    list("FF" "/pdk/models/spectre/corners.scs" "ff_lib" -40 1.98)
    list("SS" "/pdk/models/spectre/corners.scs" "ss_lib" 125 1.62)
)

out_file = outfile("/home/engineer/reports/corner_summary.csv" "w")
fprintf(out_file "Corner,Temp_C,VDD_V,DC_Gain_dB,UG_Bandwidth_MHz,Phase_Margin_Deg\n")

foreach(c corners
    c_name = nth(0 c)
    model_file = nth(1 c)
    section = nth(2 c)
    temp_val = nth(3 c)
    vdd_val = nth(4 c)

    printf("\n>>> Running Corner: %s | Temp: %d C | VDD: %.2f V...\n" c_name temp_val vdd_val)

    includeModelFile(model_file ?section section)
    temp(temp_val)
    desVar("VDD" vdd_val)

    run()
    selectResults('ac)

    ;; Calculate Key Small-Signal Metrics
    vout = v("/Vout" ?result 'ac)
    vin  = v("/Vin_p" ?result 'ac) - v("/Vin_n" ?result 'ac)
    gain_mag = db20(vout / vin)
    gain_phase = phase(vout / vin)

    dc_gain = value(gain_mag 1.0)
    ugb = cross(gain_mag 0 1 "falling")
    pm = 180.0 + value(gain_phase ugb)

    fprintf(out_file "%s,%d,%.2f,%.2f,%.2f,%.2f\n" c_name temp_val vdd_val dc_gain (ugb / 1e6) pm)
    printf("  • DC Gain: %.2f dB | UGB: %.2f MHz | PM: %.2f deg\n" dc_gain (ugb / 1e6) pm)
)

close(out_file)
printf("\nPVT Corner Analysis Complete. Report saved to corner_summary.csv\n")
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **LVS Fails: `Unmatched Nets / Ports`** | Text labels placed on `drawing` layer instead of `pin` layer, or case-sensitive net name mismatch between schematic and layout. | 1. Ensure pin labels are drawn using the exact layer-purpose pair (`MetalX` with purpose `pin` or `label`).<br>2. Check for port directionality mismatches (Input vs Output).<br>3. Inspect the Assura/PVS `lvs.rep` detailed discrepancy report. |
| **Spectre DC Convergence Failure (`gmin stepping failed`)** | Floating high-impedance nodes, bistable latches without initial bias, or steep non-linear diode models. | 1. Add `.ic` initial conditions to internal floating nodes: `analysis('dc ?force "dev_init")`.<br>2. Set `gmin=1e-12` and `cmin=1e-15` in Spectre simulation options.<br>3. Enable homotopy aids: `homotopy=all` or `homotopy=source`. |
| **`Cannot lock cellView: .cdslck file exists`** | Previous Virtuoso session terminated abnormally, leaving orphaned OpenAccess database lock files. | 1. Find stale lock file: `find <library_dir> -name "*.cdslck"`.<br>2. Verify no active Virtuoso PID owns the lock using `clsAdminTool`.<br>3. Remove orphaned lock: `rm <cell_path>/*.cdslck`. |
| **Quantus QRC Extraction Fails: `Techfile Missing`** | The QRC technology file (`qrcTechFile`) is not mapped in `cds.lib` or the process layer map is out of date. | 1. Verify path to PDK QRC rules in extraction options.<br>2. Check layer map file (`pvs_qrc.layermap`) matches current GDSII stream numbers. |

---

## Command Line Syntax & Environment Control

```bash
# 1. Launch Virtuoso in Background with Dedicated Log
virtuoso -log ~/logs/cds_session.log &

# 2. Run Headless OCEAN Simulation Script
ocean -replay ~/scripts/run_pvt_ac_corners.ocn -log ~/logs/ocean.log

# 3. Multi-Threaded Spectre Simulation via CLI (8 CPU Threads)
spectre +mt=8 -raw ./psf input.scs

# 4. Check and Remove Orphaned OpenAccess Locks
clsAdminTool -kill <hostname> <pid>
```

### Essential File & Environment Locations
- **Cadence Initialization**: `~/.cdsinit` and `~/.cdsenv`
- **Library Catalog**: `<project_dir>/cds.lib`
- **Display Resource File**: `<project_dir>/display.drf`

---

## Agent Operational Directive
> **MANDATORY**: When diagnosing LVS mismatches, verify that pin labels reside on the explicit `pin` or `label` Layer-Purpose Pair (LPP), not `drawing`. Always execute multi-corner PVT and Monte Carlo sweeps before sign-off.
