---
name: dev-post
description: >-
  Turn one raw idea into a dev.to article that sounds like you. Produces three
  title options, one full draft, and a copy-ready block. Never publishes
  without an explicit yes. Optional: can publish via Forem API if DEVTO_API_KEY
  is present.
---

# dev-post

Turns one raw idea into a dev.to article that sounds like the person who wrote
it. Optimized for dev.to's audience (beginner–intermediate web/dev tech),
feed ranking (reactions + comment count + comment likes), and syndication
best practices (canonical URL, cover image, tags).

## Before you write

1. Read `~/.claude/devto/voice.md` if it exists. That file is the user's
   voice profile: how they talk, what they never say, who they are talking to.
   If it does not exist, ask for **three of their own past posts** (dev.to or
   elsewhere), infer the voice from those, and write the file. Do not skip
   this and do not invent a voice. An article in the wrong voice is worse
   than no article.
2. Read `title-formulas.json` and `tag-suggestions.json` in this folder.
3. If the idea is thin - "post about AI" - do not pad it. Ask one batched
   question: what happened, to whom, and what did it cost or return. An
   article needs one specific true thing. Get it before writing.
4. Check `~/.claude/devto/log.md` if it exists - avoid repeating the same
   tag stack or title formula two posts in a row unless the user asks.
   Tag and formula suggestions are weighted by `dev-learn.py` audit results
   (higher weight = more likely to be suggested).

## The shape

dev.to rewards dwell time, reactions, and comments, in that order. So:

```
Line 1     the title. Alone. <10 words, keyword + optional number.
Lines 2-3  the hook. First sentence must pull the reader through.
Body       short paragraphs, 1-5 lines each, blank line between every one.
           No wall. Use H2/H3 headings only. Bold key bits.
Code       fenced markdown blocks for snippets; every block needs context.
Cover      1000×420 absolute URL. Strongly recommended; maximizes feed CTR.
CTA        one closing sentence: one specific question or one instruction.
           Never both.
Tags       exactly 4, comma-separated, mixed broad + niche.
```

Length: 800–2,500 words is the working range. Under 400 reads as a note,
not an article. Over 3,000 needs to earn every line.

- **Read time**: dev.to auto-computes `reading_time_minutes` (~260 wpm).
  Sweet spot for reach: 1–3 min reads. Sweet spot for depth: 4–7 min reads.
- **Half-life**: most views land in the first week; median post half-life is
  ~4 days. Optimize for the first 7 days, not forever.

## The loop

**1. Pick three titles, not one.** Run the idea through `title-formulas.json`
and choose three formulas that genuinely fit it. Different formulas, not three
variations of one. Show them as three numbered lines and say which you would
ship and why, in one sentence.

**2. Draft the full article** on the strongest title.

**3. Humanize it.** Run the draft through `/dev-human` before showing it.
Every article from this skill ships humanized.

**4. Pick tags.** Exactly 4 tags from `tag-suggestions.json`. Mix 2–3 broad
(#javascript, #webdev, #beginners, #tutorial, #programming) + 1–2 niche
(#react, #deno, #a11y, #graphql, #mcp). Flag `{{cover image URL}}` if missing.

**5. Print the block.** Copy-ready, in a fenced block, exactly as it should be
pasted into the dev.to editor (Basic Markdown supports YAML front matter;
Rich+Markdown editor uses the gear icon). Then, underneath:

```
POST READY
title:     #17 Build X in N Steps
length:    1,240 words · ~5 min read
humanizer: 6 artefacts stripped, human score 86 PASS
tags:      javascript, webdev, tutorial, react
cover:     {{cover image URL}}
canonical: {{canonical URL or none}}
series:    {{series name or none}}
published: {{draft or published}}
post at:   Tuesday 9:00am ET (from your plan)

Reply "yes" to log it, or tell me what to change.
```

**6. Never publish automatically.** This skill produces text. The user posts
it manually into dev.to, OR if `DEVTO_API_KEY` is present in `~/.env`, the
skill can offer to publish via `POST https://dev.to/api/articles` with headers
`api-key: $DEVTO_API_KEY` and `accept: application/vnd.forem.api-v1+json`.
On "yes", append the post to `~/.claude/devto/log.md` with the date, title,
formula_id, tags, cover, canonical, series, published, and first line.
Leave `engagement_rate`, `comment_ratio`, `reach_multiple`, `human_score`,
and `audit_rank` blank — `/dev-audit` fills those in after the post has
collected data. Then run `/dev-learn` (`dev-learn.py audit --apply`) to
promote winning formulas/tags and demote losing ones.

## Rules that make the difference

- **One idea per article.** If the draft has two, you have two articles. Say so.
- **Numbers over adjectives.** "$4,200" beats "a lot". If the user has not
  given you a number, ask for one rather than writing around the hole.
- **No engagement bait.** "Thoughts?" and "Agree?" are dead. The closing
  question has to be one only this article could ask.
- **Four tags maximum**, comma-separated, lowercase slugs (no spaces).
  Tags with spaces → 422 Unprocessable Entity.
- **Cover image must be an absolute URL.** Local paths break.
- **Canonical URL goes on the dev.to copy, not the source.** If cross-posting
  from a personal blog, set `canonical_url` on the dev.to article pointing back
  to the original. Let the original index first.
- **AI disclosure.** If AI assisted the draft, add `#ABotWroteThis` tag or an
  in-article disclosure statement per dev.to's AI guidelines. Do not publish
  AI-generated educational content the human didn't already understand.
- **No promotional backlinks.** dev.to bans posts whose main purpose is SEO
  backlinks (except personal blog or company blog posted under that company's
  org). Disclose affiliate links clearly.
- **Never fabricate.** No invented metrics, clients, revenue figures or
  outcomes under the user's name. If a number is needed and unknown, leave
  `{{your number}}` in the draft and flag it.
- **Accessibility:** alt text on images, H2/H3 headings, limit emoji at line
  ends, avoid fancy fonts.

## Example

```
/dev-post we built an internal tool that cut proposal time from 5 hours to 20 min
```

```
TITLES
1. #12 Comparison    I cut proposal time from 5 hours to 20 minutes with one script
2. #3  Mistake        For two years I charged clients for hours I wasted formatting
3. #10 List          5 ways to automate proposals without hiring a VA

Shipping #12: the ratio is believable and the number is yours.

# I cut proposal time from 5 hours to 20 minutes with one script

The first proposal I sent took all afternoon. Not because the work was hard —
because I was formatting by hand.

[... body ...]

What's one repetitive task in your workflow you'd automate first?

---
tags: javascript, automation, productivity, webdev
cover_image: https://example.com/cover.png
canonical_url: https://yourblog.com/proposal-automation
ai_disclosure_level: no_ai
```

POST READY
title:     #12 Comparison · I cut proposal time from 5 hours to 20 minutes with one script
length:    1,240 words · ~5 min read
humanizer: 6 artefacts stripped, human score 86 PASS
tags:      javascript, automation, productivity, webdev
cover:     https://example.com/cover.png
canonical: https://yourblog.com/proposal-automation
series:    none
published: draft
post at:   Tuesday 9:00am ET

Reply "yes" to log it, or tell me what to change.
```
