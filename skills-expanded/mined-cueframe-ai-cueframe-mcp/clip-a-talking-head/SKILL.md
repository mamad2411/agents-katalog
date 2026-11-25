---
name: clip-a-talking-head
description: Cuts a podcast, talk, or interview into shorts that open on the strongest sentence, reframe to the active speaker, and carry transcript-timed captions. Triggers on "clip this podcast", "pull the best moments out of this talk", "make shorts from this interview", "cut this down for social", "find the viral moment", "turn this recording into clips", "the good part is buried".
---

# Clip a talking head

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

You point at long-form footage of people talking; you get back one or more 15–60 second clips
that each open on the strongest sentence, keep a moving camera on whoever is speaking, cut the
dead air, and caption every word from the real transcript.

## Before you start

Get the source URL and what "best moment" means to the user before any setup ceremony. When the
first tool call is close and CueFrame isn't connected, load **`cueframe-connect`** and follow it
once.

Then straight back to hunting the moment — setup is a footnote, not a phase.

## Inputs

- **The recording** (required): a public https URL or existing media. Any length; the
  transcript does the finding.
- **Aspect + count**: default 9:16, 2–3 clips of 20–40s. 16:9 or 1:1 on request.
- **Brand kit**: use the project's kit for caption styling and any title cards if present;
  neutral otherwise.
- **What counts as "best"**: default = the most surprising, quotable claims. Ask only if they
  hinted at a specific topic.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md).
Watch/listen across changed cuts and caption/subject motion with `preview_clip`. For a small
correction, retain the approved edit and check relevant regressions without automatically exporting.

1. **Import and read.** `import_media` the recording, wait for ready, then `get_media_context`
   — the transcript with word timings and the face roster (with `faceId`s and speaking share)
   are your whole map. For an assisted hunt, `suggest_briefs` proposes clip candidates from the
   transcript; you still own the pick.
2. **Find the strongest sentence — it goes FIRST.** Read the transcript for the claim that
   makes someone stop scrolling. The clip opens ON that sentence, mid-conversation if needed.
   Never open on wind-up ("so, um, one thing I'd say is…") — cut TO the moment.
3. **Seed the clip.** `new_composition` at the target aspect → `apply_composition` with the
   clip trimmed so the hook sentence starts at t≈0. Order beats strongest-first; the payoff is
   the open, the context earns its place after.
4. **Cut the dead air.** `addExcludedRange` / `cutAndRipple` on false starts, filler, long
   pauses — the transcript's word timings show you exactly where speech stops. A tight talking
   clip is mostly this step.
5. **Reframe to the speaker.** `setCropIntents` with segments tiling the clip:
   `focus:{mode:"active-speaker"}` as the base, `all-faces` to hold a two-shot, a `face` +
   `shotScale:"close"` punch-in on the emphasis line. A static center crop is the amateur tell;
   the camera should move because the conversation moved.
6. **Captions from the edited clip.** Save cuts and exclusions first, then call
   `captions.fromComposition` with the speech track ID in a separate `apply_composition` call.
   It projects the real transcript through every saved edit; clips must have saved duration matching playable source duration divided by playbackRate. Re-run after later edits. Get the
   exact input from `describe_composition_ops({type:"captions.fromComposition"})` and style via
   `setCaptionStyle` — plated, high-contrast, never over the mouth or
   eyes. Where the footage allows, put the emphasized keyword BEHIND the speaker as an overlay
   clip at `zPlane:"behind-subject"` — the focused signature depth move. If the user explicitly
   wants every running caption behind the speaker, set the caption layer's own
   `zPlane:"behind-subject"`; that choice resolves cutouts across every captioned source window.
7. **Decide the audio — required.** Speech is the spine here, but decide the rest: a subtle bed
   from `search_resources` honoring the brand kit's `musicMood`, ducked under the voice — or
   intentional speech-only, recorded with its reason in the delivery note. Either is fine;
   defaulted silence is not.
8. **Prepare the subject evidence.** If `get_media_context.faces.status` is `not_detected`, call
   `prepare_media` with `kind:"subjectTrack"` and the clip's exact SOURCE trim window; if the
   edit has `zPlane:"behind-subject"`, prepare `kind:"matte"` for that same window. Poll
   `get_media_facts` with kind + startSec + endSec until `exact.state:"ready"`. A flattened
   depth title or ignored speaker crop is not preview evidence.
9. **Preview, judge, render once per clip.** `preview_frame` at t=0 and each cut; describe each
   still (is the framed person the one talking? is the top of the head in frame?).
   `score_composition` with the clip's claim as `editorialIntent`; fix relevant acceptance failures,
   then `create_render` → `wait_job (kind:"render")`.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. For this format's defaults read section 4 (Talking-head clip) of the [format standards](../video-craft-standards/references/format-standards.md).

## Delivering

The last message carries, per clip:

- The render link and where it lives (project + composition id), with the clip's opening
  sentence quoted so the user can tell them apart.
- The speech-only / bed decision and its reason (the intentional-silence note when applicable).
- Attribution for any licensed bed (provider, id, author).
- Which moments you considered and passed on — the shortlist makes the next batch a one-line
  ask.
