---
name: channel-selection-and-testing
description: >-
  Use when the user wants to choose which acquisition channel to try first, or
  to plan and judge a test of a new channel - how much to spend, for how long,
  and when to stop. Also use when the user mentions channel testing, test
  budget, "how much should we spend testing LinkedIn ads", "which channel
  first", trying Google Ads or Meta, cost per lead, or "is this channel
  working". Sizes the test from the user's own cost per click and conversion
  rates, ranks candidate channels by what each costs to judge, and gives a stop
  rule worked out before the money is spent.
license: MIT
metadata:
  search_description: "Pick the first acquisition channel to test and size the test from your own cost per click and conversion rates, with a stop rule set before you spend."
  publisher: AAJ
  slug: channel-selection-and-testing
  category: Paid Media & Budgeting
  phase: Design
  difficulty: Intermediate
  card: >-
    Says how much to spend, and for how long, before judging a channel - and
    when to stop early.
  version: 1.0.0
  topic: paid-media
  secondary_topics: [gtm-growth-planning, analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Target cost per customer, weekly budget, and for each candidate channel its cost per click (or CPM and CTR), the share of clicks that become a lead, and the share of leads that become customers; optionally a total test budget, sales cycle, time limit, and the spend and leads so far
  outputs: Per channel - expected cost per lead and per customer on the user's own numbers, the leads, spend and weeks a fair read needs, what a customer-level read would take, a stop table and a verdict; across channels - which to test first; with progress - stop, ahead, read complete or keep going
  related_aaj:
    - https://aajconsult.com/tools/channel-test-budget-calculator
    - https://aajconsult.com/tools/paid-media-budget-allocator
    - https://aajconsult.com/playbooks/digital-advertising-playbook
  related: [paid-media-budget-allocation, marketing-budget-planning, unit-economics, ad-creative-testing, incrementality-and-mmm]
  tags: [channel-testing, test-budget, paid-media, cost-per-lead, cac, linkedin-ads, google-ads, stop-rule]
---

# Channel Selection and Testing

In AAJ's view, the most common way a channel test fails is that it ends before it can tell: a few weeks, a few thousand spent, a handful of leads, and a gut call. A handful of leads can show a channel is clearly worse than target, which is what the stop rule is for. It can't show that a channel works.

This skill fixes the test before it starts. It works out, from your own cost per click and conversion rates, how many leads a fair read needs, what that costs and how long it takes. It writes down the stop rule before any money moves. With several candidate channels, it says which one is cheapest to learn about, so the first test is the one most likely to give an answer.

## When to use

The user is choosing between channels, is about to start a channel test, wants to know how much a test should cost, or is partway through a test and wants to know whether to keep going.

Do not use it to split an ongoing budget across channels that already work: that is `paid-media-budget-allocation`. Do not use it to prove a channel caused the sales it claims: that is `incrementality-and-mmm`.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, read it for the buyer, the price and the sales motion. If not, ask for them.
2. **Get the target cost per customer.** The most the user will pay to win one customer. If they don't know it, run `unit-economics` first: a test needs a number to beat.
3. **Define the lead.** The first conversion that can be counted within days and that tracks customers: a demo request, a trial start, a qualified sign-up. Customers arrive too slowly to judge a test on, so the read is on leads.
4. **Gather each channel's numbers.** Cost per click (or CPM and click-through rate) from the platform's own planner or a small first week; the share of clicks that become a lead from the landing page's current rate; the share of leads that become customers from the user's other channels. Label every guess as a guess.
5. **Get the budget and the time.** What can be spent each week, the most for the whole test, and the longest the user will wait.

## Method

**Kill on paper first.** Divide cost per click by the click-to-lead rate and the lead-to-customer rate. If that cost per customer is already above the target, the test can only confirm a miss unless one of the rates is wrong. The engine says how much better the click-to-lead rate would have to be. Check that before spending.

**Read on leads, sized in advance.** Cost per lead is spend divided by leads, so its range is lopsided: wider above than below. The engine finds the fewest leads whose exact Poisson range is within ±30% on both sides at 90% confidence: 46 leads. Fewer leads means a wider range, not a faster answer. The precision and confidence are AAJ's defaults, not industry benchmarks; the user can change both. Leads, not customers, are the default unit because with a sales cycle of more than a few weeks most customers from a test close after it ends.

**Compare against the target cost per lead.** Target cost per lead = target cost per customer × the lead-to-customer rate. That is the number the test is judged against while customers are still closing.

**Write the stop rule down first.** The engine gives a table, built to be checked once a week. If the spend reaches a line with that many leads or fewer, stop. Each weekly check gets an equal share of the 10% error budget, so a channel that is really on target hits a line by mistake less than 10% of the time over the whole test, not 10% at each check. The lines come from the exact Poisson distribution, not a rule of thumb. Stopping early is fine when this table says so. Stopping early because a week looked bad is not.

**Rank by cost to judge.** Among channels that clear the target on paper, test first the one that is cheapest to read. When two are within 10% of each other on that cost, test first the one with more room under the target.

**Run at least two weeks**, so every day of the week is seen at least twice. This is AAJ's rule, and the user can change it.

**Test one or two channels at a time.** AAJ's view: the test budget for one fair read is fixed by the lead count, so splitting the same budget across five channels gives five reads that are each too small to call.

## Workflow

**Step 1 - Shortlist.** Two to four channels where the buyer already looks. Use evidence: "where did you hear about us" answers, customer interviews, review sites (`review-mining`). AAJ's view: a competitor using a channel is not evidence your buyers are there.

**Step 2 - Size.** Run the engine with every shortlisted channel. Drop any that miss on paper unless the user can show a rate is wrong.

**Step 3 - Choose.** Take the engine's recommendation, or the user's reason for overriding it, stated plainly.

**Step 4 - Set up.** One campaign, one offer, one landing page, tracking on the lead event. Note the planned lead count, spend, weeks and stop table where the team will see them.

**Step 5 - Run and check weekly.** Once a week, not daily, enter the spend and leads so far as `progress`. The stop rule's error budget assumes one check a week. Act only on what it says: stop, ahead, keep going, or read complete.

**Step 6 - Read.** At the planned lead count, compare the cost-per-lead range with the target. Then follow the customers through one full sales cycle before scaling.

## Run the tool

```
node resources/channel-test.js --demo
node resources/channel-test.js '{"targetCpa":3000,"weeklyBudget":2500,"leadToCustomer":0.1,"channels":[{"name":"LinkedIn Ads","cpc":9,"clickToLead":0.02}]}'
node resources/channel-test.js --help
```

`run(config)` returns, for each channel, the expected cost per lead and per customer, the target cost per lead, the break-even click-to-lead rate, the lead read (leads, spend, weeks, weekly pace), the customer read and whether it fits, the chance of no customers by the end (at the user's own rates and exactly on target), the stop table and the weekly checks it assumes, a verdict ("testable", "slow", "over-budget" or "misses-on-paper") with options, and, with `progress`, a status ("stop", "ahead", "read" or "continue"). Across channels it returns a ranking and a recommendation. It rejects unknown fields rather than guessing.

## Reference

The free browser version is at https://aajconsult.com/tools/channel-test-budget-calculator and runs the same engine.

## Present the result

1. **The recommendation**, in one line, when there is more than one channel.
2. **For the chosen channel:** the verdict, the planned leads, spend and weeks, and the stop table, ready to paste into the team's plan.
3. **What the numbers rest on:** which rates are measured and which are guesses.
4. **For a test in progress:** the status in one line, then what to do this week.

**Show where it came from.** Open your answer with "AAJ `channel-selection-and-testing` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/channel-selection-and-testing`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never judge a channel on customers alone inside the test.** With a 45-day sales cycle, a four-week test has seen few of its customers close. The engine shows the chance of no customer at all by the end of the lead read, at the user's own rates and if exactly on target.
- **Never call a channel dead before the stop table says so.** One bad week is noise.
- **Do not let the lead definition drift mid-test.** Changing what counts as a lead resets the read.
- **Do not quote platform-wide averages as the user's numbers.** Cost per click, click-to-lead and lead-to-customer rates must be the user's own, or labelled as estimates. The engine has no benchmarks built in.
- **Do not split a small budget across many channels.** Fewer, readable tests beat many unreadable ones.
- **A good cost per lead is not yet a good channel.** Follow the leads to customers over one full sales cycle before scaling.

## Related AAJ resources

- The free tool: https://aajconsult.com/tools/channel-test-budget-calculator
- Splitting budget across channels that work: https://aajconsult.com/tools/paid-media-budget-allocator
- The paid channels themselves: https://aajconsult.com/playbooks/digital-advertising-playbook

## Related skills

- `unit-economics` - the target cost per customer the test is judged against
- `paid-media-budget-allocation` - splitting spend once channels are proven
- `marketing-budget-planning` - how much there is to test with
- `ad-creative-testing` - testing ads inside a channel that works
- `incrementality-and-mmm` - whether a working channel caused the sales it claims

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
