---
name: rea-brand
description: Use when the user wants to reverse engineer a person's personal brand or creator growth - how a creator, founder or influencer grew their audience, when they took off, who boosted them, how their posts are made and what wins, how they turn followers into money, and what to copy. Covers every platform the person uses (X, LinkedIn, Instagram, YouTube, TikTok, Threads, Substack and more). Also for "how did @handle grow", "teardown of <person>'s personal brand", "what makes <creator>'s posts work", "reverse engineer <person>".
---

# REA brand

One person in, a playbook out: which accounts they have, when each one took off, who boosted
them, how their posts are made and what wins, how the audience turns into money, and ten plays
the user can copy, each with a ready prompt.

Runs on every platform the person is on that treg has data for. X, LinkedIn, Instagram and
YouTube are the **core four**, with named endpoints and tuned checklists. Any other platform
(TikTok, Threads, Substack, Facebook, Reddit, Bluesky, Medium, Pinterest…) runs through the same
steps with endpoints found at run time. A platform where the person has no confirmed account gets
no calls and costs nothing.

Runs on treg. If `treg --version` fails, read https://treg.to/llms.txt, follow it to install and
sign in, then come back here. A measured 6-platform run cost about 8¢ (118 calls).

## Modes

| Mode | When | Steps | Delivers |
|---|---|---|---|
| **full** (default) | "how did PERSON grow", "teardown", "what to copy" | 0-9 | `brand.md` + `brand.html` + CSVs |
| **content** | hooks, titles, thumbnails, formats, "what content works", and nothing about growth | 0, 1, 2, 5, 10 | `content.md` + `content.html` + CSVs |

## Rules

- **Public creators only.** PERSON must publish for an audience: at least one confirmed account
  with 1,000+ followers, or a public figure (founder, author, journalist, athlete, politician).
  Anyone else → stop and say this skill is not for private individuals.
- **The public brand only.** Study what PERSON publishes, how it spreads and how it earns. Pull no
  follower lists, no contact details (email, phone), nothing about home, family or private life,
  and leave out location fields even when a profile returns one. Log in nowhere, use no cookies,
  create no accounts, comment on nothing, contact no one.
- **Name only public accounts.** In the report, name PERSON and accounts with 10K+ followers. Count
  everyone else (commenters, small accounts) instead of naming them.
- **Skip what doesn't exist.** Only the accounts confirmed in step 1 get calls. No account, a
  private account, under 10 posts, or no data source in treg → that platform is "skipped" with the
  reason. Never search a platform "just in case".
- **Other platforms.** For a platform outside the core four: `treg catalog search "<platform> user
  profile"` and `"<platform> user posts"`. Prefer a routed `treg.<platform>.<job>` tool when one
  exists; otherwise pick by inputs that match what you hold, then reliability, then price. Known
  good picks:
  - Substack: `crawl4ai.substack.publication.posts` {"publication":"DOMAIN","limit":50} returns
    likes, comments, word count and paywall status for a fraction of a cent. The free RSS feed
    (`https://DOMAIN/feed`) has no engagement, so use it only as a fallback.
  - Threads: `scrapecreators.x.v1-threads-user-posts` --query handle=h returns about the 15 latest
    posts with no paging, so expect "too few posts to call a pattern".
  - Medium or a podcast: the RSS feed, read with plain `curl`.
- **SEEN or INFERRED.** SEEN = a call result or an image shows it; link it. INFERRED = reasoned from
  what was seen; say from what. Nothing seen → "not seen", never guessed. A number PERSON states
  about themselves is "SEEN (self-reported)"; a number someone else states is a claim.
- **Money.** Before an endpoint's first call: `treg catalog get <id>`, quote its price, check it fits
  the cap. `treg call` prints each charge on stderr (`treg: charged …`); keep a running ledger from
  it and stop before the cap is passed.
- **How to call.** `anyapi.*` endpoints take a JSON body (`treg call <id> --data '{…}'`).
  `harvestapi.*` and `scrapecreators.*` take query params (`--query key=value`). `catalog get` shows
  the ready call line.
- Free first: `treg.web.search` and `treg.web.extract` with header
  `X-Treg-Route-Prefer: tinyfish` (and `X-Treg-Route-Max-Cost` set low). Blocked page → the route
  tries the next vendor; still blocked → list it as blocked and move on.
