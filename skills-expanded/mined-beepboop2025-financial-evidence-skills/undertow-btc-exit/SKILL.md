---
name: undertow-btc-exit
description: Inspect position-sized BTC exit-cost estimates and venue depth with Undertow. Use when a user asks what exiting a dollar-sized BTC position might cost.
---

Use Undertow at `https://api.seiche.info/undertow/mcp`; public research requires no account, exchange key or wallet. For “what would exiting $100,000 of BTC cost?”, call `exit_cost` with `{"size_usd":100000}`. Use the user's requested dollar amount for other sizes; ask for the size only when it is needed and absent.

Report `requested_size_usd`, `published_rung_used_usd`, `generated_at`, venue estimates in basis points, and `unable_at_observed_depth`. Published rungs approximate the requested size; never silently call a nearest-rung estimate an exact-size book walk. Inspect the clock before describing the estimate as current. Discover and use `crypto_exit_check` when the user needs its explicit freshness assessment or comparison across sizes.

The current public exit model interpolates from published depth bands. Its costs are estimates, not executable quotes, guaranteed fills, or confirmed all-in costs including fees. Keep the method and absent venues visible. Do not infer that a venue is safe, choose a venue on the user's behalf, or place an order.

Starter question: “Estimate a $100,000 BTC exit across the covered venues. Show the snapshot time, rung used, missing depth and estimation limits.”

[Browser demo](https://liquilens.in/start/?task=exit) · [Source and setup](https://liquilens-undertow.com/developers/)
