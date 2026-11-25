---
name: disk-cleanup
description: "Analyze disk usage and clean up caches, temp files, app bloat, SDK leftovers, old restore points, and more. Runs tiered safety levels — from safe caches to advanced cleanups. Supports Windows, macOS, and Linux."
user-invocable: true
disable-model-invocation: false
context: fork
agent: general-purpose
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
argument-hint: "[level: safe|standard|deep|full] [target: specific-folder-name] [--dry-run]"
---

# Disk Cleanup Skill

A systematic, tiered approach to freeing disk space. Supports Windows, macOS, and Linux.

## How to Use

Call this skill with optional arguments:
- `/disk-cleanup` — interactive mode, ask the user what level
- `/disk-cleanup safe` — Level 1 only (caches, temps, recycle bin)
- `/disk-cleanup standard` — Levels 1-3 (safe + app caches + store caches)
- `/disk-cleanup deep` — Levels 1-5 (adds OEM bloat, old SDKs, duplicates)
- `/disk-cleanup full` — All 6 levels including system restore points
- `/disk-cleanup target=<name>` — clean a specific item
- `--dry-run` — preview only, no actual deletion (append to any command)

**Workflow**: Detect Platform → Analyze → Report → Confirm → Clean → Verify.

---

## Phase 0: Platform Detection

**Always run this first.** All subsequent commands depend on the detected OS.

```bash
case "$(uname -s)" in
    Linux)   OS="linux" ;;
    Darwin)  OS="macos" ;;
    CYGWIN*|MINGW*|MSYS*) OS="windows" ;;
    *)       OS="unknown" ;;
esac
echo "Detected OS: $OS"
```

Alternatively, on Windows via PowerShell:
```powershell
Write-Host "Detected OS: Windows ($($env:OS))"
```

Key path differences by platform:

| Concept | Windows | macOS | Linux |
|---------|---------|-------|-------|
| User home | `$env:USERPROFILE` | `$HOME` | `$HOME` |
| App data (roaming) | `$env:APPDATA` | `~/Library/Application Support` | `~/.config` |
| App data (local) | `$env:LOCALAPPDATA` | `~/Library/Caches` | `~/.cache` |
| System temp | `$env:WINDIR\Temp` | `/tmp` (also `$TMPDIR`) | `/tmp` |
| User temp | `$env:TEMP` | `$TMPDIR` (or `/tmp`) | `/tmp` |
| Program files | `C:\Program Files` | `/Applications` | `/usr/bin`, `/opt` |
| Package caches | NuGet, WinGet | Homebrew, MacPorts | apt, yum, pacman, snap, flatpak |
| Trash / Recycle Bin | `C:\$Recycle.Bin` | `~/.Trash` | `~/.local/share/Trash` |

---

## Analysis Phase

First, always gather a complete picture before suggesting deletions.

### Step A1: Disk overview

**Windows:**
```powershell
$disk = Get-PSDrive C
Write-Host "C: Total: $([math]::Round(($disk.Used+$disk.Free)/1GB,2)) GB"
Write-Host "Used: $([math]::Round($disk.Used/1GB,2)) GB"
Write-Host "Free: $([math]::Round($disk.Free/1GB,2)) GB"
Write-Host "Usage: $([math]::Round($disk.Used/($disk.Used+$disk.Free)*100,1))%"
```

**macOS / Linux:**
```bash
df -h / | tail -1 | awk '{print "Total: "$2", Used: "$3", Free: "$4", Usage: "$5}'
# For more detail on specific mount points
df -h
```

Write Windows PowerShell scripts to a temp file and execute with `powershell -ExecutionPolicy Bypass -File <path>` to avoid encoding issues with non-ASCII characters.

### Step A2: Major folder sizes

**Windows:**
```powershell
$folders = @(
    "C:\Windows",
    "C:\Program Files",
    "C:\Program Files (x86)",
    "$env:USERPROFILE\AppData",
    "$env:USERPROFILE\Downloads",
    "$env:USERPROFILE\Desktop",
    "C:\ProgramData",
    "$env:USERPROFILE\Documents"
)
foreach ($f in $folders) {
    if (Test-Path $f) {
        $size = (Get-ChildItem $f -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 0) {
            Write-Host ("{0,8:F2} GB  {1}" -f ($size/1GB), $f)
        }
    }
}
```

**macOS:**
```bash
du -sh ~/Library ~/Downloads ~/Desktop ~/Documents /Applications /Library /System/Volumes/Data/private/var 2>/dev/null
```

**Linux:**
```bash
du -sh ~/.cache ~/.config ~/.local ~/Downloads ~/Desktop ~/Documents /var /opt /tmp 2>/dev/null
```

### Step A3: Deep-dive into large folders

For any folder >10 GB, drill down to find the subfolder(s) responsible.

**Windows:**
```powershell
$target = "C:\ProgramData"  # or whatever is large
Get-ChildItem $target -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($size -gt 0.5GB) {
        Write-Host ("{0,8:F2} GB  {1}" -f ($size/1GB), $_.Name)
    }
}
```

