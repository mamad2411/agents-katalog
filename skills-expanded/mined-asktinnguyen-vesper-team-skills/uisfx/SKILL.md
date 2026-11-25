---
name: uisfx
description: Add semantic, accessible interface sound effects with the uisfx npm package. Use when implementing or reviewing UI sound feedback, sound packs, one-shots, loops, audio preferences, or cue mapping in web, mobile, SaaS, media, and game interfaces.
license: MIT
metadata:
  source: https://uisfx.com
  agent_prompt: https://uisfx.com/agent-prompt.txt
  agent_guide: https://uisfx.com/docs/agent-guide.md
  package: uisfx@0.4.0 (verified 2026-08-14)
---

# UI SFX

Use UI SFX as a restrained semantic sound layer. Sound reinforces visible feedback; it never replaces text, state, focus, motion, haptics, or ARIA feedback.

## Source of truth

- Read `references/agent-prompt.txt` for the canonical implementation brief.
- Read `references/catalog.md` before choosing a pack or cue. Do not invent cue names.
- The live guide is https://uisfx.com/docs/agent-guide.md and the machine-readable catalog is https://uisfx.com/uisfx-catalog.json.
- The package is installed in the product being changed with `npm install uisfx`. Do not rely on a global npm install: global packages do not make `import 'uisfx'` resolve from arbitrary project dependency graphs.

## Workflow

1. Inspect the product's framework, client/server boundaries, shared controls, state management, async workflows, accessibility patterns, existing settings, audio, and tests before editing.
2. Compare the available packs against the product's purpose, audience, brand tone, visual and motion language, interaction density, and existing audio. Pick one coherent pack and briefly explain the fit. Do not ask the user to choose when the product context is sufficient.
3. Install the package with the project's existing package manager and preserve its lockfile.
4. Create one long-lived, client-only player. Keep it in the product's shared service/provider rather than constructing players in individual components.
5. Map real state changes to semantic cues. Add sound only where it improves confirmation, state awareness, spatial understanding, progress, or delight.
6. Add or reuse a clearly labelled, persistent sound preference and keep it optional.
7. Test the timing, lifecycle, accessibility, mute behavior, SSR safety, and production build. Report the chosen pack, action-to-cue map, changed files, preference behavior, loop cleanup, and verification.

## Player and browser lifecycle

For a browser app, use the package's Web Audio player once per application:

```ts
import { createUISFX } from 'uisfx'

const ui = createUISFX({
  pack: 'minimal',
  volume: 0.7,
  enabled: savedSoundPreference,
  preferences: { key: 'product:sound' },
})
```

- Never instantiate or play audio during SSR. Avoid duplicate players during remounts or React Strict Mode.
- Unlock Web Audio from a genuine pointer or keyboard gesture, before any `await`: call `await ui.unlock()` from that handler or synchronously start the first permitted play. Never autoplay on page load.
- Until audio is unlocked, suppress background and asynchronous cues rather than queueing stale feedback.
- `ui.play(...)` may return `null`; handle that safely.
- If the product owns an `AudioContext`, destroy the player first and then close that context during final app teardown. Use `await ui.destroy()` only when the app-level player is actually disposed.
- For native mobile, React Native, game engines, or environments without Web Audio, use `uisfx/sounds/<pack>/{cue}.mp3` or `.ogg` while preserving the same semantic and lifecycle rules.

## Semantic cue rules

Choose the cue for what happened, not what the control looks like. Usually use one cue per interaction; do not stack `press`, `select`, and `success` for one ordinary action.

Prefer meaningful transitions such as confirmed saves, validation outcomes, toggles, tabs, dialogs, committed destructive actions, undo/redo, drag-and-drop results, uploads, generation, recording, messages, media controls, purchases, milestones, and connection state.

Avoid sound for scrolling, passive layout changes, disabled controls, dense repeated lists, background refreshes, and routine hover. Use `hover` only on sparse, important fine-pointer targets; never use it for touch. If keyboard sonification is enabled, use the brief `typing` cue once per local text-entry `input` event at low volume. Throttle rapid seek, volume, hover, progress, and notification events, but do not throttle typing by default.

For async work, play `success` only after resolution and `error` only after failure. Play `delete` after deletion is committed. Choose toggle and selection cues from the resulting state.

Use `bindUISFX` data attributes only for simple one-shot DOM interactions. Use the imperative player for async outcomes, application state, loops, and lifecycle-sensitive behavior. Do not combine declarative binding and manual playback on the same element.

## Loops and cleanup

The loop cues are `loading`, `processing`, `recording`, `connecting`, `scanning`, and `streaming`.

```ts
const processing = ui.play('processing')

try {
  await runTask()
  processing?.stop()
  ui.play('complete')
} catch (error) {
  processing?.stop()
  ui.play('error')
  throw error
}
```

In real code, retain and clear each handle, make loop starts idempotent, and stop every loop on success, failure, cancellation, timeout, route change, component cleanup, mute/disable, and every `finally` path. Stop before playing an outcome. Use `ui.stopAll()` for global transitions such as logout. Never leave an invisible loop running.

## Preference and accessibility

- Add or reuse a clearly labelled sound on/off control with a persistent preference. Keep existing product preference storage; use local storage only as a fallback.
- Before disabling sound, stop active loops, clear retained handles, and call `ui.stopAll()` so mute is immediate. Apply changes with `ui.setEnabled()`, `ui.setVolume()`, and `ui.setPack()`.
- Keep visual, textual, focus, motion, haptic, and ARIA feedback intact. Sound must never be the only distinction between success, warning, and error.
- Do not interpret `prefers-reduced-motion` as an audio preference.
- Support mouse, touch, and keyboard activation without duplicate playback.

## Verification checklist

- Semantic mapping uses only names in `references/catalog.md` or the live catalog.
- Success/error cues occur after the real outcome, not on speculative clicks.
- Active loops stop on success, failure, cancellation, timeout, navigation, unmount, mute, and teardown.
- Unlocking is gesture-driven; there is no SSR audio or autoplay.
- Mute is accessible, persisted, immediate, and silent-safe when storage or Web Audio is unavailable.
- Pointer, touch, and keyboard paths do not double-play.
- Run the formatter, typecheck, relevant tests, and production build.
