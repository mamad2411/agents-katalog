# Shop design (optional advice)

Genex's experience with in-game shops players actually buy from. The hard rules (no paid
randomness, no gambling, no donation mechanics, a real-money price beside every Nex price) and the
APIs are in `genex__skill {"name":"genex-monetization"}` and `genex__skill {"name":"genex-items"}`;
what follows is optional.

## When a request crosses a hard rule

Naming the rule it crosses, in one sentence of why, and offering a compliant version concrete enough
to build tends to land well. Compliant versions that keep most of the feel:

| Asked for | A compliant version |
| --- | --- |
| Loot box, crate, card pack | Every item at a fixed, visible price, plus a visible catalog with a completion track toward a stated reward |
| Gacha, banner, summon | A deterministic unlock: a fixed price, or a stated number of runs |
| Prize wheel, slot machine | A free spin earned by finishing a run, or "pick one of three" with all three visible |
| Casino game | The same game with free chips that reset and can never be bought or cashed out; cosmetics for sale |
| Double-or-nothing, wagers | A skill-based risk inside the run (a harder route, a bigger payout) |
| Betting on matches | Leaderboards with a fixed cosmetic reward the game pays |
| Donate button, tip jar | A gift that is a purchase of a stated item, or a supporter cosmetic |
| Pay to skip a wait | No wait at all, and a permanent upgrade or a cosmetic for sale |
| Limited-time offer | A permanent tiered ladder |
| Pay-to-win boost | Cosmetics, or a boost limited to single-player content |

## A shop worth buying from

- A shop works best on top of a loop that is already worth playing.
- Items that attach to progression the game already has (a class, a mode, a look the player earns
  toward) sell better than items invented for the shop.
- An item that really does what it says in play (the axe that freezes) earns trust; one that does
  nothing earns refunds.
- Prices that relate to play (minutes of play per unit earned in the game's own currency) make the
  Nex price easy to judge.
- A few clear tiers beat a long list; every price on the store's grid.
- Building the item into the game before listing it means what is sold already works.
- The item's picture is the item itself, filling its square; a capture of its own in-game model
  matches what the player gets.
- A new item can be marked as new where the game shows its store.
- Purchases delivered at boot from `getEntitlements()` survive restarts and other devices.
