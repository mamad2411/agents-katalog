---
name: frontpage-buy-ad
description: Buy one of the 8 ad squares on frontpage.sh — pay USDC on Tempo via MPP, two HTTP calls, no accounts. Each buy bumps the square's price; the previous owner is refunded automatically with interest.
---

# frontpage-buy-ad

Use this skill when the user wants to **buy an ad square on frontpage.sh** — the perpetual auction with one large square (L), two medium (M1, M2), and five small (S1–S5). Every square is forever for sale.

Each buy is a one-shot flip: you pay the square's next price, the previous owner is refunded a multiple of what the slot was worth, and 80% of the remaining spread feeds the project pool (spent via the idea board — see [`frontpage-vote`](/skills/frontpage-vote)). Prices ratchet up per buy. The wallet that pays becomes the owner.

## Install

```bash
npx skills add DFectuoso/frontpage-sh-skills --copy                     # all frontpage skills
npx skills add DFectuoso/frontpage-sh-skills/frontpage-buy-ad --copy    # just this one
```

Testing against a dev box / Tempo testnet? Install the dev twin too: `npx skills add DFectuoso/frontpage-sh-skills-dev --copy` (gives you `frontpage-buy-ad-dev`, which overrides the base URL and network).

## Pricing

- Base price: $0.01 (10,000 µUSDC)
- **Large (L):** next price = current × 3.0 · previous owner refunded 1.5× current
- **Medium (M1, M2):** × 2.0 · refund 1.3× current
- **Small (S1–S5):** × 1.5 · refund 1.0× current (break-even)
- Spread after refund splits **20% platform / 80% project pool**

USDC on Tempo, 6 decimals; all API amounts are µUSDC integers.
**Don't reimplement the multipliers** — `GET /api/ads` returns `nextPriceMicros` per square, precomputed.

## The flow (MPP — the only payment path)

Base URL: `https://www.frontpage.sh` · full machine-readable contract: `https://www.frontpage.sh/openapi.json`

### 1. `GET /api/ads` — squares, current prices, and what the next buy costs

```bash
curl https://www.frontpage.sh/api/ads
# each ad includes: currentPrice, nextPriceMicros, tier, slot, ctaLabel/perk/promoCode, …
```

### 2. `POST /api/preview` — mint a preview token ($0.01 MPP)

Locks your creative + the quoted price into a signed token (valid 10 minutes) and returns a shareable preview URL plus an exact `next` instruction for settling.

### 3. `POST /api/buy` — charges `nextPrice` exactly, flips the square

```ts
import { privateKeyToAccount } from 'viem/accounts'
import { Mppx, tempo } from 'mppx/client'

Mppx.create({ methods: [tempo({ account: privateKeyToAccount('0x...') })] })

const res = await fetch('https://www.frontpage.sh/api/buy', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ previewToken: '<token from /api/preview>' }),
})
// { ok, transactionId, adId, slot, newOwnerWallet, newPrice, refundAmount, payment, payout, links }
```

MPP handles the 402 challenge automatically — the SDK signs the USDC transfer and retries with `Authorization: Payment …`.

- `409 PRICE_CHANGED` — the square flipped between preview and buy: re-mint the preview at the new price.
- `409 SLOT_CONFLICT` — you lost a concurrent race after paying: your charge is refunded automatically within ~1 minute.

## Payload shape (the preview body)

