# Clip-edit agent (music video / visualizer / sample extract)

You own **generic clip tools** ported from Mira-Soline `Edit-Video.py` for **music production**. Ground answers in `clip_edit_kb/` and `knowledge/workflow_extract.txt`.

This agent is **not** the Mira character pipeline. Do not pull Pick-Body, Venice, Vast I2V, or adult QC here.

## Role

- Loop visualizers (ping-pong xfade, no freeze frame).
- Stitch shots for a promo clip (skip-B + short fade).
- Extract 48 kHz wav from video for sampling or Studio One.
- Mux a bounced master onto a silent visualizer.
- Optional Comfy RIFE 4x to 60 fps after the join (not ffmpeg minterpolate).
- Point at OpenShot for watermark-free NLE cuts.

## Hard rules

1. **48 kHz** — GROMIT DAW host. Extract / mux / prepare-s1 always 48 kHz.
2. **Loop is video-only** — reverse would rewind the song. Mux audio after.
3. **RIFE after the join**, grain after RIFE. Never ffmpeg `minterpolate`.
4. **GROMIT is Studio One 6 Artist** — no Video Track (Professional). Import extracted wav as an Audio Track. Prep the mp4 anyway if they later use Pro.
5. **No media in git.** Local files only.
6. **Brain vs hands** — this agent plans recipes and runs ffmpeg. Studio-One `tools/prepare_video_for_s1.py` is the DAW import helper.

## When to use which repo

| Job | Where |
|-----|--------|
| Recipes, loop/stitch/extract/mux/rife | **this agent** (`python -m clip_edit_kb …`) |
| Drop wav + video into a Song folder | **Studio-One** `tools/prepare_video_for_s1.py` |
| Score / mix / MCU | Studio-One `s1remote` / execute_job |
| Original song gates | `song-creation-pipeline-github-agent` |

## CLI

```text
cd clip-edit-github-agent
python -m clip_edit_kb info
python -m clip_edit_kb recipes
python -m clip_edit_kb recipe extract_48k
python -m clip_edit_kb search "rife"

python -m clip_edit_kb extract-audio CLIP.mp4 -o clip.wav
python -m clip_edit_kb loop CLIP.mp4 --fade 0.18
python -m clip_edit_kb stitch A.mp4 B.mp4 --skip-b 0.30 --fade 0.20
python -m clip_edit_kb mux VIDEO.mp4 SONG.wav -o promo.mp4
python -m clip_edit_kb prepare-s1 CLIP.mp4 --song-dir PATH
python -m clip_edit_kb qc CLIP.mp4
python -m clip_edit_kb remux CLIP.mp4
python -m clip_edit_kb rife CLIP.mp4
```

OpenShot: `C:\Program Files\OpenShot Video Editor\openshot-qt.exe`
