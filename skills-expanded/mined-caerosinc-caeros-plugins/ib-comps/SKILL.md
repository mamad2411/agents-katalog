---
name: ib-comps
description: Trading comparables — peer selection, multiples, and implied valuation. Uses the private-markets vault for the peer universe and the Alpha Vantage app for public financials. Use when the user asks for trading comps, peer multiples, or market-based valuation.
---

# Trading Comps

Build a trading comparables analysis: pick peers, gather metrics, compute
multiples, imply a valuation range.

## Data access

- **Peer discovery**: `analyst_vault_query` over the vault (company profiles,
  sectors, ownership, funding history) to find and qualify peers.
- **Public financials**: the Alpha Vantage app via `apps_execute_tool`
  (app=alpha_vantage) for quotes, market cap, and fundamentals of listed
  peers. If the app isn't connected, ask the user to connect it from the
  plugin page — or proceed with user-provided figures, clearly labeled.
- No invented numbers: every metric is vault data, app data, or user input.

## Workflow

1. **Understand the subject.** Business model, sector, scale, growth. Pull
   the vault profile if the company is covered.
2. **Select 5-10 peers.** Direct competitors, business-model peers, size and
   growth peers. Show the peer list with a one-line rationale each and let
   the user veto before the heavy pull.
3. **Gather metrics per peer** (Alpha Vantage): market cap, enterprise value
   inputs (debt, cash where available), revenue and EBITDA (LTM or latest
   FY — label which), growth and margin.
4. **Compute multiples**: EV/Revenue, EV/EBITDA, and P/E where meaningful.
   Show min / 25th / median / 75th / max.
5. **Imply the range** for the subject from median and quartile multiples
   against its metrics. State which metric vintages were used.
6. **Deliver** as a table plus a short read, and offer the spreadsheets
   skill for a formatted comps sheet.

## Rules

- LTM vs FY mismatches are the classic comps error — label every figure's
  period and never mix silently.
- If fewer than 4 peers have usable data, say the comp set is thin instead
  of padding it.
