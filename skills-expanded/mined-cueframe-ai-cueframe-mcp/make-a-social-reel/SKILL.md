---
name: make-a-social-reel
description: Turns footage into a finished 9:16 social reel — hook inside 2 seconds, poster-grade type, a decided music bed, one final render. Triggers on "make me a reel from this", "turn this into a short", "cut a clip for TikTok / Reels / Shorts", "make this vertical", "make a social clip from this video", "the opening is boring", "can you make this pop for Instagram".
---

# Make a social reel

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

You hand over footage (a file URL, a talk, a product moment); you get back a 9:16 reel of 8–30
seconds that opens on its strongest image, cuts on the music, carries brand-grade type, and ends
on a deliberate beat — with a download link, not a "done".

## Before you start

Don't stall the conversation on setup — get the footage, the hook, and the tone agreed first.
When the first real tool call is imminent and CueFrame isn't connected:
load **`cueframe-connect`** and follow it once.

Thirty seconds, then straight back to the reel — treat it as a detour, never a gate.

## Inputs

- **Footage** (required): a public https URL, or something already in `list_media`. If they have
  nothing, ask for the real thing before reaching for stock — real footage is the whole edge.
- **Brand kit**: use the project's kit if one exists; otherwise ask for a color + font or extract
  one. Default: proceed with a neutral palette and say so.
- **Tone / platform**: default punchy, 15–25s, sound-on-with-captions. Ask only if the answer
  would change the cut.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
for layout and motion evidence. A follow-up tweak preserves the approved brief; inspect the
affected window and regressions without automatically rerunning the full-film judge or export.

0. **Find the claim (before anything else).** Interrogate the brand/material
   for its tension — what it believes that its category doesn't — and write
   the claim in one sentence. Derive the shot list, the bed's mood/tempo, the
   pacing, and every card's copy FROM that sentence. Use the requested visual experience as intent when the piece makes no factual claim.

1. **Import and read the footage.** `import_media` (public https URL), poll `list_media` until
   ready, then `get_media_context` — faces, transcript, word timings. The context tells you
   where the hook lives; don't guess.
2. **Pick the hook before you touch the timeline.** The strongest image, motion, or claim in the
   footage — the outcome, not the feature name, is the hook. If the best moment is at 0:47, the
   reel opens at 0:47. A logo-first opening remains valid when explicitly requested.
3. **Seed the timeline.** `new_composition` at 9:16, then `apply_composition`: clips trimmed to
   the beats you chose, a new visual beat at least every ~4 seconds. Cut TO moments; never let a
   clip run out.
4. **Reframe for vertical.** `setCropIntents` with segments that tile every clip —
   `active-speaker` or `face` focus when a person carries it, `point` focus on the action
   otherwise. A wide shot letterboxed into 9:16 is a fail, not a fallback.
5. **Author the type as cards.** Brand text is `kind:"card"` HTML — your typography,
   palette-as-fields, considered alignment — animated in its CSS or with
   `clip.setKeyframes` in a FOLLOWING `apply_composition` call. Catalog text primitives are
   utility only.
6. **Honor requested silence or existing audio.** When a bed is appropriate, search a bed with `search_resources` honoring
   the brand kit's `musicMood`, place it as an `audioRole:"music"` clip, then `materializeGrid`
   `{ grid:"beat" }` and land your cut points and transition midpoints on the markers. If the
   piece is genuinely better silent, that is a decision — record it and its reason in the
   delivery note. A reel whose silence nobody chose is not done.
7. **Caption any speech.** After saving the edited clips, use
   `captions.fromComposition` with the speech track ID in a separate `apply_composition`
   call. It follows trims, excluded ranges and clip placement across the reel. Speech clips
   must have saved duration matching playable source duration divided by playbackRate.
   Re-run it after later edits. Discover its exact input with
   `describe_composition_ops({type:"captions.fromComposition"})`, then style via
   `setCaptionStyle` (plated, bottom, out of the mouth/eyes). Most social viewing is sound-off;
   don't karaoke a beat with no speech.
8. **Inspect and revise.** `preview_frame` at the important layout and transition landmarks;
   describe each still in words, then inspect the intervening motion and relevant audio. Use
   `score_composition` only when broader critique is useful and within budget, with your one-line
   vision as `editorialIntent`, and fix the worst criterion first. Fix located acceptance failures against the brief.
9. **Export for requested final delivery.** `create_render` → `wait_job (kind:"render")`. Iterate with previews,
   not renders.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. For this format's defaults read section 1 (Social reel) of the [format standards](../video-craft-standards/references/format-standards.md).

## Delivering

Never end with "done". The last message carries:

- The render's download URL and where it lives (the project, by composition id).
- Attribution for every stock asset used (provider, id, author) — the provenance you recorded at
  import.
- The intentional-silence note with its reason, if you chose silence over a bed.
- One line on what you'd tighten next, so the follow-up edit has a starting point.
