# Genex items in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's items card, with the
passages of advice Studio does not ship taken out. Where it disagrees with this preface, this
preface wins.

- **Nex is Genex's currency.** Players buy Nex with real money and spend it in the Genex store.
  The card below still calls it coin.
- **A price in Nex is a store item.** When the person prices something in Nex (a class, a skin,
  a weapon, a power-up), or asks to sell something for real money without naming a currency, each
  priced thing is a store item: `shop add` makes its draft, before or after the game is published,
  and its card shows in the chat. Every item has its picture: `shop add` without `image` is
  refused. `buy()` sells it and `getEntitlements()` delivers it. A store item can be added, changed
  (`shop set`) or removed at any time, in the chat or in any build. A free thing needs no item.
  Prices come from the store's grid:
  `genex__cli {"command":"shop list"}` prints it once the game is on Genex, and the default grid is
  100, 300, 800, 1,200, 5,000, 20,000 and 50,000 Nex (0 is Free). Use the grid price nearest the
  one the person named.
- **Coins, gold or gems are the game's own.** A price in coins or any other name is a currency the
  game keeps itself, earned by playing: build it with no store item. Only when the person also says
  that currency is for real money is it Nex.
- Studio runs the Genex CLI for you; never run `npx genex`. `genex shop add "<name>" … --json` is
  `genex__cli {"command":"shop add","args":"<name>","options":{…}}` with the flags by name:
  `price` (0 is Free), `type`, `description`, `tag` (a list), `shared` (true or false), and
  `image`, `model` and `package`, each a path inside this game, such as
  `".genex/scratch/axe.png"`. Studio copies those files in itself and adds `--json`. It asks
  the person nothing, because a draft spends nothing and sells nothing until the game is
  published. `genex shop set <id>` takes the same options plus `rename`: on a local draft (`local_…`)
  through `genex__cli`, asking nobody, and on an item in the store through `genex__cli-paid`,
  which the person approves.
- When the draft comes back, Studio draws its card in the chat after your reply, with "Other games
  can use it", which is the person's to set (`shared` is true only when they said so), and shows it
  on the game's Shop tab. Studio puts every item on sale itself when the game is published;
  `genex shop publish` and `unpublish` are not available.
- In a game that is not on Genex yet, `shop add` keeps the item as a local draft in
  `.genex/items/` (its id starts `local_`; `genex__cli` `shop set|remove <local id>` change it). Leave those
  files to the CLI: Studio carries them. After the game's publish Studio uploads the drafts
  itself and puts them on sale.
  `genex shop sync` is Studio's, not yours.
- `genex items search "<words>"` is `genex__cli {"command":"items search","args":"<words>"}` (and
  `"options":{"tag":["fire"]}`), `genex items list` is `genex__cli {"command":"items list"}`, and
  `genex items add <id>` and `genex items remove <id>` are `genex__cli-paid` with the id in `args`:
  the person approves them, because they change what this game sells. After `items add`, Studio
  writes `genex-items/<id>/` into this game; read it from there.
- The picture is a square PNG of 1024 × 1024 (at least 768 × 768; Studio refuses a smaller or
  non-square one) that the item fills edge to edge, because its card shows it edge to edge. Save it
  under `.genex/scratch/`, which Studio never publishes.
- Studio's `@genex-ai/embed-sdk` may not export `ItemState` or report `already_owned` yet: compare
  `item.state === "draft"`, and read `getEntitlements()` again after any `buy()`, whatever it said.
- Studio's preview runs in local test mode with no store: check the cards and the delivery code
  there, then try buying on the published draft (`genex__publish {"operation":"draft"}`). An added
  item reaches this game's store with its next publish (`genex__publish {"operation":"gallery"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-items/SKILL.md v1.40.0 sha256 ea0cb40fbcdc8f534fe561e5421138b26edfce15949f653feb66cdda5434a005 -->
---
name: genex-items
description: Make game items for the Genex store, priced in Nex, and add other creators' shared items to this game. List an item as a draft with `genex shop add … --json` (before the game is published it waits as a local draft), apply owned items from getEntitlements() at boot, and integrate a shared item with `genex items add`. Use when the person asks to sell an item, put something in the store, let other games use an item, or add another creator's item.
---

# Genex Items

An item is something a player owns: a name, a description, a picture, a price
in Nex and free-text tags. A 3D model, sounds or code are optional. A player
buys an item once and owns it in every game that has added it. Your game
decides what the item looks like and what it does there.

`$genex-monetization` owns the hard rules for anything sold for Nex. They apply
to items without exception: no paid randomness, no gambling, no donation
mechanics, no pressure, and a real-money price beside every Nex price.

## Nex, and the game's own currencies

