# Genex player identity in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's embed-auth card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface, this preface wins.

## Where each part can be tested

- Studio's preview opens a game that uses `@genex-ai/embed-sdk` in local test mode
  (`?genex_local_test=1`) for you. Rendering and controls run there.
  Sign-in, saves, leaderboards and multiplayer cannot: that is expected, not a bug to chase.
- The owner can try sign-in and multiplayer on the published Genex draft: build the game, add the
  package with `genex__package {"package":"@genex-ai/embed-sdk"}`, publish a draft with
  `genex__publish {"operation":"draft"}`, wait with `genex__publish-status`, then hand the draft
  link to the user.
- Server saves never persist on the draft: loads and saves resolve `{ staging: true }` there by
  design, as the card says. They persist only once the game is published to the gallery, which
  happens only when the user wants it public.
- Studio installs the version it pins. Never run `npm i` for this package yourself.
- A game made from Studio's template has no `package.json`: there
  `genex__package {"package":"@genex-ai/embed-sdk"}` maps Studio's copy in the import map, as
  three.js is, and loads Studio's connect module after it. Never copy the SDK into the game by
  hand. Read "In a game made from Studio's template" below.
- Studio connects every web game it publishes that brings no SDK of its own, so genex.games can
  sign its players in. A game needs the SDK only to use identity, saves or leaderboards itself.

## In a game made from Studio's template

Studio connects a template game to Genex itself: its connect module calls `initEmbed()` before the
game's own code runs, in local test mode in Studio's preview and with the game's project once it is
published. Skip the card's Bootstrap step and `genex.config.ts`: never call `initEmbed()` and never
write a slug. Import everything else from `"@genex-ai/embed-sdk"` as the card shows
(`waitForPlayer`, `loadPlayerState`, `savePlayerState`, `submitScore`, `getLeaderboard`). On a
hosted page `waitForPlayer()` takes seconds to resolve. Keep the import-map entry and the connect
module's `<script>` that `genex__package` added.

## Config without `genex init`

In a game with its own `package.json`, Studio never runs `genex init`, so the game starts without `src/genex.config.ts` or `.env`, and
"re-run `genex init`" is not available. After the first draft, `genex__publish-status` reports the
game's `slug`. Write the config yourself, then publish a new draft (a template game:
`src/genex.config.js`, the same object without `as const`, imported as `./genex.config.js`):

```ts
// src/genex.config.ts
export const GENEX = {
  slug: "<the slug genex__publish-status reported>",
  apiUrl: "https://api.genex.games",
  dashboardOrigins: ["https://genex.games"],
} as const;
```

## Commands

