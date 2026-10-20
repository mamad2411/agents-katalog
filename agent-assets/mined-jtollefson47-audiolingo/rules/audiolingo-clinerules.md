# Audiolingo Workspace Rules

## Project Overview
Audiolingo is a Duolingo-meets-Sound-Gym audio engineering and music education app.
It features learning modules and games around:
- Audio equipment: compressors, EQs, preamps, mixers, effects
- Instruments: keyboards, percussion, and more
- Audio ear training, frequency recognition, gain staging, dynamics exercises

## Tech Stack
- Frontend: Next.js (App Router), React 18+, TypeScript
- Backend: Node.js (API routes via Next.js or separate Express/Fastify service)
- Audio: Web Audio API, Tone.js (preferred), or Howler.js for playback
- Styling: Tailwind CSS
- State: Zustand (per-game scoped stores)
- Testing: Vitest + React Testing Library
- Target: Web-first, designed for clean extraction to React Native / Expo for iOS

## Architecture Conventions
- /app — Next.js App Router pages and layouts
- /components — Reusable UI components (atomic design preferred)
- /modules — Self-contained learning modules (each module owns its logic, UI, and tests)
- /games — Game logic separated from UI; each game is a standalone module
- /lib — Shared utilities, audio helpers, constants
- /hooks — Custom React hooks
- /types — Global TypeScript type definitions

## Game Plugin System
- Every game is a self-contained plugin in /games/<name>/ exporting a GamePlugin object.
- Required files per game: config.ts, scoring.ts, use<Name>Store.ts, <Name>Game.tsx, index.ts.
- Every game renders inside the shared GameShell component; games must never render their own page-level chrome.
- Games communicate with the host via the typed gameEventBus (start, score, progress, complete, pause, resume) — never by importing host state.
- State for a game instance lives in a per-instance Zustand store created by the plugin's createStore factory. No module-level mutable state.
- Register new games in lib/gameRegistry.ts via registerGame().
- Game component receives GameProps: { difficulty, emit, onReset }.

## Audio Rules
- All audio processing must use the Web Audio API or Tone.js — no Flash or deprecated APIs.
- Audio nodes must be properly connected and disconnected to prevent memory leaks.
- Use AudioContext.suspend()/resume() to save battery on mobile.
- Never autoplay audio without user gesture (browser policy compliance).
- Latency-sensitive interactions (games) should use AudioWorklet where possible.

## Game & Module Design
- Each game/module must have: a config object, a scoring function, and an accessibility fallback.
- Difficulty levels: beginner, intermediate, advanced — always support all three.
- Progress and scores must be persisted (localStorage for web, AsyncStorage for native).
- Games must be completable with keyboard-only navigation.

## Cross-Platform (iOS Readiness)
- Avoid browser-only APIs without a React Native shim or abstraction layer.
- Abstract platform-specific code behind /lib/platform.ts.
- Use rem/em units and avoid fixed pixel dimensions for layout.

## Testing
- Unit test all scoring logic, audio helpers, and game state machines.
- Snapshot test UI components only when layout stability is critical.
- Do not mock the Web Audio API unless testing UI-only behavior.