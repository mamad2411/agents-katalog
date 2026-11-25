---
name: dev-comment
description: >-
  Write a helpful dev.to comment on someone else's article. Produces three
  angle options, one full comment, and a copy-ready block. Never posts
  automatically (dev.to's public API has no comment-create endpoint).
---

# dev-comment

Turns a reading into a dev.to comment that adds concrete value. dev.to
comments are threaded (max depth then flatten), support Markdown including
code blocks, and support only the ❤️ reaction on comments. Comment count +
comment likes feed into the post's "hotness" score.

## Before you write

1. Read the article. Identify one specific thing to add: a correction, a
   working snippet, a citation, a focused follow-up question, or a relevant
   personal experience.
2. Check the user's voice in `~/.claude/devto/voice.md`.
3. dev.to Code of Conduct applies: welcoming, respectful of differing views,
   graceful acceptance of criticism. No hate speech, trolling, insults,
   harassment, doxxing, or plagiarism.

## The shape

```
Line 1     the point. Lead with it. One sentence.
Body       short, 1-3 lines per paragraph. Code blocks for snippets.
           Every snippet needs context text before it.
Close      one focused question or one thank-you. Never both.
Tone       warm, concise, evidence-based. Lowercase-casual is fine.
```

Length: under 200 words is the working range. dev.to comment threads flatten
after max depth — to continue, reply to the last comment in the overall
thread.

## The loop

**1. Pick three angles, not one.** Different approaches to the same article:
   - correction/addition ("Actually, X also handles Y…")
   - working snippet ("Here's a minimal reproduction…")
   - follow-up question ("Did you consider Z for this case?")
   - personal experience ("I hit this same issue with…")

**2. Draft the full comment** on the strongest angle.

**3. Humanize.** Run through `/dev-human` before showing it.

**4. Print the block.** Copy-ready:

```
COMMENT READY
angle:    #3 follow-up
length:   85 words
humanizer: 3 artefacts stripped, human score 88 PASS

[comment body]

Reply "yes" to log it, or tell me what to change.
```

**5. Never post automatically.** dev.to's public API (v1) exposes comment
read-only (`GET /api/comments?a_id=`, `GET /api/comments/{id}`). There is no
comment-create endpoint. The user pastes it into the dev.to comment box
manually. On "yes", append to `~/.claude/devto/log.md`.

## Rules that make the difference

- **Add concrete value.** Cite sources, share a working snippet, correct with
  specifics, ask a focused follow-up. No "Great post!" drive-bys.
- **Lead with the point.** Don't bury the lede.
- **Code blocks for snippets.** Every snippet needs intro context.
- **Match dev.to's Code of Conduct tone.** Welcoming, respectful, graceful
  with criticism.
- **Disclose AI assistance** where applicable (per dev.to AI guidelines).
- **No AI-generated comments.** dev.to policy: no bots / AI-generated
  comments (exceptions: basic translation/grammar tools, assistive tech).
- **Subscribe** to the post's comments if you want to catch replies.
- **Hide, don't argue.** If someone is abusive on your post, hide it via the
  dropdown rather than escalating.
- **Reply to your own post's comments.** Authors who respond build discussion.
  Prompt replies (especially early comments) boost thread activity.
- **#discuss** tag on your own posts for open-ended questions — can earn
  "Top Discussion of the Week" badge.

## Example

```
/dev-comment this post about React server components
```

```
ANGLES
1. Correction  "Server Components don't replace Client Components; they complement them."
2. Snippet     "Here's a minimal 'use client' boundary example…"
3. Question    "How do you handle data fetching at the boundary?"

Shipping #2: gives the reader something they can paste and run.

[comment body with code block]

COMMENT READY
angle:    #2 Snippet
length:   92 words
humanizer: 2 artefacts stripped, human score 85 PASS
```

## Self-improvement: angle learning

After publishing comments, note which angle type (correction / snippet /
question / experience) draws the most replies on the user's own posts.
Promote that angle in the 3-angle options; demote angles that consistently
get zero replies. Track in `~/.claude/devto/log.md` if you want per-comment
analytics (comment replies are not exposed by the Forem API, so this is
manual observation).

## Skipped (ponytail)

- No comment-create automation (Forem API limitation).
- No reaction toggling via API (disabled in some MCP servers due to 401 scope;
  web UI only).
