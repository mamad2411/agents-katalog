---
name: validate-audiounit
description: Validate AudioUnit v2/v3 plugins (.component bundles and .appex app extensions) using Apple's auval tool. Use when user says "validate AU", "run auval", "test AudioUnit", "check the .component", "check the .appex", "validate AUv3", or needs to check AudioUnit compatibility. For .vst3 use validate-vst3; for .clap use validate-clap.
compatibility: macOS only. auval is included with Xcode command-line tools.
metadata:
  author: Oli Larkin
  version: 0.0.1
---

# AudioUnit Validation (auval)

## Plugin Install Locations

AudioUnits **must** be registered with the system for `auval` to find them — it does not accept a file path.

### AUv2 (.component)

| Location | Scope |
|----------|-------|
| `~/Library/Audio/Plug-Ins/Components/` | Current user only |
| `/Library/Audio/Plug-Ins/Components/` | All users (requires admin) |

After installing or rebuilding, force a rescan: `killall -9 AudioComponentRegistrar`

### AUv3 (.appex)

AUv3 AudioUnits are app extensions (`.appex`) embedded inside a host `.app` bundle (e.g., `MyApp.app/Contents/PlugIns/MyAU.appex`). The host app must be run at least once to register the extension with the system via `pluginkit`.

```bash
# Check if an AUv3 is registered (match by bundle ID)
pluginkit -m -v -p <bundle-id>

# List all registered AudioUnit extensions
pluginkit -m -v -A

# Manually register an appex
pluginkit -a <path-to-appex>

# Unregister an appex
pluginkit -r <path-to-appex>

# Dump full extension info for debugging
pluginkit -e -v -i <bundle-id>
```

After rebuilding, re-run the host app or use `pluginkit -a` to re-register the updated extension.

## Instructions

1. Register the plugin with the system:
   - **AUv2:** Install the `.component` in a standard Components location (see above)
   - **AUv3:** Run the host `.app` at least once, or manually register with `pluginkit -a <path-to-appex>`
2. Identify the plugin's AU type (`aufx`, `aumu`, etc.), four-character subtype, and manufacturer code
3. Force a rescan if the plugin was just built: `killall -9 AudioComponentRegistrar`
4. Run: `auval -v <type> <subtype> <manufacturer>` — this works the same for both AUv2 and AUv3 once registered
5. Check the final line — `* * * * * * * *` means all tests passed
6. If tests fail, see Common Issues below

## Basic Usage

```bash
# Validate an effect (aufx)
auval -v aufx <subtype> <manufacturer>

# Validate an instrument (aumu)
auval -v aumu <subtype> <manufacturer>

# Validate a MIDI-controlled effect (aumf)
auval -v aumf <subtype> <manufacturer>

# Validate a MIDI processor (aumi)
auval -v aumi <subtype> <manufacturer>
```

## Listing AudioUnits

```bash
# List all registered AudioUnits
auval -a

# List all AUs with their file locations
auval -al

# List AUs without instantiating them (faster)
auval -l

# List all effects
auval -s aufx

# List all instruments
auval -s aumu
```

## AudioUnit Types

| Type | Description | Example |
|------|-------------|---------|
| `aufx` | Effect | Gain, EQ, Reverb |
| `aumu` | Music Device (Instrument) | Synth, Sampler |
| `aumf` | Music Effect (MIDI-controlled) | Arpeggiator with audio |
| `aumi` | MIDI Processor | MIDI filter, transposer |
| `aufc` | Format Converter | Sample rate converter |
| `auou` | Output | Audio output |
| `aupn` | Panner | Surround panner |
| `augn` | Generator | Noise generator |

## Validation Options

