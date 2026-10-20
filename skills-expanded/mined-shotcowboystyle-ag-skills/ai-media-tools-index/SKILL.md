---
name: ai-media-tools-index
description: Curated index of agent-callable AI video and audio tooling on GitHub — ComfyUI integrations, MCP servers, agent skill packs, CLIs, agentic video frameworks, podcast pipelines, TTS, transcription, and loudness/denoise tools. Use when choosing an external tool, MCP server, or skill pack for a video or audio production task, or when the bundled runners do not cover a step.
---

# AI media tools index

Two curated indexes of projects that give agents a stable, programmatic surface (skill,
CLI, MCP, SDK) for media work. Models and human-facing GUI apps are out of scope.

| File | Contents |
|---|---|
| `references/video-tools.md` | Video: agentic frameworks, ComfyUI, MCPs, skills (generation, editing, captioning, transcoding) |
| `references/video-tools.json` | Same entries as structured data: description, stars, license, last push, categories, topics |
| `references/audio-tools.md` | Audio: CLIs, MCPs, editing/processing, podcast pipelines, TTS, transcription |
| `references/audio-tools.json` | Same entries as structured data |

## Use

1. Search the `.json` file for the task keyword in `description`, `categories`, or
   `topics`. Rank by fit, then by `pushed_at` recency and `stargazers_count`.
2. Check `archived` and `license` before recommending anything.
3. The snapshot is dated in each `.md` header. Confirm the project's current state at
   its `html_url` before installing it, and say when an entry may be stale.
4. Prefer local tools (FFmpeg, ffmpeg-normalize) for normalization and conversion;
   reach for hosted APIs only when the task needs generation.

## Source and license

Folded in from the `shotcowboystyle/ai-video-tools` and `shotcowboystyle/ai-audio-editing-tools`
indexes. The index content is licensed CC BY 4.0 (see `LICENSE` in this skill directory).