- An endpoint fails → `treg catalog search` the same job, try one alternative (named below where
  known) → else "unavailable".
- Python does all math; every number shown comes from code output. Date every count. pandas,
  scikit-learn, Pillow and markdown do the work; install them in a virtualenv if they are missing.
- Compare engagement only within a platform, never across platforms.
- **Checkpoints.** After each step print a ◆ line: a 3-line finding, what the next step checks and
  its est. cost, then keep going. Stop and ask only at step 1's table, when spend runs 50% over the
  step's estimate, or when the next call would pass the cap.

## 0 · Setup

INPUT: mode | PERSON (a name, any handle, or a profile URL) | platforms (default: every confirmed
account with a data source) | the user's own handles, niche and stage (starting out <1k / growing
1k-50k / established 50k+) | budget cap (default 1 USD) | language of PERSON's posts (default en).
The user's handles and niche are optional: without them, assume "starting out" and leave blanks
like [YOUR NICHE] in the prompts. Ask for PERSON if missing; ask for the rest only once, in the
same message.

Work in `rea-brand/<person-slug>/`: `raw/` for call results, one folder per platform, and a
`ledger.txt` with one line per call.

## 1 · Find the accounts — ~½¢, then stop for a check

Everything after this step runs only on the table this step produces.

1. Profile what the user gave:

   | Platform | Profile call | Fallback |
   |---|---|---|
   | X | `anyapi.x.user.profile` {"handle":"h"} (note `pinnedPostIds` and `createdUtc`) | — |
   | LinkedIn | `anyapi.linkedin.user.profile` {"url":"https://www.linkedin.com/in/ID"} | `harvestapi.linkedin.user.profile.main` |
   | Instagram | `anyapi.instagram.profile` {"handle":"h"} | `scrapecreators.instagram.user.profile` |
   | YouTube | `anyapi.youtube.channel` {"handle":"@h"} | `scrapecreators.youtube.channel.profile` |
   | Any other | found with `treg catalog search "<platform> user profile"` (see Rules) | the next result |

   Only a name? `treg.web.search` {"q":"\"NAME\" X LinkedIn Instagram YouTube"} → profile the
   best match. Two people share the name → ask the user which one.
2. Find the other accounts, free first: the bio, bio links and website from each profile; read the
   website and any link-in-bio page (Linktree, Beacons, Stan, bio.link, a custom page) with
   `treg.web.extract`; the YouTube channel description and links. Collect **every** social or
   publishing link found there (TikTok, Threads, Substack, Facebook, Reddit, Bluesky, Medium,
   Pinterest, a podcast…), not just the core four. Still missing one of the core four → one
   `treg.web.search` {"q":"\"NAME\" site:linkedin.com/in"} (or site:instagram.com,
   site:youtube.com, site:x.com), then profile the hit. Other platforms count only when PERSON's
   own pages link to them.
3. For each platform outside the core four, find its data source (see Rules) and profile it. No
   profile or posts endpoint in the catalog → status "skipped: no data source".
4. Confirm. A handle counts only if PERSON's site or another confirmed account links to it, or its
   own bio links back to one of them. The same name alone is not proof; namesakes are common.
5. Show this table and **stop**:

   platform | handle | confirmed by | followers | posts | data source (endpoint ids) | status (run /
   skipped: none found / private / under 10 posts / no data source) | est. cost of steps 2-7

   Ask: right person? any account missed? any platform to drop? Continue only after the answer.

## 2 · Pull the posts — ~½¢ per platform

Per confirmed platform: the latest 100 posts or the past 12 months, whichever comes first, page by
page. Stop early if the cap would be passed.

