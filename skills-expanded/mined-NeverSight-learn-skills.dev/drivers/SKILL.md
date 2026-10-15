---
name: drivers
description: >
  Audit Windows drivers, hardware health, and BIOS/firmware status. Use when the user
  wants to check if their drivers are up to date, has Device Manager errors, suspects
  hardware issues, or wants to know if their RAM is running at rated speed. Trigger for:
  "check my drivers", "Device Manager errors", "RAM not running at full speed",
  "is my GPU driver outdated", "hardware issues", "yellow triangles in Device Manager",
  "XMP not working", "update drivers".
---

# /optimize:drivers — Hardware & Driver Audit

Checks driver versions, hardware configuration, and device errors. Produces a clear
action list — most items here require manual steps, so the output is a prioritized
report, not an automated fix.

---

## Step 1 — Run the diagnostic

Run `scripts/01_diagnose.ps1` as Administrator.

Focus on: `hardware.json`, `device_errors.json`, `smart_status.json`.

---

## Step 2 — Collect additional driver detail

Run this PowerShell as Administrator for a deeper driver picture:

```powershell
# GPU driver info
$gpu = Get-WmiObject Win32_VideoController | Where-Object { $_.Name -notlike "*Microsoft*" } | Select-Object -First 1
Write-Host "GPU: $($gpu.Name)"
Write-Host "Driver version: $($gpu.DriverVersion)"
$driverDate = [Management.ManagementDateTimeConverter]::ToDateTime($gpu.DriverDate)
Write-Host "Driver date: $($driverDate.ToString('yyyy-MM-dd')) ($([int]([datetime]::Today - $driverDate).TotalDays) days ago)"

# RAM speed vs rated
Get-WmiObject Win32_PhysicalMemory | ForEach-Object {
    Write-Host "RAM: $($_.PartNumber.Trim()) | Rated: $($_.Speed) MHz | Running: $($_.ConfiguredClockSpeed) MHz | XMP: $(if ($_.ConfiguredClockSpeed -ge $_.Speed - 100) {'ACTIVE'} else {'OFF - running below rated speed'})"
}

# BIOS
$bios = Get-WmiObject Win32_BIOS
$biosDate = [Management.ManagementDateTimeConverter]::ToDateTime($bios.ReleaseDate)
Write-Host "BIOS: $($bios.SMBIOSBIOSVersion) — $($biosDate.ToString('yyyy-MM-dd')) ($([int]([datetime]::Today - $biosDate).TotalDays) days ago)"

# Device errors
$errors = Get-PnpDevice | Where-Object { $_.Status -eq "Error" }
Write-Host "`nDevices in error ($($errors.Count)):"
$errors | ForEach-Object { Write-Host "  [ERROR] $($_.Class) — $($_.FriendlyName) — $($_.InstanceId)" }

# Driver dates (flagging old ones)
Write-Host "`nDrivers older than 1 year:"
Get-WmiObject Win32_PnPSignedDriver | Where-Object { $_.DriverDate -and $_.DeviceName } |
    ForEach-Object {
        try {
            $d = [datetime]::ParseExact($_.DriverDate.Substring(0,8), "yyyyMMdd", $null)
            if (([datetime]::Today - $d).TotalDays -gt 365) {
                Write-Host ("  {0,-45} {1}" -f $_.DeviceName, $d.ToString("yyyy-MM-dd"))
            }
        } catch {}
    }

# SMART
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus | Format-Table -AutoSize
```

---

## Step 3 — Produce the report

Present findings clearly, grouped by priority:

### 🔴 Critical
- Any SMART failure predicted → immediate backup + disk replacement
- Device errors that affect core hardware (GPU, audio, network, storage controllers)

### 🟡 Important
- GPU driver > 6 months old → update via AMD Adrenalin or NVIDIA GeForce Experience
- RAM running below rated speed (XMP/DOCP off) → BIOS change, free performance
- Intel/AMD Chipset Device Software missing → download from motherboard manufacturer

### 🟢 Informational
- BIOS age > 12 months → check manufacturer site for stability/security updates
- Non-critical device errors (e.g. Bluetooth adapters not in use)
- Drivers older than 1 year that aren't causing issues

---

## Step 4 — Manual action guide

For every item that needs action, provide exact steps:

**GPU driver update:**
- AMD: Open AMD Software: Adrenalin Edition → Check for Updates
- NVIDIA: Open GeForce Experience → Drivers tab → Check for Updates
- Or download directly from amd.com / nvidia.com

**XMP/DOCP (RAM speed):**
- Press DEL at boot → AI Tweaker (ASUS) or equivalent → XMP / DOCP / EXPO → select profile I → F10 Save → reboot
- Benefit: typically +10-17% memory bandwidth, free

**Intel Chipset Device Software:**
- Go to your motherboard manufacturer's support page → search your model → Drivers → Chipset
- Download and install the INF package → reboot
- This resolves most "PCI Device", "SM Bus Controller", "Serial IO" errors in Device Manager

**BIOS update:**
- Download latest BIOS from manufacturer's support page
- Use EZ Flash (ASUS), Q-Flash (Gigabyte), or M-Flash (MSI) from within BIOS
- No USB drive needed if your BIOS supports internet flash

**For specific device errors:** include the InstanceId from the error list so the user
can paste it into Windows Device Manager or search for the exact driver package.

---

## Step 5 — What can be automated

The only driver-related change that runs automatically (no reboot):

Install available Windows Update drivers:
```powershell
$session = New-Object -ComObject Microsoft.Update.Session
$searcher = $session.CreateUpdateSearcher()
$results = $searcher.Search("IsInstalled=0 and Type='Driver'")
if ($results.Updates.Count -gt 0) {
    $toInstall = New-Object -ComObject Microsoft.Update.UpdateColl
    $results.Updates | ForEach-Object { $toInstall.Add($_) | Out-Null }
    $installer = $session.CreateUpdateInstaller()
    $installer.Updates = $toInstall
    $installResult = $installer.Install()
    Write-Host "Installed $($toInstall.Count) driver(s) from Windows Update"
    Write-Host "Reboot required: $($installResult.RebootRequired)"
}
```

Run this if the user wants to pick up whatever Microsoft has available, but note
that GPU, chipset, and BIOS updates require the manufacturer's tools — Windows Update
typically doesn't carry them.
