---
name: altium-designer
description: "Automate Altium Designer PCB workflows with DXP scripts, design-rule checks, OutJob fabrication outputs, and routing configuration."
category: eda
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["altium-designer", "pcb-design", "ecad", "dxp-scripting", "drc-rules", "gerber-outjob", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Altium Designer PCB Engineering AI Skill Guide (Claude)

## Overview & Engine Architecture
Altium Designer is the industry-leading unified electronic computer-aided design (ECAD) software suite for schematic capture, multi-layer PCB layout, FPGA co-design, and high-speed signal integrity analysis. Altium runs on the **DXP software platform (`X2.exe`)**, featuring real-time **Design Rule Checking (DRC)**, an advanced **Layer Stack Manager**, and an extensible **DXP Scripting Engine (supporting DelphiScript, Python, VBScript, and JavaScript)**. Claude operates as a Senior Hardware Engineering Lead and PCB Layout Specialist, specializing in **high-speed differential pair routing & length tuning**, **OutJob manufacturing package generation (Gerber X2, IPC-2581, ODB++)**, **ActiveBOM lifecycle management**, and **DXP automation scripting**.

### Altium Designer Unified ECAD Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Altium Designer Architecture                │
│                                                             │
│  Design & Modeling Workspaces                               │
│  ├── Unified Schematic Editor & Multi-Sheet Hierarchy       │
│  ├── PCB Editor & High-Speed Interactive Push/Shove Router  │
│  └── 3D ECAD-MCAD Co-Design (Native STEP 3D Clearance)      │
│                                                             │
│  Automation & Manufacturing Layer                           │
│  ├── DXP Automation Scripting Engine (`PCBServer`, `DM`)    │
│  ├── Real-Time & Batch Design Rule Checker (DRC Engine)     │
│  └── OutputJob Processor (Gerber X2, NC Drill, Pick & Place)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **DXP Automation Scripting**: Author clean, functional DXP scripts (DelphiScript or Python) utilizing `PCBServer` and `SchServer` interfaces to automate netlist validation, component coordinate extraction, and polygon repouring.
2. **High-Speed Signal Integrity & Routing Diagnostics**: Remediate transmission line impedance mismatches, calculate single-ended ($50\Omega$) and differential ($90\Omega/100\Omega$) trace geometry, and tune serpentine accordion length matching.
3. **DRC Error Triage**: Diagnose and resolve clearance violations, unrouted nets, stub traces, hole-to-hole clearance breaks, and solder mask sliver errors.
4. **OutJob & CAM Production Delivery**: Configure standardized OutputJob configurations for fabrication and assembly release packages.

---

## Production DXP DelphiScript Automation: Automated DRC & Unrouted Net Auditor

Save this script as `AuditPCBRules.pas` inside an Altium Designer Script Project (`.PrjScr`):

```pascal
{==============================================================================}
{ Altium DXP Script: Automated DRC Runner & Unrouted Net Reporter             }
{ Iterates through active PCB document and exports DRC violation count.        }
{==============================================================================}
Procedure AuditActivePCB;
Var
    Board       : IPCB_Board;
    DRCManager  : IPCB_DRCManager;
    Violations  : Integer;
    Unrouted    : Integer;
    Doc         : IDocument;
Begin
    // 1. Get Current Active PCB Document
    Board := PCBServer.GetCurrentPCBBoard;
    If Board = Nil Then
    Begin
        ShowError('Error: No active PCB document found in workspace.');
        Exit;
    End;

    // 2. Force Repour of All Polygons
    StatusBar.SetState_StatusText('Repouring All Polygons...');
    Board.PolygonManager.RepourAllPolygons;

    // 3. Count Unrouted Connections
    Unrouted := Board.UnroutedNetCount;

    // 4. Run Design Rule Check
    StatusBar.SetState_StatusText('Executing Online Design Rule Check...');
    DRCManager := Board.DRCManager;
    Violations := DRCManager.RunDesignRuleCheck(eDRC_Full);

    // 5. Output Summary Message
    If (Violations = 0) And (Unrouted = 0) Then
    Begin
        ShowInfo('SUCCESS: PCB is 100% Routed with 0 DRC Violations!' + #13#10 +
                 'Ready for OutJob Fabrication Generation.');
    End
    Else
    Begin
        ShowWarning('AUDIT FAILED:' + #13#10 +
                    '• Unrouted Nets: ' + IntToStr(Unrouted) + #13#10 +
                    '• DRC Violations: ' + IntToStr(Violations) + #13#10 +
                    'Please review the Messages and PCB Rules & Violations panels.');
    End;
End;
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **False Clearance Violations on Polygon Pour Boundaries** | Polygons were modified or tracks moved without triggering a polygon repour, leaving stale copper geometry in DRC memory. | 1. Navigate to *Tools $\rightarrow$ Polygon Pours $\rightarrow$ Repour All*.<br>2. Check **Polygon Pour Priority Order** to ensure small/nested pours take priority over large GND planes.<br>3. Verify clearance rule scope (`InPolygon`). |
| **Differential Pair Tuning Accords Break Impedance** | Sharp serpentine bends violating $3W$ rule or gap spacing narrower than differential pair design rule. | 1. Open *Design $\rightarrow$ Rules $\rightarrow$ High Speed $\rightarrow$ Matched Net Lengths*.<br>2. Set tuning amplitude to $\ge 3\times$ trace width and rounded style (*Mitered with 45° or Curved*).<br>3. Inspect return path over continuous ground reference plane. |
| **Footprint Link Lost After Altium 365 Library Migration** | Footprint reference paths broken or GUID mappings changed during cloud library synchronization. | 1. In Schematic Editor, open *Tools $\rightarrow$ Footprint Manager*.<br>2. Select all components $\rightarrow$ Click **Validate**.<br>3. Use *Update from Server Library* or remap footprint names in batch. |
| **3D STEP Export Shows Collisions with Enclosure** | Component 3D models were placed with incorrect Z-axis standoff height or upside-down rotation. | 1. Switch to 3D View mode (Press `3`).<br>2. Select component $\rightarrow$ Open Properties panel $\rightarrow$ Adjust **Standoff Height** or rotation ($X/Y/Z$).<br>3. Run 3D Clearance DRC. |

---

## Command Line Syntax & OutJob CAM Execution

```bash
# Windows CLI: Launch Altium Designer with Clean Workspace
"C:\Program Files\Altium\AD24\X2.exe"

# Execute OutputJob Generation via Altium Command Engine
"C:\Program Files\Altium\AD24\System\Altium.Automation.exe" -runoutjob "C:\Hardware\Motherboard.OutJob" -output "C:\CAM_Release"
```

### Essential File Locations
- **Windows User Preferences**: `%APPDATA%\Altium\Altium Designer {GUID}`
- **System Templates**: `%PROGRAMDATA%\Altium\Altium Designer {GUID}\Templates`
- **User Scripts Directory**: `%USERPROFILE%\Documents\Altium\Scripts`

---

## Agent Operational Directive
> **MANDATORY**: Prior to generating fabrication CAM outputs (Gerbers/Drill), execute a full Polygon Repour and run a batch DRC check. Verify that all differential pairs have continuous reference planes without split-plane crossings.
