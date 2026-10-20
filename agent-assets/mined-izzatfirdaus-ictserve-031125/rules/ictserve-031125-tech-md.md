# ICTServe - Technology Stack

**System**: ICTServe (iServe)  
**Version**: 3.5.0 (SemVer)  
**Architecture**: True Hybrid Architecture (Guest + Authenticated Staff + Admin)  
**Organization**: BPM MOTAC (Ministry of Tourism, Arts & Culture Malaysia)  
**Last Updated**: 1 December 2025

---

## Core Technologies

### Backend Framework

- **PHP**: 8.2.12 (Required minimum version)
- **Laravel**: 12.40.1 (February 2025 release)
- **Composer**: 2.x (Dependency management)

### Frontend Stack

- **Livewire**: 3.7.0 (Server-driven reactive framework)
- **Livewire Volt**: 1.10.1 (Single-file components)
- **Alpine.js**: 3.x (Lightweight JavaScript, bundled with Livewire)
- **Tailwind CSS**: 4.1.17 (Utility-first CSS framework with @theme config)
- **Vite**: 7.0.7 (Frontend build tool with HMR)

### Admin Panel

- **Filament**: 4.1.10 (Server-Driven UI framework)
- **Filament Forms**: Dynamic form builder
- **Filament Tables**: Data table components
- **Filament Notifications**: Toast notifications
- **Filament Widgets**: Dashboard widgets

### Database & Storage

- **MySQL**: 8.0 (Production database)
- **Redis**: 7.0 (Cache, Queue, and Reverb backend)
- **SQLite**: Development/testing database

## Real-Time & Broadcasting

- **Laravel Reverb**: 1.6.2 (Native Laravel WebSocket server)
- **Laravel Echo**: 2.2.6 (WebSocket client)
- **Pusher JS**: 8.x (WebSocket protocol)

## Authentication & Authorization

- **Laravel Breeze**: 2.3.8 (Authentication scaffolding & Self-Registration)
- **Spatie Laravel Permission**: 6.23 (Role-based access control)
- **Laravel Sanctum**: 4.0 (API token authentication) - v3.5.0
- **Laravel Socialite**: 5.x (Google Workspace SSO, optional) - v3.5.0
- **Google2FA**: 2.3 (Two-factor authentication for superuser)

## Observability & Audit (Dual System)

- **Compliance Audit**: `owen-it/laravel-auditing` v14.x (Field-level tracking)
- **Operational Log**: `spatie/laravel-activitylog` v4.x (User activity logging)
- **Laravel Telescope**: 5.x (System debugging, Superuser only)
- **Laravel Pulse**: 1.3.0 (Performance monitoring, Admin/Superuser) - v3.5.0

## Development Tools

- **Laravel Pint**: 1.26.0 (PSR-12 code formatting)
- **Larastan**: 3.8.0 (PHPStan for Laravel, Level 9)
- **PHPUnit**: 11.5.44 (Testing framework)
- **Laravel Prompts**: 0.3.8 (Interactive CLI prompts)
- **Playwright**: 1.56.1 (E2E browser testing)
- **Axe-core**: 4.11.0 (Accessibility testing)
- **ESLint**: 9.x (JavaScript linting)
- **Prettier**: 3.x (Code formatting)
- **Stylelint**: 16.x (CSS linting)

---

## Key Dependencies

### PHP Packages (composer.json)

#### Production Dependencies

```json
{
  "php": "^8.2.12",
  "aws/aws-sdk-php": "^3.363",
  "bacon/bacon-qr-code": "^3.0",
  "barryvdh/laravel-dompdf": "^3.1",
  "filament/filament": "4.1.10",
  "laravel/framework": "^12.40.1",
  "laravel/breeze": "^2.3.8",
  "laravel/mcp": "^0.3.4",
  "laravel/pulse": "^1.3.0",
  "laravel/reverb": "^1.6.2",
  "laravel/sanctum": "^4.0",
  "laravel/socialite": "^5.0",
  "laravel/telescope": "^5.0",
  "laravel/tinker": "^2.10.1",
  "league/commonmark": "^2.8",
  "livewire/livewire": "^3.7.0",
  "livewire/volt": "^1.10.1",
  "maatwebsite/excel": "^3.1",
  "owen-it/laravel-auditing": "^14.0",
  "pragmarx/google2fa-laravel": "^2.3",
  "pusher/pusher-php-server": "^7.0",
  "spatie/laravel-activitylog": "^4.0",
  "spatie/laravel-permission": "^6.23"
}
```

