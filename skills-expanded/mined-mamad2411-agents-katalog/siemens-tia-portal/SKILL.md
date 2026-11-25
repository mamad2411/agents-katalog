---
name: siemens-tia-portal
description: "Develop TIA Portal SCL and Openness automation, and inspect SIMATIC communications in an authorized test environment."
category: plc-industrial
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["siemens-tia-portal", "simatic-s7", "scl-programming", "tia-openness", "snap7", "profinet", "plc-automation", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Siemens TIA Portal Industrial Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
Siemens Totally Integrated Automation (TIA) Portal is the industry standard engineering framework for programming SIMATIC S7-1200, S7-1500, and ET 200SP programmable logic controllers, configuring SINAMICS variable frequency drives, and designing WinCC Unified HMI/SCADA interfaces. TIA Portal supports **Structured Control Language (SCL)**, **Ladder (LAD)**, **Function Block (FBD)**, and **Graph (SFC)**. The platform exposes the **TIA Portal Openness .NET API (`Siemens.Engineering.dll`)** for headless project engineering, communicates with controllers via the **S7comm / S7comm-plus protocol (TCP port 102)**, and provides software-in-the-loop virtual commissioning via **PLCSIM Advanced**. Claude operates as a Principal Industrial Automation Architect and Siemens Controls Systems Specialist, specializing in **SCL state machine development**, **TIA Openness C#/Python CI/CD pipelines**, **Snap7 direct memory access**, and **PROFINET topology diagnostics**.

### TIA Portal System Architecture & S7 Protocol Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 TIA Portal System Architecture              │
│                                                             │
│  Engineering & Openness API Layer                           │
│  ├── TIA Portal V18/V19 IDE (Project View & Portal View)    │
│  ├── TIA Openness API (.NET Framework `Siemens.Engineering`)│
│  └── WinCC Unified (HTML5 Web Engine & JavaScript Runtime)  │
│                                                             │
│  SIMATIC Execution & Hardware Core                          │
│  ├── S7-1200 / S7-1500 Multi-Tasking Execution Engine       │
│  ├── Cyclic OB1 Organization Blocks, Cyclic Interrupt OB30 │
│  └── Data Blocks (Standard DB vs Optimized Block Access)    │
│                                                             │
│  Industrial Communications & S7 Subsystem                   │
│  ├── S7comm / S7comm-plus Industrial Protocol (TCP Port 102)│
│  ├── PROFINET IO Real-Time (RT / IRT Isochronous Real-Time) │
│  └── Direct Socket & Snap7 Industrial Communication Engine  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **S7comm PLC Communication Scripting (`python-snap7`)**: Author Python scripts connecting directly to SIMATIC S7-1200/S7-1500 processors over TCP port 102 to read/write DB blocks, Merker memory (`M`), and digital inputs/outputs (`I`/`Q`).
2. **TIA Portal Openness Automation**: Build automated C# and PowerShell pipelines utilizing `Siemens.Engineering.dll` to import SCL sources, compile hardware/software, and generate `.ap19` project archives.
3. **Structured Control Language (SCL) Development**: Author clean, type-safe SCL function blocks (FB) implementing IEC timers (`TON`), PID controllers (`PID_Compact`), and sequence step controllers.
4. **Optimized DB & PUT/GET Protection Triage**: Resolve communication exceptions caused by CPU Access Protection levels and Optimized Block Access memory layouts.

---

## Production Python Automation: SIMATIC S7 PLC Data Block Reader & Writer (`python-snap7`)

Save this script as `s7_plc_client.py` (requires `pip install python-snap7`):

```python
"""
Siemens SIMATIC S7-1200 / S7-1500 PLC Communication Client (Snap7)
Connects to S7 PLC over TCP port 102, reads Data Block (DB1) variables, and writes setpoints.
"""

import sys
import struct
import snap7
from snap7.util import get_bool, set_bool, get_real, set_real, get_int, set_int

PLC_IP = "192.168.0.1"
RACK = 0
SLOT = 1 # Slot 1 for S7-1200/S7-1500; Slot 2 for S7-300/S7-400

def monitor_s7_plc():
    print(f"--- [CONNECTING TO SIEMENS S7 PLC: {PLC_IP} (Rack: {RACK}, Slot: {SLOT})] ---")
    client = snap7.client.Client()

    try:
        client.connect(PLC_IP, RACK, SLOT)
        if client.get_connected():
            print("✅ Successfully connected to SIMATIC S7 CPU via S7comm (Port 102)!")

            # 1. Read Data Block 1 (DB1) - Read 16 bytes starting at Offset 0
            # DB Layout:
            # Offset 0.0: bMotorRunning (Bool)
            # Offset 2.0: rSpeedActual (Real / Float32)
            # Offset 6.0: iPieceCount (Int16)
            db_number = 1
            data = client.db_read(db_number, 0, 16)

            is_running = get_bool(data, 0, 0)
            actual_speed = get_real(data, 2)
            piece_count = get_int(data, 6)

            print(f"\n--- [DB{db_number} LIVE MONITORING] ---")
            print(f"• Motor Running:   {is_running}")
            print(f"• Actual Speed:    {actual_speed:.2f} RPM")
            print(f"• Piece Count:     {piece_count} units")

            # 2. Write Setpoint Tag: DB1.DBD8 (rTargetSpeed = 1500.0 RPM)
            print("\nWriting Target Speed Setpoint (1500.0 RPM) to DB1.DBD8...")
            write_buffer = bytearray(4)
            set_real(write_buffer, 0, 1500.0)
            client.db_write(db_number, 8, write_buffer)
            print("✅ Setpoint successfully written to PLC memory.")

            client.disconnect()
        else:
            print("🚨 Failed to connect to S7 PLC.")

    except Exception as e:
        print(f"🚨 S7 Communication Error: {e}")
        print("Note for S7-1200/1500: Ensure 'Permit access with PUT/GET' is enabled in CPU Properties -> Protection, and DB is set to Non-Optimized (Standard).")

if __name__ == "__main__":
    monitor_s7_plc()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Snap7 Error: `CLI: function refused by CPU`** | S7-1500 CPU security settings block external PUT/GET communication, or target DB has "Optimized block access" enabled. | 1. In TIA Portal $\rightarrow$ CPU Properties $\rightarrow$ **Protection & Security**, check **Permit access with PUT/GET communication from remote partner**.<br>2. In DB Properties $\rightarrow$ **Attributes**, uncheck **Optimized block access** $\rightarrow$ Re-compile and download DB. |
| **"Cannot establish online connection: PG/PC Interface"** | Engineering station IP address is not in the same subnet as the S7 CPU or incorrect network interface selected. | In *Online $\rightarrow$ Accessible devices*, select your active Ethernet adapter $\rightarrow$ Click **Start search** to identify CPU IP and assign matching static IP to the PC. |
| **SCL Compilation Error: `Ambiguous reference`** | Duplicate Function Block (FB) or Data Type (UDT) definitions exist across Project Library and Global Library. | In Project Tree $\rightarrow$ Libraries tab, resolve duplicate versions using the **Update project components** wizard. |
| **TIA Openness Throws `SecurityException`** | Windows user account is not a member of the local `Siemens TIA Openness` user group. | Open Windows *Computer Management $\rightarrow$ Local Users and Groups $\rightarrow$ Groups*, add current user to **Siemens TIA Openness**, then log out and log back in. |

---

## Command Line Syntax & TIA Openness Recipes

```bash
# 1. Launch TIA Portal V19 via Command Line
"C:\Program Files\Siemens\Automation\Portal V19\Bin\Siemens.Automation.Portal.exe"

# 2. Query S7comm Port 102 Connectivity
python3 -c "import socket; s = socket.socket(); s.connect(('192.168.0.1', 102)); print('S7 Port 102 Open!'); s.close()"
```

### Essential File Locations
- **TIA Openness Core Assembly**: `C:\Program Files\Siemens\Automation\Portal V19\PublicAPI\V19\Siemens.Engineering.dll`
- **TIA Portal Projects**: `*.ap18`, `*.ap19`

---

## Agent Operational Directive
> **MANDATORY**: For direct S7comm communication with S7-1200 and S7-1500 PLCs, always verify that "Permit access with PUT/GET" is enabled in CPU Security settings and target Data Blocks are configured with Standard (Non-Optimized) block access.
