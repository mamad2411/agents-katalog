---
name: debug-visualization
description: "Use when creating any game or interactive toy, when adding gameplay/UI features to one, when the builder asks for value tweaks in any language (too fast/slow, too big/small, a bit more/less, move it left/right/up/down, can't hit it, my tap doesn't register, hitbox, feels floaty/heavy/off, easier/harder, change X from N to M, 'don't rebuild — just fix this'; 너무 빨라요/느려요, 버튼이 안 눌려요, 판정이 이상해요, 히트박스, 이것만 고쳐줘), or when a message contains a [TUNING] or [ERRORS] block. Once loaded, stays in force for every subsequent message in the session without being re-mentioned. Ships a live in-game tuning panel with every game so builders adjust values themselves instead of burning chat round-trips."
---

# Game Tuning Panel — build it with every game, unasked

Builders lose most of their build time to tiny tuning round-trips: "a bit faster", "move the button left", "make the hitbox bigger" — each one a full chat cycle for what should be a 2-second slider drag. You ship a live tuning panel with **every** game, so those tweaks happen in-game instantly and come back to you as one clean paste.

## If you remember nothing else

1. **Every game gets the panel, unasked.** The builder will not request it and may not know such a thing can exist. Build it anyway, every time.
2. **Every gameplay/UI constant lives in one `DebugPanel.define({...})` schema.** Game code reads `T.group.key` at the point of use — never copied into a variable at init.
3. **A tuning change edits schema defaults ONLY.** Whether the builder types "make jumps higher" or pastes a `[TUNING]` block: change those values, change nothing else, never rebuild.
4. **The panel library ships with this skill as `debug-panel.js`** — paste it verbatim between its sentinel comments, never write your own implementation, and it must survive every future edit untouched.
5. **Announce the panel on the first build, then teach with short tips.** A panel the builder doesn't know about is a failed deliverable — but repeating the same banner every reply deadens it.
6. **Once read, this skill never turns off.** It binds every future message in this session — the builder will never mention it again, and you never ask whether to apply it.

## When this applies

- Creating a game or interactive toy (something with a game loop, player input, score, or win/lose). **NOT** plain pages, forms, or documents — skip this skill entirely for those.
- Adding or changing gameplay/UI features in an existing game.
- Tuning-type requests: "too fast/slow", "too big/small", "a bit more/less", "move it left/right/up/down", "can't hit it / my tap doesn't register", "hitbox", "feels floaty/heavy/off", "make it easier/harder", "change X from N to M", "don't rebuild, only fix this".
- Panel-addition requests: "add ○○ to the tuning panel" — the hint at the bottom of the panel teaches builders to ask exactly this. Register it via the PROMOTE two-step if it's not in the schema yet, and confirm in one line naming the group it landed in.
- Any message containing a `[TUNING]` or `[ERRORS]` line — these come from the panel; handle them exactly per **Protocol** below.

**Litmus test:** if the correct fix is changing ≤3 constant values (number, position, size, color, duration), it is a tuning request → serve it through the schema, never with new inline literals. The litmus decides — trigger phrases only get you here. When the complaint could be a logic bug (especially right after you added the feature involved, e.g. "the boss doesn't take hits"), **read the relevant code first**. If the fix is code, make the smallest code fix with schema defaults untouched, and point the builder at the **show hitboxes** toggle and the **Copy errors** button.

**Reply language:** all builder-facing lines — confirmations, tips, announcements — are written in the builder's language. Keep 🔧/✅, the `[TUNING]`/`[ERRORS]` sentinels, and dotted key paths (`player.speed`) untranslated.

**Persistence — once loaded, always on:**

