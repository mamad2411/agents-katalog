---
name: sr-edit-plan
description: Turns a video and its transcript into an edit plan. Reads an SRT or VTT file to report speaking pace, dead air to cut and filler words with timestamps, re-chunks subtitles into short readable lines for vertical video, and writes a cut list, b-roll and on-screen text notes, and export settings. Use when someone asks how to edit a video, wants captions or subtitles, wants to remove pauses and ums, or says their edit feels slow. Produces instructions and a caption file to apply in CapCut, Premiere, DaVinci, Descript or any editor. Nothing edits the video itself.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the subtitle tools; ffmpeg is optional and only needed for the clip commands in sr-repurpose.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Edit plan

Editing is where a good script either keeps its pace or loses it. This skill finds the slow spots in the transcript and tells you exactly where to cut.

## Get the transcript

Ask for an SRT or VTT file. Most editors export one (CapCut, Descript, Premiere, DaVinci, YouTube Studio). If there is none, ask for a plain transcript and say the timestamps will be missing, so cuts will be by line, not by time.

## Read the pace

Tool `subtitles_analyze` with the file as `text` (CLI: `python scripts/sr.py subtitles --file talk.srt`). It reports:

- words per minute overall (a rough guide: about 150 is a relaxed conversational pace, and fast, punchy short-form often runs higher; compare with the person's own best videos, not with a rule)
- **cut list**: gaps longer than the pause threshold (default 0.7 s), with timestamps and how many seconds you would save
- filler words inside cues (um, uh, you know, okay so) with timestamps, to trim by ear, because an SRT has no word-level timing

Apply the cut list in the editor, top to bottom. Leave a short breath where a pause carries meaning (after a punchline or a reveal).

## Caption file for vertical video

Tool `subtitles_rechunk` (CLI `python scripts/sr.py rechunk --file talk.srt > talk_vertical.srt`). It re-times the words into short balanced lines of about four words and 28 characters, free to cross the original cue edges, with no one-word orphans. Import the result into the editor and style it once.

Style tips: one line, high contrast, a highlight on the key word, kept away from the platform's own buttons at the bottom and right edge.

## Pacing

Craft rules of thumb, not laws: change something on screen every few seconds (cut, zoom, text, b-roll). Use sound to mark beats. Cut the first word of a sentence if it is "so" or "and". Put a visual change inside every beat that the beat sheet flagged as long on one line or without a number, name or turn (`sr-script`, tool `script_beats`).

## Plan b-roll and on-screen text

Write a table:

```
Time | Line | On screen | Note
```

The on-screen text should add to the spoken line. Do not subtitle the same words twice in different places.

## Export

Vertical video is 9:16, 1080 by 1920. Ask the person to check the platform's current guidance in the app for frame rate, bitrate and file size. Keep a clean master without burned-in captions for repurposing.

## Gate

`human`: the person edits. When they return with the cut, ask them to export retention after publishing and run `sr-audit`.

## Do not

- Remove every pause. Silence is part of rhythm.
- Add background music so loud that it fights the voice.
- Use music you do not have rights to (`sr-policy-check`).
