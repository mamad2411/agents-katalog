---
name: add-music-bed
description: Retrofits a music bed (and ambience or SFX) onto an existing composition — license-aware search, correct mix hierarchy, ducking under speech, cuts moved onto the beat. Triggers on "add music to this", "this video feels dead", "put a bed under it", "it needs sound", "add background music", "make the cuts hit the beat", "add some sfx", "the audio is just silence".
---

# Add a music bed

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

> **Stock-audio limits (verified in production):** a Freesound import lands with
> `audioRole:"sfx"` and NO beat grid — `import_resource` takes no audioRole param, and
> `materializeGrid grid:"beat"` will 422 `grid_unavailable` on it. Set the role yourself when
> placing the clip (`audioRole:"music"` on the composition clip), put the bed on its own AUDIO
> track, kept dedicated to music. Discover curated music beds through `list_catalog`; use an available measured grid
> only when it exists. A music role alone does not establish a reliable beat grid.

You point at an existing composition that sounds empty; you get it back with a licensed bed that
matches the brand's mood, sits correctly under any speech, and — where the bed drives pacing —
cuts moved onto its beat grid. Attribution included, levels disciplined, one re-render.

## Before you start

Listen first — identify what audio the composition already has before proposing anything. When
the first tool call approaches and CueFrame isn't connected, load **`cueframe-connect`** and
follow it once.

Then back to the soundtrack — this is usually a one-sitting job.

## Inputs

- **The composition** (required): id, or find it via `list_compositions`.
- **Mood**: the brand kit's `musicMood` is the default answer — honor it before asking. No kit
  → ask for one adjective pair ("calm/driving", "warm/dark").
- **What speech exists**: check `get_media_context` on the composition's media for VO/dialogue —
  it decides the whole mix shape.
- **Beat-cut permission**: moving cuts onto the beat changes timing slightly; default yes for
  social pieces, ask for approved masters.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md).
Listen to a scoped `preview_clip` across speech, ducking, fades, and beat changes before final
delivery; stills and a visual judge cannot establish the mix. Recheck visuals where cuts moved.

1. **Read the composition and its speech.** `list_compositions` / the composition body for
   what's on the timeline; `get_media_context` for transcripts. Speech present → the voice is
   the rhythm authority and the bed serves it. Without speech, the bed is the default rhythm authority and earns beat-cuts when it has a measured grid; let the visible action drive timing instead when the brief calls for it, and preserve approved cuts unless retiming is requested.
2. **Find the bed, license-aware.** Beds come from the curated music packs —
   `import_resource { kind:"music-pack" }` — honoring the brand kit's `musicMood` (mood and
   energy matched to the cut rate). For ambience or loop textures, `search_resources
   kind:"sfx"` (Freesound, CC0-only) works too. For SFX accents, the curated pack
   (`import_resource { kind:"sfx-pack" }`) is the fast default. Record provider/id/author for
   everything — attribution ships in the delivery note.
3. **Place it with a role, not a volume.** `apply_composition`: add the bed as an
   `audioRole:"music"` clip. The engine's default mix staging already keeps voice on top;
   author `volumeDb` only to deliberately deviate. Under speech, set `duck` so the bed drops on
   words and recovers between them — the voice is never fought.
4. **Fades at the edges.** A bed that starts at full level on frame one is a jolt: fade in over
   the first beat, fade/resolve out under the end card. The bed should feel like it was always
   there.
5. **Cut to the beat where the bed drives.** `materializeGrid { clipId, grid:"beat" }` on the
   bed — the server lands beat markers at correct timeline times. Move cut points and
   transition MIDPOINTS onto markers (start a 0.5s transition 0.25s early so its center hits
   the beat). Skip this when speech is the authority — there you land accents between phrases,
   on the words that matter.
6. **Restraint is the discipline.** A few placed sounds read; a wall of them merges into mush.
   The biggest moment gets the strongest accent ONCE. And silence stays a device — clean air
   before the first hit, a dropout before the biggest beat, is worth more than any riser.
7. **Listen and verify the affected window.** Check intelligibility, ducking, fades and synchronization in a motion/audio preview; stills alone cannot verify a music change. Preserve existing cut timing unless retiming was requested. Broader judging is optional and budgeted; export only for requested final delivery.

If, after listening, the right call is NO bed — a raw testimonial, a piece whose room tone is
the point — that is a legitimate outcome of this skill: record the intentional-silence decision
and its reason in the delivery note instead of forcing a bed.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. This skill exists to satisfy the audio rule in the cross-cutting section of the [format standards](../video-craft-standards/references/format-standards.md), which also covers provenance for stock assets; section 1 adds cutting to the music grid when a bed exists.

## Delivering

The last message carries:

- The new render link and where it lives (project + composition id).
- The bed's attribution (provider, id, author, license) plus any SFX used.
- The mix decisions in one line each: role, ducking, any authored level, which cuts moved onto
  the beat.
- OR the intentional-silence note with its reason, if no-bed was the right call.
