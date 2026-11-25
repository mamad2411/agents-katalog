---
name: sr-outliers
description: Ranks posts by how far each one beat its own account's median, so a small account's breakout is not buried under a giant's average. Finds the hook shapes and topics that recur among the winners and builds a swipe file. Use when someone has a list of posts with views (their own, or public posts they collected by hand) and asks "what works in my niche", "which of my posts did best", "what should I copy" or "build me a swipe file". Needs a table with views and caption or title text; nothing is scraped.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the ranking tool; the by-hand method below needs only a spreadsheet.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Outliers: find what beat the odds

A post with 40,000 views on an account that usually gets 2,000 tells you more than one with 400,000 views on an account that usually gets 600,000. Compare each post with its own account's median.

## Get the data

You need a table with at least these columns, one row per post:

| Column | Notes |
|---|---|
| `account` | Handle. Needed to compute each account's own median. |
| `views` | A number. `12.5K` and `1.2M` are understood. |
| `text` (or `caption`, `title`, `hook`) | The first line is enough. |
| `url` | Optional, but keep it so you can go back. |
| `date`, `followers`, `duration` | Optional. Followers add a reach-to-followers ratio. |

Where it comes from, in order: the person's own export; a public profile page they copy by hand (10 to 20 recent posts per account, five to ten accounts); a connected tool. At least **8 posts**, and at least 4 per account for an account's median to mean anything. Say that 8 is a floor, not a comfortable number.

Do not scrape logged-in pages and do not invent rows.

## Run it

Tool: `outliers_rank` with the table as `text`. CLI: `python scripts/sr.py outliers --file posts.csv --top 15`. For a markdown swipe file add `format=swipe` (CLI `--format swipe`).

By hand: for each account, take the median of its views; divide each post's views by that median; sort descending.

## Read the result

- **Multiple over median.** 3x or more is worth studying. Under 2x is noise on small samples.
- **Hook score and shape.** Which of the 32 hook shapes the opener fits, and the structure with the nouns blanked (`I read {N} interview scorecards. {N} failed the same way in {time}.`).
- **Top third versus bottom third.** Differences in hook score and hook length between the best and worst posts.
- **Formulas by average multiple.** Look at `n`. One example is an anecdote, not a pattern.

## Write the takeaways

Three findings, each tied to specific posts, each with how sure you are. Then one thing **not** to copy: a trick that works only for that creator's face, fame or footage.

Save the swipe file. The shapes are for structure. The words must come from the creator's own experience (`sr-hook`).

## Gate

`approve`. The person chooses which two shapes to try first.

## Do not

- Treat views as the only success measure. Sends, saves, watch time and conversations may matter more for the goal. Ask.
- Draw a conclusion from fewer than three examples of a pattern.
- Present a pattern as "what the algorithm wants". It is what happened on those posts.
