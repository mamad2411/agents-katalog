# AGENTS.md - AI Agent Guidelines for cTikTok

This document provides guidelines for AI coding agents working on this codebase.

## Project Overview

cTikTok is a full-stack application for sharing TikTok videos privately:
- **Backend**: Bun + Hono + Drizzle ORM + SQLite
- **iOS App**: SwiftUI with MVVM architecture
- **Distribution**: Docker (backend), AltStore (iOS)

## Repository Structure

```
backend/               # Bun/Node.js backend
  src/
    db/               # Drizzle ORM schema and migrations
    middleware/       # Auth middleware (JWT)
    routes/           # Hono HTTP routes
    services/         # Business logic (TikTok download, transcoding)
    utils/            # Helpers (config, ID generation)
    app.ts            # Hono app setup
    index.ts          # Server entry point

cTikTok/              # iOS application
  cTikTok/
    Models/           # Codable data models
    Services/         # API and caching services
    Shared/           # Constants and configuration
    Utilities/        # Keychain helper
    ViewModels/       # MVVM view models
    Views/            # SwiftUI views (organized by feature)
  ShareExtension/     # iOS share sheet extension
```

---

## Build & Run Commands

### Backend (Bun)

```bash
cd backend

# Development (with hot reload)
bun run dev

# Production
bun run start

# Database migrations
bun run db:generate    # Generate Drizzle migrations
bun run db:migrate     # Apply migrations
bun run db:studio      # Open Drizzle Studio GUI
```

### iOS (Xcode)

```bash
cd cTikTok

# Build for device (unsigned)
xcodebuild -project cTikTok.xcodeproj \
    -scheme cTikTok \
    -configuration Release \
    -sdk iphoneos \
    CODE_SIGN_IDENTITY="-" \
    CODE_SIGNING_REQUIRED=NO \
    build

# Build for simulator
xcodebuild -project cTikTok.xcodeproj \
    -scheme cTikTok \
    -destination 'platform=iOS Simulator,name=iPhone 15'
```

### Testing

No test framework is currently configured. When adding tests:
- Backend: Consider using Bun's built-in test runner (`bun test`)
- iOS: Use XCTest framework

---

## Code Style Guidelines

### TypeScript (Backend)

**Imports**
- Use ES modules (`import ... from`)
- Order: external packages, then internal modules
- Use named imports for clarity

```typescript
import { Hono } from 'hono';
import { z } from 'zod';
import { db } from '../db';
import { users, videos } from '../db/schema';
```

**Formatting**
- 2-space indentation
- Single quotes for strings
- No semicolons (Bun style)
- TypeScript strict mode enabled

**Types**
- Use Zod for runtime validation schemas
- Infer types from Drizzle schema: `typeof users.$inferSelect`
- Export types at bottom of schema files

**Naming**
- `camelCase` for variables and functions
- `PascalCase` for types and interfaces
- `SCREAMING_SNAKE_CASE` for constants
- Descriptive route handler names: `videosRoute`, `authRoute`

**Error Handling**
- Use try/catch with async/await
- Return consistent JSON error responses: `{ error: 'message' }`
- Use appropriate HTTP status codes (400, 401, 403, 404, 500)
- Log with context prefixes: `[Auth]`, `[Process]`, `[TikTok]`

```typescript
try {
  const result = await someOperation();
  if (!result.success) {
    return c.json({ error: result.error }, 400);
  }
} catch (error) {
  console.error('[Service] Error:', error);
  return c.json({ error: 'Internal server error' }, 500);
}
```

**Patterns**
- Hono middleware for auth: `videosRoute.use('*', authMiddleware)`
- Background processing with status updates
- Result objects: `{ success: boolean, error?: string }`

---

### Swift (iOS)

**Imports**
```swift
import Foundation
import SwiftUI
import AVFoundation
```

**Formatting**
- 4-space indentation
- Use `// MARK: -` comments for section organization
- Consistent brace style (same line)

**Types**
- `Codable` structs for API models
- `enum` for error cases with `LocalizedError`
- Use computed properties for derived values

**Naming**
- `camelCase` for properties and functions
- `PascalCase` for types, structs, enums
- `ViewModel` suffix for view models
- `View` suffix for SwiftUI views

**Architecture (MVVM)**
- `@StateObject` to own view models in views
- `@ObservableObject` for view models
- `@MainActor` for UI-related classes
- Singleton services: `APIService.shared`
- Actor for thread-safe caching

```swift
@MainActor
final class VideoFeedViewModel: ObservableObject {
    @Published var videos: [Video] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
}
```

**Error Handling**
- Custom `APIError` enum implementing `LocalizedError`
- async/await with do-catch
- Store errors in `@Published` properties for UI

```swift
enum APIError: Error, LocalizedError {
    case invalidURL
    case serverError(String)
    case unauthorized
    
    var errorDescription: String? {
        switch self { ... }
    }
}
```

---

## Database Schema

Using Drizzle ORM with SQLite. Key tables:
- `users` - User accounts with hashed passwords
- `videos` - Video/slideshow metadata and file paths
- `friendships` - Bidirectional friend relationships
- `friendRequests` - Pending friend requests
- `friendCodes` - Shareable codes for adding friends

Generate migrations after schema changes:
```bash
cd backend && bun run db:generate
```

---

## API Structure

All routes prefixed with `/api`:
- `/api/auth/*` - Authentication (register, login)
- `/api/videos/*` - Video CRUD and streaming
- `/api/friends/*` - Friend management

Auth: JWT Bearer token in `Authorization` header.

---

## Environment Variables

Copy `backend/.env.example` and configure:
- `JWT_SECRET` - Secret for JWT signing
- `DATABASE_URL` - SQLite database path
- `DATA_DIR` - Directory for video storage

---

## CI/CD

- `.github/workflows/build-ios.yml` - Builds iOS app, bumps version, deploys to AltStore
- `.github/workflows/deploy-backend.yml` - Deploys backend via Docker

---

## Key Dependencies

**Backend**
- `hono` - Web framework
- `drizzle-orm` - Database ORM
- `zod` - Schema validation
- `bcrypt` - Password hashing
- `jsonwebtoken` - JWT auth
- `@tobyg74/tiktok-api-dl` - TikTok downloader

**iOS**
- SwiftUI - UI framework
- AVFoundation - Video playback
- URLSession - Networking
