# Genex multiplayer in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's multiplayer API card,
with the passages of design advice Studio does not ship taken out. Where it disagrees with this
preface, this preface wins. How to shape a multiplayer game (menus, lobbies, teams, testing
routines) is the game's own call; the optional `genex-recommendations` plugin holds Genex's advice
on it when it is on.

## A Godot or Unity game has its own

This card is for web games written with npm and three.js. A Godot game gets Genex multiplayer from
`godot__multiplayer`, then `godot__skill {"name":"godot-multiplayer"}`; a Unity game from
`unity__multiplayer`, then `unity__skill {"name":"unity-multiplayer"}`. Genex's relays already
serve web, Godot and Unity players.

## Facts the card's removed passages carried

- `connect()` joins the one shared room of the game's slug at once; `matchmake()` puts the player
  in the queue and the server seats them in capped rooms by the preset in `genex.matchmaking`.
- A queued or seated player counts toward `minPlayers` until `mm.cancel()` (or `room.leave()` for
  `connect()`); `matchmake()` and `connect()` are the only calls that reach the relay.
- While `mm.matchmaking.status` is `'searching'` the player is in no room: `players`,
  `connectedPlayers` and `opponents` are empty, `queue.size` counts this player, and with
  `minPlayers === maxPlayers` the room skips `'waiting'`.
- For `open`, `status` goes `searching` → `waiting` → `playing` once and never back; `matchStart`
  and `matchEnded` never fire, and `teams`, `myTeam`, `scores` and `winnerId` stay empty.
  `connectedPlayers` / `session.activePlayers` leave out seats in their reconnect grace.
- The relay runs no game simulation and no anti-cheat: it enforces identity, ownership, seating
  and rate and size caps; a client reports its own state.

## Multiplayer runs on the Genex draft link

- Studio's preview is single-player. It opens a game that uses `@genex-ai/embed-sdk` in local
  test mode (`?genex_local_test=1`): the relay gets no credential there, so `connect()` and
  `matchmake()` fail by design. Rendering and controls still run in the preview.
- The draft link is multiplayer. A draft plays in rooms of its own, apart from the live game, so
  testers on the draft link meet each other and never real players. Anyone with the link can join,
  as a guest or signed in, before the game is published to the gallery. Two tabs on one account
  are one player: the newer tab takes the seat (close code 4409).
- `genex__package {"package":"@genex-ai/multiplayer"}` adds both SDKs in one call (it includes
  embed-sdk; nobody is asked). `genex__publish {"operation":"draft"}` puts a draft online and
  `genex__publish-status` gives its link, `draftPlayUrl`. Open that link in a normal and a private
  window to be two players; `draftUrl` is the owner's draft page, behind their sign-in.
- Nobody can save or buy on the draft link, the owner included: saves and purchases work once the
  game is published.
- Studio installs the version it pins, which satisfies the card's `^0.17.0`. Never run
  `npm i` for these packages yourself.
- A game made from Studio's template has no `package.json`: it loads three.js through an import
  map, and the same `genex__package` call maps Studio's copies of both SDKs into that map and loads
  Studio's connect module after it, with nothing downloaded. Studio connects the game: never call
  `initEmbed()`, skip the card's Bootstrap step, `genex.config.ts` and "Config without `genex init`"
  below, and never write a slug. Import the rest exactly as the card shows (`waitForPlayer`,
  `getColyseusAuth` and `getColyseusUrls` from `"@genex-ai/embed-sdk"`), in plain JavaScript: the
  template has no TypeScript build, so leave out the card's type annotations. Its settings go in
  `genex.json` at the game's root (`{"matchmaking": {...}}`) wherever the card says package.json's
  `genex` field. Never copy the SDK into the game by hand.
- A game with its own build but no `package.json` needs one before `genex__package`.
- When approval is declined or times out, or the hosted test route is unavailable, the answer
  names the blocker; a declined request is not repeated without the user asking again.

## Config without `genex init`

A remixed game already has a `src/genex.config.*` (and maybe a `.env`) naming the game it was
copied from. A config naming another game signs every player into that other game, so Genex
refuses to deploy it. Publish a draft; when it is refused for naming another game, read this game's
slug from `genex__publish-status`, set it in the config, and publish the draft again.

Studio never runs `genex init`, so a new game starts without `src/genex.config.ts` or `.env`. After
the first draft, `genex__publish-status` reports the game's `slug`. Write the config yourself,
then publish a new draft (a template game: `src/genex.config.js`, the same object without
`as const`, imported as `./genex.config.js`):

```ts
// src/genex.config.ts
export const GENEX = {
  slug: "<the slug genex__publish-status reported>",
  apiUrl: "https://api.genex.games",
  dashboardOrigins: ["https://genex.games"],
} as const;
```

## Reading the reference

The card links its reference by relative path. Read it with `genex__skill` and the file exactly as
listed: `skills/genex-threejs-multiplayer/references/realtime-patterns.md`, for example
`genex__skill {"name":"genex-threejs-multiplayer","file":"skills/genex-threejs-multiplayer/references/realtime-patterns.md"}`.

