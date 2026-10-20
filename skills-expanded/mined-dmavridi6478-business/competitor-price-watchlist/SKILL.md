---
name: competitor-price-watchlist
description: Repeatable weekly competitor price/offer/positioning watchlist — define the tracking template for a niche, run a weekly brief that flags only meaningful changes with source, date, exact evidence and an UNVERIFIED label, then second-pass, verify, and optionally productise as a competitor-intelligence brief. Source is a 9-slide "AI Playbook 14/21" carousel. Use for pricing intelligence, competitor monitoring, or building a monitoring side-service. Run via /price-watchlist.
---

# Competitor Price Watchlist with AI

Core idea from the source: *"Know what changed. Know when it changed."* The point is not to "use AI" — it is to remove the bottleneck that manual checking is easy to forget. **Treat AI output as a research aid, not as proof.** Simple rule: **AI drafts the work. You approve the work.**

## Setup (3 things)

1. Pick the AI (Claude or ChatGPT — use the one you know).
2. Prepare the input: an AI tool with current web access + a spreadsheet or Notion database. Verify important figures on the original source.
3. Keep a human in the loop: check facts, claims, tone and sensitive information before using the output.

## Step 1 — Define the watchlist (exact prompt)

```
Create a competitor monitoring template for [NICHE]. Track:
• product/service
• current public price
• offer/bundle
• positioning/message
• notable promotion
• source URL
• date checked

Tell me what should be verified manually before sharing the report.
```

Store the resulting template as a Notion database or sheet (columns above + `previous value`, `change flag`, `verified?`).

## Step 2 — Run the weekly brief (exact prompt)

```
Research these public competitors: [NAMES/URLS].

Compare this week with the previous record if supplied. Flag only meaningful changes. For each change give source, date, exact evidence and why it might matter. If you cannot verify a change, say "UNVERIFIED".
```

Attach last week's record. Read the output before you use it.

## Step 3 — Second pass ("don't copy the first answer")

- Ask for **assumptions**: what did the AI have to guess?
- Ask for **gaps**: what information would improve the answer?
- Ask for a **better version**: "Make this more practical for [AUDIENCE]."
- **Verify**: facts, prices, policies, quotes, statistics — on the original page.

## Checklist you'll actually use

1. **Input** — give real context, audience and constraints.
2. **Prompt** — ask for a concrete output, not "help me with this".
3. **Improve** — find assumptions, gaps, weak spots.
4. **Verify** — check anything important before publishing, sending or selling.
5. **Apply** — the value is what you do with the output.

## Monetisation angle (from the source, with a caveat)

Sell the **outcome**, not prompting: a weekly or monthly competitor-intelligence brief to small businesses without a research team — value = consistency + verification + interpretation. Don't sell "I know how to prompt AI"; sell a specific result for a specific customer type, with a clear scope and human quality control. *Caveat:* the source gives no revenue data; treat pricing/demand as a hypothesis to test with 3 paying pilots before building anything.

## Automation option

Once the brief is stable, schedule it (`/loop`, `/schedule`, or a Zapier/Notion automation) to run weekly and post to Slack/Notion — see `scheduled-routine`, `automation-blueprint`. Keep the human verification step.

## Legal/ethical guardrails

Only public pages; respect robots.txt and terms; no login-gated scraping; cite sources; never present unverified changes as fact.

Pair with: `competitor-profiling`, `competitor-benchmark-scorecard`, `pricing`, `source-verification` (docs/procedures), `client-research-web`.
