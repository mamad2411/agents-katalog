---
name: blog-init
description: |
  This skill should be used when the user runs /4d-blog-engine:blog-init or asks any variant of "set up the blog plugin," "configure 4d-blog-engine for my repo," or "initialize a new blog project." The plugin's user is a WRITER. The setup form asks only what a writer can answer in plain English. Output is a single blog-project-instructions.md file in the writer's blog project directory. Do NOT use this skill for: starting a session on an already-initialized project (use /4d-blog-engine:blog-start), running the actual pipeline (use /4d-blog-engine:blog-pipeline), or publishing a finished post (use /4d-blog-engine:blog-publish).
allowed-tools: [Read, Write, AskUserQuestion, Bash, Glob, mcp__cowork__request_cowork_directory]
---

# Blog-Init — minimal writer-friendly setup

> **Read this when:** the user runs `/4d-blog-engine:blog-init`. The user is a writer. The form asks what the writer knows. Nothing else. The marker file records what the writer said. Nothing else.

## Hard rules — read these first

These rules exist because earlier versions of this skill repeatedly regressed toward asking the writer technical questions or stuffing detected backend values into the user-facing output. Stop.

1. **Do not ask the writer about Payload collections, Payload API URLs, Payload auth modes, server addresses, environment files, static site generators, or any backend infrastructure.** The writer doesn't know and doesn't need to.
2. **Do not read `.env.local`, `payload.config.*`, or any other backend config during setup.** Detection at setup time has no purpose — the writer hasn't published anything yet. Whatever publish needs, publish will figure out at publish time.
3. **Do not display backend values in the setup summary.** No "API base: localhost:3000". No "Auth status: unconfigured". No "Content collection: posts". The writer's eyes should see only what the writer answered.
4. **Do not infer brand options from context.** The four hero vibes below are the only options. The writer's folder choice is not a hint for additional brand options.
5. **Total writer-facing questions: at most 5.** Two folder picks, one name, one vibe, one optional live URL. Nothing more.

## STEP 0 — Re-init check (silent)

Use `Glob` to look for an existing `blog-project-instructions.md` at standard locations. If found, read it silently and use its values as defaults below. Don't announce the re-init.

## STEP 1 — Pick the blog project directory

Call `mcp__cowork__request_cowork_directory` with no `path`. The OS folder picker opens. The writer picks visually.

If they dismiss without picking, ask once whether to retry or cancel.

Store as `BLOG_PROJECT_DIR`.

## STEP 2 — Pick the publishing repo

Call `mcp__cowork__request_cowork_directory` again with no `path`. The writer picks the local clone of their blog's GitHub repo.

Validate only that it's a git repo (silent on pass):

```bash
test -d "<picked>/.git" || echo "not_git"
```

If not a git repo, ask whether to retry the picker: *"That folder isn't a git repo. Pick the folder that contains your blog's `.git` directory."*

Do **not** check for `payload.config.*` here. Do **not** read `.env.local`. The writer might be picking this folder before they've finished setting up the backend, and that's fine — setup doesn't need to know.

Store as `PUBLISHING_REPO_DIR`.

## STEP 3 — Author name

> *What name should appear as the author on posts you publish?*

Free-text. Store as `AUTHOR_NAME`.

## STEP 4 — Hero scene palette

The Release Owner Gate builds the hero for each post as a **labeled Excalidraw story scene** — title bar + 2-panel + concept icons + arrows + optional micro-chart, drawn from the post's actual content. It never generates abstract AI cover art. The palette below sets the three colors the scene uses; everything else (composition, icons, labels) is derived from the post itself.

Present exactly these four palette options via `AskUserQuestion`. **Do not add additional options inferred from the writer's folder choice or any other context.**