## Commands

`npx genex controller …` commands are not available in Studio: chat, voice and the character are
built from the SDK calls the card shows. Commands map onto Studio tools as the `genex` skill
describes (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-threejs-multiplayer/SKILL.md v1.40.0 sha256 3fb4e5e35afccc492e28c7e16820e46ccb8781ac465b40b7337d6be594473b98 -->
---
name: genex-threejs-multiplayer
description: Realtime multiplayer for Genex Three.js games with `@genex-ai/multiplayer` — a relay whose SDK auto-smooths remote players AND shared objects (you do NOT write interpolation). Use whenever 2+ players share a world: movement sync, a shared ball/NPC via objects + ownership, host-authoritative scores/waves, shots/emotes, presence.
---

# Genex Three.js Multiplayer

`@genex-ai/multiplayer` is a **relay with a smart client**: whatever you write to `me`,
`shared`, or an `object` is synced to everyone; everything else stays local. The **server**
runs no physics and no game logic — but it *does* enforce two generic invariants so the naive
path is the correct one: **exactly one smoother** (the SDK interpolates remote players and
objects for you) and **exactly one owner/host** (server-arbitrated). You read a remote player
or a shared object and it is already smooth; you never fight over who simulates the ball.

**Competitive play where cheating matters** (ranked PvP, an arena or shooter with a winner worth
faking, "so nobody can cheat") is a different kind of game: the server runs the rules. Use
`$genex-authoritative-multiplayer` for it instead of this skill, and never mix the two in one game.


## Two rules that decide whether it feels good

1. **Do NOT write your own interpolation/smoothing.** The SDK already smooths remote players
   *and* objects. Read `players.get(id).state` / `objects.get(id).state` and draw them directly.
   Buffering `state` and lerping it yourself stacks a second smoother and adds ~100 ms of lag —
   the #1 cause of a "laggy/stuttery" game here. Drawing `state` **is** the smooth path.
2. **Render YOURSELF (and objects you own) from your own local object, live.** Your input
   mutates a local object; you draw yourself from it every frame (zero latency). Never draw
   yourself from `players.get(room.id).state` — that's the network echo, round-trip-delayed.


## Install

```bash
npm i @genex-ai/multiplayer@^0.17.0
```

> Pin `@^0.17.0` (not a bare `npm i`, and not an older range): 0.17 speaks the relay's current
> wire protocol, and the relay **refuses every older SDK** — a game built on 0.16 or earlier
> cannot join a room at all (its joins fail with `unsupported protocol`). 0.17 also added a
> relay-stamped per-game player id (`p.uid`), relay-assigned teams for the `open` preset
> (`p.team`) and the `room:open` event. Earlier floors still hold: automatic TURN — the thing that
> lets players behind symmetric NAT or carrier CGNAT be heard at all — landed in 0.16, mesh voice
> in 0.15, room text chat in 0.14, host-only `setRoomOpen()` in 0.13. Because this package is
> still `0.x`, a caret range is minor-locked, so `^0.16.0` would resolve to 0.16.x and never join.

This skill targets `@genex-ai/multiplayer` **≥ 0.17.0** (relay protocol 3, `p.uid`/`p.team` and
`room:open` since 0.17; `objects`/`host` since 0.4; verified per-player `avatarUrl` since 0.12;
room text chat via `room.chat` since 0.14; mesh voice via `room.voice` since 0.15;
automatic TURN (voice connects behind symmetric NAT with no configuration) since 0.16;
`matchmake()` since 0.5; private lobbies since 0.7; auto-reconnect + `inputs`/`onHostTick`
since 0.8; soft ownership handoff since 0.8.4; confirmed controls, snap epochs, and host-tick
lifecycle guarantees since 0.9; regional relay selection via `getColyseusUrls()` since 0.10; host-only `setRoomOpen()` since 0.13;
exact-relay `url` overrides for cross-region invites since 0.11).

## Trust model

Each client is authoritative over itself, match outcomes are self-reported, and there is no server-side
simulation or anti-cheat. The server DOES enforce identity (verified tokens), object
ownership, match seating/adjudication, and rate/size caps — but a modified client can still
lie about its own position or score.

## Matchmaking (competitive presets — server-owned)

`matchmake()` seats players in **separate capped rooms** (a 1v1
duel, an FFA arena, N-v-N teams, an invite lobby) rather than the one shared `connect()` room. It
returns a handle whose **`session` is `null` while searching**; `mm.matchmaking` reports the search (its `status`, `queue.position`, `players`/`opponents`, `teams`, `scores`,
`winCondition`), and switch to the game once `session` goes live:

```ts
import { matchmake, type Session } from "@genex-ai/multiplayer";
import {
  waitForPlayer, getColyseusAuth, getColyseusUrls,
} from "@genex-ai/embed-sdk";
import { GENEX } from "./genex.config";

const { user } = await waitForPlayer();
const mm = await matchmake<MyState>({
  urls: getColyseusUrls(),
  room: GENEX.slug,
  name: user.name,
  auth: () => getColyseusAuth(), // fresh for every queue join and re-seat
});

let wired: Session<MyState> | null = null;
function syncSession() {
  const live = mm.session;
  if (live === wired) return;
  wired = live;
  if (live) wireRoom(live); // attach leave/reconnect/disconnect + game listeners
}

mm.on("queue", (payload) => {
  const q = payload as { position?: number; size?: number } | undefined;
  updateQueue(q?.position ?? 0, q?.size ?? 0);
});
mm.on("matched", () => syncSession());
mm.on("matchStart", () => syncSession()); // duel/arena/teams only
mm.on("matchEnded", (result) => showResult(result)); // duel/arena/teams only
mm.on("error", (e) => showQueueError(e)); // after SDK retries; fix, then mm.retry()
// 4409 = opened in another tab/device, 4401 = signed out: the handle stops, never requeues.
mm.on("disconnect", () => onQueueStopped()); // mm.retry() only on a click

// Every frame AND a low-rate timer: the handle swaps in a new Session after
// seating, terminal drop/requeue, and the next match.
syncSession();

// Report ONLY your own outcome — the server adjudicates. Which call fits depends on the win condition:
mm.eliminated();   // I'm out              (lastStanding)
mm.score(1);       // I scored             (firstToScore / highScoreInTime)
mm.finish();       // I finished the race  (firstToFinish)
```

For `open`, `matchStart` and `matchEnded` never fire: poll
`mm.matchmaking.status`, `mm.matchmaking.players`, and `mm.session` instead.
The event listeners above are for the batteries-included presets and do not
replace `syncSession()`.

Everything is **server-owned** — set once in `package.json` under `genex.matchmaking`, reported at
`genex preview` AND `genex publish` (removing it from package.json clears the stored config on the
next preview/publish); the client declares nothing. You never run matchmaking logic: the server
owns the queue, roles, winner-stays, forfeit, timeout, and the win condition.

If `genex.matchmaking` is absent, unavailable, or names an unknown preset, the
relay falls back to `duel`: rooms of exactly two with the duel round loop.
That is silently wrong for most 3–64 player `open` games. A `matchmake()` game
must declare and preview/publish the intended block; a `connect()` shared-world
game does not use this block.


```jsonc
"genex": {
  "matchmaking": {
    "preset": "arena",                 // open | duel | arena | teams | private
    "winCondition": "firstToScore",    // lastStanding | firstToScore | highScoreInTime | firstToFinish
    "config": { "scoreTarget": 20, "maxPlayers": 8 }   // numeric knobs, optional
  }
}
```

Presets: **open** (a room of N players — the server owns only seating/capacity/refill, you write
everything else), **duel** (1v1 winner-stays), **arena** (N-player FFA, join-anytime), **teams**
(N-v-N with a server-owned match loop + eviction), **private** (invite-code lobby). Win conditions (batteries-included presets only):
**lastStanding** (last one alive), **firstToScore** (first to the score target), **highScoreInTime**
(top score at the time cap), **firstToFinish** (first to finish). A round that hits the time cap
undecided is a draw. (`open` has no win condition — it never ends a round for you.)

### `open` (bring your own rules)

**`open`** is a room of up to `maxPlayers` that the queue seats and (optionally)
refills, and NOTHING else — no rounds, no scores, no win condition, no winner-stays eviction. You
build teams/rounds/scoring/win-logic in game code on the primitives you already have (host election,
`shared`, per-player state, the `players` list). Config knobs (all numbers):

```jsonc
"genex": { "matchmaking": { "preset": "open", "config": {
  "maxPlayers": 10,   // seat cap (clamped 2..64)
  "minPlayers": 2,    // quorum to flip waiting→playing (default 1)
  "fill": 1           // 1 = keep full: grow to max + refill freed seats (default); 0 = lock for good once simultaneously full (no substitutes)
} } } }
```

With `open`, `mm.matchmaking.status` only goes `searching`→`waiting`→`playing` (never `countdown`/
`ended`), `players` is the live roster, and `teams`/`myTeam`/`scores`/`winnerId` stay EMPTY forever
— only the server presets fill them. Watch `players` and `status`, not `matchStart`/`matchEnded`
(they never fire). `mm.matchmaking.teams` is empty on `open`: a team game keeps its own team map
(in `shared`, say).
Nobody is ever evicted. Build the rest:

| Want… | Do it in game code on top of `open` |
| --- | --- |
| Room formation & refill | Nothing — the server owns it via `minPlayers`/`maxPlayers`/`fill`. |
| Duel (1v1) | `maxPlayers: 2, minPlayers: 2`, then start when `mm.matchmaking.players.length === 2`. |
| Rounds / countdown | Host writes `{ phase, deadline }` into `shared`; clients render the countdown from the timestamp (no server clock — approximate fairness is fine at this trust tier). |
| Scores | A host-owned entry in `shared` (or per-player state); you define what a point means. |
| Win condition | Your code checks its own condition (you already compute the signals) and the host writes the result to `shared`. |
| Winner-stays / rotation | The losing **client** leaves voluntarily — `mm.cancel()` then `matchmake()` again; the freed seat refills (`fill: 1`). There is NO forced kick (a server-only power, deliberately not exposed) — a modified client can squat its seat, so if you need *enforced* rotation use `duel`/`arena`/`teams` instead. |
| Forfeit on disconnect | React to the `players` list shrinking (the SDK surfaces leaves after the reconnect grace). |
| Spectators | A game-level role: keep a "dead"/observing player seated and just render them as a watcher. There is no server spectator concept — everyone in a room is a player. |


**Private lobbies** (for `preset: 'private'`) don't use `matchmake()` — a host makes an invite code
and friends join it; the lobby is persistent (rounds replay, nobody is evicted):

```ts
import { createPrivate, joinPrivate } from "@genex-ai/multiplayer";
import { share, getEntry } from "@genex-ai/embed-sdk";              // 0.32.0+
const opts = { urls, room: slug, auth: () => getColyseusAuth() };

// host
const lobby = await createPrivate<MyState>(opts);                    // live NOW
showCode(lobby.code);                 // always show the code too: the way in when a link will not do
inviteBtn.onclick = async () => {     // share() starts inside the click, before any await
  const { status, url } = await share({ text: "Join my lobby", params: { lobby: lobby.code } });
  if (status === "copied") toast("Invite link copied");
  if (status === "unavailable") showLink(url);       // no share sheet, no clipboard: show the link
};

// friend: ONE way in, for the code from a link and for a code typed by hand
async function enter(code: string) {
  if (!/^[\w-]{1,32}$/.test(code)) return null;      // a link is text anyone can write: take a code, nothing else
  try { return await joinPrivate<MyState>(code, opts); }
  catch { showNotice("That lobby is no longer open"); return null; }
}
// at boot, after waitForPlayer(): did they arrive on an invite link?
const invited = getEntry().params.get("lobby");
const joined = invited ? await enter(invited) : null;  // null → the menu, with its "Enter code" field
// same handle API as matchmake(): lobby.session, lobby.matchmaking, eliminated()/score()/finish(), cancel()
```

`share()` builds the link itself — the game's page on Genex plus `?lobby=<code>`, or the
address the game is on where that is a preview address or a creator's own domain — and
`getEntry()` hands the parameter back to whoever opens it. **Never build the invite from
`location.href`**: on the game's page that is the frame's bare address, not the page a friend
should land on. `lobby` is this example's name; any name works except the ones Genex keeps
(`$genex-threejs-embed-auth`, `references/shells.md`). `joinPrivate` REJECTS when the code leads
to no lobby this player can reach — it closed, or its host is on another region's relay — so
catch it and show the menu, and keep the typed code as the second way in.

## Connect

Pick your own per-player state shape (any JSON). `room` is the **project slug**
— same id = same room, different ids are fully isolated.


**Joining requires the SDK's player identity — the relay rejects tokenless
joins, but accepts guests** (accountless players named like `Guest-1234`).
Load the `genex-threejs-embed-auth` skill first (it sets up `initEmbed(...)`),
then gate `connect()` on `waitForPlayer()` — NOT `waitForAuth()`, which stays
pending for guests and would keep them out of multiplayer forever:

```ts
import { connect, type Session } from "@genex-ai/multiplayer";
import { waitForPlayer, getColyseusAuth, getColyseusUrls } from "@genex-ai/embed-sdk";

type State = { x: number; z: number; q: number[] };  // YOUR per-player state (rotation as quaternion)

const { user } = await waitForPlayer();  // player gate (guest OR signed-in) — rejects only if blocked
let room = await connect<State>({
  urls: getColyseusUrls(),    // regional relays for this session (server-owned); SDK joins the fastest
  room: GENEX.slug,           // the project slug — everyone with this id shares a room
  name: user.name,            // display name — the server prefers the verified identity's name
  auth: () => getColyseusAuth(), // REQUIRED — fresh on every explicit connect attempt; NEVER log it.
});
```

**Capacity:** 64 players is the relay's **mechanical seat cap**, not a proven high-motion physics
envelope. Object-heavy rooms amplify fanout; measure the exact game at 8/16/32/64 before promising a
supported count. Above the cap the relay opens another room for the same game.

## Disconnects: transient reconnect is built in; terminal rejoin is yours

The SDK auto-reconnects after a network blip or brief signal loss: the relay holds your seat for a
grace window (~30 s). A short blip keeps the same session id, ownership, and host. If a disconnected
host exceeds the shorter simulation lease, an active peer takes authority once; the old host can
return to its seat but is demoted. Long reconnects rebase remote smoothing rather than replaying a
whole-map catch-up streak. The session reports each step:

```ts
let intentionalLeave = false;

function wireRoom(live: Session<State>) {
  live.on("reconnecting", ({ attempt }) => onConnection("reconnecting", attempt)); // inside the grace window
  live.on("reconnected", () => onConnection("live")); // same session id, ownership and host
  live.on("disconnect", (code) => {
    // 4409 means this player deliberately opened the game elsewhere. Rejoining
    // here would evict the new tab, which would rejoin and evict this one forever.
    if (code === 4409) return flushSaves();
    // Any other code: the seat is gone, and only a new connect() rejoins.
    if (!intentionalLeave) onConnection("lost");
  });
  live.on("server:restart", () => flushSaves());
}
wireRoom(room);

function leaveShared() {
  intentionalLeave = true;
  room.leave();
}
```

During `reconnecting`, remote players freeze briefly and then glide on. A deliberate `room.leave()` never auto-reconnects.

**One seat per player (enforced server-side):** joining the same game again — a second tab,
another device, or a page reload — instantly evicts the previous session (it gets
`disconnect`, code 4409). You never need to handle "the same player twice" and a reload
never leaves a ghost avatar behind. If the evicted tab was the host and holds unsaved world
state, flush it in the `disconnect` handler (code 4409, above): that tab is still alive, so an
async `saveWorldState` completes — otherwise a debounced save in flight is lost.

## Which channel for which data

**This table is the most important thing in this skill.** Every piece of networked state is one
of five kinds — put each on its channel and the game just works:

| What you're syncing | Channel | Who writes it |
| --- | --- | --- |
| Your own avatar (position, rotation, anim) | `me.set` → others read `players` | you (each player their own) |
| A moving thing nobody owns (**ball**, puck, NPC) | `objects` (claim + set) | the one current **owner** |
| Slow agreed facts (score, round, wave, seed) | `shared` | the **host** (`isHost`) |
| One-off actions (shot, emote, hit) | `send` + `on` | whoever did it |
| Discrete per-player values (hp, ammo, flags) | in `me.set`, read via `stateRaw` | you |
| Which avatar MODEL a player is (VRM look) | already on `players` as `p.avatarUrl` — sync nothing | the **relay** (verified identity) |
| **Text chat** | `room.chat` — its own channel, NOT `send` | the **relay** (stamps the sender) |
| **Voice chat** | `room.voice` — peer-to-peer audio, max 6 | nobody (the relay carries no audio) |

Getting the channel right is the whole game. A ball on `shared` stutters (not smoothed) and
fights (many writers). A ball on `objects` glides and has one owner. That's the difference.

## API surface (exact — do not invent methods)

- `room.id` — your own session id.
- `room.me.set(state)` — publish your state, **replaces it wholesale**. Fixed **10–20 Hz tick**,
  never per frame.
- `room.me.snap(state)` — respawn/teleport/mode edge. Publishes a discontinuity epoch so remotes
  hard-reseed instead of interpolating from the old pose. Never use for ordinary movement.
- `room.players` — fresh `Map` each read, **includes you** (skip `id === room.id`). Each value is
  `{ id, name, avatarUrl, connected, state, stateRaw }`: `state` is auto-smoothed (remotes) / live (you);
  `stateRaw` is the raw latest (hit-tests, discrete values). A reconnect-grace seat remains in this
  map with `connected: false`. `avatarUrl` is that player's verified VRM pick (server-set, `''`
  when unknown); never publish avatar URLs through `me.set`.
