---
name: claude-mini-app-builder
description: A 6-step method for turning one narrow, recurring calculation into a small interactive tool (a Claude Artifact) instead of a spreadsheet or one-off answer — choose one job, define 2-4 inputs, make the math explicit and testable, write a precise one-paragraph build request, test edge cases before trusting it, and re-skin it as your own tool. Worked example: a freelance/consulting quote calculator (hours x rate + extras). Use when the user has a repeatable math-based task (a quote, an estimate, a unit conversion, a scoring rubric) and wants a reusable calculator instead of redoing the arithmetic by hand each time.
---

# Build a Mini App With Claude (6 steps)

Original content compiled from a "Build Your First Mini App With Claude"
social carousel. The steps generalize past its worked example (a freelance
quote calculator); the example is kept because it's concrete.

## Step 1 — Choose one job

Pick a single, narrow, recurring calculation — not a whole app. "Turn project
details into a quote" beats "build me a business tool."

Worked example: build a simple calculator for freelance work — hours,
hourly rate, and extras produce a total quote.

## Step 2 — Define the inputs

Give the tool exactly the fields it needs — no more. Three is a good default
ceiling for a first build (this is what keeps it a mini app, not a product):

- **Estimated hours** — your time
- **Hourly rate (USD)** — your rate
- **Extra costs (USD)** — your project costs

You choose the numbers; the tool should never invent or default them
silently.

## Step 3 — Make the math explicit

Write the formula in plain arithmetic before asking Claude to build
anything, and decide up front what it deliberately does *not* do:

```
hours × rate + extras = total
10 × $50 + $100 = $600
```

- No tax calculation (unless you add it).
- No automatic discounts (unless you add them).

Stating the exclusions is as important as the formula — it stops Claude from
"helpfully" adding tax/discount logic you didn't ask for.

## Step 4 — Copy this build request

A precise, single-paragraph request works better than an open-ended one.
Adapt the bracketed parts to your own calculation:

> Create an interactive quote calculator Artifact. Inputs: hours, hourly
> rate in USD, and extra costs. Total = hours × rate + extras. Reject blank
> or negative values. Show a clear breakdown and a Copy summary button. Use
> a clean, mobile-friendly layout. Do not add taxes or discounts.

In Claude: **Settings → Capabilities → enable Code execution and file
creation** before sending this, if those aren't already on. Describe it,
preview it, refine it — treat the first result as a draft, not a final
answer.

## Step 5 — Test it before you trust it

Run at least these three cases and check the output matches your own
mental math — don't just eyeball that it "looks right":

| Test | Inputs | Expected |
|---|---|---|
| Normal input | 10 hrs, $50/hr, $100 extra | $600 |
| Zero extras | 10 hrs, $50/hr, $0 extra | $500 |
| Missing or negative input | 10 hrs, $50/hr, −$10 extra | A clear error message, not a silent wrong number |

Ask Claude to fix anything that fails before you rely on the tool for a
real quote.

## Step 6 — Make it feel like your own tool

Once the math is verified, personalize it: your name/contact on the output,
your brand color, and a one-click "Copy summary" so the estimate is easy to
paste into an email or invoice. Review every estimate before sending it —
the tool drafts the number, it doesn't approve it.

## Reusing this pattern

The same six steps work for anything that's "a few numbers in, one number
or a short breakdown out": a shipping-cost estimator, a simple ROI/break-even
calculator, a unit converter, a scoring rubric. The discipline that
transfers is steps 2–3 (few, named inputs; explicit, bounded math) and step
5 (test before trusting) — skipping either is how a "quick calculator"
quietly returns a wrong number with confidence.

Distinct from `build-claude-ai-employee` (same account, different job): that
skill is a general 7-step method for turning any repeatable *text* task into
a reusable prompt/skill; this one is specifically about a small *interactive
calculator Artifact* with numeric inputs and a testable formula.
