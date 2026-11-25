---
name: kappmaker-asc
description: Set up an app on App Store Connect (ASC) for iOS — the app record, bundle ID and App Store listing. Use when the user mentions App Store Connect, ASC, the iOS App Store or an iOS listing.
---

# KAppMaker — App Store Connect

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### create-appstore-app — App Store Connect Setup

**Syntax**: `kappmaker create-appstore-app [--config <path>]`

**Prerequisites**:
- `asc` CLI installed **≥ 1.4.0** (`brew install asc` or `brew upgrade asc`; the bulk-CSV `subscriptions pricing prices import` command used by KAppMaker 1.7.0+ requires this version)
- Repo location: https://github.com/rorkai/App-Store-Connect-CLI (renamed from rudrankriyam in 2026)
- Config keys: `ascKeyId`, `ascIssuerId`, `ascPrivateKeyPath` (for API auth)
- `appleId` — now required (used by both `asc web apps create` and privacy setup)

**Config file**: Looks for `./Assets/appstore-config.json`. If not found, prompts interactively.
- Global defaults at `~/.config/kappmaker/appstore-defaults.json` are used as base layer.

**What it does** (13 steps): Register bundle ID + enable capabilities (Sign in with Apple, In-App Purchases, Push Notifications), create/find app (fully automated — no manual ASC step needed), set content rights, create version, set categories, age rating, localizations, pricing, subscriptions, **consumable in-app purchases (credit packs)**, privacy, encryption, review contact.

**Default credit packs**: 3 CONSUMABLE IAPs ship in the template (`Basic` 10 credits / $4.99, `Pro` 30 / $9.99, `Ultimate` 80 / $19.99). Auto-fill turns each into `credit_pack_{credits}_{priceDigits}_{appname}` (e.g. `credit_pack_10_499_myapp`) — same product ID is used on Google Play and Adapty so the app code only needs one constant. Credit-pack auto-fill triggers on any `in_app_purchases[]` entry with a `credits` numeric field; other custom IAPs are left alone (the user's `product_id` wins). Created via `asc iap setup` — idempotent on rerun.

**Tip**: Before running, you can help the user review or create the `Assets/appstore-config.json` file. Read the existing config and explain each section. The user can edit it before running.

**Per-territory PPP pricing (1.7.0+ — bulk CSV import)**: subscriptions and IAPs are fanned out to **every ASC territory (~175)** with PPP-adjusted prices in ONE API call per product.
- **Subscriptions**: `asc subscriptions pricing prices import --input <csv>` (added in asc 1.4.0). CSV columns `territory,price,price_point_id`; KAppMaker writes a temp file and pipes it in. Omits `--start-date` so rows are treated as starting prices (Apple rejects future-dated rows when the territory has no starting price yet: "Create a starting price before creating future prices").
- **IAPs**: `asc iap pricing schedules create --prices "PP_ID:DATE,…"` (already batch).
- **Tier resolution**: Apple's price-point catalog uses globally-stable tier numbers (1..800; tier N = same USD-equivalent across all territories). Resolve each unique PPP USD target → tier ONCE via USA's catalog (USD-priced), then synthesise per-territory price-point IDs locally using Apple's base64 `{s, t, p}` format. Critical bug fix vs 1.6.x — old code numerically compared a USD target to local-currency prices (¥, ₩, ₹) and picked the FREE tier, silently landing products at $0 in JPN/IDR/INR/KRW/etc.
- **Distinct catalogs, distinct IDs**: subscriptions = `subscriptionPricePoints` (`s` = subscription-internal ID); IAPs = `appPricePoints` (`s` = app ID). Mixing IDs returns `400 The provided entity is invalid`.
- **Idempotent re-runs**: existing subs/IAPs now refresh pricing instead of being skipped (1.6.x silently skipped → users couldn't re-price legacy products).

**App Review screenshots (1.7.1+)**: Apple requires a review screenshot on every subscription and IAP — without one, products stay in `MISSING_METADATA` state. Config field `review_screenshot` (top-level, plus optional per-product override on each sub/IAP). Required size: **1290 × 2796 px** (iPhone 6.7" Display, portrait — matches App Store listing screenshots); minimum 640 × 920 px. Uploads via `asc subscriptions review screenshots create` (subs) and `asc iap images create` (IAPs). Idempotent during `create-appstore-app` (skips when one is already attached); silently skipped when the file at the given path doesn't exist.

**Auto-resize prompt (1.7.3+)**: when the file's dimensions don't match 1290 × 2796, KAppMaker prompts `Resize to 1290×2796 keeping aspect ratio? (Y/n)`. Y → sharp resize with `fit: 'inside'` (preserves aspect ratio, may produce 1290×726 from a 16:9 source) → temp file → upload. N → uploads as-is. Files already at 1290×2796 skip the prompt.

**Standalone monetization push (`appstore-monetization-push`)**: when the user wants to re-sync subscriptions + IAPs (refresh PPP pricing, add a new product from the config) without running the full 13-step `create-appstore-app` flow, use `kappmaker appstore-monetization-push [--subscriptions-only | --iap-only] [-c|--config <path>]`. Reads `Assets/appstore-config.json`, resolves the app by `app.id` or `app.bundle_id`, then calls the same `setupSubscriptions` / `setupInAppPurchases` functions — fully idempotent (existing products get pricing refreshed).

**Standalone REPLACE commands (1.7.3+ — `appstore-` prefix)** for swapping screenshots without re-running the full setup flow:
- `kappmaker appstore-update-subscription-review-screenshot [--file <path>] [--config <path>] [--product-id <id>]`
- `kappmaker appstore-update-iap-review-screenshot [--file <path>] [--config <path>] [--product-id <id>]`

`--file` applies to all matched products; without it, the commands use the per-product `review_screenshot` from the config. `--product-id` targets a single product. These commands FORCE-REPLACE existing screenshots by delete+create — empirically `asc … update` (both `screenshots update` and `images update --file`) doesn't actually swap the file on Apple's side, only marks the record as "uploaded".

---

## Where this sits in the flow

- **Before this:** **kappmaker-new-app** (bundle ID comes from the project).
- **After this:** **kappmaker-aso-metadata** for the listing text, **kappmaker-screenshots**, then **kappmaker-publish**.