- **Build each remote's body exactly ONCE — reserve the id BEFORE the first `await`.** You read
  `room.players` every frame, but loading a body is async and slow (seconds). If the only guard is
  the map you fill *after* the await, every frame in that window passes it: you spawn one body per
  frame, each stranded where it spawned — a trail of frozen clones behind the moving player — plus
  dozens of wasted loads. Mark the id synchronously, and drop the body if that player left mid-load:

  ```ts
  const bodies = new Map<string, Body>();
  const loading = new Set<string>();                      // the seat reservation
  function ensureBody(p: Player) {
    if (bodies.has(p.id) || loading.has(p.id)) return;    // BOTH — checked before any await
    loading.add(p.id);
    void (async () => {
      try {
        const body = await loadVrmClone(p.avatarUrl || "./assets/avatar.vrm");
        if (!room.activePlayers.has(p.id)) return;        // left while loading — never add it
        scene.add(body.scene);
        bodies.set(p.id, body);
      } finally { loading.delete(p.id); }                 // always release, success or throw
    })();
  }
  // Each frame: ensureBody for every remote, then drop bodies whose id is gone.
  for (const [id, body] of bodies) {
    if (!room.activePlayers.has(id)) { scene.remove(body.scene); bodies.delete(id); }
  }
  ```

  The same rule covers anything else you lazily load per player or per object (nameplates, weapon
  models, audio): a check that straddles an `await` is not a guard.
