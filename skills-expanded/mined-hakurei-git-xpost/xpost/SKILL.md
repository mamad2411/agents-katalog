---
name: xpost
description: "Operate X/Twitter engagement workflows from a browser session: explore or choose a topic, optionally enrich topic context with Hermes Tweet/Xquik, understand visible posts, draft and publish topic-relevant posts, attach images, like posts, and write human-sounding replies. Use when the user asks Codex to post on X, create an X post from a topic, run an X engagement round, randomly like posts, comment on topical posts, or prepare/verify X drafts with optional image upload and rate-limit checks."
---

# xpost

## Overview

Use this skill to run controlled X engagement workflows through an available browser automation surface. The shared, portable workflow lives in [references/workflow.md](references/workflow.md); read it before performing any X action.

This skill supports:

- topic discovery and comprehension
- optional read-only Hermes Tweet/Xquik topic evidence before browser verification
- named topic and preferred-topic browsing, with exclusions for topics/categories the user dislikes
- broad randomized topic sampling instead of repeatedly choosing top Explore trends
- human-sounding post and reply generation
- configurable language and tone
- optional image attachment
- randomized likes
- one-round task mode with summary
- conservative frequency checks
- browser-tool fallback order, including DrissionPage paste for image upload when normal upload fails

## Quick Start

1. Read [references/workflow.md](references/workflow.md).
2. Resolve the requested configuration: language, tone, whether to post, whether to comment, like count, image behavior, and whether the task is draft-only or publish-enabled.
3. Open or reuse an authenticated X browser session.
4. Before publishing any post or reply, verify the visible composer content matches the intended text and media.
5. After the round, summarize what was posted, replied to, liked, skipped, and any failures.

## Login Handling

Never collect X credentials in chat. Reuse an authenticated browser session when available. If X is logged out, open the login page and ask the user to complete login, 2FA, CAPTCHA, or verification manually in the browser. Resume only after verifying the logged-in X UI is visible.

## Browser Capability Order

Prefer tools in this order:

1. Native browser plugin/skill available in the current agent.
2. Existing browser MCP/devtools tools.
3. DrissionPage attached to an existing Chromium debugging port.
4. User-guided manual takeover for blocked steps.
5. Install or download additional browser tooling only with explicit user approval or an already-approved environment rule.

## Requirements and Optional Dependencies

Required:

- an AI agent that can read this skill
- an authenticated X browser session
- at least one browser automation surface, browser plugin, MCP/devtools tool, or user-guided browser takeover

Optional:

- Python 3
- DrissionPage
- `HERMES_TWEET_API_KEY` or `XQUIK_API_KEY` for optional read-only topic context

DrissionPage is not a hard dependency. Use it only as a fallback for Windows clipboard image paste when normal X image upload fails. If Python or DrissionPage is unavailable, continue with available browser tools. For image posts, try native upload first; if upload fails and no paste-capable tool exists, ask the user to attach the image manually or explicitly approve text-only posting.

Hermes Tweet/Xquik is optional and read-only in this skill. Use it only when `topic_context_source=hermes_tweet` is configured and a key is already available in the local environment. Never ask the user to paste API keys into chat. Search results can suggest candidate posts or angles, but public likes, replies, and posts still require visible browser verification.

## Helper Scripts

Use scripts only when the active environment supports them:

- `scripts/set_clipboard_image.ps1`: place an image file onto the Windows clipboard as bitmap data.
- `scripts/drission_ctrl_v.py`: connect to an existing Chromium debug session and send Ctrl+V through DrissionPage.

For image posting on X, first try the native file upload UI. If it does not produce a visible image preview, put the image itself on the clipboard and paste with DrissionPage. Do not publish until the image preview is visible.

## Publishing Flags

Treat standalone posts and replies independently:

- `publish_post=false` means do not publish a standalone/main post.
- `publish_reply=true` means a reply may be published when `comment=true` and `draft_only=false`.
- `draft_only=true` blocks all public posting, including replies.
- `require_final_confirmation=true` means show the final text/media plan and wait for approval before clicking `Post` or `Reply`.
- `require_final_confirmation=false` means publish after verification without asking again when the relevant publish flag is enabled.

Do not infer that `publish_post=false` blocks replies.

## Topic Preferences

When the user says `browse posts about {topic}`, `find a topic about {topic}`, `browse {topic} posts`, or asks to browse a specific topic, treat `{topic}` as `topic_query` and search/open that topic directly. Do not fall back to generic Explore trends unless the named topic has no usable posts. Respect `preferred_topics`, `excluded_topics`, and `excluded_topic_categories`.

Default behavior is draft-and-confirm. When a user says "post", "publish", "发", "发布", or "发一个帖子", infer the relevant publish flag as `true`, draft the content, and wait for final confirmation. Skip confirmation only when the user says "directly publish", "no confirmation", "不用确认", or sets `require_final_confirmation=false`.
