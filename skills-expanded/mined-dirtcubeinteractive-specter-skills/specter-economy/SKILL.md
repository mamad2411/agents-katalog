---
name: specter-economy
description: >-
  Specter game economy — virtual currencies and wallets, items, bundles, stores and in-game
  purchases, player inventory (add, remove, equip, consume), gacha / loot boxes with pity system,
  currency conversion, collections, and real-money gaming (RMG deposits, withdrawals, real-money
  wallets). Use for any "add coins/gems", "in-game store", "buy item", "inventory", "loot box",
  "wallet balance" or real-money feature built on Specter.
---

# Specter Economy — currencies, wallets, stores, inventory, gacha, RMG

Base URL and headers: see the `specter` skill. Catalog reads (`app/get-*`) need only `api-key`;
player actions need `Authorization: Bearer` too.

Configure the economy (currencies, items, bundles, stores, prices) in the dashboard at
https://console.specterapp.xyz — the API consumes that configuration.

## Model

- **Currency** → defined per project; *virtual* (coins, gems) or *real-money*. Each player gets a
  **wallet per currency**, auto-created at signup. Real-money currencies create three wallets:
  deposit, winnings, bonus.
- **Item** → ownable thing with properties (consumable, equippable, tradable, stackable…),
  optional unlock conditions, prices.
- **Bundle** → a container of items/currencies, openable; **gacha bundles** have weighted random
  contents and a pity counter.
- **Store** → categorized storefront of items/bundles with prices (virtual currency, real money,
  or IAP-mapped).

## Wallet operations

| Endpoint | Auth | Purpose |
|---|---|---|
| `player/me/get-wallet-balance` | Bearer | Player's balances — requires `currencyIds` (min 1); there is no fetch-all. Get currency IDs from `app/get-currencies` or the login response's `currencies[]` |
| `wallet/update-balance` | Bearer | Credit/debit a currency (e.g., match reward, sink) |
| `wallet/convert-currency` | Bearer | Convert between currencies per configured rates |
| `wallet/available-conversions` | Bearer | What conversions exist |
| `player/me/get-rm-wallet-history` | Bearer | Real-money transaction history |
| `player/get-wallet-balance` | Bearer | Another player's balance |
| `app/get-currencies` (`get-currencies`) | api-key | Currency catalog |

In wallet calls, `currencyId` is the human-readable currency ID configured in the dashboard
(e.g. `"coins"`), not the numeric `uuid` (verified on staging). Wallets are provisioned within
seconds of signup — a freshly signed-up player returns `balance: 0`, not an error.
`wallet/update-balance` responds with `{ balance, requested, applied, wasAdjusted,
adjustmentReason }` — check `applied`/`wasAdjusted` rather than assuming the full amount landed.

Balances change asynchronously when rewards are granted by tasks/leaderboards/tournaments —
re-fetch after such events instead of assuming immediate credit.

## Stores & purchases

Browse: `app/get-stores`, `app/get-store-categories`, `app/get-store-category-contents`
(api-key, cacheable) or player-aware `stores/get-*` variants (Bearer — applies unlock state).

Buy:
- `stores/default-purchase` (Bearer) — standard flow: validates price, debits wallet, grants
  item/bundle to inventory, writes wallet transaction. Use this unless you have a reason not to.
- `stores/custom-purchase` (Bearer) — custom pricing/override flow.

The response includes the updated state; treat insufficient-balance as a normal, user-facing case.

## Inventory

| Endpoint | Purpose |
|---|---|
| `player/me/get-inventory` | Owned items/bundles (paginated, filterable) |
| `inventory/add` / `inventory/remove` | Grant/take items outside a purchase |
| `inventory/equip-unequip` | Loadout state |
| `inventory/consume-item` | Decrement a consumable |
| `inventory/open-bundle` | Open a bundle → contents land in inventory/wallets |
| `player/me/get-collections` | Collection progress |

## Gacha / loot boxes

`app/get-gacha-bundle-config` (drop tables, pity rules) → `inventory/open-gacha-bundle` (Bearer,
performs the roll server-side) → `inventory/get-pity-status` (progress toward guaranteed drop).
Never roll client-side; the server is authoritative.

## Real-money gaming (RMG)

For games with cash deposits/withdrawals (where legal — these endpoints enforce the project's
configured policy):

`rmg-get-policy` → `rmg-create-order` → `rmg-validate-deposit` → `rmg-execute-deposit`;
withdrawals mirror with `rmg/validate-withdrawal` / `rmg/execute-witdrawal` (note: the live
route really is spelled `witdrawal` — match it exactly). Funds move between
the player's deposit/winnings/bonus wallets. Tournament entry fees and prize payouts integrate
with these wallets (see specter-competitions).

## Full endpoint details

All endpoint DTOs and response examples: [references/endpoints-index.md](references/endpoints-index.md)
Working client code: [examples/javascript.md](examples/javascript.md)


## Product manual (concepts & terminology)

The Specter **user manual** (the same docs game designers read in the dashboard) is bundled in
[references/manual-index.md](references/manual-index.md) — read it to understand the CONCEPTS and
intent behind this domain (what each type/feature means, how dashboard workflows map to the API),
then pair it with the endpoint references for exact request shapes.


## Client (v2) API — what you call FROM your game

The **game-side** endpoints (all `POST /v2/client/*`, authed with the project api-key + a player
access token for player-scoped calls) are indexed with full request DTOs + auth in
[references/client-api-index.md](references/client-api-index.md). Use these for code that ships in
the game/app. **Never call the `/v1/*` admin API from game code** — that's dashboard-only.
