---
name: supply-chain-ticker-mapper
description: Use whenever the user shares an industry analysis, supply-chain breakdown, technology trend article, or bottleneck/component report (e.g. NVIDIA AI servers, semiconductors, EVs, batteries, LLM AI) and wants to know WHICH COMPANIES are relevant and WHAT THEIR STOCK TICKERS are. Trigger on phrases like "find relevant companies and tickers", "which stocks benefit from this", "map this to tickers", "supply chain stocks", "誰是相關供應商", "股票代號", or any request to turn technologies/components/bottlenecks into an investable company list. For each category in the source material, researches and lists up to the top ~5 public companies per country (Taiwan TWSE/TPEx, US NASDAQ/NYSE, Japan TSE, Korea KRX, China HKEX/SSE/SZSE first, then others), producing a table with company name, ticker, exchange, and rationale, grouped by category then market. Does NOT fetch live prices; identification/mapping only (use stock-analysis or yfinance for valuation).
---

# Supply Chain → Company → Ticker Mapper

Turns a technology/industry/bottleneck writeup into a structured, sourced table of relevant publicly-traded companies and their stock tickers, organized by category.

## When to use this

The user wants to identify **which public companies play in a given technology/industry/supply chain**, with correct ticker + exchange. Works in two modes:

- **Document mode**: user has pasted or referenced content describing a technology stack, supply chain, or industry bottleneck. Categories come from that source material.
- **Topic mode**: user names a theme directly (e.g. "LLM AI", "humanoid robotics", "EV batteries"). No document required — build the category breakdown yourself (see Step 1).

Common triggers:
- "help me find relevant companies and their stock tickers"
- "who supplies X" / "誰是這個供應鏈的廠商"
- "turn this into a stock watchlist"
- "[topic] stocks by country" / "[topic] 概念股"

This skill does **not** fetch live prices, valuations, or run analysis. If the user wants quotes or analysis, hand off to `stock-analysis` or `yfinance` after producing the table.

---

## Workflow

### Step 1: Build the category breakdown

**If the user provided source material**: read it and break it into distinct technical categories using the source's own structure (headers/sections) where possible.

**If the user only named a topic**: build the category breakdown yourself before researching companies. Use `web_search` to ground this in the topic's actual value chain rather than guessing from memory.

#### For technology/compute topics: build the stack top-down first

For any topic that ultimately runs on physical hardware (AI, robotics, EVs, industrial systems), decompose the stack **top-down** before drilling into components:

1. **Application/model layer** — who builds the end product (foundation models, SaaS apps, vertical AI)
2. **Compute/cloud layer** — who provides the infrastructure (hyperscalers, GPU cloud)
3. **Chip/accelerator layer** — who designs the silicon (GPU, ASIC, networking chip)
4. **Server/system layer** — who assembles and ODMs the physical systems
5. **Component layer** — what's inside those servers (see physical checklist below)

Then, within the component layer, explicitly check for each of these before finalizing categories — this is the layer most often silently skipped:

- HBM / memory supply
- Liquid cooling (cold plates, CDU, quick disconnects, manifolds)
- Networking / optical transceivers / CPO
- Power delivery (PSU, busbar, VRM, TLVR inductors)
- **Passive components (MLCC, inductors, resistors, capacitors)** — no single famous brand, but every powered system depends on them
- PCB / substrate / copper cabling
- Advanced packaging (CoWoS or equivalent)
- Peripheral ICs (PCIe switch/retimer, BMC, PMIC)

**Self-audit before moving to Step 2**: re-read the category list and ask "if this entire list were a parts list for one physical server, what's missing?" Catches categories like passive components that are easy to skip.

If the topic/source material is in a domain where this physical checklist doesn't apply (pure software, biotech, finance), derive the equivalent breakdown from that domain instead — but default to assuming the physical layer is relevant rather than assuming it isn't.

---

### Step 2: For each category, identify candidate companies

Use the priority market order: **Taiwan → US → Japan → Korea → China → other**

Aim for up to ~5 genuine candidates per market where that many exist. Don't pad with weak fits to hit 5.

**Important structural cases:**

