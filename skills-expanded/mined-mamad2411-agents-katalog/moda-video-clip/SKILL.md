---
name: moda-video-clip
description: >-
  Generate video clips: prompt-to-video, image-to-video, reference-guided,
  extend, upscale, reframe; text CONTENT → -motion. Draft cheap, then hero
  render. Metered.
argument-hint: "[what the clip shows + what it starts from (logo/photo/frame)]"
allowed-tools: Bash(moda:*), Read
---

# moda-video-clip

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Cards before knobs

`--model` is REQUIRED on every call and there is no "auto". Read the capability
cards FIRST and copy values verbatim — guessing a duration, ratio, resolution or
`--model-params` value is how a call 422s.

1. `moda media models` — one card per model: modes (prompt→video, image→video,
   reference→video, extend), duration and resolution envelopes, aspect ratios,
   audio behaviour, billing basis.
2. Pin the knobs on EVERY call: explicit `--duration` (omitting it reserves the
   model's LONGEST clip) and the resolution the pass needs. Knobs snap
   server-side — read `applied` and `adjustments` on the result, never assume.
3. Nothing is charged until a finished render is collected, so `--no-wait` +
   `moda task status [TASK_REF] --wait` is how several drafts run at once. A
   re-run of the same call replays the existing render instead of paying twice;
   a deliberate retake needs a changed knob (`--seed`, or a new prompt).

## Sizes and defaults

| Pass | Duration | Resolution | Audio |
|---|---|---|---|
| Draft | shortest legal (≈4 s) | 720p | silent where silence is a price axis |
| Hero | what the deliverable needs | what it will be seen at | per the card |
| Upscale | — | one tier up, on the winner only | unchanged |

Hard edges, facts not preferences: video models mangle text, prices and logos —
real type and brand marks go on the canvas, never in a prompt (that is
moda-video-motion's job). There is no free-form video-to-video edit: a source
clip is a generation reference, an `--extend-video` base, or the subject of
`upscale-video` / `reframe-video`.

## Recipe — the draft ladder (the DEFAULT for anything a user will see)

1. Start assets, if any: `moda brand show [BRAND_REF] --json` for durable logo
   refs (LOOK at them first); a canvas frame via `moda export [CANVAS_REF] --format png --page [N] --pixel-ratio 2 -o frame.png`; user footage via `moda file upload [clip.mp4]`.
2. **Draft.** `moda media generate-video --prompt "[one complete instruction: subject, motion, camera, style, mood]" --model veo-3.1-lite --duration 4 --resolution 720p --no-generate-audio -o draft.mp4` — it comes back while you can still change your mind.
3. **Look at it.** `moda media video-frames draft.mp4 --count 4 -o frames/` — FREE, and the only way to SEE a render. Judge the frames against the brief; never present a clip you have not looked at.
4. **Fix, don't escalate.** A draft that missed is nearly always a PROMPT problem: change the prompt, re-draft on the fast lane. Stepping up a tier buys a sharper version of the wrong clip.
5. **Commit.** Only the surviving direction, at the length and resolution the deliverable needs, on the model the ask deserves: `moda media generate-video --prompt "[revised]" --model [HERO_MODEL] --duration [N] --resolution [TIER] -o hero.mp4`.
6. Frame-check the hero the same way, then enhance the WINNER only: `moda media upscale-video hero.mp4 --resolution 1080p -o final.mp4`, or `moda media reframe-video hero.mp4 --aspect-ratio 9:16 -o vertical.mp4`.
7. Deliver: the result is a durable `file_…`. Fetch it with `moda file download [FILE_REF] -o [name].mp4`, hand over the path plus the usage receipt. Going on a canvas instead (type, a price, a logo, a cut)? Hand off to moda-video-motion — `<video>` markup is the only way clips land on a canvas.

## Examples

- "a 10-second product video" → ladder: draft, frames, hero render.
- "animate our logo into a stinger" → image-to-video with the logo as `--image`.
- "make this 6s clip longer" → `--extend-video` on a model whose card shows it.
- "make the 16:9 into a story cut" → `reframe-video --aspect-ratio 9:16`.
- "animate this quote / this headline" → not this lane: moda-video-motion sets
  real type on a canvas; a model would mangle it.

## Errors

Any typed error → load moda-core and read its recovery reference.
422 = a guessed parameter: re-read the model card and copy the value verbatim.
Empty frames (`no_frames_decoded`) means Moda could not DECODE the file — never
regenerate on it.

## Make it recurring

Pin the model and brand defaults for this repo → moda-context; a recurring
product-clip cadence → moda-automate.

See also: moda-video — the lane fork, canvas motion, mp4/gif export ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/video.md | always — model strengths, knob rules, prompt craft, workflows |
| references/omni-and-media.md | metered-lane semantics, the best-of-N pattern, audio pairing |
