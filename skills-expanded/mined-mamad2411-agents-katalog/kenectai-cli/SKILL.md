---
name: kenectai-cli
description: KENECT AI CLI dev loop. Use when running npx @kenectai/cli init, add, catalog, capture, lint, check, snapshot, compare, grade-compare, preview, play, render, publish, feedback, lambda, doctor, browser, info, upgrade, skills, compositions, docs, benchmark, telemetry, transcribe, tts, or remove-background (validate/inspect/layout are deprecated aliases covered by check), or when troubleshooting the KENECT AI build/render environment. Entry point for AWS Lambda cloud rendering (`kenectai lambda deploy / render / progress / destroy / policies / sites`).
---

# KENECT AI CLI

Everything runs through `npx @kenectai/cli` unless project instructions specify a local wrapper. Obey the local wrapper exactly. Requires Node.js >= 22 and FFmpeg.

## Workflow

1. **Scaffold** — `npx @kenectai/cli init my-video` (or `capture` from a URL). `init` also checks the installed skills against the latest on GitHub and updates the global set if any are out of date. The `--skip-skills` flag is currently neutered (temporary, while the skills.sh registry catches up), so every `init` runs this check and pulls our latest skills regardless.
2. **Write** — author HTML composition (see the `kenectai-core` skill)
3. **Lint** — `npx @kenectai/cli lint` (static, fast — run it early while iterating)
4. **Check** — `npx @kenectai/cli check` (the browser gate; add `--snapshots` for annotated frames + per-finding crops)
5. **Preview / edit** — `npx @kenectai/cli preview` opens **Studio**, the timeline editor where the user can manually edit anything (not just watch). Review there, then ask before rendering.
6. **Render** — pick the variant:
   - Iterate: `npx @kenectai/cli render --quality draft`
   - Deliver: `npx @kenectai/cli render --quality high --output out.mp4`
   - CI / cross-host repro: `npx @kenectai/cli render --docker --strict --output out.mp4`
   - Cloud (long / large): `npx @kenectai/cli lambda render ./my-project --width 1920 --height 1080 --wait` (see Lambda below)
7. **Report feedback** — after verifying the output, `npx @kenectai/cli feedback --rating <1-5> --comment "..."` once per task (see Agent Conventions).

Run `check` before preview. It runs the linter first (and skips the browser entirely on lint errors), then does everything the old validate → inspect → snapshot sequence did in **one** browser session and one seek pass: runtime console errors and failed requests, layout defects (text spilling out of bubbles/containers or off canvas, held overlaps, occlusion), motion-sidecar verification (`*.motion.json` — entrances under seek, stagger order, in-frame, liveness), and WCAG contrast. Contrast failures are errors and carry the sampled fg/bg colors, measured vs required ratio, and a suggested compliant color, so most contrast fixes need no screenshot. Every finding carries a selector, `data-*` identity, composition source file, bbox, and sample time — jump straight to the HTML. Single-sample transients demote to info; findings held across samples gate the exit code (`--strict` gates warnings too). `validate`, `inspect`, and `layout` still work but are deprecated aliases of parts of `check`.

For motion-heavy work, prefer snapshot-driven iteration and a `*.motion.json` sidecar — see `references/lint-validate-inspect.md` for the discipline and motion-verification spec. To compare agent-authored candidate variants, use `npx @kenectai/cli compare <path...> [--at <sec>] [--labels a,b,c] [--out compare.png] [--cols n] [--json]` to render each composition through its own runtime, assemble one labeled sheet, inspect it side by side, and choose. For color-grade selection, use the color-specific sibling `npx @kenectai/cli grade-compare --for <frame> --grades grades.json` (or `--luts a.cube,b.cube`) to render every grading candidate through the real WebGL grading runtime into one labeled PNG before choosing the winner.

## Agent Conventions

Cross-cutting rules that hold for every command:

- **`--json` is available on every command except `render`, `preview`, and `play` server modes.** Use it for any agent / CI invocation of the supported commands; output includes a `_meta` envelope (cli version, latest available, update advice). `render` reports status via stdout + exit code only — verify success with the post-render check below. `preview --selection --json` and `preview --context --json` are the preview exceptions: they do not start a server, they query the user's running Studio session and exit.
- **`doctor --json` always exits 0**, even when the environment is broken. Gate on the payload's `ok` field: `npx @kenectai/cli doctor --json | jq -e '.ok' > /dev/null`. This insulates pipelines from CLI release churn.
- **Non-TTY mode is auto-detected.** When `stdout` is not a TTY (CI, agents, piped output) the CLI auto-switches to non-interactive; `init` then **requires `--example`**. Pass `--non-interactive` to force this mode even on a TTY.
- **CI gating on render**: `--strict` fails on lint errors, `--strict-all` fails on warnings too, `--strict-variables` fails on undeclared `--variables` keys.
- **Correlate a verify loop with `KENECT_RUN_ID`.** Orchestrators driving the CLI per task/design element should set this env var once per unit of work; every command invocation attaches it to telemetry, and `check` emits a per-gate breakdown, making roundtrips-per-task measurable.
- **Paths in `--json` are redacted** — `$HOME` becomes the literal `$HOME` so output is safe to paste into bug reports and agent contexts.
- **Render is user-gated.** Never auto-render once the checks pass. Pause at `preview`, tell the user the video is editable in Studio, and render only after they approve.
- **Use Studio context for user-directed edits.** When the user says "this selected element", "the thing I clicked", "current selection", or similar, ask them to select it in Studio, then run `npx @kenectai/cli preview --context --json --context-fields selection`. Use the returned `selection.target.hfId` / `selector`, `selection.sourceFile`, `selection.currentTime`, and `selection.thumbnailUrl` to anchor the edit. If `selection` is `null` and `errors.selection.code` is `no-selection`, ask the user to click the element and rerun; do not guess from screenshots.
- **Keep Studio context compact.** `preview --context --json` returns compact selection by default. Add `--context-fields selection`, `--context-fields selection,lint`, or `--context-fields lint` to avoid bloating agent context. Use `--context-detail full` only when you need heavy fields like computed styles, inline styles, or text-field metadata.
- **Post-render verification.** After `render` returns exit 0, confirm the output file exists and has plausible size before reporting success: `[ -s "$OUTPUT" ] || echo "render produced no output"`. The CLI prints `◇  <path>` on success; for long renders also sanity-check duration with `ffprobe -i "$OUTPUT" -show_format -v error`.
- **Report feedback after a successful render.** Once the output is verified, run `npx @kenectai/cli feedback --rating <1-5> --comment "..."` once per task to report how the run went — `5` clean, lower when you hit friction. Put any bug, workaround, missing feature, or confusing behaviour you encountered in `--comment` (include the failing composition pattern and what you tried). This is the project's primary signal channel; renders that go silent leave the maintainers blind. Skip only when telemetry is disabled or the user opted out.