#### Development Dependencies

```json
{
  "barryvdh/laravel-ide-helper": "^3.6",
  "doctrine/dbal": "*",
  "fakerphp/faker": "^1.24",
  "larastan/larastan": "^3.8.0",
  "laravel/boost": "^1.8",
  "laravel/pail": "^1.2.2",
  "laravel/pint": "^1.26.0",
  "mockery/mockery": "^1.6",
  "nunomaduro/collision": "^8.6",
  "nunomaduro/phpinsights": "^2.11",
  "phpunit/phpunit": "^11.5.44"
}
```

### JavaScript Packages (package.json)

#### Development Dependencies

```json
{
  "@axe-core/playwright": "^4.11.0",
  "@playwright/test": "^1.56.1",
  "@tailwindcss/forms": "^0.5.2",
  "@tailwindcss/postcss": "^4.0.0",
  "@tailwindcss/typography": "^0.5.19",
  "@tailwindcss/vite": "^4.0.0",
  "@typescript-eslint/parser": "^8.46.3",
  "autoprefixer": "^10.4.2",
  "axe-core": "^4.11.0",
  "axios": "^1.11.0",
  "concurrently": "^9.0.1",
  "laravel-echo": "^2.2.6",
  "laravel-vite-plugin": "^2.0.0",
  "lightningcss": "^1.30.2",
  "playwright": "^1.56.1",
  "postcss": "^8.4.31",
  "pusher-js": "^8.4.0",
  "tailwindcss": "^4.1.17",
  "terser": "^5.44.0",
  "vite": "^7.0.7",
  "web-vitals": "^4.2.4"
}
```

## Package Purposes

### Core Laravel Packages

- **laravel/framework**: Core framework (v12.40.1)
- **laravel/tinker**: REPL for debugging
- **laravel/pulse**: Performance monitoring (v1.3.0, Admin/Superuser only)
- **laravel/reverb**: Native WebSocket server (v1.6.2)
- **laravel/mcp**: Model Context Protocol for AI agents (v0.3.4)

### Admin & UI

- **filament/filament**: Server-Driven UI admin panel framework (v4.1.10)
- **livewire/livewire**: Full-stack reactive components (v3.7.0)
- **livewire/volt**: Single-file component syntax (v1.10.1)

### Authentication & Authorization

- **laravel/breeze**: Authentication scaffolding (v2.3.8)
- **spatie/laravel-permission**: Role-based access control (v6.23)
- **laravel/sanctum**: API token authentication (v4.0) - v3.5.0
- **laravel/socialite**: Google Workspace SSO (v5.x, optional) - v3.5.0
- **pragmarx/google2fa-laravel**: Two-factor authentication (v2.3)

### Audit & Logging (Dual System)

- **owen-it/laravel-auditing**: Field-level audit trail for compliance (v14.x)
- **spatie/laravel-activitylog**: User activity logging for operations (v4.x)
- **laravel/telescope**: System debugging (v5.x, Superuser only)

### Data & Reports

- **maatwebsite/excel**: Excel import/export (v3.1)
- **barryvdh/laravel-dompdf**: PDF generation (v3.1)

### Real-Time & Broadcasting

- **pusher/pusher-php-server**: Pusher SDK (v7.0)
- **laravel-echo**: WebSocket client (v2.2.6)
- **pusher-js**: Pusher JavaScript client (v8.x)

### Development Tools

