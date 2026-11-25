---
name: design-thumbnail-keyart
description: Make a game thumbnail or key art that shows, in under a second, what the game is, what you do in it and what you are going for, from the game's concept and theme, rendered at 1920 × 1080, benched for phone width, contrast and the platform's overlays, and read back by a fresh vision critic. Use WHENEVER the user wants a game thumbnail, Roblox thumbnail, experience thumbnail, key art, store tile, update thumbnail or cover for a game ("make a thumbnail for my Roblox game", "thumbnail for the dungeon update", "key art for this game", "ทำ thumbnail เกม", "ทำปกเกม Roblox", "ภาพปกอัปเดตเกม"), wants thumbnail variants to A/B test or for Roblox's thumbnail personalization, wants a thumbnail reviewed ("does this thumbnail read", "why is my CTR low"), or wants the look of a reference app or site recovered before designing. Not for brand banners with four steps (banner-design) or video.
---

# Thumbnail key art

A thumbnail is one moment from the game, chosen so a player scrolling past can say three things
in under a second: **what the game is**, **what you do in it**, and **what you are going for**.
The scene says those three; the type only names the game and the update.

banner-design renders it: the brief is a `<game>.keyart.toon`, banner.py's `keyart` layout lays
the title, ribbon and callouts over the scene, and bench.py measures it. Platform rules and the
sources: [references/roblox-thumbnails.md](references/roblox-thumbnails.md). Recovering a reference
app's look: [references/recon.md](references/recon.md). The game's own art, characters and fonts
win over anything here, the same order of authority as [`../core/SKILL.md`](../core/SKILL.md).

## Workflow

0. **Render path first.** Probe the image tool before designing: one cheap test call. A quota or
   auth error (Gemini's `429 … free_tier … limit: 0`) means no AI art: don't retry, take the
   vector path and say so in the hand-over. Text-only or vision-only models (an OCR or chat
   gateway) can't paint; use them as the critic in step 6. Whichever path made the art, name it:
   a vector comp is not an AI render.
1. **Read the game.** From the brief (`design/game-brief.md` if the game-dev skill made one) or
   the person, write three lines: `is` (genre + world, one sentence), `loop` (what you do, verbs),
   `goal` (what you are trying to get or reach). No brief yet: run game-dev's `design-lens`
   first. For an update thumbnail the goal is the update's new thing.
2. **Map beats to anchors.** Every beat gets one thing you can point at in the frame; no anchor, no
   element. Five at most: a thumbnail reads in under a second and a sixth competes. Write the
   table into the brief before drawing.

   | Beat | Anchor (the bench image) |
   |---|---|
   | world | snowy peaks behind everything |
   | loop: fight | the hero mid-stride, sword forward |
   | progression | a level bar over the first enemy |
   | goal | the key glowing in the arch, with its price |
   | the update | the dungeon gate at the end of the bridge |

3. **Art, with no text in it.** AI path: the brief's `prompt` (subject, pose, camera, light,
   palette, rule-of-thirds placement, "empty sky across the top centre for a title") plus a
   `negative` that bans text, logos and watermarks. Text drawn by a model misspells and can't be
   benched. Pass a reference image and, when regenerating, the previous render so the scene stays
   coherent. Vector path: a `build_*.py` that writes the scene SVG (the example's
   [build_art.py](examples/craghold/build_art.py)). Either way the art is regenerated, never
   hand-edited.
4. **Compose**: `uv run ../banner-design/scripts/banner.py <game>.keyart.toon` writes one SVG per
   variant per size (`keyart-<variant>-<game>-<w>x<h>.svg`).
5. **Bench**: `uv run ../banner-design/scripts/bench.py <svg> --bottom 120 --max-kb 3000` (Roblox:
   no text in the bottom band, where the player count sits; PNG under 3 MB). It writes the 1×, 2×,
   400 px and crop PNGs.
6. **Critic**: `uv run scripts/critic.py <game>.keyart.toon <…-400.png>`. A vision model that never
   saw the brief says what the game is, what you do, what the goal is, every word it reads and where
   its eye lands; a second call scores that read against the brief. A run fails on a string not read
   back, a beat scored 0, or a total under 4 of 6. Focus is printed, not scored: on a published
   thumbnail the model named the logo first every time, so "the title" says nothing. One sample is noise
   (the same image flipped between pass and fail), so it runs three times (`--runs`) and passes on a
   majority. Endpoint, model and key: the script's `--help`. With no key it is NOT ASSESSED, never a
   pass.
7. **Look**, one class of flaw per pass, in this order: composition → legibility →
   lighting/contrast → detail. Three passes; a flaw that survives three needs a different
   approach, not new numbers. Then the QA gate below.
