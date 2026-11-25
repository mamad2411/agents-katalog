# CLAUDE.md — Woodland Preparation Quest (Source of Truth)

## Purpose
This repository contains a Mario-style, level-based, 8-bit inspired web game (Phaser 3 + Vite + TypeScript).
It must run on mobile via QR code and feel like a game (not a website).

If you are Claude (or any AI) continuing work: READ THIS FILE FIRST.

---

## High-Level Pitch
**Chris must finish domestic “quests” across woodland levels before Babitee arrives — not to save her, but to be ready to pick her up.**
Six Jollibabees follow him and comment like a chaotic, adorable family chorus.
Temptations include “forest pigs” (forest-girl silhouettes), doom scroll, and **WHALE COIN** gamble.

---

## Non-Negotiables
1. **Level progression like Mario:** World map → Level 1 → ... → Level 6 → Final Pickup → Ending.
2. **Deterministic state machine:** exactly one scene/state active at a time.
3. **Mobile-first:** large tap targets, on-screen controls (or tap-based interactions), no hover dependencies.
4. **Stable publish:** one entry point, one world map, no duplicate scenes.
5. **Game feel:** SFX, transitions, HUD, particles (light).
6. **No “save the princess” trope:** Babitee is not being saved. Chris prepares and picks her up.

---

## Core Mechanics (Must Match)
### Global Variables (clamped each update)
- Preparation: 0..100
- Integrity: 0..100 (starts 50)
- Energy: 0..100 (starts 100)
- Hearts: 0..3 (starts 3)
- Diamonds: min 0 (starts 0)
- WhaleCoinWins, WhaleCoinLosses: integers
- HasRing: boolean (starts false)

### Failure
- If Hearts == 0 → Game Over
- If level timer hits 0 → Game Over

### Whale Coin Popup (max once per level; always triggers in Level 3)
Text: “WHALE COIN 🐋 To the moon? Trust the forest bro.”
- Ignore: Diamonds +2, Integrity +1
- Invest (50/50):
  - Win: Diamonds +15, Preparation +5, Integrity -1, WhaleCoinWins +1
  - Lose: Diamonds -8 (min 0), Preparation -3, Integrity -5, Hearts -1, LevelTimer -8s, WhaleCoinLosses +1

### Temptation Incoming Call (replaces Forest Pigs)
The “forest pigs / forest girls” temptation is now an Incoming Call modal.

- Modal shows: Incoming Call: “Forest Girl 💋” (temptation)
- Buttons: BLOCK / ACCEPT
- Countdown: 1.5 seconds visible
- If player taps BLOCK within time: success, no penalty
- If player taps ACCEPT: **instant GAME OVER**
- If timeout (no input): auto-ACCEPT → **instant GAME OVER**
- Modal must block underlying input while open.
- Jollibabee speech bubbles must PAUSE during this modal.
- Trigger counts per level remain the same as the old pig hazard:
  L1: 2 calls
  L3: 2 calls
  L4: 1 call
  L6: 2 calls


### Doom Scroll
- “Scroll more”: Integrity -5, LevelTimer -8s
- “Close”: Integrity +1

### Darmesh Call (Level 4 only)
Jollibabees must say: “Hi Darmesh!”
- Take call: Energy -10, Integrity +3, Preparation +3
- Ignore call: Integrity -5

### Market (appears after Level 2 and Level 5 only)
- Coffee (5 Diamonds): Energy +10, Integrity -1
- Gadget (20 Diamonds): Integrity -5
- Flowers (10 Diamonds): Preparation +5, Integrity +5
- Ring (25 Diamonds): Preparation +10, Integrity +10, HasRing = true

### Sacred Sleep (required before Level 6)
Hold-to-sleep 3.5 seconds:
- Energy = 100, Preparation +10, Integrity +5

### Levels (Objectives + base rewards)
- L1 Dish Cavern: clean 5 dishes. Timer 60s. Reward: Prep +5, Energy -5, Diamonds +1. + 2 pig avoid prompts.
- L2 Trash Run Trail: drag 3 trash. Timer 55s. Reward: Prep +3, Diamonds +1. + doom scroll once.
  After L2: Market available.
- L3 Doomscroll Swamp: close 4 popups fast. Timer 65s. Whale coin always triggers. + 2 pig avoid prompts.
  Reward: Prep +4, Energy -5 plus choice effects.
- L4 Darmesh’s Clearing: complete 3 “work checkboxes in order”. Timer 70s. Darmesh call mid-level. + 1 pig avoid prompt.
  Reward: Prep +3 plus call choice effects.
- L5 Garden + Groom: water 4 plants + groom (3 taps). Timer 80s.
  Reward: Prep +8 total, Integrity +2, Energy -5. + doom scroll once.
  After L5: Market available.
