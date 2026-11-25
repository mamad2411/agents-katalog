---
name: sr-text-post
description: Writes text posts and threads for LinkedIn, X, Threads and Facebook. Builds a first line that survives the preview cut, one idea per post, a structure that fits each platform, and sensible link and tag placement. Use when someone asks for a LinkedIn post, a thread, a tweet, a Threads post, a build-in-public update, or wants to turn a video or article into written posts. Keeps the creator's voice and flags what a script cannot fix.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the caption checker and humanizer; the by-hand method below works without them.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Text posts and threads

On a text platform the first line is the thumbnail. Everything that follows has to earn its place.

## Ask first

- The idea and the one thing the reader should take away.
- The platform. Writing for LinkedIn and X is different work.
- A real detail the post can stand on: a number, a name, a moment, a mistake.
- Whether to include a link, and where it goes.

## Structure by platform

**LinkedIn** (up to 3,000 characters). Only the first couple of lines show before "see more", and the exact cut changes, so ask the person to look at their live feed. First line carries the claim or the story's hook. Then short paragraphs, one thought each, a blank line between. End with a question the reader can answer in one line, or a clear takeaway. A common tip is to put links in the first comment; there is no verified source for it in the database, so test it. LinkedIn has not published its ranking weights; early engagement, comment depth and dwell time are widely modelled as inputs (inferred, low confidence, `facts_search id=linkedin.signals.modelled`).

**X** (280 characters for standard posts; Premium accounts can write much longer). One idea. Put the point first. For a thread: post 1 is the hook and stands alone; each next post advances the idea by one step; the last post says what to do and links to the source. Keep threads as short as the idea allows. X published its For You ranking code in August 2026, and secondary reports say replies, quotes and DM shares are weighted far above likes, and that reports, mutes and blocks count heavily against a post. The weights apply to predicted probabilities, not raw counts. Read `facts_search id=x.ranking.open_source` and its status before building strategy on any single number.

**Threads** (500 characters). Conversational. Lower stakes than LinkedIn. Good for a sharper take, a quick update or a question.

**Facebook.** Meta says it will preferentially promote content filmed or produced directly by the creator or page owner (`facts_search id=facebook.original.2026_04`). Write the way you would talk to people who already know you, in your own words and with your own photos or footage.

## Write

1. Start from the true detail, not from the lesson.
2. Cut the first sentence if it only clears your throat.
3. Prefer the plain word. Avoid "leverage", "unlock", "game-changer", "delve".
4. Write one version for each platform. Do not paste identical text.

## Check and polish

- `caption_check` with the platform and keywords (`sr-caption`).
- `text_humanize` for the stock phrases and typography (`sr-humanize`). The script catches patterns such as "it's not just X, it's Y", triplets, and tidy summary closers. These need a human rewrite, so rewrite them in the creator's words.

## Turn other things into text posts

From a video or article: pick two or three points, each a standalone post with its own real example. Say where it came from if it helps. Do not post a transcript.

## Gate

`approve`. Posting is `human`.

## Do not

- Write a "thought leadership" paragraph with no example in it.
- Engagement-bait ("Agree?") as the only ask.
- Tag people to pull them into a thread they did not agree to be in.
