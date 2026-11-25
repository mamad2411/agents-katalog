---
name: publish-posts
description: Publish or schedule social media posts through WoopSocial to Facebook, Instagram, Threads, LinkedIn, Bluesky, X/Twitter, Pinterest, TikTok and YouTube. Use when the user asks to post, publish, schedule, cross-post or queue content to their social accounts, or asks whether a post went out.
---

# Publish posts with WoopSocial

The WoopSocial connector must be connected. If its tools are missing, ask the user to connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`).

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## Posting workflow

1. Use `projects_list` to identify the project.
2. Use `social_accounts_list` to resolve the requested accounts. Only accounts with `status: CONNECTED` can publish, and all accounts in one post must belong to the same project. If a requested platform isn't connected, say so plainly; never skip it silently.
3. Use `social_accounts_get_platform_inputs` when a platform needs account-specific options, such as a Pinterest board or a TikTok privacy setting.
4. Reuse media returned by `media_list` when it fits. For new media, use the `media_uploads_*` session tools: upload every returned part exactly as instructed, complete the session, and wait until the media is ready.
5. Build the post from the user's content, accounts, platform-specific fields and schedule.
6. When the user wants to review the post first, or you are unsure the content fits a platform's rules, call `posts_validate` with the same request and fix every error it reports.
7. Call `posts_create` only after the target accounts, content and schedule are unambiguous.
8. Return the post ID and the requested schedule. For delivery results, use `posts_get` or `social_account_posts_list`, and distinguish pending, scheduled, published and failed states.

## Uploading media from chat

Uploads go to presigned URLs on `r2.cloudflarestorage.com`. If uploading a part is blocked, tell the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains) and try again.

## Action boundaries

Treat an explicit request to publish or schedule as authorization for that action. Ask before creating the post only when its target accounts, content, schedule, or publish-versus-draft intent is ambiguous.

Require explicit user intent before calling a delete tool for posts, account posts, projects, social accounts, media or webhooks.

Never claim that a post was published merely because creation succeeded. Report the delivery state WoopSocial returns.
