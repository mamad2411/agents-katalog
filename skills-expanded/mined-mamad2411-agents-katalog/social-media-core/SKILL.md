---
name: social-media-core
description: "Shared reference for the social-media cluster: the adapt-don't-duplicate model, the draft-before-post approval contract, voice-profile reuse, the platform × format matrix, and the create→adapt→publish pipeline every spoke shares. USE WHEN adapting copy for more than one network, choosing a publish path, or producing an asset — the interlocking rules that keep the spokes consistent."
cluster: social-media
version: 1.0.0
---

# Social Media Core

Shared model for the `social-media` cluster. The asset-makers, the adapter, and the publishers
all depend on these interlocking conventions — keep them consistent here so no spoke contradicts
another.

## 1. The decision this cluster turns on: adapt, don't duplicate

The defining move is **never broadcast identical copy across platforms**. One underlying idea
becomes one native version per network:

```
Idea ──> Primary version (strongest native form) ──adapt──> per-platform variants
                                                   (constraint, not stereotype)
```

- Start from the **strongest source version** (the original post, thread, article, or changelog), not a lowest-common-denominator blurb.
- Adapt for each platform's **constraints**, not its clichés: compress for X, add only outside-the-niche context for LinkedIn, stay direct on Threads/Bluesky.
- One post still says one thing. Don't bolt on a CTA, question, or "professional takeaway" the source didn't earn. → `crosspost`

**Rule:** each variant should read like the *same author under a different constraint* — never
the same string pasted four times, never padded or sanitized to fit a platform stereotype.

## 2. Draft-before-post contract

Publishing is **approval-gated by default**. Generate → validate → return the draft → post only
after the user approves, unless they explicitly said "post now". Validate length, thread
structure, and media before going live. This is the single safety boundary the publish spokes
share. → `x-api`, `social-publisher`, `crosspost`

## 3. Voice reuse

Capture voice **once**, reuse everywhere. If a `VOICE PROFILE` already exists in the session
(from `brand-voice` / `content-engine`), reuse it directly — do not build a second ad-hoc voice
checklist per platform. Pull recent original posts (`x-api`) when voice matching matters.

## 4. The create → adapt → publish pipeline

Most "make and post this" asks flow through three stages; pick the spoke per stage:

```
CREATE the asset ──> ADAPT the copy ──> PUBLISH
```

- **Create** — prompt-to-media (`fal-ai-media`), precise explainer (`manim-video`), real-footage edit (`video-editing`), app demo (`ui-demo`), understand/clip existing media (`videodb`).
- **Adapt** — one idea → per-platform variants (`crosspost`).
- **Publish** — single-network X (`x-api`) or multi-network scheduling (`social-publisher`).

## 5. Platform × format matrix

| Platform | Publish via | Native copy shape | Media notes |
|---|---|---|---|
| X / Twitter | `x-api` (direct) or `social-publisher` | compressed; thread only if one post would collapse it; no filler hashtags | image/video via v1.1 media upload |
| LinkedIn (profile / page) | `social-publisher` | add only outside-niche context; no forced founder-reflection | image/video, doc carousels |
| Threads | `crosspost` adapt + client | readable, direct; no fake hyper-casual creator copy | image/video |
| Bluesky | `crosspost` adapt + client | concise, preserve cadence; no feed-gaming | image |
| Instagram / TikTok / YouTube / Reddit / Facebook / WordPress / Discord / Telegram / Pinterest | `social-publisher` | platform-native, per its norms | media uploaded as assets first |

Provider keys for `social-publisher`: `x`, `linkedin`, `linkedin_page`, `instagram_business`,
`instagram`, `facebook`, `tiktok`, `youtube`, `reddit`, `wordpress`, `discord`, `telegram`,
`pinterest`.

## 6. Asset-format conventions

- Short-form video defaults to **16:9** unless the user asks vertical; export a clean thumbnail/poster that reads at social size. → `manim-video`, `video-editing`
- Smoke-test renders at low quality first; push to high quality only after composition and timing are stable.
- Generated media (`fal-ai-media`) and understood/clipped media (`videodb`) feed the editor (`video-editing`) before publish.
- Demo capture (`ui-demo`) produces WebM with a visible cursor and natural pacing.

## 7. Shared guardrails

- **Adapt, don't duplicate**: native version per platform; never identical copy across networks.
- **Draft before post**: return for approval unless told "post now"; validate length/threads/media.
- Reuse a captured `VOICE PROFILE`; don't re-invent tone per platform.
- Secrets (`SC_API_KEY`, `X_CONSUMER_*`, `X_ACCESS_TOKEN*`, fal keys) live in env vars — never in source, logs, or commits; rotate on exposure; prefer read-only tokens.
- Rate limits and write-permission **tiers are runtime facts** — read `x-rate-limit-*` headers and back off; don't hardcode quota tables. X API in particular is drift-prone — verify current developer docs before quoting limits.
- Delete banned filler ("Excited to share", "Here's what I learned", "What do you think?", "link in bio" unless literally true) on every platform.
