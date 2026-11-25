---
name: soundbox-sound-pass
description: Do a full "sound pass" on a project — read the code/design of a game, app, video or prototype, derive the list of sound events it needs, generate every one through the Soundbox MCP server, drop the files into the project and wire them up. Use when the user says "add sound to my game", "it needs SFX", "do an audio pass", "make all the sounds for this", or hands you a project with silent interactions.
---

# Soundbox: sound pass over a whole project

A sound pass is a batch job with judgement: find every moment that should make a
sound, decide what it should sound like, generate it, and integrate it. Do it in
that order — inventory before generation — so the set is coherent and the user
can veto items before minutes of GPU time are spent.

Requires the `soundbox-sfx` skill's rules for prompting and tool use; this skill
is about the *process* around it.

## 1. Inventory

Read the project (routes, components, game states, event handlers, animation
triggers, timeline). Produce a table and show it to the user before generating:

| id | trigger (where in code) | sound (prompt) | dur | kind | variations |
|---|---|---|---|---|---|
| ui_confirm | `Button onClick` primary | soft UI confirmation blip, two rising tones, clean | 0.6 | one-shot | 1 |
| step_gravel | `Player.move` on gravel tiles | single footstep on gravel, close, dry | 0.8 | set | 4 |
| amb_forest | `Level1.mount` | forest ambience, wind in leaves, distant birds, steady | 15 | loop | 1 |

Rules of thumb:
- **Kinds:** `one-shot` (plays once), `set` (random pick per trigger — footsteps,
  hits, coins), `loop` (ambience/model — ask for a steady, even prompt).
- Keep the palette small and consistent: one material vocabulary, one
  "space" per scene. Twelve good sounds beat forty mismatched ones.
- Skip anything that would need speech or music; note it as out of scope.
- If the project already has an `assets/audio` or similar directory, reuse its
  naming convention.

Ask the user to approve/edit the table (or proceed if they said "just do it").

## 2. Pre-flight

- `soundbox.list_models` → pick the loaded model; flag `commercial_use` if
  the project looks commercial.
- `soundbox.list_sounds(q=…)` for anything generic (`click`, `whoosh`) — reuse.

## 3. Generate

Call `soundbox.generate` per row, in order, `tags=[<project-name>, <kind>]`.
Sets: `variations=N`. Loops: ask for `steady`, `even`, `no events` in the prompt
so the loop point isn't obvious. Report progress every few sounds — generation
takes seconds to a minute each.

Listen-by-proxy: you can't hear results, so check `duration_s` matches intent
and re-run anything the model cut short. If a prompt errors, adjust per
`soundbox-sfx` and retry once; then move on and list it as "needs a manual take".

## 4. Integrate

- Copy each WAV into the project (`assets/sfx/<id>[_<n>].wav`), converting to
  the format the stack wants (`ffmpeg -i in.wav -codec:a libvorbis out.ogg` for
  web/Godot; keep WAV for Unity/Unreal).
- Write a manifest the code can consume:

```json
{
  "ui_confirm": { "files": ["sfx/ui_confirm.wav"], "kind": "one-shot", "gain": 0.8 },
  "step_gravel": { "files": ["sfx/step_gravel_1.wav", "sfx/step_gravel_2.wav"], "kind": "set" },
  "amb_forest":  { "files": ["sfx/amb_forest.wav"], "kind": "loop", "gain": 0.4 }
}
```

- Wire the triggers you inventoried. Prefer a tiny `playSfx(id)` helper over
  scattering file paths through the code. Sets pick randomly; loops start on
  scene enter and stop on exit; respect any existing mute/volume setting.
- Sensible default gains: UI 0.6–0.8, foley 0.8–1.0, ambience 0.3–0.5.

## 5. Hand-off

Give the user: the final table with file paths, model + licence used, what was
skipped and why, and how to regenerate any single item (prompt + seed are in
the Soundbox library, tagged with the project name).
