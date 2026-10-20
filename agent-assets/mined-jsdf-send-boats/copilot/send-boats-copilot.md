# send.boats - File Sharing Service

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap the Server Component

- `cd server`
- `npm install` -- takes 20 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- Create `.dev.vars` file with authentication credentials:
  ```
  BASIC_AUTH_USERNAME=admin
  BASIC_AUTH_PASSWORD=password
  VITE_DEV_URL=http://localhost:5173
  ```
- Initialize database schema: `npx wrangler d1 execute send-boats --local --file=schema.sql` -- takes 1-2 seconds.
- `npm run dev` -- starts in 10 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
- Server runs on http://0.0.0.0:8787 (accessible via http://127.0.0.1:8787 or http://localhost:8787)

### Authentication System

- **Web Interface**: Uses cookie-based authentication
  - Login page at `/looking-glass` with credentials from `.dev.vars`
  - Sessions stored in KV with 24-hour expiration
  - Logout at `/logout`
- **iOS App**: Uses HTTP basic authentication (same credentials)
- **Hybrid Detection**: Server automatically detects auth method via `Authorization` header
- **Environment-Aware**: Uses secure cookies only with HTTPS in production

### Test Server Functionality

- **Web browser**: Navigate to http://127.0.0.1:8787/, log in with `admin`/`password` at `/looking-glass`
- **Basic auth (iOS/curl)**: `curl -u "admin:password" http://127.0.0.1:8787/`
- Upload form: Access via web after login or `curl -u "admin:password" http://127.0.0.1:8787/upload-form`
- File list: Access via web after login or `curl -u "admin:password" http://127.0.0.1:8787/`
- Without auth, web users redirected to `/looking-glass`, API clients get 401 Unauthorized

### iOS Component

- **CANNOT BUILD ON LINUX**: iOS app requires macOS and Xcode. This environment is Linux.
- Located in `sendboats-ios/` directory
- Xcode project: `sendboats-ios/sendboats.xcodeproj`
- Includes ShareExtension for file sharing from other iOS apps
- Has UI tests in `sendboatsUITests/`

## Validation

### Server Validation Steps

ALWAYS run through these scenarios after making server changes:

1. Start development server: `cd server && npm run dev`
2. Test unauthenticated access returns 401: `curl -w "Status: %{http_code}\n" http://127.0.0.1:8787/`
3. Test authenticated file list: `curl -u "admin:password" -w "Status: %{http_code}\n" http://127.0.0.1:8787/`
4. Test upload form loads: `curl -u "admin:password" -w "Status: %{http_code}\n" http://127.0.0.1:8787/upload-form`
5. Verify HTML responses contain expected content (forms, file lists)

### iOS Validation Steps

- Cannot validate iOS builds in this environment (Linux)
- iOS testing requires macOS with Xcode installed
- ShareExtension setup instructions in `sendboats-ios/ShareExtension/README.md`

## Critical Timing and Cancellation Warnings

- **npm install**: 20 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- **npm run dev**: 10 seconds startup. NEVER CANCEL. Set timeout to 30+ seconds.
- **Database operations**: 1-2 seconds. Set timeout to 30+ seconds.
- **npm test**: Currently broken due to vitest configuration issues with prerendered page imports.

## Known Issues and Limitations

### Server Issues

- **Tests are broken**: npm test fails due to vitest configuration expecting wrangler.json instead of wrangler.toml, and prerendered page import issues.
- **No working linters**: No ESLint or other linters installed. Prettier config exists but prettier package not installed.
- **Database must be initialized**: First-time setup requires running schema.sql against local D1 database.

### Environment Limitations

- **iOS builds impossible**: This is a Linux environment. iOS development requires macOS.
- **No GitHub Actions**: No CI/CD workflows configured.

## Required Dependencies and URLs

### Server Prerequisites

- Node.js (current: v20.19.4)
- npm (current: v10.8.2)
- Wrangler CLI (current: 4.14.1, available via npx)

