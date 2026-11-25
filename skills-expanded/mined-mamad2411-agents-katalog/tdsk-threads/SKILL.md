---
name: "tdsk-threads"
description: "Knowledge base for the user-facing threads SPA — sandbox session management and interaction"
tags: ["react", "vite", "mui", "jotai", "threads", "auth", "neon", "spa", "sandbox", "session", "websocket", "terminal", "xterm", "ast", "gui-engine"]
---
# Threads Repo Skill

## Overview

The **Threads** repo (`repos/threads`, `@tdsk/threads`) is the user-facing SPA for org members to interact with sandbox sessions. Key facts:

- **Type**: User-facing sandbox session SPA (distinct from admin dashboard), Vite 5 + Bun, port 5887
- **Architecture**: Mirrors admin repo -- Jotai 3-layer state, ApiService + TanStack Query, Neon Auth, lazy-loaded routes, MUI 6 theming via shared `makeTheme()`
- **Path Aliases**: `@TTH/*` prefix via `alias-hq`
- **Features**: Dual GUI/terminal views, AST-based GUI engine, real-time WebSocket streaming, hierarchical org/project/sandbox/session navigation
- **Terminal**: xterm-based emulator via `@xterm/headless` Terminal (migrated from ghostty Wasm)

## Directory Structure

```
repos/threads/
├── configs/                # vite, frontend config, biome
├── scripts/                # setupTests, registerPaths, testUtils
├── public/                 # index.html
├── src/
│   ├── index.tsx           # Bootstrap: Jotai Provider -> AuthProvider -> App
│   ├── App.tsx             # ThemeProvider -> GlobalStyles -> RouterProvider
│   ├── actions/            # init, auth/, editor/, gui/, orgs/, projects/, sandboxes/, sessions/, sidebar/, terminal/, theme/, threads/
│   ├── components/
│   │   ├── ActivityFeed/   # ActionCard, ActivityFeed, IdleMarker, OutputCard, PromptCard, TUICard, UserInputCard
│   │   ├── ASTNodes/       # 15 node components (NodeActionTarget, NodeConfirm, NodeDiffBlock, NodeGroup, NodeLink, NodePanel, NodeSelectItem, NodeSelectList, NodeSeparator, NodeSpan, NodeStatusBar, NodeTable, NodeTableRow, NodeTextInput, NodeTextLine)
│   │   ├── Breadcrumbs/    # Breadcrumbs, OrgSelector, ProjectSelector, InstanceCrumb, SandboxCrumb, SessionCrumb
│   │   ├── ChatView/       # GenerativeUIRenderer + registry/ (GuiSelect, GuiConfirm, GuiTextInput, GuiAlert, GuiProgressBar)
│   │   ├── ConfigRow/      # ConfigRow (settings row layout)
│   │   ├── Editor/         # EditorPane, EditorStatusBar, EditorTabs, mockContent
│   │   ├── FileTree/       # FileTree, FileTreeItem, FileTree.styles, mockFiles
│   │   ├── Orgs/           # OrgCardItem, Orgs, EmptyState
│   │   ├── PagePrimitives/ # PageHeader, PillMono, ResourceCard, RowList, SectionHeader, StatStrip, StatusChip
│   │   ├── Project/        # ProjectSandboxCard, GitInfo, StatusChip, NotFound, EmptyState
│   │   ├── Session/        # SessionCommands
│   │   ├── SessionGUIView/ # SessionGUIView (top-level AST engine output renderer)
│   │   ├── SessionLayout/  # ContextPanel, SessionHeader, SessionLayout, TerminalPane
│   │   ├── Sidebar/        # Sidebar, SidebarHeader, SidebarFooter, SidebarTree, MobileSidebar, NavTree, NavProjectItem, NavSandboxItem, NavSessionItem, NavInstanceItem
│   │   ├── SmartInput/     # Context-aware input
│   │   ├── Terminal/       # TerminalView, TerminalCursorSettings, TerminalFontSettings, TerminalQuickSettings, TerminalScrollSettings, TerminalSettingsCard, TerminalTabPanels, TerminalThemeSettings
│   │   ├── Version/        # Version display
│   │   └── ViewToggle/     # ViewToggle (GUI/Terminal toggle)
│   ├── constants/          # envs, monaco, nav.tsx, options, query, sessions.tsx, storage, terminal, tokenizer, values
│   ├── contexts/           # AuthContext, AuthProvider, InteractionContext, SessionContext, SessionProvider
│   ├── hooks/              # activity/ (useActivityFeed), permissions/ (usePermissions), sandbox/ (useSandboxHasSession, useSandboxMode, useSandboxSessions), session/ (useSessionEngine, useSessionMode), theme/ (useMakeTheme, useTheme)
│   ├── pages/              # CliAuth, Home, Instance, Layout, Login, Orgs, Page, Project, Projects, Sandbox, Session, Settings
│   ├── routes/             # Routes.tsx, loaders.ts (rootLoader, orgScopeLoader, projectScopeLoader, sandboxLoader)
│   ├── services/           # api, auth, gui/ (ast/, engine/, parser/, tokenizer/, visitors/), monitorService, nav, orgsApi, projectsApi, query, sandboxApi, sessionService, storage, threadsApi, tokenRefresh
│   ├── state/              # atoms (app, gui, sessions, terminal, theme, user), accessors, selectors
│   ├── theme/              # GlobalStyles
│   ├── types/              # api, ast, contexts, engine, parser, query, routes, sandbox, sessions, terminal, theme, tokenizer
│   └── utils/              # api/, errors/, sessionStorage, stdinTranslation, terminal/
```