- **laravel/boost**: AI-assisted development (MCP, v1.8)
- **laravel/pail**: Real-time log viewer (v1.2.2)
- **laravel/pint**: Code style fixer PSR-12 (v1.26.0)
- **larastan/larastan**: Static analysis PHPStan Level 9 (v3.8.0)
- **barryvdh/laravel-ide-helper**: IDE autocomplete (v3.6)

### Testing

- **phpunit/phpunit**: PHP unit testing (v11.5.44)
- **mockery/mockery**: Mocking framework (v1.6)
- **@playwright/test**: E2E browser testing (v1.56.1)
- **@axe-core/playwright**: Accessibility testing (v4.11.0)

## Build Tools & Configuration

### Vite Configuration (vite.config.js)

```javascript
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
    ],
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    'vendor': ['axios', 'alpinejs'],
                    'echo': ['laravel-echo', 'pusher-js'],
                },
            },
        },
    },
});
```

### Tailwind CSS v4 Configuration (resources/css/app.css)

**Note**: Tailwind v4 uses CSS-first configuration via `@theme` directive instead of `tailwind.config.js`.

```css
@import "tailwindcss";

@theme {
    /* MyDS Color Tokens */
    --color-primary-500: oklch(0.55 0.15 250);
    --color-primary-600: oklch(0.48 0.15 250);
    --color-success: oklch(0.55 0.15 145);
    --color-warning: oklch(0.65 0.15 85);
    --color-danger: oklch(0.45 0.2 25);
    
    /* MyDS Typography */
    --font-heading: 'Poppins', system-ui, sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    
    /* MyDS Spacing */
    --space-4: 16px;
    --space-6: 24px;
    --space-8: 32px;
    
    /* MyDS Radius */
    --radius-m: 8px;
    --radius-l: 12px;
    
    /* MyDS Shadows */
    --shadow-card: 0px 2px 6px 0px rgba(0, 0, 0, 0.05), 0px 6px 24px 0px rgba(0, 0, 0, 0.05);
}
```

### PostCSS Configuration (postcss.config.js)

```javascript
export default {
    plugins: {
        '@tailwindcss/postcss': {},
        autoprefixer: {},
    },
};
```

## Development Commands

### Composer Scripts

```bash
# Development server with hot reload
composer run dev

# Run tests
composer run test

# Static analysis
composer run analyse
composer run analyse:save

# Code quality
composer run insights
composer run lint

# Laravel Boost MCP
composer run boost
composer run boost:install
composer run boost:update

# Setup project
composer run setup
```

### NPM Scripts

```bash
# Development
npm run dev              # Vite dev server with HMR
npm run build            # Production build

# E2E Testing
npm run test:e2e         # Run all E2E tests
npm run test:e2e:ui      # Playwright UI mode
npm run test:e2e:debug   # Debug mode
npm run test:e2e:helpdesk # Helpdesk module tests
npm run test:e2e:loan    # Loan module tests

# Accessibility Testing
npm run test:accessibility     # Run accessibility tests
npm run test:accessibility:all # Tests + report

# Code Quality
npm run lint:js          # ESLint JavaScript
npm run lint:css         # Stylelint CSS
npm run format           # Prettier formatting
npm run quality          # Run all quality checks
```

### Artisan Commands

```bash
# Development
php artisan serve        # Start dev server (port 8000)
php artisan queue:work   # Process queue jobs (Redis driver)
php artisan reverb:start # Start WebSocket server (port 8080)

# Database
php artisan migrate      # Run migrations
php artisan db:seed      # Seed database
php artisan migrate:fresh --seed # Fresh DB with seed

# v3.5.0 Specific Operations
php artisan ict:link-historical-submissions  # Link guest submissions to accounts
php artisan ict:setup-dual-audit            # Setup/Verify Dual Audit tables
php artisan ict:update-guest-counts         # Update guest submission counts

# Cache
php artisan config:cache # Cache config
php artisan route:cache  # Cache routes
php artisan view:cache   # Cache views
php artisan optimize     # Optimize all
php artisan optimize:clear # Clear all caches

# Debugging & Monitoring
php artisan tinker       # REPL
php artisan telescope:install # Install Telescope (Superuser only)
php artisan pulse:check  # Check Pulse configuration
php artisan pulse:work   # Process Pulse data

# Code Quality
php artisan pint         # Fix code style (PSR-12)
php artisan test         # Run PHPUnit tests
php artisan test --coverage # Run tests with coverage

# Laravel Boost
php artisan boost:mcp    # Start MCP server
php artisan boost:install # Install Boost
php artisan boost:update # Update Boost
```