### Cloudflare Resources Required for Deployment

- R2 bucket for file storage
- D1 database for metadata
- KV namespace for rate limiting
- Durable Objects for access counting
- Account ID and authentication credentials

## Environment Configuration

### Development vs Production

- **Development**: Uses `wrangler.toml` `[env.dev]` section
  - No custom domain routes
  - Runs on `0.0.0.0:8787` locally
  - Uses `DEV_ORIGIN` variable for environment detection
  - Cookies use `SameSite=Lax` without `Secure` flag
- **Production**: Uses main `wrangler.toml` configuration
  - Custom domain: `send.boats`
  - HTTPS required
  - Cookies use `Secure` flag with `SameSite=Strict`

### Why request.url shows production hostname in dev

- Cloudflare Workers uses production hostname from `wrangler.toml` even in dev mode
- Must use `Host` header to get actual hostname being accessed (e.g., `127.0.0.1:8787`)
- **Always use `buildUrl()` or `getOriginUrl()` helpers from `src/helpers/url.ts`** instead of `new URL(path, request.url)`
- `DEV_ORIGIN` environment variable also indicates development mode

## Rendering System Architecture

### Static Compilation with Dynamic Variable Injection

The server uses a hybrid rendering approach combining Vite's static compilation with Cloudflare Workers' dynamic templating:

1. **Build Phase (Vite)**:

   - HTML prerendered pages in `server/prerendered pages/*.html` are compiled by Vite
   - CSS is processed with Tailwind/PostCSS and bundled
   - Output goes to `server/dist/` directory
   - Prerendered Pages contain placeholder variables like `{{FILENAME}}`, `{{FILE_ID}}`, `{{META_TAGS}}`

2. **Runtime Phase (Cloudflare Worker)**:
   - Worker sits in front of compiled assets via `[assets]` binding
   - Route handlers fetch prerendered pages from `env.ASSETS` (production) or Vite dev server (development)
   - `renderPage()` helper performs simple string replacement on placeholders
   - Worker serves fully-rendered HTML with dynamic data injected

**Key Files:**

- `vite.config.ts` - Defines which prerendered pages to build as entry points
- `src/helpers/prerendered page.ts` - Prerendered Page fetching and variable substitution logic
- `src/helpers/url.ts` - URL building utilities that handle dev vs prod hostname correctly
- `wrangler.toml` - Configures `[assets]` binding to `dist/` directory

### URL Resolution: Development vs Production

**Critical Difference in Link Generation:**

- **Development Mode** (`npm run dev`):

  - Vite's `absoluteUrlPlugin` transforms all asset URLs to absolute URLs pointing to `http://localhost:5173`
  - Example: `<link href="/src/styles/full-screen.css">` becomes `<link href="http://localhost:5173/src/styles/full-screen.css">`
  - This enables hot reloading while worker runs on separate port (8787)
  - **IMPORTANT**: Navigation links (like `/download/{{FILE_ID}}`) remain relative and are NOT rewritten
  - Only asset URLs (CSS, JS, images) are made absolute via regex patterns in the plugin

- **Production Mode**:
  - All URLs are relative
  - Worker serves both prerendered pages and assets from same origin via `env.ASSETS`
  - No special URL transformation needed

**Plugin Behavior** (`vite.config.ts`):

```javascript
// Only rewrites: <link href="...css">, <script src="...">, <img src="...">
// Does NOT rewrite: <a href="...">, <form action="...">, fetch() URLs
```

**Implications for Prerendered Page Development:**

- Always use relative URLs for navigation: `/download/{{FILE_ID}}`, not `{{BASE_URL}}/download/{{FILE_ID}}`
- Asset URLs (CSS/JS) can be relative; Vite handles them appropriately per environment
- Worker's `env.VITE_DEV_URL` controls whether prerendered pages come from dev server or built assets
- **CRITICAL**: When building URLs in handlers, use `buildUrl(path, request, env)` or `getOriginUrl(request, env)` from `src/helpers/url.ts` instead of `new URL(path, request.url)` because `request.url` has the wrong hostname in dev mode

