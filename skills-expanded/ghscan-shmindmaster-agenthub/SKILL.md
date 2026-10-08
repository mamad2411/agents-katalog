---
name: media-director
description: Use when a video needs direction, a visual plan, scene design, pointer and highlight choreography, talking-head blocking, or performance notes for local voice.
---

# Media director

Translate the locked storyboard into what appears and how it is performed. Decide in this turn; do not present a menu of visual styles. You do not capture, generate, or release.

Load `../media-studio/references/engagement.md` and `scene-archetypes.md` unless kind is `product-screencast` (Recast + `product-picture.md`). When `programForm` is `technical-story`, load `../media-studio/references/technical-story.md`: the markup rules there are yours to direct per beat.

Requires `storyboard.json` and `visual-bible.json` on viewer-facing jobs. If they are missing, remit to `media-storyboard` / `media-studio-visuals`.

## 1. Visual choice

Prefer the **simplest truthful visual that maintains attention**. A cheaper still that holds across two ideas fails.

| Mode | When |
| --- | --- |
| `screen` | Claim is about a live product — `media-studio-capture` (WebM + Recast). Default on `product-screencast`. |
| `slide` / archetype kit | Type-led argument with **no** product to show — pick an archetype, not "the briefing slide" |
| `diagram` | Structure or flow (Mermaid/D2/SVG, not diffusion) |
| `talking-head` | Face must carry the line |
| `motif` / `broll` | Problem, outcome, or context — not product UI |
| `animation` | Motion itself teaches; Remotion |
| `narration-only` | A visual would decorate |

A slide or diagram that does not build across the line is a still. Call a build, a cut, Motif, or B-roll rather than holding it for a second idea.

Do not use the same `visualArchetype` twice in succession unless the storyboard marked the repeat intentional.

## 2. Pointer, click, highlight

For `screen` scenes, specify target, pointer lead → action → visible feedback → result hold (`product-picture.md`). Recast owns cursor, ripple, punch-in. Wide → punch-in on the control → hold through the native response. Config beat before the run it causes.

For type-led scenes, emphasis is type color, Remotion build-in, and hold time, not a fake cursor.

Technical stories mark up aggressively, on top of Recast: box the element that matters, dim the rest, arrow cause → effect, zoom, and label with the story vocabulary (`User action`, `Webhook`, `DB write`, `Async job`). When the beat crosses systems, put a tiny flow diagram on screen before the code. Write each beat's overlay spec (`boxes`, `arrows`, `notes`, `dim`) into `direction.json`; `media-studio-compose` renders it with `kit/screencast/render-overlay.mjs` and applies it through the manifest `overlay` hint. Code reveals are `render-code.mjs` cards: the 5–20 lines that matter, one highlight band per card, the commit named. Every visual change is motivated by the story; never add one to fill a quiet stretch.

## 3. Performance and sound

Owner voice: name the style-bank register (`explaining`, `firm`, `serious`, …). Do not write free-text "sound excited" for that speaker.

Honor storyboard `sound` (`musicCue`, `sfxCue`, `silenceOnReveal`, `transitionAudio`). Viewer-facing default is `bed` with `silence` on the hero hold.

## 4. Output

`direction.json` keyed by beat id: visualMode, visualArchetype, on-screen copy, highlight, action, register, duration, sound, pause/hold. Then `media-studio-generate`.

## 5. Final check

- [ ] Archetypes vary; no accidental consecutive repeat
- [ ] Hero has silence or a ducked rest
- [ ] Register named per beat
- [ ] Next skill is `media-studio-generate`
