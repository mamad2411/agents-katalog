# Under the Leaves

The official game manual (rules) is at [docs/manual.md](docs/manual.md).

**Mandatory rule:** before investigating, diagnosing, or fixing any bug related to game rules (phases, sectors, beings, scoring, etc.), read the manual (docs/manual.md) before concluding whether something is or isn't a bug. Never assume correct behavior from the source code alone, the manual is the source of truth for the rules.

## Build

After editing any `.ts` or `.scss` file, always recompile before considering the change done:

```
npx tsc
npx sass --no-source-map src/sass/undertheleaves.scss undertheleaves.css
```

`undertheleaves.js` and `undertheleaves.css` are build outputs, edit the `src/` sources instead. Both files are synced to the BGA Studio sandbox (sftp), so PHP files under `modules/php/` and these two compiled files all need to be deployed for a change to actually take effect in a live table, including brand new files (easy to forget on selective syncs).

## Game options

- Custom options live in `gameoptions.json` (ids 100+ in this project), and each must have a matching entry registered in `initGameStateLabels(...)` inside `Game.php`'s constructor, mapping a label name to that same id.
- Read them with `getGameStateValue('label') == 2` (this project's convention: `"1"` = Off, `"2"` = On).
- `"beta": true` / `"alpha": true` (like `"firstgameonly"`) go on a specific *value* inside `values`, not on the option itself, e.g. `values["2"].beta = true` marks picking "On" as beta, while "Off" stays a normal option. They show *no* visible mark in the table creation screen; the only effect is a warning shown to players when they actually **start** the game with that value selected (alpha additionally restricts starting to training mode, except for the developer).
- From the client, an option's raw value can also be read directly with `this.bga.tableOptions.get(optionId)` (returns an `int`), as an alternative to threading it through gamedatas.

## `cards.png` sprite sheet

- The sheet is a 6x4 background grid used via CSS `background-size`/`background-position` percentages in `src/sass/cards.scss`, but only 5 columns are real (4 card slots + 1 decorative texture column reused across rows) and only as many rows exist as there are card types with a row (Leaf/Mushroom/Puddle/Tree today).
- The percentage formulas (`background-size: (N*100)% (M*100)%`, position `(100/(N-1))% * i`) must match the sheet's *real* column/row count exactly. A stale divisor only breaks rows/columns nobody uses yet, so it can silently sit wrong for a long time until new content (like the Tree row) lands there. When cards.png changes size, re-measure real pixel boundaries (crop the image, don't guess from stated dimensions) before touching these formulas.

## `CardConfig` stays static

`CardConfig` (`modules/php/Entities/CardConfig.php`) and `Constants::CARD_CONFIGS` are static per-request definitions, not per-game state. Never add dynamic/per-game fields to it (like a card's current owner). Instead:
- Keep dynamic state in `globals` (e.g. `card:tree:owner`).
- Expose it to the client as its own sibling key in `Game::getAllDatas()` (e.g. `treeCardOwnerId`), read straight from `globals`, not nested inside the static config object.
- `CardService::list()` must always return the real `CardConfig` object for a card (never a hand-built array copy of a few fields), because other code (e.g. `ArrivalBeings.php`) dereferences `->dweller` on it.

## Notifications (server side)

- A single-notify being arrival (most `Being/*.php` classes) sends its `notify->all('arrivalX', ..., [...])` immediately followed by `$this->game->notify->all('simplePause', '', ['time' => 600])`, inline. The `beingService->notifyBeingArrivalPause(count)` helper (`count*500+200`) is reserved for the `endProcess()` batch-placement flow (`CollectorMushroomBeing`, `FriendlyPuddleBeing`), not general single-notify cases.
- `player_name` + `playerId` in notif args are auto-colored by the BGA framework, no client formatting needed. Any *other* player name field is not auto-handled: pass only the id from PHP under that same key (e.g. `previous_player` holding a playerId) and have `format.strings.ts` overwrite it in place with `this.game.bga.players.getFormattedPlayerName(id, {})`.
- `${being_icon}` renders a piece sprite (`.undertheleaves-piece[piece="..."]`), only use it for things that actually have a piece there.
- A log-only image placeholder (like `${tile_image}` or `${burly_image}`) should be built in `src/format.strings.ts`, not in the manager class, since that markup only exists for the log. It must never reuse a real element's DOM id (duplicate ids break later `getElementById` lookups elsewhere on the page) and should get a `.notif` CSS modifier to center under the log line (see `.undertheleaves-tile.notif` / `.undertheleaves-card.notif`: `display:block; margin:8px auto 0;`).

## Frontend (`src/`)

- Managers' `setup()` run in the key order of `this.games` in `src/undertheleaves.ts`. If manager B's DOM needs to exist before manager A's setup runs (e.g. `cardManager` inserting into a per-player board built by `playerManager`), order B before A.
- To move an *existing* DOM element to a new container with a slide animation (instead of remove+recreate), use `BgaLocalAnimation` (`src/animation.ts`): `new BgaLocalAnimation(this.game); .setWhere(...); .setOptions(originElement, destinationContainer, durationMs); await .call();`. Same utility used for pieces flying from the void stock and for tiles.

## Debugging on BGA Studio

- The game board runs inside an iframe, so `gameui` is not directly on the top window's console. From the outer console: `document.querySelector('iframe').contentWindow.gameui.gamedatas`.
- `notify->all('log', ...)` is not reliably rendered for ad hoc debugging. To surface a PHP value quickly, temporarily `throw new \Exception('DEBUG ' . var_export($value, true));` at the point in question (BGA shows uncaught exceptions as an error page), then remove it once confirmed.
