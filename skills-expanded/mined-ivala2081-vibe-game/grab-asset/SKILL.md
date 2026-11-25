---
name: grab-asset
description: "Auto-asset pipeline for Unity. Searches CC0 / free sources (Kenney, OpenGameArt, Itch, freesound) for art and SFX matching the project's palette and mood, then imports into Unity with proper setup. Also generates procedural placeholders (jsfxr SFX params, shader textures) when nothing fits. Trigger when the user needs assets and doesn't want to draw/compose them."
disable-model-invocation: false
---

# grab-asset

> **"I have no assets" is no longer an excuse.**

## When to invoke

- User says: "I need a character sprite" / "find me SFX" / "grab some assets"
- `/prototype` placeholders need replacement
- Stuck waiting on art (Tyroller M4)

## Hard rules

1. **CC0 / public domain / open license only.** Never recommend pirated, scraped, or unclear-license assets.
2. **Source preference order:**
   1. [Kenney.nl](https://kenney.nl) — CC0, huge library, consistent style
   2. [OpenGameArt.org](https://opengameart.org) — filter by CC0
   3. [Itch.io free asset packs](https://itch.io/game-assets/free) — check license per pack
   4. [Freesound.org](https://freesound.org) — CC0 / CC-BY for SFX (CC-BY requires attribution)
   5. Procedural fallback (see below) if nothing fits
3. **Palette match.** Read the project's existing palette (URP color profile, dominant scene colors). Recommend assets in the same hue range or that can be re-tinted.
4. **Style match.** Don't pair pixel art with smooth-shaded 3D. Pick one style early, stick with it.
5. **Document attribution.** Every asset gets a line in `Assets/_Project/CREDITS.md`.

## What this skill does

### 1. Asset discovery
Given a description (e.g., "platformer character" / "explosion SFX" / "spooky ambient track"):

- Search Kenney first (most likely hit, CC0 guaranteed)
- If miss, suggest OpenGameArt searches
- If miss, fall back to procedural

### 2. Style/palette analysis
- Read the project's existing assets (if any) — palette from sprite/texture analysis
- Read mood from Vibe Brief — "cozy warm" vs. "neon cyberpunk" vs. "muted noir"
- Filter recommendations by style match

### 3. Import setup
For each grabbed asset:
- Download to `Assets/_Project/Art/Sourced/{pack-name}/` (or `Audio/Sourced/`)
- Configure import settings:
  - **Sprites:** Pixels-per-unit set per pack convention. Filter Mode Point for pixel art, Bilinear for HD.
  - **Textures:** sRGB on for color textures. Compression: Crunched for builds.
  - **Audio:** Compressed in memory for music, Decompress on Load for short SFX.
- Add to `CREDITS.md` with attribution line and source URL.

### 4. Procedural fallback
If no asset fits, generate placeholder:

**SFX via jsfxr:**
Output the jsfxr URL with pre-filled params:
```
https://sfxr.me/#5lHsRJ7vWE5MNXvK8sxgYC5qjY8YA8mU...
```
The user clicks, hears it, downloads .wav, drops in Unity.

**Textures via shaders:**
Provide a simple unlit shader (e.g., gradient + noise) the user can apply to a Quad as placeholder background.

**Music via free packs:**
Direct user to specific Kenney music packs or recommend free Bandcamp loops with CC-BY.

## Procedure

1. **Parse the request** — what kind of asset, what mood/style.
2. **Read the brief** — match style to mood.
3. **Suggest 2-3 specific sources** with direct links. Not "search OpenGameArt" — give the actual pack name and URL.
4. **Offer to download + import** if the user picks one. (Note: actual downloading depends on having `curl` / WebFetch / browser open.)
5. **Set up the asset** — write the meta files, update CREDITS.md.
6. **Confirm placement and next step.**

## Example interaction

```
User: I need a player character sprite for a top-down shooter

Skill: Reading brief... mood is "frenetic, neon, ridiculous". Top picks:

1. Kenney Top-Down Tanks (CC0) — neon-friendly, top-down
   https://kenney.nl/assets/top-down-tanks
   Style: clean vector, easy palette swap
   Pick this if: you want stylized + readable

2. Kenney Toon Characters (CC0)
   https://kenney.nl/assets/toon-characters-1
   Pick this if: humanoid protagonist

3. OpenGameArt — Cyberpunk Top-Down character pack (CC0)
   https://opengameart.org/...
   Pick this if: you want pre-styled neon

Which one — or want me to grab #1 and set it up?

User: #2

Skill: ✓ Downloading Kenney Toon Characters to Assets/_Project/Art/Sourced/kenney-toon-characters/
       ✓ Import settings: PPU 64, Filter Mode Bilinear
       ✓ CREDITS.md updated:
         - Toon Characters by Kenney (kenney.nl) — CC0
       ✓ Drop a sprite onto the Player prefab and you're set.
```

## Anti-patterns

- ❌ Recommend an asset without license clarity
- ❌ Skip the CREDITS.md update
- ❌ Pixel art + HD smooth-shaded in the same scene (style mismatch)
- ❌ Ignore the brief's mood — recommending bright cartoon for a noir game
- ❌ Tell user to "just search" — always give specific links

## Cross-references

- Reads: [[vibe-brief]] (mood/style), existing project assets (palette)
- Replaces: `/prototype` placeholders, post-`/juice` polish gaps
- Drives: better `/feel-check` scores on M3 Context, M5 Metaphor
