---
name: cartoon-character
description: "Style for edit-video: a lip-synced 2D cartoon character that talks, blinks, frowns, lights up and swaps poses on the beat. Use Ali's cartoon or Stashy (FavStash's mascot) out of the box, or make the creator's own with any image AI. Works as the cursor in animated-explainer, as a corner presenter on any HyperFrames reel, or big at the bottom of a cartoon explainer."
---

# Cartoon character

A style on top of `edit-video`. It is a cut-out rig, not generated video: a handful
of full poses plus small face patches (mouth shapes, closed eyes, brows), switched by
one GSAP timeline from the voice. Every frame is seekable, renders are free, and the
character looks the same in every reel.

## Characters

| Character | Folder | Poses |
|---|---|---|
| **Ali**, the creator of this pack, as a cartoon | `characters/ali/rig` | neutral, point, thumbs, wave, shrug |
| **Stashy**, FavStash's mascot | `characters/stashy/rig` | neutral, point, thumbs, wave, shrug, explain |
| **The creator's own** | their own folder | whatever they make |

Both samples have mouth shapes `m-ah`, `m-eh`, `m-oo`, resting mouths `m-grin` and
`m-frown`, `e-closed` for blinks, and `u-worried` / `u-excited` brows. They are for
trying the skills; read the [terms](characters/README.md) before using one in a
published video. For a creator's channel, make their own character.

## Make your own character with AI

Any image model that can edit an image while keeping its subject works: GPT Image,
Nano Banana, Seedream, Flux Kontext and others. The full recipe and prompts are in
[make a character](references/make-a-character.md). In short:

1. **One base image** of the character, front-facing from the chest up, on a flat
   green background. Use the creator's photos as references if it's them.
2. **Edits of that base:** four or five poses, then three mouth shapes, closed eyes
   and two expressions, each changing only that part.
3. **`scripts/build_rig.py`** keys out the green, lines every edit up with the base,
   cuts the face patches and writes the rig folder with an alignment report.

A rig is 1024×1024 PNGs plus `patches.json`. New poses and patches need no code:
the presenter picks up every `pose-*.png` and every entry in `patches.json`.

## Use it

- **In `animated-explainer`:** set `CHARACTER = 'ali'`, `'stashy'` or a rig folder
  in the spec. The builder runs the steps below and puts the character in the cursor
  badge, or on the rail head with `STYLE = 'rail'`.
- **In any HyperFrames composition** (a corner presenter on a talking-head edit, or
  big at the bottom of a cartoon explainer):
  1. `python3 scripts/lipsync.py --audio voice.wav --words words.json --out mouth.json`
     turns the voice (and its word times, if you have them) into mouth shapes.
  2. Write a schedule: poses on beats, brow windows, bounces on key words
     ([example](assets/example-schedule.json)).
  3. `python3 scripts/presenter.py --rig <rig> --rig-url assets/presenter --schedule schedule.json --mouth mouth.json --out-html presenter.html --out-pres pres.json [--left --top --size]`
  4. Copy the rig to `assets/presenter/`, load `assets/presenter.css` and
     `assets/presenter.js`, paste `presenter.html` into the composition root and call
     `addPresenter(tl, PRES)` with the contents of `pres.json`, after the scene
     tweens.

## Acting

- **Pose on meaning:** shrug on the problem, point while explaining or driving the
  UI, thumbs on a win, wave on the call to action. Hold a pose at least a second.
- **Brows tell the arc:** worried before the turn, excited after it.
- **Bounce on four to six key words,** not on every line.
- **Mouth only on its own words.** With two voices, pass only this character's words
  to `lipsync.py`, so it stays quiet while the other one talks.
- **Small and in the scene.** A badge of about 200 px or a corner presenter of about
  650 px. It never covers text being read.
- **The voice matches the character.** The creator's own voice, or a clone of it
  with their OK. See `animated-explainer`'s voice options for free local voices.

## Pitfalls already paid for

- Two `tl.set` calls on one element at time 0 get reverted when the renderer seeks
  back to 0. The opening pose and mouth use `gsap.set`, which `presenter.js` does.
- An image model that redraws slightly between edits leaves patches that don't sit
  on the face. Run `build_rig.py --register` and read the alignment report before
  trusting a rig.
- Prompting "keep everything pixel-identical" stops some models from changing the
  part you asked for. Name the one thing to change and say everything else stays.
- Colour drifts across many edits (hair turning pink after a dozen). Compare every
  edit with the base and correct it before building the rig.
