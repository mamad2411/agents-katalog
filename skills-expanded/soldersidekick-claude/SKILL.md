# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Solder Sidekick™ is a web application that converts 3D printers into automated soldering robots. It processes Excellon drill files from PCB design software and generates G-code to control the printer for automated through-hole soldering.

## Commands

### Development
- `npm run dev` - Start the development server on http://localhost:5173
- `npm run build` - Build for production
- `npm run preview` - Preview the production build

### Testing
No test framework is currently configured. When implementing tests, consider adding Vitest for unit tests and Playwright/Cypress for E2E tests.

### Code Quality
No linting or formatting tools are configured. Consider adding ESLint and Prettier when requested.

## Architecture

### Tech Stack
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **State Management**: Pinia with persistence plugin (localStorage)
- **3D Visualization**: Three.js
- **UI Framework**: Bootstrap 5
- **Router**: Vue Router

### Key Components

1. **State Management** (`src/stores/drillStore.js`):
   - Central store managing drill data, machine profiles, and G-code generation
   - Persisted to localStorage
   - Handles profile management, drill file processing, and configuration

2. **Core Functionality**:
   - **File Processing**: `src/composables/useFileHandlers.js` - Parses Excellon drill files
   - **G-code Generation**: `src/composables/useGcodeGenerator.js` - Converts drill points to G-code using customizable templates
   - **3D Visualization**: `src/components/ToolpathEditor.vue` - Interactive Three.js scene for PCB preview

3. **Main Views**:
   - **HomeView**: Main toolpath editor interface
   - **GettingStartedView**: User guide and documentation

### G-code Generation Flow
1. User uploads Excellon drill file
2. File is parsed to extract drill coordinates
3. Points are optimized using nearest-neighbor algorithm
4. G-code is generated using customizable templates (start, per-point, end)
5. User can preview in 3D and download the result

### Important Implementation Details

- **Coordinate System**: Uses Three.js coordinate system with transformations for PCB visualization
- **Path Optimization**: Implements nearest-neighbor algorithm for efficient soldering paths
- **Templates**: G-code templates support variable substitution for coordinates and offsets
- **Mobile Support**: Detects mobile devices and shows appropriate messaging
- **Analytics**: Includes Google Analytics and Facebook Pixel integration
- **Persistence**: All configuration and profiles stored in localStorage via Pinia plugin

## Development Notes

- The project targets Ender-3 3D printers specifically
- No authentication system - runs entirely client-side
- File processing happens in the browser using FileReader API
- Bootstrap modals are used extensively for UI interactions
- The app includes cookie consent management for compliance