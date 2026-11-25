# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project Overview

Real-time notification system using ASP.NET Core 8 + SignalR (backend) and TypeScript + Webpack (frontend). Broadcasts notifications to all connected clients with in-memory history (last 100). Three delivery mechanisms: in-tab SignalR, Browser Notification API, and Web Push via service worker.

## Build & Run Commands

```bash
# Backend
dotnet build                              # Build .NET project
dotnet run                                # Run on http://localhost:5094

# Frontend (run from ClientApp/)
npm install                               # Install deps (required on fresh clone)
npm run build                             # Webpack production build -> wwwroot/dist/bundle.js
npm run dev                               # Webpack watch mode (development)

# Full rebuild after TypeScript changes
cd ClientApp && npm run build && cd .. && dotnet run
```

## Testing

There are no automated tests. No test framework, linter, or formatter is configured. Manual verification only:

```bash
# Send a test notification
curl -X POST http://localhost:5094/api/notification \
  -H "Content-Type: application/json" \
  -d '{"message":"Test message","type":"success"}'

# Check history
curl http://localhost:5094/api/notification/history

# Health check
curl http://localhost:5094/api/notification/health
```

## Architecture

- **Target**: .NET 8 (`net8.0`). Do NOT use .NET 9+ APIs (`MapStaticAssets`, `WithStaticAssets`).
- **Root namespace**: `notification_app` (underscore, not PascalCase -- derived from hyphenated project name).
- **Services are Singletons**: `NotificationService`, `PushSubscriptionService`, `WebPushService` -- all registered as singletons in `Program.cs`. Changing lifetime breaks shared state.
- **Service registration order matters**: `PushSubscriptionService` -> `WebPushService` -> `NotificationService` (dependency chain).
- **No interfaces for app services**: Concrete types are injected directly. No `INotificationService` etc.
- **In-memory persistence**: `ConcurrentQueue<Notification>` -- data lost on restart.
- **SignalR event**: `ReceiveNotification` -- name must match on both frontend and backend.
- **Notification model**: `{ id, message, timestamp, type }` where type is `info | success | warning | error`.
- **CORS**: Wide open (`AllowAll`) -- development only.
- **Port**: 5094 (configured in `Properties/launchSettings.json`). Frontend uses `window.location.origin` dynamically.
- **Main UI**: `wwwroot/index.html` (static SPA). The `Pages/` directory contains scaffolded Razor Pages -- not the primary interface.
- **VAPID keys**: Development keys in `appsettings.json`. Never commit production keys.

### Key Files

| Path | Purpose |
|------|---------|
| `Program.cs` | DI registration, middleware pipeline, top-level statements |
| `Controllers/NotificationController.cs` | POST notifications, GET history/health |
| `Controllers/PushController.cs` | VAPID key, push subscribe/unsubscribe |
| `Hubs/NotificationHub.cs` | SignalR hub |
| `Services/NotificationService.cs` | Notification broadcast + history (singleton) |
| `Services/WebPushService.cs` | Web Push via VAPID |
| `Models/Notification.cs` | Notification POCO |
| `ClientApp/src/index.ts` | Frontend entry point (orchestration) |
| `ClientApp/src/signalr-client.ts` | SignalR connection management |
| `ClientApp/src/notification-ui.ts` | DOM rendering |
| `ClientApp/src/types.ts` | Shared interfaces and enums |
| `wwwroot/sw.js` | Service worker for push notifications (plain JS) |
| `wwwroot/shared-websocket-worker.js` | SharedWorker for cross-tab SignalR (plain JS) |

## C# Code Style

### Namespaces & Usings
- File-scoped namespaces (`namespace X;`), not block-scoped.
- Implicit usings enabled -- only write explicit usings for non-implicit ones.
- Ordering: framework (`Microsoft.*`, `System.*`) first, then project-internal.

### Naming
- **PascalCase**: classes, methods, properties, constants (`MaxHistorySize`).
- **camelCase**: local variables, parameters.
- **`_camelCase`**: private fields (`_notificationService`, `_logger`).
- **`Async` suffix**: on all async methods (`SendNotificationAsync`).
- No UPPER_SNAKE_CASE for constants.