## Routing

React Router v7 with lazy loading, Suspense, and route loaders:

```
/ (Layout: Sidebar + SessionTabs + Outlet)
├── /                              -> Home
├── /settings                      -> Settings
├── /orgs                          -> Orgs (org list)
└── /orgs/:orgId                   -> OrgScope (orgScopeLoader)
    ├── (index)                    -> Redirect to /projects
    ├── /projects                  -> Projects
    └── /projects/:projectId       -> ProjectScope (projectScopeLoader)
        ├── (index)                -> Project
        ├── /sandbox/:sandboxId    -> Sandbox (sandboxLoader)
        └── /session/:sessionId    -> Session

/auth/cli                          -> CliAuth (CLI browser-login callback)
/auth/:pathname                    -> Login (OAuth + email/password)
*                                  -> Redirect to /
```

## Services

| Service | Purpose |
|---------|---------|
| `api.ts` | `ApiService` + `BaseApi`: fetch wrapper, Bearer token via Neon Auth, TanStack Query caching. URL: `TDSK_CADDY_PX_HOST` > `TDSK_PX_URL` > `TDSK_PX_HOST:TDSK_PX_PORT` |
| `auth.ts` | Neon Auth client wrapper: `signin(provider)`, `signout()`, `session()` |
| `gui/` | AST-based GUI engine (tokenizer, parser, AST, engine, visitors) -- see AST-Based GUI Engine section |
| `nav.ts` | `NavService` class: programmatic navigation via `history.pushState`/`replaceState` with path helpers (`org`, `projects`, `project`, `sandbox`, `session`, `settings`, `home`) |
| `orgsApi.ts` | `list()` -> `Organization[]` |
| `projectsApi.ts` | `list(orgId)` -> `Project[]` |
| `sandboxApi.ts` | `list`, `connect` -> `TSandboxConnectResponse`, `sessions` -> `TSandboxSession[]`, `stop` |
| `threadsApi.ts` | `listBySandbox` -> `Thread[]`, `messages` -> `Message[]` |
| `tokenRefresh.ts` | Proactive JWT refresh before expiry, 401 retry once |
| `query.ts` | TanStack `QueryClient` wrapper (staleTime 5min, gcTime 30min) |
| `storage.ts` | Typed localStorage wrapper with JSON serialization |

## Session Management

The core of the SPA. `openSession()` establishes a WebSocket connection to a sandbox shell by first calling `sandboxApi.connect()` to start the pod and get a `shellToken`, then opening a WebSocket to `/_/sandboxes/:sandboxId/shell?token=...&cols=80&rows=24`.