- This skill applies from the first game-related message and to **every** message after it, without being re-mentioned. Non-game messages in between do not unload it — when game work resumes, the rules still bind.
- Never ask the builder whether to add the panel or follow these rules, and never wait for a reminder. The builder chose this by giving you this repo once; that choice covers the whole session.
- Every new game, every edit, every feature, and every `[TUNING]`/`[ERRORS]` paste in this session is governed by this skill — not just the game it was first applied to.
- If your context no longer contains this skill (long session, summarization, a new agent taking over), re-read `SKILL.md` from this repo **before** touching game code. Tripwires that live in the builder's own repo and survive context loss: the `TUNABLES CONTRACT` comment atop `game.js`, the `debug-panel.js` header, and the repo-root **`AGENTS.md`** you write on the first build (see "Leave the contract in the game repo"). Seeing any of them means these rules are in force — honour them even if you cannot reach the full skill.

## The schema: single source of truth

Every gameplay/UI constant a builder could plausibly ask to change lives in **one** `DebugPanel.define` call near the top of the game code:

```js
const T = DebugPanel.define({
  player:  { _label: 'Player',
             speed:   { value: 220, min: 0, max: 600, label: 'Move speed' },
             jumpVel: { value: 520, min: 100, max: 1200, label: 'Jump strength' },
             hitW:    { value: 28, min: 8, max: 80, label: 'Player hitbox width' } },
  enemies: { _label: 'Enemies',
             spawnMs: { value: 1800, min: 200, max: 6000, label: 'Time between enemies (ms, lower = harder)' } },
  ui:      { _label: 'Buttons',
             shootX:  { value: 24, min: 0, max: 400, cssVar: '--shoot-x', unit: 'px', label: 'Shoot button X' },
             shootW:  { value: 64, min: 40, max: 160, cssVar: '--shoot-w', unit: 'px', label: 'Shoot button width' },
             shootH:  { value: 64, min: 40, max: 160, cssVar: '--shoot-h', unit: 'px', label: 'Shoot button height' } },
});
```

Game code **reads values live, at the point of use**:

```js
// WRONG — captured once at init; the panel slider will silently do nothing:
const speed = T.player.speed;
function update(dt) { player.x += speed * dt; }

// RIGHT — read at use time (destructure only INSIDE the loop body, never above it):
function update(dt) { player.x += T.player.speed * dt; }
```

Rules:

- **Keys are protocol tokens.** Schema keys and group keys are ALWAYS short English ASCII identifiers (`player.speed`, never `플레이어.속도`) — they appear in `[TUNING]` dotted paths and must be stable across languages. All human-facing text lives in `label` (leaves) and `_label` (groups), in the builder's language. The group key `advanced` is recognized by the panel (renders collapsed) — never rename the key; localize only its `_label`.
- NEVER copy a `T` value into a top-level const, a closure, or an object field you don't refresh. If an engine consumes a value once (physics gravity, materials, one-shot CSS), bind it with `onChange` (see recipes). If it only applies at generation time (grid size, level count), flag it `restart: true` and register a Restart button.
- **Timer trap:** `setInterval(spawn, T.enemies.spawnMs)` and `setTimeout(..., T.x)` capture the value once — the slider goes permanently dead. Use a dt-accumulator instead (`spawnT += dt * 1000; if (spawnT >= T.enemies.spawnMs) { spawnT = 0; spawn(); }`) or a self-rescheduling `setTimeout` that re-reads `T` on each schedule.
- **UI geometry is always tunable — position AND size, all four keys.** Every on-screen control the game has — or gains later when you add a feature — gets `x`, `y` (position) **and** `w`, `h` (width and height) in the `ui` group the moment it exists (cssVar-bound for DOM elements; a single `scale` may replace `w`/`h` only when the control can only scale as one unit). Registering position without size is the most common mistake — "make the button bigger" is asked as often as "move it". A new button shipped with only gameplay values (damage, cooldown), or with x/y but no width/height, is an incomplete feature.
- NEVER introduce a new numeric literal, px value, color, or ms duration into gameplay/UI logic. Exempt: 0, 1, -1, 2 as math identities, array indices, math constants (`Math.PI`) — and constants a builder would never plausibly ask about (internal easing factors, z-offsets) may live as named consts in one clearly-marked `// internal constants` section below the schema. When in doubt, put it in `advanced`.
- NEVER change existing schema defaults except through a tuning request or a `[TUNING]` paste.
- **PROMOTE (two-step)** — when a requested value is not in the schema yet: (1) add the key to the schema and replace **every** occurrence of that literal that means the same thing with `T.group.key` (a size used in both draw and collision must not fork); (2) change the default. Typical diff ≈ 3 lines; duplicated-literal use sites are allowed on top — call them out.
- **One define.** In a single-file game, always extend the one top `define`; a second merged `define()` is only for multi-file games where a feature module owns its constants. Merge is first-wins: a later `define()` for an existing path is silently ignored (default, range, label, AND `onChange` all discarded) — to change anything about an existing key, edit the define that first declared it; never attach `onChange` via a second define.

