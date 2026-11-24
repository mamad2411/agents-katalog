---
name: financetoolkit-mcp
description: "Analisis keuangan/saham via MCP financetoolkit (28 tool: valuasi, rasio, momentum, likuiditas) + library Python. | EN: stock finance analysis ratio valuation portfolio fundamental yfinance"
version: 1.0.0
category: data-science-kaggle
lang: id
---

# FinanceToolkit — Analisis Saham/Keuangan

## Akses
- **MCP** (tool-call): `pow mcp on financetoolkit` → restart → 28 tool
  (efficiency, profitability, valuation, momentum, liquidity, solvency, dll)
- **Python lib**: `from financetoolkit import Stock` — di venv uv `financetoolkit`
  (`~/.local/share/uv/tools/financetoolkit/.../site-packages`)
- Data harga: yfinance (perlu `pip install yfinance` di env yang dipakai)

## Contoh
- `Stock('AAPL').historical_data` · `.ratios` · `.news` · `.insider_transactions`
- Screening: `get_base` universe → filter rasio/momentum
- Alternatif data pasar ID: `data-hub search "saham"` / dataset indeks.
