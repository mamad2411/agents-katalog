---
name: clawmart-x402-skill-builder
description: Use this skill when an autopilot tick needs to ship a new x402-billed skill route. Follows the exact pattern of the existing 5 skills in src/app/api/x402/ — 402 challenge, X-Demo mode, USDC-on-Base settlement, PAYMENT_ADDRESS env var. Also writes the Convex skill document so it shows up in /api/catalog.
---

# Adding a new x402 skill

## Why this exists

The 5 existing skills (`web-summarize`, `sentiment-analyzer`, `data-extractor`, `code-reviewer`, `voicecharm-receptionist`) all follow the same protocol shape. Divergence creates breakage in `/api/catalog` and in agent SDKs that consume our catalog. Use this skill to avoid that.

## Reference implementation

Look at `src/app/api/x402/web-summarize/route.ts` before writing a new route. It's the canonical pattern. Do not improvise the 402 response body — agents parse it strictly.

## Checklist to add a skill

### 1. Route file

Create `src/app/api/x402/<slug>/route.ts` with:

```typescript
import { NextRequest, NextResponse } from "next/server";

const PAYMENT_ADDRESS = process.env.PAYMENT_ADDRESS || "0x0000000000000000000000000000000000000000";
const USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const PRICE_USDC = <decimal>; // e.g. 0.003

export async function POST(request: NextRequest) {
  const paymentHeader = request.headers.get("X-PAYMENT");
  const demoMode = request.headers.get("X-Demo") === "true";

  let body: Record<string, unknown> = {};
  try { body = await request.json(); } catch { body = {}; }

  if (!paymentHeader && !demoMode) {
    return NextResponse.json(
      {
        x402Version: 1,
        accepts: [{
          scheme: "exact",
          network: "eip155:8453",
          maxAmountRequired: String(PRICE_USDC * 1e6),
          resource: "https://clawmart.co/api/x402/<slug>",
          description: "<same sentence as Convex skill.description>",
          mimeType: "application/json",
          payTo: PAYMENT_ADDRESS,
          maxTimeoutSeconds: 30,
          asset: USDC_BASE,
        }],
      },
      { status: 402 }
    );
  }

  // TODO: actual skill logic
}
```

Pricing rule of thumb (revisit from metrics over time):
- Pure text transform: $0.001–$0.005
- Hits external paid API: cost_to_us × 2, rounded to nearest $0.001
- Heavy compute / LLM call: $0.01–$0.05

### 2. Convex skill document

The skill must exist in the Convex `skills` collection or it won't appear in `/api/catalog`. Add a migration/seed in `convex/seed.ts` (or whatever the current seed file is — check `convex/` for conventions) or via a manual mutation:

```typescript
// fields matching convex/schema.ts skills table
{
  slug: "<slug>",
  name: "<Display Name>",
  description: "<same sentence as 402 response>",
  longDescription: "...",
  category: "<Research | Data | Code | Voice | ...>",
  endpoint: "/api/x402/<slug>",
  method: "POST",
  pricePerCall: <decimal>,
  authorName: "Clawmart",
  tags: [...],
  exampleInput: JSON.stringify({...}),
  exampleOutput: JSON.stringify({...}),
  responseTime: "~Xs",
  totalCalls: 0,
  totalReviews: 0,
  averageRating: 0,
  status: "active",
  createdAt: Date.now(),
}
```

### 3. Link it in the catalog

Re-check `/api/catalog/route.ts` — it pulls from Convex automatically, so no code change there. The skill appears as soon as its Convex document has `status: "active"`.

### 4. Smoke test locally

```bash
# 402 challenge
curl -s -X POST http://localhost:3000/api/x402/<slug> -d '{}' -H 'Content-Type: application/json' | jq .
# expect x402Version, accepts[0].payTo set

# demo mode
curl -s -X POST http://localhost:3000/api/x402/<slug> \
  -H 'X-Demo: true' -d '<example input>' \
  -H 'Content-Type: application/json' | jq .
```

### 5. Update docs

If `src/app/docs/` has an index of skills, add the new one there too. Keep it short.

## Things not to do

- Don't hardcode a payment address other than `PAYMENT_ADDRESS` env.
- Don't change `network` or `asset` — x402 on clawmart means USDC on Base, period.
- Don't skip the `X-Demo: true` branch — humans testing the site from browsers depend on it.
- Don't set `status: "active"` on the Convex doc without the route being deployable. If `PAYMENT_ADDRESS` is still the zero address in Vercel, create the doc with `status: "pending"` instead.
- Don't forget to include the new slug in any existing e2e test inventory (check `src/` for test patterns before assuming there are none).
