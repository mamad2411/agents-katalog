# Skate Cat

3D skateboarding cat rhythm game built with React Three Fiber.

## Stack
- React 19, Vite, Three.js
- @react-three/fiber + @react-three/drei for 3D
- Leva for dev tuning controls
- Custom toon shading pipeline (see `src/shaders/`)

## Commands
- `npm run dev` — start dev server
- `npx eslint src/` — lint (don't run server to validate changes)

## Architecture

### State Management
`src/store.js` uses mutable refs (`gameState`) instead of React state for 60fps frame loop performance. Components read/write `gameState.speed.current`, `gameState.score`, etc. directly. This is intentional — don't refactor to Zustand/context.

### Scene Flow
1. **Intro**: CRT TV room with cat model (`IntroScene`). Player presses start.
2. **Transition**: Circular reveal effect (`TransitionEffect` + `PostEffects`) blends intro → game.
3. **Game**: Cat skateboards, jumps logs, grinds rails to music beats. Scoring is timing-based.
4. **Game Over**: Score screen with restart option.

### Key Files
- `src/App.jsx` — Top-level orchestrator: state, callbacks, Canvas setup
- `src/components/SkateCat.jsx` — Cat character: model, animations, input, physics
- `src/components/Obstacles.jsx` — Obstacle spawning, collision, grind rails
- `src/store.js` — Mutable game state refs
- `src/rhythm.js` — Beat timing, scoring windows
- `src/audioTransport.js` — Web Audio API music playback

### Directory Layout
```
src/
  shaders/     — GLSL shader strings (toon, outline, log toon)
  hooks/       — Custom React hooks (cat animation, toon shader sync)
  lib/         — Pure logic modules (obstacle patterns, lane logic, track analysis, materials)
  components/  — React/R3F components
    intro/     — Intro scene (TV room + screen)
```

### Toon Shading Pipeline
All game-world meshes use custom `ShaderMaterial` with stepped NdotL lighting, rim highlights, and eye-blink UV masking. Shaders live in `src/shaders/`, material factories in `src/lib/toonMaterials.js`.

### Leva Controls
Dev tuning panels are everywhere — shader params, camera, post-processing, timing. `useControls` calls stay with the component that uses them. Don't centralize.

---

## Components (`src/components/`)

### Core
- **SkateCat.jsx** — Cat character: GLTF model loading, toon material setup. Animation logic lives in `src/hooks/useCatAnimation.js`.
- **Obstacles.jsx** — Beat-aligned obstacle spawning, grind rail geometry, collision, scoring. Pure logic in `src/lib/`.
- **CameraRig.jsx** — Camera positioning for intro/game/transition with FOV changes and screen shake.

### Scene Composition
- **GameWorld.jsx** — Assembles the game scene: Ground, Background, Sky, SkateCat, Obstacles, particles, effects.
- **DayNightController.jsx** — Animates lighting, fog, hemisphere colors through day/night cycle.
- **PostEffects.jsx** — Post-processing: bloom, brightness/contrast, hue/saturation, transition portal rendering.

### Visual Effects
- **KickflipSparks.jsx** — Instanced particle system for jump/land/grind effects.
- **DustTrail.jsx** — Continuous dust particles behind skateboard.
- **SpeedLines.jsx** — Shader-based speed line overlay.
- **AmbientParticles.jsx** — Floating firefly-like particles.
- **MeshTrail.jsx** — Skateboard ribbon trail geometry.
- **TransitionEffect.jsx** — Custom post-processing pass for circular reveal transition.

### Environment
- **Ground.jsx**, **Background.jsx**, **Sky.jsx**, **Grass.jsx**, **Wildflowers.jsx**, **Trees.jsx**, **Pebbles.jsx**

### UI
- **GameHud.jsx** — Score, beat dots, timing feedback.
- **GameOverScreen.jsx** — End game modal.
- **TimingDebugHud.jsx** / **ObstacleSpacingDebugHud.jsx** — Dev debug overlays.

### Intro (`intro/`)
- **IntroScene.jsx** — TV room layout with models and lighting.
- **TvScreen.jsx** — Canvas-based animated title screen with start button interaction.

## State Flow
Most components read/write `gameState` (from `src/store.js`) directly via refs:
- **SkateCat** writes: `jumping`, `catHeight`, `activeGrind`, `grindSpark`, `screenShake`, `speed`
- **Obstacles** writes: `score`, `obstacleTargets`, `obstacleDebug`, `speedBoostActive`, `speedLinesOn`
- **GameWorld/DayNightController** writes: `timeOfDay`, `nightContrast`
- **CameraRig** reads: `screenShake`
- **GameHud** reads: `score`, `streak`, `lastScoringEvent`

---

## Hooks (`src/hooks/`)

### useCatAnimation.js
Core animation state machine for the cat. States: idle, jumping, grinding, spinning, death. Overlays: powerslide, squash-and-stretch, board recoil. Also handles keyboard input.

### useToonShaderSync.js
Per-frame shader uniform sync and blink animation. Lerps intro↔gameplay values.

---

## Lib (`src/lib/`) — Pure Logic

- **obstaclePatterns.js** — Pattern libraries, weighted selection, difficulty curves.
- **obstacleLaneLogic.js** — Lane positions, grind geometry, collision windows.
- **trackAnalysis.js** — Audio analysis parsing for music-aligned obstacle scheduling.
- **toonMaterials.js** — Material factory functions.
- **postProcessing.js** — Post-processing constants and interpolation.

## Shaders (`src/shaders/`)

- **toonShader.js** — Cat toon shading with eye-blink UV masking.
- **outlineShader.js** — Black outline via normal extrusion on BackSide.
- **logToonShader.js** — Simplified toon shader for log obstacles.
