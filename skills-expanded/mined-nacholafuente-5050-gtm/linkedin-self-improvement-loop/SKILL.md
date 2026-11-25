---
name: linkedin-self-improvement-loop
description: A build-measure-learn loop for your LinkedIn. Ingests your Creator analytics export, keeps a persistent belief model of what drives your reach and engagement, reconciles last cycle's beliefs against the new data, proposes ONE experiment to run next, and hands draft briefs to a drafting skill. Run it on a cadence and it compounds. Use when the user says "/linkedin-self-improvement-loop", "improve my LinkedIn", "what should I post next", "did my last experiment work", or hands over a fresh LinkedIn analytics export. Advisory by design: it proposes and drafts, a human always posts. No API keys.
---

# LinkedIn self-improvement loop

Most "content analytics" is a noun: a report you read once and forget. This is a verb.
It runs the **build-measure-learn loop** on your LinkedIn and keeps **state**, so every
cycle compounds on the last instead of starting from zero.

```
  1. MEASURE  -> 2. RECONCILE -> 3. UPDATE BELIEFS
  (ingest export)  (did last        (confidence rises if a
        ^           cycle's bet       pattern held, halves if
        |           hold up?)         it broke)
        |                                  |
  6. WAIT  <- 5. DRAFT BRIEFS <- 4. PROPOSE ONE EXPERIMENT
  (re-run next  (hand to a          (biggest effect on the
   export)       drafting skill)     least-settled belief)
```

It is **advisory**: it proposes experiments and emits draft briefs, but a human writes
and posts every post. It never touches LinkedIn directly.

## State it keeps (in `--state`, default `./state`)

| File | What |
|---|---|
| `beliefs.json` / `beliefs.md` | The model: ranked traits (topic/hook/day/length) with a confidence that updates each cycle. `.md` is git-friendly and readable. |
| `ledger.jsonl` | One line per cycle: what was reconciled, discovered, proposed. The audit trail. |
| `snapshots/<date>.json` | Parsed metrics from each export, so trends compute across exports (beats the top-50 survivorship trap over time). |

A belief is just: *"posts with this trait beat your average on the chosen metric."* It
starts at low confidence, climbs ~0.34 of the way to 1.0 each cycle it survives, and
halves when a new export contradicts it. Survive enough cycles and it's a law; break and
it's archived.

## What the user downloads (same two files every cycle)

1. **Creator analytics (required)** - `AggregateAnalytics_<name>_<dates>.xlsx`.
   LinkedIn -> profile -> **Analytics** -> **Export**. Impressions, engagements, top-50
   posts, followers, demographics. (LinkedIn caps it at the top ~50 posts / 365 days.)
2. **Data archive (optional, recommended)** - the `Complete_LinkedInDataExport` zip
   (**Settings -> Data Privacy -> Get a copy of your data -> larger archive**, email,
   ~24h). Its `Shares_*.csv` carries full post text so the loop can tag topics and hooks.

## Step 1: Locate the export

```bash
ls ~/Desktop ~/Downloads 2>/dev/null | grep -iE "AggregateAnalytics|LinkedInDataExport"
```

## Step 2: Run a cycle

```bash
cd skills/linkedin-self-improvement-loop
python loop.py \
  --analytics "/path/to/AggregateAnalytics_Name_dates.xlsx" \
  --archive   "/path/to/Complete_LinkedInDataExport_folder" \
  --state ./state \
  --metric engagements        # or impressions | er
```

`--metric` picks what the loop optimizes. `engagements` is the sane default for a personal
brand (reach is mostly downstream of engagement + the algorithm). Use `impressions` only
if pure reach is the goal, and read the ER caveat below before you do.

The loop prints its report to stdout and updates `./state`. Read the report straight back
to the user, in this order: **RECONCILE** (did last bet hold), **PROPOSE** (the one
experiment), **DRAFT BRIEFS**.

## Step 3: One-off deep snapshot (optional)

For a full one-time report (all the tables, top/bottom posts, correlations) without the
loop machinery, run the MEASURE stage directly:

```bash
python analyze.py --analytics "...xlsx" --archive "...folder" --out ./out
```

This writes a styled Excel workbook + tagged CSV. Good for handing a human a static
read; the loop is for the recurring improvement cycle.

## Step 4: Draft toward the experiment

Take the DRAFT BRIEFS and expand them into real posts. If a drafting skill exists
(e.g. `social-content`), hand it each brief's `topic` / `hook` / `post_on` and let it write
in the user's voice. Tag each post mentally with the brief's `tests` field so next cycle's
reconciliation means something. **Never auto-post** - output drafts, the human ships them.

## Step 5: Schedule the next cycle

This is what makes it a loop, not a one-off. After enough posts to measure (~2 weeks),
re-run with the next export. Offer to wire it:

```
/schedule a linkedin-self-improvement-loop run every 2 weeks
```

Each run tells the user whether the last bet paid off and picks the next one.

## Read the numbers honestly (say this every cycle)

- **Engagement rate is inversely tied to reach.** A 12k-impression post shows a lower ER%
  than a 900-impression post with equal raw engagement. The loop's default metric
  (`engagements`) sidesteps this; if you switch to `er`, know it rewards small posts.
- **Survivorship bias, fading over time.** Any single export is the top ~50 posts only. The
  loop's `snapshots/` defeat this *across* cycles, but in cycle 1 a "loss" belief just means
  "weakest of your winners," not "this bombs."
- **Small n.** Day-of-week and rare hooks can ride on 3-5 posts. The loop ignores anything
  under n=3 and shows n in every row. Treat a 1.6x effect on n=3 as a hint, not a law,
  until cycles confirm it.
- **Engagements is one blended number** (no reaction/comment/share split), and native
  image/carousel posts usually have no `MediaUrl`, so the loop can't judge media vs text.
  Don't fake a conclusion there.

## Tuning

Topic and hook detection are two regex dicts at the top of `analyze.py` (`TOPICS`, `HOOKS`),
tuned for a B2B / GTM / CRM brand. Edit for a different niche. Loop behavior (learning rate,
noise deadband, min sample size, seed confidence) is tunable at the top of `loop.py`.