| Platform | Call (and how to page) | Keep |
|---|---|---|
| X | `anyapi.x.user.posts.timeline` {"handle":"h"}, next page with `cursor` = previous `nextCursor`. Then 2 pages of `anyapi.x.user.posts` {"handle":"h","limit":50} for replies (`isReply`; the reply target is the first @handle in the text). | text, date, views, likes, reposts, quotes, replies, bookmarks, media, pinned |
| LinkedIn | `harvestapi.linkedin.user.posts` --query profilePublicIdentifier=ID --query scrapePostedLimit=year --query page=1, then page 2, 3…, passing `paginationToken` when returned (an empty page ends it). Drop rows where `header.text` shows PERSON reposting someone else. Fallback: `anyapi.linkedin.profile_posts_full` (about 5x the price). | text, date, reactions, comments, shares, format (text, image, document, video, poll, article) |
| Instagram | `anyapi.instagram.user.posts` {"handle":"h"}, next page with `cursor`. Then 2 pages of `anyapi.instagram.user.reels` {"handle":"h"} for plays and length. | caption, date, kind (reel; carousel = 2+ media; photo), likes, comments, plays, media URLs |
| YouTube | `anyapi.youtube.channel_videos` {"handle":"@h","sort":"latest"}, next page with `cursor`; one page with "sort":"popular"; 2 pages of `anyapi.youtube.channel_shorts` {"handle":"@h"}. | title, views, date, Short vs long; thumbnail = `https://i.ytimg.com/vi/ID/hqdefault.jpg` (free) |
| Any other | The posts endpoint chosen in step 1, paged as its `catalog get` says. | the same columns, whatever the platform reports |

Platform quirks, all seen in real runs:
- **X.** Drop retweets (text starts with `RT @`). A post whose whole text is one `https://t.co/…`
  link is an **X Article**: set its format to `article` (step 5 reads its title). The timeline can
  skip the pinned post, so fetch each of the profile's `pinnedPostIds` with `anyapi.twitter.tweet`
  {"url":"https://x.com/HANDLE/status/ID"}; a pinned post is often PERSON's biggest hit.
- **Instagram.** The first rows can be pinned posts from years ago. Flag posts older than the
  window as `pinned_old`, leave them out of step 5's ranking, and report them as past hits (their
  dates help step 3).
- **YouTube.** `publishedTime` is relative ("3 months ago"): store an approximate date and mark it
  approximate. `lengthText` may not parse; exact dates and lengths for the top videos come from
  step 5.

Save one CSV per platform, `<platform>/posts.csv`, with the same columns: platform, id, url, date,
date_is_approx, format, text, views, likes, comments, shares, saves, duration_s, is_reply,
media_url, pulled_at.

## 3 · When they grew — ~½¢

No source sells follower history for a person, so build each platform's curve from dated signals.

- **Milestones (SEEN, self-reported).** Regex the step 2 text for PERSON's own counts ("10k
  followers", "100,000 subscribers", "hit 50K"). On X, also `anyapi.x.search.posts`
  {"query":"from:HANDLE (followers OR subscribers)","queryType":"Top"}, 1-2 pages. Each match that
  states PERSON's own count is a dated point. Posts that list several numbers ("Year 1: 10K, Year
  2: 50K…") are the richest; read them in full.
- **Snapshots (YouTube only).** The Wayback Machine is free (plain `curl` is fine):
  `https://web.archive.org/cdx/search/cdx?url=youtube.com/@HANDLE&output=json&fl=timestamp,original&collapse=timestamp:6`
  lists one snapshot a month. Read at most 4, spread across the years, 10 seconds apart, and stop
  at the second HTTP 429. The subscriber count is in `subscriberCountText`. Skip X, Instagram and
  LinkedIn snapshots: they need JavaScript or a login and come back empty.
- **Engagement trend (INFERRED).** Python: median engagement per month per platform from step 2.
  The largest step up that holds for 2+ months is the likely inflection.
- **The early era.** What PERSON posted while still small. Go back to the year PERSON had under
  10K followers (from the milestones), else to the account's start, at most 6 years:
  - X: `anyapi.x.search.posts` {"query":"from:HANDLE since:YYYY-01-01 until:YYYY-12-31","queryType":"Top"},
    one page per year. Say these are "Top" samples, which favor hits.
  - YouTube: page `channel_videos` to the oldest video only if the channel has under 300 videos;
    otherwise use the "popular" page and say the early era was not pulled.
  - LinkedIn and Instagram: what step 2 reached, plus old pinned posts; say how far back that is.
- Output, per platform: date | signal | value | SEEN/INFERRED | link. Mark the inflection(s) and
  the first post seen.

## 4 · Who boosted them — ~2¢

Bigger accounts sharing PERSON, PERSON appearing on bigger stages, and PERSON working the replies.
Date every row against step 3's inflection. Run only the parts for confirmed platforms.

