---
name: varg-previz
description: >-
  Plan and pre-visualise any multi-shot AI video before spending credits on varg - music videos, ads and product promos, UGC-style spots, trailers, short films, explainers. Write the story (Hero's Journey, hook-problem-payoff, 3-act), lock character/product/vehicle sheets and one master plate per location, group shots into master scenes, block every camera in a three.js grey-box previz on the timeline (auto cameras from plain storyboard words like "MCU, 3/4 left, push in"), then export clean previz clips as @video1 references for Seedance 2.5 video-to-video and run one short generation per scene. Any aspect ratio, with or without a song. Use when the user asks for a previz, a 3D animatic, camera blocking or approval, shot lists, scene grouping, character or product sheets, story structure for a clip or ad, or a Seedance video-to-video pack.
license: MIT
metadata:
  author: vargHQ
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://varg.ai
compatibility: >-
  The previz app needs python3 (local server) and a browser; three.js is vendored, no npm.
  Clip capture needs bun + playwright-core + Chrome/Chromium; the pack build needs ffmpeg.
  Generation needs the varg MCP connection (https://mcp.varg.ai/mcp) or a VARG_API_KEY.
allowed-tools: Bash(python3:*) Bash(bun:*) Bash(bunx:*) Bash(ffmpeg:*) Bash(ffprobe:*) Bash(curl:*) Bash(shasum:*) Read Write Edit
---

# varg previz (template folder)

The maintained skill lives in **vargHQ/skills**:
[github.com/vargHQ/skills/tree/main/varg-previz](https://github.com/vargHQ/skills/tree/main/varg-previz).
Install it, or read its SKILL.md before planning a previz:

```bash
npx skills add vargHQ/skills --skill varg-previz
```

Without installing: <https://raw.githubusercontent.com/vargHQ/skills/main/varg-previz/SKILL.md>. The `references/`
here are a snapshot kept for links from other templates; the current versions are in vargHQ/skills.

## What this folder holds

The previz app and its setup script (local, no credits):

```bash
python3 varg-previz/scripts/new_previz.py ~/videos/my-ad --aspect 9:16 --bpm 120 --audio assets/track.mp3
python3 ~/videos/my-ad/previz/serve.py          # http://localhost:8765/previz/
cd ~/videos/my-ad/previz/seedance
python3 tools/build_pack.py --check
bun tools/capture.mjs frames "$(python3 tools/build_pack.py --plan)"   # needs playwright-core + Chrome
python3 tools/build_pack.py frames                                       # video/, requests.json, PROMPTS.md, board
```

`templates/previz/` is the app (sets, shots, posable mannequin, auto cameras, vendored three.js, pack tools, the
space-opera example). Generating from the pack spends varg credits: follow the skill (estimate first, wait for the
user's yes).
