---
name: x-thread-poster
description: Post multi-part X/Twitter threads through Chrome DevTools MCP using the user's logged-in browser session. Use when Codex is asked to open x.com, compose, publish, or automate a thread/multiple posts, especially when a source link must be included or the post style must be adapted from provided content.
---

# X Thread Poster

## Overview

Use Chrome DevTools MCP to compose and publish X threads from the user's active browser profile. Treat posting as a live external action: publish only when the user explicitly asks to post; otherwise stop after drafting or previewing.

## Workflow

1. Load Chrome DevTools MCP tools if they are not already available.
2. Prepare the complete thread text before touching the composer.
3. Open `https://x.com/compose/post` or `https://x.com/home`.
4. Use `wait_for` and `take_snapshot` to confirm the logged-in composer is visible.
5. Enter each post with real browser input events, not DOM-only filling.
6. Add another post for each thread item.
7. Click the final publish button only after all posts are present and under limits.
8. Confirm publication from the timeline or returned status links.

## Preconditions

- Use the user's existing Chrome/X session.
- If X shows login, 2FA, CAPTCHA, account lock, or a security confirmation, stop and ask the user to complete it.
- If the user asks for a draft, schedule, analysis, or review instead of posting, do not publish.
- If the generated thread is not clearly authorized for live posting, show the draft and ask for confirmation before clicking the publish button.

## Thread Preparation

- Keep every post comfortably below X's limit, preferably under 260 characters for non-Premium accounts.
- Put required source links in the first post unless the user specifies otherwise.
- For quoted/source X links, expect X to convert the raw URL into a quote card and sometimes hide the URL text after `原文：`.
- Match the requested voice: slang, idioms, personal style, directness, language, and formality.
- Avoid unverified claims, impersonation, harassment, or medical/legal/financial certainty unless the user provided vetted text.
- Numbering is optional. For a punchier X style, unnumbered short posts often read better.

## Chrome DevTools Pattern

Prefer this interaction pattern:

```text
new_page({ url: "https://x.com/compose/post" })
wait_for({ text: ["有什么新鲜事", "What is happening?!", "发帖", "Post", "登录", "Sign in"] })
take_snapshot()
click(textbox uid)
type_text(first post)
take_snapshot()
click("添加帖子" or "Add post")
type_text(next post)
repeat
click("全部发帖" or "Post all")
wait_for(success/timeline text)
take_snapshot()
```

Use localized labels from the snapshot. Common Chinese labels include:

- `帖子文本`: composer textbox
- `发帖`: single-post publish button
- `全部发帖`: thread publish button
- `添加帖子`: add another post
- `添加另一个帖子`: placeholder for the next post
- `关闭`: close composer
- `草稿`: drafts

## Input Reliability

X's composer uses Draft.js/contenteditable behavior. `fill()` can make text appear in the box while React does not enable the publish button.

Use `click()` plus `type_text()` for text entry. Use `take_snapshot()` after each post to verify both the text and the button state. If a post was inserted with `fill()` and the publish button stays disabled, discard that composer by closing it, reopen a fresh composer, and re-enter with `type_text()`.

If typing long non-ASCII text fails or drops characters, split `type_text()` calls into shorter chunks at paragraph boundaries.

## Publication Confirmation

After publishing:

- Wait for navigation back to home/timeline or a success indicator.
- Take a fresh snapshot.
- Extract the first status link from the newly posted thread, usually from the timestamp link in the first new article.
- Report the public thread URL to the user.

## Failure Handling

- If the page is not logged in, ask the user to log in.
- If publish fails with a policy/rate/length warning, read the visible error and revise only the affected post.
- If the add-post control is missing, verify the current composer is focused and the current post has valid text.
- If the final button is disabled, check for over-limit text, empty posts, or the Draft.js `fill()` issue.
- Never retry publishing blindly if the UI state is unclear; refresh the snapshot and confirm whether the thread already posted.
