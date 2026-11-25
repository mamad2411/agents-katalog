---
name: pr402-seller
description: >-
  Integrate an x402 seller on Solana via pr402 (ipay.sh): HTTP 402 gates,
  SplitVault onboarding, PAYMENT-SIGNATURE verify/settle, and discovery enrollment.
  Use whenever the user monetizes an API, adds pay-per-call, implements HTTP 402,
  mentions x402 seller, pr402 seller, X402SellerSDK, merchant wallet, SplitVault,
  x402-resources.json, x402-seller-starter, x402-subscription-starter, subscription,
  hourly daily monthly JWT subscribe, or exact-rail UniversalSettle. If seller vs buyer
  is unclear, load **pr402** first.
metadata:
  author: miraland-labs
  version: "1.2.0"
---

# x402 seller (pr402)

Help the user **monetize an HTTP API** on the pr402 facilitator using the **`exact`** rail (SplitVault via pr402) unless they explicitly need **`sla-escrow`** (escrow + oracle — different skill path; see [oracles Seller Guide](https://github.com/miraland-labs/oracles/blob/main/docs/SELLER_GUIDE.md)).

## Pay-per-call vs subscription

| Model | Gate | Starter | Reference |
| --- | --- | --- | --- |
| **Pay-per-call** (default) | 402 on each paid route | [x402-seller-starter](https://github.com/miraland-labs/x402-seller-starter) | [references/runtime-sdk.md](references/runtime-sdk.md) |
| **Subscription** (hourly/daily/monthly window) | 402 **only** on `POST /subscribe`; Bearer JWT on data routes | [x402-subscription-starter](https://github.com/miraland-labs/x402-subscription-starter) | [references/subscription-exact-rail.md](references/subscription-exact-rail.md) |

If the user wants time-window access, **do not** apply per-request 402 gates — follow the subscription reference instead.

## Two-part integration model

| Phase | Tooling | Outcome |
| --- | --- | --- |
| **Onboarding & discovery** | [x402-cli](https://github.com/miraland-labs/x402/tree/main/tools/x402-cli) or facilitator REST | SplitVault on-chain + optional directory listing |
| **Runtime gate** | `X402SellerSDK` in app code | 402 challenge → verify → settle on each paid request |

Reference implementation: **[x402-seller-starter](https://github.com/miraland-labs/x402-seller-starter)** (Rust / TypeScript / Python — **separate repo**, not inside the x402 hub).

## GitHub repos (x402 hub is virtual)

The [x402 hub](https://github.com/miraland-labs/x402) coordinates docs and ships **x402-cli** only. Clone each project from its own repository:

| Project | GitHub |
| --- | --- |
| pr402 facilitator | [miralandlabs/pr402](https://github.com/miralandlabs/pr402) |
| Seller starter | [miraland-labs/x402-seller-starter](https://github.com/miraland-labs/x402-seller-starter) |
| Buyer starter | [miraland-labs/x402-buyer-starter](https://github.com/miraland-labs/x402-buyer-starter) |
| Oracles workspace | [miraland-labs/oracles](https://github.com/miraland-labs/oracles) |
| x402-cli source | [miraland-labs/x402/tree/main/tools/x402-cli](https://github.com/miraland-labs/x402/tree/main/tools/x402-cli) |
| Subscription seller starter | [miraland-labs/x402-subscription-starter](https://github.com/miraland-labs/x402-subscription-starter) |
| Subscription seller SDK | [miraland-labs/x402-subscription-seller](https://github.com/miraland-labs/x402-subscription-seller) (`@pr402/subscription-seller`) |
| Subscription auth (Tier B) | [miralandlabs/subscription-auth](https://github.com/miralandlabs/subscription-auth) |

The on-chain **`exact`** rail uses SplitVault (UniversalSettle engine). Program source is **not public** yet — do not link integrators to a GitHub repo; use facilitator docs and the seller starter.

## Facilitator hosts

**Default for examples and production integration:**

| | Base URL | API prefix |
| --- | --- | --- |
| **Production (Mainnet)** | `https://ipay.sh` | `/api/v1/facilitator` |
| Alternate (same service) | `https://agent.pay402.me` | `/api/v1/facilitator` |

Devnet testing only: `https://preview.ipay.sh` or `https://preview.agent.pay402.me` — match facilitator host to the cluster your seller wallet uses.

Confirm `solanaNetwork` with `GET https://ipay.sh/api/v1/facilitator/health` (or your chosen host). **Never hardcode RPC URLs** — read `solanaWalletRpcUrl` from health/capabilities.

## Golden path checklist

Run in order; do not skip Activate before accepting payments.

1. **Preview** — `GET /api/v1/facilitator/sellers/{WALLET}/preview`  
   Read `lifecycle.nextStep`. If `"activate"`, proceed to step 2.

2. **Activate (on-chain)** — `POST /api/v1/facilitator/sellers/provision-tx` with `{ "wallet", "asset": "USDC" }` (or `SOL` / mint).  
   Sign the returned base64 bincode `VersionedTransaction` with the **seller wallet** and broadcast.  
   `statusCode: "ALREADY_PROVISIONED"` means done — no tx to sign.

3. **Register merchant (optional, discovery)** — challenge → sign → register.  
   Details: [references/onboarding-cli.md](references/onboarding-cli.md)

4. **Enroll API routes (optional, discovery)** — publish `x402-resources.json` manifest.  
   Details: [references/x402-resources-manifest.md](references/x402-resources-manifest.md)

5. **Runtime SDK** — boot `X402SellerSDK`, gate paid routes, handle headers.  
   Details: [references/runtime-sdk.md](references/runtime-sdk.md)

6. **Verify** — unpaid request → HTTP 402 + enriched body; paid request → HTTP 200 + `PAYMENT-RESPONSE`.

## x402 v2 headers (runtime)

| Header | Direction | Role |
| --- | --- | --- |
| `PAYMENT-REQUIRED` | Server → client | Base64 `PaymentRequired` JSON on 402 (starters may also return JSON body) |
| `PAYMENT-SIGNATURE` | Client → server | Buyer payment proof (JSON or base64) |
| `PAYMENT-RESPONSE` | Server → client | Base64 settlement result on 200 **or** 402 after failed settle |

## Critical pr402 rules (not generic x402)

- **`payTo` is a PDA**, not the seller's personal wallet. Starters use **`POST /payment-required/enrich`** so the facilitator injects vault PDAs — do not hand-derive PDAs in app code.
- **One payment asset per merchant wallet** on this facilitator. Multi-rail/multi-token → separate seller pubkeys.
- **Scheme aliases**: sellers may publish `v2:solana:exact` in `accepts[]`; verify/settle bodies use wire `exact`.
- **Mint allowlist**: if the deployment sets `PR402_ALLOWED_PAYMENT_MINTS`, wrong `asset` fails at build/verify with an explicit approved-mints message.

## Language starters

Clone [x402-seller-starter](https://github.com/miraland-labs/x402-seller-starter) and open the subdir matching the user's stack:

| Stack | Path | Run |
| --- | --- | --- |
| Rust + Axum | `rust/` | `cargo run --example axum_server` |
| TypeScript + Express | `typescript/` | `npm start` |
| Python + FastAPI | `python/` | `x402-seller-start` |

Required env (all languages): `FACILITATOR_BASE_URL` (e.g. `https://ipay.sh`), `MERCHANT_WALLET`, `SELLER_PUBLIC_BASE_URL`, `X402_AMOUNT` (USDC microunits as string, e.g. `"50000"` = 0.05 USDC).

## When implementing for the user

1. **Prefer adapting the starter** over inventing a new payment stack. Copy `X402SellerSDK` + gate/middleware pattern from the matching language.
2. **Separate onboarding from runtime** — CLI/REST onboarding once; SDK only calls enrich/verify/settle at runtime (no heavy Solana deps in the web server).
3. **Call live OpenAPI** — `GET {facilitator}/openapi.json` on the target host before guessing field names.
4. **Do not commit keypairs** — use env paths; warn if `.env` contains secrets.
5. **Escrow sellers** — if the user needs conditional delivery / oracles, stop and route to `sla-escrow` + [oracles workspace](https://github.com/miraland-labs/oracles); the seller starter is **exact-only**.
6. **Subscription sellers** — if the user needs hourly/daily/monthly access windows, use [x402-subscription-starter](https://github.com/miraland-labs/x402-subscription-starter) and [references/subscription-exact-rail.md](references/subscription-exact-rail.md); Tier B JWT auth is [miralandlabs/subscription-auth](https://github.com/miralandlabs/subscription-auth) (individual account — not `miraland-labs`), not a new payment rail.

## Live documentation

Production facilitator (default):

- [https://ipay.sh/agent-integration.md](https://ipay.sh/agent-integration.md)
- [https://ipay.sh/quickstart-seller.md](https://ipay.sh/quickstart-seller.md)
- [https://ipay.sh/seller-quick-start.md](https://ipay.sh/seller-quick-start.md)
- [https://ipay.sh/openapi.json](https://ipay.sh/openapi.json)

Devnet equivalents live under `https://preview.ipay.sh/…` when testing on Devnet.

## Related hub skills

- **`pr402`** — entry router when integrator role is unclear
- **`pr402-facilitator`** — only when **editing** the Rust facilitator, not when integrating as a seller
- **`pr402-buyer`** — when the same project also needs a paying agent client
