---
name: botkits-social-copywriting
description: >-
  Use this when writing or adapting copy for X or LinkedIn so it matches the
  platform instead of sounding like a press release.
---
# Social copywriting

Write posts that read native to X or LinkedIn. Use it once the idea exists; finish with botkits-no-ai-slop.

## Before writing

Settle four things, asking only for what's missing: platform, format (single post, thread, carousel text), the one thing the reader should take away, and the proof you have for it (a number, a screenshot, a link, a story). No proof means the post is an opinion; write it as one.

## Find the angle

Look for the detail a careful reader would stop for and a press release would bury: the mechanism, the constraint, the number that moved, the thing that changes how someone builds. Don't recap the announcement.

## Hook

The first line decides everything. If it's weak, change where the post starts instead of polishing the words. Strong openings name a specific pain, result, image, or mechanism. Weak ones restate the topic, start too wide, or tease ("you won't believe..."). Rotate how you open (a number, a quote, a flat fact, a moment mid-scene) so posts don't share a template.

## X

- Write for a reply, a quote, a send-by-DM, or a follow. In X's current published ranking code (xai-org/x-algorithm, read 14 Nov 2026), the default weights put a reply, a quote, and a DM share at 5 each and a follow at 4, against 0.708 for a like. A reply between two accounts that follow each other gets a further boost. Mutes, "not interested", blocks, and reports carry large negative weights. The weights multiply the predicted chance of each action, not raw counts, so read them as direction, not exchange rates. Write something worth answering, then answer.
- Line 1 names the concrete subject: the product, the number, the file, the result. The ranker routes posts by topic, and readers stop for a named thing, not a mood.
- End on the concrete result or a question you actually want answered. No two-beat slogan closers ("You build. It ships.") and no bait ("Thoughts?", "Agree?"): bait invites the negative signals above.
- Links: X's owner and head of product said in July 2026 that posts with links are no longer penalized, and the published code has no fixed link penalty (opening a link is a small positive signal). Link posts can still draw fewer replies because the reader leaves. Either put the link in a reply or keep it in the post, but make the post stand alone without it, and test on your own account.
- The reply that carries the link holds one concrete line and the link. It does not repeat post 1.
- Single post: one idea. Accounts without Premium get 280 characters, and a link counts as 23. On long posts, the point lands before the "show more" cut.
- Thread: 5-12 posts. Post 1 is the hook and stands alone; it gets most of the reach. Each post earns the next. The last one asks a real question or just stops.
- Video: the code ignores views of clips shorter than its minimum duration (10 seconds by default). Do not promise a ranking boost for video.
- 0-2 hashtags, never mid-thread. Never paste LinkedIn copy onto X.
- Replies on other people's posts: answer in the first sentence, add the one fact they lack, stop. See botkits-no-ai-slop, "Replies and comments".
- Posts about something you shipped: use botkits-ship-post, which starts from the commits and allows no number the commits or the owner can't back.

## LinkedIn

- The hook has to work before "see more" (about 140 characters on mobile).
- LinkedIn ranks partly on dwell time and pushes down posts people skip, so the body has to reward reading. Around 1,200-1,600 characters for a normal post.
- No links in the body. Write "Link in comments."
- No hyphens in the body. Rephrase around them.
- Up to four hashtags, at the very end.
- Include one honest note in the middle: a limit, a weak result, something not yet tested.

## Both

- Real units only: spend, views, files, minutes. Never invent a figure, quote, or date.
- No engagement bait ("like if you agree", "comment YES").
- Vary the post shape from the last one: straight prose, numbered teardown, one-line post, quote and react, changed-my-mind. Read the last few posts' first and last lines before writing; if the new one reuses an opener or closer, change it.
- No trailing period on the last line. No em dashes.
- Deliver the post in a code block, then two lines: the angle you picked and what you left out.

## Critique before rewrite

When fixing an existing post: name its job, its reader, its strongest line, and what must stay. Then rewrite.

## Inspired by

- [Jules Sauvajol, Copywriting-skill (social-copywriting)](https://github.com/judicael-s/Copywriting-skill/blob/8282f17e1f15d0f2b4fa19a90b2005864f77cbe5/skills/social-copywriting/SKILL.md) (MIT). Does well: platform limits, the see-more fold, thread structure, and a critique-before-rewrite habit. Missing: reach figures with no sources (such as links cutting LinkedIn reach by 30-50%), hook templates that are themselves AI tells ("It's not what you think"), and advice to swap conjunctions for dashes.
- [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) (Apache 2.0; weights cited as facts), README and [`home-mixer/params/param.rs`](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs), read 14 Nov 2026. Does well: the current For You ranking code with default weights (reply 5, quote 5, DM share 5, follow 4, like 0.708, open link 0.2, report -234), the 10-second video minimum, and comments warning that weights scale predicted probabilities, not counts. Missing: defaults can change through configuration at any time, and it gives no writing advice.
- Reporting on links in July 2026: [PPC Land](https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/) (Nikita Bier and Elon Musk saying link posts are no longer penalized), [Repli](https://repli.sh/blog/do-links-hurt-reach-on-x/) (searched the published code and found no link multiplier), and [Nieman Lab, April 2026](https://www.niemanlab.org/2026/04/do-links-hurt-news-publishers-on-twitter-our-analysis-suggests-yes/) (publishers who link heavily see lower engagement). Does well: the platform's own statement plus a code check and an outside counterpoint. Missing: no controlled test; correlation only.
- [X heavy ranker README, twitter/the-algorithm-ml](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md). Does well: the real published weights (April 2023): reply 13.5, reply answered by the author 75, like 0.5, "show less" -74, report -369. Missing: a 2023 snapshot, now replaced by the xai-org code above, and no writing advice.
- [LinkedIn Engineering, Understanding feed dwell time](https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time). Does well: shows dwell time is measured once half a post is visible and that predicted skips lower a post's score. Missing: no thresholds in seconds and no posting advice.

## What this version adds

- Ranking advice tied to X's current published code (2026 weights) instead of the 2023 snapshot or folklore numbers.
- A corrected link rule: the post must stand alone, link placement is a choice to test, not a known penalty.
- Closer, video, self-reply, and reply rules, plus a hand-off to botkits-ship-post for build-in-public posts.
- Dani's LinkedIn rules: no hyphens, four hashtags max, one honest note, link in comments.
- Shape and opening rotation so a feed of posts doesn't read like one template.
- Code-block delivery with an angle note, and hooks that pass botkits-no-ai-slop.