- L6 Laundry Woods: locked until Sleep done.
  Objective: fold laundry in correct A→B→C order. Timer 75s. + 2 pig avoid prompts.
  Reward: Prep +6, Integrity +3 (correct fold), Energy -5.
  Optional “Fold neatly” bonus: Integrity +3 but Timer -5s.

### Final Pickup Gate
Unlocked only after Levels 1–6 complete.
Readiness:
- Preparation >= 90
- Energy >= 50
- Diamonds >= 10
- Hearts >= 1

If not ready: show “Not ready to pick up Babitee yet.” and return to World Map.

### Endings
- Integrity < 40: “The forest needs steadier roots.”
- Integrity 40–70: “You’re growing.”
- Integrity > 70 AND HasRing: “You didn’t just prepare. You chose us.”

Show final stats and Whale wins/losses.

---

## Jollibabees (6 follower UI sprites + chatter)
Always visible on HUD/scene (not during popups/market/ending).
Personalities: one small flying, one big, one pusher, one bullied, one dreamer, one leader.

Key lines include:
- “Dadibee, focus”
- “It’s not that haard”
- “IYKYK” / “yeah, iykyk”
- “That’s right” / “yeah, that’s right”
- “I want to be like you, Dadibee, a (carpenter/dentist/doctor/gamer)”
- “I want to go to the BART” / “Yeah, it’s very popular here in the Bay area”
- “Where is Mamibee?”
- “Oooh what’s that?” / “Ohh it’s a flower!”
- “Dadibee we want honey”
- “You dont look like us” (pusher pushes bullied)
- Bullied bubble: “are you okay?”
- New: “I can’t see! you’re so big” → Big replies: “No, I’m just plump”
- Big random: “Dadibee, I’m growing”
- BART bug: “Oh a bug *sprays*”
- Darmesh call: everyone says “Hi Darmesh!”

Speech must PAUSE during: Whale popup, Market, Ending.

---

## Jollibabees Unlock Progression (Missing Babies)
Jollibabees start missing. You “find” one baby after each level.

- Start of game: 0 followers
- After completing Level 1: +1 follower
- After completing Level 2: +1 follower
- After completing Level 3: +1 follower
- After completing Level 4: +1 follower
- After completing Level 5: +1 follower
- After completing Level 6: +1 follower (total 6)

Only the found jollibabees appear trailing behind Chris.
Speech bubbles can only come from currently found jollibabees.
Personality behaviors only activate once both characters exist:
- Pusher can only push once Bullied exists.
- Big reply (“No, I'm just plump”) only after Big is found.
- Fly only after Fly is found.

Recommended unlock order (for consistency):
L1: Leader
L2: Dreamer (BART lines)
L3: Bullied
L4: Pusher (activates pushing Bullied)
L5: Big
L6: Fly
---

## Jollibabees Unlock Progression (Missing Babies)
Jollibabees start missing. You “find” one baby after each level.

- Start of game: 0 followers
- After completing Level 1: +1 follower
- After completing Level 2: +1 follower
- After completing Level 3: +1 follower
- After completing Level 4: +1 follower
- After completing Level 5: +1 follower
- After completing Level 6: +1 follower (total 6)

Only the found jollibabees appear trailing behind Chris.
Speech bubbles can only come from currently found jollibabees.
Personality behaviors only activate once both characters exist:
- Pusher can only push once Bullied exists.
- Big reply (“No, I'm just plump”) only after Big is found.
- Fly only after Fly is found.

Recommended unlock order (for consistency):
L1: Leader
L2: Dreamer (BART lines)
L3: Bullied
L4: Pusher (activates pushing Bullied)
L5: Big
L6: Fly
---

## UX / Visual Direction (Woodland)
Palette:
- Forest: #1F3B2C #2F4F3E #3F6B4F
- Wood: #5C3A21 #7A4E2D
- Highlights: #E8B45E #F4C76A
- Mist: #6D8C8A
- Ivory text: #F5F2EA
- Champagne glow: #E6C98B

UI:
- Carved wood HUD panels, vine bars, parchment speech bubbles.
- Red characters pop against forest.

---

## Rules for Future Changes
- Do not introduce new scenes unless they map to the stated flow.
- Add mechanics via shared systems (state machine, event bus), not one-off hacks.
- Keep code testable: pure reducers for stat changes, deterministic RNG wrapper.
- Mobile compatibility is mandatory.

---

## Current Priorities (If resuming mid-work)
1) Implement World Map + Level progression.
2) Implement Level templates + mini-interactions per level.
3) Implement Whale coin + Market + Sleep gating.
4) Implement Ending gate and Game Over reset.
5) Apply UI skin + audio polish.