**Common Bug: Image Sources Pointing to Worker Routes**

❌ **BROKEN in Development** (`full-image.html`):

```html
<img src="/download/{{FILE_ID}}" alt="{{FILENAME}}" />
```

- Vite's plugin rewrites to: `<img src="http://localhost:5173/download/{{FILE_ID}}">`
- Points to Vite dev server (port 5173), but route handler is on worker (port 8787)
- Results in 404 because Vite doesn't have the `/download/` route

✅ **CORRECT - Prerendered Page full URL in worker**:

```typescript
// In handler (e.g., full.ts):
import {buildUrl} from '../helpers/url';

const downloadUrl = buildUrl(`/download/${key}`, request, env);
html = await renderPage(
  'full-image',
  {
    FILENAME: escapeHtml(record.filename),
    META_TAGS: metaTags,
    DOWNLOAD_URL: downloadUrl, // Full URL built by worker with correct hostname
  },
  env
);
```

```html
<!-- In prerendered page: -->
<img src="{{DOWNLOAD_URL}}" alt="{{FILENAME}}" />
```

- Worker builds full URL: `http://127.0.0.1:8787/download/abc123`
- Vite plugin ignores it (already absolute)
- Works in both dev and production

### Prerendered Page HTML Blocking

The worker explicitly blocks direct access to HTML prerendered pages:

```typescript
if (pathname.endsWith('.html')) {
  return new Response('Not Found', {status: 404});
}
```

This ensures prerendered pages are only served through route handlers that inject dynamic data, never as raw static files.

## Project Structure

### Server (`server/`)

- `src/index.ts` - Main worker entry point
- `src/handlers/` - Request handlers (upload, download, list, etc.)
- `src/helpers/prerendered page.ts` - Prerendered Page fetching and variable substitution
- `src/helpers/` - Auth, rate limiting, other helpers
- `prerendered pages/*.html` - HTML prerendered pages with `{{VARIABLE}}` placeholders
- `src/styles/` - CSS source files processed by Vite
- `dist/` - Vite build output (prerendered pages + bundled assets)
- `schema.sql` - Database schema
- `vite.config.ts` - Static asset compilation configuration
- `wrangler.toml` - Cloudflare Workers configuration with `[assets]` binding
- `package.json` - Dependencies and scripts

### iOS (`sendboats-ios/`)

- `sendboats.xcodeproj` - Main Xcode project
- `sendboats/` - Main iOS app source
- `ShareExtension/` - Share extension for receiving files
- `SharedCode/` - Code shared between targets
- `sendboatsTests/` - Unit tests
- `sendboatsUITests/` - UI tests

## Common Commands Reference

### Development

```bash
# Server development
cd server
npm install
npm run dev  # Start local server

# Database setup (first time only)
npx wrangler d1 execute send-boats --local --file=schema.sql

# Deployment
npm run deploy  # Runs deploy-with-version.sh script
```

### Testing

```bash
# Server testing (currently broken)
cd server
npm test  # FAILS: vitest configuration issues

# Manual server validation
curl -u "admin:password" http://127.0.0.1:8787/
curl -u "admin:password" http://127.0.0.1:8787/upload-form
```

## Frequently Accessed Files

### Server Configuration

- `server/wrangler.toml` - Cloudflare Workers config with bindings
- `server/package.json` - Node.js dependencies and scripts
- `server/.dev.vars` - Local development environment variables (create manually)

### Key Source Files

- `server/src/index.ts` - Main request router
- `server/src/helpers/auth.ts` - Authentication logic
- `server/README.md` - Detailed setup and deployment instructions
- `sendboats-ios/ShareExtension/README.md` - iOS ShareExtension setup

Always validate your changes by running the development server and testing the endpoints manually before committing changes.
