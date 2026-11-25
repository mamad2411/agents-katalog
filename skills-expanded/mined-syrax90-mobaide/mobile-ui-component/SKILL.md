---
name: mobile-ui-component
description: Use when creating or modifying Android Jetpack Compose UI components, screens, ViewModels, or wiring new ServerEvent types/repositories under android/app/src/main/java/com/mobaide/app/. Enforces SOTA Compose + UDF patterns and the project's server-sync refresh rule.
when_to_use: Triggered for any work touching `android/app/src/main/java/com/mobaide/app/ui/**` or any Repository in `data/repository/**` whose state is rendered by the UI, and for adding/extending `ServerEvent` types in `data/events/**`.
---

# Mobile UI Component Rules

The Android client talks to a FastAPI server over REST + a single push WebSocket (`ServerEventBus`). Every UI piece must stay consistent with that reality. The rules below are short on purpose — read the linked reference file before writing code in that area.

## Hard rules (every screen / component)

1. **State** — One sealed `UiState` (`Loading | Success(data) | Error(message) | Empty`) per screen, owned by an `@HiltViewModel` and exposed as `StateFlow<UiState>` built with `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), Loading)`. UI MUST collect with `collectAsStateWithLifecycle()` — never raw `collectAsState()` (loses data on backgrounding and keeps coroutines alive off-screen).
2. **Composables are stateless and hoisted** — accept `Modifier` as the first optional param, take data + lambdas only, never read a ViewModel directly except in the top-level `*Screen` entry point. Every public composable has a `@Preview` for light + dark, sets `contentDescription` on non-text elements, uses `Modifier.testTag(...)` on anything a test would assert, and respects 48dp touch targets. Material3 only.
3. **Server-sync rule (load-bearing — this is why the skill exists).** Any button or gesture that triggers a server mutation OR fetch MUST end with the UI reflecting fresh server state. The canonical pattern:
   - ViewModel calls a Repository method.
   - The Repository hits REST and is the **single source of truth** — it owns a `MutableStateFlow` that the UI observes.
   - The Repository ALSO subscribes to the relevant `ServerEvent` from `ServerEventBus` in its `init`, so the WebSocket push from the server reconciles the cache automatically (see `SessionRepository` for the canonical example).
   - If no `ServerEvent` exists yet for the affected entity, **prefer** adding one (see `references/server_event_bus.md`). Only as a fallback, the ViewModel may explicitly refetch in the same coroutine after the mutation succeeds.
   - Default to **optimistic** updates with a snackbar "Retry" on failure. Pessimistic spinner only for destructive / irreversible actions (delete, force-stop).
   - Debounce rapid clicks with `collectLatest` on an intent flow, and pass a client-generated idempotency key on every mutation.
4. **One-shot events** (navigate, transient toast) MUST use `Channel<Event>(Channel.BUFFERED).receiveAsFlow()`, NEVER `SharedFlow`/`StateFlow`. `SharedFlow` replays on configuration change and triggers the navigation twice — this is a known footgun the project has hit.
5. **Errors** render via a single screen-level `SnackbarHost` driven by `UiState.Error`. Do NOT scatter ad-hoc `LaunchedEffect { snackbarHostState.showSnackbar(...) }` blocks per screen — use the shared helper in `ui/common/`.
6. **Reuse first** — before writing a new composable, check `ui/common/` (`LoadingIndicator`, `StatusChip`, `AutoScanCard`, etc.). If a new component is used in two places, promote it to `ui/common/` immediately.
7. **File layout** — `ui/{feature}/{Feature}Screen.kt`, `{Feature}ViewModel.kt`, `{Feature}UiState.kt`. Screen composable name ends with `Screen`; ViewModel name ends with `ViewModel`. ViewModels go in the same package as their screen.

## Decision flowchart

```
Does this action talk to the server?
├── No  → local hoisted state in the composable is fine. Stop here.
└── Yes → use the server-sync rule (#3).
         └── Does a matching ServerEvent already exist?
             ├── Yes → Repository subscribes in init; UI just reads its StateFlow.
             └── No  → add a new ServerEvent type (references/server_event_bus.md).
```

## Anti-patterns (do not do these)

- Business logic inside a `@Composable` function.
- `GlobalScope.launch` — always `viewModelScope` (or repository-scoped `SupervisorJob` for app-scoped caches).
- Raw `collectAsState()` instead of `collectAsStateWithLifecycle()`.
- `SharedFlow`/`StateFlow` for one-shot events (navigation, snackbars).
- Manual polling loops (`while (true) { delay(...); refetch() }`) — `ServerEventBus` is the push channel.
- A new public composable without a `@Preview`.
- A repository whose state is rendered by UI but which does not subscribe to its `ServerEvent`.

## Reference files (read on demand — do NOT load preemptively)

- `references/screen_template.md` — copy-paste skeleton: sealed `UiState` + `@HiltViewModel` + `Channel` events + `*Screen` composable wired to `SnackbarHost`.
- `references/server_sync_patterns.md` — three labeled recipes: (A) optimistic mutation + WS reconcile, (B) pessimistic destructive mutation, (C) fetch-only refresh. Read before writing any button-click handler that touches the server.
- `references/server_event_bus.md` — step-by-step for adding a new `ServerEvent` type and wiring it through a Repository. Read before introducing any new server-pushed entity.
- `references/testing.md` — Compose UI test + fake-Repository recipe. Read before writing `androidTest` for a screen.
