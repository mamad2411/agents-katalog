---
name: microsoft-powertoys
description: "Configure PowerToys FancyZones, Run, Keyboard Manager, and Awake; automate settings and troubleshoot Windows utility behavior."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["microsoft-powertoys", "fancyzones", "powertoys-run", "keyboard-manager", "awake-utility", "windows-11", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Microsoft PowerToys System Utilities AI Skill Guide (Claude)

## Overview & Engine Architecture
Microsoft PowerToys is a suite of system utilities developed by Microsoft in C++ and C# / WinUI 3 to tune and streamline the Windows desktop experience. The architecture comprises a central **Runner Daemon (`PowerToys.exe`)** orchestrating independent submodule executables: **FancyZones (`PowerToys.FancyZones.exe`)** for multi-zone window grid snapping, **PowerToys Run (`PowerToys.PowerLauncher.exe`)** for modular desktop search, **Keyboard Manager (`PowerToys.KeyboardManagerEngine.exe`)** for low-level key remapping, **Awake (`PowerToys.Awake.exe`)** for execution state power overrides, and **Text Extractor (`PowerToys.TextExtractor.exe`)** for Windows Media OCR. Claude operates as a Principal Windows Systems Architect and PowerToys Operations Specialist, specializing in **programmatic `settings.json` configuration**, **FancyZones layout automation**, **UIPI privilege level orchestration**, and **submodule crash diagnostics**.

### PowerToys Modular System Architecture & Process Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Microsoft PowerToys Stack                   │
│                                                             │
│  Central Runner & WinUI 3 Dashboard                         │
│  ├── `PowerToys.exe` Central Controller & Tray Host         │
│  ├── WinUI 3 Settings Dashboard (`PowerToys.Settings.exe`)  │
│  └── Central Config Store (`%LOCALAPPDATA%\Microsoft\PT\`) │
│                                                             │
│  Submodule Process Ecosystem                                │
│  ├── FancyZones (`PowerToys.FancyZones.exe` Win32 Hooks)    │
│  ├── PowerLauncher (`PowerToys.PowerLauncher.exe` WPF / C#) │
│  ├── KeyboardManager (`PowerToys.KeyboardManagerEngine.exe`)│
│  ├── Awake (`PowerToys.Awake.exe` `SetThreadExecutionState`)│
│  └── TextExtractor (`Windows.Media.Ocr` Screen Scraper)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Programmatic `settings.json` Manipulation**: Author PowerShell and Python scripts to automate enabling/disabling PowerToys modules, updating hotkey bindings, and deploying standardized enterprise configurations.
2. **FancyZones Multi-Monitor Grid Scripting**: Programmatically generate custom `zones-settings.json` templates defining column widths, row splits, and canvas padding.
3. **UIPI & Administrator Elevation Management**: Resolve window snapping failures on Task Manager, Registry Editor, and elevated terminals by configuring PowerToys to run with highest elevation.
4. **Awake Headless Execution Scripting**: Execute `PowerToys.Awake.exe` via CLI parameters (`--mode=indefinite --display-on=true`) during long-running builds.

---

## Production PowerShell Automation: PowerToys Module Configurator & Daemon Manager

Save this script as `Configure-PowerToys.ps1`:

```powershell
<#
.SYNOPSIS
    Microsoft PowerToys Programmatic Configuration & Daemon Manager
    Enables/disables specific modules and applies custom hotkeys via JSON settings manipulation.
#>

$PowerToysSettingsDir = "$env:LOCALAPPDATA\Microsoft\PowerToys"
$GlobalSettingsFile = "$PowerToysSettingsDir\settings.json"

function Set-PowerToysModuleState {
    param (
        [string]$ModuleName,
        [bool]$Enabled
    )

    if (-not (Test-Path $GlobalSettingsFile)) {
        Write-Error "PowerToys settings file not found at: $GlobalSettingsFile"
        return
    }

    Write-Host "--- [CONFIGURING POWERTOYS MODULE: $ModuleName] ---"

    # 1. Read and Parse Global settings.json
    $jsonContent = Get-Content -Path $GlobalSettingsFile -Raw | ConvertFrom-Json

    # 2. Update Module State in 'enabled' Dictionary
    if ($jsonContent.enabled.PSObject.Properties[$ModuleName]) {
        $jsonContent.enabled.$ModuleName = $Enabled
        Write-Host "• Updated '$ModuleName' Enabled State -> $Enabled"
    } else {
        Write-Warning "Module '$ModuleName' not found in settings.json. Adding property..."
        $jsonContent.enabled | Add-Member -NotePropertyName $ModuleName -NotePropertyValue $Enabled -Force
    }

    # 3. Save Back to Disk
    $jsonContent | ConvertTo-Json -Depth 10 | Set-Content -Path $GlobalSettingsFile -Encoding UTF8
    Write-Host "✅ Settings saved successfully to $GlobalSettingsFile"

    # 4. Gracefully Restart PowerToys Runner to Apply Changes
    Write-Host "Restarting PowerToys background runner..."
    Stop-Process -Name "PowerToys" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Process -FilePath "$env:LOCALAPPDATA\PowerToys\PowerToys.exe" -ErrorAction SilentlyContinue
    Write-Host "✅ PowerToys restarted."
}

# Example Executions:
# Set-PowerToysModuleState -ModuleName "FancyZones" -Enabled $true
# Set-PowerToysModuleState -ModuleName "Awake" -Enabled $true
# Set-PowerToysModuleState -ModuleName "ColorPicker" -Enabled $false
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **FancyZones Fails to Snap Elevated Windows** | PowerToys running with standard user privileges blocked by UIPI (User Interface Privilege Isolation). | In PowerToys Settings $\rightarrow$ General, toggle **Always run as administrator** to On. |
| **PowerToys Run (Alt + Space) Hangs or Crashes** | A corrupted Wox/Community plugin or unindexed path causing an unhandled deadlock in WPF. | In Settings $\rightarrow$ PowerToys Run $\rightarrow$ Plugins, disable suspect third-party plugins or clear `%LOCALAPPDATA%\Microsoft\PowerToys\PowerToys Run\`. |
| **Keyboard Manager Remappings Stop Working** | `PowerToys.KeyboardManagerEngine.exe` low-level hook dropped following Windows sleep/wake cycle. | In Task Manager, terminate `PowerToys.KeyboardManagerEngine.exe`; the runner will automatically respawn it. |
| **Text Extractor Displays "OCR Failed"** | Required Windows OCR Language Pack not installed for current locale. | In Windows Settings $\rightarrow$ Time & language $\rightarrow$ Language $\rightarrow$ Install **OCR Component** for active language. |

---

## Command Line Syntax & Awake Execution

```bash
# 1. Keep System Awake Indefinitely with Screen ON via CLI
"%LOCALAPPDATA%\PowerToys\PowerToys.Awake.exe" --mode=indefinite --display-on=true

# 2. Keep System Awake for 2 Hours (7200 seconds)
"%LOCALAPPDATA%\PowerToys\PowerToys.Awake.exe" --mode=timed --time-limit=7200

# 3. Launch PowerToys Settings Window
"%LOCALAPPDATA%\PowerToys\PowerToys.Settings.exe"
```

### Essential File Locations
- **Settings Store**: `%LOCALAPPDATA%\Microsoft\PowerToys\settings.json`
- **FancyZones Config**: `%LOCALAPPDATA%\Microsoft\PowerToys\FancyZones\zones-settings.json`
- **Binary Directory**: `C:\Program Files\PowerToys\` or `%LOCALAPPDATA%\PowerToys\`

---

## Agent Operational Directive
> **MANDATORY**: When configuring PowerToys to manage windows across administrative tools (e.g. Task Manager, CMD, Services), always enable "Always run as administrator" in General settings to prevent UIPI hook rejection.
