# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TwinSafeLoaderUI** is an Electron + React + TypeScript desktop application that provides a GUI for the Beckhoff TwinSAFE Loader. It enables management, loading, activation, and deletion of TwinSAFE Logic projects on EtherCAT-based safety controllers.

The architecture follows **SOLID principles** with clear separation of concerns:
- **Service Layer** - CLI abstraction and system integrations
- **Domain Layer** - Pure business logic and entities
- **State Management** - Centralized React state with persistence
- **UI Layer** - Pure presentational components

## Quick Start Commands

```bash
# Install dependencies
npm install

# Development server (Vite) - React UI only
npm run dev

# Build TypeScript (Electron main + preload)
npm run build:main

# Build React assets
npm run build:react

# Build everything
npm run build

# Run as Electron app (builds main first, then launches)
npm start

# Package as distributable Electron app
npm run dist
```

## Architecture Overview

### 4-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  UI Layer (React Components)                │
│  - App.tsx, DeviceTable.tsx, etc.          │
│  - Pure presentational, no business logic  │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  State Management (@state/)                 │
│  - useAppState.ts - Centralized state      │
│  - useLoaderActions.ts - Business actions  │
│  - useGateway.ts - Gateway operations      │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  Domain Layer (@domain/)                    │
│  - DeviceManager - Device operations       │
│  - ProjectManager - Project operations     │
│  - CredentialManager - Auth logic          │
│  - GatewayManager - Network configuration  │
│  - Pure business logic, no React/UI        │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  Service Layer (@services/)                 │
│  - CliExecutor - TwinSAFE_Loader.exe       │
│  - NetworkService - Network interfaces     │
│  - FileService - File dialogs & CSV I/O    │
│  - Abstracts external integrations         │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  External Systems                           │
│  - Electron IPC (main.ts)                  │
│  - TwinSAFE_Loader.exe                     │
│  - File system                             │
│  - Network interfaces                      │
└─────────────────────────────────────────────┘
```

### SOLID Principles Applied

1. **Single Responsibility**: Each class/hook has one reason to change
   - `DeviceManager` only handles device scanning
   - `ProjectManager` only handles project operations
   - `CredentialManager` only handles credentials logic

2. **Open/Closed**: Services can be extended without modification
   - `ICliExecutor` interface allows mock/real implementations
   - `MockCliExecutor` for testing, `CliExecutor` for production

3. **Liskov Substitution**: Services implement consistent interfaces
   - All CLI executors implement `ICliExecutor`
   - All network services implement `INetworkService`

4. **Interface Segregation**: Small, specific interfaces
   - `ICliExecutor` - Only execution capability
   - `INetworkService` - Only network queries
   - Components accept only interfaces they need

5. **Dependency Inversion**: Classes depend on abstractions
   - `DeviceManager` depends on `ICliExecutor` interface, not concrete class
   - `useLoaderActions` hook creates services via `ServiceFactory`
   - Easy to swap implementations (mock/real)

## Directory Structure

```
src/
├── types/                    # TypeScript type definitions
│   └── index.ts             # All interfaces and types
├── services/                 # Service Layer (Dependency Injection)
│   ├── CliExecutor.ts       # CLI execution abstraction
│   ├── NetworkService.ts    # Network interface access
│   ├── FileService.ts       # File operations
│   └── index.ts             # ServiceFactory
├── domain/                   # Domain/Business Logic (No React)
│   ├── DeviceManager.ts     # Device scanning & info
│   ├── ProjectManager.ts    # Load, activate, delete projects
│   ├── CredentialManager.ts # Credential resolution logic
│   ├── GatewayManager.ts    # Gateway validation & management
│   ├── utils.ts             # Pure business logic functions
│   └── index.ts             # Export all managers
├── state/                    # State Management (Hooks)
│   ├── useAppState.ts       # Centralized state + persistence
│   ├── useLoaderActions.ts  # Hook orchestrating domain layers
│   ├── useGateway.ts        # Gateway-specific operations
│   └── index.ts             # Export all hooks
├── renderer/                 # React UI Layer (TypeScript)
│   ├── App.tsx              # Root component
│   ├── components/          # Presentational components
│   │   ├── GatewaySelector.tsx
│   │   ├── UserSection.tsx
│   │   ├── DeviceTable.tsx
│   │   └── StatusBox.tsx
│   ├── utils/               # UI utility functions
│   │   ├── export.ts        # Config export/import
│   │   └── index.ts
│   └── App.css              # Styles
├── main/
│   └── main.ts              # Electron main process (TypeScript)
└── preload/
    └── preload.ts           # Electron preload script (TypeScript)
