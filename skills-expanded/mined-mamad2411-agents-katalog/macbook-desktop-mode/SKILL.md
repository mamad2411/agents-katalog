---
name: macbook-desktop-mode
description: Configure a MacBook as an always-on-AC desktop workstation with USB device resilience, battery longevity, and self-healing audio device.
allowed-tools: Read, Bash, Write, Edit, Glob, Grep, AskUserQuestion, WebSearch
---

# MacBook Desktop Mode

A holistic configuration guide for running a MacBook as an always-on-AC desktop workstation. Solves two interconnected problems: USB devices (especially USB 1.1 audio) disappearing during sleep/wake cycles, and unnecessary battery degradation from constant charge cycling.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

- USB microphone or audio device disappears after sleep/wake
- Battery is cycling unnecessarily on a plugged-in Mac
- Setting up a MacBook as a permanent desktop workstation
- Configuring `pmset` for always-on-AC use
- Setting up a powered USB hub with `uhubctl` for software-controlled USB resets
- Enhancing the AudioDeviceMonitor Swift daemon with self-healing recovery

## Root Cause Diagnosis Framework

Before applying fixes, diagnose the specific failure mode. This framework was developed from empirical analysis of an Apple Silicon MacBook kept permanently on AC, where the device that kept dropping off the bus was a bus-powered USB 1.1 audio-class microphone with no serial number — the most fragile class of USB peripheral across sleep/wake, and so the worst case these fixes are tuned for. Identify your own device with the `ioreg` command below rather than by vendor/product ID; nothing here needs one.

### DarkWake Cycling

macOS performs frequent DarkWake (partial maintenance wake) cycles — typically every 15 minutes overnight. During DarkWake:

- CPU wakes for Power Nap, network keepalive, Siri
- USB bus is partially powered but devices aren't fully re-enumerated
- USB 1.1 Full Speed devices lack Link Power Management (LPM) and can't negotiate graceful resume
- After multiple cycles, the XHCI controller drops the device from the IO registry

**Diagnostic command** — check sleep/wake history:

```bash
pmset -g log | grep -E "Sleep |Wake |DarkWake" | tail -30
```

### USB 1.1 Device Limitations

USB 1.1 devices (12 Mbps, `USBSpeed = 1`) are the most fragile across sleep/wake:

- No Link Power Management protocol
- No USB selective suspend negotiation
- Often lack serial numbers (`iSerialNumber = 0`), making re-identification after bus reset unreliable

**Diagnostic command** — check device properties:

```bash
ioreg -r -c IOUSBHostDevice -l | grep -A 20 "DEVICE_NAME"
```

Key fields: `USBSpeed` (1=Full, 2=High, 3=Super), `iSerialNumber` (0 = no serial), `IOPowerManagement.DriverPowerState`.

### USB Handle Contention

Applications like Chrome hold direct USB user client handles (`AppleUSBHostDeviceUserClient`) for WebRTC/WebAudio. These stale handles prevent clean re-initialization after sleep.

**Diagnostic command** — check who has USB handles:

```bash
ioreg -r -c IOUSBHostDevice -l | grep -B5 "IOUserClientCreator"
```

### Battery Micro-Cycling

On an always-AC Mac with no charge limit, the battery cycles between the ML-predicted level and actual charge. DarkWake cycles consume power, causing repeated charge/discharge micro-cycles.

**Diagnostic command** — check daily charge range:

```bash
ioreg -r -c AppleSmartBattery -l | grep -E "DailyMinSoc|DailyMaxSoc|Temperature|CycleCount"
```

- `Temperature` is in centidegrees (divide by 100 for Celsius)
- `DailyMinSoc`/`DailyMaxSoc` show today's charge swing range

## Phase 1: Power Configuration for Desktop Mode

### 1.1 Set Charge Limit to 80%

**System Settings → Battery → Charging Optimization → "Limit to 80%"**

On Apple Silicon, once at the limit the Mac enters AC bypass mode — power flows directly from charger to system board. The battery sits electrically disconnected, eliminating both calendar aging and cycle aging.

### 1.2 Set sleep=0 on AC

For an always-on-AC desktop, system sleep creates more problems than it solves:

```bash
# Disable system sleep on AC only (battery settings unchanged)
sudo pmset -c sleep 0

# Verify
pmset -g custom | grep -A1 "AC Power" | grep sleep
```

