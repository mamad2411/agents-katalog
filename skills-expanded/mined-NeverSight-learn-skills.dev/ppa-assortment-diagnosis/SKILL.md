---
name: ppa-assortment-diagnosis
description: >
  Diagnoses current price-pack assortment, identifies white spaces and improvement
  opportunities. Trigger when asked to: analyze SKU portfolio, map competitive landscape
  by price-pack, find white spaces in assortment, evaluate coverage across price tiers,
  diagnose PPA gaps by channel or region, or benchmark own portfolio vs competitors.
  Also trigger for: "PPA", "price pack architecture", "surtido", "portafolio de SKUs",
  "espacios en blanco", "white space", "brechas de precio", "análisis de empaque",
  "competitive landscape by pack size". Always renders inline HTML dashboard + TomTom
  map when geographic/channel data is present. Includes marketer NBA and benchmarks.
---

# ppa-assortment-diagnosis

Diagnoses current price-pack assortment across competitors, channels, regions and pack
sizes. Identifies white spaces, over-indexed SKUs, and strategic gaps. Always outputs
dashboard first, then NBA + market context.

---

## Plain Language: What This Does

```
"¿Qué SKUs tenemos vs la competencia?" → Competitive landscape mapping
"¿Dónde no tenemos pack/precio cubierto?" → White space identification
"¿Qué tamaño de pack prefiere el shopper?" → Consumer behavior analysis
"¿Cómo evolucionó el precio por kg/ml?" → Price-pack trend tracking
"¿En qué canal falta qué SKU?" → Channel × pack gap matrix
"¿Dónde geográficamente hay mayor oportunidad?" → TomTom zone mapping
```

**Core insight (EY PPA Framework):**
The right product at the right price in the right pack for the right channel.
A brand may have 20 SKUs and still have 3 critical white spaces that competitors exploit.

---

## Core Equations

### Price-per-unit metrics
```python
# Price per volume unit (eq. for cross-pack comparison)
price_per_kg  = price_shelf / (weight_grams / 1000)
price_per_ml  = price_shelf / (volume_ml / 1000)
price_per_use = price_shelf / servings_per_pack

# Relative price index vs category average
rpi = brand_price_per_unit / category_avg_price_per_unit
# RPI > 1.0 = price premium   RPI < 1.0 = price discount

# Pack size trend (eq. from Polestar methodology)
trend = (price_current - price_historical) / price_historical
```

### White space scoring
```python
# White space score for a (pack_size, price_tier) cell
ws_score = (competitor_coverage - own_coverage) * demand_weight
# ws_score > 0.5 = actionable white space
# ws_score > 0.8 = urgent gap
```

### Assortment coverage index
```python
# % of price-pack cells covered by own portfolio
coverage = own_cells_filled / total_competitive_cells
# Benchmark: category leaders typically > 0.65
```

---

## Workflow

### Step 1 — Load & profile data
```bash
python scripts/competitive_landscape.py \
    --data /mnt/user-data/uploads/sku_data.xlsx \
    --market [Mexico/Colombia/Chile/...] \
    --category [beverages/snacks/personal_care/...] \
    --output results/landscape.json
```

### Step 2 — Track price-pack trends
```bash
python scripts/price_pack_trends.py \
    --landscape results/landscape.json \
    --periods 12 \
    --output results/trends.json
```

### Step 3 — Find white spaces
```bash
python scripts/white_space_finder.py \
    --landscape results/landscape.json \
    --own-brand "[Brand Name]" \
    --output results/white_spaces.json
```

### Step 4 — Analyze consumer behavior
```bash
python scripts/consumer_behavior.py \
    --transactions /mnt/user-data/uploads/transactions.csv \
    --output results/consumer.json
```

### Step 5 — Geographic zone analysis (when channel/region data present)
```
→ Use TomTom MCP: tomtom-fuzzy-search + tomtom-area-search
  Query POIs by channel type (supermarkets, convenience, traditional trade)
  per city/zone to map distribution opportunity vs white space
→ Display results with tomtom-dynamic-map or places-map-display
```