`genex preview` is `genex__publish {"operation":"draft"}`, and the update nudge the card mentions
does not apply: Studio pins its Genex packages. Other commands map onto Studio tools as the
`genex` skill describes (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-threejs-embed-auth/SKILL.md v1.40.0 sha256 ec5bee74f3da305399cdab46d856703ed06b0851e97e62948a6b4ccafd172a50 -->
---
name: genex-threejs-embed-auth
description: Wire up player identity AND durable game state for a Genex game via @genex-ai/embed-sdk. Every player gets an identity (signed-in account or guest); per-player saves, shared world state, and leaderboards are one-line SDK calls; multiplayer requires the SDK's token either way. Also holds the shells table: what a game may do on its Genex page, in the app and on its own link.
---

# Genex Three.js Embed Auth

`@genex-ai/embed-sdk` is how a Genex game learns **who is playing it** — and
how it **saves**. Published games are playable by
**guests** (no account — the SDK mints a temporary identity like `Guest-1234`
automatically), while **signing in** unlocks saving/loading progress (each
player gets their own save slot) and leaderboard entries; multiplayer works
for both, using the SDK's token. The SDK handles every context with one
`initEmbed(...)` call:

- **Embedded in the Genex dashboard (an iframe):** a silent handshake signs
  the viewer in within a couple of seconds — or drops a signed-out viewer
  straight into guest play. No login screen either way.
- **Standalone (someone opens the game's link directly):** the visit bounces
  once through Genex (at the CDN edge in production, so the game only loads
  AFTER identity is resolved; where the edge did not, the SDK makes the same
  bounce itself) — signed-in visitors arrive already authenticated on ANY
  game with zero clicks; everyone else arrives as a guest with a small
  dismissible "sign in to save progress" popover (rendered by the SDK — don't
  build your own). Nobody ever hits a login wall on a published game.
- **Inside the Genex mobile app:** the app hands the game its player — the
  signed-in account or a guest — with no bounce and no login screen.
- **Local test mode (your own self-testing):** `?genex_local_test=1` on the
  local dev server boots a credential-less local session — see "Self-testing
  a draft" below.

While identity is resolving (or blocked) the SDK shows its own full-screen
overlay over the game, so never build a separate "connecting" screen for auth.
Guest sessions have **no** overlay — the game just plays.

## The four shells — read before you call a browser or device API

Those four contexts are the **shells** a game runs in, and they differ in far
more than identity. What a game may open, save, share, read from its URL or
ask of the player's device is different in each one, and a call the shell
refuses usually fails with no error at all.
**Find the row in [references/shells.md](references/shells.md) before you
write `navigator.*`, `window.open`, a download link, a dialog, or anything
that reads the URL.** The digest:

- **Which shell:** `getShell()` → `"page"` (the frame on the game's Genex
  page, where most players are, and any other frame), `"app"`,
  `"standalone"` or `"local"`.
- **Share, copy, open a link, save a file, fullscreen, keep the screen on,
  vibrate:** `share()`, `copyText()`, `openExternal()`, `saveFile()`,
  `setFullscreen()`, `keepAwake()`, `haptic()`, from a click or tap handler,
  before any `await`. They resolve with a reason and never throw.
- **Your own URL parameters, and where the visitor came from:** `getEntry()`,
  never `location` or `document.referrer`.
- **Microphone, camera, location:** the build declares them at
  `npx genex preview` / `npx genex publish`; the app refuses all three.
- **Never:** `alert` / `confirm` / `prompt`, `window.open`, a link or form
  that leaves the game, a service worker, reading the clipboard.
- **Local test mode is a plain browser tab, not the frame.** A call that works
  there can still be dead on the game's Genex page.

## Bootstrap

```ts
// main.ts — the FIRST thing in the boot sequence, before any other game code
import { initEmbed } from "@genex-ai/embed-sdk";
import { GENEX } from "./genex.config";

initEmbed({
  slug: GENEX.slug,
  apiUrl: GENEX.apiUrl,
  dashboardOrigins: GENEX.dashboardOrigins,
});
```

On a hosted page identity takes seconds (the dashboard handshake, or the standalone bounce), and
`waitForPlayer()` never resolves when `initEmbed()` was never called, because nothing else
resolves that promise.


Scene setup and asset loading may continue immediately after this call — auth
never blocks rendering. There are **two gates**, and picking the right one
matters:

```ts
import { waitForPlayer, waitForAuth, getColyseusAuth, getEmbedToken } from "@genex-ai/embed-sdk";

// PLAYER gate — resolves for guests AND signed-in players. Use for
// multiplayer connect() and player-name UI. This is the gate almost
// everything wants.
const { user, guest } = await waitForPlayer();
// user.id / user.name — real account identity, or guest:<id> / "Guest-1234"
// user.avatarUrl — the player's OWN VRM avatar (profile pick; per-session for
// guests). It is the FALLBACK body, not the game's character: pass it to
// loadPlayerCharacter({ avatarUrl: user.avatarUrl }) and it is used only when
// this game has no generated character of its own, with the baked
// ./assets/avatar.vrm behind it (absent on old APIs / local test mode).
// Peers resolve the same way via the multiplayer SDK's player.avatarUrl.

// ACCOUNT gate — resolves ONLY for signed-in players. For a guest it stays
// pending for as long as this page is loaded: signing in loads the game
// again, and the gate resolves on that load. Use ONLY for /state
// saving/loading and other account-bound features.
const { user: account } = await waitForAuth();
```

**NEVER gate scene boot or `connect()` on `waitForAuth()`** — for a guest it
stays pending forever and your game would sit empty. `waitForPlayer()` is the
boot-path gate; `waitForAuth()` guards saves only.

## API surface (exact — do not invent methods)

- `initEmbed({ slug, apiUrl, dashboardOrigins })` — call once, first. All three
  fields required (from `genex.config.ts`).
- `waitForPlayer()` → `Promise<{ user, guest }>` — THE gate for `connect()`
  and player-name UI; resolves for guests and accounts alike, rejects only if
  the session ends up blocked.
- `waitForAuth()` → `Promise<{ user }>` — the gate for `/state` calls and
  account-bound features. Stays PENDING for a guest for the whole page load
  (signing in loads the game again, and it resolves on that next load);
  rejects if blocked. Catch rejections and let the SDK's overlay handle the
  UX (don't build your own sign-in UI).
- `isEmbedded()` → `boolean` — structural "is in an iframe" check; NOT the same
  question as "is signed in".
- `getAuthState()` → `"pending" | "authenticated" | "guest" | "blocked"` —
  synchronous.
- `getUser()` → `{ id, name, image? } | null` — non-null once authenticated OR
  guest. Guest ids are prefixed `guest:` (local test mode: `local:test`).
- `getEmbedToken()` → `string | undefined` — the raw token, for the RARE
  advanced case of calling the Genex API by hand. The state/leaderboard
  helpers below attach it automatically — prefer them; never hand-roll fetch
  calls to `/state` endpoints.
- `getColyseusAuth()` → `{ embedToken } | undefined` — relay credential
  (REQUIRED; guest tokens are accepted). Pass `auth: () => getColyseusAuth()`
  to both `connect()` and `matchmake()` so each explicit connect and every
  automatic re-seat reads a fresh token. Tokens rotate automatically (~every
  10 minutes). Never cache the value across joins and never log it.
- `on(event, cb)` → unsubscribe fn. Events: `"authenticated"`, `"guest"`,
  `"blocked"`, `"error"`. A page load ends in one of the first three. Signing
  in loads the game again, so the account arrives as `"authenticated"` on
  the next load, not as a second event on this one.

Where the game is running and what it was opened with (`@genex-ai/embed-sdk`
0.32.0+; all three are safe to call before `initEmbed()`):

- `getShell()` → `"page" | "app" | "standalone" | "local"` — which shell this
  is. A fact about the page: not who is signed in, and not a permission. Any
  frame is `"page"`, whoever frames it, and the whole page of any React
  Native web view is `"app"`.
- `getEntry()` → `{ search, params, hash, referrer }` — the link the game was
  opened with: its own query (`search` as text, `params` as
  `URLSearchParams`), its own fragment, and the origin of the site the visitor
  came from, or `null`.
- `onShellClosing(cb)` → unsubscribe fn — `cb` runs when the page is being
  taken away: the tab closed or reloaded, the app closing the game. The last
  chance for a small `savePlayerState()`, never the only one.

Platform calls (0.32.0+): one call each that does the right thing in
whichever shell the game is in. **Call them from a click or tap handler,
before any `await`.** They resolve and never throw. What each one does in
each shell is in [references/shells.md](references/shells.md).

- `share({ text?, params? })` → `Promise<{ status, url }>`; `status` is
  `"shared" | "copied" | "dismissed" | "unavailable"`. The SDK builds the
  link; the game supplies only its own `params`. A link whose preview card
  shows the player's own result needs a server of the creator's own, and only
  when the person asks for one: "A result link with its own preview picture"
  in [references/shells.md](references/shells.md).
- `copyText(text)`, `keepAwake(on)`, `openExternal(url)`,
  `saveFile(blob, name)`, `setFullscreen(on)` →
  `Promise<{ ok: true } | { ok: false, error }>`; `error` is `unsupported` |
  `needs_gesture` | `dismissed` | `busy` | `rate_limited` | `invalid_request`
  | `too_large` | `timeout`. `unsupported` and `timeout` are ordinary answers,
  not bugs.
- `haptic(kind)` → nothing; `kind` is `"selection" | "light" | "medium" |
  "heavy" | "success" | "warning" | "error"`.
- `supports(name)` → `boolean`, synchronous: whether to draw the button at
  all. `name` is `"share" | "copy" | "awake" | "haptic" | "open" | "save" |
  "fullscreen"`.

Durable state + leaderboards (all six are safe to call from boot — they wait
for identity internally, never throw for guests, and reject only when the
session is blocked):

- `loadPlayerState()` → `Promise<{ data, version, guest?, staging? }>` — THIS
  player's own save (per-player, per-game; other players can never read or
  overwrite it). `{ data: null, version: 0 }` when they never saved.
- `savePlayerState(data, { ifVersion? }?)` → `Promise<{ saved, version?,
  conflict?, guest?, queued?, staging? }>` — save any JSON ≤ 256KB to their
  slot. For a guest nothing is saved: the value is held in memory for this
  page load only (`{ saved: false, guest: true, queued: true }`), and signing
  in loads the game again. Small saves survive tab close automatically.
- `loadWorldState()` / `saveWorldState(data, { ifVersion? }?)` — the game's
  ONE shared world slot (≤ 1MB, every player reads/writes the same blob) —
  level layouts, persistent-world object positions. Multiplayer games: only
  the host writes it (see the multiplayer skill). Always pass `ifVersion`
  here (shared slot = real races); a losing write resolves
  `{ conflict: true, version }` — reload, merge, retry.
- `submitScore(score, { board?, mode? }?)` → `Promise<{ submitted, best?,
  improved?, guest?, queued? }>` — keep-best leaderboard submit (`mode:
  "min"` for lap-time boards). A guest's score is not posted: the best value
  is held in memory for this page load only.
- `getLeaderboard({ board?, limit?, order? }?)` → `Promise<{ items, me }>` —
  top entries (verified display names — never trust client-side name input
  for this) + the signed-in player's own `{ rank, score }`. Works for guests
  too (`me: null`). `limit` caps at 100 server-side. Local test mode resolves
  `{ items: [], me: null }` locally.

Server write limits (per player, per minute): **60 player-saves, 120
world-saves, 30 score submits**. A debounced ~1/sec checkpoint never gets near
them — only a save-per-frame loop does (it surfaces as HTTP 429).

**The preview channel has no server saves.** The owner's draft workspace and
every `preview--<slug>` URL play the STAGING build, and the API refuses loads
and saves there by design (a staging build with a changed save schema must
never overwrite the save of the game people are playing). The helpers resolve
`{ staging: true }` — `loadPlayerState()` → `{ data: null, version: 0,
staging: true }`, `savePlayerState()` → `{ saved: false, staging: true }` —
and never throw or fire `"error"` for it.


## Saving progress (per-player — every player has their own slot)

Use the SDK helpers; never hand-roll fetch calls to the state API. Progression,
inventory, unlocks — anything about ONE player — goes in their player slot:

```ts
import { loadPlayerState, savePlayerState } from "@genex-ai/embed-sdk";

// boot: load whatever this player saved last time (fine for guests — resolves
// { data: null, guest: true } — and on the preview channel — { data: null,
// staging: true } — instead of failing)
const { data } = await loadPlayerState();
applyProgress(data ?? defaultProgress());

// checkpoints / level-ups: fire-and-forget, DEBOUNCED (not per frame)
void savePlayerState(progress);
```

Guests need no gating: the helpers resolve for them instead of failing. But
**a guest's progress is not saved, and it does not follow them into an
account.** The SDK holds a guest's latest save in memory for this page load
only, and signing in on the game's page or its own address loads the game
again (the SDK's popover and the Genex page both leave for the sign-in and
come back to a fresh load), so that value is gone when the account arrives.
Signing in from another tab changes nothing until the game is reloaded. If a
guest's run should survive signing in, keep your own copy on the device and
start from it when the account has no save of its own:

```ts
// at every checkpoint: the device's copy, then the save
try { localStorage.setItem("progress", JSON.stringify(progress)); } catch {}
void savePlayerState(progress);

// at boot, in place of the plain load above. loadPlayerState() waits for the
// player, so on the load after a sign-in this is already the account.
const { data, guest, staging } = await loadPlayerState();
let kept: unknown = null;
try { kept = JSON.parse(localStorage.getItem("progress") ?? "null"); } catch {}
applyProgress(data ?? kept ?? defaultProgress());
// An account with no save of its own yet keeps what this device had.
if (data === null && kept !== null && !guest && !staging) void savePlayerState(kept);
```

That copy is a cache for this device and this shell, never the save: an
account that already has a save keeps it, and the copy does not exist on
another device or on the game's other address. The SDK already tells guests
to sign in (its popover / the dashboard's card) — don't add another prompt.

**Per-player vs world:** `savePlayerState` is each player's own progress;
`saveWorldState` is the game's ONE shared world (persistent-world layouts —
see the multiplayer skill's persistence section for the host-writes pattern).
Never store per-player progression in the world slot: every player of the
game shares that single blob.

## Leaderboards

```ts
import { submitScore, getLeaderboard } from "@genex-ai/embed-sdk";

// on game over / lap complete — keep-best, so just submit every run
void submitScore(finalScore);                            // higher is better
void submitScore(lapMs, { board: "laps", mode: "min" }); // lower is better

// render a top-10 + the player's own rank
const { items, me } = await getLeaderboard({ limit: 10 });
```

Scores are per-account (one row per player per board, real display names from
their Genex account) and keep-best — submitting a worse score changes nothing
(`improved: false`). Guests can READ leaderboards; a guest's submit is not
posted, and signing in loads the game again, so submit when a signed-in
player finishes a run. Send a consistent `mode` per board. Scores are
client-reported (arcade-style trust) — don't present them as anti-cheat.

## NEVER log the tokens

**NEVER log the return value of `getEmbedToken()` or `getColyseusAuth()` — not
to `console.log`, not to a crash-reporter or analytics breadcrumb.** The token
is bounded (15 minutes, one game, one scope), but third-party logging-service
retention can outlive that. Nothing in normal game code ever needs to print it.

## Standalone behavior (what to expect, not something to code)

Opening a published game's link directly (not from the dashboard) shows a
brief "Loading…" overlay while the SDK round-trips through Genex once, then
the game starts: already-signed-in visitors come back authenticated (zero
clicks — on every game), everyone else comes back playing as a guest with the
SDK's own top-right "sign in to save progress" popover. The return trip
carries a one-time pass (or an inert guest marker) in the URL that the SDK
consumes and removes immediately. Unpublished drafts are the exception:
strangers can't play them, so a draft link shows the SDK's sign-in gate
instead (for self-testing, see local test mode below). Don't code around any
of this: `isEmbedded()` and the return-trip handling are internal SDK
concerns.

Your own `?query` comes through that round trip on every published game. Your
`#fragment` and the site the visitor came from need `@genex-ai/embed-sdk`
0.32.0+, written in `package.json` as a range that starts there (`^0.32.0`)
when the build was shipped.
Read all three with `getEntry()`, never from `location` or
`document.referrer`: until `initEmbed()` has run the address bar still holds
Genex's own fragment, and `document.referrer` is Genex's address or empty.
`embed` and every key starting `genex_` are reserved. Sizes, the other
reserved names and what each shell passes on are in
[references/shells.md](references/shells.md).

### Self-testing a draft: local test mode

An unpublished draft shows the sign-in gate to any browser that isn't signed
in as the owner — **including your own test browser** (Playwright, headless
Chrome) — and the hosted draft URL applies the same identity rule. The one
supported way to see and play the game yourself is **local test mode**: open
the local dev server with the explicit opt-in marker —

```
http://localhost:5173/?genex_local_test=1
```

(any port; append with `&` if the URL already has a query). On an exact http
loopback origin (`localhost`, `127.0.0.1`, `[::1]`) the SDK skips the
identity flow entirely and boots a guest-like session: no redirect, no
overlay, `waitForPlayer()` resolves with the unmistakable local identity
`{ id: "local:test", name: "Local Tester" }`, and the console prints a
"local test mode" notice. Requires `@genex-ai/embed-sdk` 0.5.0+ — on an older
project the marker does nothing; apply the pending platform update first (any
`genex` command prints the update nudge and how to apply it), then retry.

**It validates:** rendering, camera, controls, HUD, game feel, and real
gameplay screenshots — everything local.

**It does NOT validate** (nothing online exists in this mode; no credential
is ever minted): real sign-in (`waitForAuth()` stays pending, exactly like a
guest), saves (they queue in memory), leaderboards (`getLeaderboard()`
resolves `{ items: [], me: null }` locally), score submits, and multiplayer
(`getColyseusAuth()` is `undefined`, so `connect()` fails at the relay —
expected in this mode, not a bug to chase). Nor anything the game's Genex
page or the app refuses: this is a plain browser tab, so `window.open`, a
download link and a browser dialog all work here and are dead there
([references/shells.md](references/shells.md)).

Rules:

- Pointer lock still can't be acquired headlessly (`requestPointerLock`
  throws in headless Chromium).
- The marker is inert on any hosted URL, on https, and inside any iframe —
  local test mode cannot open the hosted draft; hosted draft access stays
  owner-only. Do NOT work around that gate: no undocumented URL fragments,
  no auth mocks, and never drive the user's own signed-in browser.
- Opening localhost WITHOUT the marker boots local test mode too on
  `@genex-ai/embed-sdk` 0.14.0+ (an older SDK runs the identity bounce
  there). Keep the marker in every URL you open: it says what you meant and
  works on every SDK since 0.5.0. `?genex_auth=1` opts that dev-server tab
  back into the real identity flow — that's for debugging real sign-in, not
  for self-testing.
- A hosted draft exercises what local test mode can't: real identity,
  saves, multiplayer. Once the game is **published**,
  any fresh browser gets in as a guest, so full visual validation also works
  without the marker.

## Checklist

- [ ] Multiplayer and player-name UI await `waitForPlayer()` — NEVER
      `waitForAuth()` (guests would hang forever). Both `connect()` and
      `matchmake()` receive `auth: () => getColyseusAuth()`.
- [ ] Saves/loads use the SDK helpers (`savePlayerState`/`loadPlayerState` for
      per-player progress, `saveWorldState`/`loadWorldState` for the shared
      world, `submitScore`/`getLeaderboard` for scores) — no hand-rolled fetch
      to `/state` endpoints, no manual guest gating (the helpers own it).
- [ ] Per-player progression lives in the PLAYER slot, never in the shared
      world slot.
- [ ] Saves are debounced (checkpoints/level-ups), not per-frame.
- [ ] No token value is ever logged or sent to analytics.
- [ ] No custom sign-in prompt, guest badge, or auth overlay — the SDK popover/
      overlay and the dashboard own all of that UX.
- [ ] Every browser or device API the game calls has its row in
      [references/shells.md](references/shells.md): sharing, copying, links
      out, file saves and fullscreen go through the SDK calls, from a click
      or tap handler; the game's own URL parameters come from `getEntry()`.

## Troubleshooting

- **Game loads then immediately navigates away (the game's own link)** — the
  identity bounce, working as designed for EVERY standalone visit. It returns
  to the game automatically (signed-in or as a guest) within a second. On a
  dev server it only happens with `?genex_auth=1` or an SDK older than
  0.14.0: open with `?genex_local_test=1`.
- **Works locally or on the game's own link, does nothing on its Genex page
  or in the app** — that shell refuses the call, with no error. Find the row
  in [references/shells.md](references/shells.md) and make the call it names.
- **`waitForAuth()` never resolves** — the player is a GUEST; that's the
  designed behavior. Anything that must run for guests belongs behind
  `waitForPlayer()` instead.
- **State is `"blocked"` / `waitForPlayer()` rejects** — an unpublished draft
  opened by a non-owner, or auth infrastructure was unreachable. The SDK
  overlay (or the dashboard, when embedded) shows the sign-in prompt; the game
  just stays paused behind it. Don't retry in a loop. Self-testing a draft
  locally? Use local test mode (`?genex_local_test=1`) instead.
- **Local test mode doesn't activate** — check all four: the value is exactly
  `genex_local_test=1`, the origin is http loopback (`localhost`/`127.0.0.1`/
  `[::1]` — not https, not a LAN IP), the page is not inside an iframe, and
  `@genex-ai/embed-sdk` is 0.5.0+ (older: apply the pending platform update).
- **Multiplayer `connect()` fails in local test mode** — by design: no relay
  credential exists there. The preview link has one, and rooms of its own.
- **Multiplayer join rejected with 401** — the join ran before
  `waitForPlayer()` resolved, without `auth: () => getColyseusAuth()`, or with a
  stale cached token on reconnect (read it fresh each call).
- **Multiplayer join rejected with 403 "guest capacity"** — the room is at its
  guest limit; only signing in gets the player a seat right now. Surface the
  relay's message as-is.
- **`/state` returns 401/403 (hand-rolled fetch)** — missing `Authorization`
  header (401), a guest token (403 `guest_no_save`), or the token belongs to a
  different game (403). All three mean the code bypassed the SDK helpers —
  switch to `savePlayerState`/`saveWorldState`, which handle every case.
- **Saves/loads resolve `{ staging: true }`** — the build is on the preview
  channel (the draft workspace, `preview--<slug>`), where server saves are off
  by design. Not an outage.
- **Saves or score submits return 429** — writing too often (per-player limits:
  60 player-saves/min, 120 world-saves/min, 30 score submits/min). Debounce to
  ~1 write/sec at checkpoints and never save in the render loop; back off a
  second and retry.
- **`saveWorldState` resolves `{ conflict: true }`** — another player wrote the
  shared slot since your last read. Expected under concurrency: reload with
  `loadWorldState()`, merge, retry with the fresh `version`. If it happens
  constantly, more than one client is acting as the writer — in multiplayer,
  only the host should save the world.
