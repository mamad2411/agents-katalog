---
name: logic-pro
description: "Automate Logic Pro MIDI with Scripter JavaScript, configure Audio Units, and troubleshoot CoreAudio or spatial-audio workflows."
category: music
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["logic-pro", "scripter-midi-fx", "audio-units", "coreaudio", "dolby-atmos", "apple-silicon-audio", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Apple Logic Pro 11 Music Production AI Skill Guide (Claude)

## Overview & Engine Architecture
Apple Logic Pro 11 is a professional digital audio workstation engineered exclusively for macOS and Apple Silicon. Logic Pro's architecture combines a 64-bit floating point summing engine, native **Audio Units (AUv2 / AUv3)** plugin hosting, the **Scripter MIDI FX JavaScript Engine**, **Dolby Atmos 3D Spatial Audio**, **Flex Time / Flex Pitch** monophonic and polyphonic formant correction, and **Session Players AI**. Claude operates as a Principal macOS Audio Architect and Logic Pro Specialist, specializing in **Scripter JavaScript MIDI FX plugin development**, **CoreAudio buffer & performance core load balancing**, **Audio Unit `auval` cache recovery**, and **AppleScript / Logic Remote OSC integration**.

### Logic Pro 11 Core Engine & Scripter Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Logic Pro 11 Architecture                   │
│                                                             │
│  Composition & Arranger Tier                                │
│  ├── Tracks Area & Live Loops Grid (Non-Linear Cell Matrix) │
│  ├── Piano Roll & Score Editor (Step Sequencer, MIDI Draw)  │
│  └── Session Players AI (Session Bassist, Keyboardist, Drum)│
│                                                             │
│  DSP & Spatial Audio Infrastructure                         │
│  ├── CoreAudio Multi-Threaded Summing (P-Core & E-Core Sched│
│  ├── Dolby Atmos 3D Object Bed & Binaural Spatial Panner    │
│  └── Flex Pitch & Polyphonic Formant Warping Engine         │
│                                                             │
│  Extensibility & Scripting Core                             │
│  ├── Scripter MIDI FX Engine (Embedded ECMAScript Runtime)  │
│  └── Audio Unit Plugin Architecture (AUv2 / AUv3 Sandboxing)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Logic Pro Scripter JavaScript Development**: Author custom MIDI FX scripts implementing event handlers (`HandleMIDI`, `ProcessMIDI`, `Reset`) and UI controls (`PluginParameters`) to transform MIDI data in real time.
2. **Apple Silicon CoreAudio Load Balancing**: Optimize Logic Pro's Multithreading settings (*Playback Tracks vs Playback & Live Tracks*) and allocate processing threads to Apple Silicon Performance (P) cores.
3. **Audio Unit Validation (`auvaltool`) Triage**: Remediate broken or crashing third-party Audio Units by forcing rescan or clearing `com.apple.audiounits.cache`.
4. **Spatial Audio Dolby Atmos Setup**: Configure 7.1.2 Surround Beds, 3D Object Tracks, and Binaural render modes for Apple Spatial Audio deliverables.

---

## Production JavaScript Automation: Custom Logic Pro Scripter MIDI FX Plugin

Paste this script into Logic Pro's built-in **Scripter** MIDI plug-in (Insert on MIDI FX slot):

```javascript
// ==============================================================================
// Logic Pro 11 Scripter MIDI FX: Intelligent Humanizer & Scale Quantizer
// Humanizes note velocity, introduces micro-timing delay, and snaps to Scale.
// ==============================================================================
var NeedsTimingInfo = true;

// 1. Define Plugin UI Controls
var PluginParameters = [
    {
        name: "Humanize Velocity",
        type: "linear",
        minValue: 0,
        maxValue: 40,
        numberOfSteps: 40,
        defaultValue: 15,
        unit: "vel"
    },
    {
        name: "Timing Jitter",
        type: "linear",
        minValue: 0,
        maxValue: 20,
        numberOfSteps: 20,
        defaultValue: 5,
        unit: "ms"
    },
    {
        name: "Scale Snap (D Minor)",
        type: "checkbox",
        defaultValue: 1
    }
];

// D Natural Minor Pitch Classes: D(2), E(4), F(5), G(7), A(9), Bb(10), C(0)
var D_MINOR_SCALE = [0, 2, 4, 5, 7, 9, 10];

function snapToScale(pitch) {
    var pitchClass = pitch % 12;
    var octave = Math.floor(pitch / 12);
    
    if (D_MINOR_SCALE.indexOf(pitchClass) !== -1) {
        return pitch; // Already in scale
    }
    // Snap to nearest scale tone
    return (octave * 12) + ((pitchClass + 1) % 12);
}

// 2. Handle Incoming MIDI Events
function HandleMIDI(event) {
    if (event instanceof NoteOn) {
        // Apply Scale Snapping
        if (GetParameter("Scale Snap (D Minor)") === 1) {
            event.pitch = snapToScale(event.pitch);
        }

        // Apply Velocity Humanization
        var maxVelOffset = GetParameter("Humanize Velocity");
        var velOffset = Math.floor((Math.random() * (maxVelOffset * 2)) - maxVelOffset);
        event.velocity = Math.min(127, Math.max(1, event.velocity + velOffset));

        // Apply Timing Jitter (Micro-delay in milliseconds)
        var jitterMs = Math.random() * GetParameter("Timing Jitter");
        event.sendAfterMilliseconds(jitterMs);
    } else {
        // Pass through NoteOff, CC, PitchBend, etc.
        event.send();
    }
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **"Audio engine was not able to process all data in time"** | I/O buffer too small for live input monitoring, or single core overloaded by serial plugin chain. | 1. In Preferences $\rightarrow$ Audio $\rightarrow$ Devices, increase **I/O Buffer Size** to `256` or `512`.<br>2. Set **Multithreading** to `Playback Tracks`.<br>3. Set **Processing Threads** to `Automatic` (all P-cores). |
| **Audio Unit Plugin Missing / Crashes on Validation** | AU validation failed in `auvaltool` or plugin cache corrupted. | 1. In terminal, clear cache: `rm -f ~/Library/Caches/AudioUnitCache/com.apple.audiounits.cache`.<br>2. In Logic Pro $\rightarrow$ Settings $\rightarrow$ **Plug-in Manager**, select plugin and click **Reset & Rescan Selection**. |
| **Bounce in Place Truncates Reverb/Delay Tails** | Default bounce settings render only selected region bounds without tail duration. | In Bounce Track in Place dialog, check **Include Audio Tail in File** or set tail duration to `5000ms`. |
| **Rosetta 2 High Overhead on M-Series Mac** | Logic Pro running under Rosetta or hosting x86_64 Intel plugins via translation bridge. | In Plugin Manager, identify non-native AUs and replace with Apple Silicon native versions. Ensure Logic Pro runs natively (Get Info $\rightarrow$ uncheck "Open using Rosetta"). |

---

## Command Line Syntax & Audio Unit Diagnostics

```bash
# 1. Inspect Audio Unit Validation Status via auvaltool
auval -v aufx comp Appl

# 2. Reset Corrupted macOS Audio Unit Cache
rm -f ~/Library/Caches/AudioUnitCache/com.apple.audiounits.cache

# 3. Read Logic Pro Preferences via defaults CLI
defaults read com.apple.logic10
```

### Essential File Locations
- **Logic Pro User Preferences**: `~/Library/Preferences/com.apple.logic10.plist`
- **Audio Units Cache**: `~/Library/Caches/AudioUnitCache/`
- **Scripter Presets**: `~/Music/Audio Music Apps/Plug-In Settings/Scripter/`

---

## Agent Operational Directive
> **MANDATORY**: For heavy mixing sessions on Apple Silicon Macs, configure Processing Threads to Automatic and Multithreading to "Playback Tracks" to prevent live input threads from monopolizing performance cores.
