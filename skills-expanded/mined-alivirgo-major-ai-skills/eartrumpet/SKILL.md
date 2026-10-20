---
name: eartrumpet
description: "Inspect and route per-application audio with EarTrumpet, WASAPI, and pycaw; troubleshoot audio sessions and output devices."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["eartrumpet", "wasapi", "windows-core-audio", "pycaw-python", "audio-endpoint-routing", "windows-11", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# EarTrumpet Windows Audio Engine AI Skill Guide (Claude)

## Overview & Engine Architecture
EarTrumpet is an open-source Windows audio management application that replaces the legacy Windows volume mixer with modern, per-application audio session routing. Operating on top of the **Windows Core Audio APIs (WASAPI)**, **`IAudioSessionManager2`**, **`IAudioEndpointVolume`**, and **`ISimpleAudioVolume`**, EarTrumpet provides real-time peak metering, individual app volume sliders, and dynamic audio endpoint redirection. Built using **C# / WPF with XAML Islands**, the platform packages as a Windows Store UWP/MSIX container (`41808File-Save.EarTrumpet`). Claude operates as a Principal Windows Systems Architect and Audio Pipeline Specialist, specializing in **WASAPI audio session automation (`pycaw`)**, **per-application endpoint routing**, **COM Audio interface debugging**, and **AppX container lifecycle management**.

### EarTrumpet System Architecture & WASAPI Audio Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 EarTrumpet & WASAPI Stack                   │
│                                                             │
│  UI Presentation & XAML Islands Layer                       │
│  ├── WinUI / XAML Islands Flyout (Windows 11 Acrylic Blur)  │
│  ├── System Tray Interop (`Shell_NotifyIcon`)               │
│  └── Hotkey Ingress & Multi-Channel Visual Peak Meters      │
│                                                             │
│  Windows Core Audio (WASAPI) COM Subsystem                  │
│  ├── `MMDeviceEnumerator` (Audio Render / Capture Endpoints)│
│  ├── `IAudioSessionManager2` (Session Enumeration & Events) │
│  └── `ISimpleAudioVolume` (Per-Process Volume & Mute State) │
│                                                             │
│  Audio Routing & Interop Policy Core                        │
│  ├── `IAudioPolicyConfigFactory` (Dynamic App Redirection)  │
│  └── Shared vs Exclusive Mode Stream Management             │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **WASAPI Audio Session Scripting (`pycaw`)**: Author Python scripts communicating directly with Windows Core Audio interfaces to list all active process audio sessions, query peak volume, and adjust per-application levels.
2. **Per-App Endpoint Routing Triage**: Identify and resolve audio routing conflicts where specific apps refuse to switch output devices due to legacy DirectSound or WASAPI Exclusive Mode locks.
3. **AppX Package Diagnostics & Lifecycle Management**: Script PowerShell commands to install, reset, and re-register EarTrumpet AppX packages across user profiles.
4. **Volume Flyout Stalling & Crash Remediation**: Diagnose XAML Island initialization exceptions on Windows 11 updates and restore system tray icon responsiveness.

---

## Production Python Automation: WASAPI Per-App Volume & Session Controller (`pycaw`)

Save this script as `manage_audio_sessions.py` (requires `pip install pycaw comtypes psutil`):

```python
"""
Windows WASAPI Audio Session Manager (pycaw)
Enumerates active per-process audio sessions, displays volume levels, and adjusts app volumes.
"""

import sys
import psutil
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def audit_audio_sessions(target_app_name: str = None, target_volume: float = None):
    print("--- [ENUMERATING WINDOWS CORE AUDIO (WASAPI) SESSIONS] ---")
    
    # 1. Query All Active Audio Sessions via WASAPI
    sessions = AudioUtilities.GetAllSessions()
    print(f"Discovered {len(sessions)} active audio session(s):\n")

    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        process = session.Process

        if process:
            proc_name = process.name()
            proc_pid = process.pid
            current_vol = volume.GetMasterVolume()
            is_muted = volume.GetMute()

            print(f"• Process: {proc_name:<24} | PID: {proc_pid:>6} | Vol: {current_vol*100:>5.1f}% | Muted: {is_muted}")

            # 2. Adjust Target Application Volume if requested
            if target_app_name and target_app_name.lower() in proc_name.lower():
                if target_volume is not None:
                    clamped_vol = max(0.0, min(1.0, target_volume))
                    volume.SetMasterVolume(clamped_vol, None)
                    print(f"  ✅ Updated '{proc_name}' Volume -> {clamped_vol*100:.0f}%")
        else:
            print("• System Sounds / Unnamed Audio Stream")

if __name__ == "__main__":
    app_filter = sys.argv[1] if len(sys.argv) > 1 else None
    vol_level = float(sys.argv[2]) / 100.0 if len(sys.argv) > 2 else None

    # Example: python manage_audio_sessions.py spotify 75
    audit_audio_sessions(app_filter, vol_level)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Application Missing from EarTrumpet Flyout** | The application is currently idle and has not initialized an active WASAPI audio render stream. | Play audio in the application (e.g. start YouTube video in browser) to register the session with `IAudioSessionEnumerator`. |
| **EarTrumpet Crashes on Launch (Windows 11)** | XAML Islands initialization fault or corrupted local UWP application state. | Run PowerShell package reset:<br>`Get-AppxPackage *EarTrumpet* | Reset-AppxPackage`. |
| **Audio Device Switching Fails on Specific Game/DAW** | Application opened the audio endpoint in **WASAPI Exclusive Mode**, locking hardware access. | In Windows *Sound Settings $\rightarrow$ Device Properties $\rightarrow$ Advanced*, uncheck **Allow applications to take exclusive control of this device**. |
| **System Tray Icon Disappears After Explorer Restart** | `Shell_NotifyIcon` registration not re-hooked following `explorer.exe` crash. | In Task Manager, restart `EarTrumpet.exe` or relaunch via `Start-Process shell:AppsFolder\41808File-Save.EarTrumpet_10tokenms02j!App`. |

---

## Command Line Syntax & AppX PowerShell Management

```powershell
# 1. Install EarTrumpet via Windows Package Manager (winget)
winget install --id File-Save.EarTrumpet -e --source winget

# 2. Launch EarTrumpet UWP Container via Shell URI
Start-Process "shell:AppsFolder\41808File-Save.EarTrumpet_10tokenms02j!App"

# 3. Terminate and Restart EarTrumpet Background Process
Stop-Process -Name "EarTrumpet" -Force -ErrorAction SilentlyContinue
Start-Process "shell:AppsFolder\41808File-Save.EarTrumpet_10tokenms02j!App"
```

### Essential File Locations
- **UWP App Data**: `%LOCALAPPDATA%\Packages\41808File-Save.EarTrumpet_10tokenms02j\`
- **Settings Store**: `%LOCALAPPDATA%\Packages\41808File-Save.EarTrumpet_10tokenms02j\LocalSettings\settings.dat`

---

## Agent Operational Directive
> **MANDATORY**: When troubleshooting applications that do not respond to EarTrumpet device redirection, check whether the target application is operating in WASAPI Exclusive Mode before advising driver reinstallation.
