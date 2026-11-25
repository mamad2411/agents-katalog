---
name: sega-master-system-devkitsms
description: >-
  Program, build, debug, and port Sega Master System (and Game Gear / SG-1000)
  homebrew games in C with devkitSMS (SMSlib + PSGlib) and the SDCC Z80
  compiler. Use whenever the user writes, compiles, fixes, optimizes, or ports
  an SMS/Master System or Game Gear game or demo: the SDCC + devkitSMS
  toolchain; producing a `.sms`/`.gg` ROM; VDP tiles, the tilemap, hardware
  sprites, palettes, PSG music/SFX, joypad input, VBlank/line interrupts, ROM
  bank switching, SRAM saves; converting assets (`.psgcompr` tiles, `vgm2psg`
  music, `folder2c`/`assets2banks`); or debugging the classic "compiles but
  boots to a black screen" failure. Trigger on mentions of devkitSMS, SMSlib,
  PSGlib, SDCC `-mz80`, ihx2sms, crt0_sms, `SMS_addSprite`/`SMS_waitForVBlank`,
  a `.sms` ROM, Master System / Game Gear homebrew, or Haroldo-OK's SMS games
  (Jill of the Jungle, Dangerous Dave, Food Fighter, Sub Rescue, Commander
  Keen). Prefer it over general knowledge for the SMS toolchain, VDP limits, or
  ROM format — easily gotten wrong from memory.
---

# Sega Master System game development & porting (devkitSMS)

