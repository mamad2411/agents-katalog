# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-time notification system MVP using ASP.NET Core 8, SignalR for WebSocket communication, and TypeScript with Webpack for the frontend. The system broadcasts notifications to all connected clients with in-memory history persistence (last 100 notifications).

## Key Architecture Decisions

### Backend Architecture
- **NotificationService is a Singleton**: Registered in Program.cs:14 as singleton to maintain shared in-memory notification history across all requests
- **In-memory persistence**: Uses `ConcurrentQueue<Notification>` to store history - data is lost on server restart
- **Broadcast only**: All notifications go to all connected clients via `Clients.All.SendAsync()`
- **CORS is wide open**: `AllowAll` policy permits any origin (development only - must be restricted for production)

### SignalR Flow
1. Client connects to `/notificationHub` endpoint
2. On connection, client fetches history via `GET /api/notification/history`
3. Client listens for `ReceiveNotification` events from hub
4. When notification is sent via `POST /api/notification`, controller → service → hub context → all clients

### Frontend Build Process
- TypeScript compiled via Webpack to `wwwroot/dist/bundle.js`
- Webpack output configured to parent directory: `path.resolve(__dirname, '../wwwroot/dist')`
- Must rebuild frontend after TypeScript changes for changes to take effect

## Common Commands

### Development Workflow
```bash
# Build and run backend
dotnet build
dotnet run

# Build frontend (production)
cd ClientApp
npm run build

# Build frontend with watch mode (development)
cd ClientApp
npm run dev
```

### After modifying TypeScript files
```bash
cd ClientApp && npm run build && cd .. && dotnet run
```

### Testing the system
```bash
# Send test notification via API
curl -X POST http://localhost:5094/api/notification \
  -H "Content-Type: application/json" \
  -d '{"message":"Test message","type":"success"}'

# Get notification history
curl http://localhost:5094/api/notification/history

# Access web interface
open http://localhost:5094/index.html
```

## Critical Implementation Details

### NotificationService Lifecycle
- Service must remain singleton - changing to scoped/transient will break history sharing
- `ConcurrentQueue` used for thread-safety since service is accessed by multiple requests
- History automatically trims to 100 items in `SendNotificationAsync` method

### Frontend-Backend Contract
- SignalR event name: `ReceiveNotification` (must match on both sides)
- Notification model: `{ id, message, timestamp, type }`
- Types: `info`, `success`, `warning`, `error`
- History loaded before SignalR connection established in `index.ts:33`

### .NET 8 Compatibility
- Project targets `net8.0` (notification-app.csproj:4)
- Does NOT use .NET 9+ APIs like `MapStaticAssets()` or `WithStaticAssets()`
- Uses standard `UseStaticFiles()` and `MapRazorPages()` instead

## Port Configuration
Default port is 5094 (configured in Properties/launchSettings.json). If changing port, update:
1. launchSettings.json
2. Frontend connection URL is dynamic via `window.location.origin` so no changes needed in TypeScript

## Extending the System

### Adding user-specific notifications
Would require:
1. Authentication system
2. User identification in hub connections (`Context.UserIdentifier`)
3. Change from `Clients.All` to `Clients.User(userId)`
4. Update NotificationService to track userId with notifications

### Adding database persistence
Would require:
1. Add Entity Framework Core package
2. Create DbContext with Notifications DbSet
3. Change NotificationService from singleton to scoped
4. Replace ConcurrentQueue with database queries
5. Add migrations and update database

### Adding notification types/categories
Notification.Type is already a string field, just add new type values and corresponding CSS classes in wwwroot/index.html styles.
