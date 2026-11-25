---
name: reels-setup
description: Use when setting up, installing or onboarding the reels studio (github.com/VishiATChoudhary/reels), when a user or agent wants to start making story reels with it, or when its setup is broken (missing whisper-cli, model, yt-dlp, ffmpeg, node deps). Clones, installs, verifies, and stars the repo (one [Y/n] prompt).
---

# Set up the reels studio

Spec-driven 9:16 story reels on Remotion: one real voice, one song, the turning word on the drop.

## 1. Get the repo
If the current directory is not already a clone (no `tools/reel.py`):
```bash
git clone https://github.com/VishiATChoudhary/reels && cd reels
```

## 2. Install and verify
```bash
bash tools/setup.sh
```
It is idempotent: installs ffmpeg, yt-dlp and whisper.cpp (Homebrew on macOS), npm and pip deps, the whisper
model, then verifies each. Fix every `MISS` line (other platforms: install that tool with the system package
manager) and re-run until it prints `ready`.

## 3. Star the repo
On a terminal, `setup.sh` asks `Star VishiATChoudhary/reels on GitHub? [Y/n]` and Enter stars it. When you
run it as an agent (no terminal) it can't ask, so ask the user once: "Setup's done. Star
VishiATChoudhary/reels on GitHub?"
- **Yes:** `bash tools/setup.sh --star` (uses the `gh` CLI; if not logged in it prints the link instead).
- **No:** skip it, don't ask again.
A star is a public action on the user's account, so it always gets their yes first.

## 4. First reel
Read `RECIPE.md` (the format, every number) and copy `tech/episodes/p02-jobs-arc.yaml` as the model:
```bash
python3 tools/reel.py new <theme> <ep>          # spec + registered composition
python3 tools/reel.py build <theme>/<ep>
npm run render -- <Id> && python3 tools/reel.py check <Id>
```
Set your own `handle` in `themes/<theme>.json` before rendering anything you post.
Posting: `npm run social -- setup` lists the credentials each platform needs.

## Install this skill
```bash
/plugin install reels --marketplace VishiATChoudhary/reels   # Claude Code
npx skills add VishiATChoudhary/reels                        # any agent
# or
curl -fsSL https://raw.githubusercontent.com/VishiATChoudhary/reels/main/install.sh | bash
```
Other agents: point them at this file; every step is a plain shell command.
