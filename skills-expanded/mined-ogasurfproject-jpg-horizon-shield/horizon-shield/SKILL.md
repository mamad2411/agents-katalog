---
name: horizon-shield
description: Audit whether a Japanese construction or renovation estimate is fair. Use when the user shares a construction or renovation quote, asks whether a price for work like exterior painting (外壁塗装), roof work, a bathroom remodel or a water heater is reasonable, asks 相場 / 適正価格 / この見積もりは高いか, wants overcharge red flags checked in an estimate or sales pitch, or wants an independently verifiable fair-price receipt. Also use for public construction-cost data for Japan and the U.S. (labor rates, unit prices, prevailing wages, permits, area factors). Uses the horizon-shield and construction-cost-data MCP tools.
---

# HORIZON SHIELD

You have the `horizon-shield` MCP server for fair-price checks and the `construction-cost-data` MCP server for the underlying cost data. It checks Japanese construction and renovation estimates against the open JCCDB dataset (v5.1: 526,128 records, 95,403 line items and 430,725 source-cited observations, CC BY 4.0) and returns fair-price references that anyone can recompute. No API key.

When a user asks whether a Japanese quote is fair:

1. No quote yet, only "what should this cost": `get_price_range` (pass `region` as a prefecture or city to apply the regional multiplier; the base value comes back too).
2. A specific quoted amount: `audit_estimate` with the work name and the price in JPY. It returns a verdict (ok, watch, alert), the fair range and the gap from the average. When candidates disagree it returns ambiguous instead of a verdict; say so rather than picking one.
3. Suspicious wording (一式 lump sum, today-only discount, free inspection, door-to-door): `check_red_flags`.
4. The user wants proof they can check themselves: `verify_fair_price`. It records the fair price with a SHA-256 hash and returns a `verify_url` where anyone recomputes it. This call appends a record to a public ledger, so tell the user before calling it.
5. The user asks who to hire: use the `find-contractor` skill.

Every price answer carries `provenance` (dataset version, sources) and `next_calls` (the next tool with its arguments filled). Follow `next_calls` rather than guessing arguments.

Construction cost data is on the second server, `construction-cost-data` (read only). For JCCDB detail use `search_jccdb_items`, `get_jccdb_observations`, `get_jccdb_labor_rate`, `compare_jccdb_regions`, `get_jccdb_work_unit_price`, `get_jccdb_index_series`, and `get_jccdb_coverage` to see what exists before answering. For the United States (USCCDB) use `get_us_construction_prices`, `get_us_prevailing_wage`, `get_us_permits`, `get_us_area_factor`, and for distribution-chain estimates `get_us_price_chain`, `get_us_import_landed_cost`, `get_us_trade_margins`, `get_us_contract_discounts`. Values the service computed are marked `computed: true`; public-works unit prices and statistics are reference data, not renovation quotes.

Rules:
- Fair-price verdicts are for Japan only, in JPY. Work names match best in Japanese; English names and romaji places are mapped and the mapping is disclosed as `normalized_from`.
- Report a concern with its numeric basis and a concrete next step. Flag, do not accuse: the result is for the homeowner to act on, it does not declare a contractor dishonest.
- Never invent a price. If an item is not covered, say so.
- Cite the source: JCCDB (curated by Toshikatsu Oga, thirty years in construction) and the provenance the tool returned.
- Two tools write: `verify_fair_price` and `create_ap2_fairness_attestation` append to the public ledger. Everything else reads.
