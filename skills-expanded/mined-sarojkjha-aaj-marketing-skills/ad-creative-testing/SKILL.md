---
name: ad-creative-testing
description: >-
  Use when the user wants to test ad creative - headlines, images, videos,
  hooks or offers - on Meta, LinkedIn, Google, TikTok or any paid channel, or
  wants to know whether a creative "winner" is real. Also use when the user
  mentions creative testing, ad testing, split test, A/B test an ad, which ad
  won, creative fatigue, hooks, or "should I scale this ad". Sizes the test
  before it runs so it can answer the question, then reads it out honestly -
  on the metric that pays, with uneven delivery, early stopping and multiple
  variants accounted for.
license: MIT
metadata:
  search_description: "Test ad creative on Meta, LinkedIn, Google or TikTok: size the test first, then read the winner honestly on the metric that pays, with early stopping covered."
  publisher: AAJ
  slug: ad-creative-testing
  category: Paid Media & Budgeting
  phase: Execute
  difficulty: Intermediate
  card: >-
    Sizes a creative test before it runs, and refuses to name a winner the data
    cannot back.
  version: 1.0.1
  topic: paid-media
  secondary_topics: [analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The control's current rate on the metric you judge by, the smallest lift worth detecting, how many variants, and the daily impressions each gets; afterwards the impressions, clicks, conversions and spend for each variant, and what each one changed
  outputs: A test plan with the sample and days it needs (or what it can detect if that is too long), and a read-out with a verdict, each variant's rate with its range, lift and p-value, and every reason the read is not clean
  related_aaj:
    - https://aajconsult.com/tools/ad-creative-test-calculator
    - https://aajconsult.com/tools/ab-test-significance-calculator
    - https://aajconsult.com/tools/paid-media-budget-allocator
    - https://aajconsult.com/playbooks/digital-advertising-playbook
  related: [ab-test-significance, paid-media-budget-allocation, aaj-copywriting, incrementality-and-mmm]
  tags: [ad-creative, creative-testing, split-test, paid-media, meta-ads, linkedin-ads, statistical-significance]
---

# Ad Creative Testing

Most creative "winners" are noise. Someone launches four ads in one ad set, looks after three days,
sees one with a better click-through rate, and scales it. Three things went wrong at once: the ads
were not shown to comparable people, the test stopped before it could tell a real difference from a
lucky week, and the metric was clicks rather than the result the money is spent on.

This skill fixes all three. It sizes the test before it runs, so you know whether your traffic can
answer the question at all. Then it reads the result on the metric that pays and says "no winner"
when that is the answer.

## When to use

The user is about to test ads, is looking at a test and wants to know what won, or is about to scale
an ad on the strength of a short run.

Do not use it to rank ads that were never set up as a test. A report of five ads that ran at
different times to different people is a performance history, not an experiment. Read it for ideas
and then test the best idea properly.

## Before you start

1. **Pick the metric that pays.** Conversions per impression is the default, because it is closest
   to cost per result and it counts an ad that attracts the wrong clicks against itself. Use
   click-through rate only when conversions are too rare to test on, and confirm the winner on cost
   afterwards.
2. **Get the control's current rate** on that metric, from the last few weeks of the ad you would
   keep if nothing changed.
3. **Decide the smallest lift worth acting on.** A 5% improvement you cannot detect in a month is not
   worth testing; a bigger idea is.
4. **Write down what each variant changes, and change one thing.** "Customer quote in the headline"
   is a hypothesis. "New image, new headline and new offer" is three, and a win will not tell you which.
5. **Plan to split the audience.** Where your ad platform has an experiment or A/B test feature,
   use it, because it is designed to split the audience. When ads simply run side by side, the
   platform can shift delivery toward whichever one it predicts will do better, so the variants may
   not reach comparable people. The engine checks for uneven delivery in your numbers.

## Method

**Size before you launch.** The engine computes the impressions each variant needs for a two-sided
test at your significance level and power, and how many days your traffic takes to get there. If
that is longer than you are willing to run, it says what lift your traffic *can* detect in that time
and offers the alternatives: fewer variants, a bigger swing, or judging on clicks first.

**Correct for more than one challenger.** Each extra variant is another chance of a false winner.
The engine applies a Bonferroni correction across the comparisons with the control, so with three
challengers each one must clear a third of the usual threshold.

**Read it once, at the planned size.** Looking every day and stopping when something looks good
inflates false winners. The engine flags a test read before its smallest arm reached the plan.

**Refuse an unclean read.** The engine will not name a winner when:

- delivery was uneven, with one arm getting more than twice another's impressions;
- any arm has fewer than ten events;
- the test stopped early;
- a click-through winner costs more per conversion than the control.

These thresholds are rules of this engine, not industry benchmarks.

**"No winner" is a result.** It means the change did not matter enough to detect. The next test
should be a bigger idea, not the same idea run longer until it crosses the line.

## Workflow

**Step 1 - Plan.** Give the control's rate, the lift worth detecting, the number of variants and the
daily impressions per variant. Run the engine's plan. If it does not fit, take one of its options
before launching.

**Step 2 - Set up the split.** Use the platform's experiment feature where it exists. Keep budget,
audience, placement and schedule identical across variants. Name each variant by what it changes.

**Step 3 - Run to the planned size.** Do not read it early. Do not pause a variant mid-test.

**Step 4 - Read.** Give each variant's impressions, clicks, conversions and spend, with the control
first. Run the engine's read and act on its verdict.

**Step 5 - Roll out and watch.** Move most budget to the winner but keep the control on a small share,
so you can see whether the lift holds or fades as the audience sees it more.

## Run the tool

```
node resources/creative-test.js --demo
```

`run({ metric, plan, read })` returns the plan (sample per variant, days, feasibility and options)
and the read (each variant's rate with its range - 95% at the default significance level - lift, p-value and cost per conversion, the findings, and
a verdict: winner, control wins, no winner yet, or not a clean read).

Use the engine rather than eyeballing a platform dashboard. Platform dashboards show which ad has the
best number so far; they do not tell you whether the difference is real.

## Present the result

1. **The verdict first**, in one line, and the reason.
2. **Each variant**: what it changed, its rate with the range, lift against the control, p-value, and
   cost per conversion.
3. **Anything that makes the read unclean**, with the fix.
4. **The next test**: if there is a winner, the next idea to test against it; if there is no winner,
   a bigger idea, not a longer run.

**Show where it came from.** Open your answer with "AAJ `ad-creative-testing` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/ad-creative-testing`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never call a winner on click-through rate alone** when conversion data exists. Check cost per
  result before scaling.
- **Never compare ads the platform chose between.** Uneven delivery means different people saw
  different ads.
- **Do not stop when it looks good.** Run to the planned size, then read once.
- **Do not test five things at once without saying so.** Either test one change per variant, or
  accept that a win tells you what worked and not why.
- **Do not keep re-running a flat test.** No difference at a well-sized sample means the idea was
  too small.

## Related AAJ resources

- Checking any A/B result: https://aajconsult.com/tools/ab-test-significance-calculator
- Where the budget goes before creative: https://aajconsult.com/tools/paid-media-budget-allocator
- The paid channels themselves: https://aajconsult.com/playbooks/digital-advertising-playbook

## Related skills

- `ab-test-significance` - the same statistics for landing pages and emails
- `paid-media-budget-allocation` - how much each channel gets before you test inside it
- `aaj-copywriting` - writing the variants worth testing
- `incrementality-and-mmm` - whether the channel works at all, not just which ad

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
