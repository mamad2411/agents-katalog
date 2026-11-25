---
name: sr-growth-loop
description: Runs the learning loop that makes a channel get better over time. Writes a hypothesis before posting, changes one variable, logs each post's result, and tests the outcome with a rank-sum permutation test that says adopt, keep testing or drop, including when there are too few posts to tell. Tests hooks, first frames, lengths, thumbnails, titles, captions and posting times. Use when someone asks what to test, whether a change worked, how to improve step by step, or wants a growth routine. Logs live on the person's own machine.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the experiment tools, which store logs in a local folder (~/.showrunner); the paper method works without them.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Growth loop

Growth is a loop: guess, test, read, keep what worked. This skill keeps the loop honest.

## The loop

1. **Pick one question** from the last audit (`sr-audit`).
2. **Write a hypothesis before you post.** "If the first line names a number, more people will stay past three seconds."
3. **Change one variable.** Same platform, same format, same topic mix as far as you can. Everything else stays put.
4. **Post at least four per variant.** Fewer than that cannot be tested, and the tool will say so.
5. **Log each result** as you go.
6. **Review.** Adopt it, keep testing, or drop it.
7. **Save the lesson** to the profile so the next plan uses it.

## Run it

```
python scripts/sr.py exp new --hypothesis "A number in the first line improves 3-second hold" --variable "first line" --metric "3-second hold %" --platform instagram
python scripts/sr.py exp log <experiment-id> A 41 --ref "reel 12 May"
python scripts/sr.py exp log <experiment-id> B 58 --ref "reel 14 May"
python scripts/sr.py exp review <experiment-id>
```

As tools: `experiment_new`, `experiment_log`, `experiment_review`. Variants are named by the person (A and B, or "number" and "no number").

## How the verdict works

The review ranks all logged posts together and compares the two variants with a rank-sum permutation test, which makes no assumption about how views are distributed. In plain terms: it asks how often shuffling the labels at random would produce a gap as big as the one you saw. It also reports the ratio of the variants' medians.

There are four outcomes:

- **"X looks better ... Adopt it and keep logging."** The p-value is under 0.1 and one variant's median is at least 1.2 times the other's.
- **"Not enough posts."** Either variant has fewer than four.
- **"No clear difference ... Run it longer, or test something bigger."** The gap is small or the p-value is high.
- **"Needs at least two variants."** Only one variant has been logged.

With four posts per variant, only big gaps can show up. Say that. A "no clear difference" result at small n means "we cannot tell", not "it does not matter". The 0.1 and 1.2 thresholds are the maintainer's choice, not a standard. Variants are compared in alphabetical order of their names, so name them A and B.

## What to test first

Order by how much a change can move the number: the hook and the first frame, then title or cover, then length, then caption first line, then the topic angle. Posting time comes last, and only with the person's own analytics. For YouTube, Test and compare in Studio can test thumbnails and since July 2025 titles too (reported, `youtube.test_and_compare`; it may not be on every channel).

## Calibrating the scorers

After 30 or more posts with hook text, run `calibrate_run`. If the hook score separates this account's winners from misses with an interval above 50%, `write_weights` saves tuned weights to the local folder. If not, trust your own tests more than the score.

## Save the lesson

When a test is adopted, add one line to the profile's `lessons` list (`profile_save`), for example "Numbers in the first line helped 3-second hold in May (n=5 each)". Write what you found, with the sample size. Send the whole list when you save, since saving merges fields and replaces a list as a whole.

## Gate

`approve` at the start (hypothesis) and the end (adopt or drop).

## Do not

- Change two things at once.
- Stop a test early because it is looking good.
- Report "it worked" without the numbers and the sample size.
