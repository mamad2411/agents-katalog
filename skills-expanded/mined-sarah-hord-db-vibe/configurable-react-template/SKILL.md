---
name: configurable-react-template
description: "Building a Databricks App frontend, adding UI features (admin, chat, reports, branding), scaffolding a React app for Databricks"
---

# Configurable React Client Template

Pluggable React component library for building Databricks App frontends with runtime branding, admin panels, chat, and reports.

- **Source:** `https://github.com/databricks-field-eng/configurable-react-client-template-for-coding-agents.git`
- **Package:** `@configurable-react-client/template`
- **Build:** tsup (library), vitest (tests), biome (lint)

## When to Use

Use this template whenever you are building a Databricks App that needs a React frontend. It provides:

- Runtime-configurable branding (colors, fonts, logos) via CSS custom properties
- Admin settings panel with a plugin system
- Floating chat widget with session management
- Reports page with drafting and export
- Layout primitives (HeaderBar, TabBar, AppShell)

## Prerequisites

- Node.js 18+
- A FastAPI backend running on **port 8000** (required by the Databricks App proxy)
- Vite as the build tool (recommended)

## Quick Start

```bash
npm install @configurable-react-client/template
```

```tsx
import {
  BrandingProvider, AppShell, FloatingChat,
  useChatState, createChatApi, createConfigApi,
} from "@configurable-react-client/template";

const chatApi = createChatApi("/api");
const configApi = createConfigApi("/api");

export default function App() {
  const chatState = useChatState({ api: chatApi, storageKey: "my-app" });

  return (
    <BrandingProvider configApi={configApi}>
      <AppShell companyName="My Company" tabs={[{ id: "home", label: "Home" }]} activeTab="home" onTabChange={() => {}}>
        <div>Home content</div>
      </AppShell>
      <FloatingChat chatState={chatState} visible={true} />
    </BrandingProvider>
  );
}
```

## Module Structure

| Module | Purpose |
|---|---|
| `api/` | `createChatApi`, `createConfigApi`, `createReportsApi`, `createAdminApi`, `fetchJson` |
| `layout/` | `AppShell`, `HeaderBar`, `TabBar`, `GearMenu` |
| `branding/` | `BrandingProvider`, CSS variable injection |
| `admin/` | `AdminPage`, plugin system, all built-in plugins |
| `chat/` | `FloatingChat`, `ChatMessage`, `MentionDropdown`, `MentionChips` |
| `reports/` | `ReportsPage`, `ReportDraftIndicator`, `AddToReportButton` |
| `monitoring/` | Cache, memory, chat-log, system monitoring tabs |
| `hooks/` | `useChatState`, `useMentionState`, `useReportDraft` |

## Core Patterns

### Dependency Injection

All components receive their dependencies as **props** (API callbacks, config, state). Never via React Context directly. This makes components testable and reusable across apps.

```tsx
<AdminPage plugins={[...]} configApi={configApi} onBack={handleBack} />
<FloatingChat chatState={chatState} visible={showChat} />
```

### CSS Custom Properties

All visual theming flows through CSS variables. `BrandingProvider` sets them on `:root`:

```css
--color-primary, --color-accent, --color-header-bg, --color-success,
--color-warning, --color-danger, --color-light-bg,
--font-sans, --font-mono
```

### Plugin System (Admin)

The admin panel is composed of plugins. Each plugin is a function returning an `AdminPlugin` object:

```typescript
interface AdminPlugin {
  id: string;
  label: string;
  icon: string | ReactNode;
  group: "settings" | "monitoring";
  component: React.ComponentType<AdminPluginProps>;
  enabled?: boolean;
  order?: number;
}
```

#### Built-in Plugins

| Plugin | Group | Purpose |
|---|---|---|
| `generalPlugin()` | settings | Company name, logo upload |
| `typographyPlugin()` | settings | Font selection, custom font upload |
| `colorsPlugin({ extraGroups?, uiFields? })` | settings | Color pickers, custom color groups via `ColorFieldDef` |
| `linksPlugin()` | settings | Header links and CTA |
| `presetsPlugin()` | settings | Save/load branding presets |
| `cachePlugin()` | monitoring | Semantic cache stats, entries, events, action buttons (purge expired, invalidate, clear all), inline settings (threshold, TTL, stats toggle) |
| `memoryPlugin()` | monitoring | Agent memory entries, search, delete |
| `chatLogPlugin()` | monitoring | Chat session transcripts, message viewer |
| `systemPlugin()` | monitoring | PG diagnostics, env vars, pgvector install |

