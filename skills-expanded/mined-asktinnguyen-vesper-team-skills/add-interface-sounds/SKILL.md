---
name: add-interface-sounds
description: Add lightweight, synthesized interaction sounds to websites and apps using Cuelume and the Web Audio API. Use when Codex needs to create, design, implement, audit, or refine sound feedback for buttons, navigation, toggles, favorites, success/error states, loading, reveals, carousels, or other UI interactions; include an accessible persisted sound preference and validate that sound remains subtle and optional.
---

# Add interface sounds

Use Cuelume as a small curated sound palette. Prefer its synthesized Web Audio cues over downloaded MP3/WAV assets unless the product explicitly needs branded music, voice, or realistic effects.

## Workflow

1. Inspect the existing interaction model and framework before editing.
2. Read [references/cuelume-api.md](references/cuelume-api.md) for the cue map and framework patterns.
3. Install `cuelume` with the project's existing package manager. Preserve its lockfile.
4. Create one client-side sound controller. Call `bind()` once after mount and restore the app-owned sound preference before normal use.
5. Add a visible sound on/off control with `aria-pressed`, a clear accessible name, and a persisted device-local preference.
6. Map sounds to meaning, not to every possible event:
   - use declarative attributes for common hover, press, release, and toggle feedback;
   - call `play()` only after meaningful outcomes such as a successful save, an error, a reveal, or content becoming ready;
   - keep high-frequency lists quiet and avoid hover sounds on dense card grids unless the user explicitly wants them.
7. Test keyboard, touch, pointer, reload persistence, and the muted state. Confirm the app still works when Web Audio or storage is unavailable.

## Product rules

- Keep sound optional. Never hide the mute control or make a user hunt through settings.
- Default to sound on only for playful or explicitly sound-forward products. For productivity, health, finance, or accessibility-sensitive products, default off unless the product already establishes otherwise.
- Never use sound as the only signal. Preserve visual text, state, focus, and error feedback.
- Avoid autoplay, background loops, music, speech, alarm-like cues, and rapid repeated sounds.
- Play outcome cues after the outcome is known. Do not play `success` before persistence or a network action succeeds.
- Respect the library's pointer-aware hover behavior instead of inventing touch hover handling.
- Store only the preference, not audio data. Treat blocked storage and unavailable audio as silent fallbacks.
- Use one palette consistently across the product. Do not mix Cuelume with unrelated UI click packs without a deliberate sound-design reason.

## Reusable asset

For React client apps, adapt [assets/react/cuelume-sound-provider.tsx](assets/react/cuelume-sound-provider.tsx). Keep product styling outside the shared controller. For non-React apps, follow the small vanilla pattern in the API reference.

## Validation

- Run the project's build and existing tests.
- Check that no server component imports browser-only behavior without a client boundary.
- Check that binding is idempotent and not repeated on every render.
- Check that turning sound off prevents future cues and survives a reload.
- Check that turning sound back on gives a single confirmation cue.
- Check that rapid pointer movement does not create a noisy cascade.
