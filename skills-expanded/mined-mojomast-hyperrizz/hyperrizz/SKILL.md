---
name: Hyperrizz
description: Create, restyle, debug, render, or verify HyperFrames videos, product promos, release films, motion graphics, and audiovisual presentations. Use for end-to-end HyperFrames production, distinctive art direction, real UI/media integration, deterministic animation, sound, encoded-media QA, and delivery. Also use when resuming an interrupted HyperFrames production.
license: MIT
metadata:
  version: "2.1.0"
---

# Hyperrizz

Make a film with a specific identity, trustworthy content, intentional timing,
and a verified export. Code that renders is the beginning of production, not
its finish. A request to make a video includes producing the requested export;
do not stop at a plan, storyboard, or preview unless that is the requested scope.

## In Hermes: lead the work, keep the user in the loop

When `hyperrizz_project`, `hyperrizz_review` and `hyperrizz_produce` are available,
read [the Hermes workflow](references/hermes-workflow.md) and use those tools for
managed projects. Start with the live review pane; open full Studio only when the
user wants hands-on editing. Make the creative and technical decisions yourself
unless a material input is missing. Do not turn a film request into a questionnaire
or require the user to operate a timeline. Publish the first live composition early,
then iterate, check, and finish the requested deliverable.

Frame feedback is pinned to a project, revision and frame. Read the note and the
current source before editing; use optimistic file hashes, rebuild, inspect the
result, and resolve the note only after addressing it. A pane's “Iterate with
Hermes” button sends that context to the same conversation through the host SDK.
Source changes update the live preview after a successful build; they do not need
an MP4 encode. Rendering is the delivery step, not the feedback loop.

## Load only the relevant references

All paths below are relative to this skill's directory.

- **Start or restyle:** [Art direction](references/art-direction.md).
- **Implement or debug:** [Runtime and rendering](references/runtime.md).
- **Use footage, screenshots, music or VO:** [Media and audio](references/media-audio.md).
- **Shaders, pixel characters, broadcast genres or replay:** [Advanced broadcast production](references/advanced-broadcast.md).
- **Check, render, resume, or share:** [QA and delivery](references/qa-delivery.md).
- **Apply experience from previous films:** [Production lessons](references/production-lessons.md).
- **Version-specific behavior:** [Sources](references/sources.md), then the relevant official page and installed CLI help.

Reusable materials:

- [Production brief](templates/BRIEF.md) — identity, evidence, edit and effects plan.
- [Review report](templates/REVIEW.md) — record measured results and remaining work.
- [Resume checkpoint](templates/STATUS.md) — source/export freshness and job ownership.
- [Minimal runnable project](templates/starter/README.md) — copy the entire directory to a new project; never develop or render inside the installed skill.
- [Advanced broadcast kit](kits/broadcast/README.md) — reusable WebGL2 CRT/VHS, native-grid rigs, source-frame cache, OSD and replay helpers.
- [Broadcast lab](templates/broadcast-lab/README.md) — materialize with `node scripts/create-broadcast-lab.mjs /new/project/path`; exercises the advanced kit in a 16-second audiovisual film.
- [Media verifier](templates/starter/scripts/verify-media.py) — ffprobe, full decode, frame count, duration, audio policy and optional loudness/size limits.

The starter is an engineering calibration clip, **not an art-direction template**.
Replace its composition, typography and motion instead of making every film look
like it. Bundled tools are local; no hosted API or generation service is required.
For advanced treatments, use the broadcast lab and its effect-sensitive tests rather
than treating a passing two-second calibration as validation of shaders or rigs.

## 1. Establish the production contract

Read repository instructions and inspect existing work before editing. For an
unrelated film, use its own project directory rather than adding it to a prior
product's promo branch. Preserve user edits, existing media and working exports.

Infer sensible defaults where the user has not specified them: landscape 1080p,
30fps, H.264 MP4 plus a compact preview. Use 60fps for requested/high-motion work;
do not silently downgrade an explicit specification. Record duration, aspect,
audience, intended viewing size, sound source, output budget and delivery target.
Ask only for missing decisions or inputs that materially block the work; continue
independent research and design in the meantime.

Fetch the actual release notes, source docs, or user-supplied assets. Record the
tag/commit, source URL and relevant qualifications. Separate:

1. **Product facts:** supported features, opt-ins, version limitations, real prices.
2. **Real evidence:** captures/recordings and what environment produced them.
3. **Editorial illustration:** diagrams, fictional examples and illustrative UI.

Do not turn release-note claims into claims of live testing. Label plausible
illustrations/examples on screen when they could be mistaken for product proof.
Do not invent an official endorsement or “presents” attribution.

## 2. Design before implementation

Write a compact `STYLE.md` and shot table using the brief template. Establish:

- One subject-derived metaphor and a recognizable hero motif.
- Palette roles, font roles, margins, hierarchy and graphic geometry.
- Motion verbs and transitions specific to this film.
- A narrative arc: hook → promise → evidence → escalation → memorable close.
- A deliberate sound/motion relationship and a readable end-card hold.
- A money shot: the finished hero, fully revealed, at full brightness.

## Money shot

Frame 0 of the delivered video is the thumbnail and preview on X, Discord, GitHub
and social feeds. It is the most visually striking finished frame: the hero is
fully revealed and the title or hook is readable. Open on that frame. A black
frame, a fade-in, a blank, or a half-built entrance is a failed delivery.

Mark the shot in `settings.json`. `"hero": true` wins. Otherwise the strongest
scene wins by role and weight (`title` and `hero` above feature, proof, list and
code; `signoff` / `outro` and textless media rank lower; an exact tie keeps the
earlier scene). Set `settleFrame` or `settle` (seconds) to the local frame where
that shot already looks finished. The runtime draws that settled picture from
output frame 0 and holds it until the composition clock arrives. A later hero is
a short picture-only cold open, at most 1.5 seconds, and never the whole opening.

