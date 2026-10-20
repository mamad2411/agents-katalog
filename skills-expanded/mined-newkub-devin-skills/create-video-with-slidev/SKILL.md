---
name: create-video-with-slidev
description: Generate visual interactive transition videos from a Slidev deck via slidev MCP + recording
argument-hint: "[topic-or-slides.md]"
related:
  - follow-create-slide-slidev
  - use-mcp
  - record-video-web-with-agents-browser
  - use-agent-browser
  - update-devin-global-mcp
  - gen-voice
  - gen-subtitle-video
  - convert-files-format
  - edit-video-with-remotion
  - create-programatic-video-with-fframes
  - report

---

## Goal

Create a presentation video from a Slidev deck focused on visual interactive transitions (slide transitions, click/motion animations, view transitions), using the `slidev` MCP server to manage the deck and recording the playback as a real video

## Scope

- Create or enhance `slides.md` via `/follow-create-slide-slidev` — every slide must have motion (not a static deck)
- Use the `slidev` MCP server (`bunx slidev mcp slides.md` — registered in `%APPDATA%\devin\mcp_config.json` via `/update-devin-global-mcp`) to inspect, edit, reorder, and navigate slides
- Record the video with `/record-video-web-with-agents-browser` (agent-browser) while auto-advancing the deck to the end
- Alternatives outside the main scope: advanced programmatic video (multi-track, effects) → use `/edit-video-with-remotion` or `/create-programatic-video-with-fframes` instead

## Execute

### 1. Plan Storyboard

> Goal: have a complete scene and transition plan before writing slides

1. Take the `topic` or the path of an existing `slides.md` from the user — if a deck already exists, skip to step 3
2. Ask for `orientation` (`landscape 16:9` default), target `duration`, `tone`, language, and whether a voiceover is wanted
3. Write the storyboard: 1 slide = 1 scene, specifying per slide — content, enter/exit transitions, click/motion beats, and dwell time (dwell time ≥ the time the animation takes to finish)

### 2. Author Deck

> Goal: a slides.md with complete visual interactive transitions on every slide

1. Run `/follow-create-slide-slidev` to create/edit `slides.md` (standalone or `D:/newkub/slides/{project}/`)
2. Set headmatter: per-slide `transition` (`slide-left`, `slide-up`, `fade-out`, `view-transition` — use `forward | backward` pairs when direction matters), `comark: true`, and `fonts` for Thai content
3. Add motion to every slide per `### Animation Transitions` of `/follow-create-slide-slidev`: `v-click` presets, `v-motion` (initial/enter/click-N states), `v-switch` for staged reveals, `clickAnimation` presets, `view-transition-name` for shared-element morphs
4. Use `Noto Sans Thai` for Thai content; no more than 5 bullets per slide; open with `layout: cover` and close with `layout: end`

### 3. Verify Deck Via Slidev MCP

> Goal: the deck is correct and MCP-drivable before recording

1. Check that the `slidev` server is in `%APPDATA%\devin\mcp_config.json` — if missing, run `/update-devin-global-mcp` to add `{ "command": "bunx", "args": ["slidev", "mcp", "slides.md"] }`
2. Call `mcp_list_tools` on the `slidev` server to see the real tools (inspect/edit/reorder/navigate) — never guess tool names
3. The stdio server operates on the `slides.md` in the cwd it launches in — if the deck lives elsewhere, pass the full path when calling tools, or use the HTTP transport `http://localhost:3030/__mcp` while the dev server runs
4. Use MCP tools to check slide count, order, and click counts per slide → yields the click budget for recording

### 4. Run Dev Server

> Goal: the deck really renders with animations

1. Run `bunx slidev <slides.md>` from the correct root per `/follow-create-slide-slidev` (port 3030 default) in the background
2. Open `http://localhost:3030` and confirm transitions actually play — on error → `/resolve-errors`
3. Check `/check-open-ports` if the port conflicts

### 5. Record Playback

> Goal: a video that captures every transition in full

1. Run `/record-video-web-with-agents-browser`: `agent-browser open http://localhost:3030 --headed`, `set viewport 1920 1080`, `wait --load networkidle`, then `record start <name>.webm`
2. Auto-advance per the click budget from step 3: `agent-browser click` on the slide area (or the `ArrowRight` key) one click at a time — `agent-browser wait <ms>` between advances, at least the transition duration (default ~700ms; 1200-1500ms is a safe choice)
3. If the slidev MCP (HTTP `__mcp`) has a navigate tool → driving via MCP instead of clicks is more deterministic
4. Loop through to the final slide, then `agent-browser record stop` + `agent-browser close`

### 6. Post-Process

> Goal: deliverable files ready to use

1. Default output is `.webm` — for `.mp4` → convert with `ffmpeg -i in.webm -c:v libx264 -crf 20 out.mp4` or `/convert-files-format`
2. Voiceover → `/gen-voice`, then mux with `ffmpeg -i video -i voice -c:v copy -shortest out.mp4`
3. Subtitles → `/gen-subtitle-video` from the final video file

### 7. Report

> Goal: summarize results and file paths

1. Run `/report`: slide count, transitions used, click beats, duration, output paths (`.webm`/`.mp4`/`.srt`)
2. Note remaining opportunities, e.g. shipping the deck as a static site via `slidev build`

## Rules

### 1. Motion Required

- Every slide must have at least one kind of motion — a slide transition, `v-click` reveal, or `v-motion`; a static deck counts as a failure
- Use varied but coherent transitions — pick one family (e.g. `slide-*` across the whole deck) and reserve `fade`/`view-transition` for section breaks
- Dwell time per click must always be ≥ animation duration, otherwise the video cuts motion mid-play

### 2. MCP Usage

- Always run `mcp_list_tools` first — the `slidev mcp` tool surface changes across versions
- `slides.md` in the config args is relative — the stdio server binds to the cwd the agent launches in; for a deck in another project, use the HTTP `__mcp` or check the cwd first
- Edit `slides.md` via MCP when possible (SSOT) — hand-edit only what MCP doesn't cover

### 3. Recording

- Always record `--headed` at a 1920x1080 viewport, per `/record-video-web-with-agents-browser`
- Advance deterministically — 1 action = 1 click state; don't rely on loose timing
- For long decks → record in multiple files split by section, then concat with ffmpeg

### 4. Safety

- Do not overwrite existing `slides.md`/video files without asking — back up or use indexed filenames
- Do not commit large video files to git

- Use /use-agent-browser if needed
- Use /use-mcp if needed
- Use /resolve-errors if needed

## Expected Outcome

- A `slides.md` where every slide has visual interactive transitions, verified via slidev MCP
- A `.webm` video file (and `.mp4` if converted) capturing all motion beats in full
- A report of output paths, duration, and transitions used