- `room.setRoomOpen(open)` — **host only.** Stop (or resume) the matchmaker putting NEW players
  into THIS room. A lobby game needs this: once your match starts, arrivals would otherwise be
  dropped into a fight already in progress. Close the room at match start and the next arrival
  forms the NEXT room instead; reopen when you return to the lobby. Everyone already inside keeps
  playing, and a reconnecting player still gets back in (reconnection uses a reserved seat, not
  matchmaking). A non-host call is ignored, so check `isHost` first — and because the host can
  change, re-assert it on `on('host')` rather than only once at match start:

  ```ts
  function startMatch() {
    if (room.isHost) room.setRoomOpen(false);   // late arrivals form the next lobby
  }
  function backToLobby() {
    if (room.isHost) room.setRoomOpen(true);
  }
  room.on("room:open", ({ open }) => showLobbyClosedBadge(!open)); // every client is told
  ```
- `room.activePlayers` — the connected-only subset of `room.players`; use its size for live quorum.
- `room.objects` — shared objects nobody owns until claimed (a ball, an NPC):
  - `claim(id)` — **legacy** optimistic request. It flips local ownership immediately and is corrected
    if the relay rejects it. Keep only for reversible old-game behavior.
  - `await claimConfirmed(id, options?)` — authoritative accepted/rejected result for a kick, seat,
    reset, or other irreversible action. Ordinary claims, including host-player contact, honor the
    relay minimum hold. `reason: "held"` includes `retryAfterMs`; retry only while contact/intent is
    still valid. `{ authority: "host" }` is reserved for current-host seed/reset lifecycle work.
    A real hold bypass returns `host-authority`; a non-host request returns `not-host`. A current-owner
    reassert is accepted as `already-owner` without extending the hold.
  - `set(id, state)` — publish it (only lands while you own it; full flat object each call).
  - `get(id)` → `{ id, owner, isMine, epoch, state, stateRaw }` or `undefined`. `state` is auto-smoothed
    (or live if `isMine`); `stateRaw` is the raw latest.
  - `release(id)` / `remove(id)` — legacy fire-and-forget operations.
  - `releaseConfirmed(id)` / `removeConfirmed(id)` — acknowledged, idempotent operations; use when
    local mode/state depends on convergence. Remove stays owner-only.
  - `snap(id, state)` — owner-only reset/teleport with an object discontinuity epoch. Ordinary motion
    stays on `set`.
  - `ids()` — all object ids seen.
