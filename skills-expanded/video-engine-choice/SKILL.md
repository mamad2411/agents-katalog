---
name: video-engine-choice
description: "Use when starting any video job. Picks fframes or HyperFrames before any code."
version: 2.1.0
author: media role of hermes-fleet-apps
license: MIT
---

# Video engine choice: fframes or HyperFrames

Two code-first video engines cover most jobs. Pick one **before** writing code, and
state the pick and its reason to the owner in one line. The rule below comes from
side-by-side tests (fframes vs Remotion vs HyperFrames, same videos, same machine);
the numbers are kept so the rule can be re-judged.

- fframes: Rust, `github.com/dmtrKovalenko/fframes`, MIT.
- HyperFrames: HTML/CSS/JS rendered in headless Chrome, `github.com/heygen-com/hyperframes`,
  Apache-2.0.

## The rule

| Job | Engine |
|---|---|
| Presentation video, explainer, chart / data animation, kinetic typography, title cards | **fframes** (default) |
| Demo of an app's own UI (rebuilding its HTML/CSS), README GIF, screencast-style | **HyperFrames** |
| Needs CSS layout: text that wraps by itself, flexbox, variable-font weight animation | **HyperFrames** |
| Maths / equations animation | Manim (bundled Hermes skill `manim-video`: this role is created with `--no-skills`, so install it if you want it) |

Remotion is not used: every composition it made in the tests was rebuilt in HyperFrames
at SSIM >= 0.996 mean, same frame counts, file sizes -0.2..+3.5 %, and its licence is
source-available, not open source. If a job seems to need it, stop and ask the owner.

When a job fits two rows, the more specific one wins (a presentation that is
mostly app screens -> HyperFrames). Still unsure: pick fframes and say why.

## Why (so the rule can be re-judged, not just obeyed)

- Built-in checks on 6 planted defects: fframes 5/6, HyperFrames 3/6 (+ a
  contrast warning), Remotion 2/6. HyperFrames names missing fonts/files
  (`lint`) and off-canvas text (`check`).
- HyperFrames SWALLOWS exceptions thrown in timeline callbacks: no log, exit 0,
  frame shipped. It also silently clamps audio gain. fframes prints the panic
  (then hangs). Keep logic out of HyperFrames callbacks.
- Render of a 57 s 1080p video, same session: fframes 20.7 s, HyperFrames 36.8 s,
  Remotion 44.7 s. The GPU barely matters for any of them: speed is never the argument.
- Edit -> one frame: Remotion ~4-5 s, HyperFrames 7.1 s, fframes ~19-20 s.
- Licences: fframes MIT; HyperFrames Apache-2.0 (GSAP, which its examples use, ships
  under GreenSock's own no-charge licence, not an OSS licence); Remotion
  source-available, free only for small teams.
- README GIFs (8-12 s, 800 px): HyperFrames 12-25 s end to end vs Remotion 6-8 s.
  Slower, but seconds; never the argument.
- HyperFrames `check` found 3 real issues in GIFs Remotion had rendered without a word
  (truncated captions, a toast over captions, 4.24:1 key-cap contrast).
- Privacy: HyperFrames sends telemetry by default. Set `HYPERFRAMES_NO_TELEMETRY=1`
  (or `DO_NOT_TRACK=1`) in every shell that runs it, before the first command.

Kinetograph 0.2.0 (renders HyperFrames/Remotion projects without Chrome) was tested and
rejected: on Windows every local image failed to load, the `window.__hyperframes`
helpers were missing (a composition that uses them crashed), sub-compositions beyond
the first were blank, SSIM 0.88-0.90, and it exited 0 anyway. Licence PolyForm Small
Business (not OSS). Re-test only when a release fixes Windows local paths and
`window.__hyperframes`.

## Re-evaluate when

HyperFrames reports exceptions from seek callbacks, fframes fixes the
render hang on a panic or the variable-font weights, or either engine loses
its built-in checks.
