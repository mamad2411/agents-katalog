---
name: dev-repurpose
description: >-
  Turn one long asset (blog post, docs, newsletter, transcript, client call)
  into a dev.to article with canonical URL back to the source. Produces title
  options, tags, body markdown, cover prompt, and a copy-ready block. Never
  publishes without an explicit yes.
---

# dev-repurpose

Treats dev.to as a syndication channel, not the source of truth. The user
writes once (on their own blog / docs / newsletter) and repurposes to dev.to
with `canonical_url` pointing to the original — preserving SEO and making
dev.to a safe distribution surface.

## Before you write

1. Read `~/.claude/devto/voice.md` if it exists.
2. Confirm the user owns the source asset (or has rights to share it).
   dev.to's plagiarism policy prohibits all plagiarism types — direct, self,
   mosaic, accidental. Users certify rights to all posted content.
3. Ask for the source URL (the canonical home).
4. Ask whether the original has already been indexed / published. Best
   practice: let the original index a few weeks first, then syndicate to
   dev.to with `canonical_url` back to it.

## The shape

Same as `dev-post`, plus canonical handling:

```
Title        <10 words, keyword + number. Can differ from source title.
Body         Adapted for dev.to: H2/H3, short paragraphs, code blocks,
             cover image, CTA/question at end. Not a verbatim copy — rewrite
             the intro for dev.to's audience.
Cover        1000×420 absolute URL (new cover, not source's).
Tags         exactly 4, mixed broad + niche.
Canonical    canonical_url = source URL. Set on dev.to copy, not source.
AI disclosure| if AI assisted, add #ABotWroteThis or in-article statement.
```

## Cross-posting flow (recommended)

1. Publish on own blog (canonical home). Let it index 1–2 weeks.
2. Repurpose to dev.to with `canonical_url` → own blog.
3. Optionally repurpose to Hashnode (canonical URL) and Medium (import from
   URL sets canonical automatically).
4. Always set `canonical_url` to the primary blog to consolidate SEO.
5. Add an explicit link back to the original in the dev.to body text.

## The loop

**1. Read the source asset.** Extract the core idea, code snippets, and
takeaways.
**2. Pick three titles.** Run through `title-formulas.json` (from dev-post).
**3. Draft the dev.to adaptation.** Not a copy — rewrite for dev.to's
beginner–intermediate audience.
**4. Humanize.** Run through `/dev-human`.
**5. Tags.** Exactly 4 from `tag-suggestions.json`.
**6. Print the block.** Copy-ready, with `canonical_url` in front matter or
gear icon. Then:

```
POST READY
title:     #12 Comparison · Adapted title
length:    1,100 words · ~4 min read
humanizer: 5 artefacts stripped, human score 84 PASS
tags:      javascript, webdev, tutorial, react
cover:     {{cover image URL}}
canonical: https://yourblog.com/original-post
series:    {{none}}
published: draft
post at:   Tuesday 9:00am ET

Reply "yes" to log it, or tell me what to change.
```

**7. Never publish automatically.** Copy-paste into dev.to editor, OR use
Forem API `POST /api/articles` if `DEVTO_API_KEY` is present (deferred feature).
Record `canonical` and `series` in `~/.claude/devto/log.md` so `/dev-learn`
can track whether syndicated posts (canonical set) underperform native ones.

## Rules

- **Canonical on dev.to copy, not source.** Don't set canonical to dev.to on
  the source blog (SEO dilution).
- **Substantial content required.** dev.to's Terms §11: posts must contain
  substantial content — may not merely reference an external link holding the
  full post.
- **Affiliate links disclosed.** Clearly state compensation relationships.
- **No promotional backlinks.** Main purpose can't be SEO backlink farming
  (except personal blog or company blog posted under that company's org).
- **No AI-generated educational content** the human didn't already understand.
- **Never fabricate metrics or outcomes.**

## Skipped (ponytail)

- No RSS import automation (dev.to has built-in RSS import; drafts only,
  manual publish).
- No auto-sync of upstream edits (RSS import doesn't auto-sync).
