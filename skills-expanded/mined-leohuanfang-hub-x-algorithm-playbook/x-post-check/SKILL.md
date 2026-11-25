---
name: x-post-check
description: Check a draft X (Twitter) post against how X's open-source For You algorithm ranks posts (github.com/xai-org/x-algorithm, October 2026), then suggest a rewrite. Use when the user asks to check, review, audit or improve an X post, tweet or thread before posting, or asks "will this do well on X".
---

# X post check

Checks a draft against seven rules that come straight from X's open-source ranking code, then rewrites it.

## What you need from the user

1. The draft (one post, or a whole thread).
2. Optional: their last 3 posts, to catch repeated openings and closings.
3. Optional: whether it will carry an image, a video (and its length), or a link.
4. Optional: their audience's main time zone.

Ask only for the draft if the rest isn't given. Don't block on the optional items.

## The seven checks

Answer each with PASS, FAIL or N/A and one sentence of reasoning.

1. **Best idea in the first post.** In a thread, every post after the first is a reply to yourself. For You drops replies from accounts the viewer doesn't follow, and the stranger retrieval index skips self-replies. So only post 1 competes for strangers' feeds. FAIL if the strongest example, number or claim sits in post 2 or later.
2. **Own video, over 10 seconds.** A post only enters the video index if the post itself carries the video. Quoting someone else's video doesn't count; re-uploading it trips duplicate detection. FAIL if the video is a quote or under 10 seconds.
3. **Worth sending to someone.** Copy-link share is weighted 20 (it was 0 from November 13 to 18, 2026, so treat it as unstable), sharing by DM 5 and a reply 5, a like 0.708. PASS if the post contains something reusable a reader would forward or answer: a number, a tool, a checklist, a method, a prompt.
4. **A real question, no asks.** Replies are weighted 5 (20 between mutual follows). FAIL if it asks for likes, follows, reposts or "reply and I'll send you X": X removes accounts from creator payouts after 3 engagement asks.
5. **Links in a reply.** No hard-coded link penalty, but link posts collect fewer likes and replies. FAIL if an external link is in the main post.
6. **No template.** "Not interested" is weighted -53. FAIL if the opening or closing repeats a line from the user's recent posts.
7. **Sounds like a person.** Small accounts flagged as low-quality AI content get a 7-day label that removes them from strangers' feeds. FAIL on generic hype words ("insane", "game-changer", "mind-blowing") or obvious template structure.

## Output

1. A short table: check, result, reason.
2. A rewritten version that passes every applicable check, under 280 characters per post, keeping the user's voice and facts. Never invent numbers.
3. One line on timing: post when the likeliest likers are awake and stay online for the first 2 hours, because X's small-account boost only considers original posts under 2 hours old with fewer than 200 home-timeline views, picked by early like rate.

## Sources

All rules come from github.com/xai-org/x-algorithm at commit 862a123 (October 17, 2026): `home-mixer/params/param.rs` (weights, cold-start thresholds), `home-mixer/filters/oon_retweet_reply_filter.rs`, `home-mixer/filters/dedup_conversation_filter.rs`, `home-mixer/scorers/author_cold_start.rs`, `phoenix-rankall-strato/` (retrieval index), `abuse-enforcement-service/service-lib/rules/enforcement_user.yaml`, plus Nikita Bier's posts on duplicate content and engagement asks (July 2026). Weights multiply the model's predicted probability of each action for that viewer, not raw counts. X updates the repo almost every weekday; re-check `param.rs` before trusting any number here.
