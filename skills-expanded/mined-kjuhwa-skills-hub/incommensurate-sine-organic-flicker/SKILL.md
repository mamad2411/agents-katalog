---

name: incommensurate-sine-organic-flicker
description: Compose a natural-looking flicker/sway value by summing 2–3 sine waves whose frequencies are non-integer ratios so the pattern never visibly loops.
category: frontend
triggers:
  - incommensurate sine organic flicker
tags: [frontend, incommensurate, sine, organic, flicker]
version: 1.0.0
---

# incommensurate-sine-organic-flicker

In `17-inkwell-whale-atlas/app.js` `drawLantern`: `const flick = .7 + .3*Math.sin(ph*2.3) + .1*Math.sin(ph*5.1);`. The base (0.7) guarantees a non-zero floor, two sines at decreasing amplitude (0.3, 0.1) add increasing frequency detail, and the frequency multipliers (2.3, 5.1) are deliberately not integer ratios of each other — so the combined waveform has a practical period in the tens of thousands of frames rather than looping every few seconds.

The same idiom drives whale lateral motion (`Math.sin(w.ph*.3)*40*w.dir`) and paper-band drift (`Math.sin((x*.006)+drift*.8+(y*.002)+...)*amp`), where mixing position-dependent and time-dependent sine arguments spatially decorrelates adjacent elements. Per-element phase offsets seeded at spawn (`ph:R(0,6.28)`) complete the illusion — identical lanterns never flicker in sync.

Use for candlelight, CRT scan jitter, water shimmer, breathing UI pulses — any "alive but not choreographed" animation. The naive `0.5 + 0.5*Math.sin(t)` alternative looks mechanical because the viewer's eye tracks the 1Hz beat. Rule of thumb: two irrational-ratio sines + a non-zero baseline is the minimum; three buys organic-looking noise without the cost of a PRNG per frame.