```

## Key Concepts

### Dependency Injection via ServiceFactory

Instead of directly importing implementations, use `ServiceFactory`:

```typescript
const cliExecutor = ServiceFactory.createCliExecutor();
// Returns CliExecutor in production, MockCliExecutor in testing
```

This allows switching between real and mock implementations globally via:
```typescript
ServiceFactory.setMockMode(true); // Use mocks
```

### State Separation

**Business State** (persisted, core to app):
- devices, gateway, binFiles, crcAfterLoad, credentials

**UI State** (transient, for presentation):
- detailsOpen, testResults, activateResults, scanStatus

See `useAppState()` for implementation.

### Manager Pattern

Each manager handles one domain:
- **DeviceManager**: Scan devices, parse CSV
- **ProjectManager**: Load, activate, delete projects
- **CredentialManager**: Resolve which credentials to use
- **GatewayManager**: Validate and manage gateways

Managers depend only on service interfaces, not React.

### Pure Components

Components receive all needed data as props:
```typescript
interface DeviceTableProps {
  devices: Device[];
  onTestLogin: (addr: string) => void;
  // ... all data and callbacks
}
```

No direct state mutation, no side effects in render.

## Data Flow Example: Load Project

```
User clicks "Laden" button in DeviceTable
  → App.handleLoadBin() callback
    → loaderActions.handleLoadBin(slaveAddr)
      → projectManager.loadProject()
        → cliExecutor.execute(['TwinSAFE_Loader.exe', '--proj', ...])
          → window.api.runLoader() [IPC to main.ts]
            → Electron execFile() with TwinSAFE_Loader.exe
              → extractProjectCrc() from stdout
        → setCrcAfterLoad(crc) [update UI state]
        → onCrcLoaded(crc) [callback to App]
      → App updates UI via state setters
        → DeviceTable re-renders with new CRC
```

## IPC Bridge (Preload)

The preload script (`src/preload/preload.ts`) safely exposes:

```typescript
interface WindowApi {
  getNetworkInterfaces(): Promise<NetworkAdapter[]>;
  runLoader(args: string[]): Promise<CliResult>;
  readCsv(filePath: string): Promise<string>;
  chooseBinFile(): Promise<string | null>;
}
```

Accessible as `window.api` in renderer process.

## TypeScript Configuration

- **tsconfig.json**: Main TypeScript config with path aliases
  - `@services` → `src/services`
  - `@domain` → `src/domain`
  - `@state` → `src/state`
  - `@components` → `src/renderer/components`
  - `@types` → `src/types`

- **tsconfig.node.json**: Config for Vite and build tools

## Development Notes

- **No mock mode in production**: Ensure `ServiceFactory.setMockMode(false)` or remove mock calls
- **Type safety**: All TypeScript, strict mode enabled
- **Async patterns**: Promises used throughout, no callbacks
- **Error handling**: Try-catch in hooks, error callbacks to UI
- **Testing**: Easy to test managers with mock services
- **DevTools**: Auto-open in dev mode

## Important Files Reference

| File | Purpose |
|------|---------|
| `src/types/index.ts` | All TypeScript interfaces |
| `src/services/index.ts` | ServiceFactory for dependency injection |
| `src/domain/DeviceManager.ts` | Device scanning logic |
| `src/domain/ProjectManager.ts` | Project operations (load, activate, delete) |
| `src/state/useAppState.ts` | Centralized persistent state |
| `src/state/useLoaderActions.ts` | Orchestrates domain managers |
| `src/renderer/App.tsx` | Root component, orchestrates everything |
| `src/main/main.ts` | Electron IPC handlers |
| `src/preload/preload.ts` | Secure API bridge to renderer |
