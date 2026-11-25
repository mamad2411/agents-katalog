---
name: real-product-showcase
description: Record real product demos from terminal, browser, or apps and ship them as verified media. Never use fake or synthetic UI for hero assets. Use when the user asks for real demos, hero MP4s/GIFs, asciinema or Remotion recordings, browser walkthroughs, app recordings, README/PR media, or says no namaak / fully realistic / complete showcase. Also use after UI changes when regenerating marketing or docs visuals.
license: MIT
compatibility: Works in Pi, Cursor, and other Agent Skills hosts. When this package has local pipeline commands, those win. Otherwise use the surface references as written.
metadata:
  author: GroepOnline
  version: "1.0.0"
---

# Real product showcase

Record the real product. Cut the tape. Check that viewers can still tell what product it is.

If someone wants a realistic demo, do not invent UI frames, mock dashboards, or "looks like Pi" renderers for the hero clip.

## Hard rules

1. **Record the real thing.** Drive the actual CLI, web app, or native app. Capture that session.
2. **Keep the chrome.** Terminal prompt bar, browser URL bar, or app title bar must stay in frame. If you cannot tell which product it is, the crop failed.
3. **Mark the beats.** Tag each proof step (for this package: skill, subagent, dashboard, handoff) so one take becomes a master plus short clips.
4. **Ship smooth video.** Prefer 1080p H.264 `yuv420p` at 30 or 60 fps. Reject 1 fps slideshows. Do not promote a GIF as the master hero.
5. **Check before you publish.** Probe codec, size, and fps. Confirm chrome is uncut and each clip ends on a real success.

## Which surface

| Surface | Capture | Read next |
|---------|---------|-----------|
| Terminal / Pi CLI / TUI | asciinema v3 + markers, then `agg` renders the `.cast` | [references/terminal-asciinema.md](references/terminal-asciinema.md) |
| Browser / web app | Playwright/CDP or a screen record of the live UI | [references/browser-capture.md](references/browser-capture.md) |
| Desktop / mobile apps | OS or device recorder + scene markers | [references/desktop-mobile-apps.md](references/desktop-mobile-apps.md) |
| Post | Trim scenes, fit framing, render 60 fps master | [references/remotion-post.md](references/remotion-post.md) |
| Checks | ffprobe, framing stills, clip contracts | [references/quality-gates.md](references/quality-gates.md) |

Pick one surface. Do not stitch fake terminal frames into a browser story.

## Workflow

### 1. Write the beats

List 3 to 6 steps that prove the product works. For this orchestrator that usually means:

1. Create a skill
2. Spawn a subagent
3. Open the live dashboard or top view
4. Show a finished handoff

Every beat needs a visible win: file on disk, running agent id, handoff JSON, green status.

### 2. Set up a disposable runtime

- Use the real binary, URL, or build you claim to show. Current package version, not an old tag.
- Isolate home/profile/session so secrets stay out of the tape.
- If the model is flaky, pre-stage fixtures, but still run the real create/copy/run path on camera.

### 3. Record with markers

- Start the recorder for that surface.
- Drop a marker at the start of each beat (asciinema `m`, chapter mark, or a short on-screen slate).
- Keep typing and idle short. Cut waits later. Do not crop chrome to make glyphs bigger.

### 4. Cut and render

- Label markers in order.
- Compress idle. Keep every scene.
- Fit typography or viewport so every captured row stays visible.
- Render one master plus one clip per scene, using the fixed scene ids and stable filenames in [references/remotion-post.md](references/remotion-post.md) (`showcase_skill-creation.mp4`, `showcase_subagent-run.mp4`, `showcase_dashboard-top.mp4`, `showcase_handoff.mp4`). Only gate and publish after all of them exist.

### 5. Gate and publish

- Follow [references/quality-gates.md](references/quality-gates.md).
- Drop review artifacts next to the PR.
- Update changelog or asset maps only when tracked docs expect it.
- GIF is fine for social or fallback. It is not the hero.

## This repo

Inside `pi-agent-orchestrator`, the showcase commands live in `package.json` (full table in `.agents/skills/showcase`):

```bash
# Record a real terminal session. Drop scene markers live while you record
# (asciinema marker hotkey); see references/terminal-asciinema.md.
npm run showcase:tmux      # tmux + asciinema -> showcase_tmux.mp4 / .gif
npm run showcase:live      # live asciinema   -> showcase_live.mp4 / .gif

# Render the source-derived Remotion hero + promo suite (dashboard_preview.mp4).
# This is programmatic; it does NOT ingest your .cast and is not a real hero take.
npm run showcase:remotion

# CI GIFs only. Not a stand-in for a real hero take.
npm run showcase:ci
```

There is no `label-scenes` or `verify-media` script: mark scenes live while recording, then gate the output by hand with the `ffprobe` checks in [references/quality-gates.md](references/quality-gates.md).

Real outputs under `docs/images/` include `dashboard_preview.mp4` (Remotion hero), the terminal masters `showcase_tmux.mp4` and `showcase_live.mp4`, and the per-scene clips `showcase_skill-creation.mp4`, `showcase_subagent-run.mp4`, `showcase_dashboard-top.mp4`, and `showcase_handoff.mp4` (cut with the edit-list flow in [references/remotion-post.md](references/remotion-post.md)).

`.agents/skills/showcase` owns the local command table. This skill owns the realism rules.

## Refuse these

- Synthetic dashboard frames sold as a live Pi session
- Prompt bar, URL bar, or nav chrome cut off
- Long typing with no agent or UI result
- A "master" that is a stretched low-fps GIF
- Missing markers, so you cannot cut clips from one take

## Done when you can report

1. Surface and capture path
2. Scenes and durations
3. Output files plus ffprobe summary
4. That product chrome is visible and each beat actually succeeded
