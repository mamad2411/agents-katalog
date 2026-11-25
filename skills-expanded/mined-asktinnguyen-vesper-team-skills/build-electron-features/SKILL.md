---
name: build-electron-features
description: Build full-stack features for the Vesper Electron app following established patterns. Use when implementing new features that span main process, preload, and renderer. Triggers on requests to add features, create new panels, add IPC handlers, or extend the navigation system.
---

# Build Electron Features

## Overview

This skill provides patterns for building complete features in the Vesper Electron app, covering the full stack from main process services to React UI components. Follow these patterns to ensure consistency with existing code.

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│  Renderer (React)                                    │
│  - Components in src/renderer/components/            │
│  - Navigation via NavigationContext                  │
│  - State management with Jotai atoms                 │
├─────────────────────────────────────────────────────┤
│  Preload Bridge (src/preload/index.ts)              │
│  - Exposes main process APIs to renderer            │
│  - Type-safe via ElectronAPI interface              │
├─────────────────────────────────────────────────────┤
│  Main Process (src/main/)                           │
│  - Services for business logic                       │
│  - IPC handlers in ipc.ts                           │
│  - App lifecycle in index.ts                        │
└─────────────────────────────────────────────────────┘
```

## Implementation Checklist

When adding a new feature, follow this order:

### 1. Define Types (`src/shared/types.ts`)

```typescript
// Data model
export interface MyFeature {
  id: string
  name: string
  // ... fields
}

// Form data for create/update
export interface MyFeatureFormData {
  name: string
  // ... subset of fields
}

// IPC channels
export const IPC_CHANNELS = {
  // ... existing channels
  MY_FEATURE_LIST: 'myFeature:list',
  MY_FEATURE_CREATE: 'myFeature:create',
  MY_FEATURE_UPDATE: 'myFeature:update',
  MY_FEATURE_DELETE: 'myFeature:delete',
  MY_FEATURE_EVENT: 'myFeature:event',  // For main→renderer events
}

// Add to ElectronAPI interface
export interface ElectronAPI {
  // ... existing methods
  myFeatureList(workspaceId: string): Promise<MyFeature[]>
  myFeatureCreate(workspaceId: string, data: MyFeatureFormData): Promise<MyFeature>
  onMyFeatureEvent(callback: (event: MyFeatureEvent) => void): () => void
}
```

### 2. Create Main Process Service (`src/main/my-feature.ts`)

```typescript
import { BrowserWindow } from 'electron'
import { readFile, writeFile, mkdir } from 'fs/promises'
import { existsSync } from 'fs'
import { join, dirname } from 'path'
import { mainLog } from './logger'
import { IPC_CHANNELS } from '../shared/types'

export class MyFeatureService {
  private items: MyFeature[] = []
  private filePath: string

  constructor(workspacePath: string) {
    this.filePath = join(workspacePath, 'my-feature.json')
  }

  async start(): Promise<void> {
    await this.load()
  }

  private async load(): Promise<void> {
    try {
      if (existsSync(this.filePath)) {
        const data = await readFile(this.filePath, 'utf-8')
        this.items = JSON.parse(data).items || []
      }
    } catch (error) {
      mainLog.error('Failed to load my-feature:', error)
      this.items = []
    }
  }

  private async save(): Promise<void> {
    const dir = dirname(this.filePath)
    if (!existsSync(dir)) {
      await mkdir(dir, { recursive: true })
    }
    await writeFile(this.filePath, JSON.stringify({ items: this.items }, null, 2))
  }

  // Broadcast events to all windows
  private broadcastEvent(event: MyFeatureEvent): void {
    const windows = BrowserWindow.getAllWindows()
    for (const window of windows) {
      if (!window.isDestroyed()) {
        window.webContents.send(IPC_CHANNELS.MY_FEATURE_EVENT, event)
      }
    }
  }

  // CRUD operations
  async create(data: MyFeatureFormData): Promise<MyFeature> { /* ... */ }
  async update(id: string, data: Partial<MyFeatureFormData>): Promise<MyFeature | null> { /* ... */ }
  async delete(id: string): Promise<void> { /* ... */ }
  list(): MyFeature[] { return [...this.items] }
}

// Per-workspace instance management
const services: Map<string, MyFeatureService> = new Map()

export function getMyFeatureService(workspaceId: string, workspacePath: string): MyFeatureService {
  let service = services.get(workspaceId)
  if (!service) {
    service = new MyFeatureService(workspacePath)
    services.set(workspaceId, service)
  }
  return service
}
```

### 3. Add IPC Handlers (`src/main/ipc.ts`)

```typescript
import { getMyFeatureService } from './my-feature'

// In registerIpcHandlers function:

ipcMain.handle(IPC_CHANNELS.MY_FEATURE_LIST, async (_event, workspaceId: string) => {
  const workspace = getWorkspaceOrThrow(workspaceId)
  const service = getMyFeatureService(workspaceId, workspace.rootPath)
  return service.list()
})

ipcMain.handle(IPC_CHANNELS.MY_FEATURE_CREATE, async (_event, workspaceId: string, data) => {
  const workspace = getWorkspaceOrThrow(workspaceId)
  const service = getMyFeatureService(workspaceId, workspace.rootPath)
  return await service.create(data)
})
```

### 4. Expose in Preload (`src/preload/index.ts`)

```typescript
// In the api object:

myFeatureList: (workspaceId: string) =>
  ipcRenderer.invoke(IPC_CHANNELS.MY_FEATURE_LIST, workspaceId),

