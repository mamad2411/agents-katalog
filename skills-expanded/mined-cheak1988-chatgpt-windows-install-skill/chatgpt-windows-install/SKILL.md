---
name: chatgpt-windows-install
description: Automatically downloads, installs, and configures the official OpenAI ChatGPT / Codex desktop client on Windows 10/11 using official CDN direct links, bypassing Microsoft Store error codes (0x80070005, 0x80073CF9, 0x80073CF3) and resolving WindowsApps permissions.
---

# ChatGPT & Codex Windows Official Client Installer Skill

When invoked, the AI agent should automatically execute the following procedure in PowerShell on Windows to install and configure the official OpenAI ChatGPT desktop application without relying on the Microsoft Store.

## Official CDN Direct Endpoints
- **x64 (Intel/AMD 64-bit)**: `https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix`
- **ARM64 (Qualcomm Snapdragon / WoA)**: `https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix`

## Installation Workflow

### Step 1: Detect Architecture & Prepare Environment
```powershell
$arch = if ([System.Environment]::Is64BitOperatingSystem -and $env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "x64" }
$downloadUrl = "https://persistent.oaistatic.com/codex-app-prod/ChatGPT-$arch.msix"
$installerPath = "$env:TEMP\ChatGPT-$arch.msix"
```

### Step 2: Download Official MSIX Package
```powershell
Write-Host "Downloading official ChatGPT $arch MSIX from OpenAI CDN..." -ForegroundColor Cyan
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13
Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
```

### Step 3: Install Package
```powershell
Write-Host "Installing ChatGPT via Add-AppxPackage..." -ForegroundColor Cyan
Add-AppxPackage -Path $installerPath
```

### Step 4: Verify Installation
```powershell
$pkg = Get-AppxPackage OpenAI.Codex
if ($pkg) {
    Write-Host "ChatGPT successfully installed! Version: $($pkg.Version)" -ForegroundColor Green
    # Launch application
    Start-Process "shell:AppsFolder\$($pkg.PackageFamilyName)!App"
} else {
    Write-Warning "Package not found in Appx registry. Check error output."
}
```

### Step 5: (Fallback) WindowsApps Permission Bypass
If the user reports double-click not opening or WindowsApps permission errors:
```powershell
$pkg = Get-AppxPackage OpenAI.Codex
if ($pkg) {
    $targetDir = "D:\ChatGPT-app"
    robocopy $pkg.InstallLocation $targetDir /E
    # Create desktop shortcut
    $wshell = New-Object -ComObject WScript.Shell
    $shortcut = $wshell.CreateShortcut("$env:USERPROFILE\Desktop\ChatGPT.lnk")
    $shortcut.TargetPath = "$targetDir\app\ChatGPT.exe"
    $shortcut.WorkingDirectory = "$targetDir\app"
    $shortcut.Save()
    Write-Host "Extracted to $targetDir and created Desktop shortcut." -ForegroundColor Green
}
```
