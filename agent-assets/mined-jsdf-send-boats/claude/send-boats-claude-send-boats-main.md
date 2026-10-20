# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a file sharing service with two main components:
- **iOS native app** (`sendboats-ios/`) - SwiftUI-based client for uploading and sharing files
- **Cloudflare Workers server** (`server/`) - Backend API handling uploads, storage, and file management

## Development Commands

### iOS App (sendboats-ios/)

**Build and Test:**
```bash
cd sendboats-ios
# Build main app
xcodebuild -scheme sendboats -configuration Debug
# Build share extension
xcodebuild -scheme ShareExtension -configuration Debug
# Run tests
xcodebuild test -scheme sendboats
# Build for release
xcodebuild -scheme sendboats -configuration Release
```

**Open in Xcode:**
```bash
open sendboats-ios/sendboats.xcodeproj
```

### Server (server/)

**Development:**
```bash
cd server
npm install
npm run dev        # Local development
npm run deploy     # Deploy to Cloudflare Workers
wrangler deploy    # Alternative deploy command
```

**Database and Storage Setup:**
```bash
wrangler r2 bucket create your-bucket-name
wrangler d1 create your-database-name
wrangler d1 execute your-database-name --file=schema.sql
wrangler kv:namespace create "RATE_LIMIT"
```

## Architecture

### iOS App Structure

**Multi-Target Architecture:**
- **sendboats** - Main application target
- **ShareExtension** - iOS Share Extension for system-wide file sharing
- **SharedCode** - Common code shared between both targets

**Key Patterns:**
- **MVVM with Combine**: `UploadViewModel` as central state manager using `@ObservableObject`
- **SwiftUI + UIKit**: Modern SwiftUI views with UIKit integration for system features
- **App Groups**: Data sharing between main app and extension via `group.jsdf.sendboats`
- **URL Scheme Communication**: Share extension opens main app via `sendboats://` URL scheme

**State Management Flow:**
```
fileSelection → previewAndUpload → uploading → success
```

**Core Services:**
- `APIClient.swift` - Network layer handling server communication
- `UploadService.swift` - File upload logic with progress tracking
- `ConfigurationManager.swift` - Persistent settings via App Groups
- `VideoThumbnailGenerator.swift` - Media processing utilities

### Server Architecture

**Cloudflare Workers Stack:**
- **Workers** - Main application logic
- **R2** - File storage
- **D1** - SQLite database for metadata
- **KV** - Rate limiting storage
- **Durable Objects** - Access counting

**Rendering Pipeline:**

The server uses a two-phase rendering system:

1. **Static Compilation (Vite Build)**
   - HTML prerendered pages in `server/prerendered pages/*.html` are processed by Vite
   - CSS compiled with Tailwind/PostCSS and bundled
   - Built assets output to `server/dist/`
   - Prerendered Pages preserve placeholder variables: `{{FILENAME}}`, `{{FILE_ID}}`, `{{META_TAGS}}`

2. **Dynamic Injection (Cloudflare Worker Runtime)**
   - Worker intercepts route requests before serving static assets
   - Handlers fetch pre-compiled prerendered pages from `env.ASSETS` (prod) or Vite dev server (dev)
   - `renderPage()` performs string substitution on placeholders with dynamic data
   - Fully-rendered HTML returned to client

**URL Resolution in Development vs Production:**

Critical difference affects how links work:

- **Development Mode** (`npm run dev` starts both Vite on :5173 and Wrangler on :8787):
  - Vite's `absoluteUrlPlugin` transforms asset URLs to absolute: `http://localhost:5173/...`
  - Example: `<link href="/src/styles/full-screen.css">` → `<link href="http://localhost:5173/src/styles/full-screen.css">`
  - Enables hot reloading across different ports
  - **Only affects**: `<link href="...css">`, `<script src="...">`, `<img src="...">`
  - **Does NOT affect**: Navigation links like `<a href="/download/{{FILE_ID}}">` or API endpoints
  - Navigation links remain relative and resolve through the worker on port 8787

