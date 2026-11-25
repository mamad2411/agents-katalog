---
name: mage-video-remake
description: |
  Recreate a viral or reference video shot for shot with your own
  characters, products, and words on Mage. Breaks the original down with
  rea-video, an open-source tool (per shot: filmed, AI-generated, or built in
  code; captions, cuts, beat, and sound), then remakes it: Magejutsu recasts
  a take whose motion matters with your character or product, Mango 4
  keyframes and Cherry 2 Pro (or Lemon) rebuild the other shots, Seed Audio
  scores it, and ffmpeg cuts it to the original's timing. Use when: "remake
  this viral video", "recreate this TikTok with my character", "copy this
  video shot for shot", "make this ad again with my product", "how was this
  video made", "is this video AI", "break this video down shot by shot".
  NOT for: a new video from a prompt (use mage-generate), a creator-style
  product video from scratch (mage-ugc-video), swapping the person in one
  clip you keep as is (mage-video-character-swap), editing your own clip
  with a prompt (mage-video-editor), or reposting someone else's video.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems. The breakdown and the final cut need a shell with Python 3.10 or later and ffmpeg; rea-video is installed by the skill at a pinned version.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Video Remake

Rebuild a video the user admires with what they own: the same hook, structure, pacing, captions, and beat; their characters, product, and words. First find out how each shot was made (filmed, AI-generated, or built in code), because that decides how to remake it and what it costs.

## Before you start

