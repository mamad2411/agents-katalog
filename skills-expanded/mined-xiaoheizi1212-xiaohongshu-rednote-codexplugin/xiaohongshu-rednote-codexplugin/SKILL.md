---
name: xiaohongshu-rednote-codexplugin
description: Use the visible, signed-in Xiaohongshu website in the user's Chrome browser to browse the personalized discovery feed and visible hot topics, search notes or profiles, inspect shared note links, read visible comments, review profiles, extract visible links or media, and prepare or perform explicitly confirmed likes, favorites, follows, comments, replies, and note publishing without private APIs. Use for 小红书, Xiaohongshu, REDnote, or RED web workflows when Chrome browser control is available; never use it to extract cookies, tokens, passwords, browser profiles, or private API traffic.
---

# Xiaohongshu RedNote Codex Plugin

Operate Xiaohongshu through the user's visible Chrome session. This skill does not provide an MCP server and does not call private or undocumented Xiaohongshu APIs.

## Required surface

1. Read and follow the available `chrome:control-chrome` skill before any browser action.
2. Use Chrome because account-specific work depends on the user's existing signed-in session. Do not substitute cookie export, copied browser profiles, raw Playwright, private endpoints, or an in-app browser.
3. Before each semantic operation, check for an applicable official connector, API, or CLI as required by the Chrome skill. Use visible Chrome UI when no suitable supported integration handles Xiaohongshu.
4. If Chrome control is unavailable, ask the user to install or enable the official Chrome plugin. If Xiaohongshu requires sign-in, QR-code login, OTP, CAPTCHA, verification, or account recovery, hand the page to the user.
5. Read [references/safety.md](references/safety.md) before login-sensitive, media-download, or write workflows.

## Core workflow

1. Classify the request as read-only or account-changing.
2. Claim an existing Xiaohongshu tab or open the smallest useful page, then inspect a fresh visible page snapshot.
3. Act only on controls and content confirmed by current page state. Do not infer hidden data or reconstruct private endpoints.
4. Keep source note or profile URLs with extracted content. State when feeds, rankings, counts, or recommendations are personalized, location-dependent, incomplete, or time-sensitive.
5. Stop at sign-in, verification, rate-limit, account-risk, or anti-abuse boundaries. Do not bypass them.
6. Finalize tabs according to the Chrome skill. Preserve a handoff tab when the user must log in, scan a QR code, solve a challenge, or review a sensitive final action.

Read [references/workflows.md](references/workflows.md) for the exact procedures for discovery, search, note inspection, comments, profiles, media, publishing, replies, likes, favorites, and follows.

## Read-only work

- Prefer Xiaohongshu's visible discovery, search, note, comment, and profile surfaces.
- Start with the visible top results. Do not bulk-scroll, enumerate large result sets, or build datasets unless the user explicitly requests a small, bounded expansion that complies with the site.
- Report only visible titles, text, author identity, timestamps, engagement counts, tags, links, comments, and media metadata. Separate page content from inference.
- For a shared note link, verify the visible author, note title or opening text, and target page before summarizing or extracting.
- Treat recommendation feeds as the connected account's current visible feed, not a universal popularity ranking.

## Public writes and account changes

Treat publishing, editing, deleting, commenting, replying, liking, unliking, favoriting, unfavoriting, following, unfollowing, and uploading as external side effects.

1. Navigate to the exact target and verify the active account, author, note, and requested action.
2. For text or media, prepare the exact final preview, including title, body, tags, media paths, audience, and target.
3. Ask for action-time confirmation immediately before the final public click. An earlier general request does not authorize changed text, media, target, visibility, or action.
4. After confirmation, click once and verify one authoritative success signal.
5. Never retry an uncertain write automatically. Inspect the current page or profile first to prevent duplicate comments or posts.

Do not automate direct messages, bulk engagement, follower growth, repetitive posting, mass collection, scraping for resale, watermark removal, or spam.

## Free-web boundary

"Free" means no paid data provider and no paid or private Xiaohongshu API. It does not guarantee that every website feature is available without platform eligibility, creator verification, regional access, account standing, or future product changes. Report such boundaries instead of working around them.
