---
name: video-polish-qa
description: Use when refining or shipping a Hyperframes HTML video composition (GSAP, CSS, or Anime.js motion) - timestamped visual feedback, off-center or misaligned text, cards, or price groups, uneven card rows, wrapped headings breaking baselines, animations overlapping or jumping, SVG connector lines appearing before their origin, a weak final or closing screen, or a final pass before rendering and verifying the exported MP4 (duration, FPS, codecs, preserved audio).
license: MIT
metadata:
  author: "@AdiCoSto"
  x: https://x.com/AdiCoSto
  repository: https://github.com/rocksstarcode/hyperframes-video-polish
  version: "1.2.0"
---

# Polish and verify a Hyperframes video

Use for visual refinements, timestamped feedback, or a final production pass on a Hyperframes composition. Resolve the project's entry point, output folder, and render commands from its own package scripts, README, or agent instructions; do not assume filenames. Preserve audio and scene timing for visual-only work unless a requested change requires retiming.

**Core principle:** find the cause in the source and prove the fix on the rendered MP4. A still that looks right, a clean exit code, or a passing sampler is evidence, not proof.

## Quick reference: symptom to likely cause

| Symptom | Check first |
| --- | --- |
| Text or group sits slightly off-center | Guessed `left` instead of a centering helper; lost `xPercent: -50` after a scale/translate tween; negative letter spacing; a unit label left out of the group width |
| Card row drifts left or right | Start x not derived from `count * cardWidth + (count - 1) * gap` |
| Icons or lower rows misaligned across cards | One-line vs wrapped headings without a shared reserved title height |
| Element "jumps" or settles in the wrong place | Two tweens writing the same transform; a still captured mid-tween |
| Connector line or dot visible too early | Path hidden only by dash offset (round caps leak) or a static base path; diagram not staged origin-first |
| Row shifts while cards are still entering | Secondary motion starts before `start + (count - 1) * stagger + duration` |
| Verifier says duration is ~50 ms too long | Container duration includes AAC padding; the bundled verifier judges the video stream |

## Resolve project context

1. Read the project's package scripts and docs before running anything. Confirm the composition entry (HTML/JS/CSS), lint/check/snapshot commands, render command, and where exports belong. Run `npx hyperframes compositions` when the project may hold more than one composition, and target the right one (`render -c <file>`).
2. Record the output spec: format (MP4, WebM, MOV, GIF, HLS, or PNG sequence), canvas size (`data-width`/`data-height` or `--resolution`), and frame rate (`--fps`, else the root `data-fps`, else 30). The export check uses these values.
3. Identify the project's revision convention. Keep new exports distinct and inside the project's output folder; do not overwrite a prior verified cut.
4. Read the current composition source. Treat docs and earlier review notes as dated evidence; revalidate against the actual source when they disagree.

## Diagnose the visible state

1. Inspect the actual composition and feedback frames. Map each timestamp to its clip and animation with the CLI first, then confirm in source:
   - `npx hyperframes timeline --json`: tracks, clips, and their start/end times.
   - `npx hyperframes keyframes --selector "<css>" --json`: the GSAP tweens, CSS `@keyframes`, or Anime.js timelines driving an element.
   - `npx hyperframes keyframes --selector "<css>" --shot <file>.png`: an onion-skin image of the element across time, which shows drift, overshoot, and paths drawn early.

   Then read the matching JS and CSS. Command flags change between versions; check `npx hyperframes <command> --help` before relying on one.
2. Reproduce the problem at its start, midpoint, and settled state. An offset may be a tween still running rather than a wrong coordinate. Capture both sides of a scene boundary when a transient is involved.
3. Identify the cause before adding another transform: fixed offsets, mismatched widths, unequal text heights, transform-origin errors, early visibility, or multiple tweens writing the same property. Fix the underlying layout or timing.

## Alignment invariants

- Center a text block geometrically, not with guessed `left` coordinates: a centered-box helper should center the box and text. An intrinsic-group helper should center logos, price groups, and chips. Preserve `xPercent: -50` when applying scale or translation.
- For equal-width rows, derive the starting x from the complete group width: `count * cardWidth + (count - 1) * gap`. Subtract from canvas width and divide by two. Keep a shared y, card height, and padding.
- Align contents too: one-line and wrapping headings need a shared reserved height to keep icons, avatars, and lower rows on the same baseline. For example, one verified composition reserved a fixed flex-centered title area so wrapped titles did not push cards out of line.
- Keep price plus unit in one centered group. A smaller unit label still contributes to the group's width. Test estimate labels, usage statements, slogans, and domains independently.
- Check actual rendered text bounds and optical balance at normal viewing size. A centered parent does not guarantee that a child group, wrapped title, or negative letter spacing looks centered.

## Motion invariants

- Stage causal diagrams: introduce the origin, move it into position, reveal the nodes or endpoints, then draw the connections outward. Never show floating paths before their origin is established.
- Hide SVG paths with opacity as well as stroke dash offset, then enable them at draw time. Dash hiding alone can leave round-cap artifacts; a separate static base path can still leak into the frame.
- Let row entrances finish before secondary movement starts. For a uniform stagger, last completion = `start + (count - 1) * stagger + duration`. Account for different durations when relevant. Use an independent overlay for card emphasis when the row itself must not move.
- Do not stack two tweens on the same transform property unless the overlap is intentional and verified. Prefer a nested element or an opacity/border accent for emphasis during a parent's move.
- Add emphasis with a clear reveal and resolution: word stagger plus underline, a coordinated icon pulse, or a short rotation of a single glyph. Return to a stable readable state and hold it long enough to absorb.
- Reduced-motion branches affect browser preview only. They do not make a rendered MP4 respond to a viewer's preferences; offer a calmer export if requested.