- `room.isHost` / `room.host` — you are (or who is) the elected authority. Use to pick the single
  writer of `shared` scores/rounds and the single simulator of host-owned objects. Settles within
  the first patch after connect — read in your loop / react to `on('host')`, not once. `isHost` is
  false while reconnecting (until the fresh snapshot lands), so gating a write on it is safe.
  `room.host === undefined` before that patch means **authority is not ready**:
  do not start host-owned simulation and do not synthesize an "acting host" from
  a locally sorted roster. Clients can briefly observe different rosters, so
  that fallback can create multiple writers. Gate host-dependent initialization
  until `host !== undefined`; if it remains unset while connected, expose it in
  diagnostics and re-seat/reconnect instead of inventing authority.
- `room.shared.get/set/keys` — key/value store (any JSON) for **slow agreed facts only**.
- `room.on(event, cb)` → unsubscribe fn. Events: `'join'`/`'change'` `(id, state)` (also fire for
  you), `'leave'` `(id)`, `'shared'` `(key, value)`, `'object'` `(id)` (ownership handoff),
  `'host'` `(id)`, and any custom `send` name.
- `room.send(type, payload)` — fire-and-forget to all **other** clients. **It never echoes to
  you**, so apply your own action's local effect directly (draw your own tracer at fire time),
  not inside `on(...)`. Relay-internal names (`state`, `shared`, `claim`, `obj`, `release`,
  `destroy`, `match:*`, `__*`) are refused — pick your own event names. `room.leave()`.
