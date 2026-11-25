---
name: audio-verification
description: Measure synthesized Web Audio when implementing sound effects or diagnosing playback and sound-quality defects.
---

# Audio verification

An audio graph that compiles can still be silent, over-range, noisy, or abruptly
cut off. Render it to samples when that will answer the reported problem, then
exercise the actual app path for scheduling, lifecycle, and device behavior.

## Evidence boundary

Measurements can establish sample-level facts. They do not establish that a cue
is pleasant, that a person heard it, or that the browser and output device played
it correctly. Report those limits explicitly.

For a changed cue:

1. Render the real graph offline when practical. Prefer importing the production
   module; if you reproduce the graph in a probe, disclose that it may drift.
2. Measure the fields relevant to the symptom. Compare before and after under
   identical settings when a meaningful baseline exists.
3. Exercise the cue in the running app when the issue involves user gestures,
   overlapping voices, scheduling, context state, or device changes.
4. If the evidence cannot settle the complaint, report the result as a bounded
   measurement or non-reproduction and identify the needed listening check.

## Running the included probe

[`scripts/audio-probe.js`](scripts/audio-probe.js) is a classic script with no
imports. Evaluate it in a browser page using an available browser automation,
preview, test runner, or developer-console facility. It defines
`globalThis.AudioProbe`.

```js
const metrics = await AudioProbe.measure((ctx, destination) => {
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(0, 0);
  gain.gain.linearRampToValueAtTime(0.3, 0.02);
  gain.gain.exponentialRampToValueAtTime(0.0004, 0.4);
  oscillator.connect(gain).connect(destination);
  oscillator.start(0);
  oscillator.stop(0.5);
}, { seconds: 0.6 });

const comparison = await AudioProbe.compare(
  { before: buildOld, after: buildNew },
  { seconds: 0.6 },
);
```

`OfflineAudioContext` requires a browser-compatible Web Audio implementation.
Use what the project or host already provides. Installing a browser engine or a
Web Audio shim solely for a small check is optional and should be proportionate
to the task.

## Interpret the current metrics accurately

The helper intentionally uses inexpensive heuristics rather than a perceptual
audio model. Compare runs made with the same sample rate, duration, and options.

| Metric | What the helper computes | Safe interpretation |
|---|---|---|
| `silent` | Peak below `1e-6` | No meaningful samples appeared in this offline render. |
| `peak` | Largest absolute sample | Output above full scale may be limited or clipped later in the playback chain; the floating-point offline render itself does not prove audible clipping. |
| `clippedSamples` | Samples with magnitude `>= 0.999` | Count near the nominal full-scale boundary. It is a conservative warning, not proof that those samples were hard-clipped or audibly distorted. |
| `rms` | Full-render root mean square | Relative level/energy for otherwise comparable cues; not a loudness standard. |
| `flatness` | Geometric/arithmetic ratio over sampled Goertzel bands | Relative tonal-versus-noise-like character within the configured bands. Windowing, duration, and signal content affect it, so avoid universal thresholds. |
| `hissShare` | Share of sampled band energy above the configured cutoff | Relative high-frequency content, not proof of audible hiss. |
| `centroidHz` | Energy-weighted center of sampled bands | Relative brightness for comparable renders. |
| `onsetRatio` | Largest raw sample in the first millisecond after the 1%-of-peak crossing, divided by global peak | Abrupt-start heuristic. Oscillator frequency and phase affect it; it is not an amplitude-envelope measurement. |
| `attackMs` | Time from the first 1%-of-peak raw sample to the first 90%-of-peak raw sample | Raw-waveform rise heuristic. Do not apply a universal click threshold or compare signals with different pitch/phase as if it were an envelope. |
| `tailRms` | RMS over roughly 10 ms before the last sample above 1% of peak | Abrupt-ending heuristic. It does not measure the final render window or prove a release click. Inspect the waveform boundary when that distinction matters. |

For click/pop investigations, inspect or calculate a short-window amplitude
envelope and the discontinuity at the actual start/stop boundary in addition to
the included onset and tail heuristics. For clipping investigations, distinguish
samples that exceed nominal full scale from a waveform already flattened by a
limiter or conversion stage. Render the real overlap pattern when several cues
can play together.

## Common Web Audio checks

- Exponential ramps require positive endpoints; use a small positive floor and
  a linear fade when starting from zero.
- Parameter steps can create discontinuities. Schedule a short transition and
  guard non-finite values.
- A wide, low-Q bandpass can retain much of a noise source. Compare spectral
  measures and level together when narrowing it.
- Track active voices and confirm they return to zero. Exercise slow and rapid
  interaction in the app when concurrency or cleanup is part of the complaint.
- Confirm `AudioContext.state` when the cue fires. Autoplay policy may require a
  trusted user gesture to start or resume audio.
- Treat sleep and output-device changes as runtime cases. Recreate the context
  only when the app observes a stale/closed context or its supported device event
  indicates that recovery is needed.

Report measured numbers and the path exercised. Phrase conclusions at the same
level as the evidence: for example, “peak fell from 1.18 to 0.82 in the offline
render and the overlap probe completed,” rather than “the sound is fixed” when
no listening or real-device check occurred.
