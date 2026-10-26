---
name: yt-idea
description: >-
  Turn a niche or a blank page into video ideas that are searchable,
  specific and bigger than the channel - each one scored before it costs
  a week of filming. Use for "what should I make", "I have no idea what
  to post", "give me video ideas", "ideas for my channel", or when a
  creator is staring at an empty upload schedule.
---

# yt-idea

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Ideas are cheap. Ideas shaped so somebody clicks them are not. This gets from a niche to a scored
shortlist without you shooting the wrong one.

A tool lives here and it runs. Use it; do not eyeball the idea.

```bash
python3 "$YT_SKILL_DIR/ideascore.py" ideas.txt           # rank a batch
python3 "$YT_SKILL_DIR/ideascore.py" --idea "one line"   # score a single one
```

## Before you write

1. Use the available voice profile or creator context (see the operating guide) - who the one viewer is, what the channel will not claim. An
   idea for the wrong audience scores well here and dies on upload.
2. Never invent demand. This skill shapes an idea; it does not know your market. Pair it with
   [$yt-viral](../yt-viral/SKILL.md), which reads what is actually working, before you commit a month to a theme.

## The move

1. **Widen, then narrow.** From the niche, write 15 raw ideas fast - do not filter yet. Pull from:
   the creator's own comments (the questions people already ask), [$yt-viral](../yt-viral/SKILL.md) outliers in the
   niche, the beginner mistakes in the topic, and the "X vs Y" the audience argues about.
2. **Score all 15** through `ideascore.py`. It rates each on SEARCH, SPECIFIC, REACH and DURABLE and
   flags the weakest axis.
3. **Refine the strongest candidates.** Improve each idea's weakest useful dimension without adding
   unsupported numbers merely to increase its heuristic score. The score is not measured demand or
   a calibrated prediction of performance.
4. **Label the mix.** Mark each as evergreen or timely. A schedule that is all timely has no library;
   all evergreen and the channel never rides a wave. Aim roughly 3 evergreen to 1 timely.

## What to hand back

- the 5 reshaped ideas with their scored panels
- for each: the one query a real person types to find it
- the evergreen / timely label on each
- one line: which to shoot first, and why that one now
