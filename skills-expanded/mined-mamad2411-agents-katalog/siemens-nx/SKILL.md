---
name: siemens-nx
description: "Automate Siemens NX modeling with NX Open Python and troubleshoot synchronous modeling or Teamcenter integration."
category: cad
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["siemens-nx", "nx-open", "parasolid", "synchronous-technology", "teamcenter", "claude", "cad-automation"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Siemens NX AI Skill Guide (Claude)

## Overview & Engine Architecture
Siemens NX (formerly Unigraphics) is the high-end CAD/CAM/CAE platform powered by the **Siemens Parasolid modeling kernel**. Claude operates as an expert Siemens NX Automation Engineer and PLM Systems Architect, specializing in **NX Open Python automation (`NXOpen`)**, **Synchronous Technology direct modeling**, **Teamcenter active integration**, **5-axis CAM toolpath optimization**, and **headless CLI batch execution via `run_journal.exe`**.

### Siemens NX Technical Architecture & Parasolid Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Siemens NX System Architecture              │
│                                                             │
│  Engineering & Manufacturing Subsystems                     │
│  ├── Parasolid B-Rep Kernel & Synchronous Direct Modeling   │
│  ├── Advanced 5-Axis CAM & Post Configurator (TCL Engine)   │
│  ├── Simcenter 3D Multiphysics FEA / CFD Solvers            │
│  └── Teamcenter PLM Active Workspace / 4-Tier Client Bridge│
│                                                             │
│  Automation & Development Layer                             │
│  ├── NX Open API (Python 3.11, C++, C# .NET, Java)          │
│  ├── Journaling Engine & `run_journal.exe` Batch Processor  │
│  └── Block UI Styler (Custom Native Dialog Framework)       │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **NX Open Python Automation**: Author deterministic, standalone Python scripts using `import NXOpen` to automate feature tree traversal, expression editing, sketch construction, and drafting export.
2. **Synchronous Technology Diagnostics**: Remediate imported geometry face-tearing, sliver faces, and unclosed shells using *Optimize Face*, *Heal Geometry*, and *Replace Face*.
3. **Teamcenter Integration & Revision Management**: Diagnose dataset checkout locks, item revision synchronization failures, and Teamcenter Integration for NX (TCCNX) communication drops.
4. **Headless Batch Scripting (`run_journal.exe`)**: Construct batch conversion utilities to translate enterprise `.prt` archives into STEP AP242 and JT visualization formats.

---

## Production Python Automation: Headless Part Inspector & STEP Exporter (`run_journal.exe`)

Save this script as `export_part.py` and run via `run_journal.exe` to inspect mass properties and export a STEP AP242 file with Semantic PMI annotations:

```python
"""
Siemens NX Open: Mass Property Inspector & STEP AP242 Exporter
Execute via: run_journal.exe export_part.py -args "C:/Parts/bracket.prt" "C:/Export/bracket.stp"
"""

import sys
import os
import NXOpen
import NXOpen.Step242Creator

def process_nx_part(input_prt: str, output_stp: str):
    the_session = NXOpen.Session.GetSession()
    the_uf_session = NXOpen.UF.UFSession.GetUFSession()

    if not os.path.exists(input_prt):
        print(f"Error: Input part '{input_prt}' does not exist.")
        sys.exit(1)

    print(f"Loading Part: {input_prt}...")
    base_part, part_load_status = the_session.Parts.OpenBaseDisplay(input_prt)
    work_part = the_session.Parts.Work

    # 1. Calculate Physical Mass & Inertia Properties
    try:
        solid_bodies = work_part.Bodies.ToArray()
        if solid_bodies:
            mass_props = the_uf_session.Modl.AskMassProps3d(
                [b.Tag for b in solid_bodies], len(solid_bodies), 1, 1, 0.001, 1
            )
            # mass_props[0] is Surface Area, mass_props[1] is Volume, mass_props[2] is Mass
            print(f"Physical Analysis -> Volume: {mass_props[1]:.4f} mm^3 | Mass: {mass_props[2]:.4f} kg")
    except Exception as e:
        print(f"Warning: Could not compute mass properties: {e}")

    # 2. Configure STEP AP242 Export
    step_creator = the_session.DexManager.CreateStep242Creator()
    step_creator.ExportAs = NXOpen.Step242Creator.ExportAsOption.Ap242
    step_creator.InputFile = input_prt
    step_creator.OutputFile = output_stp
    step_creator.ExportPmi = True # Include Product & Manufacturing Info (PMI)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_stp)), exist_ok=True)
    
    # Commit Export
    step_creator.Commit()
    step_creator.Destroy()
    print(f"Successfully exported STEP AP242: {output_stp}")

    # Clean session
    the_session.Parts.CloseAll(NXOpen.BasePart.CloseModified.CloseModified, None)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: run_journal.exe export_part.py -args <input.prt> <output.stp>")
        sys.exit(1)
    process_nx_part(sys.argv[1], sys.argv[2])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Synchronous Move Face Fails on Imported STEP** | Imported geometry contains sliver faces, self-intersecting blends, or gaps within Parasolid tolerance ($10^{-5}$). | 1. Run *Menu $\rightarrow$ Information $\rightarrow$ Geometry $\rightarrow$ Examine Geometry*.<br>2. Check for **Self-Intersection**, **Sheet Boundaries**, and **Tolerant Edges**.<br>3. Apply **Optimize Face** (*Menu $\rightarrow$ Edit $\rightarrow$ Surface $\rightarrow$ Optimize Face*) before moving faces. |
| **Teamcenter Check-In Fails (`Item Revision is Locked`)** | A previous NX session terminated abnormally without releasing the checkout lock on the Teamcenter volume. | 1. In Teamcenter Rich Client / Active Workspace, open **My Worklist**.<br>2. Select the locked dataset $\rightarrow$ *Actions $\rightarrow$ Cancel Check-Out*.<br>3. Check `%TEMP%\NX_Teamcenter_*.log` for stalled session tokens. |
| **Siemens SPLM License Server Error (`-15, Cannot connect to license server`)** | License daemon `ugslmd` is stopped on the server, or firewall blocked TCP port 28000. | 1. Verify `SPLM_LICENSE_SERVER=28000@<SERVER_IP>` in system environment variables.<br>2. Ensure `ugslmd` service is running on license host.<br>3. Check client log at `%LOCALAPPDATA%\Siemens\NX<VER>\syslog.txt`. |
| **CAM Post Configurator TCL Error during Post-Processing** | Custom post-processor encountered unhandled tool axis orientation or missing kinematic vector in machine tool definition. | 1. In NX CAM, enable **Post Configurator Debugger**.<br>2. Inspect `PC_DEBUG_OUTPUT` in the generated `.ptc` log.<br>3. Verify machine kinematic rotary limits ($A/C$ or $B/C$ axes) in Machine Tool Builder. |

---

## Command Line Syntax & Batch Processing

```bash
# Windows CLI: Execute NX Open Python Journal Headless
"%UGII_BASE_DIR%\UGII\run_journal.exe" "C:\Scripts\export_part.py" -args "C:\Parts\engine_block.prt" "C:\Export\engine_block.stp"

# Convert Legacy NX Part File to Current Version
"%UGII_BASE_DIR%\UGII\ug_convert_part.exe" -target_version=NX2312 -u "C:\Models\legacy.prt"

# Launch Siemens NX with Clean Environment
"%UGII_BASE_DIR%\UGII\ugraf.exe" -cleanup
```

### Essential File Locations & Environment Variables
- **`UGII_BASE_DIR`**: Installation root (e.g. `C:\Program Files\Siemens\NX2312`)
- **`SPLM_LICENSE_SERVER`**: License host connection (e.g. `28000@lic-server`)
- **System Configuration File**: `%UGII_BASE_DIR%\UGII\ugii_env.dat`
- **User Log Directory (Syslog)**: `%LOCALAPPDATA%\Siemens\NX<VER>\syslog_*.syslog`

---

## Agent Operational Directive
> **MANDATORY**: Always execute `the_session.Parts.CloseAll()` in batch journals to avoid memory accumulation across multi-part processing. Run *Examine Geometry* prior to synchronous modeling operations on third-party STEP/IGES bodies.