- **X mentions.** `anyapi.x.search.posts` {"query":"@HANDLE min_faves:500 -from:HANDLE","queryType":"Top"}
  and {"query":"\"NAME\" min_faves:500 -from:HANDLE","queryType":"Top"}, 1-2 pages each. Profile
  the top 15 authors with `anyapi.x.user.profile` for follower counts. Label each: quote, mention,
  recommendation, summary thread about PERSON, translation, clip, criticism. Many posts in other
  languages about one piece means it went international; say so.
- **X replies.** From step 2's replies: the share of PERSON's posts that are replies, replies per
  day, the 15 accounts they reply to most → profile the top 10. Replying mostly to much bigger
  accounts is a reply strategy (INFERRED).
- **Podcasts and guest spots.** `anyapi.youtube.search` {"query":"NAME interview"} and
  `treg.web.search` {"q":"\"NAME\" podcast interview"}. Keep only appearances where PERSON's name
  is in the title or channel and the channel is not PERSON's own: host, date, views, link.
- **LinkedIn.** On PERSON's 3 top posts: `harvestapi.linkedin.post.comments` --query post=URL.
  Count commenters with large followings, and people who appear on 2+ of the 3 posts. A repeat
  group may be an engagement circle (INFERRED, and say plainly it is a guess). Name no one under
  10K followers.
- **Instagram.** `anyapi.instagram.tagged_posts` {"handle":"h"}, 1 page → who features PERSON;
  collabs and tags in step 2 captions.
- **YouTube collabs.** Titles or descriptions that name other creators ("with", "ft.", "x").
- **Other platforms.** No separate boost search: note collabs, features and guest posts seen in
  their step 2 rows.
- Output: date | platform | who (followers) | what | reach | link | before or after the inflection.

## 5 · How the posts are made — ~2¢ + image reads (free)

Per confirmed platform: rank, look, read, topics, voice, write up.

**Rank.** Engagement: views on X and YouTube; reactions + comments on LinkedIn; likes + comments on
Instagram (plays for reels); likes + comments on Threads and Substack. Drop posts under 7 days old
(not settled) and `pinned_old` posts. Python marks the top quarter and the bottom half. Under 20
posts → list them and call no pattern ("too few posts to call a pattern").

**Details for the top posts.**
- YouTube top quarter: `anyapi.youtube.video` {"id":"…"} for the exact publish date, length
  (`durationMs`) and likes, at most 15 calls.
- X Articles: `anyapi.twitter.article` {"url":"…"} on the top 10 for title, word count and
  opening lines.

