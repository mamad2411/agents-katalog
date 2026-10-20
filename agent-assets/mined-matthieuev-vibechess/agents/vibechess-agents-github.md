# Copilot Instructions for vibeChess

This document provides context and guidelines for AI assistants working on the vibeChess codebase.

## Project Overview
vibeChess is a local-first chess application built with React, Vite, TypeScript, and Electron. It features two chess engines:
- **Maia** (via Zerofish) for human-like play at various ELO levels (1100-1900)
- **Stockfish 17.1** for post-game analysis with multi-PV suggestions

The app runs both in-browser (Vite dev server) and as a desktop application (Electron).

## Tech Stack
- **Framework**: React 19.2 + Vite 7.2
- **Language**: TypeScript 5.9
- **Desktop**: Electron 39 with electron-builder
- **State Management**: React Hooks (`useState`, `useEffect`, `useCallback`, `useRef`, `useMemo`)
- **Chess Logic**: `chess.js` 1.4 (Game state, move validation, FEN handling)
- **Chess UI**: `react-chessboard` 5.8
- **Play Engine**: Zerofish 0.0.36 + Maia neural network weights (WASM)
- **Analysis Engine**: Stockfish 17.1 (WASM/JS) running in a Web Worker
- **Icons**: `lucide-react`
- **Styling**: CSS (Global `App.css` with CSS Grid layout)
- **Unit Testing**: Vitest
- **E2E Testing**: Playwright
- **Linting**: ESLint

## Project Structure

```
src/
├── App.tsx              # Main application component
├── App.css              # Global styles and layout
├── Settings.tsx         # Settings modal component
├── Settings.css         # Settings styles
├── chessHelpers.ts      # Pure functions for move history/analysis
├── main.tsx             # React entry point
├── chess/
│   ├── types.ts         # PlayerColor, ColorChoice, GameMode types
│   └── utils.ts         # Utility functions (clamp, uciToSan, findKingSquare, etc.)
├── components/
│   ├── Sidebar.tsx      # Game controls, mode selection, ELO slider
│   ├── InfoPanel.tsx    # Move history, analysis navigation
│   └── AnalysisArrowLayer.tsx  # SVG arrows for suggested moves
└── engine/
    ├── maiaEngine.ts    # Maia/Zerofish engine wrapper
    └── engineAssets.ts  # Engine asset download/management
electron/
└── main.js              # Electron main process (window, IPC, asset downloads)
e2e/
└── chessboard.spec.ts   # Playwright E2E tests
scripts/
├── download-engines.js  # Download engines for dev server
└── strip-engines.js     # Strip engines from build (Electron downloads on first run)
```

## Architecture & Key Components

### 1. Main Application (`src/App.tsx`)
- **Role**: Central controller managing game state, dual-engine communication, and UI rendering.
- **Layout**: 3-column CSS Grid layout:
  - **Sidebar**: Game mode selection (Local 1v1 / Vs Maia), ELO slider, match controls, takeback button
  - **Main Board**: The `Chessboard` component with analysis arrows overlay
  - **Info Panel**: Move history with clickable moves for analysis navigation
- **Game Modes**:
  - `vs-maia`: Play against Maia engine at selected ELO (1100-1900)
  - `local-1v1`: Two players on the same device
- **Engine Integration**:
  - **Maia**: Loaded via `getMaiaEngine()` from `maiaEngine.ts`, uses Zerofish WASM + neural network weights
  - **Stockfish**: Loaded as Web Worker for analysis mode, uses UCI protocol

### 2. Engine Layer (`src/engine/`)

#### `maiaEngine.ts`
- Wraps Zerofish with Maia neural network weights
- Supports ELO levels: 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900
- Key exports: `getMaiaEngine()`, `snapMaiaElo()`, `setMaiaAssetPaths()`, `MAIA_ELOS`
- Weights are lazy-loaded and cached per ELO level

#### `engineAssets.ts`
- Handles engine asset discovery and download (Electron only)
- Web mode uses assets from `public/engine/` and `public/maia/`
- Electron mode downloads to `~/.vibeChess/engine/` and `~/.vibeChess/maia/` on first run
- Provides download progress events for UI feedback

### 3. Components (`src/components/`)

#### `Sidebar.tsx`
- Game mode cards (Local 1v1 / Vs Maia)
- ELO slider (1100-1900, step 100)
- Color choice selector (White / Black / Random)
- Start/Stop game, Analysis mode, Takeback buttons
- Settings button

#### `InfoPanel.tsx`
- Scrollable move history with numbered move pairs
- Clickable moves for analysis navigation
- Analysis controls (prev/next position)

#### `AnalysisArrowLayer.tsx`
- SVG overlay for drawing suggestion arrows on the board
- Supports multiple arrows with opacity based on move ranking

### 4. Chess Utilities (`src/chess/`)

#### `types.ts`
- `PlayerColor`: `'white' | 'black'`
- `ColorChoice`: `PlayerColor | 'random'`
- `GameMode`: `'vs-maia' | 'local-1v1'`

#### `utils.ts`
- `clamp()`: Numeric clamping
- `uciToSan()`: Convert UCI move to SAN notation
- `buildGameOverText()`: Generate game-over messages
- `isPlayerVictory()`: Check if player won
- `findKingSquare()`: Locate king position