## Tuning requests: routing and diff budget

Map complaints to schema keys (only after the litmus passes):

| Builder says | Change |
|---|---|
| too fast / too slow | speed, velocity, interval, duration keys |
| button too small / can't tap it | `ui.*` size keys (+ hitbox padding) |
| can't hit the enemy / unfair | hitbox w/h keys — and point them at the **show hitboxes** toggle |
| feels floaty / heavy | gravity, jump velocity |
| too hard / too easy | spawn rate, HP, timers |
| too quiet / loud | audio volume keys |
| move it left/right/up/down | `ui.*` x/y keys |

**Diff budget (hard rule):** a `[TUNING]` block with N values → at most N changed schema lines, plus the matching CSS `var()` fallback line(s) for any cssVar key. A typed tuning request → ≤3 changed lines for already-exposed keys, plus ≈3 lines per PROMOTEd key (the litmus caps a tuning request at 3 constants, so worst case ≈9 lines, all schema or use-site substitutions). If your diff is bigger, you are doing it wrong — revert and redo. Never regenerate the file for a tuning request.

**Teach while applying (never refuse, never only-teach):**
- A tweak is *consecutive* when the previous builder message was also a tweak-shaped request (any group); a `[TUNING]` paste resets the count.
- First tweak → apply it AND append one tip line naming the control by its **display labels** (never keys): `Tip: you can drag this live — 🔧 panel → {Player} → {Move speed}.`
- Second and later consecutive tweaks → lead with the control location, then the confirmation: `**{Move speed}** is live in your 🔧 panel ({Player} group) — drag it while playing for instant feel-checks. Applied: 220 → 285.`
- Stop nudging after two leads with no `[TUNING]` paste in response — the builder has chosen chat; keep applying tweaks tip-free and mention the panel again only when a new feature ships.
- When a builder describes broken behavior in prose and a console error is plausible, append one tip: `If an error badge showed up on the 🔧 button, tap Copy errors and paste it here.`

## Protocol: [TUNING] and [ERRORS] pastes

The panel's **Copy changes** button emits (header sentence is localized; the `[TUNING]` sentinel never changes):

```
[TUNING] Apply these as the new defaults. Edit ONLY these values inside DebugPanel.define — do not refactor, rebuild, or change any other code.
player.speed: 220 -> 285
ui.shootX: 24 -> 12
(2 changes from the in-game tuning panel)
```

When any user message contains a `[TUNING]` line:

