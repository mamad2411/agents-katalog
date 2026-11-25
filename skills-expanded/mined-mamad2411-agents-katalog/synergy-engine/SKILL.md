---
name: synergy-engine
description: >
  Finds people writing about the user's topics and engages them, including the authors cited in
  their own paper. Use it for "find people posting about X", "who's writing about <topic> on
  LinkedIn", "engage the discourse on Y", "run the LinkedIn outreach cycle", "build my topic
  fingerprint", "comment-first outreach", "reach out to the authors we cited", "harvest the
  bibliography", or any /synergy-engine, /synergy-discover, /synergy-run or /synergy-cite-harvest
  command. It matches what the user has published against what targets are posting, then joins
  their conversations with a like and a practitioner comment, never a pitch. Three discovery
  centers: author and content (comment-first), and citation (connect-first plus email). It scores
  against a topic fingerprint, keeps xlsx trackers as memory, dedupe and queue, and acts through
  the user's own logged-in browser with a human-approval gate on every public action. Do not use
  it for writing blog posts, generic LinkedIn analytics, or cold sales sequences.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# Synergy Engine — topic-synergy outreach, comment-first

## When this skill applies

This skill should be used when the user wants to find people writing about their topics and engage them, reach out to authors they cited in their own paper, or runs any /synergy-engine command. Triggers: "find people posting about X", "who's writing about <topic> on LinkedIn", "engage the discourse on Y", "run the LinkedIn outreach cycle", "build my topic fingerprint", "discover on-theme posts", "comment-first outreach", "synergy scan", "reach out to the authors we cited", "we cited you outreach", "harvest the bibliography", "thank the people we cited", "/synergy-engine", "/synergy-discover", "/synergy-run", "/synergy-cite-harvest". The engine matches what YOU'VE published against what TARGETS are posting, then joins their conversations with a like + a practitioner comment (never a pitch), optionally citing their own work or your anchor paper in your content. It runs three discovery centers — author + content (comment-first, from who's posting) and citation (connect-first + email, from who you cited) — scores against a topic fingerprint, keeps xlsx trackers as memory/dedupe/queue, and executes through the user's own logged-in browser with a human-approval gate on every public action. Do NOT use this skill for: writing blog posts (use 4d-blog-engine), generic LinkedIn analytics (use linkedin-growth), or cold sales sequences (use apollo).


> **Read this when:** the user wants to find and engage the people writing about their topics. Your job is to route to the right command and hold the methodology so every run stays on-pattern. The detailed contracts live in the command files; the durable rules live in `references/`.

## The one idea

Stop guessing whether a target cares about your topics. Match **what you've published** against **what they're posting**, then join the conversations where the overlap is real. Comment to *add something* and cite people; never pitch. The product or paper is the contribution, never the ask.

## The loop (three moving parts)

1. **Your fingerprint** — a structured set of themes + signature phrases distilled from your own content (an `/answers` library, a whitepaper/anchor paper, repo posts, a keyword study). This is the matching key. Built/refreshed by `/synergy-fingerprint`.
2. **Their signal** — recent posts from targets, pulled two ways (see "Two topic centers"). Discovered + scored by `/synergy-discover`.
3. **The overlap** — per-post scoring against the fingerprint, surfaced as a synergy scan and written to the tracker as the engagement queue.

## Three topic centers

- **Author center** — start from *named people* (a curated profile list). Pull their recent posts via Apify `harvestapi/linkedin-profile-posts` (by profile URL). The relationship-building lane.
- **Content center** — start from *the content*, not the author. Search recent posts by keyword/hashtag via Apify `harvestapi/linkedin-post-search`, score for fit, and the fitting authors get added to the tracker. The reach-expanding lane, anchored on a paper/POV of yours rather than `/answers` pages.
- **Citation center** — start from *who you cited*. Harvest the cited authors out of your own paper's bibliography, enrich + verify them, and reach out to thank them (email first, then a LinkedIn connect). This is the cite-then-tell lever turned into a front-to-back pipeline; it's the only center that works on people who don't post. See `references/citation-center.md` and `references/outreach-channels.md`.

The author/content centers share the fingerprint, the comment-first cycle, and the post tracker (`references/topic-synergy-methodology.md`). The citation center reuses the engine's config, voice, cadence, and human-in-the-loop rules but starts from a bibliography instead of the fingerprint, sends connect-first (plus email) instead of comment-first, and keeps its detail in a richer citation registry.