- `room.chat` — room text chat, **its own channel, not `send`**: `chat.send(text)`,
  `chat.on(m => …)`, `chat.history`, `chat.mute(id)` / `chat.unmute(id)` / `chat.muted`.
  The relay stamps `m.from`/`m.name` from the verified session (nobody can post under
  another player's name), sanitizes `m.text`, caps it at 500 chars, and replays the last
  ~50 lines so a late joiner sees the conversation. **Your own lines echo back to you** —
  render only what arrives in `on`, or every message appears twice. `chat.isTyping`
  says whether this player is typing a line. Render `m.text` with `textContent`,
  never `innerHTML`. See [references/realtime-patterns.md](references/realtime-patterns.md).
- `room.voice` — mesh voice chat: `voice.join(opts)` / `leave()` / `setMicEnabled(on)` /
  `mute(id)` / `participants` / `active` / `speaking`, plus `room.on('voice', …)` and
  `room.on('voice:rejected', …)`. **Party-sized: the relay caps it at 6** (audio is a full
  mesh — everyone uploads to everyone, and reliability, not bandwidth, breaks first). The
  room still holds 64 players; the 7th `join()` is refused, so handle `voice:rejected`
  instead of retrying. `join()` MUST run inside a click/tap — browsers gate both the mic
  prompt and audio playback on a user gesture — and it REJECTS when the microphone is
  refused, which is an ordinary outcome to show, not an error to swallow. **Two refusals are
  not the player's.** On its Genex page a game gets the microphone only when its BUILD
  declared it: `npx genex preview` / `npx genex publish` declare it when the game's own
  source calls `.voice.join()` with nothing or with options written at the call, and print
  what the build is given — read that line. `voice.join(opts)` with the options in a
  variable is not seen: declare the microphone in `package.json` then. When the
  page withheld it, `join()` rejects with an error whose `name` is `VoiceNotDelegatedError`
  (SDK 0.16.2+, Chromium browsers; elsewhere it arrives as the browser's own error): show
  "Voice chat is not available here", never "allow your microphone" — the player was never
  asked. And the Genex app refuses the microphone for every game: hide the voice button when
  `getShell()` from `@genex-ai/embed-sdk` is `"app"`. The declaration rule, and the
  `package.json` line for a call the CLI cannot see, are in `$genex-threejs-embed-auth`
  (`references/shells.md`).
  `join({ spatial: true })` gives positional audio per speaker. **TURN is automatic
  — do not pass `iceServers`**: `join()` fetches short-lived relay credentials from the
  platform before opening any peer connection, which is what lets the ~15% of players behind
  symmetric NAT or carrier CGNAT be heard at all (in a mesh they fail every leg, so they
  connect to nobody while everyone else works — a miserable bug to diagnose from a report).
  Passing `iceServers` overrides this and is only for running your own TURN.
- `room.inputs.send(payload)` / `room.inputs.on((fromId, payload) => …)` — the host-routed
  input channel for host-authoritative physics: anyone sends, ONLY the current host receives.
- `room.onHostTick(hz, cb)` — fixed simulation only while connected and host. It pauses during
  reconnect, resumes only if still host, and stops on demotion, deliberate leave, or terminal
  disconnect. Returns a disposer for removing the subsystem earlier.

## Your message budget (every publish is one relay message)

Every publish costs one relay message. The relay uses a global ceiling plus reserved lanes: player
state 30/s sustained, object control 40/s, host input 60/s, and bulk object/shared/custom traffic
120/s (all with bursts). A bulk-object flood therefore cannot consume the avatar or control lane.
Drops still produce the SDK warning; confirmed controls additionally resolve `rate-limited` rather
than silently disappearing. The budget math that matters:

- Your own state (`me.set`) at 15 Hz + ONE driven/owned moving object at 15 Hz = 30/s. Fine.
- The pattern that blows the budget: **republishing IDLE objects every tick.** A host that
  owns several parked vehicles/props must NOT `objects.set` each of them at full tick rate —
  publish an object **when it changed**, plus a low-rate keepalive (~1–2 Hz) so late joiners
  converge. Unchanged pose ⇒ no message.
- **Per-projectile objects:** each live projectile at 30 Hz is 30/s of bulk budget, and every
  spawned id counts against the room's 128-object cap until `objects.removeConfirmed` removes it.
- If you see the drop warning, count each lane separately and also leave headroom under the global
  ceiling. Reserved capacity protects presence and control, but it is not permission to spam bulk.

## The loop (input → local → tick → render)

1. **Input mutates a local object only** (`me.x += …`). Never network on keypress.
2. **A fixed tick publishes it:** `setInterval(() => room.me.set(me), 66)` (~15 Hz). If you own an
   object, `objects.set` it in the same tick. **Round numbers before publishing** —
   `Math.round(v * 100) / 100` (2 decimals ≈ cm precision) — raw floats serialize as 17-digit
   JSON and are the #1 bandwidth waste; nobody can see a 0.001-unit difference.
3. **Render at your own framerate:** yourself from your *local* object; every other player from
   `players.get(id).state` directly (already smoothed); every object from `objects.get(id).state`.
4. **Create-or-reuse one mesh per id**; remove a player's mesh on `'leave'`.


## Rotation: sync a quaternion, not an angle

Send rotation as a 4-number quaternion `q: mesh.quaternion.toArray()`; on the remote do
`mesh.quaternion.fromArray(p.state.q)`. A scalar `yaw` is lerped linearly, so a heading crossing
±π spins the long way. This applies to `objects` state too — keep object fields **flat**
(top-level numbers + a 4-number quaternion smooth; nested objects snap).

## Smoothed vs raw — `state` vs `stateRaw`

`state` is smoothed and rendered slightly in the past (that's what makes motion glide). `stateRaw`
is the newest value with no smoothing. **Draw** from `state`; **test** against `stateRaw` — hit
detection, "am I close enough to kick", pickups, and any discrete number (hp, ammo, animation id,
a 0/1 flag) that must not arrive fractional. This holds for both players and objects.

The smoothed view is ~100–150 ms in the past: at projectile or ball speeds the real object has
already passed where the smoothed one still is.

**Packed animation-flag bitfields.** Smoothing lerps EVERY numeric
field — there is no integer exemption — and a lerped bitfield decodes to garbage: with
`moving=1, running=2, grounded=8`, walking is `f=9` and running is `f=11`, and the interpolation
passes through `10`, where `10 & moving === 0` — the sprinting opponent renders as *standing
still*. Worse, the exponential ease approaches an increasing target from below, so truncation
reads `target - 1` for the whole approach (~1.5 s median before RUN appears; at a vsync-locked
frame rate it can stick one ULP below the target *forever*).
Always drive remote animation from `stateRaw`:

```js
avatar.updateFromFlags(p.stateRaw.f ?? 0, dt);   // flags are DISCRETE — never p.state.f
```

**Reaction one-shots on remotes fire on EDGES, never per frame.** If you replay a remote's
death/hit pose from their published `out`/`hp` state, track the previous value and act only on
the transition — a per-frame `reset()`/`playDown()` restarts or cancels every in-flight reaction
clip (and re-writing ghost/material flags 60×/s is pure churn).

## Shared objects (the ball, the NPC) — use `objects`, never `shared`

A ball belongs to no player. Put it on `objects`: exactly one client owns it at a time (the SDK +
relay enforce it), the owner simulates it, and everyone else reads it auto-smoothed — on the same
interpolation as a player. Ownership survives the owner leaving (reassigned to the host).

```ts
const result = await room.objects.claimConfirmed("ball");
if (result.accepted) applyKickAndFeedback();
else if (result.reason === "held" && stillTouching) retryAfter(result.retryAfterMs);

if (room.objects.get("ball")?.isMine) {
  room.objects.set("ball", stepBallPhysics());       // only the owner's writes land
}
const ball = room.objects.get("ball");
if (ball) drawBall(ball.state);                       // smoothed for everyone, live for the owner
```

**Keep contact validity alive until acceptance; do not consume one rejected rising edge forever.**
Never claim every frame: maintain one pending request, then retry after the relay delay only while the
contact remains valid. Keep object state flat.

`objects.set()` / `objects.snap()` on an object you do not own are ignored; SDK ≥0.10.2 warns once
per object/operation instead of failing silently. Host *election* and object *ownership* are
separate systems: `onHostTick` firing does not mean the host owns anything, and
`claimConfirmed(id, { authority: "host" })` answers `accepted` once it does.

Right after a claim, an object's smoothed `state` can briefly be a degenerate transform (a zero or
NaN quaternion, or a position mid-interpolation from the origin) on every client, the host
included.

## Host authority (scores, rounds, enemies)

One client is the `host` (`room.isHost`). Being host gives no authority over objects: only an
object's owner writes it.
If another player owns/drives an object (their claim landed), the host renders it from the
stream like everyone else — a host branch that pins "its" objects to a local pose without
checking `owner`/`isMine` shows every other player's driving as a frozen object:

```ts
if (room.isHost) room.shared.set("round", nextRound);   // isHost: true on one client at a time
room.on("host", (id) => {});                             // host migrated (someone left)
```

**Key scores by a STABLE identity, never the session id.** A session id dies on every reload —
the points orphan into a duplicate row and the player's color changes. The relay stamps every
player with `uid` — their stable id **in this game**, the same across reloads, never their account
id — so key `scores`/colors/`isMe` by it. When an event only carries a session id, map it via
`room.players.get(sid)?.uid`. Never publish the account id (`user.id`) in player state yourself:
every peer reads it.

When the host leaves, the objects it owned are reassigned to the new host; their `stateRaw` holds
the last published values.

## Persistent worlds (optional — survives restarts)

The relay is in-memory: room state is gone when everyone leaves or the server restarts. For a world
that persists (a driven car stays where it was parked, built structures survive), save/load the
game's shared world slot via the embed SDK, from **one authority** (the host):

```ts
import { loadWorldState, saveWorldState } from "@genex-ai/embed-sdk";

// load on boot (safe to call immediately — waits for identity internally;
// guests resolve { data: null, guest: true } and receive the live world
// through the room instead)
const { data, version } = await loadWorldState();
initWorld(data ?? defaultWorld());
let worldVersion = version;

// save from ONE authority — the elected host — debounced, WITH ifVersion so a
// stale host handoff loses loudly instead of silently clobbering:
async function persistWorld(world: unknown) {
  if (!room.isHost) return;
  const res = await saveWorldState(world, { ifVersion: worldVersion });
  if (res.saved) worldVersion = res.version!;
  else if (res.conflict) {
    // someone else wrote since our read (host migration race) — resync
    const fresh = await loadWorldState();
    worldVersion = fresh.version;
    mergeWorld(fresh.data);
  }
  // res.guest: this host is a guest (guest-only room) — saving is off until a
  // signed-in player joins; the relay prefers signed-in hosts automatically.
}
```

The slot is one JSON blob per game (≤ 1 MB) shared by every player — world layout only,
NEVER per-player progression (that belongs in each player's own `savePlayerState()` slot —
see the embed-auth skill). Don't save every frame: debounce (~1/sec), and also flush on
`document.visibilitychange === "hidden"` so the last edits survive the host closing the tab.
Guests can't write it, but the relay elects a signed-in host whenever one is present, so
host-driven saving works as long as ANY account is in the room.

## Troubleshooting auth

- **`connect()` rejects with 401/403** — 401 "auth required"/"invalid token": you joined
  without `auth`, before `waitForPlayer()` resolved, or reused a stale token for a NEW terminal
  rejoin — read `getColyseusAuth()` fresh at every connect. 403 "wrong game": the `room` value
  doesn't match this game's own slug. 403 "guest capacity": the room is at its guest
  limit — signing in gets the player a seat; surface the message as-is.
- **`disconnect` fired and the player wants back in** — the old session is dead; run your
  connect flow again from the top with a FRESH `getColyseusAuth()` (a cached auth object is
  the usual cause of a rejoin failing 401).
