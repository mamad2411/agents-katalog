---
name: sound-effects
description: Generate a small, coherent sound palette for interface moments through interchangeable provider adapters, beginning with ElevenLabs Sound Effects, then hand it to a walkthrough to check that the cues clarify rather than distract. Use when a product needs interaction sounds, feedback cues, micro-sound design, or a retro-futuristic audio layer. Triggers on sound effects, UI sounds, interaction audio, micro sounds, click sound, swipe sound, drag sound, ElevenLabs sound effects, audio feedback, retro-futuristic sound.
accepts:
  - from: design-tokens
  - from: semantic-micro-interactions
handoffs:
  - to: walkthrough
    when: generated sound cues have been wired into an operable interface and need checking in context
---

# Sound Effects

**Announce at start:** "I'm using the humane:sound-effects skill to make a small, coherent sound palette for this interface."

Sound is feedback, not wallpaper. Generate a short cue only when it acknowledges
a change that the interface needs to make felt: a panel catching after a drag,
a confirmed action, a changed mode, or a boundary reached. It is never added
merely because something moves.

## Before generating

1. Name the moment and the change it confirms. If the interface already makes it obvious, do not add a sound.
2. Read the project's token set or `DESIGN.md` when it exists. It supplies the material vocabulary; do not invent a second brand in audio.
3. Ask whether sound is opt-in, and identify motion-reduction and system sound settings. Effects must never autoplay, convey the only meaning, or prevent a task from being completed silently.

## Generate a palette, not isolated noises

Start with three to five roles. Keep each effect short and quieter than a notification.

| Moment | Duration | Prompt shape |
| --- | --- | --- |
| Press / select | 0.50 s | dry tactile click, no voice, no melody |
| Panel drag | 0.50–0.60 s | restrained low-friction mechanical glide, soft analogue texture |
| Snap / settle | 0.50 s | soft magnetic catch, rounded transient, short decay |
| Boundary | 0.50 s | muted non-alarming low pulse |
| Completion | 0.50–0.80 s | small upward confirmation tone, restrained and non-game-like |

For Humane, begin with **precise, editorial, retro-futurist, tactile, quiet** and exclude voice, melody, fanfare, harsh alarms, and bright game UI. Generate alternatives, then choose the family by listening side by side.

## Provider adapters

ElevenLabs is the first adapter, not the architecture. The generator takes a
`--provider` name and loads `scripts/providers/<name>.py`; every adapter shares
the same prompt, duration, loop, output, and receipt contract. Read
`references/provider-adapters.md` before adding one. This is where another
hosted provider or local sound model can be integrated later without changing
the skill's UI rules, prompt palette, generated files, or review handoff.

The ElevenLabs adapter calls `POST /v1/sound-generation` with
`ELEVENLABS_API_KEY`. The key belongs in the project's approved secret manager
or local environment, never in `humane.json`, a prompt, source code, or a
committed `.env` file. Read `setup/references/secrets.md` when setting up or
changing secret access.

```bash
python3 scripts/generate_sound.py --provider elevenlabs --name panel-snap --text "A soft magnetic mechanical catch; tactile analogue electronics, warm low mid tone, precise and quiet, no voice, no melody, no alarm" --duration 0.5 --out <resolved-sound-directory>/panel-snap.mp3
```

Resolve `<resolved-sound-directory>` with `artifact_path(palette,
"sound-effects")`, which produces `.design/sound-<palette>/` under the project;
never construct that path from the current working directory. ElevenLabs accepts
explicit durations from 0.5 seconds, so the generation table does not promise a
shorter value than the adapter can request. Use `--duration` only when
interaction timing needs it. `--loop` is for ambience only, never a click, drag,
or completion cue. The script writes audio plus a JSON receipt containing its
prompt and parameters, never a key.

## Wire and check

- Preload only selected, compressed effects; never fetch a key or generate in the browser.
- Trigger after a visual state change begins. A sound that predicts a change that later fails is misleading.
- Use one sound per completed gesture and rate-limit rapid hover, drag, and click events.
- Offer a visible mute control when sound recurs, preserving that choice for the current device.
- Hand the live interaction to `humane:walkthrough`. Check whether the cue clarifies what happened; do not judge it in isolation.

## Boundaries

- Never generate speech here; use a speech tool for narration.
- Never claim an effect improves accessibility without testing it with people who use sound differently or not at all.
- Never spend credits or call the API until the user approves the selected prompts and variation count.
