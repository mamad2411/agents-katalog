---
name: upsell-potential-scout
description: >
  Find upsell and cross-sell headroom in EXISTING clients by comparing what they spend with
  you against their financial capacity. Use whenever the user says "upsell", "cross-sell",
  "potenziale di upsell", "wallet share", "quanto potrebbe spendere ancora [cliente]", "su
  quali clienti posso crescere", "dove ho margine di crescita sui clienti", "espandere gli
  account esistenti", "upsell potential [client]", "how much more could [client] spend",
  "where's the headroom in my book", "expansion opportunities in my accounts", "grow my
  accounts", or asks which current clients are under-penetrated. Outputs a wallet-share
  ranking with expansion rationale. Not for finding new prospects (use prospects-scout) or
  ranking a list of prospects (use priority-ranker).
metadata:
  version: "1.0.0"
---

# Upsell Potential Scout

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`). Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill.

Quantify how much room each existing client has to spend more with you.

## Read your context first
Read the commercial context (core §3): spend hook + capture rate, and the current deal value per client. Current deal values come from the saved portfolio, a CRM connector if one is available, or an uploaded spreadsheet/CSV. The saved typical deal size is not a per-client value, so never use it as one. If no deal values are available anywhere, say so once and offer to run capacity-only sizing (spend capacity without wallet share). If a needed field is missing, ask once and offer to save it.

## Steps
For each client (or the one named):
1. **Current spend with you** — from the portfolio / CRM / uploaded file. Use the annual value, so it compares with the annual spend-hook line.
2. **Financial capacity** - resolve the client, then read the spend-hook cost line and overall health (growth, liquidity, profit) with a specific metric read; for several clients at once, batch them in the many-company comparison, for one fiscal year (the latest most of them have filed, unless the chain already fixed one). The spend-hook cost line is not in the financial analysis, so the full analysis adds nothing here.
3. **Wallet share** = current deal value ÷ spend-hook metric. Low share + healthy finances = headroom. High share = near saturation (defend, don't push).
4. **Headroom (€)** = (spend-hook metric × capture rate) − current deal value. At or below zero the account is saturated: show it as saturated, not as a negative amount.
5. **Compatible lines not yet sold** — compare what similar portfolio clients buy vs what this client buys; surface the gap as a concrete upsell suggestion. This needs the portfolio, CRM or file to say which lines each client buys; without that, leave the column empty rather than guess.
6. **Health check** — flag any client whose finances are deteriorating (renewal/credit risk), even if wallet share looks low.

## Output
Per core §5, the full ranking is a file and the chat carries a digest. The ranking orders clients by upsell potential (headroom €, descending) with columns: client, current deal value, spend-hook line, wallet share %, estimated headroom, suggested next line, and a one-line rationale. The chat digest: total identified headroom across the book (healthy accounts with positive headroom only), the top 3 expansion targets, and a table of the top of the ranking with the same columns; say which fiscal year and statement basis the figures use. Flag at-risk accounts in a separate note. Offer the ranking also as a spreadsheet, with your client's spreadsheet capability.

## Guardrails
Wallet share without a health read is misleading — always pair headroom with the client's financial trajectory. Never recommend pushing a client showing distress signals; flag for retention instead. Rationale mandatory on every row.