**What this preserves:**

- Display sleep still works (`displaysleep=10` on AC)
- Battery sleep settings unchanged (`sleep=1` for travel)
- `ttyskeepawake=1` still honored

**What this eliminates:**

- DarkWake cycling (root cause of USB dropout)
- Battery micro-cycling during maintenance wakes
- Thermal cycling (repeated cold↔warm transitions)

**Cost:** ~5-8W idle draw on Apple Silicon. No fan spin. ~$5-8/year in electricity.

### 1.3 Verify Power Configuration

```bash
# Full power settings
pmset -g custom

# Battery health snapshot
ioreg -r -c AppleSmartBattery -l | grep -E "Temperature|CycleCount|DailyMinSoc|DailyMaxSoc|MaxCapacity|IsCharging"

# Active power assertions
pmset -g assertions
```

## Phase 2: Hardware Layer — Powered USB Hub

### 2.1 Why a Powered Hub

A powered USB hub creates a **USB session boundary**. The Mac's XHCI controller maintains a session with the hub (a robust USB 2.0+ device with serial number). The hub independently maintains sessions with connected devices. Sleep/wake only stresses the Mac↔Hub link.

Additionally, the hub enables **software-controlled USB port reset** via `uhubctl` — the equivalent of a physical unplug/replug without touching hardware.

### 2.2 Hub Selection Criteria

Requirements:

- **Externally powered** (not bus-powered) — must have its own power supply
- **uhubctl-compatible** chipset — supports per-port power switching
- **USB 2.0+ hub** with serial number for reliable re-identification

Compatible chipsets (from the uhubctl project):

- VIA VL805/VL812/VL817
- Realtek RTS5411
- Genesys Logic GL850G/GL3510

### 2.3 uhubctl Setup

```bash
# Install
brew install uhubctl

# List compatible hubs (must have powered hub connected)
uhubctl

# Cycle all ports (2-second off period)
uhubctl -a cycle -d 2

# Cycle specific port on specific hub
uhubctl -a cycle -p 1 -l 1-1 -d 2
```

## Phase 3: Software Layer — AudioDeviceMonitor Enhancement

The reference implementation is a Swift daemon (`AudioDeviceMonitorRunner.swift`) deployed as a macOS launchd KeepAlive agent. It combines:

1. **Priority enforcement** (original) — sets default input/output to highest-priority available device
2. **Device guardian** (v2) — state machine tracking, disappearance detection, recovery cascade
3. **Wake detection** — IOKit power notifications via `IORegisterForSystemPower`
4. **Heartbeat** — 60-second periodic check for silent drops
5. **Recovery cascade** — uhubctl port cycle → retry → Telegram notification

### 3.1 State Machine

```
                    ┌──────────┐
          ┌────────▶│ PRESENT  │◀──────────────┐
          │         └────┬─────┘               │
          │              │ device gone          │
          │              ▼                      │
          │     ┌──────────────┐               │
          │     │ DISAPPEARED  │               │
          │     │  (3s debounce)│               │
          │     └──────┬───────┘               │
          │            │ still missing          │
          │            ▼                        │
          │     ┌──────────────┐     found     │
          │     │  RECOVERING  │───────────────┘
          │     │ uhubctl cycle│
          │     └──────┬───────┘
          │            │ max attempts
          │            ▼
          │     ┌──────────────┐
          │     │     DEAD     │
          └─────│  (Telegram)  │
          replug└──────────────┘
```

### 3.2 Key Architecture Decisions

- **IOKit power callbacks** instead of `NSWorkspace` — no AppKit dependency, works in headless launchd daemons
- **IOKit message constants defined manually** — Swift can't import `iokit_common_msg()` C macros; values computed from `sys_iokit (0xe0000000) | message_code`
- **Synchronous uhubctl/curl calls** — acceptable because the main RunLoop queues CoreAudio callbacks during blocking; no events lost, just delayed by recovery time
- **Telegram via curl subprocess** — no library dependency; credentials loaded from a dotenv file at startup
- **Single-threaded via main queue** — all CoreAudio callbacks, heartbeat, and power notifications dispatch to `.main`; no locks needed

### 3.3 Build and Deploy