Session intent resolution: `null` = new session, `string` = specific session ID, `undefined` = auto-resolve from sessionStorage. The WebSocket handles lifecycle messages (`connected`, `joined`, `reconnected`, `visibility`, `user-joined`, `user-left`, `error`) and feeds raw terminal data to the GUI engine.

Module-scoped state (not Jotai): `connections` (Map of WebSocket instances), `rawBuffers` (terminal output ring buffer per session), `terminalWriters` (subscriber callbacks for terminal data via `subscribeTerminalData()`).

### Session Actions

| Action | Purpose |
|--------|---------|
| `openSession(opts)` | Connect WebSocket, register GUI engine, returns `Promise<sessionId>` |
| `closeSession(sessionId, opts?)` | Close WebSocket, destroy engine, remove from state |
| `sendInput(sessionId, text)` | Send binary text to WebSocket |
| `activateSession(sessionId)` | Set as active session |
| `loadSandboxSessions(sandboxId)` | Fetch sessions from backend API |
| `subscribeTerminalData(sessionId, cb)` | Subscribe to decoded terminal data, returns unsubscribe |

### GUI Actions

| Action | Purpose |
|--------|---------|
| `registerEngine(sessionId)` | Create a `SessionEngine` for a session, wire AST/feed callbacks to state |
| `destroyEngine(sessionId)` | Tear down engine and clean up state maps |
| `destroyAllEngines()` | Tear down all engines |
| `setEngineAst(sessionId, doc)` | Update AST document in state |
| `appendFeedEvents(sessionId, events)` | Append feed events to the session's feed state |

### Terminal Actions

| Action | Purpose |
|--------|---------|
| `load()` | Load terminal settings from storage |
| `set(settings)` | Persist terminal settings to storage |
| `update(partial)` | Merge partial settings update |
| `reset()` | Reset terminal settings to defaults |

## AST-Based GUI Engine

The threads app uses an AST-based pipeline to render structured terminal output as interactive GUI components:

**Pipeline**: Raw terminal data -> **Tokenizer** (classify, decode, palette, runs, blocks, borders) -> **Parser** (flatParser, modeDetector, scopeParser) -> **AST** (node tree) -> **Engine** (SessionEngine, xtermBridge) -> **Visitors** (accessibilityVisitor, feedVisitor, interactionVisitor, renderVisitor)

### Tokenizer (`services/gui/tokenizer/`)

Converts raw terminal cell grids into classified token runs with color/style info:

- `tokenize()` -- main entry: viewport + cursor -> token result with palette
- `classify` -- cell classification into semantic types
- `decode` -- cell decoding, color resolution, test viewport builder
- `palette` -- palette detection and caching across frames
- `runs` -- group cells into styled runs
- `blocks` -- segment runs into logical blocks
- `borders` -- trace box-drawing borders for panel detection

### Parser (`services/gui/parser/`)

Parses token streams into structured data with mode detection:

- `parse()` -- main entry: token result + mode context -> `TDocument`
- `flatParser` -- parse flat content regions (text lines, prompts)
- `modeDetector` -- detect viewport mode (`interactive`, `streaming`, `tui`, `idle`) from cursor/dirty-row heuristics
- `scopeParser` -- parse structured scopes (panels, tables, selects, diffs)

### AST (`services/gui/ast/`)

Creates typed AST node tree from parsed output. Node types include: `Document`, `Panel`, `Group`, `TextLine`, `Span`, `Table`, `TableRow`, `SelectList`, `SelectItem`, `TextInput`, `Confirm`, `DiffBlock`, `StatusBar`, `ActionTarget`, `Link`, `Separator`.

### Engine (`services/gui/engine/`)

Per-session engine managing the full pipeline:

- `SessionEngine` -- class that owns a WASM-backed virtual terminal (`xtermBridge`), processes incoming data through tokenize -> parse -> diff, emits AST documents and feed events via callbacks. Uses `requestAnimationFrame` for batched processing with idle-check interval for mode transitions.
- `xtermBridge` -- creates browser-side ghostty virtual terminal (`TBrowserVTerminal`) for VT parsing without a visible terminal element. Provides `write`, `resize`, `getDirtyRows`, `getCursor`, `getViewport`, `isAlternateScreen`, `markClean`, `free`.

