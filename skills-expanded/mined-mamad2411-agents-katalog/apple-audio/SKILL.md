---
name: apple-audio
description: "Build real-time audio graphs, DSP, synthesis, and spatial audio on Apple platforms with AVAudioEngine, AudioToolbox, Core Audio, and Audio Unit (AUv3) extensions. Covers the engine graph (AVAudioEngine, AVAudioPlayerNode, AVAudioMixerNode, effect/EQ nodes, taps), real-time DSP and synthesis (AVAudioSourceNode, AVAudioSinkNode, render blocks, AVAudioPCMBuffer, AVAudioFormat), audio session and routing (AVAudioSession categories/modes, interruptions, route changes, ports), spatial/3D audio (AVAudioEnvironmentNode, PHASE), MIDI (CoreMIDI, AVAudioUnitSampler/MIDIInstrument), and Audio Unit extensions (AUv3, AUAudioUnit, internal render block). Use when building a synthesizer, audio effect, DAW feature, real-time mixer, metering/visualizer, voice processor, spatial audio scene, MIDI instrument, or AUv3 plug-in. Does NOT cover simple file playback/recording or video (use apple-media), on-device ML/speech (use apple-on-device-ai), or SwiftUI layout (use swiftui-expert-skill)."
---

# Apple Audio (AVAudioEngine, Core Audio, Audio Units)

Guide for real-time audio: building engine graphs, doing DSP and synthesis,
managing the audio session, rendering spatial audio, handling MIDI, and shipping
Audio Unit (AUv3) extensions on iOS, iPadOS, macOS, and tvOS.

## Contents

