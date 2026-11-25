---
name: x-post-review
description: Weekly or monthly review of your own X (Twitter) posts, calibrated against the current open-source For You algorithm. Reads your post-level numbers (impressions, likes, replies, profile visits, follows), finds what worked and what the algorithm is penalizing, and outputs a short action list for the next period. Use when the user asks for a weekly/monthly X review, "how did my posts do", or "what should I change on X".
---

# X post review

## Inputs

1. Post-level numbers for the period. Best: an export from X Analytics (x.com/i/account_analytics, Content tab). If the account can't export, a pasted table or screenshots work. Useful columns: post text or link, date and time, impressions, likes, replies, reposts, bookmarks, profile visits, new follows, and whether the post is a reply, a thread post or an original.
2. The rules in effect: read `RULES.md` in this repo. Before trusting any number, run `python3 scripts/param_history.py --since <start of period>` (or check `CHANGELOG.md`) and note anything that changed during the period.
3. **Fix the measurement window before grouping.** An export may contain only a date, while a post ID encodes an exact creation timestamp. Use exact timestamps in the requested time zone to select posts, and state whether metrics are lifetime totals for those posts or activity occurring during the period. Keep account daily totals separate, state their time-zone limitations, and reconcile only matching windows. Missing metadata or private metrics stay unknown, never zero.
4. Optional: the user's goal for this period (reach, followers, clicks to a site).
5. **If the analytics page is unavailable** (for example X shows a subscription wall), fall back to public counts (views, likes, replies, reposts, bookmarks) and say plainly that profile visits and follows per post are missing for this period; never estimate them. Record the account's follower count, and if possible the follower list, at every review, so the next review can still report net follower change and who followed, even without analytics. Save the following list too: comparing both lists with the previous review gives new followers, lost followers and new mutual follows (accounts in both lists now that were not in both last time). That is the only way to count new mutuals without asking anyone.

## Steps

1. **Split the posts** into: originals, thread posts after the first, replies to other accounts, posts with own video, posts with links. Report count, total impressions and median impressions for each group. Split replies further by the size of the account replied to (for example 20,000 followers and up vs below), and by how fast the reply came (within 60 minutes of the original vs later). Replies to a big account can carry most of an account's impressions while reaching only that account's reply section, so mixing them with small-account replies hides both patterns. A post's ID encodes its time (`(id >> 22) + 1288834974657` ms), so reply delay can be computed from the replied-to post's ID.
   - Public data sources often drop the reply-to field on an account's own thread posts. Treat a post as a later thread post when its conversation ID differs from its own ID and the conversation's first post is the user's; otherwise thread follow-ups get counted as standalone originals and drag the originals' median down.
   - **Check coverage before grouping.** Compare the number of posts you collected with the change in the account's total post count over the same window, and look at the count per group. An empty group the user clearly posted in (for example zero originals in a week with daily threads) usually means the parser dropped rows, not that nothing was posted. One known cause: some public sources return the account's own timeline items without an author field, so a filter on author name silently discards every original. Fix the parser and rerun before writing anything.
   - Confirm thread and reply relationships from metadata. Text beginning with a mention, or an account's size alone, does not prove a mutual relationship. Keep unknown reply targets and replies to other small accounts separate from confirmed mutuals. Report classification coverage.
2. **Funnel per group:** impressions → profile visits → follows. Name the group that actually produces followers, and the one that produces reach without followers.
   - **Check concentration.** If one or two posts produced most of the period's follows (say more than half), say so and treat it as possibly chance, not as proof the format works. Name the post.
   - **Reconcile with account totals.** The sum of per-post follows and profile visits is usually lower than the account-level totals on the Overview tab (some follows aren't tied to a post, and the two views may use different time windows or time zones). Report both numbers and their windows; don't present the per-post sum as the account's follower growth.
3. **Check each rule** against what the user did:
   - Threads: how much of the reach came from post 1 vs later posts.
   - Video: own uploads vs quoted videos.
   - Timing: median impressions by posting hour; flag posts where the first 2 hours fell outside the audience's waking hours.
   - Repetition: repeated openings or closings across posts.
   - Links in main posts.
   - Engagement asks ("repost", "follow for more", "reply X and I'll send").
4. **Top and bottom 3 posts** with one line each on why, tied to a rule when possible. Say clearly when the reason is a guess.
5. **Algorithm changes in the period** that could explain a shift (from step 2 of Inputs).

## Output

A one-page report:
- Numbers table (step 1 and 2)
- 3 things that worked, 3 that didn't, each with the rule behind it
- **Action list for next period: at most 5 items**, each concrete and checkable ("Move every external link to the first reply", "Post originals between 9:00 and 11:00 ET and stay online 2 hours")
- What to measure next time to know if the actions worked

Label every claim as **data** (from the user's numbers), **code** (from RULES.md) or **guess**. Never infer private metrics the user didn't provide.