### Visitors (`services/gui/visitors/`)

Traverse AST for different purposes:

- `renderVisitor` -- `renderNode(node)` / `renderDocument(doc)`: converts AST nodes to React elements (the ASTNode components)
- `feedVisitor` -- `diffToFeedEvents(prevDoc, nextDoc)`: diffs two documents to produce incremental `TFeedEvent[]` for the ActivityFeed
- `accessibilityVisitor` -- `getAriaProps(node)`: generates ARIA attributes for AST nodes
- `interactionVisitor` -- `collectInteractions(doc)`: extracts interactive elements for keyboard/input handling

### ASTNode Components (15)

Visual representations of AST nodes, rendered by `renderVisitor`:

| Component | AST Node Type | Purpose |
|-----------|--------------|---------|
| `NodePanel` | `Panel` | Bordered panel with title |
| `NodeGroup` | `Group` | Logical grouping container |
| `NodeTextLine` | `TextLine` | Single line of styled text |
| `NodeSpan` | `Span` | Inline styled text run |
| `NodeTable` | `Table` | Tabular data layout |
| `NodeTableRow` | `TableRow` | Single table row |
| `NodeSelectList` | `SelectList` | Selection list (arrow/number select) |
| `NodeSelectItem` | `SelectItem` | Individual selection option |
| `NodeTextInput` | `TextInput` | Text input field |
| `NodeConfirm` | `Confirm` | Yes/No confirmation prompt |
| `NodeDiffBlock` | `DiffBlock` | File diff display |
| `NodeStatusBar` | `StatusBar` | Status bar (bottom of screen) |
| `NodeActionTarget` | `ActionTarget` | Clickable action target |
| `NodeLink` | `Link` | Hyperlink |
| `NodeSeparator` | `Separator` | Visual separator line |

### ActivityFeed (7 components)

Event-driven feed display rendered from `TFeedEvent[]` produced by the feedVisitor:

| Component | Feed Event Kind | Purpose |
|-----------|----------------|---------|
| `ActionCard` | `action` | Tool/action invocation display |
| `OutputCard` | `output` | Command output block (collapsible) |
| `PromptCard` | `prompt` | AI/system prompt display |
| `UserInputCard` | `input` | User-entered command/text |
| `TUICard` | `tui` | Full-screen TUI snapshot |
| `IdleMarker` | `idle` | Idle state indicator |
| `ActivityFeed` | -- | Container that renders event list |

### SessionGUIView

Top-level GUI view component that orchestrates AST engine output rendering. Reads the AST document from `guiASTState` and feed events via `useActivityFeed(sessionId)`. Renders in two modes:
- **TUI mode** (`mode === 'tui'` with AST doc): renders full AST document via `renderDocument()` with `InteractionContext` for keystroke forwarding
- **Feed mode** (has feed events): renders `ActivityFeed` with event list
- Falls back to AST document rendering or empty ActivityFeed

### GenerativeUIRenderer

Legacy component still present for backend-sent `generative-ui` WebSocket messages. Recursively renders a `TJsonComponentTree` using registered components (GuiSelect, GuiConfirm, GuiTextInput, GuiAlert, GuiProgressBar) or allowed HTML elements, with `onAction` callbacks for interaction.

`translateInteraction()` in `utils/stdinTranslation.ts` converts GUI interactions to stdin bytes: ArrowSelect (arrow keys + Enter), NumberSelect (digit + Enter), YesNo (`y`/`n` + Enter), TextInput (text + Enter), Keystroke (raw key).

## SmartInput

Context-aware input adapting based on session state and permissions. Single component in `SmartInput/SmartInput.tsx`.

## Terminal

Full terminal emulator via `ghostty-web` with configurable settings. The `Terminal/` directory contains:

