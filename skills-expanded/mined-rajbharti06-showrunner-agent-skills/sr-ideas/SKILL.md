---
name: sr-ideas
description: Builds a bank of content ideas from the creator's pillars and real experience, scores each one on pain, proof, novelty, fit and effort, flags near-duplicates, and picks the first batch. Use when someone is stuck for ideas, asks "what should I post", wants a month of topics, or needs to choose between ideas. Crosses pillars with twelve proven angles to seed brainstorming, then ranks with a transparent weighted score.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the scoring tool; the by-hand method below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Ideas: from experience, not from nowhere

The best ideas are things the creator has lived, seen or tested, aimed at a real person's problem. This skill produces prompts for the creator to answer, then helps pick.

## Ask first

- What are your three pillars? (From `sr-strategy`, or the profile.)
- What did your audience ask you in the last month, in comments, DMs or real life?
- What did you get wrong this year that cost you something?

## Seed

Tool `ideas_matrix` with the pillars (CLI `python scripts/sr.py matrix --pillars "A,B,C"`). It crosses each pillar with twelve angles: the mistake most people make, the myth to retire, the story behind it, the teardown of something that worked, the checklist, the comparison, the beginner trap, behind the scenes, the result and how it happened, the prediction and what to do now, the question your audience keeps asking, the unpopular opinion.

Each prompt is a question for the creator, not an idea. Pick the 10 to 15 they can answer from their own life, and write each answer as one line: a specific claim with a number, name or place in it.

Ask for **one real detail per idea**: the number of times, the name of the place, what exactly went wrong. If they have none, the idea is not ready.

## Score

Rate each idea 1 to 5 on:

| Criterion | Weight | Ask |
|---|---|---|
| Pain | 30% | Does the target viewer already feel this problem? |
| Proof | 25% | Can the creator show it happened to them? |
| Novelty | 15% | Would someone who has seen the usual advice learn something? |
| Fit | 15% | Does it serve the promise and one pillar? |
| Effort | 15% (inverted) | How hard is it to make? 1 is easy. |

Write the lines as `idea | pain | proof | novelty | fit | effort` and run `ideas_score` (CLI `python scripts/sr.py ideas --file ideas.txt`). Unrated ideas get neutral 3s and are marked, so rate them. Near-duplicates are flagged: merge or drop.

By hand: score = 30% pain + 25% proof + 15% novelty + 15% fit + 15% (6 minus effort), rescaled to 0 to 100.

## Pick

Take the top six. Check the batch for balance: not all one pillar, not all one format, at least one that is cheap to make. Show the ranked list and the reason for the top three.

Keep the rest as the idea bank. Add to it every week from comments.

## Gate

`approve`. They choose what goes into the next batch.

## Do not

- Pad the list with generic topics nobody asked for.
- Invent a story to make an idea "stronger". Ask for the real one.
- Treat the score as a prediction. It is a way to compare options.
