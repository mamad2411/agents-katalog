---
name: genex-ai-sfx
description: Generate a real sound effect (mp3) from a text prompt with `npx genex sfx`, then play it in Three.js (positional or global audio). Use when the user wants a specific sound — a gunshot, footstep, pickup chime, explosion, engine hum, UI click, whoosh — triggered on a game event.
---

# Genex AI · SFX

Turn a prompt into a real **mp3** sound effect and wire it to a game event.

## Run

```bash
npx genex sfx "<prompt>"
npx genex sfx "punchy laser zap, short and dry" --duration 2
```

`--duration <sec>` (0.5–22) sets a target length; omit it to let the model pick.
Blocks until ready, then prints its public URL:

```
https://assets.genex.technology/generations/<id>/audio-sfx
```

The mp3 lives in Genex storage (R2) and loads straight from that URL — you don't download
it and nothing is committed to your repo. The URL is permanent (local dev, published game,
and remixes alike).

## Play it in Three.js

Audio needs **one `AudioListener` on the camera**. Then load the clip and play it
on an event. Browsers block autoplay — start audio after a user gesture (click/keydown).

**Positional** (3D, attenuates with distance — attach to an object):

```ts
import * as THREE from "three";

const listener = new THREE.AudioListener();
camera.add(listener);

// the URL `npx genex sfx` printed (R2 sends CORS headers, so cross-origin works):
const SFX_URL = "https://assets.genex.technology/generations/<id>/audio-sfx";
const buffer = await new THREE.AudioLoader().loadAsync(SFX_URL);

const sound = new THREE.PositionalAudio(listener);
sound.setBuffer(buffer);
sound.setRefDistance(5);
laserMesh.add(sound); // follows the object

// on fire:
if (!sound.isPlaying) sound.play();
```

**Global** (UI/non-spatial — same volume everywhere): use `new THREE.Audio(listener)`
instead of `PositionalAudio` and don't attach it to a mesh.

Reuse one loaded `buffer` across many plays; create a fresh `Audio`/`PositionalAudio`
(or call `sound.play()` again once stopped) per trigger.

## Publish checklist

- Load it from the **URL** the command printed — absolute and permanent, so it resolves
  the same in local dev, the published game, and remixes. Nothing to commit.

## Options

- `--duration <sec>` — target length 0.5–22 (shown in Run above); omit to let
  the model pick.
- `--no-wait` — enqueue and return immediately (the file won't be downloaded;
  re-run without `--no-wait` to fetch it).
- `--api-url <url>` — override the API base (local dev).

## Troubleshooting

- **"Not authorized"** — run `npx genex init` first (in the project — it resolves this project's own CLI) (it writes your `GENEX_TOKEN`).
- **"Out of credits" (`insufficient_credits`)** — the account has no credits left for
  this sound generation. Tell the user the facts the CLI printed: their balance, this
  generation's cost, and when their credits refill. Then offer to continue the build
  with a procedurally-coded placeholder (a small WebAudio-synthesized stub sound)
  and mark the spot with `// TODO(genex): regenerate when credits refill` so the
  real asset is one command away later. Do not stop the session over this.
- **"Email not verified" (`email_verification_required`)** — generation credits
  unlock after the account's email is verified. Give the user the verify link the
  CLI printed, wait for them to confirm, then re-run the command.
- **No sound** — the `AudioContext` is suspended until a user gesture; trigger the
  first play from a click/keydown. Confirm the camera has an `AudioListener`.
- **Too quiet/loud** — `sound.setVolume(0..1)`; for positional, tune
  `setRefDistance` / `setRolloffFactor`.
