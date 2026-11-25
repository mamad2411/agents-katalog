---
name: kappmaker-adapty
description: Configure Adapty for a KAppMaker app — the subscription provider dashboard, products, paywalls and SDK keys. Use when the user mentions Adapty, or asks who handles entitlements, subscription state or paywall delivery and their project uses Adapty. For RevenueCat use kappmaker-revenuecat; to create the store products themselves use kappmaker-monetization.
---

# KAppMaker — Adapty

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### adapty setup — Subscription Management

**Syntax**: `kappmaker adapty setup [--config <path>]`

**Prerequisites**:
- `adapty` CLI installed (`which adapty`; auto-installs via npm if missing)
- Adapty authentication (CLI handles via browser OAuth)

**Config file**: Looks for `./Assets/adapty-config.json`. If not found, prompts interactively.
- Global defaults at `~/.config/kappmaker/adapty-defaults.json` are used as base layer.

**What it does** (8 steps): Create/find app, set access level, create products (with iOS/Android IDs), create paywalls, create placements.

**Product ID format**: Aligned with App Store Connect AND Google Play Console so Adapty links them across all three systems automatically.

For subscriptions: `ios_product_id` = `{appname}.premium.{period}.v1.{price}.v1`, `android_product_id` = `{appname}.premium.{period}.v1`, `android_base_plan_id` = `autorenew-{period}-{priceDigits}-v1`. Routed to access level `Premium`.

For credit pack IAPs (entries with `credits` field): `ios_product_id` = `android_product_id` = `credit_pack_{credits}_{priceDigits}_{appname}`. `android_base_plan_id` is left empty (IAPs have no base plan). **Period is `consumable`** and the product is routed to a separate `credit_pack_access` access level (so buying a credit pack does not grant the recurring `Premium` entitlement).

**Adapty CLI consumable-period workaround**: the Adapty CLI v0.1.5 hardcodes a period whitelist that excludes `consumable`. KAppMaker bypasses this for credit packs by hitting Adapty's REST API directly (using the auth token cached at `~/.config/adapty/config.json` or `ADAPTY_TOKEN` env var). Subscriptions and lifetime products still go through the CLI. No user-visible difference; just a transparent fallback.

**Prices are not developer-set in Adapty**: the `price` field in `Assets/adapty-config.json` only drives ID generation (and mirrors into ASC/GPC). Adapty's developer API explicitly strips price fields from product creation — verified via OPTIONS metadata ("Strips response to plan-specified fields (id, title, vendor_products)"). Prices appear in the Adapty dashboard only after the user connects App Store Connect and Google Play integrations there (dashboard-only step; not exposed via CLI/API). When users complain that prices are missing in Adapty, point them to: Adapty dashboard → Settings → Integrations → connect ASC (paste the same `.p8` / Key ID / Issuer ID they used for `kappmaker create-appstore-app`) and Google Play (upload the same service-account JSON used by `kappmaker gpc setup`). The mobile Adapty SDK already shows correct prices in-app — it fetches them from native store APIs at runtime regardless of dashboard state.

**Multi-access-level config shape**: `access_levels: [...]` (plural) replaces the legacy single `access_level`. Each product has an `access_level_sdk_id` field linking it to one of the access levels. Existing configs with the legacy field auto-migrate on load.

**Default Credits Paywall + placement**: The Adapty template ships with a `Credits Paywall` containing the 3 default credit packs and a `Credits` placement (developer_id `credits_pack`). App code fetches it with `Adapty.getPaywall("credits_pack")`.

**Idempotent re-runs**: `adapty setup` lists existing products / paywalls / placements first and skips ones already present. Safe to rerun at any time.

**Prerequisite ordering**: If the user wants Adapty on Android, the Play Console products must exist first. The `create` orchestrator handles this automatically (step 8 runs `gpc setup` before step 9 runs Adapty), but if invoked standalone, tell the user to run `kappmaker gpc setup` (or at least `gpc subscriptions push`) before `kappmaker adapty setup`.

---

## Where this sits in the flow

- **Before this:** **kappmaker-monetization** — create the store products first; Adapty references them.
- **After this:** Paywall work in the app itself.