- **TerminalView**: Core terminal emulator with JetBrains Mono font, Catppuccin Mocha theme, 10000-line scrollback. Uses FitAddon for auto-resize. On mount, replays `getRawBuffer(sessionId)` to restore output. Input/output wired: `term.onData` -> `sendInput()`, `term.onResize` -> `sendControl(resize)`, `subscribeTerminalData()` -> `term.write()`.
- **TerminalSettingsCard**: Settings panel container
- **TerminalCursorSettings**: Cursor style/blink configuration
- **TerminalFontSettings**: Font family/size settings
- **TerminalScrollSettings**: Scrollback buffer configuration
- **TerminalThemeSettings**: Terminal color theme selection
- **TerminalQuickSettings**: Quick-access settings popover
- **TerminalTabPanels**: Tab panels for settings categories

## ViewToggle

Toggle between GUI and Terminal views. `ToggleButtonGroup` with `gui` and `terminal` modes.

## Sidebar Navigation

Hierarchical navigation: **Org -> Project -> Sandbox -> Session/Thread**. Key components: `Sidebar` (responsive via `DesktopSidebar`/`MobileSidebar`), `NavTree` (groups sandboxes by project), `NavProjectItem`, `NavSandboxItem` (with status indicator), `NavSessionItem`, `NavThreadItem`, `SBLogo`.

## Session Tabs

`SessionTabs` (desktop tab bar with close buttons, status dots, permission badges) and `OpenSessionStrip` (mobile compact chip bar). Status dot colors: green = working, amber = permission needed, gray = idle.

## Pages

- **Session**: Primary workspace -- GUI/terminal toggle via ViewToggle, SessionCommands toolbar, SmartInput, auto-reconnect via SessionProvider, disconnected state shows sandbox config + "Start Session" button
- **Sandbox**: Session list (own + shared) with reconnect/join/new actions
- **Project**: Sandbox card grid with runtime chips, status indicators, git info
- **Projects**: Project list per selected org
- **Orgs**: Organization list/selection with OrgCardItem cards
- **Home**: Dashboard with org/project/sandbox summary, mobile OpenSessionStrip
- **CliAuth**: CLI authentication callback page for `tsa login --browser`
- **Settings**: Terminal settings, theme preferences
- **SessionCommands**: Stop, Restart, Recreate, New, Share/Shared toggle, Leave (non-owner)

## Contexts

| Context | Purpose |
|---------|---------|
| `AuthContext` / `AuthProvider` | Neon Auth session management, user state, token refresh |
| `SessionContext` / `SessionProvider` | Per-session state: `isOwner`, `connecting`, `pendingOp`, `sandboxId`, `projectId`, `session`. Handles auto-reconnect when navigating to a session URL without an active WebSocket. |
| `InteractionContext` | Provides `sendKeystroke` callback to ASTNode components for keyboard interaction forwarding |

## Hooks

| Directory | Hooks | Purpose |
|-----------|-------|---------|
| `activity/` | `useActivityFeed` | Returns feed events and viewport mode for a session from GUI state |
| `permissions/` | `usePermissions` | Permission checking |
| `sandbox/` | `useSandboxHasSession`, `useSandboxMode`, `useSandboxSessions` | Sandbox session state queries |
| `session/` | `useSessionEngine`, `useSessionMode` | Session engine access and mode detection |
| `theme/` | `useMakeTheme`, `useTheme` | MUI theme creation and access |

## State Management

Jotai with the same 3-layer pattern as admin: atoms -> accessors -> selectors.

**Atoms** (`src/state/`):
- `app.ts`: `sidebarOpenState`, `orgIdState`, `activeProjectIdState`, `activeOrgRoleState`, derived `activeOrgState`, `activeProjectState`
- `gui.ts`: `guiASTState` (Map of AST documents per session), `guiFeedState` (Map of feed events per session), `guiModeState` (Map of viewport mode per session), `guiEngineState` (Map of SessionEngine instances per session)
- `sessions.ts`: `projectsAtom`, `sandboxesAtom`, `orgsAtom`, `activeSessionAtom`, `openSessionsAtom`, `backendSessionsAtom`
- `terminal.ts`: `terminalSettingsAtom` (cursor, font, scroll, theme preferences)
- `theme.ts`: `themeTypeState`
- `user.ts`: `userState`

