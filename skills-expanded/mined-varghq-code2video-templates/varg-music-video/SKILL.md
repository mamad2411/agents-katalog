---
name: varg-music-video
description: >-
  Make an AI music video with varg from a song: measure the song (beats, downbeats, word timings), write a story that
  visualises the lyrics, storyboard it on the beat grid, lock character/vehicle/location anchors, generate short
  Seedance scenes, QA every output, cut them frame-exact onto the song, add lyrics and graphics in HyperFrames, run
  director-note rounds and export (incl. a small file for Telegram). Use when the user wants a music video, a clip for
  a track, a lyric-driven AI video, an anime/cinematic video to a song, or asks how such a video is made. Simple path
  first; for heavy camera/geography work hand over to varg-previz.
metadata:
  author: vargHQ
  version: "1.0.0"
compatibility: >-
  python3 with librosa (song map) and optionally faster-whisper (word timings); ffmpeg/ffprobe; HyperFrames CLI for
  the graphics pass; varg MCP (https://mcp.varg.ai/mcp) for generation.
---

# varg music video (template folder)

The maintained skill lives in **vargHQ/skills**:
[github.com/vargHQ/skills/tree/main/varg-music-video](https://github.com/vargHQ/skills/tree/main/varg-music-video).
Install it, or read its SKILL.md before making a music video:

```bash
npx skills add vargHQ/skills --skill varg-music-video
```

Without installing: <https://raw.githubusercontent.com/vargHQ/skills/main/varg-music-video/SKILL.md>. The worked
99 s anime example (file formats, QA, director notes) is its `references/anime-case-study.md`.

## What this folder holds

The four scripts that the skill links to. They run locally and cost no credits:

```bash
python3 varg-music-video/scripts/songmap.py assets/song.mp3 --lyrics lyrics.txt --out songmap.json   # librosa (+ faster-whisper for words); --bpm if the generator gives it
python3 varg-music-video/scripts/rough_cut.py storyboard.json place.json renders/cut.mp4 --clips out/ --audio assets/song.mp3
bash varg-music-video/scripts/contact_sheet.sh renders/cut.mp4 qa/cut.jpg 2    # timestamped QA sheet
bash varg-music-video/scripts/tg_export.sh renders/final_v1.mp4               # small copy for Telegram (add 720 for ~15-18 MB)
```

Generating the scenes spends varg credits: follow the skill (estimate first, wait for the user's yes).
