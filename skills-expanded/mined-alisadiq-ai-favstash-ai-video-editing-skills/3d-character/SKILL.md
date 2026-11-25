---
name: 3d-character
description: "Style for edit-video: a cute 3D character reel with no camera and no Blender. A chibi kid (a boy or a girl, colours and hair yours to set) talks to camera on a soft pastel stage, lip-synced to a locked voice, with camera cuts on spoken words, a floating card that types in, and the line word-lit on top. Built in Three.js and rendered by HyperFrames on your machine."
---

# 3D character

A style on top of `edit-video`, which owns the voice, sound mix and review. The whole
reel is a small 3D scene drawn in code: a chibi character built from simple shapes,
one pastel colour for the floor and the sky, soft light, and the camera cutting on
the words. three.js (pinned 0.168.0) comes from the workspace runtime that `edit-video`'s
`scripts/init-workspace.mjs --install` prepares, like GSAP; the builder copies it into each
reel, and HyperFrames renders it like any other composition.

## The look: simple and cute

- **One character, chibi proportions:** a big round head, glossy dot eyes, blush, a
  single smooth fringe, a small body and stubby arms. It talks with the voice,
  blinks, nods on accent words, points, hops and waves; on a happy beat its eyes
  curve shut.
- **One colour, soft light.** The floor and the sky are the same pastel, so the
  character floats in a clean space with a soft shadow under it. No desks, no busy
  props, no dark moody sets: they read as clutter at phone size.
- **At most one prop:** a floating card that pops in, types two short lines and
  fills a progress bar, then leaves before the next wide shot.
- **The spoken line on top,** big and word-lit, with the accent word in a serif
  italic in the accent colour.

## The character

`CHARACTER` in the spec sets it:

| Option | Values |
|---|---|
| `look` | `'boy'` (side-swept hair, hoodie, shorts) or `'girl'` (two buns, top, skirt) |
| `skin`, `hair`, `top`, `bottom`, `shoes` | Any colour, as `'#rrggbb'` |

Pair it with a stage colour that flatters it: peach `#FFE9D6` with a blue accent for
the boy, sky `#E6F4FF` with a pink accent for the girl.

A new character is new shapes in `assets/characters.js`: spheres and capsules for
the body, a mouth that scales with the voice, eyes that blink. Keep the same
`update(state)` contract and the stage drives it. Keep it simple: a few big shapes,
big eyes, one colour per part.

## Workflow

Work in a run folder from `edit-video` (`scripts/new-edit.mjs`). Each reel is a
folder `work/<reel>/` with its `spec.py` and `voice/`. Start from
[the worked example](example/spec.py).

1. **Script.** One idea, 10–40 s, short lines. Mark the word to stress with
   `*stars*`; the character nods on it.
2. **Voice.** `edit-video`'s `scripts/voice.py work/<reel> --engine files|hyperframes`
   writes `voice/vo.wav` and every word's time. Use a voice that suits the
   character; `edit-video`'s voice options cover free local voices and cloning.
3. **Spec.** `build(T)` returns the shots (`full`, `close`, `side`) and when they
   cut, the acts (`wave`, `point`, `hop`, `happy`) and when they start and end, the
   card, and one sound cue per visible event. The contract is in the docstring of
   [`scripts/build.py`](scripts/build.py).
4. **Build:** `python3 <skill>/scripts/build.py work/<reel>`. It copies the stage,
   the character and three.js into the reel and writes `index.html` and `cues.json`.
5. **Look before rendering.** `hyperframes snapshot work/<reel> --describe false --at …`
   at the hook, each cut, the card and the last second. Or open `index.html` from a
   local web server and fire `hf-seek` events in the browser console.
6. **Render:** `hyperframes render work/<reel> --fps 30 --quality delivery --workers 2 --output previews/<reel>-v01.mp4`.
   It draws at twice the size and scales down, so allow about 10 s per second of
   video. WebGL renders on the GPU.
7. **Sound and review** with `edit-video`: `sfx-sync.mjs mix work/<reel>/cues.json --voice work/<reel>/voice/vo.wav …`,
   then the usual review of the encoded cut.

## Shots and acting

- **Open full:** the whole character under the hook, so frame 1 reads at a glance.
- **Close on the line that matters,** side shot when the card comes in, back to full
  for the ending.
- **Point at the card** while it's on screen, then **wave** and go **happy** on the
  call to action.
- Cut on spoken words, about every 2–3 s. Hold a shot longer only while the
  character is doing something.

## Pitfalls already paid for

- A detailed mascot with realistic eyes, fur and a moody set looked off-putting.
  Simple shapes and a pastel stage read as cute.
- Framing by height alone crops a wide character. The stage frames by height and
  width (`width` in the character).
- A card left in the last wide shot gets cut off at the frame edge. Give it an `out`
  time.
- The composition has no GSAP timeline; the root carries `data-no-timeline` so
  HyperFrames' lint accepts it, and time comes from the `hf-seek` event.
