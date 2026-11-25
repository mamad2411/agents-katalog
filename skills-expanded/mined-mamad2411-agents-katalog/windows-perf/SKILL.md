---
name: windows-perf
description: 'Use this skill only when the user explicitly asks to diagnose CPU spikes, fix Windows performance issues, disable telemetry services, or clean up startup items on Windows.'
version: 1.0.0
---

# Windows Performance Tuning

Diagnose CPU spikes and disable unnecessary services and startup items on a Windows developer machine.

## Step 1 — Find the real-time CPU offender

Use WMI perf counters for current CPU %, not cumulative totals:

```powershell
Get-CimInstance Win32_PerfFormattedData_PerfProc_Process |
  Sort-Object PercentProcessorTime -Descending |
  Where-Object { $_.PercentProcessorTime -gt 1 } |
  Select-Object -First 15 Name, PercentProcessorTime, IDProcess |
  Format-Table -AutoSize
```

> `Get-Process | Sort-Object CPU` shows cumulative seconds since start — not current load. Always confirm with WMI perf counters.

## Step 2 — Get process details

```powershell
Get-Process -Id <pid> | Select-Object Name, Id, Path, StartTime, CPU | Format-List
```

## Step 3 — Disable the offending service

```powershell
Stop-Service <ServiceName> -Force
Set-Service <ServiceName> -StartupType Disabled
```

If the process lingers after stopping the service:
```powershell
taskkill /PID <pid> /F
```

## Step 4 — Run the cleanup script

Disables known CPU-hungry and telemetry services and removes unnecessary startup items. Requires admin PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/Disable-UnnecessaryServices.ps1
```

### Services the script disables

| Service | Description |
|---|---|
| `SNAPOService` | Sonitude audio APO — known CPU spinner, not needed with Bluetooth headphones |
| `CxUtilSvc` / `CxMonSvc` | Conexant audio utilities |
| `DiagTrack` | Windows Connected User Experiences & Telemetry |
| `HPAudioAnalytics` | HP audio analytics |
| `HpTouchpointAnalyticsService` | HP Touchpoint analytics |
| `hpLHAgent` / `hpLHWatchdog` | HP Insights telemetry agent |
| `Intel Analytics Service` | Intel telemetry |
| `dptftcs` | Intel Dynamic Tuning Technology telemetry |
| `ipfsvc` | Intel Innovation Platform Framework — spawns `ipf_helper.exe`, known CPU consumer |
| `W3SVC` | IIS web server — unusual to need on a workstation |

### Startup items the script removes

| Entry | Description |
|---|---|
| `MicrosoftEdgeAutoLaunch_*` | Edge silent background launch |
| `GoogleChromeAutoLaunch_*` | Chrome silent background launch |
| `Adobe Acrobat Synchronizer` | Acrobat collaboration sync |
| `StartLoad` | Yealink Wireless Presentation Pod |
| `ClickShare` | Barco ClickShare presentation tool |

## Gotchas

- Audio APO services (`SNAPOService`) are safe to disable even when using Bluetooth — APO only affects the laptop's built-in audio pipeline.
- To re-enable a service: `Set-Service -Name <name> -StartupType Automatic; Start-Service <name>`
- To identify which service is inside a high-CPU `svchost`: `tasklist /svc /fi "pid eq <pid>"`
- Intel Analytics is resolved automatically by DisplayName pattern — no manual action needed if the service is not present on a given machine.
- Both `HKCU` and `HKLM` startup entries are checked. `HKLM` writes are allowed because the script already enforces admin elevation.
