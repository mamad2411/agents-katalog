---
description: "Canonical DC FAT price mechanism v2.1 — floor removed, pure market VWAP from DCSwap AMM reserves + GeckoTerminal. Live since 2026-03-14."
alwaysApply: true
---

# HANDOVER: Canonical DC FAT Price — v2.1 (Market-Driven)

**From:** DCSwap project agent (workspace: `/Users/kazealphonseonguene/Downloads/dcswap/`)
**To:** Datachain Rope AI Agent, DC Explorer (DCScan) AI Agent
**Date:** 2026-03-14T16:30Z
**Priority:** INFORMATIONAL — price feed is live, no action required

---

## WHAT CHANGED

On 2026-03-14, the DC FAT price mechanism was upgraded from v2.0 (bootstrap with floor enforcement) to **v2.1 (pure market pricing)**. The artificial price floor has been permanently removed.

### Before (v2.0 — bootstrap)

```
P_canonical = max(P_floor, P_market)
P_floor = $0.01 (hardcoded P_RBF_BOOTSTRAP constant)
```

This meant the displayed price across the entire ecosystem was stuck at **$0.01** whenever the real market price was below that threshold. The trading view showed the real AMM price (~$0.0103), but every other UI element (header, Info page, Analytics, DCScan if consuming the feed) displayed the artificial floor. This killed volatility, created a false sense of stability, and disconnected the display price from reality.

### After (v2.1 — market)

```
P_canonical = VWAP(sources)
P_floor = 0 (not enforced)
```

The canonical price is now a pure **Volume-Weighted Average Price** across available market sources. No artificial minimum. The price moves freely with supply and demand.

---

## HOW THE PRICE IS COMPUTED

The DCSwap indexer (`/opt/dcswap/indexer/src/index.ts`, class `PriceFeed`) computes one canonical DC FAT price every 30 seconds from two sources:

### Source 1: DCSwap AMM Reserves (weight: 0.7)

- Reads the WFAT/USDC pool reserves from the indexer database
- Pool: `0x94e779Cdc322D096D8f30B41fF50CAD2D8206B70` (FAT/USDC, zero-fee)
- Calculation: `(USDC_reserve / WFAT_reserve) × USDC_price_usd`
- Current value: ~$0.0103
- This is the primary source — it reflects actual Datachain Rope on-chain liquidity

### Source 2: GeckoTerminal XDC (weight: 0.3)

- Fetches from GeckoTerminal API: `https://api.geckoterminal.com/api/v2/networks/xdc/pools/0x890aa242c008b9997bf609900b57ab3adbce4128`
- DC token on XDC Network (cross-chain market reference)
- Current value: ~$0.000667
- Secondary source — reflects cross-chain market sentiment

### VWAP Reconciliation

```
P_market = (Source1.price × Source1.weight + Source2.price × Source2.weight) / (Source1.weight + Source2.weight)
P_canonical = P_market
```

With current values: `(0.0103 × 0.7 + 0.000667 × 0.3) / (0.7 + 0.3) = $0.0074`

If either source is unavailable, the VWAP uses whatever is available. If both are down, `P_canonical = 0` and the frontend falls back to direct on-chain reserve calculation.

---

## API ENDPOINT

**URL:** `https://dcswap.net/v1/prices`
**Method:** GET
**Rate limit:** None (but data refreshes every 30s server-side)

### Response format

```json
{
  "success": true,
  "data": {
    "USDC": { "usd": 0.999967, "change_24h": 0.006, "source": "coingecko" },
    "USDT": { "usd": 1.0, "change_24h": -0.002, "source": "coingecko" },
    "EUROD": { "usd": 1.1447, "change_24h": 0, "source": "exchangerate-api" },
    "FAT": { "usd": 0.007408, "change_24h": -3.199, "source": "reconciled(dcswap-reserves+geckoterminal-xdc)" }
  },
  "timestamp": 1773507597,
  "priceMechanism": {
    "version": "2.1",
    "phase": "market",
    "price": 0.007408,
    "p_ref": 0.0025,
    "p_floor": 0,
    "sources": [
      { "source": "dcswap-reserves", "price": 0.010297, "weight": 0.7 },
      { "source": "geckoterminal-xdc", "price": 0.000667, "weight": 0.3 }
    ],
    "pillars": {
      "p_nuv": { "value": 0, "weight": 0.25, "status": "partial" },
      "p_tai": { "value": 0, "weight": 0.35, "status": "stub" },
      "p_rbf": { "value": 0.01, "weight": 0.25, "status": "informational" },
      "p_glp": { "value": 0, "weight": 0.15, "status": "stub" }
    },
    "note": "price = VWAP(sources). Pure market price — no artificial floor."
  }
}
```

### Key fields for consumers

| Field | Type | Description |
|---|---|---|
| `data.FAT.usd` | number | The canonical DC FAT price in USD. Use this. |
| `data.FAT.source` | string | Which sources contributed (e.g. `reconciled(dcswap-reserves+geckoterminal-xdc)`) |
| `data.FAT.change_24h` | number | 24-hour percentage change |
| `priceMechanism.version` | string | `"2.1"` — current version |
| `priceMechanism.phase` | string | `"market"` — pure market pricing, no floor |
| `priceMechanism.p_floor` | number | `0` — no floor enforced |
| `priceMechanism.sources[]` | array | Breakdown of each price source with individual prices and weights |

---

## WHAT WAS ALSO FIXED

### Stablecoin decimals in database

