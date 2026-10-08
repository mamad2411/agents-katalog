---
name: x-algorithm
description: Write X (Twitter) posts that the For You algorithm actually rewards. Grounded in the open-sourced X recommendation system — the Grok-based transformer ranker, Phoenix retrieval, Thunder in-network store, and Grox content-understanding pipeline. Use when the user wants to write a post, thread, reply, or quote; plan a content strategy; review or rewrite an existing draft; debug why a post flopped; or understand how the For You ranking works. Triggers include "write a tweet", "X post", "twitter post", "thread", "viral tweet", "improve this post", "why didn't this perform", "what to post", "x algorithm", "for you feed", "twitter algorithm".
license: Apache-2.0
---

# X Algorithm: Writing Posts That Get Ranked

A single source of truth for writing on X, derived directly from the open-sourced For You algorithm. No folklore, no growth-hack myths — only what the actual ranker, retrieval system, and content classifiers reward or punish.

## How the Feed Actually Works

Every For You impression is the output of this pipeline:

```
Sources                Filters               Scoring                 Selection
─────────              ───────               ───────                 ─────────
Thunder (in-network)   age, vf, muted        Phoenix transformer     top-K by score
Phoenix (OON ANN)      blocks, dedupe        → P(19 actions)         author diversity
ads / wtf / prompts    seen/served           weighted sum            ads blender
                       subscription gate     OON multiplier
```

Two ways into a user's feed:

1. **Thunder (in-network)** — they follow you. Sub-millisecond lookup. Always preferred.
2. **Phoenix retrieval (out-of-network)** — a two-tower model embeds your post and the user's engagement history into the same space, then ANN-searches. You land here when your content lives in the topical neighborhood of posts the user recently engaged with.

Then **Phoenix ranking** (a Grok-based transformer) predicts probabilities for ~19 engagement actions per candidate, the **Weighted Scorer** combines them, **Author Diversity** decays repeated authors, **OON Scorer** down-weights out-of-network, and the top-K wins.

There are no hand-engineered relevance features anymore. The transformer learns from the user's `UserActionSequence` (their recent aggregated actions). That is the entire feature set.

## The 19 Actions That Define Your Score

The ranker predicts a probability for each. Final score = Σ(weight × P(action)).

### Positive signals (you want these)

| Action | What it is | Why it matters |
|---|---|---|
| `favorite` | like | Baseline engagement. |
| `reply` | someone replies | Strong — replies have their own weight. |
| `retweet` | repost | Strong distribution signal. |
| `quote` | quote post | Amplification + a separate `quoted_click` and `quoted_vqv` reward chain. |
| `photo_expand` | tap to expand image | Image must be intriguing at thumbnail size. |
| `click` | tap a link/post | Headline/curiosity gap matters. |
| `profile_click` | tap your name/avatar | Your identity made them curious. |
| `vqv` | "video quality view" | **Only counted if `video_duration_ms > MIN_VIDEO_DURATION_MS`**. No 2-second loops. |
| `share` | native share menu | |
| `share_via_dm` | shared in DM | Independent signal — "I want my friend to see this". |
| `share_via_copy_link` | copied link | Save-worthy content. |
| `dwell` | dwelled at all | Binary. The hook has to land. |
| `cont_dwell_time` | continuous dwell duration | Longer linger = more weight. |
| `cont_click_dwell_time` | dwell after clicking into post | Reward for delivering on the click. |
| `follow_author` | viewer follows you | One of the strongest positive signals. |

### Negative signals (these subtract from your score)

| Action | Effect |
|---|---|
| `not_interested` | Manual "not interested" tap. |
| `block_author` | Block. |
| `mute_author` | Mute. |
| `report` | Report. |
| `not_dwelled` | **Scroll-past with no dwell.** Heavy penalty. Most posts die here. |

The negative weights are real and subtractive — a post that gets scrolled past by many users actively pushes its own score down. "No engagement" is not neutral; **`not_dwelled` is negative**.

## What This Means For How You Write

### 1. Optimize for diverse engagement, not just likes
The model weights 19 actions. A post that earns one reply and one share and one quote outperforms a post with three likes. Write things people want to **reply to, quote, save, or DM**.

### 2. The hook has to stop the scroll
Every scroll-past is a `not_dwelled` negative. The first visible line (and the thumbnail of any media) is the entire battle. If the user doesn't dwell, you don't just get zero — you go negative.

### 3. Longer is fine if it earns the dwell
`cont_dwell_time` is a continuous weight. A post people read for 12 seconds beats one read for 2. But that only works if the hook earns the read — pad-for-length kills you on `not_dwelled`.

### 4. Make it quotable, not just likeable
Quotes trigger `quote_score` + downstream `quoted_click_score` + `quoted_vqv_score`. A take that begs for "this, but also…" outperforms a self-contained one.