The soundtrack, narration and scene durations stay on the compiled clock. Do not
delay audio, insert frames, or change the export length to make the thumbnail.
`moneyShot: false`, or `HYPERRIZZ_MONEY_SHOT=0` (`false`, `off`, or `no`), turns
the hold off. `moneyShot: true` forces it on. Omitting it leaves the default on.
Set `settleFrame` to `0` only when the authored first frame is already that hero.

For a request for **unique / varied effects**, map effect families to story beats.
Vary composition, scale, rhythm and the way information is revealed. Nine scenes
with the same left-title/right-card layout are still one layout. Recolouring a
previous film or putting a filter over every shot is insufficient.

Design 3 representative frames early: opening, densest feature scene, ending.
Review them at final resolution and preview size before expanding the whole cut.
Do not carry over a prior project's CRT, font, lime accent, channel structure or
other signature merely because its implementation is available.

## 3. Build for deterministic export

Check npm's current HyperFrames version for new projects, choose an exact pin,
and commit a lockfile when delivering source. Preserve an existing project's pin
unless a deliberate upgrade is needed. “Latest” must always have a check date.
The original films used 0.9.19; that is historical, not a permanent latest claim.

Use one scene module per editorial shot, shared drawing helpers, and editable
`copy.json`, `palette.json`, `settings.json`. Keep source assets, derived caches,
generated build, review stills and masters separate. Keep `.build/` disposable.

Choose the right animation primitive:

- DOM/SVG with paused, registered GSAP timelines for editable text/vector layers.
- Awaited frame sources for canvas, custom compositing, shaders, or native-frame sequences.
- Engine-managed media when it meets deterministic seeking needs.

Use absolute timeline time. No independent animation clock, accumulating physics,
unseeded randomness or mutable per-seek PRNG. Await fonts and asset decode. Register
frame sources early; provide `ready`, return asynchronous render work, honor
cancellation, and use `data-no-timeline` where no timeline exists. Give every timed
media element a stable ID: missing audio IDs can produce silent exports.

Verify repeated, reverse and shuffled seeks through the same render path. Include
cut ±1 frame samples and a motion-sensitive check: a frozen picture also passes
same-time equality. Do not hide failures by weakening pixel equality casually.

## 4. Prepare evidence and sound

Preserve original UI pixels, colours, attribution and meaningful context. Crop to
the content, not empty chrome. Recapture at a higher device scale when needed for
readable close-ups. Do not invent detail through upscaling or rebuild UI as a
convincing “real” screenshot. Use clearly identified editorial illustrations when
real footage is unavailable; keep missing-input proof status explicit.

For rhythm-led work, establish the actual tempo **and downbeat/phrase phase**.
Use one frame-indexed time map for audio, original footage and replayed highlights.
Round absolute beat boundaries to frames; avoid cumulative rounding drift. Do not
restart a running musical pattern at a scene or section change unless it really
restarts there. Derive audio-reactive graphics from real PCM analysis.

Use the supplied/permitted soundtrack. Original synthesis is an option when the
brief permits it, not a substitute for a specifically required recording. Shape
its arrangement around the edit. Preserve VO timing on locked edits. Measure the
**final encoded audio**; PCM measurements do not prove AAC true-peak compliance.

## 5. Review, render, verify

Run the smallest complete chain that establishes the requested deliverable:

1. Reproducible install/build, lint, runtime check.
2. Exact-time stills, full-resolution/preview-size review and cut-boundary review.
3. Seek determinism, motion/effect controls, source/copy/timing assertions.
4. One bounded render, followed by preview encode.
5. Encoded-file probe, full decode, frame/duration checks, audio checks, budgets,
   and the frame-0 money-shot check (extract frame 0; reject near-black and blank).
6. Inspect frames from the actual MP4; watch the export and audition audio when
   playback capabilities exist. Record unperformed listening/realtime review.

Canvas text is outside the framework's DOM contrast/layout analyzer. A report of
`0/0` text checks is **not** readability certification. Manually review dense frames
and use crop/text bounds checks as appropriate. Review expected warnings instead
of retiming a locked edit just to silence a heuristic.

Shared-host defaults: **one render, two workers, nice 19, two CPU cores where
supported, FFmpeg decoder/encoder/filter threads capped at two, no concurrent
browser-heavy jobs**. A worker count alone does not cap FFmpeg threads. Only delete
this project's derived frames; record cache ownership and avoid blanket cleanup.

Preserve the existing review file while rerendering. Render to a candidate name,
verify the candidate, then replace each published file atomically. Rerender after
any visual/copy change; new stills do not update an older MP4.

## 6. Deliver and preserve continuity

Write `REVIEW.md` / `TEST_REPORT.md` with exact commands, versions, measured values,
visual checks, source scope and unrun checks. Keep a compact `STATUS.md` for long
work: current source fingerprint, latest verified export, active job IDs/logs,
remaining steps and any served paths. On resume, inspect state before launching a
new job. Let asynchronous completion notifications drive follow-up; do not poll.

For Tailscale sharing, discover the actual assigned IP, choose an unused port,
serve only a dedicated output/share directory on that interface, and verify HTTP
success and size. Keep private review addresses out of committed/public files.
Do not present a URL as live before checking it.

Deliver the playable MP4 link/path first, then preview/contact sheet, actual
duration/resolution/frame rate/size, and the editable project location. Describe
creative choices concretely. Do not imply audio mastering, authentic behavior,
live Hermes use or perceptual quality was tested without evidence. Commit, push,
open a PR or publish publicly only when the user's scope calls for it; never merge
an explicitly review-only PR.
