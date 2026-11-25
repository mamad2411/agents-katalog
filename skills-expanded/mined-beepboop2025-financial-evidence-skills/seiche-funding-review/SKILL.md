---
name: seiche-funding-review
description: Review dollar funding conditions, repo and reserve context with Seiche's published evidence. Use for a morning funding check or money-market research question.
---

Use the Seiche MCP connection at `https://api.seiche.info/mcp`. The public endpoint needs no account or API key. If it is unavailable, report the connection failure instead of reconstructing a current reading from memory.

Start with `money_market_context` and `{"section": "summary"}`. Preserve the snapshot time, each channel's value, unit, observation date and freshness, the source freshness counts and any stale or unavailable metric. A newly generated snapshot does not make its underlying daily or weekly observations current. Keep the countercase and the desk's limits with the conclusion: a three-year rank is descriptive context, not a forecast or probability. This MCP connection does not serve Seiche's legacy stress score or forecasts while their source rights are qualified; never reconstruct them. If the user needs the repo/reserves mechanism, discover the current schema for `money_market_context` and call it with the relevant supported section.

Answer the user's funding question with the source-reported reading, what evidence is old or missing, and links to the underlying evidence when provided. Do not turn this context into an instruction to trade or infer any institution's creditworthiness from the system-wide reading.

Starter question: “Which dollar funding channel looks most stretched against its own last three years, and which underlying observations are old or missing?”

[Browser demo](https://liquilens.in/start/?task=funding) · [Source and setup](https://seiche.info/developers/)
