---
name: reddit-post-engagement
description: Publish a Reddit post and/or drive an FAQ-style comment thread on it from an existing logged-in session. Use when the user asks to share a project on Reddit, reply to questions on their post, or add comments with links on a post. Covers rate-limit pacing for low-karma accounts and the working API path on old.reddit.com.
---

# Reddit Post + Engagement Thread

## When to use
- Sharing a project/bot on Reddit (text post with story + credits + repo link).
- Adding 5-10 FAQ-style self-comments answering "questions" about features/functions, each linking the repo.

## Verified working path (old.reddit.com)
- New-Reddit shreddit submit/comment UI: DO NOT use. Shadow-DOM synthetic events never enable Post, and `/api/submit` fetches from that page return 403.
- Navigate the logged-in session to `https://old.reddit.com/r/<SUBREDDIT>/submit` (or the post page for comments).
- Read the modhash: `uh` from `input[name="uh"]` on the page, or `(await fetch('/api/me.json')).json().data.modhash`.
- Text-post kind: the hidden `input[name="kind"]` must be `self` (form defaults to `link` → submit rejects with "Please enter a URL").
- Submit: `fetch('/api/submit', {POST, Content-Type: application/x-www-form-urlencoded, body: uh, kind='self', sr, title, text, api_type='json'})` with `credentials:'same-origin'`. Success → `data.url` = new post URL.
- Comment: same pattern against `/api/comment` with `thing_id=t3_<id>` (post) and `api_type='json'`.
- Form `submit()`/button clicks are unreliable (a field named `submit` shadows the method; JS click handlers silently no-op).

## Rate limiting (low-karma accounts) — CRITICAL
- Posting more than ~2 comments in a few minutes → `RATELIMIT "Take a break for 8-9 minutes"`.
- Sustainable cadence: 1 comment per ~9-10 minutes, or after each success wait ~8.5 min (use a 510s sleep between attempts).
- If `RATELIMIT 1 minute` appears, wait ~75s and retry the same comment (do not skip).
- Do NOT batch-comment inside one evaluate call that outlives the MCP timeout — each comment should be its own call, with sleeps done OUTSIDE the page (PowerShell `Start-Sleep`), never `await sleep` inside evaluate (kills the request).

## Content rules
- Every comment answers one feature/function question in `Q: ... A: ...` form.
- Every comment ends with the repo URL, e.g. `github.com/yashas-13/anything-telegram`.
- Official credits (Pravidhi Solutions, Yashas Prakash, BrowserClaw/BrowserOS MCP, Claude Code, opencode, 9router, Telegram, GitHub) belong in the main post body.

## Verification
- Reload the post page: the `N comments` count must equal the number posted, and each author link must be the posting account.
- If a post/comment is removed (AutoModerator), the page shows it but content is `[removed]` — surface this to the user.
