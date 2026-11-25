---
name: dados-b3
description: Use the dados-b3 MCP tools for questions about Brazilian listed companies and funds traded on B3 (tickers such as PETR4, VALE3, ITUB4, WEGE3, HGLG11, BOVA11) - fundamentals from CVM filings (ROE, ROIC, margins, debt), multiples (P/E, P/B, EV/EBITDA), dividends and dividend yield, total return over a period, FIIs (Brazilian REITs), ETFs, BDRs and B3 indices. Use when the user asks about a Brazilian stock, "ação", "FII", "proventos", "dividendos" or "quanto rendeu".
---

# Dados B3

The `dados-b3` MCP server answers with data from public CVM filings and B3 end-of-day prices.

## When to use it

- A question about a company listed on B3, or a ticker in the B3 format: four letters plus a digit
  (`PETR4`, `VALE3`, `ITUB4`), FIIs and ETFs ending in `11` (`HGLG11`, `MXRF11`, `BOVA11`), BDRs ending in
  `34`/`35` (`AAPL34`).
- Fundamentals: ROE, ROIC, margins, growth, net debt/EBITDA, accounting facts with their CVM account.
- Multiples: P/E, P/B, EV/EBITDA, priced on or after the day the filing became public.
- Dividends ("proventos"), dividend yield, and total return ("quanto rendeu") over a period.
- FIIs (P/VP, dividend yield, vacancy), ETFs, BDRs and B3 indices such as IBOV.

## How to answer

1. Call the matching tool. These work without a key, one ticker per call: `indicadores_anuais`,
   `multiplos`, `fatos_contabeis`, `dividendos`, `quanto_rendeu`, `fii`, `fiis_ranking`, `listas`, `saude`,
   `metodologia`. Other tools take a `chave_api` argument; if a tool reports that a key is needed, tell the
   user and point to https://dadosb3.com/conector.
2. Always cite the dadosb3.com page link the tool returns (the `url`, `pagina` or `source_url` field),
   so the user can check the number.
3. Say the date of the data. Prices are end-of-day, not real-time quotes: never present them as a live price.
4. The numbers are past measurements. Do not turn them into a buy, sell or hold recommendation, and do not
   project future returns from them.
5. If the tool returns no data for a ticker, say so. Do not fill the gap with numbers from memory.