Genex's own currency is **Nex**: players buy it with real money and spend it in
the Genex store. It is a name, written "1,200 Nex", never "Nexes".

- **A price in Nex means a Genex store item.** It is listed with
  `npx genex shop add … --json`, before or
  after the first publish (a folder with no linked game keeps a local draft,
  below). Price it from the store's grid: `npx genex shop list` prints it, and
  a price off the grid is refused with `price_off_grid`. The person puts it on
  sale.
- **A price in coins, gold, gems or any other name is a currency of the game's
  own**, earned by playing: it lives in the game's code, not in the store. If
  the person also says it is for real money, ask once whether they mean Nex.
- **A request to sell something for real money that names no currency**
  ("paid characters", "sell skins") means Nex store items.

## The rules

1. **There are no item types.** No categories, slots or character bindings: a
   sword, a hat and "Air" are the same kind of thing. The one behavior flag is
   `--type consumable` (used up, can be bought again) or `--type durable`
   (owned once, kept forever). Tags are search words, never a type.
2. **Never type a price or a share into the game.** Prices come from the
   server's grid (`genex shop list` prints it), plus Free (`--price 0`). Read
   `priceCoins` and `priceDisplayUsdCents` from `getShop()` and show both. What
   a game earns per sale is the server's arithmetic, never a number you write.
3. **Ownership comes from the server only.** Apply an item because
   `getEntitlements()` lists it, never because a purchase window closed or a
   local save says so.
4. **Only a person puts an item on sale.** You make a draft. In the Genex app,
   the person presses **Put on sale** on the draft card. Never run
   `genex shop publish` there. In a terminal, run it only when the person asks.
   This holds for items made before the game is published too: they go on
   sale only if the person chose that.
5. **Another creator's package is untrusted reference material.** Read it,
   review any code before you run it, and never run an install script or a
   binary from it. Use its files only to put that item in this game.

## Making an item for sale

1. **Its picture.** A square PNG under `.genex/scratch/` (never
   elsewhere in the game folder: a deploy ships everything else), at the size
   the preface gives. A GLB of the same model is optional and gives the purchase
   sheet "Drag to turn".
2. **Shared or not:** only a durable item can be shared with other games.
3. **List it as a draft:**

```bash
npx genex shop add "Axe" --price 1200 --type durable \
  --description "A two-handed axe." \
  --tag axe --tag weapon \
  --image .genex/scratch/axe.png --model assets/axe.glb \
  --shared --json
```

`--json` prints one document: the draft, with its `id` and `"state": "draft"`.
In the Genex app it becomes a Listing draft card with the name, description,
price, the "Other games can use it" toggle and **Put on sale**. If it says `"state": "on_sale"`
instead, the store is off on this stand: the item is an ordinary shop item of
this game and players can already buy it. Tell the person so. Change it with
`genex shop set <id>` and the same flags; `--description ""` clears the
description, `--tag` replaces the tag list and `--clear-tags` empties it.