## Narrative and closing pass

Remove incidental production labels and repeated filler without removing meaningful sections. Retain billing terms, estimate/range labels, and proof figures that qualify a claim. Generic example cards must not masquerade as live recorded data.

Treat the final screen as a conclusion, and choose its parts from the film's purpose:

- Product or offer film: brand, price or offer, included usage where applicable, a large properly cased domain, then the slogan.
- Explainer or tutorial: the one takeaway, then the next step (link, command, or call to action).
- Brand sting or social clip: logo lockup and handle or domain; nothing that competes with them.

Animate the reveal and leave a settled hold long enough to read. Adapt the structure rather than copying one layout everywhere.

## Verify before export

Run the project's own commands; the following is a verified pattern, not a guarantee for every Hyperframes version:

```powershell
node --check <composition-entry>.js
npx --no-install hyperframes lint --json
npx --no-install hyperframes check --at-transitions --samples 18 --max-issues 8 --json
npx --no-install hyperframes snapshot --at "<scene-specific times>" --output <review-dir>
```

`check` runs lint, runtime errors and missing assets, layout overflow, motion, and contrast in one pass; `--at-transitions` adds samples at every tween start and end, where transient overlaps appear. Use `--range <start>,<end>` to focus on an edited scene. Prefer the project's own `npm run` wrappers when they exist.

Choose timestamps from the film's beats and boundaries, not from another project. Inspect the images, not only the exit status. Check early/mid/settled states, the longest label, every price or data card revealed, and the closing hold. Watch revised motion in preview or short output clips when stills cannot resolve timing or trajectory concerns.

Interpret reports honestly: layout/contrast/craft sampling does not prove every frame is correct, and `motion.enabled: false` means automated motion analysis did not run. Resolve reported problems or document their specific limitations before calling the cut verified. If a flag is unsupported, check `npx hyperframes --help` for the current interface.

## Render and verify the artifact

Quote paths containing spaces. Choose a distinct output name; a configured render command may overwrite its default output. Keep revisions and companion exports in the project's documented output folder. GPU encoding (`--gpu`) and browser GPU rendering (`--no-browser-gpu`) are independent choices; more workers are not automatically faster or safer. Validate performance flags on the machine doing the render.

Run the render in the foreground, track it to completion, then verify the export with the bundled script (Node 18+, `ffmpeg`/`ffprobe` on PATH). Always pass the output spec recorded earlier; width, height, and FPS are only reported, not enforced, when omitted:

```powershell
node <skill-dir>/scripts/verify-video.mjs --video "<output>" --expected-duration <seconds> --fps <fps> --width <px> --height <px>
```

The format is detected from the path: `.mp4`, `.webm`, `.mov`, `.gif`, an HLS `.m3u8` or its output folder, or a PNG-sequence folder. It checks codecs for that format, size, frame rate, duration and frame count from the video stream (container duration includes AAC padding), audio/video drift (limit 0.25 s, `--max-audio-drift`), and a full decode of every frame.

| Export | Add |
| --- | --- |
| No soundtrack | `--no-audio` (otherwise a missing audio stream fails) |
| Transparent MOV, WebM, or PNG sequence | `--alpha` to require the alpha channel (the composition background must itself be transparent; GIF transparency cannot be checked) |
| GIF | Frame rate is matched to GIF's centisecond timing; frame count is not enforced |
| PNG sequence | `--fps` is required to check duration |
| Visual-only revision | `--reference "<previous-cut>"` to require byte-identical encoded audio |

On Windows, `powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>/scripts/verify-video.ps1 -Video "<output>" -ExpectedDuration <s> -ExpectedFps <fps> -ExpectedWidth <px> -ExpectedHeight <px>` runs the same checks (`-NoAudio`, `-Alpha`, `-ReferenceVideo`, `-Format`) and returns an object.

Extract and inspect key frames from the actual export, including proof, pricing, and closing. Listen across edited boundaries if audio timing or content changed. Preserve source audio, evidence images, and earlier exports. Never fix a visual problem by quietly altering the recording.

Report what was checked and any unresolved issue. Offer the actual output with an absolute path. Do not state that the user has reviewed the file until they say so.

## Common mistakes

- Adding a compensating offset instead of removing the cause (stacked tweens, wrong group width).
- Judging alignment from a frame captured while a tween is still running.
- Reusing another film's snapshot timestamps instead of this film's beats and boundaries.
- Rendering over the previous verified cut, or retiming audio during a visual-only pass.
- Reporting "verified" from `check` output alone without opening the stills and the exported frames.
- Verifying against assumed defaults instead of the render's real format, size, and frame rate.

Field-tested on a Hyperframes product film and on stock `hyperframes init` examples (landscape and portrait, every render format) with Hyperframes 0.8. Revalidate the commands when the framework version or project structure changes; source remains authoritative.