**Accessors** (`src/state/accessors.ts`): 30+ imperative `get*/set*/reset*` functions for use outside React. Key: `setOpenSession`, `removeOpenSession`, `setActiveSession`, `setGuiAsts`, `setGuiFeeds`, `setGuiModes`, `setGuiEngines`, `setTerminalSettings`, `resetTerminalSettings`.

**Selectors** (`src/state/selectors.ts`): Read-only hook-based access for components. Key: `useUser`, `useOrgId`, `useOpenSessions`, `useActiveSession`, `useSandboxes`, `useOrgs`, `useProjects`, `useActiveOrg`, `useActiveProject`, `useGuiAst`, `useGuiFeed`, `useGuiModes`, `useGuiEngines`, `useBackendSessions`, `useTerminalSettings`.

## Key Patterns

**AST Pipeline**: Terminal output flows through tokenizer -> parser -> AST -> engine -> visitors. Each session has its own `SessionEngine` instance that owns a WASM virtual terminal, processes incoming data via `requestAnimationFrame` batching, and emits AST documents + feed events through callbacks. Feed events are diffed incrementally (`diffToFeedEvents`) so only changes propagate.

**Dual View**: Users can toggle between GUI view (AST-rendered via SessionGUIView) and raw terminal view (ghostty-web TerminalView) using the ViewToggle component. GUI view switches between TUI mode (full AST render) and feed mode (ActivityFeed) based on the viewport mode detected by the engine.

**Session Persistence**: Browser `sessionStorage` tracks active sessions per sandbox: `storeSession`, `removeStoredSession`, `getStoredSessions`, `findSandboxForSession` (reverse lookup for Session page).

**Token Refresh**: `TokenRefreshManager` schedules proactive refresh before JWT expiry. On 401: refresh + retry once.

**Navigation**: `NavService` singleton (`nav`) provides programmatic routing via `history.pushState`/`replaceState` with typed path helpers. Route loaders (`rootLoader`, `orgScopeLoader`, `projectScopeLoader`, `sandboxLoader`) prefetch data on navigation.

## Integration Points

- **@tdsk/components**: `makeTheme`, `Loading`, `Text`, `LoadingButton`, `Storage`, `TSIcon`, `useEffectOnce`, `MemoChildren`, `useTheme`, `colors`, `cmx`, `dims`
- **@tdsk/domain**: `User`, `Organization`, `Project`, `Sandbox`, `Thread`, `Message`, `TInteraction`, `TJsonComponentTree`, `AllowedHtmlElements`, `ESandboxSessionVisibility`, `TSandboxConnectResponse`, `TSandboxSession`, `SandboxIdPrefix`
- **Path Aliases**: `@TTH/*` (threads), `@TDM/*` (domain), `@TSC/*` (components)

## Types

| Type File | Contents |
|-----------|----------|
| `api.types.ts` | API response/request types |
| `ast.types.ts` | AST node types (`TDocument`, `TFeedEvent`, `TViewportMode`, node union types) |
| `contexts.types.ts` | Context type definitions (`TInteractionCtx`) |
| `engine.types.ts` | Engine types (`TBrowserVTerminal`, engine callbacks) |
| `parser.types.ts` | Parser types (`TModeContext`, parsed output structures) |
| `query.types.ts` | TanStack Query key types |
| `routes.types.ts` | Route path enum (`ERoutePath`), route params |
| `sandbox.types.ts` | Sandbox-specific types |
| `sessions.types.ts` | Session types (`TOpenSession`, `TPendingOp`, `TViewMode`, `TSessionLocationState`) |
| `terminal.types.ts` | Terminal settings types (`TTerminalSettings`) |
| `theme.types.ts` | Theme types (`EThemeType`) |
| `tokenizer.types.ts` | Tokenizer types (`TPalette`, cell/run/block types) |

## Commands

```bash
pnpm start          # Dev server (port 5887)
pnpm build          # Production build
pnpm test           # Vitest tests
pnpm types          # TypeScript type checking
```
