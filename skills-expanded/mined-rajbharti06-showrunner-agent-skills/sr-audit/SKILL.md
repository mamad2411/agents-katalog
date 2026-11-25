---
name: sr-audit
description: Reads a creator's own numbers honestly. Compares each post to the account's own median, ranks winners and misses, reads a retention curve for cliffs and bumps, checks whether the hook score actually predicts this account's results, and finishes with one lesson and one change for next week. Use for a weekly or monthly review, when someone asks why a post flopped or won, or wants to know what to do more of. Works from analytics exports pasted or attached. Warns when there are too few posts to conclude anything.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the tools; the by-hand method works without them.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Audit

Numbers are easy to misread. The rule here: compare a post with the same account's usual posts, name what is different, and change one thing.

## Ask first

- The platform and the time window.
- A table of posts as CSV with at least `account`, `views` and `hook` columns, and optionally `likes`, `url`, `platform` and `posted`. Use the key number for that platform in place of views if it is a better measure (`references/metrics-by-platform.md`).
- For video, the retention curve from the platform's analytics for one or two posts, as a CSV with `seconds` and `retention_percent` columns.
- What they changed in this period, if anything.

## Method

1. **Count the sample.** Under about ten posts, say that conclusions are weak. Under four per variant, there is no test.
2. **Use the account's own median.** For each post compute the multiple over the account median. Winners are well above it, misses well below. Compare to yourself, not to someone with ten times your audience.
3. **Rank.** Tool `outliers_rank` on the table (CLI `python scripts/sr.py outliers --file posts.csv --platform short`). It lists the top and bottom with the multiple.
4. **Find what differs.** Put the top three and the bottom three side by side: hook, topic, length, format, first frame, day. Name differences you can see, not guesses about the algorithm.
5. **Read retention.** Tool `retention_read` (CLI `python scripts/sr.py retention --file curve.csv --duration-seconds 45`). It reports the shape, where the audience leaves, and bumps worth keeping. Fix the first cliff first.
6. **Check the scorer.** With 30 or more posts and hook text, run `calibrate_run`. It splits the account's posts at its own median and reports how often the hook score ranks a winner above a miss, with a 90% interval. If the interval includes 50%, the score is not helping this account, and the tool says so.
7. **Write one lesson and one change.** Not five. Log the change as an experiment (`sr-growth-loop`).

## Output

```
Window | Posts | Median | Best | Worst
What the winners share:
What the misses share:
Retention note:
One lesson:
One change next week:
Confidence: low / medium / high, and why
```

## Honesty rules

- A single viral post is an outlier. Look for a pattern in at least three.
- Views are not the goal. Ask what the goal was (`sr-strategy`): followers, leads, saves, sends.
- Platforms report different things. Use the measures in `references/metrics-by-platform.md` and state what each one means.
- If the data cannot answer the question, say so and say what to collect.

## Gate

`approve`. The change goes into the next sprint.

## Do not

- Declare a rule from two posts.
- Compare a three-month-old channel with a ten-year-old one.
- Trust any single number the heuristic scorers print. They are unvalidated until `calibrate_run` says otherwise for this account.
