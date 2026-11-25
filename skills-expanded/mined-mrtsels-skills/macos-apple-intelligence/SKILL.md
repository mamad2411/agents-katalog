---
name: macos-apple-intelligence
description: Enable Apple Intelligence (端侧 + PCC云端) on Chinese-market Macs (CH/A region) using RegionSpoof/enableMacosAI kext. Covers SIP/AMFI checks, install, PCC 32080 diagnosis (server-side vs pool staleness), attestation pool troubleshooting, and GREYMATTER eligibility verification.
---

# macOS Apple Intelligence Enablement (CH/A → LL/A)

> **Diagnose before acting.** When troubleshooting PCC 32080, check the log signal (`attestationsExist` count, `didn't receive any inline attestations`) BEFORE touching the pool. Wrong action wastes time and frustrates the user.
>
> **Be concise.** This user operates in extreme-directive mode: short commands, single words ("看log", "?"). No chatty explanations, no step-by-step walkthroughs unless asked. Deliver evidence, not speculation.

Enable **full Apple Intelligence** (on-device + Private Cloud Compute) on a Chinese-market Mac (region code CH/A) by spoofing the region to LL/A at the IORegistry level.

## Tooling

Use **SkyBlue997/enableMacosAI** (github.com/SkyBlue997/enableMacosAI) — a unified repo with `install.sh` (install/status/diagnose/uninstall), pre-built kext, and LaunchDaemon for auto-load. ~1.5k⭐.

## Prerequisites

- macOS 27+ / Apple Silicon
- **SIP disabled** — `csrutil disable` from Recovery (hold Touch ID/power at boot → Terminal)
- **AMFI enabled** (default) — no `amfi_get_out_of_my_way` boot-arg
- **Apple Account region** set to a supported country (US/JP/etc.), not China/CN
- **System language == Siri language** — both English (US) recommended for stability

## Installation Flow

```bash
# 1. Clone (tmp gets cleaned on reboot, re-clone if needed)
mkdir -p /tmp/enableMacosAI && cd /tmp/enableMacosAI
git clone https://github.com/SkyBlue997/enableMacosAI.git .

# 2. Run install — copies kext + LaunchDaemon, then prompts for approval
sudo ./install.sh

# 3. Go to System Settings → Privacy & Security → scroll to bottom
#    → click [Allow] for "com.local.RegionSpoof was blocked from loading"
#    → **Restart**

# 4. macOS 27+ extra step (even with SIP off):
#    After restart → System Settings → Privacy & Security → "Enable System Extensions..."
#    → Touch ID / password → Shutdown →
#    Recovery (hold power) → Startup Security Utility → Security Policy → enable kernel extensions
#    → Restart

# 5. Verify
sudo ./install.sh status
# Expected output:
#   SIP: 已关(Permissive)
#   AMFI: 启用
#   region=LL/A: 是
#   kext 已加载: 是
#   GREYMATTER: 4(eligible)
```

## Verification Commands

```bash
# Region
ioreg -ard1 -c IOPlatformExpertDevice | plutil -p - | grep region-info

# GREYMATTER eligibility (4 = eligible)
sudo /usr/libexec/PlistBuddy -c 'Print :OS_ELIGIBILITY_DOMAIN_GREYMATTER:os_eligibility_answer_t' /private/var/db/eligibilityd/eligibility.plist

# Full diagnose (paste into GitHub issues)
sudo ./install.sh diagnose

# Apple Foundation Models CLI — most authoritative PCC check
fm available
#   System model available               ← end-side works
#   PCC model available                   ← cloud-side works
#   Error: PCC inference is not available in this context.  ← see below for context dependency
```

## Apple Foundation Models CLI (`fm`)

The `/usr/bin/fm` CLI is Apple's official tool for interacting with Foundation Models. The key diagnostic commands:

| Command | Purpose |
|---------|---------|
| `fm available` | Check both system + PCC model availability |
| `fm available --model system` | Check only end-side model |
| `fm available --model pcc` | Check only cloud-side (PCC) model |
| `fm respond 'prompt'` | Generate a response (default: system model) |
| `fm respond --model pcc 'prompt'` | Generate via PCC server |
| `fm respond --model pcc --stream 'prompt'` | Streamed PCC response |
| `fm chat` | Interactive session |
| `fm quota-usage` | Check model quota |

**IMPORTANT: fm CLI environment dependency.** The `fm` CLI may return different PCC availability depending on the calling process's XPC bootstrap context:

- **User's Terminal.app (zsh)**: Most reliable. Full Aqua session XPC bootstrap. Run `fm available` here for the real answer.
- **Hermes terminal tool (bash via Python)**: May incorrectly report "PCC not available" even when PCC works. The Hermes process lineage has a different XPC audit session.
- **Always verify by running `fm` from the user's own Terminal.app, not the Hermes TUI terminal tool.**

Actual PCC status is determined by `fm respond --model pcc` from Terminal.app, not by the terminal tool's `fm available` output.

## Post-Install

- AI models (~30GB total) **auto-download** in the background via Apple services through whatever proxy/VPN is active
- Check download progress via `nettop` — traffic shows under MacPacketTunnel (Shadowrocket) / nsurlsessiond / AssetCache
- Model asset size check: `sudo ./install.sh diagnose` shows current download status

## Post-Install: Ensure Persistence Across Reboots

**Root cause of "Apple Intelligence disappears after reboot" on macOS 27 Beta 3:**

The install process downloads files from GitHub — these arrive with `com.apple.quarantine` extended attribute. At boot, the LaunchDaemon `com.local.regionkext` and its load script are rejected by the system because of this quarantine flag. Result: kext loads (region=LL/A) but the eligibility files are never refreshed, so GREYMATTER falls back to 2 after every restart.

**Fix** — remove quarantine xattr from the LaunchDaemon, script, and kext, then re-register:

```bash
# 1. Remove quarantine from all three components
sudo xattr -dr com.apple.quarantine /Library/LaunchDaemons/com.local.regionkext.plist
sudo xattr -dr com.apple.quarantine /usr/local/bin/region-kext-load.sh
sudo xattr -dr com.apple.quarantine /Library/Extensions/RegionSpoof.kext

# 2. Re-register and kickstart the LaunchDaemon
sudo launchctl bootout system /Library/LaunchDaemons/com.local.regionkext.plist 2>/dev/null
sudo launchctl bootstrap system /Library/LaunchDaemons/com.local.regionkext.plist
sudo launchctl kickstart -k system/com.local.regionkext
sleep 10

# 3. Verify
sudo launchctl print system/com.local.regionkext
#   runs > 0
#   last exit code = 0
sudo cat /var/log/region-kext.log
#   region-kext-load done  ← latest entry
sudo ./install.sh status
#   GREYMATTER: 4(eligible)
```

## Known Pitfalls

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| kext not approved | Didn't click Allow in Privacy & Security | System Settings → Privacy & Security → Allow → Restart |
| `Authenticating extension failed` | SIP partially on (Reduced Security) | Must be fully off (Permissive) |
| GREYMATTER=2 despite region=LL/A | Apple Account region still CN, or language mismatch | Change account country + language, restart eligibilityd |
| PCC fails (32001 + RetryAfter) | Apple backend rate-limiting | Stop clicking, wait hours/overnight |
| PCC fails (32080) + `didn't receive any inline attestations` in log | **Server-side SEP attestation rejection** — PCC server detects CH/A hardware identity against claimed LL/A. NOT fixable by pool reset. | End-side models work; PCC-dependent features (tone rewrite, Image Playground, Reframe) will not work on CH/A hardware. |
| PCC fails (32080) + `attestationsExist: clientCacheSize=0` or small | Local attestation pool genuinely empty | Reset + idle 15-30 min (see references/pcc-troubleshooting.md) |
| 32080 persists after pool reset | Making PCC requests immediately after reset prevents daemon from idle-building attestations | Don't touch PCC for 15-30 min after reset |
| `BUG IN CLIENT OF libsqlite3.dylib: vnode unlinked while in use` | Deleted db.sqlite while daemon held SQLite WAL/journal from a prior session | Kill daemon FIRST, THEN delete files (never reverse) |
| /tmp/enableMacosAI missing after reboot | tmpfs cleared on restart | Re-clone the repo |
| AI disappears after reboot (GREYMATTER=2) despite kext loaded | `com.apple.quarantine` xattr on LaunchDaemon/script/kext blocks boot-time execution, eligibilityd never refreshed | Remove quarantine xattr from plist, script, and kext; re-register + kickstart (see §Post-Install: Ensure Persistence Across Reboots) |