**macOS / Linux:**
```bash
TARGET="$HOME/Library"  # or whatever is large
du -sh "$TARGET"/*/ 2>/dev/null | sort -rh | head -20
```

Also output top-20 largest files in that target for context:
```bash
# Cross-platform: find largest files
find "$TARGET" -type f -exec du -h {} + 2>/dev/null | sort -rh | head -20
```

### Step A4: Large file discovery (drive-wide)

This is the most general discovery method -- works regardless of what apps are installed.

**Windows (PowerShell):**
```powershell
# Top 50 largest files on C: (excluding system dirs), takes ~1-3 min
Get-ChildItem C:\ -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 100MB } |
    Sort-Object Length -Descending |
    Select-Object -First 50 |
    ForEach-Object { Write-Host ("{0,10:F2} MB  {1}" -f ($_.Length/1MB), $_.FullName) }
```

**macOS / Linux (faster, using find):**
```bash
find / -type f -size +100M -exec du -h {} + 2>/dev/null | sort -rh | head -50
# Or for home directory only (much faster):
find ~ -type f -size +50M -exec du -h {} + 2>/dev/null | sort -rh | head -50
```

### Step A5: Large directory discovery (home drive)

Find the biggest directories in the user's home, regardless of platform:
```bash
# Cross-platform (bash)
du -sh "$HOME"/*/ 2>/dev/null | sort -rh | head -20
```

### Step A6: Auto-discover app cache directories (Level 2 prep)

Before running Level 2, auto-discover which app data directories are consuming the most space:

**Windows:**
```powershell
# Scan AppData\Local and AppData\Roaming for large subdirs
foreach ($base in @($env:LOCALAPPDATA, $env:APPDATA)) {
    Write-Host "`n=== $base ==="
    Get-ChildItem $base -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $size = (Get-ChildItem $_.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 100MB) {
            Write-Host ("{0,8:F2} GB  {1}" -f ($size/1GB), $_.Name)
        }
    }
}
```

**macOS:**
```bash
du -sh ~/Library/Caches/*/ ~/Library/Application\ Support/*/ 2>/dev/null | sort -rh | head -30
```

**Linux:**
```bash
du -sh ~/.cache/*/ ~/.config/*/ ~/.local/share/*/ 2>/dev/null | sort -rh | head -30
```

### Step A7: Version check (SDKs, JDK, runtimes)

Check for duplicate/multiple versions. This is cross-platform.

**Windows:**
```powershell
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' 2>$null |
    Where-Object { $_.DisplayName -match "SDK|JDK|Java.*Development|Android|iOS.*Sdk|Python [0-9]|Node\.js|dotnet" } |
    Select-Object DisplayName, DisplayVersion, InstallDate,
        @{N="SizeMB";E={ if ($_.EstimatedSize) { [math]::Round($_.EstimatedSize/1024,1) } else { 0 } }} |
    Sort-Object DisplayName | Format-Table -AutoSize
```

**macOS / Linux:**
```bash
# Check for multiple Java versions
ls -d /usr/lib/jvm/* 2>/dev/null; ls -d /Library/Java/JavaVirtualMachines/* 2>/dev/null
# Check for multiple Python versions
ls -d /usr/local/bin/python* /usr/bin/python* 2>/dev/null
# Check for multiple Node versions (nvm)
ls -d ~/.nvm/versions/node/* 2>/dev/null
# Check for multiple .NET SDKs
ls -d ~/.dotnet/sdk/* 2>/dev/null; ls -d /usr/share/dotnet/sdk/* 2>/dev/null
# Check for multiple Go versions
ls -d /usr/local/go*/ 2>/dev/null
```

### Step A8: Docker disk usage

```bash
# Show total Docker disk usage
docker system df 2>/dev/null || echo "Docker not installed or not running"

