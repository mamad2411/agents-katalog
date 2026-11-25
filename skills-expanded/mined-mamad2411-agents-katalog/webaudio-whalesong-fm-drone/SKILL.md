---

name: webaudio-whalesong-fm-drone
description: Synthesize whale-song-like drones via low-frequency FM with slow pitch glides and amplitude swells in WebAudio.
category: algorithms
triggers:
  - webaudio whalesong fm drone
tags: [algorithms, webaudio, whalesong, drone]
version: 1.0.0
---

# webaudio-whalesong-fm-drone

For ambient "song" textures (whales, wind, resonant chambers), skip sample assets and build a two-operator FM voice: a carrier oscillator (40–200 Hz sine) modulated by a slow modulator (0.3–3 Hz) whose output feeds carrier.frequency via a GainNode. Layer a slow LFO on a master GainNode for amplitude swell, and route through a BiquadFilter (lowpass ~800 Hz) to tame harshness. The result is a few hundred bytes of code that reads as organic cetacean vocalization rather than a synth tone.

```js
const car = ctx.createOscillator(); car.frequency.value = 80;
const mod = ctx.createOscillator(); mod.frequency.value = 0.7;
const modGain = ctx.createGain(); modGain.gain.value = 30;
mod.connect(modGain).connect(car.frequency);
const amp = ctx.createGain(); amp.gain.setValueAtTime(0, t0);
amp.gain.linearRampToValueAtTime(0.4, t0 + 2);
amp.gain.linearRampToValueAtTime(0, t0 + 6);
car.connect(amp).connect(lowpass).connect(ctx.destination);
```

Stagger multiple voices with random detune (±5 Hz) and phase-offset start times so the chorus never aligns. Cap voice count (~4) and reuse nodes across calls; creating a new OscillatorNode per "song" is fine but schedule stop() to avoid leaks. This generalizes to any "living drone" ambience — foghorns, temple bells, engine hums — where pitched samples would bloat bundle size.
