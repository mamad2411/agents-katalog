---
name: check-render
description: Verify a rendered video before handing it over — decodes every frame and reports frozen stretches, black gaps, hard cuts to black at the end, an intro that doesn't animate, wrong duration, low bitrate and missing audio. Use it after every render of an edit, and whenever the user says the video "lags", "drops frames", "freezes", "is static", "cuts off at the end" or looks low quality.
---

# Checking a render

A few spot frames miss most real problems: a clip that freezes for half a second, an intro image
sequence that rendered as a still, a Dip to Black that hard-cuts instead of fading (viewers call it
lag), a 20 Mbps export when 40 was wanted. Check the whole file.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_render.py out.mp4 --intro-frames 105 --expect-seconds 39.8 \
  --min-mbps 15 --fade-frames 50
```
Needs Pillow and `FILMCRAFT_CLI="${user_config.filmcraft_cli}"`. Exit code 1 means fix something;
`problems` says what and where (frames and seconds). `--keep <dir>` keeps the decoded frames for a
look (or for match-grade).

## Reading the results and fixing

| Problem | Usual cause | Fix |
|---|---|---|
| frozen inside the edit | source clip shorter than its slot, a still where a clip should be, a stale image sequence | check the shot's in-point + length; bake sequences (`import_media bake=true`) |
| intro does not animate | the app kept old frames of a re-written image sequence | write frames to a new folder, bake to .mov, re-import |
| ending: cuts to black | Dip to Black on the last clip | `fade` (opacity keyframes) on the last shot and the caption |
| black gaps | a hole between clips, a missing clip (offline media) | `list_timeline`; re-place the clip |
| low bitrate | default export | `render(bitrateMbps: 30-40)` |
| no audio stream | music placed with `audio: false`, or `noAudio` | place the soundtrack on A1 |

"Laggy" can also mean 24 fps clips judder in a 30 fps edit (frame blending fixes it) or the viewer's
player struggling with a high bitrate — frozen-frame analysis tells these apart from real drops.

Then look at frames from each section yourself, and tell the user what you verified and what you
couldn't (listening to the audio).
