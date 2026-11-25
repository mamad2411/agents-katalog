---
name: ccvideo
description: Make product promo videos in the Claude video team style — terracotta canvas, macOS terminal window, animated Claude Code session — with Remotion. Use when the user asks for a product/feature promo, launch video, terminal demo video, or a "Claude-style" video.
---

# ccvideo — Claude-style product promo videos

You are producing a short promo video (20–45 s, 1920×1080 @ 30 fps) in the
visual language of Anthropic's Claude launch videos: a warm terracotta canvas,
a single macOS terminal window running a Claude Code session, text that types
and streams in, brief camera pushes between locked framings, serif title cards.

## Prerequisites

1. A Remotion project must exist. If not, scaffold one:
   `npx create-video@latest --yes --blank --no-tailwind .` then `npm i`.
2. Packages (install with `npx remotion add <pkg>` so versions match):
   `@remotion/google-fonts`, `@remotion/transitions`, `zod` (declare zod
   explicitly — the library imports it directly; do not rely on it being a
   transitive dependency).
3. The component library must exist at `src/ccvideo/`. If it does not, copy
   every file from this skill's `templates/` directory into `src/ccvideo/`.
   Do not rewrite these components from scratch.
4. The capture/verify tooling must exist at `scripts/` in the project root.
   If it does not, copy this skill's `scripts/` directory (including
   `scripts/lib/`) there. All scripts resolve `captures/` against the
   directory you run them from, so always run them from the project root.

## Ground truth (non-negotiable content rules)

Video content is never hand-written into scene components. Every fact shown —
numbers, paths, endpoints, command output, line counts — must come from a
capture of something that really ran:

- Each video has a `captures/<name>/` directory holding raw artifacts (API
  responses, extracted session events) plus a `props.json` built from them
  deterministically. `props.json` is the single source of truth the
  composition renders.
- **Capture first.** Before making the video, run the real thing:
  - `node scripts/capture-xapi-cli.mjs` — live X data via the xapi CLI
    (`npx xapi-to`, key in `~/.xapi/config.json`; the `xapi` skill in
    `.agents/skills/xapi/` documents all its capabilities).
  - `node scripts/capture-x-user.mjs` — official X API variant (needs
    `X_BEARER_TOKEN`; `--sample` writes placeholder data with
    `raw-meta.json` marked `sample: true` — never publish a sample capture).
  - `node scripts/transcript-to-props.mjs <session.jsonl> --prompt-match
    <str> --out captures/<name>` — replay a real Claude Code session turn
    (transcripts live in `~/.claude/projects/<project-slug>/*.jsonl`).
  - New data source? Write a new capture script following the same pattern:
    fetch reality → save raw → build props via a shared deterministic
    builder in `scripts/lib/`.
- **Verify before publishing:** `node scripts/verify-props.mjs
  captures/<name>` rebuilds props from the raw artifacts and fails on any
  hand-edit. Fix by re-capturing, never by editing `props.json`.
- Honest-replay boundary: pacing is a performance (typing speed, spinner
  time), but capability must be real — the video may only show what the
  captured run actually did. This extends to chrome: session-header facts
  (Claude Code version, cwd) come from the capture (`claude --version`,
  real cwd) or the header is omitted; the spinner's token counter renders
  only when the capture provides a real `thinkingTokens` value (otherwise
  seconds only). Sample captures fail `verify-props` outright
  (`--allow-sample` exists solely for pipeline testing).
- Captures aim to be commit-safe, with defense in depth — not a guarantee:
  `transcript-to-props` persists only the inputs the video actually uses
  (the selected events' shown lines + counts, one truncated command output,
  the summary bullet lines), scrubs secret-shaped strings (API keys, Bearer
  tokens, URL credentials, env/JSON password fields, private keys), and
  rewrites both normal and slug-flattened home paths to `~` — all before
  props are built, so props, video, and archived raw see identical redacted
  content. Pattern lists can never be complete: always review a capture
  before committing, and treat any redaction warning as a stop sign.

## Workflow

1. **Capture first** (see Ground truth): produce `captures/<name>/props.json`
   from a real run.
2. **Beat sheet from the capture.** Presentational text (card titles,
   thinking word) lives in the capture script's constants/flags — pick the
   one prompt, the code beat, the run output, the summary bullets. Aim for
   the classic arc: code → created → ran+output → summary.
3. **Compose:** register a `<Composition>` in `src/Root.tsx` using
   `GroundedVideo` from `src/ccvideo` with `schema={groundedVideoSchema}`,
   `defaultProps` imported from the capture's `props.json`, and
   `calculateMetadata` deriving duration via `groundedVideoDuration` —
   durations follow content automatically. Custom scene work beyond the
   standard arc: build with the library primitives, same rules.