myFeatureCreate: (workspaceId: string, data: MyFeatureFormData) =>
  ipcRenderer.invoke(IPC_CHANNELS.MY_FEATURE_CREATE, workspaceId, data),

// Event listener with cleanup
onMyFeatureEvent: (callback: (event: MyFeatureEvent) => void) => {
  const handler = (_event: Electron.IpcRendererEvent, featureEvent: MyFeatureEvent) => {
    callback(featureEvent)
  }
  ipcRenderer.on(IPC_CHANNELS.MY_FEATURE_EVENT, handler)
  return () => {
    ipcRenderer.removeListener(IPC_CHANNELS.MY_FEATURE_EVENT, handler)
  }
},
```

### 5. Add Navigation (if feature needs its own panel)

**`src/shared/types.ts`:**
```typescript
export interface MyFeatureNavigationState {
  navigator: 'myFeature'
  rightSidebar?: RightSidebarPanel
}

export type NavigationState =
  | ChatsNavigationState
  | SourcesNavigationState
  // ... existing
  | MyFeatureNavigationState

export const isMyFeatureNavigation = (
  state: NavigationState
): state is MyFeatureNavigationState => state.navigator === 'myFeature'
```

**`src/shared/route-parser.ts`:**
```typescript
// Add to COMPOUND_ROUTE_PREFIXES
const COMPOUND_ROUTE_PREFIXES = [
  'allChats', 'flagged', /* ... */, 'myFeature'
]

// Add parsing
if (first === 'myFeature') {
  return { navigator: 'myFeature', details: null }
}

// Add to buildRouteFromNavigationState
if (state.navigator === 'myFeature') {
  return 'myFeature'
}
```

**`src/shared/routes.ts`:**
```typescript
myFeature: () => 'myFeature' as const,
```

**`src/renderer/contexts/NavigationContext.tsx`:**
```typescript
import { isMyFeatureNavigation } from '../../shared/types'
export { isMyFeatureNavigation }
```

### 6. Create React Components

**`src/renderer/components/my-feature/MyFeatureList.tsx`:**
```typescript
import { useState, useEffect, useCallback } from 'react'
import type { MyFeature, MyFeatureEvent } from '../../../shared/types'

interface MyFeatureListProps {
  workspaceId: string
}

export function MyFeatureList({ workspaceId }: MyFeatureListProps) {
  const [items, setItems] = useState<MyFeature[]>([])

  // Load items
  useEffect(() => {
    window.electronAPI.myFeatureList(workspaceId).then(setItems)
  }, [workspaceId])

  // Subscribe to events for live updates
  useEffect(() => {
    const cleanup = window.electronAPI.onMyFeatureEvent((event: MyFeatureEvent) => {
      // Refresh list on relevant events
      window.electronAPI.myFeatureList(workspaceId).then(setItems)
    })
    return cleanup
  }, [workspaceId])

  // ... render
}
```

### 7. Add to AppShell Sidebar

**`src/renderer/components/app-shell/AppShell.tsx`:**
```typescript
import { MyFeatureList } from '@/components/my-feature/MyFeatureList'
import { isMyFeatureNavigation } from '@/contexts/NavigationContext'

// Add handler
const handleMyFeatureClick = useCallback(() => {
  navigate(routes.view.myFeature())
}, [])

// Add to sidebar links array
{
  id: "nav:myFeature",
  title: "My Feature",
  icon: SomeIcon,
  variant: isMyFeatureNavigation(navState) ? "default" : "ghost",
  onClick: handleMyFeatureClick,
},

// Add to navigator panel rendering
{isMyFeatureNavigation(navState) && activeWorkspaceId && (
  <MyFeatureList workspaceId={activeWorkspaceId} />
)}
```

### 8. Initialize on App Start (if needed)

**`src/main/index.ts`:**
```typescript
import { startMyFeatureServices, stopMyFeatureServices } from './my-feature'

// In app.whenReady():
await startMyFeatureServices(workspaces, windowManager)

// In before-quit:
await stopMyFeatureServices()
```

## Key Patterns

### Workspace Isolation
Each workspace gets its own service instance and data file:
```typescript
const services: Map<string, MyService> = new Map()
export function getService(workspaceId: string, path: string): MyService {
  let service = services.get(workspaceId)
  if (!service) {
    service = new MyService(path)
    services.set(workspaceId, service)
  }
  return service
}
```

### Event Cleanup in React
Always return cleanup function from event subscriptions:
```typescript
useEffect(() => {
  const cleanup = window.electronAPI.onSomeEvent(callback)
  return cleanup  // Prevents memory leaks
}, [deps])
```

### JSON Persistence
Use JSON files for simple data (<1000 items):
```typescript
// File: ~/.craft-agent/workspaces/{id}/feature.json
{
  "items": [...]
}
```

### Type-Safe IPC
Define channels as constants and types for handlers:
```typescript
// shared/types.ts
export const IPC_CHANNELS = {
  FEATURE_ACTION: 'feature:action',
}

// main/ipc.ts
ipcMain.handle(IPC_CHANNELS.FEATURE_ACTION, async (_event, ...args) => {
  // TypeScript knows the channel name
})
```

## References

- Solution doc: `docs/solutions/best-practices/electron-scheduler-feature-implementation-20260122.md`
- Example feature: `src/main/scheduler.ts`, `src/renderer/components/scheduler/`