- Locate the `DebugPanel.define` schema and set each listed dotted path's `value:` to the new value. Values may be numbers, booleans, strings, or `#hex` colors — keep the type exactly. If a path appears more than once, apply the last occurrence.
- If a shown old value doesn't match the current schema default, **apply the new value anyway** (the paste may predate your previous apply) — never stall to ask; append one parenthetical: `(note: player.speed's old value differed from your paste — saved the new value regardless)`. If the new value already equals the current default, say it was already applied. If a listed path is missing from the schema, skip it and name it.
- For cssVar keys, update every CSS `var()` fallback for that variable to the new default in the same diff, and note it (`… + 1 CSS fallback synced`).
- Change **zero** other lines, and reply with one line:

```
✅ Applied 2 tuning changes as new defaults (player.speed 220→285, ui.shootX 24→12). Nothing else touched.
```

No summary, no suggestions, no refactor, no "improvements" to nearby code. If the message also contains other requests, apply the tuning edits exactly per this protocol first (still schema-only, still within budget), make the ✅ line the first line of your reply, then handle the rest normally.

The panel's **Copy errors** button emits:

```
[ERRORS] Fix ONLY this error with the smallest possible change. Keep my tuned values as they are.
TypeError: Cannot read properties of undefined (reading 'x') — at game.html:342 — seen 7×
```

When a message contains an `[ERRORS]` line: fix exactly that error with the smallest change, keep all schema defaults as they are, and confirm in one or two lines referencing the error message. Do not refactor or rebuild.

## Building the panel into a game

**File layout — external files (the default; host-safe). Sandboxed host platforms block inline scripts via CSP (`script-src 'self'`), so the library goes in its own `.js` file:**

```html
<body>
  <script src="./debug-panel.js"></script>   <!-- verbatim library, its own file, loaded FIRST -->
  <script src="./game.js"></script>
</body>
```

`debug-panel.js` is the file shipped next to this skill, byte-for-byte. Head of `game.js`:

```js
/* TUNABLES CONTRACT — read before editing this file.
   1. Every gameplay/UI constant lives in the DebugPanel.define schema below. Never inline new literals.
   2. Tuning requests and [TUNING] pastes edit these defaults ONLY — never restructure other code.
   3. debug-panel.js must be loaded (first script) and stay verbatim.
   4. New feature => add its constants to the schema; the panel picks them up automatically.
   5. A cold agent can re-anchor from AGENTS.md at the repo root. */
const T = DebugPanel.define({ /* ... */ });