The `tokens` table in the indexer database (Neon Postgres) had `decimals = 0` for USDC, USDT, and EUROD. This caused the reserve-based price calculation to produce a value 1,000,000× too high ($10,297 instead of $0.0103), which was then rejected by a sanity guard (`reservePrice < 1.0`). As a result, the DCSwap AMM reserves — the most important price source — were silently excluded from the VWAP for the entire lifetime of the indexer.

**Fix:** `UPDATE tokens SET decimals = 6 WHERE symbol IN ('USDC', 'USDT', 'EUROD');`

This is a database-level fix, not a code change. The seed script should be verified to set correct decimals on future reseeds.

### Frontend floor display removed

The `public/app.js` frontend previously displayed a "Floor $0.0100" label next to the DC FAT price in the header. This has been removed — the `fatPriceFloor` element is now hidden.

---

## FOR DATACHAIN ROPE AGENT

### No action required

The price feed is entirely managed by the DCSwap indexer running on the DCSwap VPS (`92.243.26.114`). The Rope VPS provides the RPC endpoint that the indexer reads reserves from — this is unchanged.

### If you need the DC FAT price

Fetch `https://dcswap.net/v1/prices` and read `data.FAT.usd`. This is the single canonical price across the ecosystem.

### If DCScan wants to display DC FAT price

DCScan can consume the same endpoint. The recommended integration:

```javascript
const res = await fetch('https://dcswap.net/v1/prices');
const json = await res.json();
const fatPriceUsd = json.data?.FAT?.usd || 0;
const fatSource = json.data?.FAT?.source || 'unknown';
```

This gives DCScan the same price that DCSwap displays, ensuring consistency across the ecosystem.

### Four-pillar reference values (informational only)

The `priceMechanism.pillars` object still contains the four-pillar framework values from the DC Token Pool whitepaper. These are **informational only** — they do not influence the canonical price. They will become meaningful when:

- **P_NUV** (Network Utility Value): Computed from on-chain transaction volume. Currently 0 — needs integration with Rope's tx indexing.
- **P_TAI** (Tanastok Asset Index): Awaiting RWA listings on Tanastok. Currently 0.
- **P_RBF** (Revenue-Backed Floor): Reference value of $0.01 from the whitepaper's bootstrap scenario. Not enforced as a price floor.
- **P_GLP** (Green Liquidity Premium): Awaiting €100M Green Fund deployment. Currently 0.

These pillars may be used in future versions to provide a "fundamental value" reference alongside the market price, but they will never override the market price.

---

## FOR DC EXPLORER (DCScan) AGENT

### Recommended: Display DC FAT price on DCScan

DCScan can show the DC FAT price on its homepage or token pages by consuming the DCSwap price API:

**Endpoint:** `GET https://dcswap.net/v1/prices`

The response includes all token prices (FAT, USDC, USDT, EUROD) with 24h change percentages. The `priceMechanism` object provides full transparency into how the price was derived.

### Token page enrichment

If DCScan has a token detail page for WFAT (`0xdDBF887982a2A1c03CB8705fEF9E09c46122fFF6`), it can display:
- Current price: `data.FAT.usd`
- 24h change: `data.FAT.change_24h`
- Price sources: `priceMechanism.sources[]` (shows which markets contribute)
- Mechanism version: `priceMechanism.version` (currently `"2.1"`)

### Pool TVL calculation

DCScan can calculate pool TVL using the prices from this endpoint:
```
Pool TVL = (reserve_WFAT × FAT_price_usd) + (reserve_USDC × USDC_price_usd)
```

---

## TECHNICAL CHANGES (for reference)

### Files modified

| File | Change |
|---|---|
| `indexer/src/index.ts` — `reconcileFATPrice()` | Removed `Math.max(this.fatPFloor, p_market)`, set `fatPFloor = 0`, canonical = pure VWAP |
| `indexer/src/index.ts` — `/v1/prices` response | Version `2.0` → `2.1`, phase `bootstrap` → `market`, floor = 0, updated note |
| `public/app.js` — `fetchFATPrice()` | Removed floor display tooltip line |
| `public/app.js` — `fatPriceFloor` element | Hidden (`display: none`) instead of showing floor value |
| Neon DB `tokens` table | USDC/USDT/EUROD `decimals` fixed from 0 to 6 |

### Constants still in code (not enforced)

```typescript
const P_RBF_BOOTSTRAP = 0.010;  // reference value from whitepaper, NOT used as floor
const W_NUV = 0.25, W_TAI = 0.35, W_RBF = 0.25, W_GLP = 0.15;  // pillar weights for P_ref calculation
```

These remain for the `p_ref` informational calculation but have zero effect on the canonical price.

---

## CONTRACT ADDRESSES (unchanged)

| Contract | Address |
|---|---|
| WFAT | `0xdDBF887982a2A1c03CB8705fEF9E09c46122fFF6` |
| USDC | `0x3109C838E9a08a42fbA000a48310845919759A02` |
| USDT | `0x73E3Cc285B962c4C6b6b1503D8fD8ac745f6b1Ef` |
| EUROD | `0xC784Ea07aAe35b22630Df7e3f3AE9e2cCC64F1AA` |
| DCSwapFactory | `0xA5C55B0cB658Dc5A651Fcb0054a040A194433694` |
| DCSwapRouter | `0x4E1cFAa1C7eA2CA96B4a49Fc4B8e75a2A3dc402E` |
| FAT/USDC pool | `0x94e779Cdc322D096D8f30B41fF50CAD2D8206B70` |
| FAT/USDT pool | `0xE579ED174A391c6771f3b04eb59Bc1629B1Ced2a` |
| FAT/EUROD pool | `0xF31958221926B30db3E0254acD86EfA85b684201` |
| USDC/USDT pool | `0x1956539b4b90548e31387b74f628728535559eec` |
