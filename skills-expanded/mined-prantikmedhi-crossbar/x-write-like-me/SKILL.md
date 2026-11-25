---
name: x-write-like-me
description: Draft X posts, replies, quotes and threads in the user's own voice by studying their recent posts with Crossbar, then post only what the user approves. Use when the user asks to write, draft or reply on X "like me", in their voice, or to turn notes, a link or a changelog into a post.
---

# Write like the user

## 1. Learn the voice (once per session)

Call `x_whoami`, then `x_user_posts` for the user (about 40 posts, `include_replies: true`).
Note, don't over-fit:
- length (one-liners or paragraphs), line breaks, lists
- case (all lowercase?), punctuation, emoji (which, how often), hashtags (usually none)
- how they open and end, whether they use links in the post or in a reply
- topics they post about and what they never touch

## 2. Draft

- Give 2–3 options of different shapes (one-liner, short take, mini-thread) unless asked for one.
- Under 280 characters each unless the user has longer posts.
- Plain claims over hype. No "🚀 Excited to announce", no "game-changer", no hashtag walls,
  unless that is how the user writes.
- Replies: read the post with `x_get_post` first; answer the post, not the topic.
- Threads: first post must stand alone. Number only if the user does.

## 3. Approve, then post

Show the drafts. Post nothing until the user picks one, and then post **exactly** that text with
`x_post`, `x_reply` or `x_quote`. For a thread, post the first, then reply to your own post with
each next one, in order, using the id the previous call returned.

Report the link. If the `write` field is not `applied`, check the profile before trying again.