// ... game code ...
```

**Only on single-file-only platforms** (where separate files are impossible) may you inline the library — in two separate `<script>` blocks so a corrupted paste can never take the game down with it:

```html
<script>
/* ==== DEBUG PANEL v2 — verbatim library, do not edit (builder's tuning panel). Only the ENABLED and LANG lines may be changed. ==== */
/* ... the full, unmodified contents of debug-panel.js ... */
/* ==== END DEBUG PANEL ==== */
</script>
<script>/* TUNABLES CONTRACT (as above) */ const T = DebugPanel.define({ /* ... */ }); /* ... game code ... */</script>
```

An inline build **cannot be uploaded to a sandboxed host** — `script-src 'self'` blocks inline scripts, so the panel (and the inline game code) won't run there. The moment publishing intent appears, split into external files. If you cannot reproduce the library completely and verbatim, ship the game WITHOUT the panel block rather than with a truncated one.

**Verbatim rule:** paste the library exactly as shipped. The only two lines you may ever change inside the sentinels are `ENABLED` (set `false` on publish) and `LANG` (`'en'` or `'ko'`, match the builder's language). NEVER rename `DebugPanel`, the `[TUNING]`/`[ERRORS]` sentinels, the sentinel comments, or the `advanced` group key — they are protocol tokens.

**Version marker:** the header carries the library version — `v2` is what ships with this skill. The builder's repo holds a byte-for-byte copy, so a copy stamped lower is stale: when you open a game whose header shows an older version, replace the whole library with the shipped one (keeping that repo's `ENABLED`/`LANG` lines) before touching game code. Bump the marker in both files whenever `debug-panel.js` changes.

**API you author against (everything else is built in):**

- `DebugPanel.define(schema) → T` — leaves are `{value, min?, max?, step?, label?, options?, onChange?(v), cssVar?, unit?, restart?}` or bare `number`/`boolean`/`'#hex'`/`string`. Groups take an optional `_label` display name (mandatory whenever the builder's language is not English). Returns the live values tree.
- `DebugPanel.stat(name, fn)` — live readout row (FPS is built in).
- `DebugPanel.box(name, fn)` — hitbox provider for **canvas-drawn** things; `fn` returns `[{x, y, w, h, color?}]` in canvas backing-store pixel coords each frame (or draws directly via the overlay ctx it receives). Shown by the built-in **show hitboxes** toggle. Never write `box()` providers for DOM elements — the built-in **outline UI** toggle covers those. (Simplest: draw hitboxes in your own render pass, where the game's own coordinates are already correct.)
- `DebugPanel.button(label, fn)` — action row. Restart must re-init in-page (call your own `init()`/level-gen, or `scene.restart()` in Phaser). Never `location.reload()`: in sandboxed iframes it silently discards every un-pasted tuned value.
- `const dt = DebugPanel.frame(rawDt)` — one line in the loop wires pause / slow-mo / step-frame. Returns 0 while paused — never divide by dt.
- Built in, zero work for you: floating 🔧 button (top-right, above any on-screen game controls; the panel is a bottom sheet on phones) + backtick toggle (layout-independent), first-run toast, search, per-value reset, Reset all, **Copy changes** (`[TUNING]`, with a synchronous copy fallback for locked-down mobile clipboards), error capture — script errors **and** failed resource loads (images/audio/scripts: COEP blocks, CDN 403s, sprite 404s) — with a badge on the 🔧 button + **Copy errors** (`[ERRORS]`), show hitboxes, outline UI (DOM bounds + px sizes), −/+ steppers for touch fine-tuning.
- Persistence: panel tweaks are saved per value together with the default they were tuned against; a saved tweak is dropped automatically when the code ships a different default for that key (your `[TUNING]` apply wins over the stale tweak). Changing `document.title` resets saved tweaks.

**What to expose (curation, hard rules):** 8–20 controls visible in 3–6 groups, counting only non-`advanced` groups (hard cap 25 visible). `advanced` is uncapped — the no-new-literal rule always beats the count: overflow goes into `advanced`, never back into inline literals. Expose a value only if a builder might plausibly ask to change it in chat; never derived values, loop counters, or two values with a hidden invariant between them. Labels are plain language **in the builder's language**, with units and direction hints (`'Time between enemies (ms, lower = harder)'`) — never variable names.

Genre starting points (then add what the specific game needs):

| Genre | Expose first |
|---|---|
| Platformer | move speed, jump strength, gravity, coyote time (ms), player hitbox scale, enemy speed |
| Shooter | player speed, fire rate, bullet speed/size, enemy spawn interval, enemy HP, screen shake |
| Runner | scroll speed, speed ramp, obstacle gap, jump physics |
| Puzzle | animation speed, input tolerance, hint delay, grid size (`restart: true`) |
| Idle/clicker | income per click, cost curve exponent, tick rate |
| Rhythm | note speed, hit windows (perfect/good ms), **audio offset (mandatory)**, note density |
| Every game | `x`, `y` (position) and `w`, `h` (width/height) for each on-screen control the game actually has, master volume — plus `box()` providers for player, enemies, and every canvas-drawn tappable |

**Wiring recipes:**

- **Canvas loop:**
  ```js
  function tick(now) {
    const dt = DebugPanel.frame(Math.min((now - last) / 1000, 0.05)); last = now; // clamp tab-background spikes
    if (dt) update(dt);            // frame() returns 0 while paused — never divide by dt
    render(ctx);
    requestAnimationFrame(tick);
  }
  DebugPanel.box('player', () => [{ x: player.x, y: player.y, w: T.player.hitW, h: player.h }]);
  DebugPanel.stat('enemies', () => enemies.length);
  ```
  Fixed-timestep loops: feed `frame()` into the accumulator (`acc += DebugPanel.frame(rawDt)`), never into each fixed step. `setInterval` loops: call `const dt = DebugPanel.frame(1/60)` at the top of the tick and return early when it is 0.
  Camera games: inside the `box()` provider, either return boxes already converted to canvas pixels (`x: e.x - cam.x, …`) or apply your camera transform to the overlay ctx yourself (`ctx.save(); ctx.translate(-cam.x, -cam.y); …draw…; ctx.restore()`) — the provider runs in the panel's own loop on a separate overlay canvas, never inside your render pass. Coordinates are the canvas's **internal** (backing-store) pixels: if you scale for devicePixelRatio, multiply box coords by dpr (or `ctx.scale(dpr, dpr)` the overlay ctx first).
- **DOM/CSS game:** route every tunable style through `cssVar` — the panel sets the custom property. Every `var()` usage MUST carry a fallback equal to the schema default, including unit: `#shoot { left: var(--shoot-x, 24px); }`. The fallback is what players get when `ENABLED = false` or the panel block is gone — a stale fallback silently un-tunes the published game. **Hard rule:** any edit that changes a cssVar key's default (typed tweak, PROMOTE, or `[TUNING]` paste) also updates every fallback for that var in the same diff.
- **Phaser (the engine builders reach for most).** Two layers:
  - *Engine consumes values once* (Three.js too): construct the engine reading `T.*` (`gravity: { y: T.world.gravity }`, `new THREE.Color(T.fx.tint)`) — `define()` runs first, so this also picks up values restored from a previous session; `onChange` does NOT fire for that initial value. Add a guarded `onChange` for live edits: `onChange: v => { const s = game?.scene?.scenes?.[0]; if (s) s.physics.world.gravity.y = v; }`. Never use `this` in a top-level schema; always guard `onChange` against the engine not existing yet (restored values fire `onChange` during `define()`). Values needing a fresh scene get `restart: true` + `DebugPanel.button('Restart', () => scene.restart())`. Call `DebugPanel.define` **once at the top level, never inside `create()`** (which re-runs on restart).
  - *Four things the panel can't wire for you, because Phaser runs its own loop:*
    1. **Pause / slow-mo don't reach Phaser on their own.** `DebugPanel.frame()` only scales the dt *you* integrate; Phaser's physics, tweens, timers and animations run on Phaser's own delta and ignore it. Collapse the two panel controls into one *effective scale* (`0` = frozen) and mirror it into the scene **only when it changes** — so you never stomp a pause/slow the game sets for its own effects (hitstop, cutscene). Do **not** use `scene.pause()`: a paused scene stops `update()`, so it could never poll its way back on.
       ```js
       create() { this._eff = 1; }                            // last effective scale: 0 frozen · 1 normal · 0.5 half
       update(time, delta) {
         const eff = DebugPanel.paused ? 0 : DebugPanel.timeScale;
         if (eff !== this._eff) {                              // only on change — don't clobber game-owned pauses
           this._eff = eff;
           this.time.timeScale = this.tweens.timeScale = eff;  // timers + tweens (0 = frozen)
           this.anims.globalTimeScale = eff;                   // animations
           if (this.physics && this.physics.world) {           // Arcade bodies
             this.physics.world.isPaused = (eff === 0);
             if (eff) this.physics.world.timeScale = 1 / eff;  // ⚠ Arcade timeScale is INVERSE (2 = half speed)
           }
         }
         if (eff === 0) return;                                // panel paused — skip your own update
         const dt = (delta / 1000) * eff;
         player.x += T.player.speed * dt;                      // read T.* at the point of use
       }
       ```
    2. **Hitboxes via `box()` work against Phaser's canvas.** The built-in **show hitboxes** toggle finds Phaser's canvas automatically; return Arcade **body** coords minus camera scroll — they line up because `Scale.NONE` keeps the canvas backing store equal to world units (so keep Phaser at default resolution, no custom backing size):
       ```js
       const cam = this.cameras.main; // default zoom 1
       DebugPanel.box('player', () => [{ x: p.body.x - cam.scrollX, y: p.body.y - cam.scrollY, w: p.body.width, h: p.body.height }]);
       ```
       For a **scrolling or zooming camera**, prefer Phaser's native debug instead — a schema boolean whose `onChange` toggles `this.physics.world.drawDebug` (`this.physics.world.createDebugGraphic()` first if arcade `debug` was off; `debugGraphic.clear()` when turning it off). Phaser draws it inside its own camera transform, so it stays correct with no manual scroll/zoom math.
    3. **Surface Phaser loader failures in the panel.** The panel's error capture only sees DOM-attached elements; Phaser loads textures/audio off-DOM, so a missing sprite never reaches the 🔧 badge. Bridge it once in `preload`:
       ```js
       this.load.on('loaderror', f => window.dispatchEvent(new ErrorEvent('error',
         { message: 'Phaser load failed: ' + f.key + ' — ' + f.src, filename: f.src })));
       ```
       Now a failed load shows in the ⚠️ errors group and **Copy errors** (`[ERRORS]`) like any other error.
    4. **Phaser HUD uses numeric keys, not `cssVar`.** `cssVar` and the **outline UI** toggle only touch DOM nodes; Phaser draws its HUD inside the canvas. Expose an in-canvas control's position/size as plain numeric schema keys read where you place the GameObject (reposition via `onChange`, or `restart: true` for layout done once in `create`). `cssVar` stays for DOM-based on-screen controls.
