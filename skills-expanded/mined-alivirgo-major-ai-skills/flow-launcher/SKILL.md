---
name: flow-launcher
description: "Build Flow Launcher plugins with C# or Python JSON-RPC, configure plugin manifests, and integrate Everything search."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["flow-launcher", "python-jsonrpc-plugin", "csharp-plugins", "everything-search", "hotkey-launcher", "windows-11", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Flow Launcher Extensible Productivity AI Skill Guide (Claude)

## Overview & Engine Architecture
Flow Launcher is an open-source, extensible productivity launcher and desktop search application for Windows built on **C# / .NET 8 and WPF**. Flow Launcher integrates natively with **Voidtools Everything**, Windows programs, bookmarks, web search queries, and third-party extensions. The engine executes external plugins via a bi-directional **JSON-RPC standard I/O (stdin/stdout) protocol** across Python, Node.js, and executable binaries, or natively in-process via **C# .NET assemblies (`Flow.Launcher.Plugin.dll`)**. Claude operates as a Principal Windows Productivity Architect and Extensibility Developer, specializing in **Python JSON-RPC plugin development**, **C# plugin authoring**, **JSON-RPC query routing**, and **hotkey conflict remediation**.

### Flow Launcher System Architecture & JSON-RPC Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Flow Launcher Architecture                  │
│                                                             │
│  UI Presentation & Search Bar Layer                         │
│  ├── WPF Search Canvas (Themes, Acrylic Blur, Animations)   │
│  ├── Global Hotkey Engine (Default: `Alt + Space`)          │
│  └── Result List View (Icons, Subtitles, Action Menus)      │
│                                                             │
│  Plugin Host & Query Dispatcher Core                        │
│  ├── Action Keyword Router (e.g. `g` Google, `w` Wikipedia) │
│  ├── Native C# In-Process Host (`IPlugin`, `IContextMenu`)  │
│  └── Out-of-Process JSON-RPC Engine (Python / Node / Exec)  │
│                                                             │
│  Data & Indexing Integration Subsystem                      │
│  ├── Everything Search IPC Bridge (`Everything64.dll`)      │
│  ├── Windows Shell Programs & Control Panel Indexer         │
│  └── Settings Store (`%APPDATA%\FlowLauncher\Settings\`)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Python JSON-RPC Plugin Development**: Author production-grade Flow Launcher Python plugins communicating over standard I/O, parsing the incoming JSON payload (`query` method), and emitting formatted result arrays.
2. **C# .NET Plugin Development**: Build compiled `.dll` plugins implementing `IPlugin`, `IContextMenu`, and `ISettingProvider` for maximum execution speed.
3. **Plugin Manifest (`plugin.json`) Engineering**: Configure action keywords, execution file paths, dependencies, and metadata descriptors.
4. **Hotkey Conflict & Everything Integration Triage**: Resolve hotkey collisions (*PowerToys Run vs Flow Launcher on `Alt + Space`*) and repair IPC connectivity to the Everything search daemon.

---

## Production Python Code: Complete Flow Launcher Python Plugin (`main.py` + `plugin.json`)

### 1. `plugin.json` (Plugin Metadata Manifest)
Save in `%APPDATA%\FlowLauncher\Plugins\SystemDiagnostics\plugin.json`:

```json
{
  "ID": "6A9E4D2B-8C1F-4B5A-9E3D-7F2A1C4E8B90",
  "ActionKeyword": "sys",
  "Name": "System Diagnostics",
  "Description": "Displays live CPU, RAM, and Disk telemetry directly in Flow Launcher.",
  "Author": "AI Systems Engineering Team",
  "Version": "1.0.0",
  "Language": "python",
  "Website": "https://github.com/Flow-Launcher/Flow.Launcher",
  "ExecuteFileName": "main.py",
  "IcoPath": "icon.png"
}
```

### 2. `main.py` (JSON-RPC Protocol Implementation)
Save in `%APPDATA%\FlowLauncher\Plugins\SystemDiagnostics\main.py` (requires `pip install psutil`):

```python
"""
Flow Launcher Python Plugin: System Diagnostics
Implements standard Flow Launcher JSON-RPC stdin/stdout protocol to stream system metrics.
"""

import sys
import json
import psutil

class SystemDiagnosticsPlugin:
    def __init__(self):
        # Read incoming JSON-RPC request from Flow Launcher via stdin
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            return

        try:
            request = json.loads(raw_input)
            method = request.get("method")
            parameters = request.get("parameters", [])

            if method == "query":
                query_text = parameters[0] if parameters else ""
                self.query(query_text)
            elif method == "open_task_manager":
                self.open_task_manager()

        except Exception as e:
            self.send_error(str(e))

    def query(self, query_text: str):
        # Query Live System Metrics via psutil
        cpu_percent = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\")

        results = [
            {
                "Title": f"CPU Utilization: {cpu_percent}%",
                "SubTitle": f"{psutil.cpu_count(logical=True)} Logical Cores | Click to open Task Manager",
                "IcoPath": "icon.png",
                "JsonRPCAction": {
                    "method": "open_task_manager",
                    "parameters": [],
                    "dontHideAfterAction": False
                }
            },
            {
                "Title": f"RAM Load: {mem.percent}% ({mem.used / (1024**3):.1f} GB / {mem.total / (1024**3):.1f} GB)",
                "SubTitle": f"Available Memory: {mem.available / (1024**3):.1f} GB",
                "IcoPath": "icon.png"
            },
            {
                "Title": f"C: Drive Space: {disk.percent}% Used ({disk.free / (1024**3):.1f} GB Free)",
                "SubTitle": f"Total Capacity: {disk.total / (1024**3):.1f} GB",
                "IcoPath": "icon.png"
            }
        ]

        # Send JSON-RPC response back to Flow Launcher via stdout
        output = {"result": results}
        print(json.dumps(output))

    def open_task_manager(self):
        import subprocess
        subprocess.Popen("taskmgr.exe")

    def send_error(self, err_msg: str):
        output = {
            "result": [
                {
                    "Title": "Plugin Error Occurred",
                    "SubTitle": err_msg,
                    "IcoPath": "icon.png"
                }
            ]
        }
        print(json.dumps(output))

if __name__ == "__main__":
    SystemDiagnosticsPlugin()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Python Plugins Fail to Execute Silently** | Flow Launcher cannot resolve Python path or `python.exe` is not in system environment. | In Flow Launcher Settings $\rightarrow$ **Plugin Store** $\rightarrow$ **Python Settings**, specify absolute path to `python.exe`. |
| **Hotkey `Alt + Space` Does Not Trigger Launcher** | Conflict with Windows PowerToys Run, Discord overlay, or GeForce Experience. | In Flow Launcher Settings $\rightarrow$ **General**, assign a new hotkey combination (e.g. `Ctrl + Space` or `Alt + D`). |
| **Everything Search Returns "Everything is not running"** | `Everything.exe` background process or service is stopped. | Start Everything service: `Everything.exe -svc-start` and verify Everything plugin is enabled in Flow Settings. |
| **Flow Launcher Crashes on Startup** | Corrupted `Settings.json` file following an ungraceful shutdown. | Restore backup settings or delete corrupted `%APPDATA%\FlowLauncher\Settings\Settings.json`. |

---

## Command Line Syntax & Flow Launcher Ingress

```bash
# 1. Launch Flow Launcher GUI
"%LOCALAPPDATA%\FlowLauncher\Flow.Launcher.exe"

# 2. Trigger Search Query via Command Line
"%LOCALAPPDATA%\FlowLauncher\Flow.Launcher.exe" --query "sys"

# 3. Query Flow Launcher Process via PowerShell
Get-Process -Name "Flow.Launcher"
```

### Essential File Locations
- **Installed Plugins**: `%APPDATA%\FlowLauncher\Plugins\`
- **Application Settings**: `%APPDATA%\FlowLauncher\Settings\Settings.json`
- **Plugin Data Store**: `%APPDATA%\FlowLauncher\Settings\Plugins\`

---

## Agent Operational Directive
> **MANDATORY**: When developing Flow Launcher Python plugins, always emit responses as valid JSON strings to stdout (`json.dumps({"result": [...]})`) without any extraneous debug print statements that would corrupt the JSON-RPC pipe.
