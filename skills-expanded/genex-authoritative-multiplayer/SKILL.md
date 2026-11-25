# Genex server-authoritative multiplayer in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's server-authoritative
multiplayer card, with its CLI-only testing section taken out. Where it disagrees with this
preface, this preface wins.

## What Studio runs of it today

- Writing works: the room module, its `authority` block and the client, in any web game made here.
  A Unity game writes the same room module and block (in `genex.json`) with a C# client: follow
  section 5 of `unity__skill {"name":"unity-multiplayer"}`, not this card's client half.
- Shipping works. `genex__publish` (draft or gallery) sends the room module with the build: Studio
  ships `@genex-ai/authority-dev` itself, stages `server/` and every file the module imports beside
  the public copy (never in it), and the publish bundles and validates the module before any game
  file moves. A module that fails stops the publish with each typed reason in the job's error; fix
  the module and publish again. The job's `room` (in `genex__publish-status`) says it plainly:
  `validated` and `uploaded` with the module's `moduleSha256` once it passed and went up with this
  build, or the gate's `failures`; tell the person from it. On Genex's servers the owner needs
  Genex Pro: a free account is refused with `authority_requires_pro` after validation, and nothing
  is uploaded.
- Testing it on this computer works, with `genex__room` in place of the card's
  `npx genex-authority-dev` commands (a game's commands cannot download it):
  - `genex__room {"action":"validate"}` is the publish gate's own check: `{passed, failures}`.
    Run it after every change to the module, and fix each failure before anything else.
  - `genex__room {"action":"start","latencyMs":75}` serves the room on this computer with bots
    and loads the game's preview into it, so the person plays against the bots there. The preview
    takes a seat and your own test client needs another: with the authority block's `maxPlayers`
    the default is that less 2 bots (at most 3), and a `bots` count that leaves no seat free is
    refused by name. `genex__room {"action":"status"}` answers the room's last REPORT, its `ctx.log`
    lines and errors, and `rooms`: more than 1 (its `warning`) means players did not all fit and
    opened another room, so start with fewer bots; the REPORT's `perRoom` lists each room's seats,
    players and bots. A client that joins with a `matchKey` needs the same `"matchKey"` on `start`,
    or the bots play in the game's other pool. Read it while the room runs, as the card's testing reference describes. Stop it with
    `genex__room {"action":"stop"}`. The preview hands the game the room's address through the
    embed SDK's local test mode (`getAuthorityUrls()`): never write the address into the game.
- Before a publish, validate, then play it in a local room with bots, and say what you saw. Never
  report a server-authoritative game as online before a draft of it passed.
- A passed draft's `draftPlayUrl` (in `genex__publish-status`) is where two people test the rooms:
  a guest joins there with no account, and the owner's Genex Pro pays for the rooms. `draftUrl` is
  the owner's draft page, behind their sign-in.

## Packages

- `genex__package {"package":"@genex-ai/multiplayer"}` adds both SDKs at Studio's pins (nobody is
  asked): `@genex-ai/multiplayer` with `@genex-ai/multiplayer/authority`, and `@genex-ai/embed-sdk`
  with `getAuthorityUrls`. Never run `npm i` for them yourself; the card's step 4 does not apply.
- `@genex-ai/authority-dev` ships with Studio: never install it in the game.
- A room module imports nothing at runtime from a package, and imports the game's own files only
  from folders inside the game (`src/`, `shared/`), never a file at the game's top level or in a
  hidden folder: the publish refuses those, and a link anywhere on the way.

## A game made from Studio's template

- It has no `package.json`: the `authority` block goes in `genex.json` at the game's root, beside
  any other setting: `{"authority": {"module": "server/room.js", "tickHz": 30, "maxPlayers": 8}}`.
  Keep `genex.json` valid JSON and add no package.json beside it: Genex reads a package.json first,
  so a stray one, or a `genex.json` that does not parse, would drop the block. The publish and
  `genex__room` refuse such a game by name (`export_room_manifest_shadowed`,
  `export_room_manifest_broken`) rather than ship it with no room.
- The same `genex__package` call maps `@genex-ai/multiplayer/authority` in its import map; a game
  that mapped multiplayer earlier gets it by making the call again. Never copy the SDK by hand.
