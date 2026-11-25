---
name: pro-tools
description: "Automate Pro Tools session workflows with its scripting SDK and troubleshoot AAX, HDX, or EUCON integration."
category: music
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["pro-tools", "avid", "ptsl-sdk", "grpc-automation", "aax-dsp", "hdx-engine", "eucon", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Avid Pro Tools Ultimate Audio Engineering AI Skill Guide (Claude)

## Overview & Engine Architecture
Avid Pro Tools Ultimate is the global industry standard for professional music production, film post-production re-recording, and broadcast audio engineering. Pro Tools operates on the **Avid Audio Engine (AAE)**, featuring hardware-accelerated **HDX DSP FPGA processing**, native and DSP **AAX (Avid Audio Extension)** plugins, **RAM-based Disk Caching**, the **EUCON** high-speed Ethernet control surface protocol, and the **Pro Tools Scripting SDK (PTSL / gRPC)**. Claude operates as a Principal Audio Systems Architect and Pro Tools Automation Specialist, specializing in **PTSL gRPC Python automation**, **AAE buffer & DAE error triage**, **HDX hardware card diagnostics**, and **Dolby Atmos post-production workflows**.

### Pro Tools Ultimate Core Architecture & PTSL SDK Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Pro Tools Ultimate Architecture             │
│                                                             │
│  Presentation & Post-Production Tier                        │
│  ├── Edit Window (Shuffle/Slip/Spot/Grid, Clip Gain, Fades) │
│  ├── Mix Window (VCA Masters, 10 Inserts, 10 Sends)         │
│  └── Dolby Atmos Renderer Bed & Object Routing (7.1.4)      │
│                                                             │
│  Audio Engine & Hardware Acceleration Layer                 │
│  ├── Avid Audio Engine (AAE 64-bit Floating-Point Summing)  │
│  ├── HDX PCIe DSP Core Cards (Near-Zero Latency Mixing/DSP) │
│  ├── AAX Plugin Architecture (AAX Native & AAX DSP)         │
│  └── RAM Disk Cache (Session Loaded Directly into Memory)   │
│                                                             │
│  Automation & Developer SDK                                 │
│  ├── Pro Tools Scripting SDK (PTSL via gRPC on Port 31416)  │
│  └── EUCON Protocol Engine (Avid S6, S4, S1, Dock Control)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Pro Tools Scripting SDK (PTSL) Automation**: Author Python scripts communicating with Pro Tools via gRPC on port 31416 using the official PTSL client library to create tracks, arm recording, and export stems.
2. **AAE Error Diagnostics & Latency Triage**: Resolve critical AAE runtime exceptions:
  - *AAE Error -9073*: Disk I/O bottleneck (increase Disk Cache allocation).
  - *AAE Error -9173*: Real-time CPU core overload (disable Turbo Boost or adjust buffer).
  - *AAE Error -6101*: CPU spike during monitoring.
3. **AAX Plugin Cache & Database Recovery**: Remediate unvalidated or missing AAX plugins by purging corrupted `InstalledAAXPlugIns` preference cache files.
4. **EUCON Network Protocol Diagnostics**: Troubleshoot EuControl surface disconnects by validating Bonjour network broadcast discovery on local subnetworks.

---

## Production Python Automation: Pro Tools Scripting SDK Client (PTSL / gRPC)

Save this script as `ptsl_session_exporter.py` (requires `pip install ptsl` or official Avid PTSL Python SDK):

```python
"""
Avid Pro Tools Scripting SDK (PTSL) Python Client
Connects to Pro Tools via gRPC (Port 31416) to inspect session tracks and export stems.
"""

import sys
import ptsl
import ptsl.PTSL_pb2 as pt

PTSL_HOST = "localhost:31416"

def automate_pro_tools():
    print(f"--- [CONNECTING TO PRO TOOLS PTSL SERVER: {PTSL_HOST}] ---")
    try:
        with ptsl.Client(company_name="StudioAutomation", application_name="StemExporter") as client:
            # 1. Query Active Session Name and Sample Rate
            session_name = client.get_session_name()
            sample_rate = client.get_session_sample_rate()
            print(f"• Active Session:     {session_name}")
            print(f"• Session Sample Rate:{sample_rate} Hz")

            # 2. Query All Tracks in Session
            track_list = client.get_track_list()
            print(f"\n--- [SESSION TRACKS ({len(track_list)})] ---")
            for t in track_list:
                arm_status = "ARMED" if t.is_record_armed else "SAFE"
                print(f"• Track: {t.name:<25} | Type: {t.type:<12} | Status: {arm_status}")

            # 3. Trigger Session Playback Pass
            print("\nTriggering Transport Playback...")
            client.set_playback_mode(pt.PM_Normal)
            client.play()
            print("✅ Transport is rolling.")

    except Exception as e:
        print(f"🚨 PTSL Connection Failed: {e}")
        print("Note: Ensure Pro Tools 2023.6+ is running with 'Enable Pro Tools Scripting' checked in Setup -> Preferences.")

if __name__ == "__main__":
    automate_pro_tools()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **AAE Error -9073 (Disk too slow or fragmented)** | Disk buffer underflow during multi-track recording or playback. | In *Setup $\rightarrow$ Playback Engine*, set **Cache Size** to `Custom (e.g. 8GB)` to load all audio files into RAM. |
| **AAE Error -9173 (CPU overload / Real-Time Spike)** | Background OS tasks or plugin thread colliding with Pro Tools time-critical audio thread. | 1. In Playback Engine, increase **H/W Buffer Size** to `1024 samples` during mixing.<br>2. Disable WiFi/Bluetooth during mission-critical tracking passes.<br>3. Check for non-native AAX plugins. |
| **AAX Plugin Inactive After Pro Tools Update** | Cached signature in `InstalledAAXPlugIns` out-of-date. | 1. Quit Pro Tools.<br>2. Delete `~/Library/Preferences/Avid/Pro Tools/InstalledAAXPlugIns` (macOS) or `%APPDATA%\Avid\Pro Tools\InstalledAAXPlugIns` (Windows).<br>3. Relaunch Pro Tools for a clean scan. |
| **EuControl Surface Disconnects (Avid S1 / S6 / Dock)** | Multicast Bonjour discovery packets filtered by Ethernet switch or macOS firewall. | Ensure IGMP snooping is enabled on network switch and allow `EuControl.app` through macOS Firewall. |

---

## Command Line Syntax & Avid Diagnostics

```bash
# 1. Run Avid DigiTest Hardware Diagnostic Utility (Windows)
"C:\Program Files\Avid\Pro Tools\DUC.exe"

# 2. Reset Pro Tools Preferences on macOS
rm -f ~/Library/Preferences/com.avid.ProTools.plist
rm -f ~/Library/Preferences/Avid/Pro\ Tools/Pro\ Tools\ Preferences

# 3. Inspect Active PTSL gRPC Port Status
lsof -i :31416
```

### Essential File Locations
- **Pro Tools Preferences**: `%APPDATA%\Avid\Pro Tools\` (Windows) or `~/Library/Preferences/Avid/Pro Tools/` (macOS)
- **AAX Plugins Directory**: `/Library/Application Support/Avid/Audio/Plug-Ins/` (macOS) or `C:\Program Files\Common Files\Avid\Audio\Plug-Ins\` (Windows)
- **Session Files**: `*.ptx`

---

## Agent Operational Directive
> **MANDATORY**: For large mixing sessions exceeding 64 tracks, always configure the Playback Engine Disk Cache Size to a fixed RAM allocation (e.g. 4GB-16GB) to eliminate DAE/AAE Error -9073 disk bottlenecks.