- **React-ish:** keep sim values in a mutable object outside React state and read `T.*` in the game loop; for values that affect rendered JSX, add `onChange: bump` to EACH such key (`bump` = version-bump setState) — there is no global change hook, one `onChange` cannot see other keys. Guard `bump` against firing before mount: restored values fire `onChange` during `define()`.

**Failure posture (invariant):** the game must behave identically if the panel block is deleted or its init throws (the library's built-in shim + your CSS `var()` fallbacks guarantee this — don't undermine them). Never make game logic depend on the panel existing beyond the `T =` define call and the optional `frame()` line.

## Announce and teach

**When the full announcement fires:** (a) the first build of a game; (b) once more later ONLY if several tweak requests have gone by and no `[TUNING]` paste has ever arrived. Feature additions get the short line instead. Tuning replies end with the tip line (typed tweaks) or the ✅ line (`[TUNING]` pastes) — never the full announcement.

**Publish-off reminder (occasional — important).** The panel MUST be hidden from players before the game ships, and the builder may not even know it exists (it can be injected silently). So *drop a one-line reminder every few substantive edits* — and again whenever the game looks close to finished — that the tuning panel must be turned off before publishing. Keep it light and infrequent: never on `[TUNING]`/`[ERRORS]` protocol replies, never right after the full announcement, and not two replies in a row. This is the one extra line you may append on top of a feature-addition or general-edit reply. (When the builder actually signals publish intent, the **Publish intent** rule below takes over: you set `ENABLED = false`.)