- It has no TypeScript build: write the room module and every file it shares with the client in
  plain JavaScript (`server/room.js`, `src/world.js`), without the card's type annotations and
  `import type` lines, importing shared files by their `.js` path.
- Its public copy holds `index.html`, `src/` and `assets/`: keep server-only code in `server/`
  and shared code in `src/`.
- Studio connects the game: never call `initEmbed()`. The `room` for `connectAuthority` is the
  game's slug, from `src/genex.config.js` as the multiplayer card's preface describes
  (`genex__skill {"name":"genex-threejs-multiplayer"}`).

## An Unreal game

- The room module, its `authority` block in `genex.json`, `genex__room` and the publish are the
  same as above: only the client differs. Read `unreal__skill {"name":"unreal-multiplayer"}` for
  it: `unreal__multiplayer` adds Genex's Unreal plugin (shipped with Studio, never fetched by the
  game), and the client joins with its `Genex Authority Subsystem`. Ignore this card's
  `@genex-ai/multiplayer` and embed SDK steps for an Unreal game.

## Reading the references

The card links its references by relative path. Read one with `genex__skill` and the file exactly
as listed, for example
`genex__skill {"name":"genex-authoritative-multiplayer","file":"skills/genex-authoritative-multiplayer/references/module-api.md"}`.

## Commands

