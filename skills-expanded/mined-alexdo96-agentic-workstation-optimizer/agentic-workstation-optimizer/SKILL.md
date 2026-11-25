---
name: agentic-workstation-optimizer
description: >-
  Diagnose and optimize Windows hardware and software performance (CPU power plan &
  scheduler, GPU HAGS & DirectX Flip Model, RAM svchost consolidation & working-set
  trim, SSD/NTFS I/O, Windows UI responsiveness), network throughput (NIC buffers,
  EEE/ULP power saving, TCP stack), corporate network/VPN compatibility for Cloud AI
  APIs (Anthropic, OpenAI, Gemini, OpenRouter), ephemeral ports for automated testing
  (Playwright, Appium, API tests), WSL2 Mirrored Networking, and Local AI (Ollama)
  with automatic backup and rollback. Supports Home (-Mode All / Gaming) and Office
  (-Mode Work) environments.
---

# Agentic Workstation Optimizer (`agentic-workstation-optimizer`)

This skill provides a practical workflow to diagnose and optimize Windows hardware, software, network, gaming, automated testing, and AI workflows on both **Company (Office)** and **Home** PCs. Every change is backed up automatically before being applied so the machine can be restored to its original settings at any time.

---

## 1. Operating Modes (`-Mode All | Work | Gaming`)

1. **Company / Office PC (`-Mode Work`):**
   - **Safety Rules:**
     - Never modify company router or firewall settings.
     - Never alter corporate DNS servers, Active Directory settings, or VPN profiles.
     - Skips gaming-specific registry keys (`GameDVR`, `Games` MMCSS profile).
   - **Scope:** Unlocks CPU power plan (`Ultimate Performance` / `High performance`) & foreground scheduler (`Win32PrioritySeparation = 38`), consolidates RAM `svchost.exe` processes (`SvcHostSplitThresholdInKB`), speeds up SSD/NTFS file I/O (`LongPathsEnabled`, `disablelastaccess`, `8dot3name`), removes Windows network throttling (`NetworkThrottlingIndex`), increases NIC hardware buffers (`2048`), configures Node.js IPv4 priority (`--dns-result-order=ipv4first`) & Windows Certificate Store (`NODE_USE_SYSTEM_CA=1`, `git http.sslBackend=schannel`), expands ephemeral ports (`55,535` ports for Playwright/Appium/API tests), configures WSL2 Mirrored Networking, and tunes GPU HAGS + Ollama memory usage.
2. **Home PC — Gaming + AI + Work (`-Mode All`, Default):**
   - Includes all optimizations from `-Mode Work`, plus Gaming & Multimedia optimizations: DirectX Windowed Flip Model (`SwapEffectUpgradeEnable=1`), Auto Game Mode, disabling background `GameDVR` capture overhead, setting `MMCSS` `Games` priority (`GPU Priority = 8`, `Priority = 6`, `Scheduling Category = High`), and optional home router Wi-Fi 6 (`160MHz`) tuning.
3. **Dedicated Gaming Mode (`-Mode Gaming`):**
   - Focuses on CPU power & scheduler, GPU HAGS & DirectX Flip Model, MMCSS `Games` priority, disabling `GameDVR`, RAM & SSD I/O, and low-latency network settings (`TCPNoDelay`, NIC buffers, disabling EEE/ULP sleep states).

---

## 2. Included Scripts (`./scripts/`)

| Script | Purpose |
| :--- | :--- |
| [diagnose-network-ai.ps1](./scripts/diagnose-network-ai.ps1) | Read-only check: NIC buffers, Windows TCP stack, ephemeral ports, SSD/NTFS settings, IPv6 vs IPv4 routing, non-fragmented VPN MTU size, Cloud AI API latency, CDN download speed, CPU/RAM/GPU/Gaming settings, Ollama/WSL2 config, and `-SaveReport` summary generator. |
| [optimize-workstation.ps1](./scripts/optimize-workstation.ps1) | Main optimization script (`-Mode All \| Work \| Gaming`): Automatically runs `backup-and-rollback.ps1` first, then applies hardware, software, network, gaming, testing, WSL2, and AI settings. |
| [backup-and-rollback.ps1](./scripts/backup-and-rollback.ps1) | Saves current system settings to `backups/latest-snapshot.json` (`-Action Backup`) and restores original settings (`-Action Rollback`). |
| [optimize-wsl2.ps1](./scripts/optimize-wsl2.ps1) | Updates `~/.wslconfig` with `networkingMode=mirrored`, `dnsTunneling=true`, `autoProxy=true`, and `autoMemoryReclaim=gradual` so WSL2/Docker keeps network access on corporate VPNs and releases unused RAM. |
| [free-ai-resources.ps1](./scripts/free-ai-resources.ps1) | Stops idle Ollama models sitting in GPU VRAM (`ollama stop`), closes leftover WebDriver processes (`chromedriver`, `geckodriver`, `msedgedriver`), and trims idle background working-set RAM via Win32 `EmptyWorkingSet`. |

---

## 3. Execution Steps

### Step 1: Run Diagnostics
```powershell
powershell -ExecutionPolicy Bypass -File "<path-to-skill>/scripts/diagnose-network-ai.ps1" -SaveReport
```
Review the output for:
- CPU power plan stuck on `Balanced` or default `Win32PrioritySeparation = 2`.
- Fragmented `SvcHostSplitThresholdInKB` or disabled GPU HAGS / DirectX Flip Model.
- Small NIC buffers (`256`/`512` instead of `2048`) or enabled adapter power-saving modes (`EEE`, `ULP`, `ITR`).
- Default Windows packet throttling (`NetworkThrottlingIndex = 10`).
- Broken IPv6 routing (causing Node.js / Claude Code / Playwright to wait on IPv6 timeouts before using IPv4) or reduced MTU size over VPN (`Effective Non-Fragmented MTU < 1500`).
- Default ephemeral port limits (`MaxUserPort` unset).

### Step 2: Apply Optimizations (Automatically Backs Up First)
```powershell
# Home PC (Gaming + AI + Work):
powershell -ExecutionPolicy Bypass -File "<path-to-skill>/scripts/optimize-workstation.ps1" -Mode All

# Office / Company PC (Work + AI only, no gaming tweaks):
powershell -ExecutionPolicy Bypass -File "<path-to-skill>/scripts/optimize-workstation.ps1" -Mode Work
```
*(If the current terminal is not running as Administrator, the script applies all user-level settings and prints a 1-line command to run in an elevated PowerShell window for registry and network adapter changes).*

### Step 3: Free RAM & GPU VRAM (Optional)
```powershell
powershell -ExecutionPolicy Bypass -File "<path-to-skill>/scripts/free-ai-resources.ps1"
```

### Step 4: Verify Results
```powershell
powershell -ExecutionPolicy Bypass -File "<path-to-skill>/scripts/diagnose-network-ai.ps1" -SaveReport
```
Compare the before and after values for the user.

### Step 5: Revert Changes (If Needed)
```powershell
powershell -ExecutionPolicy Bypass -File "<path-to-skill>/scripts/backup-and-rollback.ps1" -Action Rollback
```

### Step 6: Router / Wi-Fi 6 Configuration (Optional, Home Networks Only)
See [references/router-optimization.md](./references/router-optimization.md).