## Environment Configuration

### Required Environment Variables

```env
# Application
APP_NAME=ICTServe
APP_ENV=local
APP_KEY=base64:...
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_LOCALE=en
APP_FALLBACK_LOCALE=en
APP_TIMEZONE=Asia/Kuala_Lumpur

# Database
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=ictserve
DB_USERNAME=root
DB_PASSWORD=

# Cache & Queue
CACHE_STORE=redis
QUEUE_CONNECTION=redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=null

# Mail
MAIL_MAILER=smtp
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@motac.gov.my
MAIL_FROM_NAME="${APP_NAME}"

# Broadcasting (Laravel Reverb)
BROADCAST_CONNECTION=reverb
REVERB_APP_ID=...
REVERB_APP_KEY=...
REVERB_APP_SECRET=...
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http

# Laravel Pulse (v3.5.0)
PULSE_ENABLED=true
PULSE_INGEST_DRIVER=database
PULSE_STORAGE_DRIVER=database

# Laravel Sanctum (v3.5.0)
SANCTUM_STATEFUL_DOMAINS=localhost,127.0.0.1
SANCTUM_TOKEN_EXPIRATION=30

# Google OAuth (Optional, v3.5.0)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI="${APP_URL}/auth/google/callback"

# AWS (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1

# Laravel Telescope (Superuser only)
TELESCOPE_ENABLED=true
TELESCOPE_STORAGE_DRIVER=database
```

## System Requirements

### Production Environment

- **PHP**: 8.2.12 or higher
- **MySQL**: 8.0 or higher
- **Redis**: 7.0 or higher (required for Queue, Cache, Reverb)
- **Node.js**: 20.x or higher (for asset builds)
- **Composer**: 2.x
- **Web Server**: Nginx 1.24+ or Apache 2.4+
- **SSL/TLS**: Certificate for HTTPS (required)

### Development Environment

- **Docker**: 20.x or higher (recommended)
- **Docker Compose**: 2.x or higher
- **PHP**: 8.2.12 with extensions: BCMath, Ctype, JSON, Mbstring, OpenSSL, PDO, Tokenizer, XML
- **Git**: 2.x or higher
- **Laragon**: 6.x (Windows alternative)

### Browser Support (WCAG 2.2 AA Compliant)

- **Chrome/Edge**: Latest 2 versions
- **Firefox**: Latest 2 versions
- **Safari**: Latest 2 versions
- **Mobile**: iOS Safari 14+, Chrome Android 90+

### PHP Extensions Required

- BCMath
- Ctype
- JSON
- Mbstring
- OpenSSL
- PDO (MySQL driver)
- Tokenizer
- XML
- GD or Imagick (for image processing)
- Redis extension (for Redis support)

## Performance Optimizations

### Backend

- **OPcache**: PHP opcode caching enabled
- **Redis**: Session, cache, and queue storage
- **Queue Workers**: Background job processing with Supervisor
- **Database Indexing**: Optimized queries with composite indexes
- **Eager Loading**: Prevent N+1 queries with `with()` and `load()`
- **Laravel Pulse**: Real-time performance monitoring (v3.5.0)
  - Slow query detection (>500ms threshold)
  - Queue job metrics tracking
  - Server health monitoring (CPU, memory, disk)
  - Cache hit/miss rate tracking

### Frontend

- **Vite**: Fast HMR and optimized builds with code splitting
- **Lazy Loading**: Dynamic imports for large components
- **Asset Optimization**: Minification, Brotli compression
- **Tailwind CSS JIT**: On-demand CSS compilation (v4.1.17)
- **Image Optimization**: WebP conversion, responsive images
- **CDN**: Static asset delivery (production)