1. **Mage tools:** `list_models`, `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, `list_references`, `create_character`, `create_reference`, and `create_upload`. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **A shell** with `python3 --version` at 3.10 or later and `ffmpeg -version`. Without one, this skill cannot break the video down or cut the result: say so and offer `mage-generate` for single shots.
3. **The video as a file.** A TikTok, Instagram, or YouTube link is a web page, not a video file: ask the user for the file, or to download it with a tool they already use. Only for a video they may study.
4. **Rights.** The remake borrows structure and technique, never content: no footage, music, voice, logos, on-screen words, or faces from the original reach the result. A recast replaces every person in its clip. Cast real people only with their consent.

## UX rules

1. Ask once, in one message, for what is missing: the video, who stars (a saved `@character` or a photo), the product (a photo), and the message or offer. Default to the original's aspect ratio and length.
2. Show how the original was made and the remake plan, with every paid line priced by `estimate_cost` and the total, before generating anything. Wait for a yes. Ask again before anything the plan did not include.
3. Video is the expensive part: offer a draft path when the total is large (Cherry Mini at 480p, Magejutsu Lite or Feather, one shot first).
4. rea-video's own remake section suggests other services' models. Plan on Mage's models only, and never tell the user which outside model made the original.
5. Deliver links with short labels in story order, no JSON or ids. Links expire after 30 days. Remind the user once that platforms may require AI-generated videos to be labeled.

## Workflow

### 1. Install rea-video (once)

rea-video ([JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video), Apache-2.0) runs on the user's machine. Install the pinned v0.1.0 commit, never the moving `main`:

```bash
pipx install "rea-video[ocr] @ git+https://github.com/JuneYaooo/rea-video@1b4a340957bdc25155deec55489523bdb3412842"
rea-video --help
```

No pipx, a Python that is too new, or an OpenCV clash: `references/breakdown.md`.

### 2. Break it down

```bash
rea-video decompose video.mp4 -o breakdown/ref --lang en
rea-video review breakdown/ref
```

It cuts the video into shots, measures how each was made (frame cadence, sensor noise, whole-frame motion, metadata), and reads the captions with their times and styles, the stickers, the camera moves, the light, the music's tempo, and the sound effects. A 20-second clip takes about a minute. The first run downloads the voice and music separation models; `--no-stems` skips them. Use `--lang zh` when the user writes Chinese.

**If you can see images, review every shot.** A downloaded video is recompressed, which erases the sensor noise that tells filmed footage from generated: the tools alone often call a filmed TikTok AI. Look at `breakdown/ref/storyboard.jpg` and each shot's sheet, `shots/shot_NNN.jpg`, fill `review_answers.json`, and merge it with `rea-video apply-review breakdown/ref --by agent`. What to fill and how the merge weighs it: `references/breakdown.md`.

Then read the package in layers, and stop when you have what you need: `REEL.md` (the verdict and a map), `reel/timeline.md` (one line per shot; keys ending in `~` are inferred), a shot's `reel/shots/<n>.md`, and `reel/sound.md` or `reel/packaging.md` for one aspect. Never open `breakdown.json`, and skip `reel/remake.md`.

### 3. Tell the user how it was made

A few lines: what it is ("21 s, 14 shots: one creator filmed on a phone at a kitchen counter, a styled caption on every line, no music, sound effects on each text pop"), the hook in the first two seconds and why it works, the story's steps, what the user must supply (their screen recording, their product), and which shots stay uncertain.

### 4. Plan the remake

**Recast** when the original is one take of 4 to 30 seconds whose motion is the point (a dance, a transition, a stunt): Magejutsu keeps its motion, camera, and timing and rebuilds the person or the product from the user's references. **Rebuild** everything else, shot by shot. Mixing is common: recast the take whose motion matters, rebuild the rest.

| Shot was | Remake it with |
|---|---|
| AI-generated video, 3D, 2D animation, stop motion | A Mango 4 keyframe with the user's `@handle`, then Cherry 2 Pro; shots that share a set and cast as one Cherry 2 Pro clip |
| Filmed footage | Magejutsu when the exact performance matters; otherwise a phone-footage keyframe and Cherry 2 Pro, or the user films it |
| A talking avatar | The user's character speaking the new line on Cherry 2 Pro with their saved voice |
| Motion graphics, kinetic text, UI | Code (HTML and CSS, or a template tool) from the shot's timings, or a Mango 4 still animated with Lemon |
| A screen recording or screenshot | The user's own recording; never a fake of an app they don't own |
| A still with a push or pan | A Mango 4 still, moved with ffmpeg |
| A clip from a film or show | Never reused: a new shot that does the same job, or cut |

Model settings, prompts, and short shots: `references/shot-routes.md`. Keep the original's story steps and swap in the user's case, product, and words, not only the lead. Write new lines at the original's length per shot so the timing holds.

Price each line with `estimate_cost` (upload a source clip with `create_upload` first so it can be measured) and show the plan as a table: shot, how the original made it, the Mage route, Gems. Wait for a yes.

### 5. The cast

- `list_characters` and `list_references` first. Save a person the remake reuses with `create_character` from a sharp, front-facing face photo, and a product with `create_reference` (kind `object`) from a clean photo; mention them as `@handle` in every prompt.
- Lock each face and the product in a Mango 4 keyframe before any video: a still costs a fraction of a clip.

### 6. Generate

For each line: `generate` with a new UUID `idempotency_key`, then `get_request` with `wait_seconds: 120` until it's done (a recast takes several minutes). Start the lines that don't depend on each other together. Check each result against its keyframe and the original shot; regenerate a shot only when it is plainly broken, and say what it costs.

### 7. Cut it to the original's timing

Trim every clip to its shot's exact start and end (the `time` line in `reel/shots/<n>.md`; the timeline rounds), never speeding it up, join them in order, lay the user's captions in the original's position and style, and put the new music under the whole cut. Commands: `references/assembly.md`.

## Deliver

```text
Remake ready (21 s, 9:16, 14 shots, 6,240 Gems): https://…
Hook: same 2-second product reveal, now with @nova and your bottle.
```

Offer once: a second hook to test, or the same remake in another language.

## References

- `references/breakdown.md`: installing rea-video, running it, the shot review, and reading its package.
- `references/shot-routes.md`: the Mage model, settings, and prompt for each kind of shot, recasts, and short shots.
- `references/assembly.md`: ffmpeg commands to cut, caption, and score the remake to the original's timeline.