> **Important:** Settings plugins (general, colors, typography, links, presets) must be composed into a **single "Branding" sidebar tab** with inner tab navigation — NOT registered as separate `AdminPage` plugins. Monitoring plugins are registered separately. See `integration-patterns.md` for the required `adminPlugins.tsx` pattern.
>
> **Important:** Register ALL monitoring plugins, not just some. Every `*TabApi` you wire in `apiFactories.ts` needs its corresponding plugin in the `AdminPage plugins` array. See `integration-patterns.md` for the full list.

#### Custom Color Groups

```typescript
import { colorsPlugin, type ColorFieldDef } from "@configurable-react-client/template";

const myColors: ColorFieldDef[] = [
  { label: "Card Background", key: "color_card_bg", desc: "Background for dashboard cards" },
  { label: "Sidebar", key: "color_sidebar", desc: "Sidebar navigation background" },
];

colorsPlugin({ extraGroups: [{ title: "Dashboard Colors", fields: myColors }] });
```

### Layout

Use `AppShell` which combines `HeaderBar` + `TabBar`. Do NOT use `AppShell` combined with an explicit `HeaderBar` -- they are redundant.

```tsx
<AppShell
  companyName="My Company"
  tabs={[{ id: "home", label: "Home" }, { id: "admin", label: "Settings" }]}
  activeTab={activeTab}
  onTabChange={setActiveTab}
  gearMenuItems={[{ label: "Settings", onClick: () => setActiveTab("admin") }]}
>
  {/* tab content */}
</AppShell>
```

## Vite Configuration (Required)

```typescript
// vite.config.ts
resolve: {
  dedupe: ["react", "react-dom"],  // prevent dual React instances
}
```

```javascript
// tailwind.config.js
content: [
  "./src/**/*.{js,ts,jsx,tsx}",
  "./node_modules/@configurable-react-client/template/dist/**/*.{js,mjs,cjs}",
]
```

## Required Backend Endpoints

The API factories expect these endpoints on your FastAPI backend:

| Factory | Endpoints |
|---|---|
| `createChatApi("/api")` | `POST /api/chat`, `GET /api/chat/history`, `GET /api/chat/sessions`, `DELETE /api/chat/sessions/:id` |
| `createConfigApi("/api")` | `GET /api/config`, `PATCH /api/config`, `POST /api/config/logo`, `POST /api/config/font`, `POST /api/config/reset`, `GET /api/config/presets`, `POST /api/config/presets`, `DELETE /api/config/presets/:name` |
| `createReportsApi("/api")` | CRUD on `/api/reports`, export |
| `createAdminApi("/api")` | `/api/admin/cache/*`, `/api/admin/memory/*`, `/api/admin/system`, `/api/admin/chat/*` |

These backend routers can be generated by the **chat-app-utilities** package (see that skill).

## Key Types

`AdminPlugin`, `AdminPluginProps`, `ColorFieldDef`, `BrandingConfig`, `ChatState`, `ChatApiCallbacks`, `ConfigApiCallbacks`, `ReportsApiCallbacks`, `TabDefinition`, `GearMenuItem`

See `references/type-inventory.md` for complete type definitions.
See `references/integration-patterns.md` for full code examples.

## Guardrails

- NEVER delete existing Databricks Apps or shared resources without explicit user confirmation.
- NEVER use port 8080 -- Databricks App proxy requires port 8000.
- NEVER combine `AppShell` with an explicit `HeaderBar` -- `AppShell` already includes it.
- NEVER register `generalPlugin()`, `colorsPlugin()`, `typographyPlugin()`, `linksPlugin()`, or `presetsPlugin()` as separate `AdminPage` plugins -- compose them into a single "Branding" tab with inner navigation. See `integration-patterns.md` for the `adminPlugins.tsx` pattern.
- ALWAYS register ALL monitoring plugins (`cachePlugin`, `memoryPlugin`, `chatLogPlugin`, `systemPlugin`) -- not just some.
- ALWAYS dedupe React in Vite config to avoid dual-instance errors.
