---
name: framevideo-cli
description: FrameVideo CLI dev loop — `npx framevideo` for scaffolding (init), validation (lint, inspect), preview, render, and environment troubleshooting (doctor, browser, info, upgrade). Use when running any of these commands or troubleshooting the FrameVideo build/render environment. For asset preprocessing commands (`tts`, `transcribe`, `remove-background`), invoke the `framevideo-media` skill instead.
---

# FrameVideo CLI

Everything runs through `npx framevideo`. Requires Node.js >= 22 and FFmpeg.

## Workflow

1. **Scaffold** — `npx framevideo init my-video`
2. **Write** — author HTML composition (see the `framevideo` skill)
3. **Lint** — `npx framevideo lint`
4. **Visual inspect** — `npx framevideo inspect`
5. **Preview** — `npx framevideo preview`
6. **Render** — `npx framevideo render`

Lint and inspect before preview. `lint` catches missing `data-composition-id`, overlapping tracks, and unregistered timelines. `inspect` opens the rendered composition in headless Chrome, seeks through the timeline, and reports text spilling out of bubbles/containers or off the canvas.

## Scaffolding

```bash
npx framevideo init my-video                        # interactive wizard
npx framevideo init my-video --example warm-grain   # pick an example
npx framevideo init my-video --video clip.mp4        # with video file
npx framevideo init my-video --audio track.mp3       # with audio file
npx framevideo init my-video --example blank --tailwind # with Tailwind v4 browser runtime
npx framevideo init my-video --non-interactive       # skip prompts (CI/agents)
```

Templates: `blank`, `warm-grain`, `play-mode`, `swiss-grid`, `vignelli`, `decision-tree`, `kinetic-type`, `product-promo`, `nyt-graph`.

`init` creates the right file structure, copies media, transcribes audio with Whisper, and installs AI coding skills. Use it instead of creating files by hand.

When using `--tailwind`, invoke the `tailwind` skill before editing classes or theme tokens. The scaffold uses Tailwind v4.2 via the browser runtime, not Studio's Tailwind v3 setup.

## Linting

```bash
npx framevideo lint                  # current directory
npx framevideo lint ./my-project     # specific project
npx framevideo lint --verbose        # info-level findings
npx framevideo lint --json           # machine-readable
```

Lints `index.html` and all files in `compositions/`. Reports errors (must fix), warnings (should fix), and info (with `--verbose`).

## Visual Inspect

```bash
npx framevideo inspect                 # inspect rendered layout over the timeline
npx framevideo inspect ./my-project    # specific project
npx framevideo inspect --json          # agent-readable findings
npx framevideo inspect --samples 15    # denser timeline sweep
npx framevideo inspect --at 1.5,4,7.25 # explicit hero-frame timestamps
```

Use this after `lint` and `validate`, especially for compositions with speech bubbles, cards, captions, or tight typography. It reports:

- Text extending outside the nearest visual container or bubble
- Text clipped by its own fixed-width/fixed-height box
- Text extending outside the composition canvas
- Children escaping clipping containers

Errors should be fixed before rendering. Warnings are surfaced for agent review; add `--strict` to fail on warnings too. Repeated static issues are collapsed by default so JSON output stays compact for LLM context windows. If overflow is intentional for an entrance/exit animation, mark the element or ancestor with `data-layout-allow-overflow`. If a decorative element should never be audited, mark it with `data-layout-ignore`.

`npx framevideo layout` remains available as a compatibility alias for the same visual inspection pass.

## Previewing

```bash
npx framevideo preview                   # serve current directory
npx framevideo preview --port 4567       # custom port (default 3002)
```

Hot-reloads on file changes. Opens the studio in your browser automatically.

When handing a project back to the user, use the Studio project URL, not the
source `index.html` path:

```text
http://localhost:<port>/#project/<project-name>
```

Use the actual port from the preview output and the project directory name. For
example, after `npx framevideo preview --port 3017` in `codex-openai-video`,
report `http://localhost:3017/#project/codex-openai-video`.

Treat `index.html` as source-code context only. It is fine to link it as an
implementation file, but do not label it as the project or preview surface.

## Rendering

```bash
npx framevideo render                                # standard MP4
npx framevideo render --output final.mp4             # named output
npx framevideo render --quality draft                # fast iteration
npx framevideo render --fps 60 --quality high        # final delivery
npx framevideo render --format webm                  # transparent WebM
npx framevideo render --docker                       # byte-identical
```

| Flag                 | Options               | Default                    | Notes                                                              |
| -------------------- | --------------------- | -------------------------- | ------------------------------------------------------------------ |
| `--output`           | path                  | renders/name_timestamp.mp4 | Output path                                                        |
| `--fps`              | 24, 30, 60            | 30                         | 60fps doubles render time                                          |
| `--quality`          | draft, standard, high | standard                   | draft for iterating                                                |
| `--format`           | mp4, webm             | mp4                        | WebM supports transparency                                         |
| `--workers`          | 1-8 or auto           | auto                       | Each spawns Chrome                                                 |
| `--docker`           | flag                  | off                        | Reproducible output                                                |
| `--gpu`              | flag                  | off                        | GPU-accelerated encoding                                           |
| `--strict`           | flag                  | off                        | Fail on lint errors                                                |
| `--strict-all`       | flag                  | off                        | Fail on errors AND warnings                                        |
| `--variables`        | JSON object           | —                          | Override variable values declared in `data-composition-variables`  |
| `--variables-file`   | path                  | —                          | JSON file with variable values (alternative to `--variables`)      |
| `--strict-variables` | flag                  | off                        | Fail render on undeclared keys or type mismatches in `--variables` |

**Quality guidance:** `draft` while iterating, `standard` for review, `high` for final delivery.

**Parametrized renders:** the composition declares its variables on the `<html>` root with **`data-composition-variables`** — a JSON **array of declarations** (`{id, type, label, default}` per entry) that defines the schema. Scripts inside read the resolved values via `window.__framevideo.getVariables()`. The CLI **`--variables '{"title":"Q4 Report"}'`** is a JSON **object keyed by id** that overrides those declared defaults for one render; missing keys fall through, so the same composition runs unchanged in dev preview and in production. (Sub-comp hosts can also override per-instance with **`data-variable-values`** — same object shape, scoped to one mount of the sub-composition. See the `framevideo` skill for the full pattern.)

## Asset Preprocessing

`npx framevideo tts`, `transcribe`, and `remove-background` produce assets (narration audio, word-level transcripts, transparent video) that get dropped into a composition. Each downloads its own model on first run. For voice selection, whisper model rules (the `.en`-translates-non-English gotcha), output format choice (VP9 alpha WebM vs ProRes), and the TTS → transcribe → captions chain, invoke the `framevideo-media` skill.

## Troubleshooting

```bash
npx framevideo doctor       # check environment (Chrome, FFmpeg, Node, memory)
npx framevideo browser      # manage bundled Chrome
npx framevideo info         # version and environment details
npx framevideo upgrade      # check for updates
```

Run `doctor` first if rendering fails. Common issues: missing FFmpeg, missing Chrome, low memory.

## Other

```bash
npx framevideo compositions   # list compositions in project
npx framevideo docs           # open documentation
npx framevideo benchmark .    # benchmark render performance
```
