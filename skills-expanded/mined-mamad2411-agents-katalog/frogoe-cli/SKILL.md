---
name: frogoe-cli
description: >
  The frogoe CLI development loop: init, add, run, check. Use for scaffolding
  a new game, copying registry HUD blocks, serving with live reload and phone
  QR, and running contract lint with stable finding codes (--json for the
  self-heal loop). Also use when diagnosing scaffold or check failures.
---

# frogoe CLI

Run commands as `bun packages/cli/src/bin.ts <cmd>` from the repo (published:
`npx frogoe <cmd>`). Requires bun.

## Development loop

1. **Scaffold:** `frogoe init my-game` — boots a runnable folder (living
   stub game, BRIEF stub, pinned .frogoe/). `cd my-game`.
2. **Find the part:** before hand-writing HUD, look in the registry —
   `frogoe add fuel-gauge` copies a themeable block into blocks/ and prints
   its bindings + placement snippet. Hand-write only once nothing fits.
3. **Iterate:** `frogoe run` — live reload on every save, QR for the phone
   (safe-area only exists on real devices; test there before shipping).
   Phone on another network / strict wifi? `frogoe run --tunnel` serves a
   public cloudflared URL (auto-downloaded once, cached; reload survives
   SSE-less proxies via a version poll — ≤2s). `frogoe run` itself starts
   the tunnel automatically when the lan looks unreachable (firewall
   blocking, vpn-routed, no lan address) and says so in the banner.
   Playtests are telemetered: fps dips, page errors and lock-screens
   print live in the terminal and persist to `.frogoe/sessions/*.jsonl`
   (local only — nothing leaves the machine). After a session:
   `frogoe report` — duration, fps mean, dips below 30 with their
   wall-clock moment, errors, hidden periods.
4. **Gate:** `frogoe check` — exit 1 on errors. In agent loops use
   `frogoe check --json`; every finding carries {code, file, line, severity,
   fix, recipe} — read the fix, apply, re-run. One iteration heals.

## Finding codes (stable — never renumber)

| Code                                                                                                                 | Severity | Meaning                                      |
| -------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------- |
| brief/missing, brief/frontmatter, brief/todo, brief/contrast                                                         | error    | intent undeclared or incomplete              |
| folder/index-missing, folder/canvas, folder/viewport-fit, folder/touch-select, folder/importmap, folder/game-missing, folder/contract-pin | error    | shell/pin broken (touch-select: phone long-press summons text selection — iOS + Android) |
| input/incremental-drag                                                                                               | error    | the shipped wall-rocket bug (+= p.dx)        |
| input/absolute-steering, layout/innerwidth-spawn                                                                     | warning  | thumb-ghosting / parity risks                |
| audio/suspended-only                                                                                                  | warning  | resume gated on === "suspended" — iOS "interrupted" contexts stay silent (frogoe-core → audio.md) |
| game/loop-update, game/loop-render                                                                                   | warning  | runtime will teach, fix first                |
| blocks/binding-orphan                                                                                                   | warning  | selector targets nothing (block not pasted?) |

## check --live — the sandbox pass

`frogoe check --live` adds a headless-browser pass (chrome-headless-shell,
auto-downloaded + cached, pinned build): loads the real game on the run
server, both viewports (mobile 390×844 + desktop 1280×800). Mobile runs
the FULL LIFECYCLE — boot → play (input ladder: jittered taps + one hold
+ one drag sweep) → end (passive death within 45s) → retry (click
`[data-block-retry]`, expect reload, healthy reboot) → stability (the
death→retry cycle runs twice; works-once bugs surface on round two).
Severity follows the held-failure rule: a defect seen once is a warning;
held across a window it is an error.

| Code                                        | Severity | Meaning                                                                                                                          |
| ------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| live/page-error                             | error    | uncaught exceptions in the page (persists across retries)                                                                        |
| live/console-error                          | warning  | console.error output (de-duplicated against page errors)                                                                        |
| live/canvas-missing / live/canvas-unpainted | error    | no canvas / loop.render never drew (re-checked after each retry reload)                                                          |
| live/contract-missing                       | error    | window.__frogoe absent — the contract never booted                                                                               |
| live/state-stuck                            | error    | state never left "loading" — also fires when a retry reboot lands sick                                                           |
| live/early-death                            | error    | state "over" before any input — the game kills itself on its ready screen; gate physics behind the first input.on("down")         |
| live/hud-outline                            | error    | HUD text without outline/stroke — the GAME readability convention (backgrounds change every frame; the outline is the guarantee) |
| live/layout-collapse                        | error    | HUD element with text but zero box (CSS collapse)                                                                                |
| live/fps                                    | warning  | mean fps below 30 — heavy per-frame work (cache gradients, cut shadowBlur)                                                       |
| live/fps-sustained                          | error    | low fps held 3s+ — consistently slow, not jittering (cut allocations, shrink offscreen canvases)                                |
| live/fps-throttled                          | warning  | collapse under 4x cpu throttle (the Lighthouse mobile anchor) — mid-range phones will feel it; cut per-frame work              |
| live/frozen-frame                           | warning  | canvas held the same frame 3 samples while playing — loop.render stopped or draws a static scene                                |
| live/paused                                 | warning  | state read "paused" during scripted play — pause() without resume()                                                              |
| live/state-corrupt                          | error    | state outside the contract's set — game code mutating window.__frogoe directly                                                    |
| live/no-input / live/not-playable           | error    | game never wired input / scripted taps changed nothing                                                                           |
| live/audio-locked                           | error    | audio stayed suspended after an INJECTED interruption + real input — the game lacks gesture-scoped resume wiring (frogoe-core → references/audio.md) |
| live/never-ends                             | warning  | no death within 45s of passive play — fine for endless games; feed games are short loops                                          |
| live/finish-event-missing                   | error    | "over" without frogoe:finish, or the event without "over" — forged state machine                                                 |
| live/no-gameover-card                       | warning  | ended without a [data-block-gameover] overlay — install game-over-card                                                           |
| live/no-retry                               | error    | no [data-block-retry] button — the player is hard-stuck after death                                                              |
| live/retry-dead                             | error    | clicking retry produced no reload — wire it to location.reload()                                                                 |
| live/runtime-failure                        | error    | the sandbox itself crashed on a viewport — report the output                                                                     |

Snapshots land in `snapshots/` — `live-{mobile,desktop}.png` at boot,
`live-mobile-over{,-2}.png` and `live-mobile-retry{,-2}.png` at each
death/retry — the human-eye evidence. Pure decisions and the full
lifecycle are unit-tested against a scripted driver; the browser path
runs real Chrome (no mocks — quality is measured, not simulated).

## bundle — externals dissolve

`frogoe bundle` turns the folder into ONE self-contained HTML in dist/:
import-map modules bundled (contract inlined), fonts fetched + embedded as
base64 @font-face, local media as data URIs, provenance banner with sha256.
Author-time externals are allowlisted (jsdelivr, esm.sh, unpkg, Google
Fonts) and must be version-pinned — `@latest` and bare tags fail the bundle
with `bundle/unpinned`; unknown hosts fail with `bundle/blocked-origin`.
The artifact self-scans: if any remote URL survives, `bundle/leaked-remote`
fails the build — nothing ships half-dissolved.

## Boundaries

- check is deterministic/static; live output measures (rendered contrast)
  arrive with the sandbox layer. The declared-palette contrast check is the
  static floor.
- bundle requires network for CDN assets (allowlist + pin + sha256); offline
  games with only local assets bundle with zero fetches.
