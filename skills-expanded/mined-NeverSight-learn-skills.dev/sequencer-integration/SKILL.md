---
name: sequencer-integration
description: Production-ready guidance for app developers and coding agents to integrate and operate @kzkymur/sequencer in JavaScript/TypeScript apps. Use when tasks mention timelines, sequencing, scheduled callbacks, canvas timeline views, or the @kzkymur/sequencer library. Covers safe defaults, error guards, and Queue vs Independent modes.
---

Purpose

- Help an application developer and their coding agent integrate and use @kzkymur/sequencer effectively.
- Provide minimal, reliable steps with links to focused references.

When To Use

- Building animations, audio cues, game or UI events, or any timed workflow.
- Needing linear (serial) or overlapping (parallel) event execution with millisecond control.

Quick Workflow

1) Choose Mode
- Queue (class `Sequencer`): run fragments strictly in order.
- Independent (class `IndependentSequencer`): run fragments by start time; multiple can overlap.

2) Define Fragments
- Queue: `new Fragment(name, durationMs, callback?)`.
- Independent: `new IndependentFragment(name, durationMs, startMs, callback?)`.
- Modular: `new CustomFragment(name, startMs)` then `addFragment(...)` with independent/custom fragments; duration is computed; callback cannot be set directly.

3) Initialize
- Queue: `const seq = new Sequencer(pitchMs, speed=1.0, loop=false, useUniversalWorker=false)`.
- Independent: `const seq = new IndependentSequencer(pitchMs, speed=1.0, loop=false)`.
- Pitch is the tick interval; smaller is smoother but costlier. `useUniversalWorker=true` improves timer precision.

4) Compose
- `push(fragment)` to append.
- `insert(index, fragment)` for Queue only (throws on Independent).
- `remove(fragment)` by identity.

5) Control
- `await seq.play(delayMs=0)`; throws if already playing or delay < 0.
- `seq.stop(delayMs=0)`; throws if not playing or delay < 0.
- `await seq.waitCompleted()` to await natural end (must be playing).
- `await seq.replay(delayMs=0)`; requires not playing; resets time to 0.

6) Visualize (optional)
- `seq.renderToCanvas(ctx, { width?, height?, activeColor?, inactiveColor?, timeIndicatorColor?, onFragmentClick? })`.

Safety & Error Guards (agent-minded)

- Validate inputs before calling:
  - `setPitch(p > 0)`, `setSpeed(s > 0)`; non-positive or NaN throws.
  - `play/stop(delay >= 0)`; negative or NaN throws.
  - `insert(0..fragments.length)`; out-of-range throws.
  - Duplicates: pushing a fragment with an existing `id` throws.
- Independent mode: `insert(...)` always throws (unsupported).
- CustomFragment: cannot set callback; name must be non-empty; start must be ≥ 0.

Handy Getters

- `getFragments()` returns a copy of current fragments.
- `getCurrentTime()` current elapsed ms.
- `getPitch()`, `setPitch(...)`.
- `setSpeed(...)`, `setLoopFlag(...)`, `isLooping()`.

Open These References When Needed

- `references/quick-start.md` – install + minimal setup.
- `references/api.md` – precise method signatures and invariants.
- `references/patterns.md` – common patterns (UI, audio, games, tasks).
- `references/testing.md` – unit/integration test scaffolds.
- `references/troubleshooting.md` – known errors and fixes.

Notes For Coding Agents

- Prefer creating fragments once and reusing via `.copy()` when repeating patterns.
- Await `waitCompleted()` when callers expect completion before proceeding.
- For canvas, ensure `totalDuration > 0` before rendering to avoid divide-by-zero visuals.
- `onFragmentClick` is hit-tested against the most recent render result; keep a render loop running if layout changes over time.
- For high precision timelines, set `useUniversalWorker=true` (Queue mode) and avoid heavy work in callbacks.

References

- See the skill-creator guidance in `.agents/skills/skill-creator/` for structure and progressive disclosure patterns.
