---
name: frontpage-million
description: Buy pixels on the frontpage.sh million-pixel canvas — pay USDC on Tempo via MPP, two HTTP calls, no accounts. Pick each pixel's colour, plus one optional link + label for the whole batch; any owned pixel with a link is clickable.
---

# frontpage-million

Use this skill when the user wants to **buy pixels on the frontpage.sh "million" canvas** at `/million` — a 1000×1000 grid (1,000,000 pixels). You choose an RGB colour per pixel, plus **one optional link + label for the whole buy**. Any pixel can be bought; if it's already owned you outbid the current owner and the price steps up.

The wallet that pays owns the pixels. The optional **link + label apply to every pixel in the buy**, and **any pixel you own with a link is clickable** (shown on hover) — no minimum block, no contiguity. A single linked pixel works. (Taking one of someone's pixels only takes that pixel; it never breaks the links around it.)

## Install

```bash
npx skills add DFectuoso/frontpage-sh-skills --copy   # all frontpage skills (recommended)
```

Testing against a dev box / Tempo testnet? Install the dev twin: `npx skills add DFectuoso/frontpage-sh-skills-dev --copy` (gives you `frontpage-million-dev`, which overrides the base URL and network).

## Pricing (a doubling ladder)

- A pixel starts at **$0.005** and the price **doubles every time it's sold**: never-owned = $0.005, then $0.01, $0.02, $0.04, $0.08, …
- On a re-buy the new price is **2× what the previous owner paid** (pixels are priced exactly like a medium "M" ad slot). They're refunded **1.3× what they paid** — always a **+30% gain, never a loss**. The remaining 0.7× splits **20% platform / 80% project pool** (the pool is spent via the idea board — see [`frontpage-vote`](/skills/frontpage-vote)).
- All amounts are integer µUSDC ($0.005 = 5,000). **Don't compute prices yourself** — `/api/million/quote` returns the exact per-pixel price and the batch total.
- Max **2,500 pixels per buy** (a 50×50 block).

## The flow (MPP — the only payment path)

Base URL: `https://www.frontpage.sh` · machine-readable contract: `https://www.frontpage.sh/openapi.json`

Coordinates are `x` (column) and `y` (row), both `0..999`. `rgb` is a 6-hex colour like `#ff0000`.

**Free reads (no MPP, no auth) — these are all of them; there is no `/status`:** `GET /api/million/grid` (every bought pixel + price), `GET /api/million/pixel?x=&y=` (one pixel), `GET /api/million/snapshot` (raw RGB byte plane of the board), `GET /api/million/links` (clickable-link overlay), `GET /api/million/activity` (recent buys). Only `POST /api/million/quote` (free) and `POST /api/million/buy` (paid) below mutate.

### 0. (optional) `GET /api/million/grid` — the whole board, to choose WHERE to buy

Returns every **bought** pixel with its next-buy `priceMicros` + owner/link metadata. Pixels NOT in the list are unbought and cost `basePriceMicros` ($0.005). Use it to find empty or cheap regions before quoting.

```bash
curl https://www.frontpage.sh/api/million/grid
# { grid: 1000, total: 1000000, sold, basePriceMicros, pixels: [{ x, y, timesBought, priceMicros, linkLive, url, label, owner }] }
```

To find a cheap empty region: pick coordinates that don't appear in `pixels` → those are unbought and cost base price ($0.005 each).

### 1. (optional) `GET /api/million/pixel?x=&y=` — inspect one pixel

```bash
curl "https://www.frontpage.sh/api/million/pixel?x=500&y=500"
# { owned, timesBought, nextPriceMicros, nextPriceUsd, url, label, linkLive, owner }
```

### 2. `POST /api/million/quote` — price the batch (FREE)

Body: `{ pixels: [{ x, y, rgb }], url?, label? }` — pixels carry only coords + colour; the optional `url` + `label` are **batch-level** and applied to every pixel. **Free, no payment** — plain `fetch`, no MPP. Returns a signed quote token, the total, the **priced `pixels` array** (each echoed with the stamped `url`/`label` + its `timesBought`), and a **`previewUrl`** you can open or share to see the proposed pixels rendered on the live board. Token valid 10 minutes. (The link + label are screened — egregiously offensive/scammy content is rejected with `400 MODERATION_FAILED`.)

```ts
const quote = await (await fetch('https://www.frontpage.sh/api/million/quote', {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({
    pixels: [{ x: 500, y: 500, rgb: '#ff0000' }],
    url: 'https://mysite.com', label: 'my site',   // optional, applied to all pixels
  }),
})).json()
// { token, quoteId, count, totalMicros, totalUsd, expiresAt, previewUrl, pixels: [...] }
// DEFAULT: show quote.previewUrl to the user and wait for their go-ahead before buying
// (skip this confirmation only if they explicitly told you to buy directly).
```

### 3. `POST /api/million/buy` — charges the quoted total exactly, settles the batch

**Send just `{ quoteId, email }`** — the server already has the priced pixels from the quote, so you DON'T re-send the array (this keeps the buy tiny even for thousands of pixels). `email` is required — the receipt goes there and the address is added to the frontpage.sh newsletter.

```ts
const res = await (await fetch('https://www.frontpage.sh/api/million/buy', {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ quoteId: quote.quoteId, email: 'you@example.com' }),
})).json()
// { ok, buyId, settledCount, lostCount, chargeAmountUsd, refundedToBuyerMicros, refundsQueued }
```

`email` is required and validated **before** the charge — a missing/invalid email returns `400 VALIDATION` and never charges. MPP handles the 402 challenge automatically — the SDK signs the USDC transfer and retries with `Authorization: Payment …`.

> Legacy form still works: `{ token, pixels, email }` (re-send the quote's exact `pixels` array). Prefer `quoteId`.

- **Best-effort settlement.** If a pixel's price moved between quote and buy (someone else bought it), it's skipped and that pixel's cost is **refunded to you** (`lostCount` > 0, `refundedToBuyerMicros` > 0). Re-quote those pixels to try again at the new price.
- `400 TOKEN_INVALID_OR_EXPIRED` — re-quote (tokens last 10 min). `404 QUOTE_NOT_FOUND` / `409 QUOTE_ALREADY_USED` — re-quote. `409 DUPLICATE_BUY_CREDENTIAL` — this payment already settled.
- **Confirming.** Success is the `{ ok: true, buyId, … }` body — there's no receipt URL. To verify it landed, re-read `GET /api/million/pixel?x=&y=` and check `owned: true` with your `rgb`/`url`. The pixel shows on the board at `https://www.frontpage.sh/million`.

## Adding a link/label

Pass `url` (and optionally `label`) at the **top level** of the quote body — it's applied to every pixel in the buy, and each owned pixel is then independently clickable (label shows on hover). No block, no minimum — even one pixel works:

```ts
const pixels = []
for (let y = 100; y < 105; y++) for (let x = 100; x < 105; x++) pixels.push({ x, y, rgb: '#1133ff' })
// quote({ pixels, url: 'https://mysite.com', label: 'my site' }) → buy({ quoteId: quote.quoteId, email })
// → every bought pixel is clickable; the label shows on hover
```

## Heuristics for agents

- **Show the preview before buying — by default.** The buy spends real USDC and can't be undone. After quoting, send the user `quote.previewUrl` (it renders the proposed pixels on the live board) and wait for their go-ahead before calling `/api/million/buy`. Only skip this confirmation when the user has explicitly told you to buy directly without review.
- **Pick the spot with `GET /api/million/grid`.** It lists every owned pixel + price; anything absent is base price ($0.005). Scan for an empty/cheap region before quoting.
- **Quote, then buy with `quote.quoteId`** — the server settles from the persisted quote, so big art stays a tiny buy call (no pixel re-send, no payload limits).
- **Don't compute prices** — read `totalUsd` / per-pixel `priceMicros` from the quote.
- **For a link, just set `url` (+ `label`) at the top level of the quote.** It applies to every pixel; even a single linked pixel is clickable.
- **A `lostCount` > 0 isn't an error** — those pixels were outbid mid-flight and refunded; re-quote to retry.
- **Keep batches ≤ 2,500 pixels.** Split larger art into multiple buys.
- **Watch the canvas live** at `https://www.frontpage.sh/million` (real-time updates as buys land).
