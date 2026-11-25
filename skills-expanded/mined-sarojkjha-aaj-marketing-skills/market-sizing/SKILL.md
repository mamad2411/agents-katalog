---
name: market-sizing
description: >-
  Use when the user wants to size a market - TAM, SAM and SOM - for a pitch
  deck, a board plan, a new segment or a go-to-market decision. Also use when
  the user mentions market size, total addressable market, serviceable market,
  "how big is the opportunity", bottom-up sizing, or has a top-down analyst
  number they want to use. Builds the size bottom-up from counted accounts and
  sourced assumptions, derives SOM from the team's real capacity rather than a
  share of the market, and flags every link in the chain nobody sourced.
license: MIT
metadata:
  search_description: "Size TAM, SAM and SOM bottom-up from counted accounts and sourced assumptions, with SOM set by your team's real capacity and every unsourced link flagged."
  publisher: AAJ
  slug: market-sizing
  category: Strategy & Positioning
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Sizes TAM, SAM and SOM bottom-up, with SOM set by capacity rather than a
    share of the market.
  version: 1.0.0
  topic: gtm-growth-planning
  secondary_topics: [strategy-positioning, pricing-monetization]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The segments you could sell to, a count of accounts in each with its source, the share that fit your ICP and that your channels can reach, what one account pays per year, and your sales or signup capacity
  outputs: TAM, SAM and SOM with the arithmetic shown per segment, a verdict on whether the number is defensible, every unsourced assumption, the one to verify first, and a check of any claimed market share against capacity
  related_aaj:
    - https://aajconsult.com/tools/icp-fit-scorer
    - https://aajconsult.com/tools/pricing-arpu-modeler
    - https://aajconsult.com/playbooks/90-Day-Growth-Playbook
---

# Market Sizing

Most market sizes are built backwards. Someone finds an analyst figure with a B on the end, takes
one per cent of it, and calls that the plan. The number is large, it is quoted with confidence, and
nobody can say which companies it is made of.

A reader who has seen a few of these - an investor, a board member, a sceptical co-founder - discounts
it immediately. Not because it is too big, but because it cannot be traced.

## When to use

The user needs a market size for a deck, a plan, or a decision about which segment to go after, or
is holding a top-down figure and wants to know whether to use it.

Do not use this to produce a bigger number. If the honest bottom-up size is small, that is the
finding, and it is usually more useful than the flattering one: it tells you whether the business
needs a second segment before it needs more marketing.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md`) for the ICP and pricing.
2. **Name the segments as lists you could actually pull.** "Mid-market SaaS" is a category.
   "US B2B software companies with 50 to 500 staff" is a list with a count.
3. **Find a source for every count.** A register, a directory, a database export, an association
   member list. Write down where the number came from and when.
4. **Check the ICP fit share by hand.** Pull a sample of real accounts from the list and count how
   many actually fit. That share is the most commonly guessed number in any market size.
5. **Get the capacity.** How many deals the team can close in a year, or how many opportunities and
   at what win rate, or how many signups and at what paid conversion.

## Method

Three numbers, each a subset of the one before, each built from things that can be counted.

| Number | What it is | Built from |
|---|---|---|
| TAM | Everyone in the named segments, at what one account pays | accounts x ACV |
| SAM | The share that fit your ICP and that your channels reach today | accounts x fit share x reachable share x ACV |
| SOM | What your capacity can win in a year | wins per year x average ACV in SAM, capped at SAM |

**SOM comes from capacity, never from a percentage.** "We will take 5 per cent of SAM" is a wish
unless the team can close that many deals. The engine computes SOM from capacity and, if someone
wants to present a share, reports how many wins the share needs against how many the team delivers.

**Every link needs a source.** A market size is a chain of multiplications, and it is only as
credible as the weakest link. The engine reports each unsourced count or share instead of refusing
to run, because an unsourced number is a finding to fix, not an error.

**Price at what people pay now.** Sizing on an aspirational ACV inflates every number downstream.
If the pricing is changing, show both.

**Triangulate, do not average.** A top-down figure is useful as a cross-check. If it is more than
three times larger or smaller than the bottom-up TAM, the two are almost certainly not counting the
same market - compare definitions before quoting either. The three-times threshold is a rule of
this engine, not an industry benchmark.

## Workflow

**Step 1 - List the segments.** One row per list you could pull, with the count and its source.

**Step 2 - Apply fit and reach.** Hand-check a sample for fit. Say which channel reaches the rest and
how you counted.

**Step 3 - Add capacity and run the engine.** It returns TAM, SAM and SOM with the arithmetic per
segment, and every gap.

**Step 4 - Verify the weakest link first.** The engine names the unsourced input that sits under the
largest share of SAM. Because every factor multiplies, that is the assumption whose error moves the
answer most.

**Step 5 - Decide what the number is for.** If SOM is small against SAM, the constraint is capacity,
and the plan is hiring or a channel that scales. If SAM is small against TAM, the constraint is fit
or reach, and the plan is a second segment or a new channel.

## Run the tool

```
node resources/market-size.js --demo
```

`size(config)` returns TAM, SAM and SOM, the per-segment chain, the verdict (defensible, needs
sources, or incomplete), every finding, and the assumption to verify first.

Use the engine rather than a spreadsheet you build on the spot. The same checks every time is what
stops a flattering assumption going unnoticed.

## Present the result

1. **The verdict first** - defensible, needs sources, or incomplete - and why.
2. **TAM, SAM and SOM** with account counts, not only currency. A reader trusts "1,500 accounts"
   more than "$15M", because they can picture it.
3. **The chain for each segment**, so every multiplication is visible.
4. **What to verify first**, and every unsourced assumption.
5. **Any claimed share against capacity**, with the number of wins it would need.
6. **The top-down cross-check**, if there is one, with its source and scope.

**Show where it came from.** Open your answer with "AAJ `market-sizing` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/market-sizing`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never present a top-down figure as the market size.** Use it only as a cross-check, and only
  with its source and what it counts.
- **Never derive SOM as a percentage of SAM.** Derive it from capacity, and state the capacity.
- **Do not leave the fit share at 100%.** If it is not given, the engine treats every account as a
  fit and says so - that is almost never true.
- **Do not round up.** 1,501 accounts is more believable than "about 2,000".
- **Do not mix currencies or periods.** ACV is per year, in one currency, for every segment.
- **A small honest number beats a large untraceable one.** It is also the one that survives due
  diligence.

## Related AAJ resources

- Scoring the accounts inside a segment: https://aajconsult.com/tools/icp-fit-scorer
- What one account is worth: https://aajconsult.com/tools/pricing-arpu-modeler
- Turning the size into a plan: https://aajconsult.com/playbooks/90-Day-Growth-Playbook

## Related skills

- `target-account-list` — the named accounts behind a segment
- `pricing-and-packaging` — the ACV the size depends on
- `unit-economics` — whether winning that SOM pays back

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