4. **Verify with stills** before declaring done. Render one still per beat:
   `npx remotion still <CompId> --frame=<n> --scale=0.5 out.png`
   and look at them. Check: nothing clipped by the terminal window (a
   `[ccvideo]` overflow warning in render output means trim beats), timing
   feels unhurried, colors match the palette.
5. Run `node scripts/verify-props.mjs captures/<name>`, then preview with
   `npx remotion studio --no-open`; final render with
   `npx remotion render <CompId> out/<CompId>.mp4` (add
   `--props=captures/<name>/props.json` to render a different capture
   without touching code; add `--scale=2` for a 4K master like the official
   demos — compositions stay 1920×1080 @ 30 fps in code).

## Two themes

Pick per product, both share the brand terracotta `#D97656`/`#D97757`:

- **Terracotta** (default) — warm canvas, Claude Code REPL session. For
  agent/AI-workflow stories. Components: `GroundedVideo`/`DataSession`.
- **Dark** (the `ant` CLI demo grammar) — near-black canvas `#0B0B0B`,
  warm-black terminal `#181716` separated only by a subtle border, shell
  prompt `▶ ~/dir >` (arrow `#8B92C9`, chevron `#5FA97B`), cream serif
  `#D6D4CF`. Structure is **chaptered**: pixel-logo wordmark card →
  [interstitial card (mono kicker + thin divider + serif claim) → fresh
  shell beat (type real command, real output fades in, idle prompt
  returns)] per chapter → wordmark outro. For CLI/developer-tool products.
  Components: `DarkVideo`/`ShellBeat`/`InterstitialCard`/`WordmarkCard`,
  palette `dark` in `theme.ts`, schema `darkVideoSchema` (built from
  captures like the light theme — e.g. `props-dark.json` written by
  `capture-xapi-cli.mjs`, verified by `verify-props.mjs`).

## The look (non-negotiable style rules)

- Canvas `#CC7D5D`, terminal `#2B2C36`, titlebar `#3A3634`. Body text
  `#E3E4EB`, dim `#9899A1`, comments `#6C6E6A`, line numbers `#83848C`.
  Accents: periwinkle `#B8B9F2` (paths, inline code, strings), teal `#85BEC5`
  (keywords), gold `#F2C43D` (status arrows). All defined in
  `src/ccvideo/theme.ts` — import, never hardcode.
- Fonts: JetBrains Mono for everything terminal, Source Serif 4 for title
  cards. Loaded in `theme.ts` via `@remotion/google-fonts`, with Noto Sans SC
  already appended as CJK fallback for both stacks — Chinese prompts render
  out of the box.
- Terminal window 1560×950 centered (985 when a session `header` is shown;
  dark theme 1860×1010), 14 px radius, deep soft shadow, three
  traffic lights, mono titlebar text that mirrors the task, e.g.
  `dev — · Implement X — claude — 106×31`.
- The Claude Code session must look real: `>` input row above a gold
  `⏵⏵ auto mode on (shift+tab to cycle) · esc to interrupt` status bar (both
  always visible, pinned to the bottom); a `✻ Cogitating…` spinner in a
  fixed-height slot just above the input row; `●` tool-result bullets; a
  numbered code block ending in `… +N lines (ctrl+o to expand)`; a bold
  `What it does` summary with `-` bullets.
- Camera: no sustained zoom or pan on terminal scenes, ever — slow
  fractional scaling makes small mono text visibly drift and swim. The only
  allowed camera motion is `<CutZoom>`: **brief, strongly-eased moves
  (~0.6 s) between otherwise locked framings** — push into dense content,
  hold, pull back for the payoff. Text may be mid-scale only during a
  deliberate fast move, never for seconds. Keep the same `origin` on the
  pull-out as the push-in so it doesn't read as a lateral slide.
  `DataSession` applies this automatically around the `run` beat.
  `<SlowZoom>` remains title-cards-only.
- Session authenticity chrome (all schema-driven, all optional):
  `header` (pixel logo + `Claude Code vX` + model/cwd line, always visible),
  `windowTitleIdle` → `windowTitle` swap at prompt submit, prompt echo as a
  highlighted block, spinner with live `(Ns · ↓ N tokens)` counters and an
  optional `⎿ Tip:` line, status bar that gains `esc to interrupt` only
  while working. Extra beat kinds: `answer` (rich prose block), `alert`
  (red-highlight row), `tool` beats may carry `⎿` children lines.
- **No transcript drift.** Terminal text may only fade in place: no
  positional entrance animations inside the window, and never mount/unmount
  an element that reflows lines below it — transient rows (spinners,
  progress) live in fixed-height slots so their disappearance shifts nothing.
