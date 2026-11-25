---
name: sr-repurpose
description: Turns one long video, podcast, talk or article into a week of native pieces. Scores a transcript for the best 20 to 60 second windows on opening hook, self-containment, density and payoff, writes ready-to-run ffmpeg commands for 9:16 cuts with matching caption files, then adapts each piece for each platform with a new first frame, platform captions and no foreign watermarks, plus text and carousel spin-offs. Use when someone has long content and asks for clips, Shorts, Reels, a content week or "how do I get more out of this video".
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the clip finder; ffmpeg on the person's machine to run the cut commands (optional, the timestamps work in any editor).
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Repurpose: one source, many pieces

A good long piece contains five good short ones. Find them, cut them well, and make each one feel native to where it lands.

## Ask first

- The source file and its transcript (SRT or VTT).
- Which platforms get a version (the hub and spokes from the intake).
- Whether the speaker is centred in the frame. It decides crop versus pad.

## Find the clips

Tool `clips_find` with the transcript as `text` and options `min_seconds`, `max_seconds`, `count`, `target_seconds`, `source` (the file name) and `crop` (`center` or `pad`). CLI:

```
python scripts/sr.py clips --file talk.srt --count 5 --source talk.mp4
```

Each candidate has a start, end, score, and sub-scores for hook, self-containment, density, payoff and pace, the opening line, a ready-to-run ffmpeg command for a 9:16 cut, and a caption file starting at 00:00:00. Only the transcript is scored, so watch each clip cold, with the sound off, before you trust it.

By hand: look for a complete thought of 20 to 60 seconds that starts on a claim, needs no earlier context, and ends on the payoff.

## Cut

The ffmpeg commands crop the centre of a 16:9 frame to 9:16 at 1080 by 1920 and re-encode with libx264 and AAC. If the speaker is off-centre, use `crop=pad` or cut in the editor. Re-time the captions with `subtitles_rechunk` (`sr-edit-plan`).

## Make each one native

For every platform:

- A **new first frame** and a new first line. The clip's mid-conversation start is rarely a good hook.
- A **platform-specific caption** (`sr-caption`). Not the same text everywhere.
- **No watermarks** from other apps. Export clean.
- Different cover text if the platform has a cover.

## Spin off text and carousels

Pick two or three points from the source and turn each into a standalone text post (`sr-text-post`) or one carousel (`sr-carousel`) with its own example. Do not post a transcript.

## Originality

Reported between April and October 2026: YouTube, Instagram and Facebook each announced changes that favour original content over reposts (`facts_search id=general.originality_trend`). Instagram said it will stop recommending accounts that regularly repost content they did not create. YouTube said it is further prioritising original content from 1 October 2026. Clips cut from your own long video are your own work. The announced changes are aimed at reposting other people's content, so if the source is not the creator's, add real commentary, analysis or new footage.

## Schedule

Hub piece first, spokes the next day, never everything at once. Build it with `sr-calendar`.

## Gate

`approve` on the clip list. Cutting and posting are `human`.

## Do not

- Post a clip that needs the previous five minutes to make sense.
- Cut mid-word to hit a length.
- Use the full-length audio over a clip's cut without checking sync.
