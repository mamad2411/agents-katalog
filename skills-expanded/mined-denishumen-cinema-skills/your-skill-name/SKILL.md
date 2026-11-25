---
name: your-skill-name
description: >-
  What this skill does AND when Claude should use it, in one or two sentences.
  Name the concrete triggers a user would actually type, for example
  "color grade this", "make a LUT", "teal and orange look", "match these shots".
  Max 1024 characters. Third person, no marketing words.
# ---------------------------------------------------------------------------
# Optional fields from the Agent Skills spec (work everywhere):
# license: MIT
# compatibility: Requires ffmpeg 6+ and Python 3.10+ on PATH
# metadata:
#   discipline: color-grading
#   version: "0.1.0"
#   author: your-github-handle
#
# Optional fields that only Claude Code understands. Remove them before
# uploading the skill to claude.ai or the Skills API (they reject unknown keys):
# argument-hint: "[clip-or-folder]"
# allowed-tools: Bash(ffmpeg:*) Bash(ffprobe:*) Read Write
# disable-model-invocation: false
# ---------------------------------------------------------------------------
---

# Skill title

<!--
How to use this template
1. Copy the whole `skill-template/` folder to `skills/<discipline>/<your-skill-name>/`.
2. The folder name and the `name:` field MUST be identical: lowercase letters,
   digits and single hyphens, max 64 chars, starting with the discipline prefix
   (see CONTRIBUTING.md), e.g. `grade-look-builder`.
3. Keep this file under ~500 lines. Move long material to `references/`.
4. Write everything in your own words. No quotes or excerpts from books,
   scripts, manuals or other people's skills — summarise the principle instead
   and credit the source by title and author in "Sources".
5. Delete these HTML comments and every section that does not apply.
-->

One short paragraph: the job this skill does, the result it produces, and where
it sits in the pipeline (brief → script → style bible → shot list → sources →
edit → grade → sound/voice → export).

## When to use

- The user asks for … (list real phrasings and situations)
- A previous pipeline step produced … and the next step is …

## When not to use

- … → use `other-skill-name` instead
- … is out of scope (say why)

## Inputs

| Input | Required | Format | Usually comes from |
|---|---|---|---|
| Style bible | yes | `style-bible.md` | `templates/style-bible.md` / `pipeline-orchestrator` |
| Shot list | no | `shots.csv` | `direct-shot-list` |
| Source media | no | folder of clips / frames | camera, AI generation |

If a required input is missing, ask for it (or offer to create it with the
skill that owns it) instead of guessing.

## Steps

1. **Read the context.** Load the style bible and the relevant part of the
   script or shot list. Restate the goal in one line.
2. **Plan.** List what you will produce and how you will check it. For anything
   that costs money or overwrites files (paid APIs, renders, deletions), show the
   plan and wait for the user's OK.
3. **Do the work.** Concrete, numbered actions. Put exact commands in fenced
   code blocks. Long command recipes go in `references/`, reusable code goes in
   `scripts/`.
4. **Check.** Run the quality checklist below; fix and re-check before reporting.
5. **Hand off.** Save outputs with the naming convention below and name the next
   skill in the pipeline.

## Outputs

| File | Format | Notes |
|---|---|---|
| `…/result.ext` | … | naming: `ep01_sc03_sh07_v001.ext` |

## Quality checklist

- [ ] Matches the style bible (palette, framing rules, sound palette, voice)
- [ ] Continuity holds with the previous and the next shot/scene/episode
- [ ] Technical specs are correct (resolution, fps, color space, loudness …)
- [ ] Files are named and placed per the project layout
- [ ] Nothing copied verbatim from copyrighted sources

## Supporting files

Load these only when needed:

- [references/overview.md](references/overview.md) — deeper explanation, tables, command recipes
- `scripts/example.py` — run it, do not paste it into the conversation

## Sources

Principles in this skill are summarised in our own words from:

- *Book Title* — Author (year)
