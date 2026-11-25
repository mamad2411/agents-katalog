---
name: botkits-video-plan-page
description: >-
  Use this before you render a video, when the script is written and someone has
  to approve it. It turns a script file into one self-contained HTML page with a
  playable animatic (timed captions, a HUD, key frames or "to paint" cards), a
  scrubbable timeline, the hook versions, the shot list, title and thumbnail
  options, the order of work, and the open choices with a copy-ready approval
  reply. Use it to get a yes on the plan before you spend time or GPU on shots.
---

# Video Plan Page

A script in a chat message is hard to judge. You can't feel the pacing, and nobody can see
which shot goes with which line. This skill builds one HTML file that plays the script as
an animatic. Each caption shows for its estimated read time. Each shot shows its key frame,
or a card that describes the picture still to make. Below the animatic, the reviewer reads
the plan, answers a few choices, and copies a single reply back to you.

Build nothing until that reply arrives.

## When to use

- A script is written and the next step costs real time: key frames, animation, voice, edit.
- Someone else signs off (a client, a channel owner, a teammate) and reads on a phone.
- You want one link that holds the whole plan, not five messages.

Skip it for a single-shot clip or a script with no picture notes.

## Steps

1. **Write `script.json`.** Required: `title` and `lines`. Each line has a `who` code (`C` caption,
   `N` narrator, `S` the enemy or inner voice, `X` picture only) and `text`. A `|` splits the
   caption into two rows. Add `see` to any line that starts a new shot: one sentence about the
   picture. Add `level` and `beat` for the structure bar, and `hud` for an on-screen counter.
   Leave out `t` and `dur`. The script times each line at 2.6 words a second (at least 2.4 s,
   or `min` if you set it).
2. **Write `plan.json` (optional).** It holds everything that is not the script: header chips,
   level names, speaker labels, `colours` for the `knows` dots, the order of work, a Gantt chart
   in hours, extra cards, and the `decisions`. Mark one option per decision `rec: true`. Put key
   frames under `keys` (`"S03": "keys/s03.png"` or a start time such as `"12.5"`). Paths are
   relative to `plan.json`.
3. **Build.**

   ```sh
   python3 scripts/plan_page.py example/script.json --plan example/plan.json --out plan.html
   ```

   Add `--no-webfonts` if the page must not call outside servers. Missing images print a warning,
   and those shots stay "to paint".
4. **Check it yourself.** Open it at desktop and phone width (390 px). Press play once at 4×.
   Click a shot row, check that the animatic jumps to it, then change one choice and read the
   reply.
5. **Send one link.** Host the file anywhere static. It has no other files. Ask for the reply,
   and treat "approve" as all recommended choices.
6. **Build from the reply only.** Apply the choices to the script before you make any shot.

## Rules

- Keep private or unreleased material out of a page you host in public. Images are embedded,
  so anyone with the link sees them.
- Each image is shrunk to 960 px JPEG (when Pillow is installed). The page refuses to build
  over 15 MB.
- Fonts: the page asks Google Fonts for its display, body, mono, and handwriting faces. Every
  font stack ends in system fonts, so offline (or with `--no-webfonts`) it still reads well.
- The output is generated. Edit `script.json` and `plan.json`, then rebuild.
- Hook check letters (optional, on `quest.hooks[].checks`): M mirrors the viewer, H leaves a
  half guess, S has one surprise, N uses an exact number, B fits in one breath.

## Files

- [scripts/plan_page.py](scripts/plan_page.py): the builder. The docstring lists every field.
- [scripts/template.html](scripts/template.html): the page; the builder fills in the data.
- [scripts/test_plan_page.py](scripts/test_plan_page.py): `python3 -m pytest -q skills/video/botkits-video-plan-page/scripts`
- [example/script.json](example/script.json) and [example/plan.json](example/plan.json): a made-up
  45-second film, *Seven Days to One Loaf*. Its 11 key frames and 2 thumbnails are AI-generated
  stills in [example/keys/](example/keys/) (960 px JPEG), so a fresh clone builds the page with pictures.

## Checklist

- [ ] Every shot line has a `see` sentence
- [ ] Each decision has exactly one recommended option
- [ ] Page opened at desktop and 390 px; play, scrub, tabs and copy work
- [ ] No private names, emails or account IDs in the inputs or images
- [ ] Nothing built until the reply came back

> **Next step: from approved plan to Shorts.** When the long cut is done, the free
> [botkits-shorts-reframe](../botkits-shorts-reframe/SKILL.md) skill crops it to 9:16 Shorts.

## Inspired by

Dani Acosta's storytelling-video plan page in a private channel repo (yt-daniacostaai, pull
request #204): a single page that plays the script as an animatic, lists the shots, and ends
with choices and a copy-ready approval reply. That version was built for one channel. It
named that channel's characters in code, its example film pointed at image files on one
machine, a missing image stopped the build, and the page had no doctype or viewport, so
phones got a scaled-down desktop layout.

## What this version adds

- A real HTML document (doctype, charset, viewport), so the phone layout works, and the
  "to paint" note no longer runs under the caption at 390 px.
- Hidden tabs and cards now actually hide (`[hidden]` wins over the grid layout).
- No character names in code: dot colours come from `plan.json` or a neutral palette.
- A missing image warns and leaves the shot "to paint". The build continues.
- System-font fallbacks for every face, plus `--no-webfonts`.
- UTF-8 reads and writes, a byte-accurate size limit, safer escaping of script text, and
  tolerance for hooks without checks and lines without a level.
- The approval reply names every picked option by its label (recommended ones marked), not by a
  separate reply code, so the reply always matches what was ticked.
- A neutral demo that builds from a fresh clone, and tests that cover each fix.