## PCC Error 32080 — Diagnostic First

Error 32080 has **two different root causes** with different solutions. **Diagnose the log before acting.** Reset the pool when the pool is empty; do NOT reset when the server is rejecting.

### Scenario A: Local Pool Staleness (fixable)

**Key signal**: `attestationsExist: clientCacheSize=0` or very small, after a known trigger (region change, AMFI toggle, long idle, first boot).

The local `db.sqlite` has no valid attestations. Fix: reset the pool. See [references/pcc-troubleshooting.md](references/pcc-troubleshooting.md) §"Local Pool Staleness".

### Scenario B: Server-Side Attestation Rejection (hardware limitation)

**Key signal**: `didn't receive any inline attestations` in the log. The daemon HAS attestations (40+ cached, `clientCacheSize=40`), sends them to the PCC server, but the server refuses to return inline attestations.

The SEP chip on a Chinese-market Mac generates hardware-level attestation proofs embedded at the factory. The PCC server cross-references this hardware identity against the claimed region and detects a CH/A ↔ LL/A mismatch. The kext spoofs region-info in IORegistry (sufficient for end-side eligibility checks), but cannot change SEP hardware identity.

**Evidence pattern** (real CH/A Mac, macOS 27):
```
16:12:09  attestationsExist: clientCacheSize=40   ← has proofs
16:12:09  returning 2 attestations                ← sends them
16:12:09  didn't receive any inline attestations  ← SERVER REJECTS
16:12:17  Node substreams task finished successfully  ← computation runs
16:12:17  Ropes request finished successfully          ← computation succeeds
16:12:17  IncomingUserDataReader shutdown=32080         ← attestation layer fails, results not delivered
```

Computation (Ropes) runs fine — the PCC node processes the request. But the attestation layer around it rejects, so results can't be delivered back.

**This is a fundamental limitation** of the IORegistry-spoof approach for PCC. End-side models (Genmoji, Writing Tools basic features, summarization) work fine since they don't need attestation. Only PCC-dependent features (tone rewrite, Image Playground, Reframe) are affected on Chinese-market hardware.

## PCC Attestation Pool Reset (for Scenario A only)

When PCC logs show Code=32080 AND `attestationsExist: clientCacheSize=0`, perform a local pool reset. **Do NOT reset when the key signal is `didn't receive any inline attestations`** — it won't help.

Full recipe in [references/pcc-troubleshooting.md](references/pcc-troubleshooting.md).

Quick reset:

```bash
# 1. Find attestation store path
DIR="$(sudo lsof -c privatecloudcomputed -Fn 2>/dev/null | sed -n 's/^n//p' | grep -m1 -oE '.*/attestationstore_v3')"

# 2. Kill daemon FIRST (launchctl kill may not work — use pgrep)
PID="$(pgrep -f privatecloudcomputed)"
sudo kill -KILL "$PID"
# VERIFY the daemon is dead before deleting (ps aux | grep privatecloudcomputed)
# Otherwise you trigger libsqlite3 BUG when deleting files held open

# 3. Delete stale files
rm -f "$DIR"/db.sqlite* "$(dirname "$DIR")"/nodesReceived.log

# 4. Wait 15-30 min — daemon auto-restarts via XPC on next PCC request.
#    DO NOT TOUCH PCC during this window. Idle daemon builds attestations.
```

## Uninstall

```bash
cd /tmp/enableMacosAI
sudo ./install.sh uninstall
# Restart to revert region to CH/A
```
