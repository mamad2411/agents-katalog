---
name: social-midia
description: Use when the user wants to draft, post, schedule, or analyze content on a social network (LinkedIn, X/Twitter, Instagram, Facebook, TikTok, YouTube, Threads, Reddit), asks about a platform's official API (auth, scopes, endpoints, rate limits, analytics), or needs cross-network publishing workflows. Routes to the per-network skill; does not execute the work itself.
triggers: [user, model]
---

# Social Midia - router

One skill per network. Pick the network, read its `SKILL.md`, then its
`api.md` only when API work is actually needed.

## Safety rules (all networks)

- **Never post, schedule, or authenticate without explicit user
  confirmation.** Drafts are copy-ready blocks; the user publishes.
- Credentials: reference env var **names** only. Never read, print, or
  commit secret values.
- Official APIs only. No browser automation or scraping to post.
- LinkedIn API ToS bans automated posting (Terms 3.1, item 26): LinkedIn is
  draft + paste, always.
- Claims about API behavior must cite the official doc URL from `api.md`.
  Mark anything unverified as UNVERIFIED; never invent limits or features.

## Network picker

| User wants | Read |
|---|---|
| LinkedIn post, article, org page, B2B outreach | `linkedin/SKILL.md` |
| X post, thread, poll, long-form article, replies | `x-twitter/SKILL.md` |
| Instagram post, reel, story, carousel | `instagram/SKILL.md` |
| Facebook Page post, reel, story, scheduled posts | `facebook/SKILL.md` |
| TikTok video or photo post, drafts | `tiktok/SKILL.md` |
| YouTube upload, Shorts, playlist, scheduled premiere-style publish | `youtube/SKILL.md` |
| Threads post, reply moderation, polls | `threads/SKILL.md` |
| Reddit post, comment, subreddit rules, flair | `reddit/SKILL.md` |
| Cross-network scheduling, auth/app setup, ToS constraints | `reference/cross-network.md` |

## Workflow

1. Route to the network SKILL.md. If the task touches the API, also read
   that network's `api.md`.
2. Credential state: check which env var names the network uses (its
   `api.md` lists them). Ask the user whether tokens exist; never ask for
   or print the values.
3. Output drafts as copy-ready fenced blocks. On explicit "yes", hand the
   user the publish steps for their platform (UI steps or API call order
   from `api.md`); the agent does not press publish.

## Where detail lives

- `<net>/SKILL.md`: capabilities, auth model, formats/limits, scheduling,
  analytics, professional routines.
- `<net>/api.md`: endpoints, scopes, upload flows, rate limits, error
  traps, with official doc URLs.
- `reference/cross-network.md`: scheduling matrix, app-review gates,
  automation/ToS constraints, env-var conventions.
- Research provenance: `.devin/research/social-midia/<net>.md`.
