---
name: desktop-tune
description: Use for desktop stability or battery health when a macOS laptop or desktop is used as a mostly plugged-in workstation — always-plugged-in behavior, sleep/wake instability, USB device dropouts, audio device disappearance, display sleep issues, or battery charge limits.
---

# Desktop Tune

Tune a plugged-in macOS workstation for stable daily use without sacrificing portability. This skill uses macOS-specific tools (`pmset`, `system_profiler`, `ioreg`).

## Workflow

### Step 1: Collect Evidence

Run all diagnostic commands. **Completion**: every command returns output.

```bash
pmset -g custom
pmset -g assertions
pmset -g log | grep -E "Sleep |Wake |DarkWake" | tail -40
system_profiler SPPowerDataType
system_profiler SPUSBDataType
ioreg -r -c AppleSmartBattery -l | grep -E "CycleCount|MaxCapacity|Temperature|IsCharging"
```

For disappearing USB/audio devices, add:

```bash
system_profiler SPAudioDataType
ioreg -r -c IOUSBHostDevice -l | grep -A 20 "<device-name>"
```

### Step 2: Classify the Issue

Determine the primary category from the collected evidence:

- **Battery**: cycle count climbing while plugged in, charge limit questions, health degradation.
- **Sleep/wake**: DarkWake frequency, system sleep/wake instability, Power Nap issues. Do not assume every wake issue is USB — check power assertions and logs first.
- **USB/audio dropout**: devices disappearing after sleep. USB 1.1 and older audio devices are more vulnerable.

### Step 3: Apply the Safe Change Ladder

Apply the smallest reversible change that matches the issue, starting from the top:

1. **Built-in optimization first**: use macOS battery charge optimization or 80% limit when available. Do not change battery settings based on generic advice if the Mac already manages charging well.
2. **Hardware before software**: use a powered USB hub for fragile devices before writing recovery automation. Powered hubs are more reliable than bus-powered hubs for microphones and audio interfaces.
3. **Separate display sleep from system sleep**.
4. **AC-only power changes**: if the user wants always-on behavior, adjust only AC power settings — never disable sleep globally. Example:

   ```bash
   sudo pmset -c sleep 0
   pmset -g custom
   ```

   Rollback (use the user's previous value if it was not `1`):

   ```bash
   sudo pmset -c sleep 1
   ```

5. **Monitoring last**: add self-healing or daemon scripts only after the device failure is reproducible. Do not build a daemon before checking whether a powered hub or sleep setting fixes the issue.

### Step 4: Verify

Re-run the diagnostic commands from Step 1 and confirm the change had the intended effect.

## Hardware Reference

- USB 1.1 and older audio devices are more likely to drop during sleep/wake.
- Powered hubs are more reliable than bus-powered hubs for microphones and audio interfaces.
- Hub chipsets that support software port cycling can recover devices without unplugging them.

## Reporting

For each recommendation, state:

- Current evidence
- Change scope: battery, sleep, USB, audio, monitoring
- Risk to portability or power use
- Rollback command
- Verification command