### Core Web Vitals Targets

| Metric | Target | Description |
|--------|--------|-------------|
| **LCP** (Largest Contentful Paint) | <2.5s | Guest forms load time |
| **FID** (First Input Delay) | <100ms | Interaction responsiveness |
| **CLS** (Cumulative Layout Shift) | <0.1 | Visual stability |
| **Filament Dashboard Load** | <3s | Admin panel with caching |

## Security Features

### Application Security

- **CSRF Protection**: Laravel middleware for all forms
- **XSS Prevention**: Blade automatic escaping
- **SQL Injection**: Eloquent ORM with prepared statements
- **Rate Limiting**: 60 requests/minute for guest forms, 60 requests/minute for API
- **2FA**: Google Authenticator TOTP for superuser accounts
- **Password Hashing**: bcrypt with dynamic cost factor
- **API Token Authentication**: Laravel Sanctum with abilities and expiration (v3.5.0)
- **Google OAuth**: Domain-restricted SSO (@motac.gov.my only) (v3.5.0)

### Security Headers

```php
// SecurityHeadersMiddleware
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
```

### Encryption & Key Management

| Context | Algorithm | Key Size | Rotation |
|---------|-----------|----------|----------|
| **Data at Rest (Database)** | AES-GCM | 256-bit | Quarterly |
| **Data in Transit (HTTPS)** | TLS 1.3 | 256-bit | Auto (cert) |
| **Password Hashing** | bcrypt | Dynamic | Per change |
| **API Tokens (Sanctum)** | SHA-256 | 256-bit | 30-day expiry |
| **Status Tokens** | SHA-512 | 512-bit | 72-hour expiry |
| **Google OAuth** | OAuth 2.0 | - | Per session |

### Infrastructure Security

- **HTTPS**: SSL/TLS 1.3 encryption (required)
- **Firewall**: UFW/iptables with whitelist
- **Fail2Ban**: Brute force protection
- **Security Headers**: CSP, HSTS, X-Frame-Options
- **IP Blocking**: Malicious IP blacklist
- **File Upload Scanning**: ClamAV virus scanning

## Monitoring & Logging

### Application Monitoring

- **Laravel Pulse**: Real-time performance metrics (v1.3.0, Admin/Superuser only)
  - Slow query tracking (>500ms threshold)
  - Queue job success/failure rates
  - Request response times and patterns
  - Server health metrics (CPU, memory, disk)
  - Cache hit/miss rates
  - 7-day data retention with automatic pruning
- **Laravel Telescope**: Request debugging and monitoring (v5.x, Superuser only)
  - Full access to all features: requests, commands, jobs, exceptions, logs, queries, models, events, mail, notifications, cache, Redis
  - No restrictions for superuser role
- **Laravel Pail**: Real-time log streaming (v1.2.2)

### Error Tracking

- **Laravel Log**: File-based logging with daily rotation (14-day retention)
- **Sentry**: Error tracking (optional, production)
- **Bugsnag**: Exception monitoring (optional, production)

### Audit & Compliance Logging (Dual System)

- **owen-it/laravel-auditing**: Field-level audit trail for compliance (v14.x)
  - Tracks all model changes (old/new values)
  - 7-year retention for PDPA compliance
  - IP address hashing for privacy
- **spatie/laravel-activitylog**: User activity logging for operations (v4.x)
  - Tracks user actions (login, logout, form submissions, approvals)
  - Used for dashboard widgets and operational reports

### Performance Monitoring

- **Laravel Debugbar**: Development profiling (disabled in production)
- **Clockwork**: Request profiling (development only)
- **New Relic**: APM (optional, production)

---

## True Hybrid Architecture v3.5.0

### Architecture Overview

ICTServe implements a **True Hybrid Architecture** that supports three access modes:

1. **Guest Mode**: Quick access without login (token-based status tracking)
2. **Authenticated Staff Mode**: Full dashboard with submission history and profile management
3. **Admin/Superuser Mode**: System administration via Filament panel

