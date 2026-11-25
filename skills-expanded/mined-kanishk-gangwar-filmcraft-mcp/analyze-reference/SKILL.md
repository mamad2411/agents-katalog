---
name: analyze-reference
description: Take a reference video (a reel, TikTok, CapCut template, music video, ad) apart frame by frame — exact cut frames, beat/tempo, flashes and light leaks, transitions, intro construction, picture-in-picture sections, captions, ending and colour — so an edit can copy its structure precisely. Use it whenever the user gives a video to imitate ("edit like this", "same style", "match this reel"), asks how a video was edited, or points at a timestamp in a reference that your edit doesn't match yet. Also finds the beat of a song by listening to it (tempo, beat and bar frames, loud sections, drops) when the user wants clips cut to music without a reference video.
---

# Analysing a reference video

Users compare your edit to the reference second by second. Guessing the style from a few frames
(or the post's caption) gets the vibe and misses the details they care about: exact cut timing, how the
title is built, what happens at 0:10 or 0:15. Measure instead. Scripts need Pillow and
`FILMCRAFT_CLI="${user_config.filmcraft_cli}"` (or filmcraft-cli on PATH); `${CLAUDE_SKILL_DIR}`
is this skill's folder.

## 1. Get frames

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract_frames.py ref.mp4 work/ref --scale 0.25
```
Every frame as a PNG plus `info.json` (fps, size). For close study of a short span (a title, a
transition) extract again at `--scale 1 --start S --end S`.

If you only have a link (Instagram/TikTok usually need a login to download), ask for the file. A browser
can show the post, but frame-accurate work needs the video.

## 2. Cuts, beat, flashes

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/detect_cuts.py work/ref          # add --soft for dissolves/whips
```
Gives cut frames, shot lengths, the common shot length (the beat: e.g. 23 frames ≈ 78 BPM, with
half-beat bursts of 11–12), sudden-brightness flashes (cream/white flash frames, light-leak peaks) and
black frames. Expect a structure like: intro → flash → fast half-beat burst → long hold → burst →
holds → on-beat section → fade. Keep the cut frames verbatim for the new edit.

### The beat from the sound

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/detect_beats.py ref.mp4 --fps 30 --json work/beats.json
```
Listens to the soundtrack (a video or a song file: mp3, m4a, wav) and prints the tempo, every beat
and estimated bar start as sequence frames at `--fps` (song at frame 0), the loud / quiet sections
and drops. On a reference, the cuts should sit on these beats within a frame or two; when the visual
cuts are ambiguous (dissolves, fast motion), trust the beats. Tempo can read at double or half the
feel (156 vs 78 BPM): the cut lengths tell you which one the editor used, or pass `--bpm`.
`confidence` below 1.5 (exit code 2) means no real beat, e.g. speech or ambient sound.

## 3. Look at every section

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/contact_sheet.py work/ref work/sheet_intro.jpg --to 150 --every 3
python3 ${CLAUDE_SKILL_DIR}/scripts/contact_sheet.py work/ref work/sheet_body.jpg --from 150 --every 10 --cols 14
python3 ${CLAUDE_SKILL_DIR}/scripts/contact_sheet.py work/ref work/sheet_t10.jpg --from 278 --to 306 --cols 7 --zoom 2
```
`--crop x0,y0,x1,y1` isolates the picture area (e.g. a 16:9 band inside a 9:16 reel); `--zoom` for
detail. Read the sheets and write down, per section:
- **Intro**: how the title is made (photos stacked into letters? footage inside letters? typed?),
  letter shape and size, order and timing of each piece (frame numbers), what the first frame shows.
- **Transitions** at each cut: hard cut, flash (colour, frames), whip, light leak (streaks? flare
  direction? blowout?), zoom.
- **Non-cut sections**: pictures popping onto the frame on the beat (positions, sizes, flash before
  each), split screens, slide-ins. Positions as fractions of the frame, timings as frames.
- **Framing**: full frame, letterboxed band, aspect.
- **Caption/text**: wording style, font look (monospace, serif), size, position, whether it stays on.
- **Ending**: hold length, fade to black (how many frames).

Zoom into anything the user calls out ("the 2026 is not like the video", "at 0:10 there's an effect")
at full resolution before rebuilding it.

## 4. Colour

Measure the reference's look over the body of the video (skip the intro and any black bars):
```bash
python3 ${CLAUDE_SKILL_DIR}/../match-grade/scripts/color_stats.py work/ref --crop 0,112,180,208
```
Note shadow neutrality, highlight warmth (R minus B), brightness and saturation for match-grade.

## Output

Write the findings as a short spec (cut frames, beat, per-section notes, colour numbers) the
recap-edit plan can follow, and show the user the key sheets when it helps them confirm.