8. **Variants.** Roblox personalises between 2-5 active thumbnails. Make each one a different
   moment aimed at a different player motivation (mastery, exploration, collection, social), not
   a colour swap. A variant row can carry its own art, ribbon, `goal` and `loop`, and a callout
   marked `only` stays in its variant. Keep the current best thumbnail in every new test: since
   July 2025 Roblox doesn't reset the traffic of a test that includes its winner.

## The brief (`<game>.keyart.toon`)

```
id: craghold
size[2]: 1920,1080
sizes[2]: 1920x1080,1280x720
is: "A blocky fantasy adventure on a snow mountain"
loop: "Fight monsters on the way up, level up, earn gold"
goal: "Buy the dungeon key and open the gate"
title[2]: CRAGHOLD,QUEST
kicker: DUNGEON UPDATE
title_at: top-left
title_max: 76
art: art-dungeon.svg
style: dark
colors[2]{token,value}:
  fg,#5BB8FF
  accent,#FFB23F
anchors[2]{beat,anchor,where}:
  goal,"gold key burning in the arch + its price",right third
  progression,"LVL bar over the first enemy",left third
callouts[2]{kind,text,sub,x,y,fill,only,tx,ty}:
  badge,KEY,"12,500 GOLD",0.80,0.21,,dungeon,0.775,0.47
  bar,LVL 5,,0.60,0.36,0.35,dungeon,0.655,0.45
prompt: "…scene only, no text…"
negative: "text, letters, numbers, logo, watermark, …"
variants[2]{id,motivation,art,kicker,goal,loop}:
  dungeon,mastery and reward,art-dungeon.svg,DUNGEON UPDATE,,
  summit,exploration,art-summit.svg,NEW SUMMIT,"Climb to the summit flag","Climb the path to new peaks"
```

- `title`: one or two lines, fitted from 100 px (or `title_max`) down to 56 px on the 1280 grid (it
  refuses to render a title that doesn't fit). `title_at: top-left` frees the centre for the scene. Line 1 takes `fg`, line 2 `accent`; `panel` is the outline,
  the stepped side and the callout plates; `cta` / `on_cta` the ribbon; `bar` the level bar.
  `colors` override a preset (`style`), so a palette needs only the tokens it changes.
- `callouts`: `badge` (a label and an optional big `sub`) or `bar` (a label and a `fill` from 0 to 1),
  centred at `x`, `y` as fractions of the frame. `tx`, `ty` draw a red arrow from the plate to its prop
  (the level bar to its enemy, the price to the key): a plate floating free of its prop reads as UI.
- `fonts[n]{role,font}` maps text roles to `family-weight` for a Thai title (`title,kanit-700`).
- `anchors`, `prompt` and `negative` don't render. They travel with the brief so anyone can make
  the image again and see why each element is there.

## QA gate

- [ ] The critic passes on a majority of 3 runs: every string read back, every beat ≥ 1, total
      ≥ 4 of 6.
- [ ] The bench passes: core text inside the safe zone, contrast ≥ 4.5:1 (≥ 3:1 large bold),
      nothing in the bottom band, the PNG under the limit.
- [ ] The title reads at 400 px wide (the `-400.png`) and in grayscale.
- [ ] One focal point, and it is the goal or the hero: the brightest thing in the frame. Judge it
      by eye on the 400 px PNG; the critic's focus line names the logo on any thumbnail.
- [ ] Vector style, built from code. A painted, AI-looking render is not the target; the loop
      reading in one frame is.
- [ ] Every anchor is in the frame and you can find it within two seconds; nothing in the frame
      lacks an anchor.
- [ ] Text is only the title, the ribbon and the callouts; about three words besides the title.
      Callout text is at least 42 px at 1920 (28 on the 1280 grid, the `keyart` default).
- [ ] The hero has a face that reacts (eyes, brows, mouth), and the loop is shown, not written:
      the hit, the coins, the thing being climbed.
- [ ] At most two hue families plus one accent; the goal carries the accent.
- [ ] Honest: everything shown is in the game today. Family-friendly, your own assets, no other
      game's names or characters.

## Hard rules

- Recon is read-only: the public client and its bundle, nothing behind a login, no requests to
  someone else's backend, no spending anyone's credits to watch a paid endpoint.
- Say which path made the art (image model and which one, or vector).
- Keep the brief, the art script or prompt, and the render command: a thumbnail that can't be
  made again is a dead end.

## Worked example

[examples/craghold](examples/craghold/README.md): a mock blocky adventure. One brief, two variants
(the dungeon update for mastery, the summit for exploration), vector art because the image model
was out of quota, benched and passed by the critic.