```bash
# Basic open/initialize test only (fast, good for debugging)
auval -o -v aufx <subtype> <manufacturer>

# Run with stress test (multi-thread test for race conditions, default 600s)
auval -stress -v aufx <subtype> <manufacturer>

# Run stress test with custom duration (in simulated seconds)
auval -stress 120 -v aufx <subtype> <manufacturer>

# Run with real-time safety test (requires sudo, uses dtrace)
sudo auval -real-time-safety -v aufx <subtype> <manufacturer>

# Repeat validation N times (catches open/init bugs)
auval -r 5 -v aufx <subtype> <manufacturer>

# Stop on first error (useful for debugging)
auval -de -v aufx <subtype> <manufacturer>

# Stop on first warning (stricter)
auval -dw -v aufx <subtype> <manufacturer>

# Quiet mode (errors/warnings only)
auval -q -v aufx <subtype> <manufacturer>

# Quiet mode suppressing parameter/factory preset info
auval -qp -v aufx <subtype> <manufacturer>

# Wait after finish (for memory profiling with 'leaks' tool)
auval -w -v aufx <subtype> <manufacturer>

# Load AudioUnit out-of-process
auval -oop -v aufx <subtype> <manufacturer>

# Open as component (not plugin)
auval -comp -v aufx <subtype> <manufacturer>
```

## Strict Options

Strict options enforce checks that would otherwise only produce warnings. Use `-strict` to enable all strict checks — this should be used by default for thorough validation.

```bash
# Enable all strict checks (recommended)
auval -strict -v aufx <subtype> <manufacturer>

# Individual strict options:
# Enforce AudioUnitScheduleParameter output check (always enforced since Leopard)
auval -strict_SP -v aufx <subtype> <manufacturer>

# Enforce parameter default values fall between min and max
auval -strict_DefP -v aufx <subtype> <manufacturer>

# Require conformant kAudioUnitProperty_CPULoad implementation (if in use)
auval -strict_CPUL -v aufx <subtype> <manufacturer>
```

## Batch Validation

```bash
# Validate all AUs of a given type from one manufacturer
auval -vt aufx <manufacturer>

# Continue on error in batch/repeat mode (don't stop at first failure)
auval -c -vt aufx <manufacturer>

# Run commands from a file (one command per line)
auval -f /path/to/commands.txt
```

If no options are given, auval looks for a file called `auv-autorun.txt` in the launch directory or `/tmp/` and runs commands from it.

## Component ID Formats

Component IDs can be specified as 4-char codes or 8-digit hex values. These are equivalent:

```bash
auval -v aufx bpas appl
auval -v 61756678 62706173 6170706C
```

The two formats can be mixed freely.

## Return Codes

| Code | Meaning |
|------|---------|
| `0` | OK — all tests passed |
| `-1` | AU failed validation |
| `1` | General error |
| `2` | Fatal error |
| `4` | Unauthorized (open) |
| `5` | Unauthorized (init) |

## Memory Leak Testing

```bash
# Start auval with leak detection
export MallocStackLogging=1
auval -v aufx <subtype> <manufacturer> -w -q

# In another terminal, find the PID and check for leaks
ps axc | awk '{if ($5=="auvaltool") print $1}'
leaks <PID>
```

## AUv2 vs AUv3 Conflicts

AudioUnit v2 and v3 plugins are identified by their type+subtype+manufacturer code. If both formats are registered with the same codes, the system will prefer one (typically AUv3), which can cause confusion during development.

**Best Practice:** Use different subtypes for AUv2 and AUv3 during development. Most build systems (JUCE, iPlug2, iPlug3, etc.) provide separate configuration fields for AUv2 and AUv3 subtypes.

To temporarily remove an AUv3 so the AUv2 is used instead: `pluginkit -r <path-to-appex>`

## Force AU Rescan

```bash
# Kill the registration daemon to force rescan
killall -9 AudioComponentRegistrar

# Wait a moment, then list AUs
sleep 2
auval -a
```

## Common Issues

### AU Not Found
```
FATAL ERROR: didn't find the component
```
- Verify plugin is in a standard location (see Plugin Install Locations above)
- Rescan: `killall -9 AudioComponentRegistrar`
- Check Info.plist for correct type/subtype/manufacturer
- **AUv3:** Ensure the host app was run at least once, verify registration with `pluginkit -m -v -p <bundle-id>`, and re-register with `pluginkit -a <path-to-appex>` if needed

### Class Collision Warning
```
objc: Class XYZ is implemented in both...
```
- Each plugin must have unique Objective-C class names
- Use your build system's support for unique class name prefixes