- Title cards: serif headline in near-black `#1F1508` on the terracotta,
  mono subtitle at 68 % opacity, fade-up entrance. Headline ≥ 132 px,
  subtitle ≥ 52 px at 1920 wide.

## Component API (`src/ccvideo`)

Data-driven layer (preferred for whole videos):

- `<GroundedVideo {...props}>` — intro card → session → outro card, entirely
  from a `groundedVideoSchema` value (a capture's `props.json`).
- `<DataSession {...props.session}>` — renders any `sessionSchema` value:
  optional header, prompt typing, spinner, then `beats` (discriminated
  union: `code`, `tool`, `run`, `summary`, `answer`, `alert`). Applies the
  run-beat cut-zoom automatically; warns at render time if content will
  overflow.
- `sessionTiming(props, fps)` / `groundedVideoDuration(props, fps)` — pure
  timing derivation; use in `calculateMetadata`.
- `<Rich segments>` — renders JSON segments `{t: 'plain'|'kw'|'code'|
  'comment'|'dim'|'bold', s}`; the bridge from props.json to styled text.

Presentation primitives:

- `<TerminalWindow title width? height? variant?>` — window on the canvas
  (`variant="dark"` for the dark theme). Children
  are a flex column; give the transcript `flex: 1` so `<InputBox>` +
  `<StatusBar>` pin to the bottom.
- `<TypeText text from cps? cursor?>` / `<Cursor>` — typewriter, 35–45 cps.
- `<InputBox typedText? from? cps?>` — `>` row; no `typedText` = blinking cursor.
- `<StatusBar mode? hint?>`.
- `<Thinking from? until? word? stats? tokens? tip?>` — spinner; `stats`
  shows live `(Ns)` — plus `↓ N tokens` only when `tokens` carries a real
  captured count; `tip` adds a `⎿ Tip:` line. Put it in a fixed-height slot
  between transcript and input; `until` fades it out in place.
- `<Line from?>` — one output row, 8-frame fade-in (opacity only).
- `<ToolLine from>` — `●` bullet row.
- `<CodeBlock from lines stagger? startLineNo? expandNote?>` — numbered lines.
- Token spans: `<K>` keyword, `<C>` code/path, `<Cm>` comment, `<Dim>`, `<B>`.
- `<SessionHeader version modelLine>`, `<PromptEcho>`, `<AlertLine from?>`,
  `<ToolChild from?>` — session chrome (see style rules).
- `<CutZoom cuts={[{from, scale?, origin?, ease?}]}>` — brief eased moves
  between locked framings; the only camera motion allowed on terminal scenes.
- `<SlowZoom from? to?>` — title cards only, never around a terminal.
- `<TitleCard title subtitle? titleSize?>`.

All animation is frame-driven (`useCurrentFrame` + `interpolate`, clamped,
inline in `style`). Never use CSS `transition`/`animation`.

## Timing cookbook (30 fps session scene, ~14 s)

`DataSession` derives all of this automatically via `sessionTiming` — the
table below is for hand-built custom scenes only.

| Beat | Frame |
|---|---|
| Idle window, cursor blinking | 0–20 |
| Prompt types (`cps≈38`) | 20–105 |
| Prompt echoed as highlighted block, input clears | ~110 |
| `✻ Thinking…` spinner | 115–170 |
| Code block streams (stagger 4) | 170–240 |
| `●` tool result | ~240 |
| `What it does` + bullets (stagger ~16) | 268–330 |
| Hold on final state | ≥ 2 s |

Sequence the swaps with `<Sequence from/durationInFrames layout="none">`.
Let output beats breathe — when in doubt, slower. Transitions overlap scenes:
total duration = sum of scenes − sum of transition frames.

## Worked examples (patterns to reproduce)

The bundled scripts are themselves complete worked examples:

- **API-capture video** (`scripts/capture-xapi-cli.mjs` + both builders in
  `scripts/lib/build-props.mjs`) — one capture run produces a terracotta
  Claude Code session video *and* a dark chaptered CLI video from the same
  raw data. The run-output beats replay the script's real stdout, `+N lines`
  is the script's real line count, and the session header carries the real
  `claude --version` and cwd.
- **Session-replay video** (`scripts/transcript-to-props.mjs`) — converts a
  real Claude Code session turn (JSONL transcript) into a video script,
  with redaction and minimal storage built in. Handles CJK prompts via the
  bundled font fallback.

Register the resulting `props.json` on a `GroundedVideo` (terracotta) or
`DarkVideo` (dark) composition as described in the Workflow section.
