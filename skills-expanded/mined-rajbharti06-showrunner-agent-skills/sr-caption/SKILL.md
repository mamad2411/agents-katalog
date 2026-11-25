---
name: sr-caption
description: Writes and checks captions and descriptions for Instagram, TikTok, YouTube, Facebook, LinkedIn, X and Threads. Shows exactly what the feed shows before the more cut, then checks length, the first line, a concrete number or name in the visible window, hashtag count, number of asks, search terms, links and readability for the chosen platform. Use when someone asks for a caption, a description, hashtags, alt text, or whether a caption is too long or buried.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the checker; the by-hand checklist below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Captions

A caption has two jobs: make a scroller stop, and help the right people find the post. The first line does the first job. The keywords do the second.

## Ask first

- Which platform, and what is the piece? (Each platform has a different preview cut.)
- The hook already chosen for the piece, so the caption adds to it instead of repeating it.
- The one thing you want people to do. One.
- The search terms a person would type to find it.

## Write

1. **First line.** Lands inside the preview. Specific. Says something the video does not already say on screen.
2. **Body.** Two to five short lines with line breaks. Each line one thought. The creator's voice (`sr-voice`).
3. **One ask.** Save, send to a friend, comment with a word, follow. Pick one. People do one thing.
4. **Keywords.** The main search phrase in the first line or the first sentence, and again naturally in the body. TikTok search is described as using caption keywords, hashtags, on-screen text and spoken words (low confidence, `facts_search id=tiktok.search.inputs`), so say the keyword out loud, show it on screen and write it in the caption.
5. **Hashtags.** Few and relevant. The cap differs by platform (below). Reported: Adam Mosseri said he would not think of hashtags as a way to get more distribution (`instagram.hashtags.distribution`), so treat them as labels, not a growth lever.
6. **Links.** Not clickable in Instagram or TikTok captions. Use the bio link. On LinkedIn, a common tip is to put the link in the first comment instead of the opening. Showrunner has no verified source for that, so test it (`sr-growth-loop`) before you rely on it.

## Check

Tool `caption_check` with `platform` set and optional `keywords` (CLI: `python scripts/sr.py caption --file caption.txt --platform instagram --keywords "interview,junior developer"`). It prints the preview box, then checks:

- length against the platform limit
- first line fits inside the preview
- a number or name in the visible window
- hashtag count against the cap or ceiling
- number of different asks
- search terms present, and in the visible window
- links that will not work
- walls of text
- stock phrases that read as machine-written

Fix every FAIL. Decide on purpose about each WARN.

## Platform limits at a glance

Limits move. Check `facts_search platform=<name> topic=limits` before you rely on one, and say how old the fact is. In the database on 2 November 2026:

| Platform | Limit | Status |
|---|---|---|
| Instagram | Captions up to 2,200 characters | official |
| Instagram | Five hashtags per post | reported |
| Instagram | Roughly the first 125 characters show before "more" | inferred, low confidence |
| YouTube | Titles up to 100, descriptions up to 5,000 | official |
| YouTube | More than 15 hashtags and all are ignored | official |
| LinkedIn | Posts up to 3,000 characters | official |
| X | 280 for standard posts; Premium accounts can write far longer | official |
| Threads | 500 characters | official |

Where a preview length is only inferred, the checker uses it as a guide. Ask the person to look at the live feed.

## Different caption per platform

Do not paste the same caption everywhere. Rewrite the first line for each platform, keep the one ask, and match its norms: shorter on X and Threads, more context on LinkedIn, keyword-led on YouTube.

## Alt text

If the platform has an alt text field, write one plain sentence saying what is in the image or slide. It helps people using screen readers, and it is free search text.

## Gate

`approve`. Then the `humanize` pass (`sr-humanize`).

## Do not

- Stack a call to action for every action the platform offers.
- Use a trending hashtag unrelated to the post.
- Write "link in bio" if the bio link does not match the post.
