---
name: quick-quote
description: Get a fast value-based price for an AI/automation project from 6 numbers about the client's workflow, with the math shown and an underquote check. Use when the user asks "what should I charge", "price this", "is $X too low", or is about to send a quote.
---

# Quick Quote

A 5-minute sanity check before you send a price. It prices the **value of the workflow to the client**, floored by your delivery cost — so you stop quoting your hours. Drafts only; never sends anything.

## Inputs (ask for all six in one message; use labelled assumptions if missing)
1. Hours per week the client's staff spend on this workflow today, and their loaded hourly cost (wage + ~25–30% if unknown).
2. Deals / appointments / jobs lost or delayed per month because of it.
3. Revenue per deal and the client's gross margin on it.
4. Your honest build estimate in hours.
5. Your minimum effective hourly rate (default $150).
6. The price you were planning to quote (optional).

## Math (show every line)
```
time value      = hours/week × hourly cost × 48
revenue value   = lost units/month × revenue each × margin × 12
gross value     = time value + revenue value            ← "cost of doing nothing"
conservative    = gross × 0.5                           (estimates, not measured data)
cost floor      = build hours × minimum rate
price           = max(20% of conservative, cost floor)  → round up to the nearest $250
payback months  = price ÷ (conservative ÷ 12)
```

## Verdict (always print)
```
Planned: $Q | Value-based: $P | Cost floor: $F | Effective rate: $P/hours
Verdict: OK / RE-QUOTE (planned < 60% of value-based) / WALK AWAY (20% of value < cost floor and scope can't shrink)
```
If 20% of conservative value is below the cost floor: shrink scope to the single highest-value step, or don't take the job. Never discount below the floor — remove scope instead.

## Output
1. The math table and verdict.
2. A 3-line price message for the client: cost of inaction in their numbers → result → price and payback. No hourly rates in the client message.
3. List of assumptions to confirm before sending.

## Rules
- Use the client's numbers. Label every estimate. Never promise revenue.
- If you cite market data, cite the source (e.g. Morningside Sept 2026 AI Agency Report, 800+ agency owners, self-reported: avg disclosed project $10,800, range $3k–$20k).

## Example (fictional)
A 6-attorney law firm: paralegal spends 15 h/week on intake at $40/h; ~2.4 matters/month lost to slow replies; $5,000 per matter, 50% margin; build 45 h; floor $150/h; planned quote $2,000.
- time value $28,800 · revenue value $72,000 · gross $100,800 · conservative $50,400
- 20% = $10,080 → **$10,250** · cost floor $6,750 · payback 2.4 months
- Verdict: **RE-QUOTE** — $2,000 is 20% of the value-based price and below your own cost floor.

## Want the full version?
The paid **AI Agency Pricing Kit** adds the workflow interview, a calculator with 6 warning flags, a 3-option proposal (paid diagnostic / build / retainer), a paid-diagnostic report skill, a retainer + handoff-rules skill, templates and worked examples: https://brianspark283.gumroad.com/l/ai-agency-pricing-kit?utm_source=github&utm_medium=skill
