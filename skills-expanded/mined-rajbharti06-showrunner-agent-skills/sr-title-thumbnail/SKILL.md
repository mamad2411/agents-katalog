---
name: sr-title-thumbnail
description: Designs a YouTube title and thumbnail as one message in two places. Writes five titles, scores them for length, keyword placement, specificity, curiosity and clarity, flags clickbait promise risk, checks that the thumbnail text does not repeat the title, and sets up a Test and compare plan. Use when someone asks for a YouTube title, thumbnail ideas, "why is my click-through rate low", or is about to publish a video. Also works for Reel cover text.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the scoring tool; the by-hand checklist below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Title and thumbnail

On YouTube the title and thumbnail are one pitch. They share a small space and split the job: the title says what it is, the thumbnail says why you should care right now.

## Ask first

- What does the video actually deliver? (If the promise is bigger than the video, fix the promise.)
- What phrase would the viewer type to find this? That is the keyword.
- Who is it for?
- Is there a face, an object or a result that can be shown?

## Titles

Write five that differ in angle: the result, the mistake, the number, the question, the comparison. Rules of thumb that hold up:

- Put the keyword in the first 40 characters or so.
- Use a specific number, name or time when you have a true one.
- About 35 to 65 characters reads cleanly everywhere. The limit is 100 (`facts_search platform=youtube`).
- Open a gap, then keep the promise inside the video.
- Avoid ALL CAPS shouting, stacked punctuation and phrases that promise what the video cannot deliver.

Score with `title_score`, one title per line, with `keyword` set (CLI: `python scripts/sr.py title --file titles.txt --keyword "interview mistakes"`). It scores length, keyword, specificity, curiosity and clarity, flags promise-risk phrases and takes points off for shouting and stacked punctuation. Like the hook score, it is a heuristic and has not been validated against click-through rates.

## Thumbnail

Three concepts, each in one sentence. Craft principles, not laws:

- One focal point. Readable at phone size.
- Three to four words of text at most, and only if they add something the title does not say.
- Strong contrast between subject and background.
- A real face with a clear expression works when the creator is the story. An object or result works when it is.
- Matches what the video delivers.

Check the pair: `title_score` with `thumbnail_text` set. It measures word overlap and thumbnail word count and prints a test plan.

## Test it

If their channel has Test and compare in YouTube Studio, use it. Reported: it tests thumbnails, and titles since July 2025, but availability can differ by channel (`facts_search text="test compare"`). Change one thing per test. Let it run to a winner or a full week of impressions. Log the lesson with `experiment_log` (`sr-growth-loop`).

## Reels and Shorts covers

The same split applies. Cover text should add a second angle to the caption's first line, not repeat it.

## Gate

`approve`. They pick the pair and say what feels untrue.

## Do not

- Write a title the video does not pay off. Retention and trust both pay for it.
- Copy a competitor's thumbnail layout wholesale.
- Claim a title "will" get a click-through rate.