- [Framework Selection Router](#framework-selection-router)
- [Audio Session First (iOS)](#audio-session-first-ios)
- [Engine Graph Overview (AVAudioEngine)](#engine-graph-overview-avaudioengine)
- [Buffers & Formats](#buffers--formats)
- [Real-Time DSP & Synthesis](#real-time-dsp--synthesis)
- [Metering & Taps](#metering--taps)
- [Spatial Audio](#spatial-audio)
- [MIDI](#midi)
- [Audio Unit Extensions (AUv3)](#audio-unit-extensions-auv3)
- [The Real-Time Thread Rules (Critical)](#the-real-time-thread-rules-critical)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Framework Selection Router

| Goal | API |
|---|---|
| Mix, route, and apply effects to live audio | `AVAudioEngine` graph |
| Schedule and play buffers/segments with sample accuracy | `AVAudioPlayerNode` |
| Generate audio in code (synth, procedural, custom DSP) | `AVAudioSourceNode` (render block) |
| Tap raw audio from a node (metering, analysis, recording) | `installTap(onBus:)` |
| Pull audio out of the graph manually (offline/render) | `AVAudioSinkNode` / manual rendering mode |
| Apply built-in effects (reverb, delay, EQ, distortion) | `AVAudioUnitEffect` subclasses |
| 3D / positional audio | `AVAudioEnvironmentNode` or PHASE |
| Play MIDI / sampled instruments | `AVAudioUnitSampler`, CoreMIDI |
| Ship a reusable effect/instrument plug-in | Audio Unit v3 (`AUAudioUnit`) extension |
| Lowest-level/legacy real-time callback | AudioToolbox `AudioUnit` / `AUGraph` (legacy) |
| Just play a file or record to a file | **Use `apple-media`** (`AVAudioPlayer` / `AVAudioRecorder`) |

Decision rules:
- **`AVAudioEngine` is the default** for anything real-time, mixed, or processed.
  Reach below it (AudioToolbox/Core Audio) only for legacy code or constraints
  the engine cannot meet.
- For non-real-time "play this file" or "record to this file," stay in
  `apple-media` with `AVAudioPlayer`/`AVAudioRecorder` -- don't spin up an engine.
- Use **AUv3** (not the deprecated AUv2/Component Manager) for plug-ins.

## Audio Session First (iOS)

On iOS/iPadOS/tvOS, configure `AVAudioSession` **before** starting the engine, or
routing, sample rate, and interruption behavior will be wrong.

```swift
import AVFAudio

let session = AVAudioSession.sharedInstance()
try session.setCategory(.playAndRecord,
                        mode: .measurement,            // low-latency, flat response
                        options: [.defaultToSpeaker, .allowBluetoothA2DP])
try session.setPreferredSampleRate(48_000)
try session.setPreferredIOBufferDuration(0.005)        // ~5 ms for low latency
try session.setActive(true)
```

Rules:
- Pick the **category** for capability (`.playback`, `.record`, `.playAndRecord`,
  `.ambient`) and the **mode** for behavior (`.default`, `.measurement`,
  `.voiceChat`, `.spokenAudio`, `.videoRecording`).
- `setPreferredIOBufferDuration` is a *request*; read back the **actual**
  `ioBufferDuration` and `sampleRate` after activation and adapt.
- Handle `AVAudioSession.interruptionNotification`: the engine **stops** on
  interruption -- pause, and restart on `.ended` with `.shouldResume`.
- Handle `AVAudioSession.routeChangeNotification`: a new route can change the
  sample rate; rebuild/reconfigure if `reason` is `.newDeviceAvailable` or
  `.oldDeviceUnavailable` (e.g., unplugged headphones -> pause, don't blast the
  speaker).
- macOS has no `AVAudioSession`; manage devices via Core Audio / the engine's
  `inputNode`/`outputNode` instead.

See [references/audio-session.md](references/audio-session.md) for categories,
modes, interruption/route handling, and latency tuning.

## Engine Graph Overview (AVAudioEngine)

The engine is a graph of **nodes** connected by **buses**. Audio flows from source
nodes through processing nodes to the output node.

```swift
import AVFAudio

let engine = AVAudioEngine()
let player = AVAudioPlayerNode()
let reverb = AVAudioUnitReverb()
reverb.loadFactoryPreset(.largeHall)
reverb.wetDryMix = 30

engine.attach(player)
engine.attach(reverb)

let format = engine.mainMixerNode.outputFormat(forBus: 0)
engine.connect(player, to: reverb, format: format)
engine.connect(reverb, to: engine.mainMixerNode, format: format)

engine.prepare()
try engine.start()

player.scheduleBuffer(buffer, at: nil, options: .loops)
player.play()
```

Key rules:
- `attach(_:)` every node **before** connecting it.
- Match formats across a connection, or pass an explicit `AVAudioFormat`. A
  mismatch is the most common reason audio is silent or distorted.
- `engine.mainMixerNode` and `engine.outputNode` are created lazily -- touching
  them instantiates them.
- Call `engine.prepare()` then `try engine.start()`; wrap in do/catch.
- Reconnecting nodes while running is allowed but can glitch -- pause heavy
  reconfiguration where possible.
- Accessing `engine.inputNode` activates the microphone (and needs
  `NSMicrophoneUsageDescription` + session permission -- see `apple-media`).

See [references/avaudioengine.md](references/avaudioengine.md) for player
scheduling, effect chains, sub-mixers, manual rendering, and reset/restart.

## Buffers & Formats

`AVAudioFormat` describes sample rate, channel count, and sample layout;
`AVAudioPCMBuffer` holds the samples.

```swift
let format = AVAudioFormat(standardFormatWithSampleRate: 48_000, channels: 2)!
let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: 1024)!
buffer.frameLength = 1024

// Float (deinterleaved) channel data:
let left  = buffer.floatChannelData![0]
let right = buffer.floatChannelData![1]
for frame in 0..<Int(buffer.frameLength) {
    left[frame]  = 0
    right[frame] = 0
}
```

Rules:
- Prefer **`.pcmFormatFloat32`, deinterleaved** for processing (the engine's
  native working format). Convert to/from integer/interleaved only at edges.
- Use `AVAudioConverter` for sample-rate or format conversion; never resample by
  hand unless you know the DSP.
- `frameCapacity` is allocation size; `frameLength` is how many frames are valid
  -- set it after filling.

## Real-Time DSP & Synthesis

Generate or process samples in a render block with `AVAudioSourceNode`.

```swift
var phase: Float = 0
let sampleRate: Float = 48_000
let frequency: Float = 440
let twoPi = 2 * Float.pi

let source = AVAudioSourceNode { _, _, frameCount, audioBufferList -> OSStatus in
    let abl = UnsafeMutableAudioBufferListPointer(audioBufferList)
    let increment = twoPi * frequency / sampleRate
    for frame in 0..<Int(frameCount) {
        let value = sin(phase)
        phase += increment
        if phase >= twoPi { phase -= twoPi }
        for buffer in abl {
            let ptr = buffer.mData!.assumingMemoryBound(to: Float.self)
            ptr[frame] = value
        }
    }
    return noErr
}

engine.attach(source)
engine.connect(source, to: engine.mainMixerNode,
               format: AVAudioFormat(standardFormatWithSampleRate: 48_000, channels: 1))
```

The render block runs on the **real-time audio thread**. Obey
[the real-time rules](#the-real-time-thread-rules-critical): no allocation, no
locks, no Swift runtime calls that can block.

See [references/realtime-dsp.md](references/realtime-dsp.md) for oscillators,
envelopes, lock-free parameter passing, `AVAudioSinkNode`, and using vDSP/Accelerate.

## Metering & Taps

Tap a node to observe audio (levels, FFT, waveform, recording) without breaking
the chain.

```swift
engine.mainMixerNode.installTap(onBus: 0, bufferSize: 1024,
                                format: engine.mainMixerNode.outputFormat(forBus: 0)) { buffer, time in
    // Compute RMS / peak here; this runs on a real-time-ish thread.
    // Hop to main only to publish UI values.
}
// Remove when done:
engine.mainMixerNode.removeTap(onBus: 0)
```

Rules:
- One tap per bus. Remove it before reconfiguring or stopping.
- Do **not** update UI directly from the tap; compute, then dispatch a small
  scalar to the main actor.
- For spectrum analysis use Accelerate's `vDSP`/`vDSP_DFT` on the tapped buffer.

## Spatial Audio

Two paths:
- **`AVAudioEnvironmentNode`** -- positional mixing inside `AVAudioEngine`. Set
  each source node's `AVAudio3DMixing` position; set the listener position and
  orientation on the environment node. Choose a `renderingAlgorithm`
  (`.HRTF`/`.HRTFHQ` for headphones).
- **PHASE** (`Physical Audio Spatialization Engine`) -- higher-level engine for
  games/AR with geometry, occlusion, reverb presets, and dynamic events.

See [references/spatial-audio.md](references/spatial-audio.md) for environment
setup, 3D positioning, head tracking, and choosing PHASE vs `AVAudioEngine`.

## MIDI

- Play sampled instruments with `AVAudioUnitSampler` (load a SoundFont/`.aupreset`,
  then `startNote(_:withVelocity:onChannel:)`).
- Send/receive external MIDI with **CoreMIDI** (`MIDIClientCreateWithBlock`,
  input/output ports, `MIDIEventList` on modern OSes).
- Sequence with `AVAudioSequencer` driving the engine.

See [references/midi.md](references/midi.md) for CoreMIDI setup, the modern
`MIDIEventList` API, and sampler/sequencer wiring.

## Audio Unit Extensions (AUv3)

Ship reusable effects/instruments as an **App Extension** hosting an
`AUAudioUnit` subclass.

- Implement `internalRenderBlock` (the real-time DSP) -- it must be real-time
  safe.
- Expose parameters via an `AUParameterTree`; host automation reads/writes them.
- Declare the component type in the extension's `Info.plist`
  (`aufx` effect, `aumu` instrument, `aumf` music effect).
- Test by loading in a host (GarageBand, AUM, Logic) and with `auval`.

See [references/auv3-extensions.md](references/auv3-extensions.md) for the
extension target, render block, parameter tree, and factory presets.

## The Real-Time Thread Rules (Critical)

Render blocks, source/sink callbacks, AUv3 `internalRenderBlock`, and tap blocks
run on a **priority real-time thread**. Blocking it causes glitches/dropouts.
Inside these blocks you must **NOT**:

- Allocate memory (`malloc`, array growth, `String`, boxing).
- Take locks (`os_unfair_lock` `lock`, mutexes, `@synchronized`, Swift actors).
- Call ObjC/Swift methods that may allocate or use ARC retain/release on new
  objects, throw, or bridge.
- Do file/network I/O, logging (`print`/`os_log` in hot paths), or `DispatchQueue`
  work.

Instead:
- Pre-allocate all buffers and state outside the block.
- Pass parameter changes in lock-free (atomics, a single-producer ring buffer, or
  `os_unfair_lock` with **`trylock`** only).
- Keep the block branch-light; use Accelerate (`vDSP`) for vector math.
- Capture only value types / pre-retained references; avoid creating new closures
  per render.

See [references/realtime-dsp.md](references/realtime-dsp.md) for safe
parameter-passing patterns.

## Common Mistakes

- Starting the engine before configuring `AVAudioSession` -> wrong sample rate /
  no input.
- Format mismatch on a `connect(_:to:format:)` -> silence or distortion.
- Allocating, locking, or logging inside a render/tap block -> dropouts.
- Forgetting to `attach()` a node before connecting it.
- Leaving a tap installed across reconfiguration -> crash or stale data.
- Updating UI directly from a tap/render block instead of hopping to main.
- Ignoring interruption/route-change notifications -> dead audio after a call or
  unplugged headphones.
- Touching `engine.inputNode` without mic permission + usage string.
- Treating `setPreferredIOBufferDuration`/`setPreferredSampleRate` as guaranteed
  instead of reading back the actual values.
- Using deprecated AUv2/`AUGraph` for new plug-ins instead of AUv3.

## Review Checklist

- [ ] `AVAudioSession` category/mode/sample-rate/buffer set before engine start;
      actual values read back.
- [ ] Interruption and route-change notifications handled.
- [ ] All nodes `attach()`-ed before `connect()`; formats matched.
- [ ] Engine started in do/catch; `prepare()` called.
- [ ] Render/source/sink/AUv3/tap blocks are **real-time safe** (no alloc, locks,
      I/O, logging).
- [ ] Parameters cross into render blocks lock-free (atomics/ring buffer).
- [ ] Taps removed before reconfigure/stop; UI updates hop to main.
- [ ] Mic input gated behind permission + `NSMicrophoneUsageDescription`.
- [ ] Plug-ins target AUv3 (`AUAudioUnit`), validated with `auval`.
- [ ] Format conversion uses `AVAudioConverter`, not hand-rolled resampling.

## References

- [references/audio-session.md](references/audio-session.md) -- categories, modes, interruptions, route changes, latency tuning.
- [references/avaudioengine.md](references/avaudioengine.md) -- graph construction, player scheduling, effects, sub-mixers, manual rendering.
- [references/realtime-dsp.md](references/realtime-dsp.md) -- source/sink nodes, oscillators/envelopes, lock-free params, vDSP/Accelerate.
- [references/spatial-audio.md](references/spatial-audio.md) -- AVAudioEnvironmentNode 3D mixing, head tracking, PHASE vs engine.
- [references/midi.md](references/midi.md) -- CoreMIDI, MIDIEventList, AVAudioUnitSampler, AVAudioSequencer.
- [references/auv3-extensions.md](references/auv3-extensions.md) -- AUv3 extension target, internalRenderBlock, AUParameterTree, presets.

Apple documentation:
- [AVFAudio / AVAudioEngine](https://developer.apple.com/documentation/avfaudio)
- [Audio Toolbox](https://developer.apple.com/documentation/audiotoolbox)
- [Core Audio](https://developer.apple.com/documentation/coreaudio)
- [Core MIDI](https://developer.apple.com/documentation/coremidi)
- [PHASE](https://developer.apple.com/documentation/phase)
- [Audio Unit v3](https://developer.apple.com/documentation/audiotoolbox/audio_unit_v3_plug-ins)
