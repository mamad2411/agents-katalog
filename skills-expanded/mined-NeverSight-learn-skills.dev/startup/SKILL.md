---
name: startup
description: >
  Audit and clean up Windows startup programs to speed up boot time and reduce idle RAM.
  Use when the user wants faster boot, fewer things loading at startup, or wants to know
  what runs automatically. Trigger for: "too many startup programs", "slow boot",
  "too many things open at startup", "disable startup apps", "what runs at boot",
  "my PC takes forever to start".
---

# /optimize:startup — Startup Program Audit

Inventories everything that loads when Windows starts and helps the user decide what
to keep, what to remove, and what to postpone until actually needed.

---

## Step 1 — Inventory everything

Run this PowerShell as Administrator to get the full picture:

```powershell
$items = @()

# HKCU Run
$hkcu = Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -EA SilentlyContinue
$hkcu.PSObject.Properties | Where-Object { $_.Name -notlike "PS*" } | ForEach-Object {
    $items += [PSCustomObject]@{ Source="HKCU"; Name=$_.Name; Value=$_.Value }
}
# HKLM Run
$hklm = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -EA SilentlyContinue
$hklm.PSObject.Properties | Where-Object { $_.Name -notlike "PS*" } | ForEach-Object {
    $items += [PSCustomObject]@{ Source="HKLM"; Name=$_.Name; Value=$_.Value }
}
# HKLM32 Run
$hklm32 = Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run" -EA SilentlyContinue
$hklm32.PSObject.Properties | Where-Object { $_.Name -notlike "PS*" } | ForEach-Object {
    $items += [PSCustomObject]@{ Source="HKLM32"; Name=$_.Name; Value=$_.Value }
}
# Startup folders
foreach ($folder in @([Environment]::GetFolderPath("Startup"), [Environment]::GetFolderPath("CommonStartup"))) {
    Get-ChildItem $folder -EA SilentlyContinue | ForEach-Object {
        $items += [PSCustomObject]@{ Source="Folder"; Name=$_.Name; Value=$_.FullName }
    }
}
# Scheduled tasks at logon
Get-ScheduledTask -EA SilentlyContinue | Where-Object {
    $_.State -ne "Disabled" -and ($_.Triggers | Where-Object { $_ -and $_.CimClass.CimClassName -match "Logon|Boot" })
} | ForEach-Object {
    $items += [PSCustomObject]@{ Source="Task"; Name=$_.TaskName; Value=$_.TaskPath }
}

$items | Format-Table -AutoSize
```

---

## Step 2 — Present the inventory

Show the user the full list grouped by source (HKCU, HKLM, folders, tasks).
For each item, briefly describe what it is if it's not obvious from the name.

Common identifications:
- `SecurityHealth` / `SecurityHealthSystray` → Windows Defender tray — keep
- `Focusrite Notifier` → audio interface driver notification — keep if has Focusrite
- `Plex Media Server` → Plex server — keep if running as home server
- `Parsec.App.0` → remote gaming client — keep if used for remote access
- `Discord` → chat app — can open manually
- `Spotify` → music app — can open manually
- `EpicGamesLauncher` → game launcher — can open manually
- `EADesktop` → EA game launcher — can open manually
- `Steam` → game launcher — can open manually (or keep if they always use it)
- `AdobeAAMUpdater` / `AdobeUpdater` → Adobe auto-updater — managed by CC app
- `GoogleDriveFS` → Google Drive sync — depends if constant sync is needed
- `OneDrive` → Microsoft OneDrive — depends on use
- `DSALaunchAgent` / `DSATray` → Intel Driver Support Assistant — not needed at boot
- `GoodSync` / `gsync` → backup sync tool — can run on schedule
- `TeamViewer` → remote support — service runs when app opens
- `com.squirrel.slack.slack` → Slack — can open manually
- `Notion` → note-taking — can open manually
- Any app name with "Update" or "Updater" → rarely needs to run at startup

---

## Step 3 — Ask what to keep

Tell the user:

> "Here's everything that loads when Windows starts. Tell me what you want to keep
> and I'll remove the rest. At minimum, I'd suggest keeping:
> - SecurityHealth (Windows Defender)
> - Any audio interface software (Focusrite, Scarlett, etc.)
> - Anything you need available the moment you sit down (Plex, Parsec, etc.)"

Wait for their answer.

---

## Step 4 — Back up and execute

Before removing anything, export the current state:
```powershell
reg export "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" startup_backup_hkcu.reg /y
reg export "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" startup_backup_hklm.reg /y
```

For each item to remove:

**Registry (HKCU/HKLM):**
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "AppName"
```

**Startup folder shortcuts:**
```powershell
Remove-Item "C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\App.lnk" -Force
```

**Scheduled tasks:**
```powershell
Disable-ScheduledTask -TaskName "TaskName"
```

Kill the process for each item removed (so the effect is immediate):
```powershell
Stop-Process -Name "ProcessName" -Force -ErrorAction SilentlyContinue
```

---

## Step 5 — Report

Show:
- Items before → after
- RAM freed immediately (from killed processes)
- Note: full boot speed improvement shows on next cold start

To restore any item later:
```powershell
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" `
    -Name "AppName" -Value '"C:\path\to\app.exe"'
```