### 5. Convert viewers to followers
`follow_author` is heavily weighted. Every post should make the case for following you — clear identity, distinct voice, on-niche signal. Profile + pinned post matter because `profile_click` also scores.

### 6. Avoid anything that risks `block` / `mute` / `report` / `not_interested`
Rage-bait, slop, misleading hooks, engagement farming — these maximize short-term `click` but blow up `not_interested`/`mute`, which are weighted negatively. Net is often negative.

### 7. Video must be substantive
`vqv` only counts when video duration exceeds the minimum threshold. Sub-threshold loops literally cannot earn the video reward. There's also a `quoted_vqv` reward when your video is quoted — make videos that beg to be quoted.

### 8. Images: thumbnail-test everything
`photo_expand` is its own positive signal. The thumbnail has to make someone tap. Crops, faces, contrast, clear focal point.

### 9. Make content shareable, not just consumable
`share`, `share_via_dm`, `share_via_copy_link` are three independent rewards. Frameworks, lists, screenshots of useful info, before/after, "saved this for later" content — these all score.

## What Will Quietly Kill Your Post

These run **before scoring** — if any fires for a viewer, your post is dropped from their candidate set entirely.

| Filter | Triggers when | Implication |
|---|---|---|
| `AgeFilter` | Post older than threshold | Timeliness matters. Posts decay out of consideration. |
| `MutedKeywordFilter` | Your text contains a user's muted keyword | Common words (e.g. "crypto", "AI", politics terms) lock you out of muted audiences. |
| `AuthorSocialgraphFilter` | Viewer blocked/muted you | Permanent for that viewer. |
| `VFFilter` (visibility) | Safety classifier marks `Drop` | Spam, violence, gore, PTOS violations → invisible everywhere. |
| `IneligibleSubscriptionFilter` | Paywalled post, viewer not subscribed | Locks paid content to subscribers only. |
| `PreviouslySeenPostsFilter` | Viewer already saw it | One impression per viewer. |
| `PreviouslyServedPostsFilter` | Already served this session | Same. |
| `RepostDeduplicationFilter` | Multiple reposts of same content | Mass-repost manipulation collapses. |
| `DedupConversationFilter` | Multiple branches of one thread | Only one branch shown. |
| `SelfpostFilter` | You're the viewer | Never see your own. |

**Practical implications:**

- A "controversial topic hook" is also a "muted keyword" landmine. Calibrate.
- One conversation, one branch — replying 10 times to your own thread doesn't multiply reach.
- Mass-rebloging your own old content gets collapsed.

## Content Understanding (Grox)

Beyond the ranker, a separate `grox/` pipeline runs **VLM-based classifiers** on posts:

- **Banger initial screen** — a vision-language model scores `quality_score` (0–1), threshold **0.4 for positive**. Also emits `slop_score` and `has_minor_score`, plus taxonomy categories.
- **Post safety screen deluxe** — VLM safety pass for PTOS policy.
- **Spam detection** — aggressive on accounts <1K followers replying. If you reply-spam from a small account, the spam classifier flags you and the in_reply_user_follower_count bucket determines logging.
- **PTOS policy / safety_ptos_category** — policy enforcement.
- **Multimodal post embedder (v2 / v5)** — multimodal embeddings used downstream.

So a post is also being judged on **visual + textual quality** by an LLM. AI-generated slop is detected and scored against you. Posts with minors flagged. Topical categorization happens automatically — you don't pick the category, the classifier does.

## Distribution Mechanics

### In-network vs Out-of-network

Out-of-network candidates are multiplied by `OON_WEIGHT_FACTOR` (< 1.0) in `OONScorer` / `RankingScorer`. **In-network always wins on equal scores.** The single highest-leverage growth move on X remains: **be followed by people in the audience you want to reach.**

Two exceptions where OON penalty softens:

1. **Topic match** — if the viewer follows topics that match the post, `TopicOonWeightFactor` replaces the regular OON factor (typically higher → easier OON reach).
2. **New users** — eligible new users (account younger than a threshold AND following at least `NEW_USER_MIN_FOLLOWING`) get `NEW_USER_OON_WEIGHT_FACTOR` instead.

**Implication**: Topical, categorizable posts travel further OON than generic ones. The Phoenix two-tower retrieval needs a coherent neighborhood to embed your post into.

### Mutual follow Jaccard (MinHash)

`MutualFollowJaccardHydrator` computes the Jaccard similarity between the viewer's follow graph and the author's follow graph via MinHash (≥256 hashes). Authors whose graph overlaps the viewer's get a stronger signal. **Tribe matters.** Posts from authors followed by accounts the viewer also follows have a structural advantage.

### Author diversity decay