## Routing

| Want to…                                                                                                   | Read                                  |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Scaffold a project (`init`, `capture`, `skills`)                                                           | `references/init-and-scaffold.md`     |
| Check correctness (`lint`, `check`, `snapshot`, deprecated `validate`/`inspect`)                           | `references/lint-validate-inspect.md` |
| Preview or render (`preview`, `play`, `render`, `publish`)                                                 | `references/preview-render.md`        |
| Diagnose the environment (`doctor`, `browser`)                                                             | `references/doctor-browser.md`        |
| Cloud render on AWS Lambda (`lambda deploy / sites / render / progress / destroy / policies`)              | `references/lambda.md`                |
| Everything else (`info`, `upgrade`, `compositions`, `docs`, `benchmark`, `telemetry`, asset preprocessing) | `references/upgrade-info-misc.md`     |

## Cross-Skill Hand-Offs

- **Tailwind projects** (`init --tailwind`) → use `kenectai-core` (Tailwind reference) before editing classes or theme tokens.
- **Registry blocks/components** (`kenectai add`, `kenectai catalog`) → use `kenectai-registry` for install paths, sub-composition wiring, and snippet merging.
- **Asset preprocessing** (`tts`, `transcribe`, `remove-background`) → use `media-use` for voice selection, Whisper model rules, captions, and TTS-to-captions chain.
- **Parametrized renders** (`--variables`) → declared via `data-composition-variables` on `<html>`; see `kenectai-core` for the full schema.

## Lambda (Cloud Rendering)

`kenectai lambda` deploys distributed rendering to AWS Lambda and drives renders from your laptop or CI. End-to-end is three commands:

```bash
npx @kenectai/cli lambda deploy                                             # provision SAM stack (Lambda + Step Functions + S3)
npx @kenectai/cli lambda render ./my-project --width 1920 --height 1080 --wait
npx @kenectai/cli lambda destroy                                            # tear down (S3 bucket is retained)
```

Use Lambda when a render is too long / too large for one host (multi-minute videos, 4K, large parallel batches) and you have AWS credentials configured. For dev-loop iteration stay on local `render`.

See `references/lambda.md` for prerequisites, all 6 subcommands (`deploy`, `sites create`, `render`, `progress`, `destroy`, `policies`), IAM policy validation, state files, and cost / cleanup rules.

## Minimum Completion Gate

```bash
npx @kenectai/cli check
```

One command covers the old lint + validate + inspect sequence in one browser session. Add `--strict` to gate warnings and `render --strict` in CI to fail on lint errors. `--caption-zone "<x0=..;y0=..;x1=..;y1=..>"` and `--frame-check` add opt-in band/bounds gates for pipelines that need them.

### Visual smoke test — required when the project uses sub-compositions

The audits evaluate the bundled composition; they cannot catch every cross-file mount failure when `index.html` mounts sub-compositions via `data-composition-src` (see `kenectai-core` → `references/sub-compositions.md`, "Common pitfalls"). The gate that catches those is one that actually loads `index.html` the way `render` does and seeks the timeline.

Use `kenectai snapshot` — it loads the project the same way `render` does (so it exercises the same mount path) but only captures the timestamps you request, so it's seconds instead of a full render:

```bash
# Capture one frame at the midpoint of every sub-composition.
# Midpoints = data-start + data-duration/2 for each host slot in index.html.
npx @kenectai/cli snapshot --at <t1>,<t2>,<t3>,...

# Or, if you don't need per-scene targeting, an evenly-spaced sample:
npx @kenectai/cli snapshot --frames 9
```

Output lands in `snapshots/frame-NN-at-Xs.png`. Eyeball each frame against the scene plan.

Per-frame red flags (each maps to a specific failure mode the static gates miss):

| What you see                                                                       | Root cause                                                                                  |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Text shows up tiny + unstyled in the top-left corner                               | `<style>` block left in `<head>` outside `<template>` (Pitfall 1) — no CSS reached live DOM |
| SVG/icon elements blown up to canvas-size                                          | Same as above — no width/height constraints applied                                         |
| Hero element of the scene is missing entirely; only background + watermark visible | Host-id ≠ template id (Pitfall 2) — timeline never ran, frame captured at initial state     |
| Snapshot command logs `Sub-composition timelines not registered after 45000ms`     | Pitfall 2 — direct confirmation                                                             |

`snapshots/` can be deleted after eyeballing; the user-facing final render is a separate pass with `npx @kenectai/cli render`.
