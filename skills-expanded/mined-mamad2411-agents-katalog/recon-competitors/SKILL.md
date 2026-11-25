---
version: 0.1.0
name: recon-competitors
description: |
  Benchmark a brand against its rivals using RECON UGC's competitor board,
  and explain head-to-head why one video beat another.
  Use when: "how do we compare to X", "competitor analysis", "what are our
  competitors posting", "who is winning in our category", "why did their
  video beat ours", "what formats are they running that we aren't", or any
  request to position one brand's short-form output against others.
  NOT for: general library research (use recon-research) or writing a shoot
  plan (use recon-brief).
allowed-tools: Bash
---

# RECON competitors

The competitor board only contains brands the user chose to track. It is their
curated set — never present it as "the whole market", and never imply RECON is
showing them other customers' boards.

## Pull the board

```bash
reconugc competitors                    # defaults to the app category
reconugc competitors --industry ai-tools
```

Each row gives: active creatives, average outlier, creative score, engagement
rate, top format, and share of voice.

## Reading it honestly

- **Share of voice is view-weighted**, so one runaway hit can make a brand look
  dominant. Always sanity-check it against average outlier and post count before
  calling someone "the leader".
- **Average outlier is the skill signal.** A brand posting 20 videos at 2x is
  running a working system. A brand with one 100x+ fluke and nineteen duds is not.
- A row marked *still indexing* has no numbers yet. Say that plainly rather than
  reporting it as zero.
- **Format gaps** are the actionable part: formats rivals run that the user does
  not. That is where the next test should come from.

## Head to head

```bash
reconugc compare <post-id-a> <post-id-b>
```

Returns the winner, the margin, why, and a row-by-row read on hook, pacing,
format, and proof.

The verdict is decided on **outlier score, not raw views** — otherwise the bigger
account wins every time on audience size alone. When two videos are genuinely
close, RECON says so; do not manufacture a winner it did not call.

## How to report

Lead with the decision, not the table:

> "@rival is winning on volume, not craft — 20 posts at 1.9x average. Your best
> video beat anything they have. The real gap is format: they run Product Demo,
> you have never shipped one."

Then show the numbers underneath. Two or three rows of evidence, not a data dump.

## Adding a brand

If the user wants a brand that is not on the board, tell them to add it in
Competitors with the TikTok handle. Indexing runs in the background and takes about
a minute — the row appears as *still indexing* until then. Do not promise numbers
that are not there yet.