### Step 6 — Generate report + dashboard
```bash
python scripts/assortment_gap_report.py \
    --landscape results/landscape.json \
    --white-spaces results/white_spaces.json \
    --consumer results/consumer.json \
    --output dashboard_data.json
```

**Output sequence:**
```
1. [bash_tool] Run all scripts
2. [web_search] Category benchmarks: avg SKUs per brand, price tier distribution,
   pack size trends for [market] [category] [year]
3. [TomTom MCP] If geographic data → map channel POIs per zone
4. [show_widget] HTML dashboard: landscape matrix + white space heatmap +
   trend chart + geo map
5. [text] NBA + market context (region, city, category, SKU level)
6. [text] Caveats: data recency, panel vs POS source differences
```

---

## Market Context (always include in output)

Every output must reference:
- **Market**: country + city/region
- **Category**: macro-category + sub-category
- **Channel**: MT (Modern Trade) / TT (Traditional Trade) / E-comm / Club
- **Time period**: data vintage + trend window
- **Competitive set**: defined brands in scope
- **Price tiers**: defined entry / mainstream / premium / super-premium breakpoints

---

## Dashboard panels

1. **KPI bar** — own SKUs, competitor SKUs, coverage index, top white space score,
   price tier gaps, RPI vs category
2. **Price-Pack Matrix** — rows=pack sizes, cols=price tiers, cells=brand coverage
   (color = own / competitor / white space / both)
3. **White Space heatmap** — score by (pack_size × price_tier × channel)
4. **Price trend chart** — price/kg or price/ml evolution by brand over time
5. **Consumer behavior panel** — avg purchase size, price paid, frequency by segment
6. **TomTom geo map** — channel POIs per zone, colored by white space opportunity
7. **NBA panel** — 5-6 specific actions

---

## Marketer Insights Layer (MANDATORY)

### Web search before benchmarking
```
web_search: "price pack architecture [category] [market] trends [year]"
web_search: "average SKUs per brand [category] [country] Nielsen [year]"
web_search: "pack size trends [category] LATAM [year]"
```

### Translate metrics to business language

| Technical | Business meaning |
|---|---|
| ws_score > 0.8 | "Competitor owns this space — we have zero presence" |
| coverage < 0.50 | "We cover less than half the competitive price-pack landscape" |
| RPI > 1.2 | "We price 20%+ above category avg — only justified if brand equity supports it" |
| trend > 0.15 | "Prices in this pack size rose 15% — inflation passing or premiumization signal" |
| price_per_kg gap | "Our 500g is 30% more expensive per kg than our 1kg — shopper notices" |

### NBA — Next Best Actions

Always produce 5-6 specific actions adapted to market/category context:
- **White space priority**: "Launch [pack_size]g at [price_tier] for [channel] —
  ws_score=[X], [N] competitors present, zero own coverage"
- **Over-indexed SKU**: "SKU [X] cannibalizes [Y] with 85% shopper overlap —
  rationalize or reposition"
- **Price corridor gap**: "No SKU between $[A] and $[B] — shopper trading up
  from entry tier has no step"
- **Channel-specific gap**: "Traditional trade has no [small_pack] below $[X] —
  competitors dominate impulse occasion"
- **Geographic priority**: "Zone [X] has [N] supermarkets with no [category]
  coverage above [price_tier] — distribution win opportunity"
- **Pack size trend**: "[Size] pack growing [X]% YoY — validate if portfolio
  has winning offer in this format"

---

## Integration with OS

| Skill | Handoff direction |
|---|---|
| `data-intake-normalizer` | Always first — validate SKU/price/channel data |
| `rgm-analyzer` | PPA diagnosis feeds RGM revenue waterfall |
| `ppa-portfolio-optimizer` | Diagnosis → Optimizer builds the solution |
| `price-demand-optimization` | White space price points → demand curve validation |
| `market-basket-analysis` | Cross-category white spaces → basket affinity |
| `category-space-planner` | Pack gaps → shelf space reallocation |
| `trade-promotion-roi` | New SKU launch → promo plan for distribution gain |

---

## References

- `references/polestar_ppa_methodology.md` — Price-pack architecture framework
- `references/ey_ppa_framework.md` — EY commercial excellence model
- `references/price_tier_benchmarks.md` — Category price tier definitions by market
