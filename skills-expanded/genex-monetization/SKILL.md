# Genex payments in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's monetization card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Genex's currency is Nex; the card below calls it coin. Anything with a fixed price in Nex (a
  class or level unlock, a skin, an item), or anything the person wants to sell for real money
  without naming a currency, is a Genex store item, listed with `shop add` and its picture at any
  time (the `genex-items` skill, `genex__skill {"name":"genex-items"}`), whatever the card below
  says about catalogs. A price
  in coins, gold or gems is the game's own currency, unless the person says it is for real money:
  then it may be Nex.
- The card's dynamic payment requests (`requestPayment`, `getPayment`, `getPayments`) are only for
  an amount decided while playing, such as a player-approved action. They need no CLI call.
- Studio's `@genex-ai/embed-sdk` already exports them. Add the package with
  `genex__package {"package":"@genex-ai/embed-sdk"}` if the game does not have it yet; never run
  `npm install` for it. In a game made from Studio's template, import them from
  `"@genex-ai/embed-sdk"` and never call `initEmbed()`: Studio's connect module does, as the
  `genex-threejs-embed-auth` skill describes.
- Studio's preview runs in local test mode, which has no wallet: a payment there never opens the
  platform sheet. Check the buttons, layout and delivery code with the game's own test fixtures.
  A real payment needs a build published on Genex (`genex__publish`), a signed-in player and that
  player's confirmation.