| Palette | Ground | Accent | Secondary |
|---|---|---|---|
| Warm editorial (Recommended) | `#F8F1E5` warm off-white | `#2C3E50` deep navy | `#C9A66B` muted gold |
| Neutral notebook | `#F4F4F2` bone | `#1A1A1A` near-black | `#6B7280` cool gray |
| Bold graphic | `#FFFFFF` white | `#000000` black | `#FF3333` signal red |
| Dark atmospheric | `#0A0A0A` near-black ground | `#E8E8E8` paper | `#6B7280` cool gray |

All share: aspect ratio = `16:9`; dimensions = `1600x900`; hand-drawn line weight; no photoreal rendering, no glossy 3D, no abstract gradients. Forbidden = `photoreal rendering, AI-cover gradients, stock-photo people, network-graph clichés` — labeled human silhouettes/hands as illustrated icons are fine when the story calls for them.

Store the picked palette's `BRAND_VIBE_NAME` (e.g. `warm-editorial`), `BRAND_PALETTE` (the three hex codes), and the fixed `BRAND_KEYWORDS = "labeled excalidraw story scene, hand-drawn, editorial infographic"`, `BRAND_FORBIDDEN`, `BRAND_ASPECT`, `BRAND_DIMENSIONS`.

## STEP 5 — Live site URL pattern (optional)

> *Optional. What's your blog's live URL pattern? Used to show you the live link after publishing. Use `{slug}` for the post slug. Example: `https://myblog.com/blog/{slug}/`. Leave blank to skip.*

Free-text, blank-allowed. Store as `LIVE_URL_PATTERN`.

## STEP 6 — Voice file check (silent)

Slugify `AUTHOR_NAME` to kebab-case (lowercase, ASCII, spaces and punctuation become hyphens). Example: "Jane Doe" → `jane-doe`. Store as `AUTHOR_SLUG`.

Check whether `<BLOG_PROJECT_DIR>/<AUTHOR_SLUG>-voice.md` already exists. Store the boolean as `VOICE_FILE_EXISTS`. Don't ask the writer about voice yet — that happens at the end. The check is just so the summary can route them to the right next step.

## STEP 7 — Write the marker file

Compose and write to `<BLOG_PROJECT_DIR>/blog-project-instructions.md`:

```markdown
---
title: "4D Blog Engine — Project Instructions"
date: <today YYYY-MM-DD>
type: reference
status: active
plugin: 4d-blog-engine
plugin_version_at_init: 0.4.0
schema: blog-project-instructions/v4
---

# 4D Blog Engine — Project Instructions

This file is the marker the 4d-blog-engine plugin uses to find your blog project. Don't move or rename it.

## Setup

- **Blog project directory:** `<BLOG_PROJECT_DIR>`
- **Publishing repo:** `<PUBLISHING_REPO_DIR>`
- **Author:** `<AUTHOR_NAME>`
- **Author slug:** `<AUTHOR_SLUG>` (used to resolve the voice file path)
- **Voice files:** any `*-voice.md` in this directory. The pipeline picks based on which one(s) exist. Default author's file would be `<AUTHOR_SLUG>-voice.md`. Create with `/4d-blog-engine:blog-voice`; run more than once for multiple authors (guest contributors, co-writers).
- **Hero scene palette:** `<BRAND_VIBE_NAME>`
- **Live site URL pattern:** `<LIVE_URL_PATTERN or "(not set)">`

## Hero image brand style

The Release Owner Gate uses this block to compose the hero-image prompt for each post. Edit values here to change the look without re-running `/blog-init`.

- **Palette:** `<BRAND_PALETTE>`
- **Style keywords:** `<BRAND_KEYWORDS>`
- **Forbidden elements:** `<BRAND_FORBIDDEN>`
- **Aspect ratio:** `<BRAND_ASPECT>`
- **Dimensions:** `<BRAND_DIMENSIONS>`

## How to change anything

Edit values above directly. The plugin reads this file every time you run `/blog-start`, `/blog`, or `/blog-publish`. No need to re-run `/blog-init` unless the directory paths themselves change.
```

## STEP 8 — Create Posts/, drafts/, and drafts/blog-media/ subdirectories