**Look.** Download now (Instagram links expire within hours) the image, cover, first slide or
thumbnail of every top-quarter post and 5 bottom posts into `<platform>/img/`. Build one contact
sheet per platform and tier (a Pillow grid with each post's engagement under it), save them as
`<platform>/img/sheet_<platform>_top.jpg` and `sheet_<platform>_bottom.jpg` (the report template
looks for these names), plus a sidecar beside each, `sheet_<platform>_<tier>.json`: a list of
`{"rank", "engagement", "url"}` in sheet order, which the report prints as linked captions. Match
the cell shape to the media (portrait for Instagram and LinkedIn, 16:9 for YouTube and Shorts).
Open the sheets. A file that does not download is "not read", never described from its caption.

**Read** each post against its platform's checklist. What the text or image shows is SEEN; why it
might work is INFERRED. Check the format split first: when one format holds most of the top
quarter (Articles on X, carousels on Instagram, text images on LinkedIn), that is the pattern,
and hook wording may show no difference at all.

- **X.** Articles vs regular posts: share of the top quarter and median views of each. Article
  titles, length in words, and the first lines. Regular posts: the first line (before "Show
  more"): length, a number, "I" or "you", a question, a contrarian claim. Thread or single
  (`anyapi.twitter.thread` {"url":"…"} on the top 3 threads, if any). Media: none, screenshot, chart
  or metric card, video, meme, photo of PERSON. Hour posted. PERSON's own numbers in top posts.
- **LinkedIn.** The 2 lines before "see more". White space and line length. Format: text, image,
  document carousel, video, poll, article. Image shows PERSON's face, a product, or a text graphic.
  Story, advice, list or contrarian take. The closing question or CTA. Hashtag count. Days posted.
- **Instagram.** Which kind wins: reel, carousel or photo. Cover or first slide: headline words,
  face, template. Carousels: slide count, what the last slide asks. Reels: length, on-screen hook
  text. Caption: the line before "more". "Comment WORD to get X" lead magnets. The grid: repeated
  colours, fonts, frames.
- **YouTube.** Title: length, number or money, a time frame ("in 6 months"), first person,
  question, brackets, the promise. Thumbnail: face and its emotion, words on it (count them; don't
  assume ≤ 4), before/after, contrast and main colour. Do title and thumbnail repeat or add to each
  other? Length, Shorts vs long, upload rhythm.
- **Any other platform.** Use the nearest checklist. Threads and Bluesky → X. TikTok and Facebook
  reels → Instagram reels plus YouTube Shorts (cover, on-screen hook, length, sound). Substack,
  Medium and other newsletters → YouTube's title list plus subtitle, length in words, free vs paid,
  publish rhythm. Reddit → title pattern (question, story, "I made…"), subreddits. Pinterest → pin
  image and title.

**Topics.** Label every post with one of 3-6 topic pillars drawn from the posts, one set across
all platforms. Python: share of posts and median engagement per pillar per platform. A pillar that
is 10% of posts but 40% of top posts is the money topic. Report the share left as "other"; keyword
rules alone can leave a third of posts unlabeled.

**Voice.** Tone, sentence length, signature phrases and coined terms, recurring series, emoji use,
how posts open and close. Two quoted examples each.

**Write up**, per platform:
- **Pattern.** 3-5 traits the top quarter shares and the bottom half lacks, each counted ("7 of 9
  top posts open with a number, 2 of 14 bottom ones"). A trait that shows no difference is not a
  pattern; drop it.
- **House style.** What repeats everywhere: colours (named, hex read off the images), fonts,
  templates, series names.
- **Formulas.** The 2-3 fill-in templates behind the top hooks, titles or covers ("I [did hard
  thing] for [time]. Here's what I learned:"), one real example each.
- **Early vs now.** What changed between step 3's early era and today.

## 6 · The cross-platform system — no calls

- **Home base.** The platform with the biggest following and the earliest posts.
- **Repurposing.** Match posts across platforms that carry the same idea within 14 days (Python:
  TF-IDF cosine ≥ 0.5 on text, title or caption; check the top 10 matches by eye). Also match long
  pieces by exact title across newsletters, X Articles and YouTube within 30 days. Which platform
  gets an idea first, the median lag in days, and how its form changes (letter → Article → quote
  card → video).
- **Cadence.** Posts per week per platform over the last 13 weeks, best days and hours (say the
  timezone), weeks with no posts.
- **Who each platform is for.** The audience implied by each platform's topics and CTAs (INFERRED).
- **Skipped platforms.** List them. If one is where the user's audience is, say PERSON's playbook
  does not cover it.

## 7 · Funnel and money — ~1¢

- Read every bio link, link-in-bio page, product page and PERSON's site with `treg.web.extract`.
  Record: newsletter (Substack, beehiiv, Kit; the subscriber count if public), community (Skool,
  Discord, Circle; members and price), courses and digital products (the price next to the buy
  button, plus bundles and post-purchase upsells), quizzes that route people to an offer, a
  company or SaaS, coaching, consulting or booking links, speaking, affiliate links, merch.
- CTAs: per platform, the share of posts with a CTA and what it asks (follow, subscribe, link in
  bio, comment WORD, DM, reply). Pinned posts and featured sections.
- Sponsors: YouTube `anyapi.youtube.video_sponsors` {"url":"…"} on the top 5 and latest 5 videos
  (a "suspected sponsor" that is PERSON's own product is self-promotion, not a sponsor); elsewhere
  #ad, #sponsored, "paid partnership" or "partnered with" in step 2 text.
- Output, the funnel map: attention (platforms and followers) → capture (newsletter, community,
  lead magnet, quiz) → money (products, sponsors, services). Each SEEN or INFERRED, linked, with
  prices seen and the date.

## 8 · Moves vs growth — no calls

Which moves came right before growth sped up. Python only; everything is already pulled.

- **Moves.** One row per dated move from steps 2-7: first post on a platform, a new format (first
  thread, Article, carousel, Short, newsletter), a new series, a boost from step 4, a guest spot, a
  product or newsletter launch, a posting rate that doubled, a milestone.
- **Growth.** Per platform: monthly median engagement and the milestone points from step 3.
- **Line up.** Per move: median engagement in the 2 months before vs the month of and the 2 after;
  lift = after minus before. Moves under a month apart form one cluster; credit the cluster, never
  one move inside it.
- Under 6 months of data or under 5 moves on a platform → list the rows, claim no lift.
- Write up: the 3 moves or clusters with the largest lift, and boosts that moved nothing. The lift
  is SEEN as numbers; that the move caused it is INFERRED (monthly data, moves overlap, growth has
  other causes).
- Save `moves-vs-growth.csv`.

## 9 · The playbook — no calls

- **Ten plays,** ordered by evidence × lift (step 8) × fit for the user's stage and platforms. For a
  user who is starting out, weight early-era moves highest: what PERSON did at 1k beats what they
  do at 1M. Each play: the play (one line) | evidence (SEEN/INFERRED + links) | effort (day / week /
  quarter) | time to first result + the metric | THE PROMPT: a paste-ready prompt for the user's
  agent that starts the play for the user's own brand (concrete: posts to write with the formula
  filled in for the user's niche, accounts to reply to, a lead magnet to draft, a series to start).
  At least one play per platform where step 5 found a pattern.
- **Don't copy:** 2-3 things that look like the secret but the evidence does not support ("posts 10
  times a day" when the jump came from one podcast), what PERSON's own data shows failing, and what
  only works at PERSON's size.
- **Timeline:** every dated move in order, against each platform's growth signals, with its lift.
- **By platform:** pattern, house style, formulas, voice, what worked and what didn't, linked.
- **14-day plan** for the platforms the user chose (default: the 3 where PERSON's patterns are
  clearest): day by day, what to post (with the formula), who to engage with, and the one number
  to check on day 14.
- **Before writing,** re-check every number in the draft against the code output; drop any claim a
  recount does not support.
- **Method notes:** endpoints called, skipped platforms and why, blocked pages, images not read,
  approximate dates, the date of every count, what is INFERRED or self-reported, no affiliation
  with PERSON. The bill: total and per step, and the balance before and after.
- Deliver `brand.md` + one-file `brand.html` + the CSVs. End with the first play to run this week.
- **Build the HTML with the shipped template**, never by hand:
  `python3 <this skill's base directory>/report/build_report.py rea-brand/<person-slug>/brand.md`
  (needs `pip install markdown`; Pillow is optional). It gives every run the same design: contents
  sidebar, stat tiles, evidence pills, Stripe-style tables, growth chart, contact sheets and
  copy-prompt buttons, light and dark. Write `brand.md` to its conventions:
  - `# PERSON: personal brand teardown`, then one meta line (date, platforms, posts, calls, cost).
  - A ```` ```stats ```` block before `## The short version`, one tile per line:
    `VALUE | label | SEEN | source` (4 tiles; source is the post URL or a `#section` anchor such
    as `#x`, `#instagram`, `#bill`, so every tile links to its evidence).
  - `## The short version` as a numbered list of 5: each item a bold lead sentence, then one
    sentence of detail with the key count (all five must fit the first screen), ending with a
    "First play to run this week" line.
  - A ```` ```chart ```` block under `## When he grew`: `point YYYY-MM VALUE LABEL` lines (from the
    milestones; at least 2, or the report says there is not enough data), `pin YYYY-MM text` lines
    (dated moves), and one `caption` line. Malformed lines are skipped with a warning.
  - Each play's prompt in a ```` ```prompt ```` block.
  - One `### <Platform>` heading per platform under the content section; contact sheets saved as
    `<platform>/img/sheet_<platform>_top.jpg` and `_bottom.jpg` are placed under it automatically.
  - Write SEEN and INFERRED as plain words; the template turns them into pills.

## 10 · Content report (content mode) — no calls

- Per platform: sample size and dates, pattern, house style, formulas, voice, top 5 posts linked.
- Across platforms: the shared style, where one platform breaks it, and the repurposing chain.
- For the user (when handles were given): per platform, 5 ready hooks, titles or covers written
  from the formulas for the user's niche, and one paste-ready prompt that makes the first post.
- Method notes as in step 9.
- Deliver `content.md` + one-file `content.html` + the CSVs, built with the same template and
  conventions as step 9: `python3 <this skill's base directory>/report/build_report.py
  rea-brand/<person-slug>/content.md`.