- Store items (a picture, a description, a draft the person puts on sale, items other games can
  use, another creator's item) follow the `genex-items` skill, which says how Studio runs
  `genex shop add … --json` and `genex items add`.
- The card's "Existing catalog items" commands are how every store item is listed in Studio:
  `npx genex shop list` is `genex__cli {"command":"shop list"}`, `npx genex shop add` is
  `genex__cli` with the item name in `args` and the flags by name in `options` (a draft, which asks
  nobody), and `npx genex shop set|remove|test` on an item in the store is `genex__cli-paid` with the sku in
  `args` (on a local draft, `genex__cli`). The
  user approves each paid call, because it changes what the game sells. `genex shop publish` is not
  available: Studio puts the game's items on sale when it is published.
- Other commands map onto Studio tools as the `genex` skill describes
  (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-monetization/SKILL.md v1.40.0 sha256 0eacdccdfa4851c2380a71a713ec33c2179673bd27cb8aed7518791181421e69 -->
---
name: genex-monetization
description: Sell things in a Genex game for Nex, the currency players buy with real money — fixed-price Genex store items (`genex shop add`) by default, dynamic payment requests only for amounts decided while playing. Use when the player asks to sell things, add a shop, monetize, or make the game earn. Carries the hard rules: no paid randomness, no gambling, no donation mechanics, and a real-money price beside every Nex price.
---

# Genex Monetization

Genex's own currency is **Nex**: players buy it with real money and spend it in
the Genex store. Spending it inside a game is a ledger movement the game never
touches. You design what is for sale; the platform owns the wallet, the
confirmation, and the money. Nex is a name: "1,200 Nex", never "Nexes".

Load this when the user asks to sell something or add payments.

## Which currency the person means

- **A price in Nex means a Genex store item.** It is listed with
  `npx genex shop add … --json`, before or
  after the first publish (a folder with no linked game keeps a local draft).
  Price it from the store's grid: `npx genex shop list` prints it, and a price
  off the grid is refused with `price_off_grid`. The person puts it on sale.
  `$genex-items` owns the steps.
- **A price in coins, gold, gems or any other name is a currency of the game's
  own**, earned by playing (see the per-game currency note below). If the
  person also says it is for real money, ask once whether they mean Nex.
- **Selling something for real money with no currency named** ("paid
  characters", "sell skins") means Nex store items.

## Store items first, payment requests for amounts decided in play

Anything with a fixed Nex price is a **store item** (`$genex-items`): a sword,
a skin, a character, a level pack, a boost. The store draws its card, its
purchase sheet and its receipt; the game delivers it from `getEntitlements()`.

A **dynamic payment request** (`requestPayment()`, below) is only for an amount
decided while playing: a player-approved action whose price the run sets, or a
top-up of a size the player picks. Never wrap a fixed-price item in one.

## The hard rules, and the test that generalizes them

Before you build ANY purchasable thing, run this test:

> **Does the player pay?** (with Nex, or with anything bought with Nex —
> directly or indirectly, including a per-game token or key that Nex bought.)
> **Is the outcome uncertain when they pay?**
> **Is there a prize** — an item, currency, or advantage they wanted?
>
> **All three yes = paid randomness. Build the deterministic version instead.**

That triad is the test used by every app store to identify gambling, and it
catches mechanics that do not exist yet — which a list of banned names cannot.

Four things are never built, whatever the request:

1. **No paid randomness.** No loot boxes, gacha, mystery boxes, crates, packs,
   prize wheels, raffles, "spin for a bonus", "chance to double your Nex".
   Directly or indirectly.
2. **No gambling in Nex.** No wagering, staking, betting, coinflips, casino or
   slot mechanics denominated in Nex or in anything Nex buys.
3. **No donation or begging mechanics.** No "donate to me" prompts, tip jars, or
   player-to-player Nex transfers. Nex buys goods; it never just moves.
4. **No pressure.** No countdown timers, "ends in", "limited time", "only N
   left", or stock counters anywhere in the shop.

**Randomness the player EARNS by playing is gameplay, not commerce, and is
completely fine**: an enemy dropping a random item, a chest you found in the
level, a procedural layout, a critical-hit roll, a shuffled deck. The line is
what triggered the roll — play, or payment. Build those freely.

Genex refuses paid randomness outright rather than allowing it with disclosed
odds. That is stricter than any app store, and it is why no Genex game needs an
odds table, an age gate, or a per-country check.

### When a request crosses a line

Name the rule it crosses and build a compliant version. Never build the banned
version "as an option" or a partial one. There is no escalation path.


## Store items (the default)

Every fixed-price item is a Genex store item. `$genex-items` owns making one —
its picture, its description, the draft the person puts on sale, items other
games can use, and adding another creator's item. Its rules add to these; they
never replace them.

```bash
npx genex shop list   # the price grid in Nex, and this game's items
npx genex shop add "Iron Key" --price 100 --type durable --json
npx genex shop test <sku-id>  # owner-only free entitlement; no Nex moves
```

When the Genex
store is on, `genex shop add` makes a draft: `getShop()` leaves it out of the
live game and `buy()` cannot sell it until the person puts it on sale. `--json`
makes the Genex app show its **Put on sale** card; never put it on sale
yourself. Before the game is published, items can be made all the same: they
wait as local drafts and go up as drafts with `genex publish`; still, only the
person puts one on sale. With the store off, the item is on sale at once:
tell the person so.

`getShop()` reads store items even for guests and preview builds;
`buy({ skuId })` requests their platform confirmation. Prices follow the grid
printed by `genex shop list`. Render `name`, `iconUrl`, `priceCoins` (the price
in Nex) and `priceDisplayUsdCents`. `genex shop set` edits a listing and `genex shop remove` retires it
without removing a buyer's ownership.

Re-list `getEntitlements({ excludeConsumed: true })` on boot. Branch on
`skuType` (`consumable`/`durable`), never `type` (purchase/gift/test/free).
For a consumable, await `consumeEntitlement(id)` BEFORE applying its effect
and skip `alreadyConsumed: true`. This prevents repeated delivery but a crash
between consume and save can lose that effect; do not promise atomic game-state
delivery. A durable ownership unlock is never consumed: restore it from the
entitlement on every boot. Dynamic receipts do not use this consumption API.

## Dynamic payment requests (amounts decided in play)

Only for an amount the run decides — a player-approved action whose price play
sets, a top-up of a size the player picks. A fixed price is a store item
(above). From `@genex-ai/embed-sdk`, after `initEmbed()` and player identity
are ready:

```ts
import { requestPayment, getPayment, getPayments } from '@genex-ai/embed-sdk';

// Prepare and save this order AND its promised action before enabling the button.
// Generate its id once. Keep the same id and terms across retries and reloads.
const order = {
  orderId: 'unlock-iron-gate-run-42',
  title: 'Open the iron gate',
  description: 'Unlock the shortcut for this run.',
  amountCoins: 75, // Nex, set by this run: the gate's toll grows with depth
};

buyButton.addEventListener('click', async () => {
  const result = await requestPayment(order); // first async operation in the click
  if (result.status === 'canceled') return;
  if (result.status === 'succeeded' && result.payment) {
    await applyPaidOrderOnce(result.payment); // your saved, idempotent game action
    return;
  }
  if (result.status === 'pending') {
    showMessage('Payment is still being checked.');
    return; // recover this order; do not create a replacement charge
  }
  showMessage('Purchase did not complete.');
});
```

A payment request needs no `genex shop add`, SKU id or item icon: it buys a
described game action whose amount was decided in play. The hard rules above
still apply. The game never supplies a recipient: the platform uses the game's
own split. This API is for Nex commerce; in-game LLM requests use their own
funding and consent flow (`$genex-llm-in-games`), not a payment wrapped around
a model call.

The server freezes `title`, `description`, `amountCoins` and the real-money
value before Genex asks the player. **Creating a request neither debits nor
reserves Nex.** Only the player's explicit confirmation on the platform
surface can move money. The game cannot draw, skin or confirm that sheet.

An `orderId` belongs to this player in this game. The same id with the same
terms returns the same payment, including a terminal result. Changing its terms
returns `payment_conflict`. After an order is canceled or expired, a deliberate
new purchase gets a new id; a network retry never does. Do not generate ids
inside a retry loop or replace them just because the SDK stopped waiting.

### Confirmation and results

**Call `requestPayment()` synchronously from the click handler.** On the game's
own origin it reserves a popup while the user gesture is live, then fills it
with the platform confirmation. Awaiting a save or fetch first can block it;
prepare and persist the order before enabling its purchase button.

The result has `status`, optional `payment` (the receipt), and optional `message`.
Statuses are `succeeded`, `canceled`, `expired`, `insufficient_balance`, `failed`
and `pending`. A timeout or uncertain response is `pending`: it is not proof of
failure and not permission to apply the action or charge again. `canceled` is
ordinary player choice; do not show an error for it.

**Your game cannot read the player's Nex balance.**
The wallet spans the platform; Genex shows the balance and handles consent.
Only fulfil a payment whose authoritative receipt says `succeeded`.

The surface depends on the shell (`$genex-threejs-embed-auth`,
`references/shells.md`):

- **On the game's Genex page the sheet is drawn above the game.** To show it,
  the page leaves fullscreen first, and the SDK lets go of the
  pointer lock before it asks. Fullscreen and pointer lock come back only from
  a later click or key press.
- **The Genex app has no purchase surface yet.** `requestPayment()` fails
  without opening a sheet, and `buy()` resolves
  `failed` without opening anything too. When `getShell()` from `@genex-ai/embed-sdk` is `"app"`,
  hide payment buttons or make the shop browse-only; do not show a failure toast.
- Local test mode has no wallet. Preview builds cannot spend real Nex either.
  Verify layout and delivery with game-owned test fixtures; a real payment needs
  a published build, a signed-in player and explicit platform consent.

### Receipts and delivery after a restart

```ts
const payment = await getPayment(savedOrderId); // null only when not found
if (payment?.status === 'succeeded') await applyPaidOrderOnce(payment);

let cursor: string | undefined;
do {
  const page = await getPayments({ cursor, limit: 100 });
  for (const receipt of page.payments) await applyPaidOrderOnce(receipt);
  cursor = page.nextCursor ?? undefined;
} while (cursor);
```

`getPayment()` returns any status for one order; read/network errors throw and
are not absence. `getPayments()` lists successful receipts, scoped to the
current player and game. Follow `nextCursor` to completion. Use the per-order
read for a known pending request, and scan receipts on boot before purchases
can affect play.

A receipt has `id`, `orderId`, `title`, `description`, `amountCoins`,
`priceDisplayUsdCents`, `status`, `failureCode`, `createdAt`, `paidAt` and
`expiresAt`. It proves payment, **not delivery of the promised game action**.
It creates no platform entitlement and nothing the resale market can list.

`applyPaidOrderOnce` is game code, not an SDK helper. Bind the saved `orderId`
to the promised action before requesting payment. For an unlock, set the same
ownership flag every time. For a one-time quantity change, save the changed
state and the fulfilled receipt id together; replaying the receipt must be a
no-op. A game with its own backend should enforce the receipt's unique id in
that backend's transaction. Never use receipt titles as executable instructions
or apply an effect just because the confirmation window closed.

Test recovery after closing the tab, a repeated success receipt, a delayed
response and a canceled order. Also check concurrent fulfillment if the game
permits multiple tabs; two read-modify-write saves are not a transaction.
Do not make a real-money purchase automatically to test the feature.

## Checklist

- [ ] Every fixed Nex price is a store item, listed with
      `genex shop add … --json` at a grid price, left for the person to put on sale
- [ ] A dynamic payment carries only an amount decided in play; its saved order
      binds one stable id, exact terms and promised action
- [ ] `buy()` and `requestPayment()` start directly from a click/tap
- [ ] Genex shows the frozen Nex and real-money price and receives consent
- [ ] No payment buttons in the Genex app
- [ ] Cancellation is silent; uncertain outcomes remain pending
- [ ] Recovery reads entitlements and receipts before applying any paid action
- [ ] Fulfillment is idempotent, including reload and concurrent-tab cases
- [ ] No paid randomness, Nex wagering, donation prompt or pressure timer
- [ ] Nothing sold is unreachable without paying

## Troubleshooting

**The confirmation window was blocked** — an `await` ran before
`requestPayment()`, or there was no click. Persist the order earlier and make
the payment request the click handler's first async operation.

**`payment_conflict`** — the same order id was reused with different terms.
Recover its original request; create a new id only for a new purchase.

**`pending` or an interrupted tab** — use `getPayment(orderId)`. Never assume
failure, issue a replacement charge, or deliver while the status is uncertain.

**Payment succeeded but nothing happened** — find the saved order's action and
recover its receipt. The platform records payment; the game owns fulfillment.

**The player got the effect twice** — delivery did not deduplicate by receipt
id or the save update raced. Fix fulfillment; do not change the order id.

**`guest_no_wallet`** — ask the player to sign in before purchase.

**`staging_no_purchase`** — previews cannot spend; verify layout there and use
a published build for an explicitly approved real purchase.

**`surface_cap`** — the amount exceeds the server's limit for this confirmation
surface. Do not split it into smaller hidden charges to bypass the limit.

**`price_off_grid`** — a store item's price is not on the grid. The refusal
prints it (so does `genex shop list`); pick a price from it, or 0 for Free.
Dynamic payments accept whole amounts subject to their own caps.

**Everything Nex-related 404s** — Nex commerce is off on this stand.
