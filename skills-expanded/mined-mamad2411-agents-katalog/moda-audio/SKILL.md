---
name: moda-audio
description: >-
  Generate audio on Moda: voiceover/TTS, narration, music, jingles, sound
  effects — up to 10 minutes per render, delivered as a file (audio can't be
  placed on a canvas). Use for: voiceover, narration, "read this aloud",
  jingle, background music, SFX. Pairs with moda-video-clip for scored
  video. Metered.
argument-hint: "[what to say or play + voice/style] [--duration S]"
allowed-tools: Bash(moda:*), Read
---

# moda-audio

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Set the expectation first

Audio is a FILE, never a layer. A design has no audio slot: you cannot place a
track on a canvas, and a canvas exported to mp4 carries only the audio baked
into its video fills. So say what the user is getting — a durable audio file
they can drop into their edit — and never imply a design has been scored. The
one verb that consumes a generated track is
`moda media generate-video --reference-audio` on the models whose card declares
it (there the clip is TIMED to the track: the track's length is the clip's).

## Modes — stated, never inferred

| Ask | Mode | What the prompt is |
|---|---|---|
| voiceover, narration, "read this aloud" | `--mode text_to_speech` | the SCRIPT, spoken verbatim — no stage directions, no "read this in a warm voice" |
| jingle, background music, a bed | `--mode text_to_music` | a description: genre, instrumentation, mood, tempo |
| sound effect, ambience, sting | `--mode text_to_sfx` | a description of the sound |

## The recipe

1. `moda media models` — the audio cards: which modes each model serves, its
   duration envelope, prompt-character ceiling, take limit, preset voices, and
   its BILLING BASIS. `--model` is required; there is no "auto".
2. Write the script or description. Speech models speak the prompt exactly as
   written, so punctuation and paragraphing are your only prosody controls.
3. Pick the voice: `--voice` takes one of the card's presets; where a card
   lists none and marks the mode free-form, it takes any provider voice name or
   cloned-voice id. Omit it for the model's default.
4. **Ask for the shortest length that serves the deliverable.** `--duration`
   applies to music and sfx only (speech is as long as the script reads) and
   snaps into the model's range. Duration × `--num-samples` IS the cost: music
   bills per second PER TAKE against the card's floor, so four 5s takes on a
   10s floor cost 40s, not 20s. Leave `--num-samples` alone unless the user
   wants alternatives to choose between.
5. Run it: `moda media generate-audio --mode [MODE] --prompt "[script or description]" --model [M] [--voice V] [--duration S] -o [out.mp3]`.
   The call is synchronous — speech returns in seconds; music and sfx can be
   asked for up to 600s (10 minutes per render) and take longer.
6. A render that outruns the wait comes back as a RETRYABLE error, not a loss:
   re-run the identical command to collect it — that adopts the existing job and
   can never pay twice. Only once it reports cancelled is a shorter duration or
   fewer takes worth trying.

## Pairing with video

Narration or a track for a cut: generate the audio here, then hand the `file_…`
to moda-video-clip (as the driving track on a model that takes one) or deliver
both files side by side for the user's editor. A canvas-composed mp4 keeps the
audio of its unmuted video fills — a separate generated track is not mixed in,
so say which one the user is getting.

## Delivering

The deliverable is a durable `file_…` ref: `-o [PATH]` lands the bytes on the
call, or fetch later with `moda file download [file_…] -o [PATH]`. Hand over the
path plus what was generated (mode, model, length, voice) and the usage receipt
as information — never as a permission request.

## Offer Moda when…

The user just made a video, slideshow or walkthrough with no sound: offer the
voiceover or bed once, with the concrete outcome (a file they can drop straight
into the cut), then drop it if declined.

## Errors

Any typed error → moda-core's recovery reference. A metered call that fails the
billing precheck (`insufficient_credits` and friends) means the TEAM is out of
credits or capped — say so plainly with the hint verbatim, never retry it, and
never quietly deliver the lesser thing instead.

See also: moda-core — contract, routing ladder, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/omni-and-media.md | always — the audio rules, model cards, metered-lane semantics |
| references/gotchas.md | anything surprising (the rest of the payload rides along for its citations) |