This skill turns an idea — or an existing game to port — into a **playable,
verified `.sms` ROM**, built with **SDCC** (Z80 C compiler) and **devkitSMS**
(sverx's SMSlib + PSGlib). It bundles a consistent toolchain snapshot, project
templates, a headless test emulator, and references distilled from Haroldo-OK's
open-source SMS games.

The SMS is a Z80 with a tile/sprite VDP (256×192, two 16-colour palettes,
≤64 sprites / 8-per-line), a 4-channel PSG, and **8 KiB of RAM**. There is no
framebuffer and no float unit. Success means respecting those limits, not
fighting them.

Do **not** rely on memory for SMSlib signatures, VDP addresses, build flags, or
the ROM header — they are precise and version-sensitive. Read the references and
**verify by building and by running the test harness.**

## Definition of done (do not stop at "it compiled")

A ROM that links tells you almost nothing; the default failure is a clean build
that **boots to a black screen**. A task is done only when all hold — report each:

1. **Compiles and links** — no SDCC errors, no `?ASlink` undefined-symbol warnings.
2. **Becomes a ROM** — `ihx2sms` reports `SEGA header found, checksum updated`.
3. **Not a black screen** — `smstest` boots the real ROM; a screenshot frame has
   the display on and several distinct colours.
4. **Reaches its states** — scripted input drives title → play (→ game over) and
   named game variables take expected values.
5. **Reachable by the user** — the `.sms` is copied to a known output path and
   presented, not left in a scratch dir.

Details and the harness DSL: `references/testing.md`.

## Step 0 — set up the toolchain (once)

```sh
bash scripts/setup_toolchain.sh          # installs SDCC, builds tools + harness
export PATH="$HOME/.devkitsms/bin:$PATH" # ihx2sms, folder2c, smstest, assets2banks
```

This installs SDCC (≥ 4.2, required), builds `ihx2sms`/`folder2c` from the
bundled public-domain sources, installs a **mutually-consistent** SMSlib/PSGlib/
crt0/header set into `~/.devkitsms`, builds the `smstest` emulator, and runs a
smoke build. Full details + flag meanings: `references/toolchain-and-build.md`.

## Pick the workflow

- **New game from scratch** → copy `assets/template/` (Makefile + `src/main.c`
  skeleton), then read `references/game-structure.md` for the frame loop, actor
  pattern, fixed-point, and collision model. For a game like an existing one,
  clone that reference repo instead (`references/examples.md`). For a **Game
  Gear** target read `references/game-gear.md` first. For a **tile-grid / maze**
  game (Pac-Man, Sokoban, Bomberman) also read `references/grid-and-maze-games.md`
  (lane movement, turn-queuing, tunnel wrap, target-cell chaser AI, procedural
  art, maze validation); for an **RPG / adventure / roguelike** (scrolling world,
  menus, dialogue, turns, battles, saves) read `references/rpg-adventure-roguelike.md`.
- **Porting an existing game** (DOS/SDL/Allegro/C, C64/6502, Game Boy, MSX, GBA,
  Genesis, browser/JS, another console) → `references/porting.md` (if the original
  is a **script/bytecode VM**, also `references/interpreter-ports.md`; if a view is
  too expensive to compute live but is a pure function of a little state,
  `references/prerendered-video.md`; for rotation / scaling / pseudo-3D or a
  raycaster the VDP can't do natively, `references/faux-rotation-and-pseudo-3d.md`).
  Core idea: keep the platform-clean game logic, rewrite
  the platform layer against SMSlib, down-res to 256×192, turn runtime bitmaps
  into compiled-in tiles, replace framebuffer collision with a RAM tile-grid, and
  kill floating point.
- **Building/fixing an existing devkitSMS project** → use the project's **own**
  vendored SMSlib (header+lib together — see the version rule below). Regenerate
  data with `folder2c`, then build.
- **Debugging** → jump to "Black-screen triage" below and `references/testing.md`.
- **Optimizing** → fixed-point everywhere, precomputed LUTs, avoid `*`/`/`/`%` by
  non-powers-of-two, `--max-allocs-per-node 100000`, keep hot data in RAM.

Whatever the path, wire up a `smstest` playtest early — it is how you *know* you
are done instead of hoping.

## The build pipeline (four steps)

```sh
folder2c data data                          # assets/ -> data.c + data.h
sdcc -c -mz80 -I$DK/include \               # each .c -> .rel
     --peep-file $DK/include/peep-rules.txt  file.c -o file.rel
sdcc -o game.ihx -mz80 --no-std-crt0 --data-loc 0xC000 \   # link (crt0 FIRST,
     $DK/lib/crt0_sms.rel *.rel $DK/lib/SMSlib.lib $DK/lib/PSGlib.lib  # libs LAST)
ihx2sms game.ihx game.sms                    # .ihx -> padded ROM + checksum
```

`$DK` = `~/.devkitsms`. Prefer `assets/template/Makefile` (single ROM) or
`assets/template/Makefile.banked` (>48 KiB, bank-switched); both add a `playtest`
target. Linking also emits `game.noi` (symbols the test harness reads) — keep it.

## The canonical frame loop

```c
for (;;) {
    keys = SMS_getKeysStatus();          // input
    update_world();                      // RAM-only: physics, AI, collision (fixed-point)
    SMS_initSprites();                   // build sprite list in RAM
    draw_actors();                       //   SMS_addSprite / SMS_addSpriteClipping
    SMS_finalizeSprites();
    SMS_waitForVBlank();                 // frame clock (60/50 Hz), exactly one per loop
    SMS_copySpritestoSAT();              // push sprites — FIRST thing after VBlank
    update_hud();                        // any other VRAM writes go here too
}
```

**The one hard rule: touch VRAM / CRAM / the sprite SAT only during VBlank.** All
game logic is RAM work before the wait; every VRAM write happens after it. Music
ticks from the line interrupt (`PSGFrame()` in the handler) so it survives slow
frames. See `assets/template/src/main.c` and `references/game-structure.md`.

## Hard constraints cheat-sheet

- **RAM is 8 KiB** at `0xC000` (`--data-loc 0xC000`). No real heap — use static
  fixed-size pools, keep large/immutable data in ROM.
- **VRAM is 16 KiB**: 448 tile slots + tilemap + SAT. Plan the tile budget up
  front. Reach VRAM only via SMSlib VDP calls, only in VBlank.
- **Colour is 2 bits/channel** (`RGB(r,g,b)`, 0–3), two 16-entry palettes (BG +
  sprite); sprite entry 0 is transparent.
- **Sprites: ≤64 total, 8 per scanline.** Wide rows flicker — stagger or use
  8×16 tall mode.
- **No float, slow divide.** Use 8.8 fixed-point and precomputed LUTs.
- **Code lives in the fixed first 32 KiB**; page data banks into `0x8000–0xBFFF`
  with `SMS_mapROMBank(n)`.
- **Embed the ROM header once** at file scope: `SMS_EMBED_SEGA_ROM_HEADER(9999,0)`
  (+ optional `SMS_EMBED_SDSC_HEADER_AUTO_DATE(...)`), else `ihx2sms` can't fix a
  checksum and real hardware/emulators may reject it.

## Version consistency (the #1 build breaker)

`SMSlib.h` and `SMSlib.lib` **must** come from the same devkitSMS version. Across
releases, `SMS_addSprite` changed from a function to a macro over
`SMS_addSprite_f` and the calling convention moved to `__sdcccall(1)` (needs SDCC
≥ 4.2). Symptoms and fixes:

- `?ASlink-Warning-Undefined Global '_SMS_addSprite'` → mismatched header/lib.
  Use one consistent set (the bundle, or the project's own vendored pair).
- `error 98: conflict with previous declaration of 'putchar'` → old code vs SDCC
  4.2 `<stdio.h>`; drop the local prototype, use SMSlib's text renderer.

More in `references/toolchain-and-build.md`.

## Black-screen triage

When a ROM compiles but shows black, check in this order (see
`references/testing.md`, `references/game-structure.md`):

1. **Display left off** — no `SMS_displayOn()` after setup.
2. **Palette never loaded** — every pixel maps to a black entry. Load BG/sprite
   palettes before the first frame.
3. **Tiles/tilemap never uploaded** — nothing to show. Load with display off.
4. **VRAM written outside VBlank** — setup raced the beam; do bulk loads with the
   display off, per-frame writes after `SMS_waitForVBlank()`.
5. **Crash in setup** — a bad pointer/among the `UNSAFE_*` calls wedged `main`
   before the loop. Add a `smstest` `expectvdp display 1` right after setup.
6. **Missing/!bad ROM header** — checksum not fixed; re-check the embed macro.

Run `smstest game.sms tests/playtest.txt` (start from the smoke test in
`references/testing.md`) to see exactly which frame goes wrong and to grab `.ppm`
screenshots.

## Bundled resources

- `scripts/setup_toolchain.sh` — one-shot toolchain install + harness build + smoke test.
- `assets/devkitSMS/` — pinned, consistent SMSlib/PSGlib/crt0/headers + tool sources (`VERSION.txt` explains the version rule).
- `assets/template/` — `Makefile`, `Makefile.banked`, and a commented `src/main.c` game-loop skeleton.
- `assets/smstest/` — the headless SMS test emulator (`smstest.c` + superzazu's MIT Z80 core) and its build, with flat and call-graph profilers (`prof_report.py`, `prof2.py`), PAUSE/NMI, PSG logging, state dumps, cartridge RAM, garbage power-on RAM, and hardware-realism checks (`expectpace` VRAM pacing, `spmin` stack depth). `ATTRIBUTION.md` credits sources.
- `assets/smsvideo/` — reusable pre-rendered-video toolkit: `smsvideo.py` (delta/snapshot tile-stream encoder + verifier), `smsvideo.{c,h}` (runtime player), `mkrom.py` (bank splicer), banked `Makefile`, `example.c`. See `references/prerendered-video.md`.
- `assets/playtest.example.txt` — a real, worked playtest script.
- `references/toolchain-and-build.md` — install, pipeline, flags, memory model, version gotchas, GG/SG notes.
- `references/smslib-api.md` — task-oriented SMSlib + PSGlib API map.
- `references/game-structure.md` — frame loop, fixed-point, actor pattern, collision, HUD, state machine.
- `references/rpg-adventure-roguelike.md` — scrolling OR flip-screen tilemap worlds, menus & dialogue boxes, turn-based/roguelike loops (procgen, FOV) AND real-time action combat (i-frames, knockback), party HUD/minimap, SRAM battery save (+ how to test it). For RPGs/adventures/roguelikes.
- `references/grid-and-maze-games.md` — tile-grid/maze games: lane movement, turn-queuing, tunnel wrap, ghost-style target-cell AI, per-actor speed, procedural sprite/tile generation, maze flood-fill validation, clearing the nametable. Also **metatiles** (16×16 blocks) for large maps.
- `references/faux-rotation-and-pseudo-3d.md` — faking effects the VDP can't do (rotation, sprite scaling, pseudo-3D) by projecting sprites through precomputed tables; discrete-size metasprites; keeping the background cheap.
- `references/game-gear.md` — the Game Gear: the 160×144 LCD window at (48,24) inside the 256×192 frame, 12-bit two-byte CRAM, the Start button (no PAUSE NMI), half-size art vs cropping, single-layer tricks (sprite HUD, colour-0 gradients), testing `.gg` ROMs in smstest.
- `references/interrupts-raster-and-sampled-audio.md` — the line interrupt: raster effects (per-row scroll), digitized speech/samples on the PSG, interrupt races (VDP address latch, bank switches, library routines re-enabling IRQs), latching input in the frame interrupt.
- `references/interpreter-ports.md` — porting script/bytecode-VM engines (Flashback, Another World, SCUMM-likes): run logic VMs live and pre-render renderer VMs, build an oracle from the original engine, stage opcodes by measured first use, in-ROM tick-for-tick self-checks, fail-soft unported opcodes, RAM overlays over ROM tables, bounded walks, bank layout by what you can lose.
- `references/prerendered-video.md` — effects the Z80 can't compute live (pseudo-3D road, rotations): pre-render offline and stream from ROM as simulation-indexed tile deltas + snapshots, inside the VBlank budget. Keeps it a game (the sim seeks the video), not a movie.
- `references/assets.md` — images→tiles, music→PSG, maps, compression, banking.
- `references/testing.md` — the harness, the playtest DSL, making variables visible, definition of done.
- `references/porting.md` — the port method and the original→SMS systems mapping.
- `references/examples.md` — catalog of Haroldo-OK's games and what to copy from each.
- `references/community-examples.md` — field-tested techniques from shipped devkitSMS games: Game Gear target, built-in text renderer, hardware sprite-collision (and its Power Base Converter caveat), SRAM saves, PRNG-from-register-R, bank-switching data, input edge patterns.