# Detail breakdown
docker system df -v 2>/dev/null
```

---

## Cleanup Levels

### Level 1 — Safe Caches (always clean)

No risk, all auto-regenerated. Platform-adaptive.

#### 1a. Package manager caches

| Cache | Windows | macOS | Linux |
|-------|---------|-------|-------|
| npm | `$env:LOCALAPPDATA\npm-cache` | `~/.npm` | `~/.npm` |
| yarn | `$env:LOCALAPPDATA\Yarn\Cache` | `~/Library/Caches/Yarn` | `~/.cache/yarn` |
| pnpm | `$env:LOCALAPPDATA\pnpm-cache` | `~/Library/Caches/pnpm` | `~/.cache/pnpm` |
| pip | `$env:LOCALAPPDATA\pip\cache` | `~/Library/Caches/pip` | `~/.cache/pip` |
| Go modules | `%GOPATH%\pkg\mod` | `~/go/pkg/mod` | `~/go/pkg/mod` |
| Cargo (Rust) | `%USERPROFILE%\.cargo\registry\cache` | `~/.cargo/registry/cache` | `~/.cargo/registry/cache` |
| Gradle | `%USERPROFILE%\.gradle\caches` | `~/.gradle/caches` | `~/.gradle/caches` |
| Maven | `%USERPROFILE%\.m2\repository` | `~/.m2/repository` | `~/.m2/repository` |
| CocoaPods | N/A | `~/Library/Caches/CocoaPods` | N/A |
| Homebrew | N/A | `~/Library/Caches/Homebrew` | `/home/linuxbrew/.cache` |
| apt | N/A | N/A | `sudo apt-get clean` / `/var/cache/apt/archives` |
| snap | N/A | N/A | `sudo snap saved` → `sudo snap forget` |
| flatpak | N/A | N/A | `flatpak uninstall --unused` |
| Conda | `%USERPROFILE%\.conda\pkgs` | `~/.conda/pkgs` | `~/.conda/pkgs` |
| pipenv | `%USERPROFILE%\.virtualenvs` | `~/.local/share/virtualenvs` | `~/.local/share/virtualenvs` |

**Windows cleanup snippet:**
```powershell
# npm
if (Test-Path "$env:LOCALAPPDATA\npm-cache\_cacache") { Remove-Item "$env:LOCALAPPDATA\npm-cache\_cacache" -Recurse -Force -ErrorAction SilentlyContinue }
if (Test-Path "$env:LOCALAPPDATA\npm-cache\_npx") { Remove-Item "$env:LOCALAPPDATA\npm-cache\_npx" -Recurse -Force -ErrorAction SilentlyContinue }
if (Get-Command npm -ErrorAction SilentlyContinue) { npm cache clean --force 2>$null }

# pip
if (Get-Command python -ErrorAction SilentlyContinue) { python -m pip cache purge 2>$null }

# Go modules (only if no active Go dev, they re-download)
if (Test-Path "$env:GOPATH\pkg\mod") {
    Write-Host "Go module cache: $((Get-ChildItem "$env:GOPATH\pkg\mod" -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1GB) GB"
    # Defer to user confirmation
}

# Gradle
if (Test-Path "$env:USERPROFILE\.gradle\caches") {
    Write-Host "Gradle cache: $((Get-ChildItem "$env:USERPROFILE\.gradle\caches" -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1GB) GB"
}
```

**macOS / Linux cleanup snippet:**
```bash
# npm
rm -rf ~/.npm/_cacache 2>/dev/null
npm cache clean --force 2>/dev/null

# pip
python3 -m pip cache purge 2>/dev/null

# yarn
rm -rf ~/Library/Caches/Yarn 2>/dev/null  # macOS
rm -rf ~/.cache/yarn 2>/dev/null           # Linux

# pnpm
pnpm store prune 2>/dev/null

# Go
go clean -modcache 2>/dev/null

# Cargo
rm -rf ~/.cargo/registry/cache 2>/dev/null

# Gradle
rm -rf ~/.gradle/caches 2>/dev/null

# Conda
conda clean --all --yes 2>/dev/null

# Homebrew (macOS)
brew cleanup -s 2>/dev/null

# apt (Linux)
sudo apt-get clean 2>/dev/null
sudo apt-get autoremove --yes 2>/dev/null

# snap (Linux, remove old revisions)
snap list --all 2>/dev/null | awk '/disabled/{print $1, $3}' | while read snapname revision; do sudo snap remove "$snapname" --revision="$revision" 2>/dev/null; done