### User Roles & Capabilities

| Role | Access Level | Capabilities |
|------|--------------|--------------|
| **Guest** | Public forms | Submit tickets/loans, track status via token |
| **Staff** | Authenticated dashboard | View own history, edit profile, submit as authenticated, link guest submissions |
| **Admin** | Filament panel | Manage tickets, loans, assets, users, assign tickets |
| **Superuser** | Full system access | Configuration, audit logs, user management, Laravel Telescope |

### Self-Registration Flow

1. Staff visits `/register` with `@motac.gov.my` email
2. System validates email domain
3. Email verification sent (24-hour expiry)
4. User verifies email via signed URL
5. Account activated with `staff` role
6. Optional: Link previous guest submissions

### Flexible Login System

- **Email**: Full email address (`ahmad.ibrahim@motac.gov.my`)
- **Username**: Short username extracted from email (`ahmad.ibrahim`)
- **Backend**: `extractUsernameFromEmail()` method in User model
- **Security**: Generic error messages (no user enumeration)

### Account Linking Service

**Purpose**: Link historical guest submissions to new staff accounts

**Features**:

- Find unlinked submissions by email
- Atomic transaction for data integrity
- Update `user_id` on helpdesk_tickets and loan_applications
- Track linked submission count

**Implementation**: `AccountLinkingService` with `findUnlinkedSubmissions()` and `linkSubmissions()` methods

### Database Schema (Hybrid Support)

**Key Fields**:

- `users.staff_number`: Staff identification
- `users.google_id`: Google OAuth ID (nullable, v3.5.0)
- `helpdesk_tickets.user_id`: Nullable FK (NULL for guests)
- `loan_applications.user_id`: Nullable FK (NULL for guests)
- `helpdesk_tickets.status_token_hash`: SHA-512 for guest tracking
- `loan_applications.approval_token_hash`: SHA-512 for email approvals

---

## API Authentication (Laravel Sanctum v4.0)

### Token-Based Authentication

**Purpose**: Secure API access for future mobile apps and external integrations

**Features**:

- Token generation with configurable abilities
- Token expiration management (default: 30 days)
- Usage logging for audit trail
- Rate limiting (60 requests/minute)

### Token Abilities

| Ability | Description |
|---------|-------------|
| `read:tickets` | View helpdesk tickets |
| `write:tickets` | Create/update helpdesk tickets |
| `read:loans` | View loan applications |
| `write:loans` | Create/update loan applications |
| `admin:all` | Full admin access |

### API Endpoints

```http
GET  /api/tickets       # List tickets (requires read:tickets)
POST /api/tickets       # Create ticket (requires write:tickets)
GET  /api/loans         # List loans (requires read:loans)
POST /api/loans         # Create loan (requires write:loans)
```

### Token Management

- **Creation**: Via Filament admin panel (Admin/Superuser only)
- **Revocation**: Individual token or all user tokens
- **Monitoring**: `api_token_usage_logs` table tracks all API calls

---

## Google Workspace SSO (Optional, v3.5.0)

### OAuth 2.0 Integration

**Provider**: Laravel Socialite v5.x
**Domain Restriction**: `@motac.gov.my` only
**Flow**: Authorization Code Grant

### Features

- **Auto-Account Creation**: New users automatically registered
- **Account Linking**: Existing users linked to Google account
- **Fallback**: Traditional Laravel Breeze login always available
- **Audit Logging**: All OAuth events logged for compliance

### Configuration

```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

### Routes

```http
GET /auth/google          # Initiate OAuth flow
GET /auth/google/callback # Handle OAuth callback
```

---

## MyGovEA & MyDS Compliance

### Design System Alignment

ICTServe follows **Malaysia Government Design System (MyDS) v2025.2** and **MyGovEA Design Principles**.

### Typography System

- **Headings**: Poppins (400/500/600 weights)
- **Body**: Inter (400/500/600 weights)
- **Monospace**: JetBrains Mono

### Color Tokens (MyDS)

```css
/* Primary Colors */
--color-primary-500: oklch(0.55 0.15 250);
--color-primary-600: oklch(0.48 0.15 250);