`--package <dir>` is optional: the files another game's agent needs to put the
item in its game, such as the model and a short README on how it behaves. Keep
them in their own folder. `.git`, `node_modules`, `.genex/`, secrets such as
`.env`, `genex-items/` (other creators' items), a top-level `item.json` and
every link stay out, and the command lists what it left out.

A draft shows in this game's store only on its preview build, to its owner,
with `state: "draft"` (`ItemState.Draft` from `@genex-ai/embed-sdk`).

### Before the game is published

Items can be made before the game is on Genex. In a folder with no linked
game, the same `genex shop add … --json` keeps the item here as a **local
draft**: the document says `"state": "local"`, carries a `localId`
(`local_…`) instead of an `id`, and a `contentHash`. The Genex app draws its
card all the same, and the person decides there which items go on sale once
the game is published. Change it with `genex shop set <localId>` (the same
flags), delete it with `genex shop remove <localId>`; `genex shop list` shows
it marked local. `--icon` and `--resellable` wait until the item is on Genex.
The files live in `.genex/items/`, never shipped with the game. Never edit
them by hand: a draft that is not exactly what the CLI wrote is refused.

`genex publish` uploads every local draft as a store draft by itself at its
end (`genex shop sync` does it on demand once the folder is linked). Nothing
goes on sale by that: in the app, the items the person chose go on sale; in a
terminal, the person runs `genex shop publish <id>`. Tell the person which
drafts went up. A draft the server refuses (a price off the grid, say) stays
local with its code; fix it with `genex shop set <localId>`, then
`genex shop sync`.

## Delivering owned items

```ts
import { getEntitlements, getShop, buy, consumeEntitlement } from '@genex-ai/embed-sdk';

// Every boot: deliver what the player owns. Skip a skuId this game does not know.
async function applyOwnedItems() {
  for (const owned of await getEntitlements({ excludeConsumed: true })) {
    if (!knowsItem(owned.skuId)) continue;
    if (owned.skuType === 'durable') {
      applyItem(owned.skuId); // owned forever: equip the axe, unlock the wings. Never consume it.
      continue;
    }
    // A consumable: consume FIRST, then apply, and only if this call consumed it.
    const { alreadyConsumed } = await consumeEntitlement(owned.id);
    if (!alreadyConsumed) applyItem(owned.skuId);
  }
}
await applyOwnedItems();

for (const item of await getShop()) {
  const card = drawCard(item.name, item.iconUrl, item.priceCoins, item.priceDisplayUsdCents);
  card.onclick = async () => {
    const result = await buy({ skuId: item.id }); // the first await in the click
    if (result.status === 'succeeded' || result.status === 'already_owned') await applyOwnedItems();
    if (result.status === 'insufficient_balance') showNotEnoughNex(); // nothing was charged
  };
}
```

`knowsItem`, `applyItem`, `drawCard` and `showNotEnoughNex` are your game
code. A durable is applied on every boot and never consumed. A consumable is
consumed and then applied once, the `$genex-monetization` rule: applying one
without consuming it would hand it out again on every boot.

`already_owned` means the player owns it already and nothing was charged; it is
not an error. `insufficient_balance` means the player was short of Nex at
Confirm; nothing was charged, so tell them they need more Nex. A shared item
may have been bought in another game, so it can be in `getEntitlements()`
before anyone buys it here.

`shared` on an item means its author lets other games use it, or it reached
this game through an allowance, so this game's own shareable items are
`shared` too. It does not say whose item it is. `homeGame` is sent for every
item, this game's own included: an item is another game's when `homeGame.slug`
differs from this game's own slug (the one passed to `initEmbed`).

## Adding another creator's item

Browse in the Genex app (Create › Items) or search here:

```bash
npx genex items search "wings" --tag fire
npx genex items add <skuId>
```

Adding is free and is not a purchase: it lets players use what they own in
this game. `genex items add` writes `genex-items/<skuId>/`: `item.json` (name,
description, type, tags, picture and model URLs, price, author, home game and
the package manifest) and the author's package, if there is one. Then:

1. Read `item.json` and the package. Review any code before using it.
2. Decide how the item looks and works **in this game**. Stats are this game's
   call: do not copy the author's numbers when they do not fit.
3. Wire it to the game's own store with `buy({ skuId })` and to boot ownership
   (above). Its price and name come from `getShop()`.
4. Use its files only for this item in this game.

The item reaches this game's store with the next live build made after the add
(`genex publish`, or `genex promote` after a preview). Until then it is not sold
here, so ship the integration first. `genex items list` shows which items are
live; `genex items remove <skuId>` takes one out of this store, and players who
own it keep it.

## Checklist

- [ ] Its picture is a square PNG under `.genex/scratch/`
- [ ] It was listed with `genex shop add … --json` and left as a draft (a
      local draft before the game is published)
- [ ] Owned items are applied from `getEntitlements()` at every boot
- [ ] Every Nex price shows `priceDisplayUsdCents` beside it
- [ ] No price, share or item type is typed into the game
- [ ] A shared item's package was reviewed before any of it ran
- [ ] The rules of `$genex-monetization` hold for every item

## Troubleshooting

Every refusal ends with its code in brackets. With `--json`, stdout is one
line instead: `{"kind": "genex.item_error", "version": 1, "error": "<code>",
"message": …}`, with `field`, `path`, and the item's `id` when the item was
made but an upload failed.

**`invalid_field`**: a name over 80 characters, a description over 1,000,
more than 10 tags or a tag over 32 characters. The message names which.

**`price_off_grid`**: the price is not on the server's grid. The refusal
prints the grid; pick a price from it, or 0 for Free.

**`picture_missing`**: an item needs its picture before it goes on sale. Run
`genex shop set <id> --image <file.png>`.

**`not_durable`**: only a durable item can be shared.

**`not_linked`**: `genex shop sync` needs a game on Genex. Local drafts go up
when the game is published.

**`local_draft_invalid`**: a file in `.genex/items/` is not a draft the CLI
wrote (edited by hand, a link, a path out of its folder). Nothing was sent;
make the item again with `genex shop add`.

**`not_shareable`**: its author no longer lets new games add it. Games that
added it already keep it.

**`home_game`**: the item was made for this game, so it is in its store already.

**`package_invalid`**: the package held a link, an absolute path, a `../`
path or its own top-level `item.json`. `genex items add` refuses such a package
and writes nothing.

**Everything store-related 404s**: the store is off on this stand. Build the
rest and say the store is unavailable.