> Reminder line (builder's language): `Heads-up — before you publish or share this, the 🔧 tuning panel should be turned off so players don't see it. Just say "publish it" and I'll switch it off and get it ready.`

The announcement (adapt the two placeholders to this game's actual control labels — the same strings shown in the panel; no keyboard shortcuts — most builders are on mobile, and the panel's own first-run toast teaches desktop players):

> 🔧 Your game has a live tuning panel: tap the 🔧 button in the game to adjust things like **{Jump strength}** and **{Time between enemies}** while you play. When it feels right, tap **Copy changes** and paste the result here — I'll save those as the new defaults.

- After adding a feature: register its tunables and say so — `Added 3 sliders to your 🔧 panel ({Boss} group).`
- **Publish intent** — the builder signals the game is finished and ready for others to play, in any language (EN: "publish", "done", "ship it", "release", "share it"; KO: "완성", "배포", "출시", "공유", "올려줘") → set `ENABLED = false` inside the panel block. NOT publish intent: mid-build satisfaction, or any message that also requests further changes — if more work is asked in the same message, keep the panel on.
- If the game is still a single inline file, **split the library and game code into external files** (`<script src>`) as part of publishing — inline scripts are blocked by a sandboxed host's CSP and the game would not run there.
- Before setting `ENABLED = false`, add one line: `If you have panel tweaks you haven't pasted as [TUNING] yet, tap Copy changes and paste them first — un-pasted tweaks won't ship.`
- Publish confirmation: `Hid the tuning panel for players — say "show the panel" to bring it back.` Re-enable on any show-the-panel intent (EN: "show the panel"; KO: "패널 다시 켜줘/보여줘") → `ENABLED = true`. **NEVER delete the panel block.**

## Leave the contract in the game repo — `AGENTS.md`

A builder's later edits often land in a **fresh session or a different tool** that never loaded this skill — and the only thing that survives is what sits in their game repo. The `debug-panel.js` header and the `TUNABLES CONTRACT` comment atop `game.js` are the in-file tripwires; back them with a repo-root **`AGENTS.md`** a cold agent reads before touching code.

**On the first build — and whenever you add the panel to a game — ensure `AGENTS.md` exists at the repo root carrying this block, created and refreshed only between its markers.** Never touch text outside the markers (the builder's own notes, or blocks other tools manage), and if the file is absent create it starting with a `# AGENTS.md` line.

```markdown
<!-- TUNING PANEL CONTRACT — auto-managed, do not hand-edit between these markers -->
## 🔧 This game has a live tuning panel (`debug-panel.js`) — read before editing game code
- **Every gameplay/UI constant lives in ONE `DebugPanel.define({...})` schema**; game code reads `T.group.key` at the point of use — never copy it into a top-level const. `debug-panel.js` is verbatim — do not edit it.
- **A tuning request or a `[TUNING]` paste edits schema `value:` defaults ONLY** — never rebuild or refactor. A `[ERRORS]` paste = fix that one error with the smallest change.
- **A new feature adds its constants to the schema** — including `x`/`y`/`w`/`h` for every on-screen control.
- **Turn the panel OFF (`ENABLED = false`) before publishing.**
- Full rules: the `TUNABLES CONTRACT` comment atop `game.js` and the `debug-panel.js` header. Re-read them before any non-trivial edit.
<!-- END TUNING PANEL CONTRACT -->
```

It is a repo document for agents, not a game asset — it need not go into the published sandbox bundle.

## Before you respond — final gate

Run this on every reply that changed game code:

- [ ] Any new ≥2-digit literal, px, #hex, or ms value in gameplay/UI logic? → move it into the schema (or the marked `// internal constants` section if a builder would never ask about it)
- [ ] `debug-panel.js` loaded first and verbatim as an external file (or, single-file-only, the panel block intact between sentinels in its own script tag), `define()` called before game code? For sandboxed-host publishing: external files, **no inline `<script>`**.
- [ ] Tuning request or `[TUNING]` paste? → diff confined to schema `value:`s (+ matching CSS fallbacks), within budget
- [ ] New feature? → its tunables registered (English keys, localized `label`/`_label`) — **including all four of `x`, `y` (position) and `w`, `h` (width/height) for every new on-screen control; position without size is incomplete** — `box()` providers still correct, short line announced
- [ ] Every schema value actually takes effect live (read-at-use, `onChange`, or `restart: true` + Restart button)? No timer-trap `setInterval(…, T.x)`?
- [ ] Phaser game? → `define()` once at top level (not in `create()`); panel pause/slow-mo mirrored into the scene (Arcade `timeScale` inverse); `box()` uses body coords minus camera scroll (or `world.drawDebug`); loader errors bridged; HUD tunables numeric, not `cssVar`
- [ ] Repo-root `AGENTS.md` present and current with the Tuning Panel contract block (write it on the first build; refresh only between its markers)?
- [ ] Would this game's most likely complaints (too fast / can't tap it / too hard) each map to a **visible** control? If not, promote it out of `advanced` now
- [ ] Been several edits since the last publish-off reminder, or does the game look near-done? → append the one-line "turn the panel off before publishing" reminder (skip on `[TUNING]`/`[ERRORS]`/tip/announcement replies, and not two replies in a row)
- [ ] Reply ends correctly: full announcement (first build only), short feature line, tip line, ✅ line (`[TUNING]`), short fix confirmation (`[ERRORS]`), or publish confirmation — one of these, never stacked. (Exception: the occasional publish-off reminder may be appended to a feature-addition or general-edit reply.)
