# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Install dependencies
npm install

# Start development environment (runs both Vite and Electron concurrently)
npm run dev

# Development sub-commands
npm run dev:vite     # Start Vite dev server only
npm run dev:electron # Start Electron only

# Code quality and building
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues automatically
npm run type-check   # Run TypeScript type checking
npm run format       # Format code with Prettier
npm run build        # Full build: lint + type-check + vite build + electron-builder
npm run build:vite   # Build renderer only with Vite
```

## Architecture Overview

This is an Electron-based podcast recording application with a React frontend using Web Audio APIs for real-time audio processing and recording.

### Process Architecture
- **Main Process** (`src/main/main.js`): Electron main process handling window management, file I/O, and IPC
- **Renderer Process** (`src/renderer/`): React application running in the Electron renderer
- **Preload Script** (`src/main/preload.js`): Security bridge between main and renderer processes

### Key Components Structure

**Audio Pipeline:**
- `useAudioRecorder` hook: Core audio recording logic using MediaRecorder API and Web Audio API
- `AudioVisualizer`: Real-time waveform display using Canvas API
- `VolumeMeters`: dB-level visualization with clipping detection
- Audio format conversion: WebM recording → WAV output (browser-native conversion)

**File Management:**
- Custom filename format: `YYYYMMDD_HHMMSS_title_hostname.wav`
- Desktop default save location
- IPC-based file writing from renderer to main process
- Chunk-based recording for long sessions (5-minute auto-save intervals)

**Device Management:**
- Dynamic audio input device enumeration
- Device-specific recording with `getUserMedia` constraints
- Real-time device switching with audio context re-initialization

### Development Patterns

**IPC Communication:**
Main process exposes these APIs via preload script:
- `toggleAlwaysOnTop()`: Window management
- `showSaveDialog(title, inputSource)`: File save dialog with custom naming
- `writeFile(filePath, buffer)`: File system operations
- `getDefaultSavePath(title, inputSource)`: Generate default file paths

**State Management:**
- React hooks for UI state
- useRef for audio context persistence across re-renders
- Callback-based audio stream management to avoid closure issues

**Audio Processing:**
- 44.1kHz mono recording
- Real-time analysis with AnalyserNode
- Manual WAV encoding from WebM using AudioBuffer → PCM conversion
- Gain control via GainNode in Web Audio graph

### Build Configuration

**Vite Configuration:**
- Root set to `./src/renderer` for renderer process
- Output to `../../dist/renderer`
- Development server on port 3000

**Electron Configuration:**
- Main entry: `src/main/main.js`
- Window: 420x800px (min 400x750px)
- Security: contextIsolation enabled, nodeIntegration disabled

### Code Quality Tools
- ESLint with TypeScript, React, and Prettier plugins
- TypeScript strict mode with React 19 support
- Concurrent development with hot reload for both Vite and Electron

### File Format and Conversion
The app records in WebM format but saves as WAV files through a custom browser-based conversion process that decodes WebM to AudioBuffer, then manually constructs WAV files with proper RIFF headers and PCM data.