```ts
{
  slot: "S1",            // L | M1 | M2 | S1..S5
  name: string,          // 1-64 chars
  tagline?: string,      // ≤140
  url: string,           // https://...
  monogram: string,      // 1-4 chars (e.g. "TS")
  logoColor: string,     // hex like "#0A0A09"
  logoBg: string,        // hex
  adBg: string,          // CSS background, e.g. "linear-gradient(135deg,#F1ED4A,#FFA850)"
  adHeadline?: string,   // tier caps: large 48 / medium 56 / small 32 (use \n for line breaks; large renders BIG — keep it short).
                         // OPTIONAL: leave it empty/omitted for an "image-only" ad — no title/subtitle, the image fills the
                         // square (requires an image). The square still opens the details overlay + keeps its footer/perk.
  blurb?: string,        // ≤500
  ownerHandle: string,   // 1-30, single word, no spaces (e.g. "@fooofa") — your byline
  ownerEmail: string,    // REQUIRED — purchase receipt + "you've been outbid,
                         // refund wired" notice land here. Never public.

  // image: rendered as a COVER layer over adBg, at the square's true ratio.
  // Animated GIF is allowed and animates on the grid (the social card shows its
  // first frame). ⚠ PNG, JPEG or GIF ONLY. webp, svg and avif are REJECTED (HTTP
  //   400 IMAGE_UNSUPPORTED) — the server checks the actual bytes, not the
  //   filename/MIME, so re-encoding a webp as ".png" still fails. Convert to
  //   PNG, JPEG or GIF before sending. (Many models default to webp — do NOT.)
  image?: string,        // base64/data URL, PNG, JPEG or GIF only; max 3 MB per image
  imageUrl?: string,     // OR a public PNG/JPEG/GIF URL — we download & re-host it in
                         // our own store (no hot-linking). Must be publicly
                         // fetchable & ≤4 MB, else 400 (IMAGE_FETCH_FAILED /
                         // IMAGE_UNSUPPORTED).
  // BIG FILES (animated GIFs are often 1–3 MB): do NOT inline the base64 into a
  //   CLI argument — shells cap a single arg at ~128 KB and even a 1 MB image is
  //   ~1.4 MB of base64. With the mppx CLI (≤0.6.31 sends only inline string
  //   bodies, NO multipart), the path is `imageUrl`: host the file at a PUBLIC
  //   url and pass it. On a dev box see the -dev skill for the localhost trick.
  //   (This endpoint also accepts multipart/form-data with `image` as a FILE
  //   part — no arg limit, no hosting — but only from a client that does BOTH
  //   multipart AND the MPP payment; mppx pays but can't multipart, plain curl
  //   multiparts but can't pay, so multipart needs a custom MPP client.)
  // recommended dimensions (2× display, true slot ratios):
  //   large 1712×944 (1.81:1) · medium 1136×464 (2.45:1) · small 560×464 (1.21:1)

  // richer creative (all optional; OMITTING THEM ON A BUY CLEARS THEM —
  // creatives never carry over from the previous owner):
  ctaLabel?: string,     // ≤24 — custom button text, e.g. "get the deal"
  perk?: string,         // ≤140 — offer line, shown prominently in the details view
  promoCode?: string,    // ≤24 — copyable code next to the perk
  xHandle?: string,      // optional X/Twitter handle (@handle, bare, or x.com URL)
                         // — @mentioned in the auto-tweet when the square flips
  titleFont?: string,    // headline typeface: "grotesk" (default) | "mono" | "serif" | "display" | "script".
                         // Any other value → 400 INVALID_TITLE_FONT. Applies on-site AND on the social card.
}
```

## Heuristics for agents

- **Read `nextPriceMicros` from `/api/ads`** — no tier math needed; it's exactly what `/api/buy` will charge.
- **Bring a perk.** Squares with a perk + promo code give viewers a reason to click through — that's the conversion the slot is for.
- **Pass the brand's `xHandle`.** Every buy auto-posts to @frontpagesh; with `xHandle` set, that post @mentions the brand (notifies them, invites a retweet — free reach).
- **Images must be PNG, JPEG or GIF — never webp.** The server validates the actual bytes and returns `400 IMAGE_UNSUPPORTED` for webp/svg/avif (and for a webp renamed `.png`). If your source is webp, convert it to PNG, JPEG or GIF first. Animated GIFs animate on the grid; the social card uses their first frame.
- **Uploading a big image (esp. a GIF)? Don't inline base64.** A 1–3 MB GIF base64 won't fit in a single CLI argument (~128 KB shell limit). With the **mppx** CLI (inline string bodies only, no multipart), host the file at a public URL and pass `imageUrl`. The endpoint also accepts `multipart/form-data` with `image` as a file part, but only from a client that does multipart *and* the MPP payment (mppx can't multipart; plain curl can't pay) — so for mppx, `imageUrl` is the path. The decoded image must be ≤3 MB; a fetched `imageUrl` must also be ≤4 MB to download.
- **Design for the real ratio.** Your image cover-crops to the slot's shape (and tighter crops on mobile) — keep the message in the center.
- **Moderation runs server-side** (OpenAI omni-moderation) over every text field AND the creative image. Sexual / hateful / harassing / violent / self-harm / illicit content → `400 MODERATION_FAILED` (charged, since moderation runs post-payment).
- **The flip is instant.** The previous owner's refund settles inline or via the retry worker; read `payout.status` on the receipt.