## The engagement cycle (decision tree)

Always act first; cold DMs die. Every target runs through one tree. The fork is whether their post maps to one of your content categories.

- **Path A** (maps to a content category): publish/augment the answer citing their work, then **like + comment** referencing it (with your URL), then **DM/connect**. On non-posting experts it collapses to "cite, then DM."
- **Path B** (relevant, no category fit): **like + comment** that engages / challenges / poses a question. Link your own work only sparingly.
- **Third lever — cite-then-tell** (strongest): cite the target's own work, or your anchor paper, in your content, then open with "we cite your work in X." The only lever that works on people who don't post.

Full tree + the competitor rule (cite at the idea level, never the product) in `references/topic-synergy-methodology.md`.

## Commands

| Command | Does |
|---|---|
| `/synergy-engine:synergy-init` | One-time setup: declare the tracker location, the fingerprint content sources, the anchor paper/URL, and the LinkedIn channel(s). Creates the xlsx tracker. |
| `/synergy-engine:synergy-fingerprint` | Build/refresh the topic fingerprint from the configured sources. |
| `/synergy-engine:synergy-discover` | Discover on-theme posts (author and/or content center) via Apify, score against the fingerprint, dedupe against the tracker, write the synergy scan + queue. |
| `/synergy-engine:synergy-run` | Run the comment-first cycle on due/approved targets via Claude in Chrome: like + comment (+ cite + connect), HITL-gated. Log to the tracker. |
| `/synergy-engine:synergy-schedule` | Stand up the every-other-day prep task (stages drafts + books a calendar block; never posts). |
| `/synergy-engine:synergy-status` | Show the tracker: engaged / queued / due, by topic center. |
| `/synergy-engine:synergy-cite-harvest` | **Citation center.** Harvest cited authors from a paper's bibliography -> triage -> OpenAlex/ORCID -> Clarify dedup -> Apollo enrich + verify gate -> LinkedIn resolve + Apify verify -> draft email + connect note -> citation registry. Never sends. |
| `/synergy-engine:synergy-cite-run` | Send the "we cited you" outreach: email first (Mailtrap, BCC Dorian), then the LinkedIn connect note, with the send discipline. HITL-gated. Logs to the registry. |
| `/synergy-engine:synergy-cite-accept-check` | Daily follow-through: detect accepted invites, DM every new accept (gated), advance the registry. Schedulable. |

## Routing

- "set up / configure the engine" → `/synergy-init`
- "build/refresh my fingerprint" → `/synergy-fingerprint`
- "find people posting about X" / "who's writing about Y" / "content center sweep" → `/synergy-discover`
- "run the cycle" / "engage these" / "comment on the due ones" → `/synergy-run`
- "automate it" / "every other day" → `/synergy-schedule`
- "what's queued" / "tracker state" → `/synergy-status`
- "reach out to the people we cited" / "we cited you" / "harvest the bibliography" / "who did we cite" → `/synergy-cite-harvest`
- "send the citation emails / connects" / "thank the authors we cited" → `/synergy-cite-run`
- "who accepted" / "fire the accept-replies" / "citation follow-through" → `/synergy-cite-accept-check`

If the engine isn't configured yet (no tracker / config marker found), route to `/synergy-init` first.

## Non-negotiables (full list in references/cadence-and-guardrails.md)

- **The plugin never auto-posts.** Every public action (comment, like, connect, DM) and every live content edit goes through an explicit human OK in the same session, through the user's own logged-in browser.
- **Watch the "Post as" selector.** LinkedIn's identity caret sits next to the like button; a stray click switches your comment to a company page. Verify the composer says the intended actor before every comment, and reset it if it drifted.
- **Cite, don't pitch.** Competitor-founders get idea-level engagement that cites the paper, never the product.
- **Verified citations only.** Never fabricate a work or misattribute it. Verify author + title before citing.
- **Voice:** no em-dashes, 80%+ contractions, practitioner register, typographer's quotes. The comment adds something a senior peer would nod at.
- **Cadence:** <=5 fresh targets/run, comment same-day, connect 2-3 days later, no re-comment within ~3 of a person's posts.
- **The tracker is the source of truth** for dedupe and the queue. Never engage a target already "Engaged" or "Ready for review" unless its Next Action Date is due.
