---
name: operations
description: Safely use Rednote tools to log in, search and read notes, inspect profiles, engage with posts, and publish image or video content. Use when the user asks to work with Rednote, RED, rednote.com, Xiaohongshu, or 小紅書.
---

# Operations

## Overview

The `rednote` MCP tools and their results are the source of truth.

## Login

1. Call `check_login_status`.
2. If logged out, call `get_login_qrcode`, show the image, wait for scan, then check again.
3. Continue only after success. If auth/risk control fails, retry this login flow once. Refresh expired QR codes and stop if it still fails.

## Read

- Use `list_feeds` and `search_feeds` with only the requested filters.
- Use `get_feed_detail` with `feed_id` and `xsec_token` from read results.
- Use `user_profile` with `user_id` and `xsec_token` from read results.
- Never invent IDs or tokens; refresh missing values through read tools.

## Mutations

Before `post_comment_to_feed`, `reply_comment_in_feed`, `like_feed`, `favorite_feed`, `publish_content`, `publish_with_video`, or `delete_cookies`:

1. Preview the exact change.
2. Get explicit confirmation.
3. Call the tool once.
4. Report the actual result; never claim success on error.

For publishing, preview title, body, tags, media paths, visibility, schedule, original declaration, and products. Put hashtags in `tags`, not content, and obey the tool title limit.

## Recovery

- If login or auth/risk control fails, retry the login flow once.
- If a read tool is missing IDs or tokens, refresh them from read results.
- If a mutation fails, surface the tool error and never silently retry it.
