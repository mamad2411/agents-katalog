---
name: espresso-check
description: >
  Trims the user's own writing — commit messages, Slack posts, emails, reports,
  self-reviews, READMEs. Finds the padding and shows the shorter version. This
  edits text the user wrote, not your own answers. Use when the user says
  "espresso check", "/espresso-check", "trim this", "cut this down", "is this
  too long", or pastes text asking to tighten it. One-shot review, persists
  nothing.
---

# espresso-check

You are editing the **user's** text, not your own. Do not confuse this with
espresso mode, which governs how you talk. Here the user hands you writing and
you cut it.

## Input

Whatever the user pastes or points at: a commit message, a Slack message, an
email, a PR description, a report, a self-review, a section of a README.

If no text was given, ask for it in one line and stop.

## What to cut

- Openers that say nothing — "I wanted to reach out", "Just following up"
- Hedges — "I think maybe", "sort of", "kind of", "a bit"
- Filler qualifiers — "very", "really", "quite", "actually", "basically"
- Restating the subject line or the question in the first sentence
- Closing throat-clearing — "Thanks in advance", "Hope that makes sense"
- Anything said twice in different words
- Passive voice where the actor matters

## What to keep

- Every fact, number, name, date, and commitment
- The ask. If the text asks for something, the cut version still asks for it
- Tone appropriate to the reader. Short is not curt — a message to a manager
  stays polite while losing the padding
- Domain terms the reader needs

Never invent content. If the original is vague about something, the cut
version is vague about the same thing — say so in the notes rather than
filling the gap yourself.

## Output

Two required blocks, plus a third when it applies. In this order, nothing else:

1. **Cut version** — the rewritten text, ready to paste
2. **Removed** — up to three bullets naming what you cut and why
3. **Kept deliberately** — only if you left something that looks like padding
   but is load-bearing. Omit this block entirely if there is nothing to say

No preamble. No "here's your revised text". Start with the cut version.

## Length target

Aim for 40-60% of the original. If the original was already tight, say so in
one line and return it unchanged — do not cut for the sake of cutting.
