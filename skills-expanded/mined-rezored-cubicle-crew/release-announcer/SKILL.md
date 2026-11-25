---
name: release-announcer
description: Prepare social media announcements (LinkedIn, Facebook, X, Reddit) for a new release of Cubicle Crew and stage them in the user's browser, filled in and waiting for the user to press Publish, or scheduled where the platform supports it. Use this skill whenever the user mentions a new version, release, tag, changelog or "what's new" together with posting, announcing, sharing or promoting it, or asks to prepare/draft/schedule posts for LinkedIn, Facebook, X/Twitter or Reddit about the project — even if they only say "пусни постове за новата версия" or "announce the release".
---

# Release Announcer

Turn a new Cubicle Crew release into four platform-specific posts and stage them in the
user's own logged-in browser. The user stays the one who publishes: the skill fills in
composers and stops. That matters because posting is public, hard to undo, and each
platform punishes things that look automated or spammy.

## Hard rule: never publish on your own

Never click Post / Publish / Tweet / Share / Submit. Stop with the composer filled in.
Clicking **Schedule** is allowed only when the config says `"mode": "schedule"` for that
platform AND the user approved the summary in step 5 in this conversation. If a dialog,
captcha, login prompt or unexpected screen appears, stop on that platform and tell the
user, rather than clicking through it.

## Workflow

### 1. Load the config

Read `.claude/release-announcer.json` in the repo root. If it doesn't exist, copy
`assets/config.example.json` there, then ask the user the few questions needed to fill it
(Facebook profile or Page, which subreddits, post language, draft vs schedule, preferred
time). Ask once; after that the config is the source of truth.

### 2. Find out what's new

Work out the version and the changes, in this order of preference:

1. `gh release view <tag> --json tagName,name,body,url,assets` (latest if no tag given)
2. `git describe --tags --abbrev=0` and `git log <prev-tag>..<tag> --oneline --no-merges`
3. `package.json` version and any CHANGELOG / release notes in `docs/`

Read the README's feature table so you describe features the way the project does.
Pick 2–4 changes a *user* would care about (new shop items, a new lounge activity, a
fix for something annoying). Skip refactors, CI, dependency bumps unless they're the
whole release. If you can't tell what changed, ask instead of inventing features.

### 3. Write the posts

Read `references/writing.md` for voice and per-platform shape. Write one post per
enabled platform — don't paste the same text everywhere; each platform has its own
audience and length. Always include the release link (or the repo link) and mention
the media you plan to attach.

Pick media from `docs/media/` (e.g. `demo.gif`, `trailer.mp4`, `states.png`,
`night.png`) or from new screenshots the release adds.

### 4. Save a review file first

Write everything to `release-posts/<version>.md` (one section per platform, with
character counts and the chosen media). This is the fallback: if the browser part fails,
the user can still copy-paste. Add `release-posts/` to `.gitignore` if it isn't there.

### 5. Show the summary and get a go-ahead

Show the user the posts (or point to the file) and a one-line plan per platform, e.g.
"LinkedIn: schedule Tue 10:00 · X: draft · Facebook: draft · Reddit r/ClaudeAI: draft".
Wait for an OK or edits before opening the browser.

### 6. Stage in the browser

Use whichever browser tool is available — Claude in Chrome (start Claude Code with
`--chrome` or run `/chrome`) is preferred because it uses the user's logged-in sessions.
A Playwright-style MCP works too, but then the user has to log in in that browser.

Open **one tab per platform** and leave each tab open. Follow `references/platforms.md`
for each site's composer, limits, scheduling and quirks. Platform UIs change often: if
an element isn't where the reference says, look at the page and adapt, and if you
genuinely can't find it, stop on that platform and report rather than guessing.

Attach media if the browser tool can upload files. If it can't, leave the composer
filled and tell the user exactly which file to attach.

### 7. Report

End with a short checklist the user can act on:

- which tabs are open and waiting for a click
- what got scheduled and for when
- anything skipped and why (e.g. "Reddit: r/SideProject only allows self-promo on Saturdays")
- media still to attach by hand

## Files

- `references/platforms.md` — per-platform composer, limits, scheduling, rules. Read before step 6.
- `references/writing.md` — voice and post templates. Read before step 3.
- `assets/config.example.json` — config template.
