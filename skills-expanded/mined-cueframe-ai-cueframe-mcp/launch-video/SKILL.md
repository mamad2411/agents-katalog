---
name: launch-video
description: Turns screen recordings and product footage into a 30–90 second 16:9 launch film — payoff-first hook, real product surface punched in, a building bed or narration, one CTA end card. Triggers on "make a launch video", "announcement video for this feature", "turn this screen recording into a demo film", "product video from these captures", "we're shipping Friday and need a video", "feature announcement".
---

# Launch video

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

You bring real screen recordings or product footage plus the one outcome the feature delivers;
you get back a 30–90 second 16:9 announcement that opens on the payoff, shows the actual product
doing the real thing, builds under a bed or narration, and lands on a single CTA.

## Before you start

Nail the payoff sentence and collect the captures before any setup. When the first tool call
approaches and CueFrame isn't connected, load **`cueframe-connect`** and follow it once.

Keep the momentum — the video plan is the hard part, the connection is not.

## Inputs

- **Real captures** (required): screen recordings, product footage, real output. CueFrame does
  not screen-record — the user records (or uses a capture client) and you `import_media` the
  file. Never mock what's missing; ask for the real capture.
- **The payoff**: the outcome in the user's words ("close the books two days faster"), plus the
  CTA (one action) and launch date if any.
- **Brand kit**: project kit if present; ask for wordmark + accent color otherwise.
- **Voice**: default a building instrumental bed with captioned key lines; narrated VO if they
  have a script or want one generated.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
for layout and motion evidence. A follow-up tweak preserves the approved brief; inspect the
affected window and regressions without automatically rerunning the full-film judge or export.

1. **Import the real surface.** `import_media` every capture; wait for ready;
   `get_media_context` for what each recording actually shows (and the transcript, if narrated
   footage exists). Inventory the strongest 3–5 real moments before writing a beat.
2. **Open on the payoff, not the name.** The hook is the OUTCOME — the result on screen, the
   pain disappearing — inside the first seconds. "Introducing X" is throat-clearing; the
   outcome-first frame is the hook. No logo, no title card first.
3. **Structure: hook → problem → reveal → proof → CTA.** `new_composition` at 16:9 →
   `apply_composition` with the beats. Pacing tightens as the payoff approaches — clips get
   shorter toward the reveal.
4. **Punch in on the real pixels.** A click target is tiny in a full-frame capture;
   `setCropIntents` with `point` focus segments zooming to the exact UI region per step,
   `frame-center` in the gaps, tiling every clip. The single biggest amateur-to-pro delta in
   product video.
5. **Cards for the claims and the end card.** Key lines and the closing CTA are `kind:"card"`
   HTML in the brand's type and palette, animated in its CSS or with
   `clip.setKeyframes` in a FOLLOWING `apply_composition` call. When the brief calls for a CTA, use one, on the end card, held long enough to read; include a date only when relevant.
6. **Audio when requested or appropriate.** Preserve explicit silence; otherwise: `search_resources` for a bed honoring the brand kit's
   `musicMood`, energy arcing toward the reveal; place it `audioRole:"music"`,
   `materializeGrid { grid:"beat" }`, and land beat boundaries and the reveal on the grid. If
   narrated: the VO is the rhythm authority instead — cut to the voice and duck the bed under
   it. Explicit silence is a supported creative choice.
7. **Caption narration.** For transcribed voice, save the edits first, then call
   `captions.fromComposition` with the narration track ID in a separate `apply_composition`
   call. Speech clips must have saved duration matching playable source duration divided by
   playbackRate. Re-run after later edits. Use authored word timings for generated VO without a
   transcript, and style legibly via `setCaptionStyle`. Caption narration when requested or appropriate; preserve an explicit uncaptioned format.
8. **Inspect and deliver.** `preview_frame` at t=0, hook-end, the reveal, and the end
   card; describe each still and ask whether a real capture is on screen; distinguish actual captures from reconstructed artwork. Inspect motion through the important handoffs and listen to changed audio. Use `score_composition` only when broader critique is useful and within budget, with the payoff line as `editorialIntent`. Fix the observed acceptance failures, then export for requested final delivery.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. For this format's defaults read section 2 (Launch film) of the [format standards](../video-craft-standards/references/format-standards.md).

## Delivering

Close with the handoff, never "done":

- The render link and where it lives (project + composition id).
- Attribution for the bed and any licensed asset (provider, id, author).
- The intentional-silence note with its reason, when relevant to the requested delivery.
- A one-line cutdown offer: the 16:9 master can become 9:16 / 1:1 siblings for social (see
  `every-format-from-one-edit`).