- **Categories concentrated in one market**: some categories (e.g. foundation model developers) are structurally US-dominated or China-dominated. When this is the case, note it explicitly rather than padding other markets with marginal players. Skip markets that have no genuine public players.
- **Categories where private companies dominate**: for categories where the top players are private (e.g. OpenAI, Anthropic, xAI in foundation models), **lead the category table with a prominent note** — don't bury it in a footnote. State: "Note: most top-tier [category] players are private. The table covers publicly traded proxies only."

For categories with fragmented supply chains (passive components, PCB/substrate, cooling, power), use `web_search` per market to verify current top players rather than relying on recall:
- `"<category>" 排名 廠商 2026` — Taiwan-language roundups reliably name the top 4-6 listed players
- `"<category>" companies AI server market share` — for US/global
- Targeted searches for Japan (TSE) and Korea (KRX) if the category likely has players there

Watch for these ownership patterns:
- **Wholly-owned subsidiaries**: map to the parent ticker and note the relationship (e.g. "TLVR inductors via subsidiary Cyntec — Delta owns 100%")
- **Cross-border acquisitions**: list under the current parent's market/ticker, not the brand's historical home (e.g. KEMET → Yageo/TWSE, not US)

---

### Step 3: Resolve each company to its primary ticker

For each company:
- **Primary ticker** on its home exchange (TWSE 4-digit, TSE 4-digit, KRX 6-digit, SSE/SZSE 6-digit, HKEX 4-digit, or US ticker)
- **Exchange** explicitly (e.g. "TWSE: 2330", "NASDAQ: NVDA", "TSE: 6920", "HKEX: 9888")

**ADR / dual-listed companies**: for companies with both a US ADR and a primary Asian listing (e.g. Baidu: BIDU on NASDAQ, 9888.HK on HKEX; TSMC: TSM on NYSE, 2330 on TWSE), list both tickers and note which is the primary home-market listing. The home-market ticker has higher liquidity and is the authoritative reference; the US ADR is often more accessible for US-based investors.

If uncertain about an exact ticker, verify with `web_search`. Getting a ticker wrong is worse than omitting it — if you can't verify, say so in the rationale column.

**Wholly-owned subsidiaries not separately listed**: map to the parent company's ticker and note the subsidiary relationship. Don't invent a ticker; don't silently drop the row.

---

### Step 4: Build the output table

One table per category (or combined table with a Category column for short requests):

| Company | Ticker | Exchange | Rationale |
|---|---|---|---|

- **Company**: English name + Chinese/Japanese/Korean name if source material used it
- **Ticker**: Exact ticker/code
- **Exchange**: TWSE / TPEx / NASDAQ / NYSE / TSE / KRX / HKEX / SSE / SZSE / other
- **Rationale**: one short clause — what specifically they supply or why they're relevant

Within each category, group rows by market in priority order (Taiwan → US → Japan → Korea → China → other) with up to ~5 per market. Use a sub-heading or blank-row separator per market when 3+ markets are represented.

**Final sanity checks before presenting:**

1. **Missing rows**: for every category, confirm the market leader in the #1 priority market for that niche is in the table, not just the easiest names to recall. A category with only US/Japan names while its Taiwan leader is missing means the per-market search wasn't run.
2. **Missing categories**: re-scan against the physical/electrical checklist from Step 1. If the topic involves physical servers/hardware and any checklist layer isn't its own category, add it — don't let it stay folded into a broader catch-all.
3. **Stack coverage**: for compute/AI topics, confirm the top-down stack (application → compute → chip → server → component) has at least one category per layer, or explicitly note why a layer has no public investable companies.

---

### Step 5: Present and offer next steps

After the table:
- Note any categories where no specific public company could be identified (private suppliers, in-house components)
- Note that live quotes/valuation aren't included — offer to pull via `yfinance` or hand off to `stock-analysis` if wanted

---

## Output format notes

- Markdown table directly in conversation — reference content for scanning, not a long-form document
- For large outputs (15+ rows spanning many categories), offer to export to `.xlsx` via the `xlsx` skill
- Keep rationale clauses tight (under ~12 words)
- Don't give investment recommendations — this skill identifies relevant companies only. If asked, note that Claude isn't a financial advisor and can present factual information rather than a recommendation
