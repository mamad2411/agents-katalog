# Audio Subsystem

## Purpose
Implement glitch-free positional 3D audio: DSP mixing graphs, HRTF/spatialization, distance attenuation, occlusion, streaming playback, bus architecture, and underrun-proof scheduling within a strict latency budget.

## Use when
- Implementing positional 3D audio, listener models, attenuation curves, or occlusion/obstruction.
- Designing the DSP mixing graph: buses, sends, effects chain order, headroom, and clipping policy.
- Adding streaming playback (music, dialogue) with seamless looping and gapless transitions.
- Auditing audio latency, buffer underruns, sample-rate conversion, or clipping distortion.

## Do not use when
- Authoring music, SFX content, or voice recordings rather than the playback engine.
- Tuning graphics frame pacing without audio involvement (use `game-runtime`).
- Implementing networked voice chat signaling rather than local mixing (use `network-security` for transport).

## Required context
- Audio asset inventory: sample rates, channel layouts, and 3D positional requirements.
- DSP graph requirements: buses, effects chain, occlusion model, and latency ceiling (ms).
- Target output devices and platform mixer constraints.

## Procedure
1. **Fix the Mix Contract**: Define sample rate (48 kHz), buffer size (e.g., 256 frames ≈ 5.3 ms), bus layout (master/music/sfx/dialogue/voice), and total latency ceiling (e.g., ≤ 40 ms input-to-output). All scheduling derives from these numbers.
2. **Build the DSP Graph**: Route sources → submix buses → master with explicit effect order (e.g., source EQ → occlusion low-pass → reverb send → bus compressor → limiter). Keep ≥ 6 dB headroom per bus; only the master limiter touches 0 dBFS.
3. **Spatialize Correctly**: Apply distance attenuation (inverse-square with clamped near/far fields), HRTF or panning for direction, and raycast-based occlusion (low-pass + gain cut, e.g., −12 dB fully occluded). Doppler only when relative velocity is physically meaningful.
4. **Stream Without Gaps**: Decode compressed streams (Opus/Vorbis) on a background thread into a lock-free ring buffer sized ≥ 3× the audio callback period. Pre-buffer before start; crossfade loop points over ≥ 10 ms to avoid clicks.
5. **Schedule Underrun-Proof**: The audio callback never allocates, locks, or does I/O — it only drains pre-mixed buffers. Voice stealing uses lowest-priority-oldest policy with a configurable polyphony cap (e.g., 64 voices).
6. **Verify**: Run `scripts/verify.sh`. Prove zero underruns over a 10-minute soak with 64 concurrent voices, attenuation/occlusion spot-checks against expected dB tables, and gapless loop spectral continuity.

## Decision rules
- **Callback Purity**: No allocation, locks, syscalls, or file I/O inside the real-time audio callback — ever.
- **Headroom Discipline**: Individual buses never exceed −6 dBFS peak; only the master limiter may approach 0 dBFS.
- **Occlusion Is Audible**: Any geometry between source and listener must produce measurable attenuation; silent occlusion is a bug.
- **Click-Free Guarantee**: All starts, stops, loop wraps, and parameter changes are ramped (≥ 5 ms) to prevent discontinuities.

## Evidence required
- 10-minute soak log with zero underruns at full polyphony.
- Attenuation/occlusion spot-check table (expected vs measured dB).
- Loop-continuity and voice-stealing test results.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Positional 3D audio implementation with distance attenuation and occlusion.
- DSP mixing graph with clipping-free headroom and streaming playback.
- Latency and underrun benchmark evidence.

## Stop conditions
- Positional mix verified glitch-free within latency budget on target devices.
- Soak test shows zero underruns and zero clipping events.
- Token budget exhausted.

## Escalation rules
- Escalate to lead architect if the platform mixer floor latency exceeds the design ceiling (requires design tradeoff, not code tuning).
- Escalate immediately on audible corruption that reproduces across devices (likely DSP graph or resampling defect).