### 5. Helper Logic (`src/chessHelpers.ts`)
- `sanitizeVerboseHistory()`: Replays moves to ensure validity
- `buildAnalysisEntriesFromVerbose()`: Converts move history into analysis-friendly format with FENs

### 6. Settings (`src/Settings.tsx`)
- Modal with sidebar navigation
- **Board Customization**: Theme colors (Green, Brown, Blue, Gray), takeback limits
- **Chess Engine**: Status display, mid-game ELO change toggle

### 7. Electron Main Process (`electron/main.js`)
- Creates BrowserWindow loading the Vite build
- IPC handlers for engine asset management
- Downloads Stockfish, Zerofish, and Maia weights on first launch
- Serves local assets via custom protocol

## Coding Conventions & Patterns

### React & Hooks
- **Strict Mode**: App runs in React Strict Mode. Effects must be resilient to double-invocation.
- **Dependency Arrays**: Always include all dependencies in `useEffect` and `useCallback`.
- **Refs for Engines**: Use `useRef` for worker instances and engine objects to avoid re-initialization.
- **Memoization**: Use `useMemo` for expensive calculations (e.g., analysis entries from history).

### Chess Engines

#### Maia (Play Engine)
- Initialized via `getMaiaEngine(assets, elo, onStatus)` returning a `MaiaEngine` instance
- Call `engine.goFen(fen)` to get the best move
- ELO changes require reloading weights: `engine.setElo(newElo)`

#### Stockfish (Analysis Engine)
- UCI protocol via Web Worker `postMessage`
- Command flow: `uci` → `isready` → `setoption name MultiPV value N` → `position fen X` → `go movetime Y`
- Parse `info` lines for PV data, `bestmove` signals completion

### TypeScript
- **Strict Typing**: Avoid `any`. Use types from `chess.js` (`Move`, `Square`, `PieceSymbol`).
- **Custom Types**: Define in `src/chess/types.ts` or locally for component-specific types.
- **Null Safety**: Handle potential `null` from `chess.js` methods.

### Testing

#### Unit Tests (Vitest)
- Located alongside source files (e.g., `chessHelpers.test.ts`, `maiaEngine.test.ts`)
- Run with `npm run test`
- Cover edge cases, typical usage, and invalid inputs

#### E2E Tests (Playwright)
- Located in `e2e/chessboard.spec.ts`
- Uses `VITE_E2E=1` environment variable for deterministic behavior
- Tests: drag-and-drop, click-to-move, analysis mode, settings, takebacks
- Run with `npm run test:e2e` or `npm run test:e2e:ui`

### UI/UX
- **Loading States**: Use skeleton placeholders for async engine analysis
- **Analysis Arrows**: Draw on board to show suggested moves
- **Game Over Dialog**: Modal with result and New Game option
- **Desktop Layout**: Fixed 3-column grid optimized for 1024px+ screens

### Verification Workflow
After every modification, run:
```bash
npm run build      # TypeScript + Vite build
npm run lint       # ESLint
npm run test       # Vitest unit tests
npm run test:e2e   # Playwright E2E tests
```

## Common Tasks

### Adding a New Game Feature
1. Update types in `src/chess/types.ts` if needed
2. Add state and handlers in `App.tsx`
3. Update `Sidebar.tsx` for controls
4. Add unit tests for logic
5. Add E2E tests for user interactions

### Modifying the Maia Engine
1. Update `src/engine/maiaEngine.ts`
2. Add tests in `maiaEngine.test.ts`
3. If changing asset paths, update `engineAssets.ts` and `electron/main.js`

### Adding a New ELO Level
1. Add to `MAIA_ELOS` array in `maiaEngine.ts`
2. Update `MAIA_ELOS` in `electron/main.js` for download
3. Ensure weight file exists at download source

### Modifying Settings
1. Add state in `App.tsx`
2. Pass props to `Settings.tsx`
3. Add UI controls in appropriate section
4. Persist to localStorage if needed

### Debugging
- **Maia Engine**: Look for `[Maia]` prefixed logs in console
- **Stockfish**: Look for `[Stockfish]` prefixed logs in console
- **Debug Mode**: Run `npm run dev:debug` to enable `VITE_DEBUG=1` for verbose logging
- **Custom FEN**: Debug mode prompts for custom starting position
- **React DevTools**: Inspect component state and props

## Environment Variables
- `VITE_DEBUG=1`: Enable debug mode with verbose logging
- `VITE_E2E=1`: E2E test mode with deterministic engine responses
- `VIBE_STOCKFISH_DOWNLOAD_BASE_URL`: Override Stockfish download source
- `VIBE_ZEROFISH_DOWNLOAD_BASE_URL`: Override Zerofish download source
- `VIBE_MAIA_DOWNLOAD_BASE_URL`: Override Maia weights download source

## NPM Scripts
- `npm run dev`: Build and run Electron app
- `npm run dev:clean`: Clear cache and run Electron app
- `npm run dev:debug`: Run Vite dev server with debug mode
- `npm run build`: TypeScript + Vite production build
- `npm run test`: Run Vitest unit tests
- `npm run test:e2e`: Run Playwright E2E tests
- `npm run test:e2e:ui`: Run Playwright with UI
- `npm run lint`: Run ESLint
- `npm run engines:download`: Download engine assets for dev server
- `npm run electron:build`: Build desktop app for distribution