`npx genex preview` is `genex__publish {"operation":"draft"}` and `npx genex publish` is
`genex__publish {"operation":"gallery"}`; both carry the room module (above). Other commands map
onto Studio tools as the `genex` skill describes (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-authoritative-multiplayer/SKILL.md v1.40.0 sha256 956e9e2600339ce919fadee720d61e6aa018fb778068fd10acc735be7472a002 -->
---
name: genex-authoritative-multiplayer
description: Server-authoritative multiplayer for Genex games — the game's own room module runs on Genex's servers, players only send input, and the server decides every move and hit (lag-compensated). Use for competitive play where cheating matters: ranked PvP, arenas, shooters (first-person, hitscan or dodgeable projectiles), car football, "so nobody can cheat". Casual co-op and hangouts use genex-threejs-multiplayer instead. Load before writing the room module or any networking code.
---

# Genex Server-Authoritative Multiplayer

In a server-authoritative game the **server runs the game's rules**. The game ships a **room
module** — one script, `server/room.ts` or `server/room.js` — that Genex runs in a sandbox at a
fixed tick. Players send typed input (`moveX`, `moveY`, `yaw`, `buttons`, …); the server moves
every body, judges every shot against where the shooter saw its target, and writes the state every
client renders. A modified client can lie only about its own stick and buttons.

The client half is `connectAuthority` from `@genex-ai/multiplayer/authority`: it predicts the
player's own body with the same movement preset the server runs (so moving feels instant), draws
everything else 100 ms in the past, and reconciles when the server's truth arrives.

## Casual or server-authoritative

| | Casual — `$genex-threejs-multiplayer` | Server-authoritative — this skill |
|---|---|---|
| Who runs the rules | Each player's browser; Genex's relay passes messages | Genex's servers run the game's room module |
| Cheating | A modified client can say where it is and what it hit | The server decides every move and every hit |
| Fits | Co-op, hangouts, party, turn-based, casual races | Competitive shooters, arenas, ranked play — anything with a winner worth faking |
| On Genex's servers | Free | Needs Genex Pro for the game's owner |
| Building and testing | Free | Free, on this machine, with no account |

"Competitive", "ranked", "PvP", "esports", "so nobody can cheat" or "server-authoritative" mean
this skill; everything else is casual. When the person has not said which, ask in one line and say
what each costs. Never mix the two in one game: an authority game has no relay `Session`, no host
and no shared objects — the server owns all state.

## What you write

1. **The room module**, `server/room.ts` (or `.js`): `export default` a room with `contract: 1`,
   `config`, `init`, `onJoin`, `onLeave`, `onInput` and `step`. It is server code: keep it and
   everything only it uses in `server/`. Shared pure code (a movement step the client also runs)
   may live in `src/` and be imported by both. The full API and the sandbox's rules are in
   [references/module-api.md](references/module-api.md); four complete games to start from (an
   arena with instant shots, one with bolts players can dodge, a car arena with a ball, and the car
   arena on server physics with crates) are in
   [references/room-template.md](references/room-template.md).
2. **The manifest block**, in package.json:

   ```json
   { "genex": { "authority": { "module": "server/room.ts", "tickHz": 30, "maxPlayers": 8, "preset": "topdown" } } }
   ```

   A game without a package.json (one made from Studio's template) puts the same object in
   `genex.json` as `{ "authority": { … } }`. `module` is a plain relative path to a `.js` or `.ts`
   file inside the game folder. The rest is optional: `maxPlayers` (1 to 64) is the most a room
   seats (the module may ask for fewer), `tickHz` (20, 30, 60 or 120) is the rate for a module whose
   `config` names none (120 only for a module that asks for physics), and `preset` names its movement preset. Left out, each comes from the
   module's own `config`. A malformed block is not ignored — `genex preview` refuses it and says why.
3. **The client**: `connectAuthority` with the identity from `$genex-threejs-embed-auth`, input
   written to `session.input`, `session.frame(now)` once per render frame, and the scene drawn
   from `session.entities()`.
4. **The packages**: `npm i @genex-ai/multiplayer@latest @genex-ai/embed-sdk@latest` and
   `npm i -D @genex-ai/authority-dev`. The game needs a `@genex-ai/multiplayer` that exports
   `@genex-ai/multiplayer/authority` and an embed SDK at 0.35.0 or newer (it has
   `getAuthorityUrls`). If the import does not resolve after installing `@latest`, the release with
   server-authoritative rooms is not out yet: tell the person plainly and stop, rather than writing a
   server of your own. Projectiles need `@genex-ai/multiplayer` 0.17.4 or newer.

## Rules that decide whether it plays well

1. **The server decides; the client asks.** Health, score, pickups, kills, respawns and round
   state change only in the room module, and the client draws them from `session.entities()` and
   the module's events. Show a muzzle flash or play a sound at once if you like, but never draw a
   hit, a kill or a score the server has not sent.
2. **Never move your own body yourself.** Write the stick and aim into `session.input`; the session
   predicts your body with the room's preset and corrects it. A game whose movement is not the
   preset passes its own step as `predict: { step }` — the exact step the module runs
   ([references/presets.md](references/presets.md)).
3. **The module must be deterministic.** The same seed and inputs must give the same room: no
   clock, no timers, and randomness only from `ctx.random()` (`Math.random` is the same seeded
   generator inside the sandbox). `validate` and `replay` check this, and a publish refuses a
   module that fails.
4. **Bump `epoch` to teleport.** A respawn or a teleport that does not bump the entity's `epoch`
   slides across the map on every other screen.
5. **Keep per-tick work bounded.** Each tick has a CPU and memory budget; a runaway loop ends the
   room for everyone in it. Loops run over entities or players, never "until something happens".
6. **The server's plane is x/y, and +z is up.** `yaw` turns from +x toward +y. For `firstperson`
   and `vehicle`, draw at three.js `(x, z, -y)` with `rotation.y = yaw`: their input's "right" is
   the server's, and a mirrored drawing steers the car the wrong way. The topdown templates draw the
   server's `y` as three's `z`, which works there because they read input in the same drawn axes.

## Movement: pick a preset

| The game | `config.preset` | Notes |
|---|---|---|
| Seen from above (twin-stick, top-down shooter) | `topdown` | 30 Hz is enough |
| On foot through a level (a first-person or third-person shooter) | `firstperson` | Source-engine-style movement through a world of boxes and ramps; `tickHz: 60` |
| Cars (car football, a derby, a track of ramps) | `vehicle` | Rocket League's handling, kept level, through the same kind of world; `tickHz: 60` |
| Anything else | none: your own step | Shared by the module and the client, `predict: { step }` |

`firstperson` and `vehicle` move through a fixed collision world the module exports
(`defineRoom({ world })`) and the client hands its session (`connectAuthority({ …, world })`),
from one file both import: the session predicts only while the two hash the same. Their inputs,
parameters, units and CPU budget are in [references/presets.md](references/presets.md); read it
before writing either side. A ball the cars knock about is one projectile the module re-launches
(template 3, and "Running a ball" in presets.md).

## Feel settings: contacts, inputs, lifts, tick rate, regions, fast channel

Seats that touch (standing on heads, shoving, passing through), starved inputs, moving platforms, 120 Hz,
regions and the UDP fast channel are **settings in `config`**, picked by genre (`shooter`, `platformer`,
`party`, `physics-sandbox`, `vehicle-arena`), never code that names the game. Read
[references/settings.md](references/settings.md) for a worked config per genre before writing any of them.

## Physics: crates, balls, doors

When things must collide with each other (a stack that topples, a ball between cars and walls, a
door a player shoves), the module asks for server physics (`config.physics`) and spawns bodies with
`ctx.physics`; clients only draw them. It is new: check physics.md for when the servers run it. Read
[references/physics.md](references/physics.md) first; template 4 is the car arena with a physics ball
and crate stacks.

## Shots: hitscan or projectile

- **Instant** (a rifle, a laser): `ctx.rewind.hitscan` in `onInput`, lag-compensated with
  `config.lagComp`. Template 1.
- **Something players see travel and can dodge** (a bolt, a rocket, a grenade, an arrow, a
  dodgeball): a projectile. The module launches it once with `ctx.projectiles.launch` and judges it
  with `ctx.projectiles.sweep`; the shooter's client calls `session.predictProjectile` while staging
  the input that fires, and every client draws it from `session.entities()`. Template 2. Read
  [references/projectiles.md](references/projectiles.md) before writing either side.

Never make a travelling shot a plain entity the module moves in `step`: it costs an update every
tick and every client draws it 100 ms late. Every client in a room whose module launches
projectiles must support them; one that does not draws each projectile frozen where it was
launched.

## The client in one screen

```ts
import { connectAuthority } from "@genex-ai/multiplayer/authority";
import { getAuthorityUrls, getColyseusAuth, waitForPlayer } from "@genex-ai/embed-sdk";
import { GENEX } from "./genex.config";

await waitForPlayer();
const session = await connectAuthority({
  urls: getAuthorityUrls(),
  room: GENEX.slug,
  auth: () => getColyseusAuth(),
});

function loop(now: number) {
  session.input.moveX = stick.x; // [-1, 1] on the server's x axis
  session.input.moveY = stick.y; // [-1, 1] on the server's y axis
  session.input.yaw = aimAngle; // radians, 0 along +x
  session.input.buttons = firing ? FIRE : 0;
  session.frame(now); // sends the due inputs, predicts you, interpolates everyone else
  for (const [id, e] of session.entities()) drawBody(id, e.x, e.y, e.yaw, e.epoch);
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
session.on("shot", (data) => showTracer(data)); // an event the room module emitted
session.on("disconnect", (code) => showLeft(code));
```

A refused join rejects with a `code`: 402 (the owner's plan does not include Genex servers — final),
424 (no room module is published for this build yet), 426 (the SDK is too old), 429 (the owner's
server time or room limit is used up — try later) or 503 (no server free — the session already retried). Say each
in the player's words; never loop on 402 or 424. The whole client, with three.js, is in
[references/room-template.md](references/room-template.md).

## Shipping it

`npx genex preview` and `npx genex publish` ship the room module with the build, and refuse to
ship one that is not ready:

- **Before anything is built**, the module is bundled and validated with the game's own
  `@genex-ai/authority-dev` (the same check as `npx genex-authority-dev validate`). Any failure stops
  the deploy and prints its typed reason; the full report is kept at `.genex/authority/report.json`.
- **Before any game file uploads**, the module and its report go to a private store that the game's
  address never serves, and `server/` is left out of the public build.
- **On Genex's servers the owner needs Genex Pro.** A free account is refused with
  `authority_requires_pro` and nothing is uploaded; it can still build and test everything locally.
  Say so before the person publishes.
- A preview link plays in rooms apart from the live game, as casual multiplayer's does, and
  `npx genex promote` / `npx genex rollback` move the module together with the build — a rollback can
  restore the previous module alone when only `server/` changed.