# flatpak
flatpak uninstall --unused --noninteractive 2>/dev/null
```

#### 1b. Browser caches

| Browser | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache` + `Code Cache` | `~/Library/Caches/Google/Chrome/` | `~/.cache/google-chrome/` |
| Edge | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache` + `Code Cache` | `~/Library/Caches/Microsoft Edge/` | `~/.cache/microsoft-edge/` |
| Firefox | `%APPDATA%\Mozilla\Firefox\Profiles\*\cache2` | `~/Library/Caches/Firefox/Profiles/` | `~/.cache/mozilla/firefox/` |
| Brave | `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cache` | `~/Library/Caches/BraveSoftware/Brave-Browser/` | `~/.cache/BraveSoftware/Brave-Browser/` |
| Opera | `%APPDATA%\Opera Software\Opera Stable\Cache` | `~/Library/Caches/com.operasoftware.Opera/` | `~/.cache/opera/` |
| Vivaldi | `%LOCALAPPDATA%\Vivaldi\User Data\Default\Cache` | `~/Library/Caches/Vivaldi/` | `~/.cache/vivaldi/` |

**Windows cleanup snippet (auto-detect which browsers are installed):**
```powershell
$browsers = @{
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache" = "Chrome Cache"
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache" = "Chrome Code Cache"
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache" = "Edge Cache"
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache" = "Edge Code Cache"
    "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\Cache" = "Brave Cache"
    "$env:LOCALAPPDATA\Vivaldi\User Data\Default\Cache" = "Vivaldi Cache"
}
foreach ($entry in $browsers.GetEnumerator()) {
    if (Test-Path $entry.Key) {
        $size = (Get-ChildItem $entry.Key -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
        if ($size -gt 0) {
            Write-Host ("{0,8:F2} MB  {1}" -f ($size/1MB), $entry.Value)
        }
    }
}
```

For Firefox, also look for profile caches:
```powershell
$ffProfiles = "$env:APPDATA\Mozilla\Firefox\Profiles"
if (Test-Path $ffProfiles) {
    Get-ChildItem $ffProfiles -Directory | ForEach-Object {
        $cachePath = Join-Path $_.FullName "cache2"
        if (Test-Path $cachePath) {
            $size = (Get-ChildItem $cachePath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
            if ($size -gt 0) { Write-Host ("{0,8:F2} MB  Firefox cache: {1}" -f ($size/1MB), $_.Name) }
        }
    }
}
```

**macOS / Linux:**
```bash
# Auto-detect and clean any browser cache
for dir in \
    ~/Library/Caches/Google/Chrome \
    ~/Library/Caches/Microsoft\ Edge \
    ~/Library/Caches/Firefox \
    ~/Library/Caches/BraveSoftware/Brave-Browser \
    ~/.cache/google-chrome \
    ~/.cache/microsoft-edge \
    ~/.cache/mozilla/firefox \
    ~/.cache/BraveSoftware/Brave-Browser; do
    if [ -d "$dir" ]; then
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "$size  $dir"
    fi
done
```

#### 1c. Developer tool caches

| Cache | All Platforms (relative to home) |
|-------|-------------------------------|
| `.cache/` (codex-runtimes, puppeteer, selenium) | `~/.cache/codex-runtimes`, `~/.cache/puppeteer`, `~/.cache/selenium` |
| VS Code / Cursor | `~/.vscode/extensions/.cache`, `~/AppData/Roaming/Code/CachedData` (Win), `~/Library/Application Support/Code/CachedData` (Mac), `~/.config/Code/CachedData` (Linux) |
| JetBrains caches | Covered in Level 2 |
| Android SDK | `~/Android/Sdk/.temp`, `~/Android/Sdk/emulator` (old emulator images) |
| Electron apps (Slack, Discord, Teams, etc.) | `~/AppData/Roaming/Slack/Cache` (Win), `~/Library/Application Support/Slack/Cache` (Mac), `~/.config/Slack/Cache` (Linux) |

#### 1d. System temp files

**Windows:**
```powershell
# Windows Temp
Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
# User Temp
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
# Recycle Bin
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
```

**macOS:**
```bash
# User cache/temp
rm -rf ~/Library/Caches/*/ 2>/dev/null
rm -rf /tmp/* 2>/dev/null
# Trash
rm -rf ~/.Trash/* 2>/dev/null
# System logs (older than 7 days)
sudo find /var/log -name "*.log" -mtime +7 -delete 2>/dev/null
```

**Linux:**
```bash
# User cache (caution: this clears all user caches)
rm -rf ~/.cache/*/ 2>/dev/null
# System temp
sudo rm -rf /tmp/* 2>/dev/null
# Trash
rm -rf ~/.local/share/Trash/* 2>/dev/null
# Journal logs (older than 3 days, keep max 500MB)
sudo journalctl --vacuum-time=3d 2>/dev/null
sudo journalctl --vacuum-size=500M 2>/dev/null
```

#### 1e. Log files (auto-discover)

**Windows:**
```powershell
# Find large .log files in %TEMP% and AppData
Get-ChildItem "$env:TEMP", "$env:LOCALAPPDATA", "$env:APPDATA" -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -match "\.log$|\.etl$" -and $_.Length -gt 10MB } |
    Sort-Object Length -Descending |
    Select-Object -First 30 |
    ForEach-Object { Write-Host ("{0,8:F2} MB  {1}" -f ($_.Length/1MB), $_.FullName) }
```

**macOS / Linux:**
```bash
find ~/ -type f \( -name "*.log" -o -name "*.etl" \) -size +10M -exec du -h {} + 2>/dev/null | sort -rh | head -30
```

---

### Level 2 — App Caches (mostly safe)

Application cache/addon/download folders. Apps re-download if needed.

**IMPORTANT**: Instead of relying on a fixed list of apps (which won't generalize), **first run Step A6 (auto-discover)** to identify which per-app data directories are actually consuming significant space on THIS machine, then cross-reference with the patterns below.

#### 2a. Auto-discovery heuristics

After running Step A6, classify discovered large directories by heuristic:

- **Cache directories** — paths containing `cache`, `Cache`, `caches`, `CachedData`, `temp`, `tmp` → safe to delete
- **Log directories** — paths containing `logs`, `Logs`, `log`, `diagnostics` → safe to delete old
- **Download directories** — paths containing `download`, `Downloads`, `downloads`, `installer` → check with user
- **Addon/plugin directories** — paths containing `addons`, `plugins`, `extensions`, `components` → usually re-downloadable
- **Data/settings** — paths containing `data`, `Data`, `storage`, `databases` → DO NOT delete without explicit user confirmation

#### 2b. Common app patterns (reference table)

Use this table to interpret discovered directories. This is a **reference** -- the auto-discovery in Step A6 is the primary method.

| App Category | Path Patterns (cross-platform) | What to target |
|-------------|-------------------------------|----------------|
| JetBrains IDEs | `{JetBrains,IntelliJIdea,PyCharm,WebStorm,AndroidStudio}/*/caches/`, `*/logs/` | `caches/`, `logs/` only |
| VS Code / forks | `{Code,Code - Insiders,Cursor,VSCodium}/CachedData`, `*/Cache/` | `CachedData`, `Cache/` |
| Office suites | `kingsoft/`, `wps/`, `WPS Office/`, `Microsoft/Office/`, `LibreOffice/` | `addons/`, `download/`, `cache/`, `backup/` |
| IM / Conferencing | `Tencent/`, `WeChat/`, `QQ/`, `Teams/`, `Slack/`, `DingTalk/`, `WeMeeting/`, `Zoom/`, `Discord/` | `Cache/`, `cache/`, `temp/`, `download/` |
| Video / Media | `bilibili/`, `JianyingPro/`, `CapCut/`, `Adobe/`, `DaVinci/` | `cache/`, `Cache/`, `media/`, `proxy/`, `render/` |
| AI / ML tools | `Doubao/`, `ChatGPT/`, `Copilot/`, `Ollama/`, `LM Studio/`, `huggingface/` | `Cache/`, `models/` (models are large re-downloads, confirm first) |
| Education / Enterprise | `Seewo/`, `zoom/`, `Webex/` | `Cache/`, `downloads/`, `recordings/` (recordings may be user data) |
| NVIDIA / GPU | `NVIDIA Corporation/`, `AMD/` | `installer/`, `Download/`, `cache/` |
| Creative apps | `Adobe/`, `Figma/`, `Canva/`, `GIMP/`, `Blender/`, `Unity/`, `Unreal Engine/` | `Cache/`, `temp/`, `scratch/` |

#### 2c. Safety rules for Level 2

- **Only delete cache/log/temp/download subdirectories**, never user documents or settings
- **Show the user each app + size before deleting**
- **For model files (Ollama, HuggingFace, LM Studio)**: models are huge re-downloads; only delete if user confirms they don't use those models anymore
- **For recordings/chat histories**: these are user data, not cache; require explicit confirmation
- **When uncertain**: offer to rename the directory to `<name>.bak` instead of deleting

---

### Level 3 — Store & Package Caches

#### 3a. Windows-specific

| Item | Location | Notes |
|------|----------|-------|
| NuGet packages cache | `%ProgramFiles(x86)%\Microsoft SDKs\NuGetPackages\` | VS cache, auto-restore on next build |
| UWP NuGet packages | `%ProgramFiles(x86)%\Microsoft SDKs\UWPNuGetPackages\` | Same |
| WinGet (App Installer) | `%LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_*\LocalState\` | Windows package manager cache |
| Game launcher caches | `C:\ProgramData\Ubisoft\`, `C:\ProgramData\Epic\`, `%ProgramFiles(x86)%\Steam\depotcache\` | Only if user no longer plays |
| Windows Update cache | `C:\Windows\SoftwareDistribution\Download\` | Safe: `del /q /s` this folder; WU redownloads |

#### 3b. macOS-specific

| Item | Location | Notes |
|------|----------|-------|
| Homebrew cache | `~/Library/Caches/Homebrew/` | `brew cleanup -s` |
| MacPorts | `/opt/local/var/macports/software/` | `sudo port clean --all installed` |
| App Store updates | `/Library/Updates/` | Safe to delete (old update packages) |
| Xcode derived data | `~/Library/Developer/Xcode/DerivedData/` | Rebuild on next compile |
| Xcode device support | `~/Library/Developer/Xcode/iOS DeviceSupport/` | Old iOS symbol files |
| Xcode simulators | `~/Library/Developer/Xcode/iOS Simulator/` | Old simulator images |
| iOS backups | `~/Library/Application Support/MobileSync/Backup/` | Only if user confirms |
| .NET NuGet | `~/.nuget/packages/` | `dotnet nuget locals all --clear` |

#### 3c. Linux-specific

| Item | Location | Notes |
|------|----------|-------|
| apt cache | `/var/cache/apt/archives/` | `sudo apt-get clean` |
| yum/dnf cache | `/var/cache/yum/`, `/var/cache/dnf/` | `sudo dnf clean all` |
| pacman cache | `/var/cache/pacman/pkg/` | `sudo paccache -r` (keep 3 versions) |
| snap revisions | `/var/lib/snapd/snaps/` | Old revisions |
| flatpak unused | `/var/lib/flatpak/` | `flatpak uninstall --unused` |
| .NET NuGet | `~/.nuget/packages/` | `dotnet nuget locals all --clear` |
| Docker (see dedicated section) | `/var/lib/docker/` | `docker system prune` |

---

### Level 4 — Vendor Bloat & OEM Software

Hardware vendor support software often accumulates huge backup/remediation data. This is mostly Windows-specific.

| Common Vendors | Typical Large Paths |
|----------------|-------------------|
| Dell | `C:\ProgramData\Dell\SARemediation\SystemRepair\Snapshots\` |
| Dell | `C:\ProgramData\Dell\SupportAssist\Agent\Downloads\` |
| Lenovo | `C:\ProgramData\Lenovo\` |
| HP | `C:\ProgramData\HP\` |
| ASUS | `C:\ProgramData\ASUS\` |
| Acer | `C:\ProgramData\Acer\`, `C:\ProgramData\OEM\` |
| NVIDIA | `C:\ProgramData\NVIDIA Corporation\` (driver installer cache) |
| AMD | `C:\AMD\` (driver installer extracts) |
| Intel | `C:\ProgramData\Intel\` |
| Realtek | `C:\ProgramData\Realtek\` |

**Auto-discovery approach** (more general than hardcoded paths):
```powershell
# Find large vendor directories in ProgramData
Get-ChildItem "C:\ProgramData" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    if ($size -gt 500MB) {
        Write-Host ("{0,8:F2} GB  {1}" -f ($size/1GB), $_.FullName)
    }
}
```

#### For Dell SupportAssist restore points specifically:

```powershell
$snapshots = "C:\ProgramData\Dell\SARemediation\SystemRepair\Snapshots"
Get-ChildItem $snapshots -Directory | Where-Object { $_.Name -match "^\d+.*Backup$" } |
    Sort-Object Name -Descending | Select-Object -Skip 1 | Remove-Item -Recurse -Force
# Also remove orphaned .param.xml / .reg.inp / .reg_*.inp for deleted snapshots
```

This keeps only the most recent snapshot. The catalog DB (`SnapshotsList.xml`, `base.sqlite`) will have stale references but Dell SupportAssist self-heals on next run.

---

### Level 5 — Old SDK & Runtime Versions

Check for duplicate versions and offer to prune. **Cross-platform.**

#### Auto-discovery (find installed SDKs by version):

**Windows:**
```powershell
# Find all SDK/runtime entries in Add/Remove Programs
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*' 2>$null |
    Where-Object { $_.DisplayName -match "SDK|JDK|Java|Android|iOS|Windows SDK|.NET (Core|SDK|Runtime)|Python [0-9]|Node\.js|Go [0-9]" } |
    Select-Object DisplayName, DisplayVersion, InstallDate,
        @{N="SizeMB";E={ if ($_.EstimatedSize) { [math]::Round($_.EstimatedSize/1024,1) } else { 0 } }} |
    Sort-Object DisplayName | Format-Table -AutoSize
```

**macOS / Linux:**
```bash
# Java
ls -la /Library/Java/JavaVirtualMachines/ 2>/dev/null
ls -la /usr/lib/jvm/ 2>/dev/null

# .NET
dotnet --list-sdks 2>/dev/null
dotnet --list-runtimes 2>/dev/null

# Python
ls -d /usr/local/bin/python3.* /usr/bin/python3.* 2>/dev/null

# Node (via nvm)
nvm ls 2>/dev/null

# Go
ls -d /usr/local/go*/ 2>/dev/null
```

#### Common duplicates to watch for:
- Java JDK: multiple versions (e.g., 13 + 23) — remove oldest
- Android SDK: .NET MAUI Android SDK packs (e.g., 33 + 34) — keep newest
- iOS SDK packs (16 + 17) — keep newest
- MacCatalyst SDK packs (16 + 17) — keep newest
- Windows SDK multiple versions (rare on disk, but in registry)
- .NET SDK/Runtime older versions
- Python older versions (keep 2 latest minor versions)

**Uninstall approach** (for SDKs that show in Add/Remove Programs):

```powershell
# Find the uninstall string for a specific app
$app = Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' 2>$null |
    Where-Object { $_.DisplayName -match "Java.*13|JDK 13" }
if ($app.UninstallString) {
    Write-Host "Uninstall string: $($app.UninstallString)"
}
```

Then run the uninstall string, either with `/quiet` if available, or show the user the command.

**For disk-level deletion of .NET SDK packs:**

```powershell
$sdkPacks = "C:\Program Files\dotnet\packs"
# Find packs with multiple versions:
Get-ChildItem "$sdkPacks\Microsoft.Android.Sdk.Windows" -Directory | Sort-Object Name
# Remove oldest:
Remove-Item "$sdkPacks\Microsoft.Android.Sdk.Windows\33.0.95" -Recurse -Force
```

---

### Docker Cleanup (any level, developer-focused)

Docker can consume tens of GBs. Run this analysis and offer to the user at any level.

```bash
# Check if Docker is available
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    echo "=== Docker Disk Usage ==="
    docker system df
    echo ""
    echo "--- Detailed ---"
    docker system df -v 2>/dev/null | head -80
else
    echo "Docker not available or not running."
fi
```

**Cleanup commands (from safest to most aggressive):**

| Command | What it removes | Risk |
|---------|----------------|------|
| `docker builder prune --force` | Build cache only | Safe |
| `docker image prune --force` | Dangling images (`<none>:<none>`) | Safe |
| `docker image prune -a --force` | All unused images | Moderate |
| `docker container prune --force` | Stopped containers | Moderate |
| `docker volume prune --force` | Unused volumes | Caution (data loss) |
| `docker system prune --force` | Everything unused (NOT volumes) | Moderate |
| `docker system prune -a --force --volumes` | Everything unused INCLUDING volumes | High |

---

### Level 6 — System Restore Points & System Cleanup (Advanced)

#### 6a. Windows System Restore Points

```powershell
# List all restore points
Get-ComputerRestorePoint | Sort-Object CreationTime -Descending | Format-Table -AutoSize

# Keep only the latest (CAUTION!)
vssadmin list shadows
```

**Always keep at least one recent restore point.**

#### 6b. Windows System Cleanup (additional items)

| Item | Location | Notes |
|------|----------|-------|
| Hibernation file | `C:\hiberfil.sys` | `powercfg -h off` (disables hibernation, frees RAM-size file) |
| Windows.old | `C:\Windows.old` | Post-upgrade backup, safe to delete via Disk Cleanup |
| Windows Update cache | `C:\Windows\SoftwareDistribution\Download\` | Safe, auto-redownloads |
| Delivery Optimization | `C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization\` | Safe, peer-to-peer update cache |
| System error dumps | `C:\Windows\Minidump\`, `C:\Windows\MEMORY.DMP` | Debug dumps, safe if not debugging |
| Windows Error Reporting | `%LOCALAPPDATA%\Microsoft\Windows\WER\` | Crash report archives |

**Third-party restore point folder structure** (Dell example):

```
C:\ProgramData\Dell\SARemediation\SystemRepair\Snapshots\
├── 1719555382-param.xml         # Snapshot metadata (old)
├── 1719555382-reg_0001.inp      # Registry backup (old, ~400 MB)
├── 1723004775-Backup/           # Full backup directory (old, ~76 MB)
├── 1733660823-Backup/           # Full backup directory (latest, ~3 GB)
│   ├── 1733660823-state.sqlite
│   └── *.dll, *.evtx, etc.
├── Backup/                      # Shared system file backup store (keep)
├── base.sqlite                  # Snapshot catalog (keep)
└── SnapshotsList.xml            # Catalog (keep)
```

Only delete snapshots that predate the most recent one. The `Backup/` root folder may be shared -- keep it.

#### 6c. macOS Time Machine local snapshots

```bash
# List local snapshots
tmutil listlocalsnapshots / 2>/dev/null
# Delete local snapshots (free up "purgeable" space)
sudo tmutil deletelocalsnapshots / 2>/dev/null
```

#### 6d. macOS system storage analysis

```bash
# Show system storage breakdown (macOS Ventura+)
system_profiler SPStorageDataType 2>/dev/null
# Show "purgeable" space
diskutil apfs list 2>/dev/null | grep -A5 "Purgeable"
```

---

## Execution Pattern

For every cleanup action:

1. **Detect platform** — adapt commands accordingly
2. **Measure before** — show current size
3. **Confirm** — ask user: "Delete XYZ (X.XX GB)?" with clear risk level
4. **Execute** — run the deletion command
5. **Measure after** — show size delta
6. **Report** — cumulative freed space

### Dry-run mode

When `--dry-run` is specified, do everything except the actual deletion:
- Perform all analysis and size calculations
- Show what **would** be deleted and how much space it would free
- End with a summary: "Would free X.XX GB if executed"
- Offer: "Run without --dry-run to execute cleanup?"

### Command examples

For folders (cross-platform via bash):
```bash
# Delete a directory
rm -rf "/path/to/target/" 2>/dev/null

# Windows fallback (for stubborn files)
cmd.exe /c "rmdir /s /q C:\path\to\target 2>nul"

# macOS/Linux: use sudo for system locations
sudo rm -rf /path/to/system/cache 2>/dev/null
```

For package managers:
```bash
npm cache clean --force 2>&1
python -m pip cache purge 2>&1
brew cleanup -s 2>&1          # macOS
sudo apt-get clean 2>&1        # Linux
```

For uninstallers (Windows):
```powershell
# Quiet uninstall
Start-Process -FilePath "uninstaller.exe" -ArgumentList "/quiet" -Wait
```

For Docker:
```bash
docker system prune -a --force 2>&1
```

---

## Finding Hidden / Protected Files

Some backup tools create hidden system files. Platform-specific approaches:

**Windows:**
```bash
# Use cmd.exe for hidden/system files
cmd.exe /c "dir /a /s /b C:\Path\To\Check 2>nul"
```

**macOS / Linux:**
```bash
# Include hidden files in size calculation
du -sh /path/* /path/.[!.]* 2>/dev/null
# Find files with hidden/system attributes
find /path -name ".*" -type f 2>/dev/null
```

For Dell SARemediation specifically, the `Snapshots/` folder contains the data;
the root `SystemRepair/` folder size may include VSS data not visible as standard files.

---

## Important Safety Rules

1. **Detect platform first** — never assume the OS
2. **Never delete user documents** — Desktop, Documents, Pictures files need explicit confirmation
3. **Never delete without showing the user what will be deleted and how much space it will free**
4. **Always keep at least one restore point** for system protection
5. **Don't touch Windows system folders** (System32, WinSxS, etc.) except Temp
6. **For vendor tools** (Dell, Lenovo, Apple): understand what the folder does before deleting
7. **When in doubt about a folder**, offer to rename it instead of delete (add `.bak` suffix)
8. **After cleanup**, always show the user the total freed space and remaining free space
9. **Prefer auto-discovery over hardcoded lists** — broad scans find what's actually taking space
10. **For large re-downloadable assets** (models, SDKs, emulator images): warn the user about re-download size/time

---

## Consolidated Safe Cleanup Scripts

### Windows Safe Cleanup (Level 1)

```powershell
Write-Host "=== Disk Cleanup: Level 1 (Safe) ==="
$beforeGB = [math]::Round(((Get-PSDrive C).Used)/1GB, 2)

# 1. npm cache
if (Test-Path "$env:LOCALAPPDATA\npm-cache\_cacache") {
    Remove-Item "$env:LOCALAPPDATA\npm-cache\_cacache" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$env:LOCALAPPDATA\npm-cache\_npx" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$env:LOCALAPPDATA\npm-cache\_prebuilds" -Recurse -Force -ErrorAction SilentlyContinue
}

# 2. pip cache
python -m pip cache purge 2>$null | Out-Null

# 3. .cache (dev tool caches)
$userCache = "$env:USERPROFILE\.cache"
@("codex-runtimes", "puppeteer", "selenium") | ForEach-Object {
    $p = Join-Path $userCache $_
    if (Test-Path $p) { Remove-Item "$p\*" -Recurse -Force -ErrorAction SilentlyContinue }
}

# 4. Browser caches (auto-detect)
$browserPaths = @(
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Vivaldi\User Data\Default\Cache"
)
$browserPaths | ForEach-Object {
    if (Test-Path $_) { Remove-Item "$_\*" -Recurse -Force -ErrorAction SilentlyContinue }
}

# 5. System temp files
Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue

# 6. Recycle Bin
Clear-RecycleBin -Force -ErrorAction SilentlyContinue

# 7. Windows Update cache
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue

$afterGB = [math]::Round(((Get-PSDrive C).Used)/1GB, 2)
Write-Host "Safe cleanup complete. Freed approx: $($beforeGB - $afterGB) GB"
Write-Host "Free space now: $([math]::Round(((Get-PSDrive C).Free)/1GB, 2)) GB"
```

### macOS Safe Cleanup (Level 1)

```bash
#!/bin/bash
echo "=== Disk Cleanup: Level 1 (Safe) ==="
before=$(df -h / | tail -1 | awk '{print $4}')

# npm / yarn / pnpm
rm -rf ~/.npm/_cacache 2>/dev/null
npm cache clean --force 2>/dev/null
rm -rf ~/Library/Caches/Yarn 2>/dev/null
pnpm store prune 2>/dev/null

# pip
python3 -m pip cache purge 2>/dev/null

# Homebrew
brew cleanup -s 2>/dev/null

# User caches
rm -rf ~/Library/Caches/*/ 2>/dev/null

# Temp files
rm -rf /tmp/* 2>/dev/null

# Trash
rm -rf ~/.Trash/* 2>/dev/null

# Xcode derived data
rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null

# .cache
rm -rf ~/.cache/codex-runtimes ~/.cache/puppeteer ~/.cache/selenium 2>/dev/null

# Docker (if installed)
docker builder prune --force 2>/dev/null
docker image prune --force 2>/dev/null

after=$(df -h / | tail -1 | awk '{print $4}')
echo "Safe cleanup complete."
echo "Free space before: $before, after: $after"
```

### Linux Safe Cleanup (Level 1)

```bash
#!/bin/bash
echo "=== Disk Cleanup: Level 1 (Safe) ==="
before=$(df -h / | tail -1 | awk '{print $4}')

# npm / yarn / pnpm
rm -rf ~/.npm/_cacache 2>/dev/null
npm cache clean --force 2>/dev/null
rm -rf ~/.cache/yarn 2>/dev/null
pnpm store prune 2>/dev/null

# pip
python3 -m pip cache purge 2>/dev/null

# Go
go clean -modcache 2>/dev/null

# Cargo
rm -rf ~/.cargo/registry/cache 2>/dev/null

# apt
sudo apt-get clean 2>/dev/null
sudo apt-get autoremove --yes 2>/dev/null

# snap (remove old revisions)
snap list --all 2>/dev/null | awk '/disabled/{print $1, $3}' | while read snapname revision; do
    sudo snap remove "$snapname" --revision="$revision" 2>/dev/null
done

# flatpak
flatpak uninstall --unused --noninteractive 2>/dev/null

# journal logs
sudo journalctl --vacuum-time=3d 2>/dev/null
sudo journalctl --vacuum-size=500M 2>/dev/null

# User caches
rm -rf ~/.cache/*/ 2>/dev/null

# Temp files
sudo rm -rf /tmp/* 2>/dev/null

# .cache
rm -rf ~/.cache/codex-runtimes ~/.cache/puppeteer ~/.cache/selenium 2>/dev/null

after=$(df -h / | tail -1 | awk '{print $4}')
echo "Safe cleanup complete."
echo "Free space before: $before, after: $after"
```
