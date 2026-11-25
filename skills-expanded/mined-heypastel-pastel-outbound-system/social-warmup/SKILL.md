---
name: social-warmup
description: Networker — makes the user a familiar name before any DM by drafting comments and reactions on prospects' LinkedIn posts through Pastel, choosing the posts worth it. Use for "which posts should I comment on", warming up leads ranked 50-69, or working the Pastel posts inbox.
---

# Social warmup — Networker

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

An invitation from someone who left a smart comment on your post last week gets accepted. The comment is there to add to _their_ conversation; the pitch waits for the DM.

## Steps

1. **Choose posts:** `pastel_recommend_best_posts` (status `NEW`), or for specific leads `pastel_query_posts` with their name or company. Read each with `pastel_get_details`.
2. **Leave alone:** job announcements, personal or sad news, and posts older than 7 days.
3. **Draft:** `pastel_draft_reply(post_id)`, or `pastel_get_reply_prompt` to write within Pastel's reply guidance yourself. Then `human-voice`.
4. **A comment worth leaving** adds one concrete thing — a number, an example, a respectful counterpoint — or asks the author something they'll enjoy answering. One to three sentences. No product name, no link, no "happy to chat".
5. **After approval:** `comment_on_post` (or `save_reply` to keep it as a Pastel draft), plus `react_to_post` where it fits. Then `mark_post_status` → `REPLIED`, and `PASS` with a `pass_reason` on the skipped ones.
6. **Hand-off:** anyone who replies to or reacts on the comment goes to `campaign-launch` three to five days later, with "we commented on [post], [date]" as their signal.

## Output

```
# Warmup — [date]

### [Author] · [Company] · posted [date]
Post starts: "…"
Why this one: …
Comment:
> …
Action: comment + like | save as draft | pass — reason
```

Close with one `pastel_show_posts` call with the chosen ids.
