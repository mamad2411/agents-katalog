---
name: setup
description: Set up Reel Studio in the current project - copy the renderer, engines, scripts and templates into it, install dependencies and check Chrome, ffmpeg and the optional tools. Use right after installing the plugin, when asked to "set up reel studio", or when another skill needs core/render.mjs and it is missing. Also updates the kit with --update.
---

# Setting up Reel Studio in a project

Compositions load `/core/...`, `/engines/...` and `/brands/...` from the project root, so the kit lives in the
project, not only in the plugin. This copies it in once.

1. Kit root: `${CLAUDE_PLUGIN_ROOT}` (set only when this runs from the Claude Code plugin). If that text is shown
   literally (not a path), or you are Codex, Copilot or another agent, the kit is already in this project (a clone of
   the repo, or `npx reel-studio init`). Skip to step 3; to update the kit there, run
   `npx reel-studio@latest init --update`.
2. Run, from the project root:
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/init-project.sh" "${CLAUDE_PLUGIN_ROOT}" .
   ```
   It copies `core/`, `engines/`, `scripts/`, `examples/engines-demo/`, `brands/_template/` and
   `productions/_TEMPLATE/`, adds `AGENTS.md`, `CLAUDE.md` (which imports it), `STATUS.md` and `.gitignore` if missing, adds a `desk` entry to `.claude/launch.json` (so "open the desk" works in the Claude desktop app), never overwrites existing
   files, runs `npm install` in `core/` and prints which tools are found.
   To refresh `core/`, `engines/` and `scripts/` after a plugin update, add `--update` as the third argument.
3. Fix any ❌ the script prints. Fix what you can yourself; for the rest, tell the person in plain words what is
   missing and what it is for, with the one command to paste (e.g. "Video export needs ffmpeg: `brew install
   ffmpeg`"). Chrome elsewhere → `CHROME_PATH=/path/to/chrome`. Don't paste the script's whole output.
4. Check the machine with one frame (no Blender needed):
   ```bash
   node core/render.mjs still examples/engines-demo/index.html /tmp/reel-studio-check.png --t 3
   ```
   Look at the PNG: a toon donut with "Three.js" above it means rendering works.
5. Optional, for a free AI voice: `pip install kokoro-onnx soundfile` (the voice model downloads on first use).
6. Hand over like a person, not a log. The person is usually a marketer: one short message, no paths or tool names.
   For example: "All set, I can make videos here now. What are we promoting? Tell me about the product (a website
   link is perfect) and I'll take it from there." No brand in `brands/` yet → `new-brand`; otherwise → `make-video`.
   Both start as a conversation.
