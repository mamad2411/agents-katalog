---
name: crossbar
description: Use the user's own X (Twitter) account through the Crossbar MCP tools (x_*) or the `crossbar` CLI. Use whenever the user asks to read their timeline, search X, read a thread, check mentions, notifications or DMs, or to post, reply, quote, like, repost, bookmark, follow, mute, block or DM on X.
---

# Crossbar: the user's X account

Crossbar's tools act as the signed-in user on x.com. Reads are free to run. Writes are public and
permanent under the user's name, so treat them like sending an email.

## Start

1. Call `x_whoami`. If it answers `class: "auth"`, call `x_login` (it imports the session from the
   user's browser). If that fails, tell the user to run `crossbar login --window`.
2. No MCP tools? Use the CLI: `crossbar <command> --json` (see `crossbar --help`).

## Reading

- Posts take an id or a URL. Users take `@handle`, a profile URL or a numeric id.
- Lists are paged. Pass `next_cursor` back as `cursor`. Stop when you have enough; don't crawl.
- `x_get_post` returns the post, the thread above it and the replies. Use it before replying.
- `x_search` supports X's operators: `from:`, `to:`, `@`, `"exact phrase"`, `-word`, `lang:en`,
  `min_faves:100`, `min_retweets:`, `filter:links`, `-filter:replies`, `since:2026-01-01`,
  `until:`. Modes: `latest`, `top`, `media`, `people`.
- Summarize what you read. Quote short bits, link the post (`https://x.com/i/status/<id>`).

## Writing

- Post **exactly** the text the user approved. Never invent, "improve" or extend it after approval.
  Draft first, show it, wait for a yes.
- Keep posts within 280 characters unless the user says their account allows longer posts.
- Read a write's `write` field: only `applied` is proven. After `accepted` or `may_have_applied`,
  do **not** send again. Check the profile or post instead. `again: true` is only for a deliberate
  repost of identical text after checking x.com.
- `x_delete_post` and `x_block` are destructive. Confirm each one by name.
- `undo: true` reverses like, repost, bookmark, follow, mute and block.
- DMs go to `@user` or a `conversation_id`. Crossbar can't start a brand-new conversation yet.

## Pace

This is a personal account at human pace. No bulk follows, no mass likes, no reply spam, no
scraping thousands of accounts. If a task needs that, say so and stop.

## Not supported yet

Media uploads, polls, scheduled posts, Spaces, editing or pinning posts, lists, communities,
profile edits.
