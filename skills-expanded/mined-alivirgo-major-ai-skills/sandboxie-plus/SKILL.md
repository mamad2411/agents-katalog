---
name: sandboxie-plus
description: "Configure Sandboxie-Plus isolation settings and disposable test environments, and troubleshoot sandbox execution boundaries."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["sandboxie-plus", "sbiedrv-sys", "application-isolation", "sandboxie-ini", "start-exe-cli", "malware-containment", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Sandboxie-Plus Application Isolation AI Skill Guide (Claude)

## Overview & Engine Architecture
Sandboxie-Plus is an open-source Windows application containment and virtualization engine. Operating via a low-level kernel filesystem and registry filter driver (**`SbieDrv.sys`**), the background Windows service (**`SbieSrv.exe`**), and a Qt6 GUI frontend (**`SandMan.exe`**), Sandboxie intercepts all write operations. All file modifications and registry keys are redirected to isolated storage silos (**`C:\Sandbox\%USER%\%BOX%\`** and **`HKEY_USERS\Sandbox_%USER%_%BOX%`**). Sandboxie supports **Standard Isolation**, **Enhanced Isolation (AppContainer / Token Filtering)**, and **Security-Hardened Compartment Boxes**. Claude operates as a Principal Windows Security Architect and Systems Containment Specialist, specializing in **declarative `Sandboxie.ini` engineering**, **`Start.exe` CLI automation**, **kernel driver troubleshooting**, and **ephemeral testing workflows**.

### Sandboxie-Plus Kernel Virtualization Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Sandboxie-Plus System Stack                 │
│                                                             │
│  User Interface & Management Tier                           │
│  ├── `SandMan.exe` (Qt6 Modern UI Management Console)       │
│  ├── `Start.exe` Command Line Launcher (`/box:<BoxName>`)   │
│  └── `Sandboxie.ini` Declarative Configuration Engine       │
│                                                             │
│  Service & User-Mode Isolation Core                         │
│  ├── `SbieSrv.exe` Windows Service (SYSTEM Token Broker)    │
│  ├── `SbieDll.dll` User-Mode API Interceptor & Hook Engine  │
│  └── AppContainer Token Restrictions & RPC Filtering        │
│                                                             │
│  Kernel Driver & Storage Virtualization                     │
│  ├── `SbieDrv.sys` Kernel Filter Driver (Write Redirection) │
│  ├── File Silo: `C:\Sandbox\%USER%\<BoxName>\drive\C\...`   │
│  └── Registry Silo: `\Registry\User\Sandbox_<User>_<Box>`   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Declarative `Sandboxie.ini` Architecture**: Author customized sandbox policies defining read/write path exceptions (`OpenFilePath`), write-protected zones (`WriteFilePath`), blocked network access (`BlockInternetAccess=y`), and auto-deletion rules (`AutoDelete=y`).
2. **Automated Headless Sandboxed Execution (`Start.exe`)**: Construct automation scripts launching untrusted binaries, web browsers, or installer packages inside isolated sandbox instances via CLI.
3. **Kernel Driver & HVCI Compatibility Triage**: Remediate `SBIE2204 Cannot start driver` errors caused by Windows Hypervisor-Protected Code Integrity (HVCI) or anti-cheat driver conflicts.
4. **Ephemeral Sandbox Lifecycle Automation**: Script automated routines provisioning a fresh sandbox, running an untrusted payload, harvesting generated log files, and wiping sandbox storage.

---

## Production Python Automation: Automated Ephemeral Sandbox Runner & Collector

Save this script as `run_sandboxed_payload.py`:

```python
"""
Sandboxie-Plus Ephemeral Execution & Artifact Collector
Provisions an isolated disposable sandbox, launches an application, and purges sandbox on exit.
"""

import sys
import os
import subprocess
import time
import shutil

SBIE_START_EXE = r"C:\Program Files\Sandboxie-Plus\Start.exe"
BOX_NAME = "EphemeralTestBox"

def run_isolated_payload(target_executable: str, collect_dir: str = None):
    print(f"--- [INITIALIZING SANDBOXIE-PLUS CONTAINMENT: {BOX_NAME}] ---")

    if not os.path.exists(SBIE_START_EXE):
        print(f"🚨 Error: Sandboxie launcher not found at: {SBIE_START_EXE}")
        return

    # 1. Terminate any previous processes in box
    print("Flushing any existing processes in target sandbox...")
    subprocess.run([SBIE_START_EXE, f"/box:{BOX_NAME}", "/terminate"], capture_output=True)

    # 2. Launch Untrusted Executable inside Sandbox
    print(f"Launching untrusted executable inside [{BOX_NAME}]: {target_executable}...")
    proc = subprocess.Popen([SBIE_START_EXE, f"/box:{BOX_NAME}", target_executable])

    print("• Process launched inside kernel sandbox. Waiting for completion...")
    proc.wait()
    print("✅ Sandboxed process finished execution.")

    # 3. Harvest Artifacts from Sandbox File Silo if requested
    user_name = os.environ.get("USERNAME", "User")
    sandbox_root = rf"C:\Sandbox\{user_name}\{BOX_NAME}"

    if collect_dir and os.path.exists(sandbox_root):
        print(f"Collecting modified sandbox artifacts to: {collect_dir}...")
        os.makedirs(collect_dir, exist_ok=True)
        # Copy created/modified files
        for root, dirs, files in os.walk(sandbox_root):
            for f in files:
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, sandbox_root)
                dest_path = os.path.join(collect_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
        print("✅ Artifacts successfully collected.")

    # 4. Wipe Sandbox Storage
    print("Purging ephemeral sandbox storage...")
    subprocess.run([SBIE_START_EXE, f"/box:{BOX_NAME}", "delete_sandbox"], capture_output=True)
    print("✅ Sandbox storage wiped cleanly.")

if __name__ == "__main__":
    exe = sys.argv[1] if len(sys.argv) > 1 else "notepad.exe"
    out = sys.argv[2] if len(sys.argv) > 2 else "C:\\Temp\\SandboxOutput"
    run_isolated_payload(exe, out)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`SBIE2204 Cannot start driver (SbieDrv)`** | Windows Core Isolation (HVCI Memory Integrity) blocking driver or driver service stopped. | 1. In elevated terminal, run: `sc start SbieDrv`.<br>2. Ensure Sandboxie-Plus is updated to latest release supporting current Windows 11 kernel build. |
| **Sandboxed Application Cannot Access Internet** | Sandbox policy includes `BlockInternetAccess=y` or `RestrictInternet=y`. | In `Sandboxie.ini` under `[<BoxName>]`, set `BlockInternetAccess=n` or configure `AllowNetworkAccess=y`. |
| **Sandbox Fails to Delete / File Locked Error** | Orphaned background helper process still holding file handles inside sandbox. | In terminal, force terminate all box processes:<br>`"C:\Program Files\Sandboxie-Plus\Start.exe" /box:<BoxName> /terminate` $\rightarrow$ Retry delete. |
| **Clipboard Copy/Paste Fails from Sandbox** | OpenClipboard restrictions active in security-hardened compartment box. | In `Sandboxie.ini` under target box, add: `OpenClipboard=y`. |

---

## Command Line Syntax & `Start.exe` Recipes

```bash
# 1. Launch Browser inside Dedicated Sandbox
"C:\Program Files\Sandboxie-Plus\Start.exe" /box:DefaultBox "C:\Program Files\Google\Chrome\Application\chrome.exe"

# 2. Terminate All Active Processes in a Sandbox
"C:\Program Files\Sandboxie-Plus\Start.exe" /box:DefaultBox /terminate

# 3. Reload Sandboxie.ini Configuration Changes
"C:\Program Files\Sandboxie-Plus\SbieIni.exe" /reload
```

### Essential File Locations
- **Configuration**: `C:\Windows\Sandboxie.ini` or `C:\Program Files\Sandboxie-Plus\Sandboxie.ini`
- **Sandbox Root Storage**: `C:\Sandbox\%USER%\<BoxName>\`
- **Driver**: `C:\Windows\System32\drivers\SbieDrv.sys`

---

## Agent Operational Directive
> **MANDATORY**: When isolating untrusted or potentially malicious software with Sandboxie-Plus, always configure `BlockInternetAccess=y` and `AutoDelete=y` in `Sandboxie.ini` to prevent data exfiltration and ensure automatic artifact sanitization upon process exit.