```bash
mkdir -p "<BLOG_PROJECT_DIR>/Posts"
mkdir -p "<BLOG_PROJECT_DIR>/drafts"
mkdir -p "<BLOG_PROJECT_DIR>/drafts/blog-media"
```

Silent. No announcement.

The folders have distinct roles in the writer's mental model:

- **`Posts/<slug>/`** — the pipeline's forensic working directory for each piece. Holds the four-phase artifacts (`01-delegation.md`, `02-description.md`, `03-discernment/*`, `04-diligence/*`), the state file, the changelog. Heavy and detailed.
- **`drafts/<slug>.md`** — clean single-file drafts. Phase 4 sign-off copies the signed `04-diligence/blog.md` here automatically. The writer can read and tweak the draft directly without digging into the pipeline folders. `/blog-publish` reads from `drafts/` (not from `Posts/`).
- **`drafts/blog-media/`** — non-hero attachments referenced from a post's `media:` YAML frontmatter (spreadsheets, PDFs, audio, etc.). Drop files here; reference them in your post as `media: [{ file: /blog-media/<filename>, caption: "..." }]`. On `/blog-publish`, the file is copied to the publishing repo's `public/blog-media/<filename>` so the post's link resolves at the live URL `/blog-media/<filename>`.

## STEP 9 — Report back and route to next step

The report-back depends on whether a voice file already exists (the `VOICE_FILE_EXISTS` boolean from STEP 6).

**If a voice file already exists** at `<BLOG_PROJECT_DIR>/<AUTHOR_SLUG>-voice.md`:

```
Blog project ready.

  Project folder: <BLOG_PROJECT_DIR>
  Publishing to:  <PUBLISHING_REPO_DIR>
  Author:         <AUTHOR_NAME>
  Voice file:     <AUTHOR_SLUG>-voice.md (found)
  Hero scene:     <BRAND_VIBE_NAME> palette

Next: run /4d-blog-engine:blog-pipeline <path-to-your-base-document> to write your first post.
```

**If no voice file exists yet**, offer to run `/blog-voice` now via `AskUserQuestion`:

```
Blog project ready.

  Project folder: <BLOG_PROJECT_DIR>
  Publishing to:  <PUBLISHING_REPO_DIR>
  Author:         <AUTHOR_NAME>
  Voice file:     <AUTHOR_SLUG>-voice.md (not created yet)
  Hero scene:     <BRAND_VIBE_NAME> palette

The pipeline needs a voice profile before it can write in your voice.
That's an 8-question interview — usually 15-40 minutes — that produces
the file the pipeline uses as STEP 0 of every post.

Want to do the voice interview now, or later?
```

Options for `AskUserQuestion`:

1. **Run /blog-voice now** — hands off to the `blog-voice` skill.
2. **Later** — leave the marker file as is. The writer can run `/4d-blog-engine:blog-voice` whenever they're ready. Note in the report-back that they must complete the voice interview before `/blog` will run.
3. **I have a voice file from elsewhere — let me drop it in** — surfaces a one-line instruction: *"Copy your voice file to `<BLOG_PROJECT_DIR>/<AUTHOR_SLUG>-voice.md` and you're done. The plugin reads from disk, doesn't care who produced the file."*

That's the entire summary. The writer sees what the writer chose plus a clear path to the voice file. No technical infrastructure values.

## What this skill does NOT do

- It does not read `payload.config.*`.
- It does not read `.env.local`.
- It does not detect, store, or display backend infrastructure values.
- It does not validate that the publishing repo is a Payload project. (Publish will check that at publish time, when the writer is actually trying to publish.)
- It does not infer brand vibes from context.

## Degradation behaviors

- **Folder picker unavailable** (remote Cowork session): fall back to `AskUserQuestion` with a couple of plausible default paths plus a "Custom" free-text option. Surface a one-line note that the picker is unavailable.
- **Writer wants a brand vibe outside the 4 options:** tell them they can edit the brand-style block in `blog-project-instructions.md` directly to customize the palette and keywords. Don't add a fifth option in this skill.