`AuthorDiversityScorer` ranks by score, then for each subsequent post by the same author, multiplies score by `decay_factor^position + floor`. Burst-posting collapses your own scores within one feed render. **Space posts out.** Five posts in five minutes is worse than five posts over a day.

### Engagement caching window

`EngagementCountsHydrator` caches like/reply/repost/quote counts:
- New tweets (<30 min old): 5-min TTL
- Older: 10-min TTL

The first ~30 minutes set the trajectory the rest of the system rides on. Early engagement compounds. Post when your audience is online.

## A Pre-Post Checklist

Before you publish, gate against this list:

1. **Hook in the first visible line** — would a stranger stop scrolling? If not, rewrite. (`not_dwelled` is negative.)
2. **One specific, on-niche idea** — needed for Phoenix retrieval to embed you in a useful neighborhood.
3. **Replyable / quotable** — does it have a hook for a take or a "yes, but" — or is it self-contained and dead-end?
4. **Shareable** — would someone DM this or copy the link?
5. **Image / video tested at thumbnail size** — crop, focal point, contrast. Videos longer than the min-duration threshold.
6. **No muted-keyword landmines** for the audience you're targeting.
7. **No slop / clickbait that risks `not_interested`, `mute`, `report`**.
8. **Identity intact** — would `profile_click` reward a clear "follow this account because…" payoff?
9. **Timing** — is your audience awake? First 30 min decides the rest.
10. **Spacing** — not stacked on top of your own recent posts.

## Replies, Quotes, Threads

- **Replies from <1K-follower accounts** are aggressively spam-screened. Quality over quantity. One thoughtful reply > ten "great post 🔥".
- **A separate reply-ranking model** decides reply order on conversations. Same content rules apply at higher selectivity.
- **Quote posts** are doubly valuable to *you*: they trigger the quote-side rewards (`quote`, `quoted_click`, `quoted_vqv`) for the quoted author. Quote good posts in your niche — it's a positive signal for them AND puts you in front of their audience.
- **Threads**: only one branch of a conversation is shown per viewer (`DedupConversationFilter`). Posting a 10-reply self-thread doesn't multiply impressions of the same conversation. Lead post must stand alone.

## When the User Asks "Why Did This Flop?"

Walk through, in order:

1. **Filter dropouts** — too old? muted keyword? safety flag? subscription-gated?
2. **Hook / dwell** — would a stranger stop on the first line? If not, every scroll-past pushed score down.
3. **OON viability** — was it topical and embedable, or generic and floating?
4. **Author diversity** — did you post 4 other times in the same window?
5. **Negative signals** — did the framing invite mutes / not-interested?
6. **Visual quality** — would the banger initial screen score this >0.4? Any AI-slop tells?
7. **In-network base** — do you have followers in the audience that should care? OON is hard. The followers route is the moat.
8. **Timing** — first 30 min set the curve. Was anyone online?

## Anti-Patterns The Algorithm Punishes

- Engagement-bait questions ("agree?", "RT if you agree") — they trigger `not_interested` from sophisticated users; net negative.
- Reply-guy spam from small accounts — flagged by spam classifier.
- Posting the same idea 5x in a day — author diversity decay + repost dedup.
- 2-second meme loops as primary video format — sub-threshold for `vqv`.
- Threaded mega-posts where the first tweet is just "🧵" — viewer never dwells past it.
- AI-generated slop with no edit — banger screen's `slop_score` flags it.
- Hostile / dunking content — short-term `click`, long-term `mute`/`block`/`report`.

## What's NOT In The Algorithm (Despite Folklore)

- **No link penalty as a hard rule.** Links are scored via `click_score` and `cont_click_dwell_time` — if people click *and* dwell, you're rewarded.
- **No follower-count multiplier.** The transformer doesn't see your follower count as a feature. Reach is driven by predicted engagement, mutual-follow Jaccard, in-network membership, and topic match.
- **No "post X times per day" rule.** Author diversity decays within a single feed render, not across days.
- **No "best time to post" hardcoded.** The 30-min engagement-cache window is real, but "when" depends entirely on when *your specific audience* is online.

## How To Use This Skill

When the user asks you to write or improve a post:

1. Ask (or infer) the **goal**: reach, replies, follows, shares, clicks.
2. Ask (or infer) the **audience**: who follows them, what topic neighborhood?
3. Draft against the **pre-post checklist**, optimizing for the goal's primary action.
4. Call out **specific algorithmic risks** in the draft (muted keywords, hook strength, length-for-dwell trade-off, OON viability).
5. If reviewing existing copy, run the **"why did this flop"** sequence.
6. Never recommend tactics that look like engagement farming — net-negative on `not_interested` / `mute`.

Be direct. Cite the mechanism (e.g., "`not_dwelled` is weighted negative — your first line has to stop the scroll") so the user learns the *why*, not just the *what*.
