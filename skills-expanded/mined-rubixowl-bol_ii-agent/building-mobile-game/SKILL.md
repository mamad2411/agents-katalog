---
name: building-mobile-game
description: Build mobile games and game-like interactive experiences in React Native and Expo. Use when Codex is creating or refactoring arcade, puzzle, casual, action, physics-based, or animation-heavy gameplay, including Expo game setup with the with-reanimated template, sprite-sheet generation and extraction, frame-based animation, touch controls, simple collision and physics loops, score and game-state systems, and cross-platform verification on web plus iOS and Android.
---

# Mobile Game Workflow

## References

- `./references/setup-and-loop.md` -- Expo bootstrap, worklets setup, engine selection, game loop order, physics rules, packages, and performance checks
- `./references/assets-and-animation.md` -- sprite-sheet prompt templates, extraction workflow, naming, animation state mapping, and validation checklist
- `./scripts/extract_sprites.py` -- connected-component sprite extractor with background removal and optional frame normalization
- `./scripts/normalize_animation_frames.py` -- shared-scale frame normalizer with optional anchor frame locking for existing characters

## Mandatory Reading Order

For any new mobile game task, read both reference files before planning implementation or calling project tools:

1. Read `./references/setup-and-loop.md` first.
2. Read `./references/assets-and-animation.md` second.
3. Only after both references have been read should you choose libraries, plan gameplay, generate assets, or start coding.

Do not stop after reading only `setup-and-loop.md`. The asset reference is also mandatory for almost every real game because it covers sprite-sheet prompting, extraction, and normalization.

The only acceptable exception is a deliberately art-free prototype that uses simple geometric placeholder shapes and no image generation. When in doubt, read both references anyway.

## Quick Start

1. Read `./references/setup-and-loop.md`, then read `./references/assets-and-animation.md`.
2. Start from `mobile_app_init(..., example="with-reanimated", with_tailwind=False)` for animation-heavy or gesture-heavy game projects.
3. Install `react-native-worklets@0.5.1` and put `"react-native-worklets/plugin"` last in `babel.config.js`. Never add `"react-native-reanimated/plugin"`.
4. Choose the lightest rendering stack that can support the mechanic:
   - `react-native-game-engine` for most 2D arcade or puzzle loops
   - `@shopify/react-native-skia` for custom 2D drawing and effects
   - `expo-gl` plus `three` for 3D or GL scenes
   - `matter-js` only when the game truly needs richer physics
5. Build gameplay in this order: input, movement, collisions, scoring or lives, pause or restart, then polish.
6. Ask `generate_image` for one whole animation strip at once, not one frame at a time, so character identity and proportions stay consistent.
7. Split raw strips with `./scripts/extract_sprites.py`, then standardize them with `./scripts/normalize_animation_frames.py` when the game needs fixed frame sizes or an exact existing idle anchor.
8. Verify the game on Expo web and on mobile before calling the feature done.

## Core Rules

- Keep physics simple first. Use manual velocity, gravity, and AABB collisions before reaching for a full physics engine.
- Build one mechanic at a time and re-test immediately after each layer.
- Keep gameplay rendering separate from overlays such as score, pause, settings, and game-over UI.
- Use only cross-platform APIs for rendering, animation, input, storage, audio, and haptics.
- Do not pull game art from random URLs. Generate assets locally and keep them under `assets/images/`.
- Use `generate_image` for sprite sheets and explicitly ask for multiple states, transparent background, and large spacing between poses or items. Do not accept a single hero illustration when the game needs animation frames.
- Ask for a full strip with explicit slot count, slot size, and canvas layout. Do not ask the model to patch one tiny frame at a time unless you are prepared for character drift.
- Normalize with one global scale for the whole strip. Do not rescale each frame independently or tall poses will make the character shrink.
- Normalize animation frame sizes for each entity so characters do not jitter between states.

## Decision Guide

- Need route structure, navigation polish, or general Expo UI? Load `building-ui` as well.
- Need async APIs, leaderboards, or cloud save? Load `data-fetching` for the network layer.
- Need to port browser game code or use a web-only library inside Expo? Load `use-dom`.

## Delivery Checklist

- The project boots from the reanimated example and uses `react-native-worklets/plugin` correctly.
- The core loop is playable end to end with real input, collision, scoring, and failure or success states.
- Sprite sheets were generated with `generate_image`, split cleanly, backgrounds are transparent, and per-entity frames share one canvas size with one global scale.
- If the animation extends an existing shipped character, frame 01 can be locked to the exact in-game idle anchor instead of a regenerated approximation.
- Audio, haptics, pause or resume, and persistence are implemented when the design calls for them.
- Web preview and at least one mobile target have been checked for controls, frame pacing, and collision bugs.
