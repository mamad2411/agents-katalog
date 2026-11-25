---
name: kappmaker-revenuecat
description: Configure RevenueCat for a KAppMaker app — entitlements, connected store products, offerings and packages, via the CLI or the RevenueCat MCP server. Use when the user mentions RevenueCat, or asks who handles entitlements, subscription state or paywall delivery and their project uses RevenueCat. To create the store products themselves use kappmaker-monetization; for Adapty use kappmaker-adapty.
---

# KAppMaker — RevenueCat

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.
3. **API key** — a **secret API v2 key** (`sk_…`) from the RevenueCat dashboard (Project settings →
   API keys → V2). A v1 key will not work — and **v2 keys are per-project**: the key is minted
   inside one project and can only see that project, so each app needs its own. Pass it once with
   `kappmaker revenuecat setup --api-key sk_...` and it is saved for that app (keyed by bundle ID in
   `~/.config/kappmaker/revenuecat-keys.json`); every later command finds it automatically.
   Resolution order: `--api-key` → `REVENUECAT_API_KEY` env → the per-app map → the global
   `revenuecatApiKey` config value (a fine shortcut when the account has only one app).

### revenuecat setup — Provider Setup

**Syntax**: `kappmaker revenuecat setup [--config <path>]`

**Syntax**: `kappmaker revenuecat setup [--config <path>] [--api-key <sk_...>]`

**Prerequisites**: an API key resolvable per the order above (no external CLI — talks straight to
`api.revenuecat.com/v2`). The RevenueCat **project** must already exist in the dashboard. Because
the key is project-scoped, it identifies the project by itself — no project ID to configure. The
command also cross-checks: a config carrying one project's ID with a key from another fails loudly
instead of writing into the wrong project.

**Config file**: `./Assets/revenuecat-config.json`. If missing, prompts for app name / bundle ID /
package ID and writes one from the built-in template (2 subscriptions + 3 credit packs, same
defaults as the Adapty template).

**What it does** (7 steps): validate key → load config → find/create the App Store + Play Store
apps → entitlements (`premium`, `credit_pack_access`) → connect store products → attach products
to entitlements → offerings (`default`, `credits_pack`) with one package per product.

**Product ID alignment** — same generator as ASC / Play / Adapty, so IDs line up with what
`create-appstore-app` and `gpc setup` created. One RevenueCat-specific rule: **Play subscriptions
are connected as `productId:basePlanId`** (e.g. `myapp.premium.weekly.v1:autorenew-weekly-699-v1`)
— RevenueCat rejects the bare subscription ID as ambiguous. Play one-time products and all iOS
products use their plain IDs.

**Packages** use RevenueCat's standard keys (`$rc_weekly`, `$rc_monthly`, `$rc_annual`, …); credit
packs get `credit_pack_<credits>`. The credits offering identifier is `credits_pack` — the same
constant the app code already uses for Adapty's placement, so the mobile code keeps one constant
regardless of provider.

**Idempotent re-runs**: everything is find-before-create (entitlements by lookup_key, products by
store identifier, offerings/packages by lookup key); "already attached" errors on re-attach are
swallowed. Safe to rerun any time.

**Dashboard-only steps** (the command prints this checklist): App Store Connect API key upload,
Play service credentials upload, copying the per-app public SDK keys (`appl_…` / `goog_…`) into the
mobile app, and marking `default` as the current offering. RevenueCat cannot validate purchases
until the store credentials are uploaded.

### The RevenueCat MCP server — dashboard work in conversation

RevenueCat also ships an MCP server: endpoint `https://mcp.revenuecat.ai/mcp`, authenticated with
the same v2 secret key (Bearer) or OAuth. When it is connected in the session, you can inspect and
manage projects, apps, products, entitlements, offerings and packages conversationally — useful for
one-off questions ("what offerings exist?", "attach this product to premium") without running the
full setup. The CLI flow above remains the right tool for the repeatable, config-driven setup;
the MCP is for ad-hoc inspection and small corrections. Do not mix the two mid-flow — finish a
`revenuecat setup` run before making MCP-side edits, or the run's find-before-create logic will
see half-finished state.

### Pushing ONE new product later

Don't re-run the full setup to add a product — `kappmaker subscription add` / `kappmaker iap add`
push to the stores AND mirror into the provider(s) the project uses. See **kappmaker-monetization**
for the flags; `--provider revenuecat` forces the RevenueCat push when no config file exists yet.

---

## Where this sits in the flow

- **Before this:** **kappmaker-monetization** — create the store products first; RevenueCat
  connects to them by store identifier.
- **After this:** Paywall work in the app itself (fetch offering `default` / `credits_pack` via the
  RevenueCat SDK).