- **Production**:
  - All URLs relative
  - Single origin serves everything
  - No URL transformation

**Prerendered Page Development Guidelines:**
- Use relative URLs for all navigation and API calls: `/download/{{FILE_ID}}`
- Never hardcode absolute URLs or base paths
- Asset links (CSS/JS) are automatically handled by Vite per environment
- Worker blocks direct `.html` access; prerendered pages only served through handlers with data injection
- **CRITICAL**: Always use `buildUrl(path, request, env)` or `getOriginUrl(request, env)` from `src/helpers/url.ts` instead of `new URL(path, request.url)` because `request.url` contains the production hostname even in dev mode

**IMPORTANT: Image/Media Sources Pointing to Worker Routes**

When an `<img>` or `<video>` source points to a worker route (not a static asset), you must build the full URL in the worker and prerendered page it in:

❌ **BROKEN** - Relative path in `<img src>` pointing to worker route:
```html
<!-- full-image.html - BROKEN IN DEV -->
<img src="/download/{{FILE_ID}}" alt="{{FILENAME}}" />
```
Problem: Vite's plugin rewrites to `http://localhost:5173/download/...` (port 5173), but the download handler is on the worker (port 8787). Results in 404.

✅ **CORRECT** - Worker builds full URL using helper:
```typescript
// In handler (full.ts):
import { buildUrl } from '../helpers/url';

const downloadUrl = buildUrl(`/download/${key}`, request, env);
html = await renderPage('full-image', {
  DOWNLOAD_URL: downloadUrl,  // e.g., "http://127.0.0.1:8787/download/abc123"
  FILENAME: escapeHtml(record.filename),
}, env);
```
```html
<!-- Prerendered Page: -->
<img src="{{DOWNLOAD_URL}}" alt="{{FILENAME}}" />
```
Result: The `buildUrl()` helper uses the `Host` header to get the correct hostname (127.0.0.1:8787 in dev, send.boats in prod). Vite plugin ignores already-absolute URLs. Works in both dev and production.

## Testing Framework

**iOS Testing:**
- **Unit Tests**: Swift Testing framework (`sendboatsTests/`)
- **UI Tests**: XCTest framework (`sendboatsUITests/`)
- **Build Monitoring**: Automated error tracking with `xclogparser` generating JSON reports

**Test Execution:**
```bash
# Run all tests
xcodebuild test -scheme sendboats
# Run specific test target
xcodebuild test -scheme sendboats -only-testing:sendboatsTests
```

## Share Extension Integration

The iOS app includes a comprehensive Share Extension that:
- Accepts all file types via `TRUEPREDICATE` activation rule
- Processes files through the same upload pipeline as main app
- Uses App Groups for configuration sharing
- Returns to main app via URL scheme after successful upload

**Setup Requirements:**
- App Groups entitlement: `group.jsdf.sendboats`
- URL scheme handler: `sendboats://`
- Share Extension Info.plist configuration for file type support

## Configuration

**iOS App:**
- Server settings persisted via `ConfigurationManager` using App Groups
- Configuration shared between main app and share extension
- Default server endpoint configurable in app settings

**Server:**
- `wrangler.toml` contains Cloudflare Workers configuration
- Environment variables for authentication (`AUTH_USERNAME`, `AUTH_PASSWORD`)
- Dynamic hostname detection (no hardcoded URLs)

## File Upload Flow

1. **File Selection**: Document picker or photo library (main app) / system share (extension)
2. **Preview Generation**: Video thumbnail creation for media files
3. **Upload**: Multipart upload to Cloudflare Workers endpoint
4. **Response Processing**: Extract view URL and full URL from server response
5. **Success Display**: Show URLs with copy/share functionality

## Key Features

- Native iOS file upload with progress tracking
- Video preview generation and thumbnail extraction
- System-wide sharing via iOS Share Extension
- URL copying and native iOS share sheet integration
- Persistent server configuration
- Cross-target code sharing between main app and extension