The daemon is a single-file Swift program compiled into a self-contained binary:

```bash
# Compile
swiftc -O -framework CoreAudio -framework IOKit \
    -o /path/to/output/audio-device-monitor \
    AudioDeviceMonitorRunner.swift

# Codesign for launchd (ad-hoc, no Apple Developer account needed)
codesign -s - -f -i com.yourorg.audio-device-monitor /path/to/output/audio-device-monitor
```

Deploy as a launchd agent (user-level, KeepAlive):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourorg.audio-device-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/output/audio-device-monitor</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>ProcessType</key>
    <string>Background</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>/Users/yourusername</string>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/logs/audio-device-monitor-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/logs/audio-device-monitor-stderr.log</string>
</dict>
</plist>
```

Load: `launchctl load ~/Library/LaunchAgents/com.yourorg.audio-device-monitor.plist`

### 3.4 Configuration (in Swift source)

Priority lists and guarded devices are defined as constants at the top of the Swift source:

1. `inputPriorities` / `outputPriorities` — ordered arrays, highest priority first
2. `guardedDevices` — array of `GuardedDevice(name:, isInput:)` for disappearance monitoring
3. Tuning constants: `heartbeatInterval` (60s), `disappearDebounce` (3s), `maxRecoveryAttempts` (3)
4. Notification credentials: loaded from a dotenv file (path configured in `loadCredentials()`)

After changes, recompile and restart the launchd agent.

## Phase 4: Verification and Monitoring

### 4.1 Battery Health Monitoring

```bash
# Quick battery snapshot
ioreg -r -c AppleSmartBattery -l | grep -E "Temperature|CycleCount|DailyMinSoc|DailyMaxSoc|MaxCapacity"

# Full power state
pmset -g batt
system_profiler SPPowerDataType | grep -E "Cycle|Condition|Maximum|Charging"
```

With the 80% charge limit set and `sleep=0` on AC:

- `DailyMinSoc` and `DailyMaxSoc` should converge (no swing)
- `Temperature` should stay under 3500 (35°C) at steady state
- `CycleCount` accumulation should slow dramatically

### 4.2 USB Device Health

```bash
# Current USB device tree
system_profiler SPUSBDataType

# IOKit details for a specific device
ioreg -r -c IOUSBHostDevice -l | grep -A 25 "DEVICE_NAME"

# Kernel USB assertions (shows which devices prevent sleep)
pmset -g assertions | grep USB
```

### 4.3 Audio Monitor Logs

```bash
# Tail live logs (adjust path to your log location)
tail -50 /path/to/logs/audio-device-monitor-stderr.log

# Key log patterns to watch for:
# "Starting v2 — device guardian mode"     → v2 features active
# "System woke — checking devices"         → wake detection working
# "ALERT: '<device>' disappeared"          → device dropout detected
# "recovered via uhubctl!"                 → automated recovery succeeded
# "recovery FAILED"                        → manual replug needed
```

## Anti-Patterns

| Anti-Pattern                             | Why It Fails                                                 | Correct Approach                                   |
| ---------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| Changing `powernap=0` to reduce DarkWake | Trades USB stability for missed iCloud sync, Find My, etc.   | Set `sleep=0` on AC — eliminates DarkWake entirely |
| Disabling Optimized Battery Charging     | Allows battery to charge to 100% — worse for longevity       | Set explicit 80% charge limit                      |
| Killing Chrome to release USB handles    | Whack-a-mole; any WebRTC app can grab handles                | Powered hub creates session boundary               |
| Polling `system_profiler` for USB status | Expensive subprocess, 2-3 second latency                     | CoreAudio property listeners are instant           |
| Using `NSWorkspace.didWakeNotification`  | Requires AppKit/NSApplication — won't work in launchd daemon | `IORegisterForSystemPower` callback                |
| Resetting USB via IOKit when device gone | Can't reset a device that's already dropped from IO registry | uhubctl power-cycles the physical port             |

## See Also

- **`kokoro-tts:realtime-audio-architecture`** — Complementary skill covering audio _playback_ patterns (PortAudio, GIL contention, jitter elimination, device hot-switching). This skill handles the system/USB layer; that one handles the application/playback layer.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Fix any script, reference, or dependency that no longer matches reality.
4. **Log it.** — Evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
