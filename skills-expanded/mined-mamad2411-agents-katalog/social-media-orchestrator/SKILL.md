---
name: social-media-orchestrator
description: "Route a social-media task to the right skill among 8 specialists — making the asset (image/video/audio via fal.ai, explainer animation via Manim, demo capture, video editing, video understanding), adapting copy per platform, and publishing/scheduling to X and 13 networks. USE WHEN a user wants to create, adapt, schedule, or publish social content but hasn't named the specific tool or platform."
cluster: social-media
version: 1.0.0
---

# Social Media Orchestrator

The single entry skill for social-media work. It locates the task on the **create → adapt →
publish** pipeline and delegates to one of 8 specialist spokes. The cross-cutting model every
social task shares — adapt-don't-duplicate per platform, draft-before-post approval, voice
reuse, and the platform/format matrix — lives in `social-media-core`; read it before adapting
copy for more than one network or pushing anything live.

## Routing map (intent → spoke)

**Make the asset (create)**
- Image / video / audio from a prompt → `fal-ai-media` (Nano Banana, Seedance/Kling/Veo, TTS)
- Technical explainer / diagram / graph animation → `manim-video`
- Edit / cut / structure real footage (FFmpeg → polish) → `video-editing`
- Record a product demo / walkthrough / screen capture → `ui-demo`
- See / understand / search existing video & audio, auto-clip moments → `videodb`

**Adapt the copy (per platform)**
- Distribute one idea across X / LinkedIn / Threads / Bluesky without duplicating → `crosspost`
  *(voice + per-platform rules in `social-media-core`)*

**Publish & schedule**
- Direct X/Twitter API — post, thread, media, search, analytics → `x-api`
- Multi-platform scheduling/publishing across 13 networks (SocialClaw) → `social-publisher`

## Folded spokes (extended cluster-map)

Additional specialists folded into this cluster. Route to these the same way — load on demand
(see "Loading spokes on demand" below). They extend the create → adapt → publish pipeline with
content strategy, per-platform CLIs, and bookmark-intake automation.

**Strategy & ideation (before the asset)**
- Plan content pillars, hooks, calendars, repurposing & engagement strategy across LinkedIn / X / IG / TikTok / FB → `social-content`
- Run the full source-to-distribution content pipeline (brief → packet → staging → dry-run/publish), coordinating OpenClaw/Paperclip/Higgsfield/inference.sh adapters → `ai-content-pipeline`

**Per-platform CLIs (read, engage, publish)**
- X/Twitter via inference.sh apps — post/create-with-media, like, retweet, DM, follow → `twitter-automation`
- X/Twitter via the local `bird` CLI — read timelines, search, threads/replies, bookmarks/likes, post (draft→confirm→post) → `bird-cli`
- Instagram via the `gram`/`glam` CLI — login/cookie auth, download profiles/posts/stories/highlights → `gram-cli`
- Reddit via the local `reddit-cli` — read subreddits/users/threads, monitor inbox/mentions, publish with confirmation → `reddit-cli`
- Discord ops via the `message` tool (`channel=discord`) — send/read/react/poll/threads/search → `discord`

**Bookmark intake & opportunity mining**
- Ingest X bookmarks + IG saves, dedupe, AI-enrich, route into a PARA/Obsidian vault → `social-intake-orchestrator`
- Convert X bookmark intake into actionable implementation opportunities + cadence-based Discord digests → `x-bookmark-opportunity-skill`

## Standard Operating Flow

1. Locate the task on the pipeline: are we **creating** an asset, **adapting** copy, or **publishing**? Most "post this" asks touch all three in that order.
2. If the asset is the bottleneck, pick the right maker first: prompt-to-media → `fal-ai-media`; precise explainer → `manim-video`; real footage → `video-editing`; app demo → `ui-demo`; understand/clip existing media → `videodb`.
3. If it lands on **more than one platform**, pull the adapt rules from `social-media-core` and run `crosspost` — never ship identical copy across networks.
4. Publish via the narrowest path: single-network X work → `x-api`; multi-network scheduling/campaigns → `social-publisher`. **Draft for approval before posting** unless the user explicitly said post now.
5. Return: chosen spoke(s), the asset(s) produced, the platform-specific variants, scheduling/approval state, and the next action.

## Guardrails

See `social-media-core`. In short: **adapt, don't duplicate** — every platform gets a native
version, never the same copy in four costumes; **draft before you post** — return for approval
unless told otherwise; reuse a captured `VOICE PROFILE` rather than re-inventing tone; keep
provider secrets in env vars, never in source or logs; treat rate limits and write-permission
tiers (especially X) as runtime facts to read, not static tables to hardcode. The cluster's
value is platform-fit content shipped safely — don't quietly mass-broadcast or post unreviewed.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
