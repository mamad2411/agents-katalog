---
name: semwright-audio-production
description: Use when an agent must synthesize, edit, render, analyze, validate, repair, save, reopen, or export professional audio through Semwright audio-domain, Faust, Ardour, and the native analysis provider.
---

# Semwright audio production

Use the live Semwright capability catalog. Do not invent DSP parameters, Ardour object IDs, paths, compiler flags, Lua, OSC packets, plugin code, or filesystem authority.

## Production loop

1. **DISCOVER** the audio providers and describe the exact Faust, analysis, or Ardour capability before execution.
2. **INSPECT** the current project/session and retain its revision. Treat native plugin state and incomplete routing as explicit fidelity limits.
3. **PLAN** with the shared Composition/audio-authoring contract when the task is more than one primitive operation. A plan is data, never authority.
4. **APPLY** only typed operations through the Broker. Mutations must be revision-bound; stale or ambiguous state is a stop condition.
5. **RENDER** deterministic synthesis, hash-pinned sample-backed graphs, or bounded polyphonic MIDI through Faust; or export a managed Ardour session through its native path. Never overwrite an existing artifact.
6. **MEASURE** the actual artifact. Distinguish sample peak/RMS from standards-based loudness and true peak; silence and insufficient windows may be UNKNOWN.
7. **VALIDATE** deterministic routing, ranges, channels, cues, delivery limits, artifact digests and declared postconditions.
8. **REPAIR** only bounded deterministic findings. If loudness and peak constraints conflict, report the conflict or request an explicitly authorized dynamics processor rather than oscillating gain.
9. **SAVE/REOPEN** Ardour candidates when persistence matters, and verify the protected source remained unchanged when save-as promises that boundary.
10. **REVERIFY** from fresh state and preserve receipts, source revisions, backend versions and artifact hashes.

Faust source is derived from typed synthesis data. Callers never provide arbitrary Faust source or compiler flags. Sample playback requires a hash-bound asset from the read-only audio-assets grant; polyphonic MIDI uses the pinned Faust allocator semantics and rejects ambiguous same-pitch overlap. Ardour deep editing uses a Semwright-owned fixed Lua adapter plus owner-pinned Ardour 8.4 utilities; values are argv, not code. Plugin mutation is limited to owner allowlist IDs and observed parameter identity. Live OSC is a separate best-effort surface and lack of acknowledgement is not proof of mutation.

Read only the focused reference needed for the current task:

- [assets and provenance](references/assets-and-provenance.md)
- [routing and units](references/routing-and-units.md)
- [synthesis and DSP](references/synthesis-and-dsp.md)
- [Ardour sessions](references/ardour-sessions.md)
- [analysis and repair](references/analysis-and-repair.md)
- [cues and recovery](references/cues-and-recovery.md)
