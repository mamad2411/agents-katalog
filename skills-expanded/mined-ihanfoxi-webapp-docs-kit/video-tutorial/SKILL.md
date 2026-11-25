---
name: video-tutorial
description: Creates user-manual style video walkthroughs of a web app as 1920×1080 MP4 files, recorded from the real app with Playwright. The camera zooms into each field, a red box highlights it, a cursor moves to it and a caption explains the step; an .srt subtitle file is included. Use when asked for "/video-tutorial", a tutorial video, a training video, a screencast or a video manual of a web app. Not meant for social media or marketing videos.
argument-hint: "[topic or walkthrough name]"
---

# Video tutorial

Produces **one video per walkthrough** that shows how to use the app, as if a
Full HD monitor were being recorded. In every step the camera zooms into the
element, a red box highlights it, the cursor moves to it and a caption explains
what to do. The format is described in `references/video-style.md`.

In this guide `$H` is this skill's `scripts/` folder and `$V` is
`../visual-check/scripts`, shared by the three webapp-docs-kit skills.

## Before you start

1. If `$V/node_modules` does not exist: `cd $V && npm install`. `ffmpeg` and
   Chromium are required (see `/visual-check`).
2. Use the same `docs/webapp-docs.json` and `docs/manuals/<name>/walkthrough.json`
   as `/user-manual`. If they do not exist, create them following
   `../user-manual/SKILL.md` (questions about the environment and scope),
   `../visual-check/references/configuration.md` and
   `../user-manual/references/walkthrough-format.md`.
3. **Screens behind sign-in or other preconditions:** this kit does not sign
   in, handle credentials or assume user roles. If the screens are behind a
   login or any other precondition, **stop and ask the user how they want to
   handle it**. Never ask for, type or store passwords, tokens or cookies
   yourself, and never work around access controls.
4. **Music.** Videos have no music by default. If the user provides a track
   they are allowed to use, pass it with `--music`.
5. **Branding.** Optional `video.logo`, `video.primaryColor` and
   `video.accentColor` in the config. Caption texts can be translated with
   `video.labels`.

## Walkthroughs for video

A walkthrough that works for the manual almost always works for the video. For video, review it like this:

- Each `text` describes **one** action in about 20 words at most. It is read while the screen is still.
- Group steps in scenes of 3 to 8 steps. Each scene opens with a title card.
- Add `"mark"` to `go` steps on screens with a lot of empty space so the camera
  moves closer to the useful area.
- Use `"zoom": false` to explain large areas, like a side menu or a whole table.
- Actions that change data use `"simulate": true`.
- A video lasts 1 to 5 minutes. If there is more content, split it into
  several walkthroughs (`docs/manuals/getting-started/`, `docs/manuals/orders/`).
  Each walkthrough is one video.

## Steps

1. **Record** the app states at a real 3840×2160 with a 1920×1080 viewport:
   ```bash
   cd <project>
   node $H/record.js docs/webapp-docs.json docs/manuals/<name>/walkthrough.json
   ```
   It prints the path of `timeline.json`, in `~/.cache/webapp-docs-kit/video/<app>/<name>/`.
2. **Preview before rendering.** Render one frame per step and a contact sheet:
   ```bash
   node $H/compose.js <timeline.json> <output>/video-<app>-<name>.mp4 --preview
   ```
   **Open `sheet.png`.** Check that the red box is on the right element, that
   the caption does not cover what it explains and that no personal data is
   left unblurred. If something is wrong, adjust `zoom`, `mark` or `redact` in
   the walkthrough and repeat from step 1.
3. **Render:**
   ```bash
   node $H/compose.js <timeline.json> <output>/video-<app>-<name>.mp4 [--music track.mp3] [--volume 0.25]
   ```
   Writes the `.mp4`, the `.srt` with the captions and, with `--music`, a `-music.mp4`.
4. **Check at least 3 frames** of the final video:
   `ffmpeg -ss <s> -i video.mp4 -frames:v 1 <temp folder>/frame.png`, and open them.
5. Repeat for every requested walkthrough.

`<output>` is `video.output` from `docs/webapp-docs.json`. Default:
`~/Videos/walkthroughs/<app>/<name>/`. **MP4 files never go into the repository.**

## Delivery

Report each video's path and duration, whether music was used, and which steps were simulated.