### Types & Access
- Access modifiers always explicit (`public`, `private`).
- Nullable reference types enabled. Use `?` annotations, `??` coalescing, default to `string.Empty`.
- Return `IActionResult` / `Task<IActionResult>` from controllers (not generic `ActionResult<T>`).
- Return anonymous objects: `Ok(new { success = true })`, `BadRequest(new { error = "msg" })`.

### Patterns
- Constructor injection for all dependencies.
- `async Task` return type (never `async void`, never `ValueTask`).
- Direct `await` -- no `.Result`, `.GetAwaiter().GetResult()`, or `ConfigureAwait(false)`.
- Try/catch with generic `Exception`. Log error + return error response. No custom exception types.
- Guard clauses for input validation: `if (string.IsNullOrWhiteSpace(x)) return BadRequest(...)`.
- Structured logging with `ILogger<T>`: `_logger.LogInformation("Message: {Param}", param)` -- never string interpolation in log calls.

### Formatting
- Allman brace style (opening brace on its own line).
- 4-space indentation.
- One blank line between methods.
- DTOs/request classes defined at bottom of controller file, outside the controller class.

### Comments
- Single-line `//` only. No XML doc comments (`///`), no block comments.
- Spanish for domain logic, English for technical notes.

## TypeScript Code Style

### Imports & Exports
- Named imports only, no default imports: `import { Foo } from './foo';`.
- Namespace import for signalR: `import * as signalR from '@microsoft/signalr';`.
- External imports first, then internal. Relative paths with `./`, no `.ts` extension.
- Named exports at declaration: `export class Foo { }`. No default exports, no barrel files.

### Naming
- **PascalCase**: classes, interfaces, enums, enum members.
- **camelCase**: methods, variables, private fields (no `_` prefix).
- **UPPER_SNAKE_CASE**: module-level constants (`API_BASE_URL`, `HUB_URL`).
- **kebab-case**: file names (`signalr-client.ts`, `push-manager.ts`).
- No `I` prefix on interfaces.
- `get` prefix for getters: `getIsActive()`, `getConnectionState()`.
- `setup` prefix for initialization: `setupListeners()`, `setupEventHandlers()`.

### Types
- `interface` for data shapes, `enum` (string enums) for state sets. No `type` aliases.
- Union types inline for constrained values: `type: 'info' | 'success' | 'warning' | 'error'`.
- Nullable fields as explicit unions: `connection: signalR.HubConnection | null = null`.
- DOM elements: `document.getElementById('x') as HTMLButtonElement` with null guard.

### Patterns
- `async/await` exclusively in `.ts` files. `.then()` chains only in plain JS worker files (`sw.js`, `shared-websocket-worker.js`).
- One class per file. Entry point (`index.ts`) is procedural with standalone functions.
- Explicit `public`/`private` on all class members.
- Try/catch: `console.error('Message:', error)` + optional `alert()`. Return `null`/`false` on failure.
- Guard clauses: `if (!element) return;` after DOM queries.
- Callbacks via stored references: `onNotification(callback)` pattern.

### Formatting
- Single quotes for all strings.
- Semicolons always.
- No trailing commas.
- 4-space indentation.
- K&R brace style (opening brace on same line).
- Template literals for string interpolation.

### Comments
- Single-line `//` only. No JSDoc.
- Spanish for domain comments, English for technical/infrastructure.

## Critical Rules

1. **Never change service lifetimes** -- all app services must remain singletons.
2. **SignalR event name `ReceiveNotification`** must match on both sides.
3. **Rebuild frontend** after any TypeScript change -- it does not auto-serve `.ts` files.
4. **Do not use .NET 9+ APIs** -- project targets `net8.0`.
5. **Frontend uses `window.location.origin`** for API URLs -- no hardcoded ports in TypeScript.
6. **No linter/formatter configured** -- follow existing conventions manually.
7. **Comments in Spanish** for domain logic, English for technical infrastructure.
8. **Service registration order** in `Program.cs` must respect the dependency chain.
9. **VAPID keys** in `appsettings.json` are dev-only -- never commit production keys.