/* Semantic Colors */
--color-success: oklch(0.55 0.15 145);
--color-warning: oklch(0.65 0.15 85);
--color-danger: oklch(0.45 0.2 25);
```

### Spacing System (MyDS)

| Size | Value | Usage |
|------|-------|-------|
| 1 | 4px | Micro spacing |
| 2 | 8px | Button groups |
| 4 | 16px | General spacing |
| 6 | 24px | Sub-sections |
| 8 | 32px | Main sections |

### Radius System (MyDS)

| Name | Size | Usage |
|------|------|-------|
| xs | 4px | Context menu items |
| s | 6px | Small buttons |
| m | 8px | Buttons, CTAs |
| l | 12px | Content cards |
| full | 9999px | Avatars, badges |

### WCAG 2.2 AA Compliance

- **Color Contrast**: 4.5:1 for text, 3:1 for UI components
- **Keyboard Navigat Tested with NVDA and JAWS

---

## Deployment Architecture

### Development Environment

```yaml
# docker-compose.yml
services:
  app:
    image: php:8.2-fpm
    volumes:
      - ./:/var/www/html
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: ictserve
  
  redis:
    image: redis:7.0
  
  reverb:
    command: php artisan reverb:start
```

### Production Stack

```text
┌─────────────────────────────────────┐
│     Load Balancer (Nginx)           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Application Servers (PHP-FPM 8.2)  │
│  - Laravel 12.40.1                   │
│  - Livewire 3.7.0                    │
│  - Filament 4.1.10                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Database (MySQL 8.0)                │
│  - Master-Slave Replication          │
└──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Cache & Queue (Redis 7.0)           │
│  - Session Storage                   │
│  - Queue Backend                     │
│  - Reverb Backend                    │
└──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  WebSocket Server (Reverb 1.6.2)    │
│  - Real-time Notifications           │
└──────────────────────────────────────┘
```

### Deployment Checklist

- [ ] Run `composer install --no-dev --optimize-autoloader`
- [ ] Run `npm run build`
- [ ] Run `php artisan config:cache`
- [ ] Run `php artisan route:cache`
- [ ] Run `php artisan view:cache`
- [ ] Run `php artisan migrate --force`
- [ ] Configure Supervisor for queue workers
- [ ] Start Laravel Reverb service
- [ ] Configure SSL/TLS certificates
- [ ] Set up automated backups
- [ ] Configure monitoring (Pulse, Telescope)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.5.0 | 1 Dec 2025 | Laravel Pulse, Sanctum API, Google SSO, Responsible Officer, Accessory Tracking |
| 3.4.0 | 29 Nov 2025 | Hybrid Architecture: Staff role, Dashboard, Account Linking |
| 3.3.0 | 29 Nov 2025 | Guest-First Architecture standardization |
| 3.2.0 | 29 Nov 2025 | Technology stack version updates |
| 3.1.0 | 29 Nov 2025 | Laravel 12, Livewire 3, Filament 4, Reverb |
| 3.0.0 | 31 Oct 2025 | Internal-only architecture transition |

---

## References

- **D00_SYSTEM_OVERVIEW.md** - System overview and architecture
- **D01_SYSTEM_DEVELOPMENT_PLAN.md** - Development plan and methodology
- **D11_TECHNICAL_DESIGN_DOCUMENTATION.md** - Technical design details
- **D13_UI_UX_FRONTEND_FRAMEWORK.md** - Frontend framework and MyDS compliance
- **Laravel 12 Documentation**: <https://laravel.com/docs/12.x>
- **Livewire 3 Documentation**: <https://livewire.laravel.com/docs/3.x>
- **Filament 4 Documentation**: <https://filamentphp.com/docs/4.x>
- **MyDS Design System**: <https://design.digital.gov.my/en>
- **WCAG 2.2 Guidelines**: <https://www.w3.org/TR/WCAG22/>
