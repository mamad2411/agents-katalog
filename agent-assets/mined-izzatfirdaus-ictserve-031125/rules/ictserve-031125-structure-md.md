# ICTServe - Project Structure

**Version:** 3.5.0 (True Hybrid Architecture)  
**Last Updated:** December 1, 2025  
**Architecture:** True Hybrid (Guest + Authenticated Staff + Admin Panel)

## Directory Organization

### Core Application (`app/`)

```text
app/
├── Console/          # Artisan commands
│   └── Commands/     # Custom commands (auto-registered in Laravel 12)
├── Contracts/        # Interface definitions
├── Enums/           # Enumeration classes (Status, Priority, Role, etc.)
├── Events/          # Event classes for broadcasting
├── Exceptions/      # Custom exception handlers
├── Filament/        # Filament 4.1.10 admin panel resources
│   ├── Pages/       # Custom admin pages (SLA, Email Templates, Unified Audit)
│   ├── Resources/   # CRUD resources (Assets, Tickets, Loans, Users)
│   └── Widgets/     # Dashboard widgets (Stats, Performance, Activity)
├── Http/
│   ├── Controllers/ # Route controllers
│   │   ├── Api/     # API endpoints (Laravel Sanctum)
│   │   ├── Auth/    # Authentication (Breeze + Google SSO)
│   │   ├── Guest/   # Guest form controllers
│   │   └── Staff/   # Staff dashboard controllers
│   ├── Middleware/  # Custom middleware (minimal in Laravel 12)
│   └── Requests/    # Form request validation
├── Jobs/            # Queue jobs (emails, notifications, reports)
├── Listeners/       # Event listeners
├── Livewire/        # Livewire 3.7.0 components
│   ├── Guest/       # Guest forms (Helpdesk, Loan)
│   ├── Staff/       # Authenticated staff components (Dashboard, Profile)
│   └── Admin/       # Admin-specific components
├── Mail/            # Mailable classes (WCAG 2.2 AA compliant)
├── Models/          # Eloquent models
│   ├── User.php     # User model with hybrid support
│   ├── HelpdeskTicket.php  # Nullable user_id FK
│   ├── LoanApplication.php # Nullable user_id FK
│   ├── Audit.php    # Compliance audit (owen-it)
│   └── Activity.php # Operations log (spatie)
├── Notifications/   # Notification classes (Email, Database, WebSocket)
├── Observers/       # Model observers
├── Policies/        # Authorization policies (RBAC)
├── Providers/       # Service providers
│   ├── AppServiceProvider.php
│   ├── FilamentServiceProvider.php
│   └── PulseServiceProvider.php  # Laravel Pulse access control
├── Rules/           # Custom validation rules
├── Services/        # Business logic services
│   ├── HelpdeskService.php
│   ├── LoanService.php
│   ├── ApprovalService.php
│   ├── RegistrationService.php
│   ├── AccountLinkingService.php
│   ├── TokenService.php
│   ├── NotificationPreferenceService.php
│   ├── ResponsibleOfficerService.php
│   ├── AccessoryTrackingService.php
│   ├── ApiTokenService.php
│   ├── GoogleSsoService.php
│   ├── PerformanceMonitoringService.php
│   ├── AccessibilityComplianceService.php
│   ├── SLAManagementService.php
│   └── StandardsComplianceChecker.php
├── Traits/          # Reusable traits
│   ├── HasAuditTrail.php
│   ├── HasActivityLog.php
│   └── HasNotificationPreferences.php
└── View/            # View composers
```text

### Database (`database/`)

```text
database/
├── factories/       # Model factories for testing
│   ├── UserFactory.php
│   ├── HelpdeskTicketFactory.php
│   ├── LoanApplicationFactory.php
│   └── AssetFactory.php
├── migrations/      # Database schema migrations
│   ├── *_create_users_table.php  # True Hybrid: nullable user_id FK support
│   ├── *_create_helpdesk_tickets_table.php
│   ├── *_create_loan_applications_table.php
│   ├── *_create_loan_transaction_accessories_table.php  # v3.5.0
│   ├── *_create_personal_access_tokens_table.php  # Laravel Sanctum
│   ├── *_create_pulse_tables.php  # Laravel Pulse
│   ├── *_create_audits_table.php  # owen-it/laravel-auditing
│   └── *_create_activity_log_table.php  # spatie/laravel-activitylog
├── seeders/         # Database seeders
│   ├── DatabaseSeeder.php
│   ├── RolePermissionSeeder.php  # Spatie Permission roles
│   ├── DivisionSeeder.php
│   ├── AssetCategorySeeder.php
│   └── UserNotificationPreferenceSeeder.php
└── data/           # Static data files
```text

### Resources (`resources/`)

```text
resources/
├── css/
│   └── app.css      # Tailwind CSS entry point
├── js/
│   ├── app.js       # Main JavaScript entry
│   ├── bootstrap.js # Laravel Echo, Axios setup
│   └── performance-optimizations.js
├── lang/            # Translation files
│   ├── en/          # English translations
│   └── ms/          # Bahasa Melayu translations
└── views/
    ├── components/  # Blade components
    ├── filament/    # Filament view overrides
    ├── livewire/    # Livewire component views
    ├── layouts/     # Layout templates
    └── pages/       # Page templates
```text

### Routes (`routes/`)

```text
routes/
├── web.php          # Web routes (helpdesk, assets)
├── api.php          # API routes
├── auth.php         # Authentication routes
├── channels.php     # Broadcasting channels
├── console.php      # Artisan commands
└── ai.php           # AI/MCP integration routes
```text

### Configuration (`config/`)

```text
config/
├── app.php          # Application config (locale, timezone)
├── audit.php        # Laravel Auditing config
├── auth.php         # Authentication config
├── database.php     # Database connections
├── filesystems.php  # Storage config
├── mail.php         # Email config
├── permission.php   # Spatie Permission config
├── queue.php        # Queue config
└── reverb.php       # WebSocket config
```text

### Tests (`tests/`)

```text
tests/
├── Feature/         # Feature tests (HTTP, database)
│   ├── Helpdesk/
│   ├── Loan/
│   └── Admin/
├── Unit/            # Unit tests (services, models)
├── Browser/         # Laravel Dusk tests
├── e2e/             # Playwright E2E tests
│   ├── helpdesk.module.spec.ts
│   ├── loan.module.spec.ts
│   └── accessibility.comprehensive.spec.ts
└── TestCase.php     # Base test case
```text

### Documentation (`docs/`)

```text
docs/
├── D00_SYSTEM_OVERVIEW.md  # v3.5.0 - True Hybrid Architecture
├── D01_SYSTEM_DEVELOPMENT_PLAN.md  # v3.5.0
├── D02_BUSINESS_REQUIREMENTS_SPECIFICATION.md  # v3.5.0
├── D03_SOFTWARE_REQUIREMENTS_SPECIFICATION.md  # v3.5.0 - 38 Requirements
├── D04_SOFTWARE_DESIGN_DOCUMENT.md  # v3.5.0 - 100 Correctness Properties
├── D05_DATA_MIGRATION_PLAN.md  # v3.5.0
├── D06_DATA_MIGRATION_SPECIFICATION.md  # v3.5.0
├── D07_SYSTEM_INTEGRATION_PLAN.md  # v3.5.0
├── D08_SYSTEM_INTEGRATION_SPECIFICATION.md  # v3.5.0
├── D09_DATABASE_DOCUMENTATION.md  # v3.5.0 - Dual Audit System
├── D10_SOURCE_CODE_DOCUMENTATION.md  # v3.5.0
├── D11_TECHNICAL_DESIGN_DOCUMENTATION.md  # v3.5.0
├── D12_UI_UX_DESIGN_GUIDE.md  # v3.5.0 - MOTAC Branding
├── D13_UI_UX_FRONTEND_FRAMEWORK.md  # v3.5.0
├── D14_UI_UX_STYLE_GUIDE.md  # v3.5.0
├── D15_LANGUAGE_MS_EN.md  # Bilingual localization
├── D16_BROADCASTING_SETUP.md  # Laravel Reverb WebSocket
├── D17_QUEUE_MANAGEMENT_HORIZON.md  # Laravel Horizon
├── helpdesk_form_to_model.md  # Helpdesk data mapping
├── loan_form_to_model.md  # Asset loan data mapping
├── broadcasting-setup.md  # Real-time setup guide
├── email-notification-system.md  # Email notifications
├── performance-optimization-report.md  # Performance audit
├── admin-guide/     # Administrator documentation
├── user-manual/     # End-user guides
├── security/        # Security documentation
├── frontend/        # Frontend compliance guides
│   ├── accessibility-guidelines.md
│   ├── color-contrast-accessibility.md
│   ├── core-web-vitals-testing-guide.md
│   └── filament-admin-interface-compliance.md
└── reference/       # Technical references
```text

### Scripts (`scripts/`)

```text
scripts/
├── docker/          # Docker helper scripts
│   ├── start-dev.ps1
│   ├── stop-dev.ps1
│   └── init-dev.ps1
├── laragon/         # Laragon setup scripts
│   └── setup-laragon.ps1
└── tools/           # Development utilities
```text

## Architectural Patterns (v3.5.0 True Hybrid Architecture)

### 1. True Hybrid Architecture

**Three Access Modes:**

1. **Guest Mode**: Quick access without login (nullable user_id FK)
2. **Authenticated Staff**: Self-registration with @motac.gov.my email
3. **Admin Panel**: Filament 4.1.10 for admin/superuser roles

**Data Association:**

- Guest submissions: `user_id = NULL`, tracked via email
- Staff submissions: `user_id = {user.id}`, auto-fill from profile
- Optional account linking: Retrospectively link guest submissions to new staff account

### 2. MVC with Service Layer

```text
Request → Controller → Service → Model → Database
                    ↓
                Response
```text

- **Controllers**: Handle HTTP requests, delegate to services
- **Services**: Business logic, complex operations (HelpdeskService, LoanService, etc.)
- **Models**: Data access, relationships, scopes (nullable user_id FK support)
- **Repositories**: Optional abstraction for data access

### 3. Livewire Component Architecture (v3.7.0)

```text
Blade View ↔ Livewire Component ↔ Service Layer ↔ Models
     ↓              ↓                    ↓
  Alpine.js    Real-time Updates    Dual Audit
                (Reverb 1.6.2)      (owen-it + spatie)
```text

- **Volt Components**: Single-file components for simple interactions (Volt 1.10.1)
- **Class-based Components**: Complex forms and data tables
- **Hybrid Logic**: `Auth::check()` for auto-fill vs manual input
- **Real-time**: WebSocket integration via Laravel Reverb + Echo

### 4. Filament Admin Panel (v4.1.10)

```text
Filament Resource → Form/Table Schema → Model → Database
        ↓                                  ↓
   Authorization (Policies)          Dual Audit
                                    (owen-it + spatie)
```text

- **Resources**: CRUD interfaces for models (Tickets, Loans, Assets, Users)
- **Pages**: Custom admin pages (SLA Management, Email Templates, Unified Audit Log)
- **Widgets**: Dashboard statistics (Performance, Activity, Stats)
- **Actions**: Bulk operations, exports (CSV, PDF)
- **Access Control**: admin + superuser roles only
- **Laravel Telescope**: superuser-only debugging (unrestricted access)

### 5. Event-Driven Architecture

```text
Action → Event → Listener → Job (Queue) → Notification
                                ↓              ↓
                           Dual Audit    Multi-Channel
                        (owen-it + spatie)  (Email, DB, WebSocket)
```text

- **Events**: Ticket created, loan approved, asset overdue, etc.
- **Listeners**: Trigger jobs, send notifications, log activities
- **Jobs**: Queued email sending, report generation, performance monitoring
- **Broadcasting**: Real-time UI updates via Laravel Reverb (WebSocket)
- **Notifications**: Email, Database, WebSocket (multi-channel based on user preferences)

## Core Components (v3.5.0)

### 1. Helpdesk Module (True Hybrid)

**Models**:

- `HelpdeskTicket` (nullable user_id FK, form_reference_code)
- `HelpdeskComment`, `HelpdeskAttachment`

**Controllers**: `HelpdeskController` (guest + staff routes)  
**Livewire**:

- `Guest\HelpdeskForm` (hybrid with Auth::check() logic)
- `Staff\TicketList`, `Staff\TicketDetail`

**Services**:

- `HelpdeskService` (hybrid user_id logic)
- `SLAManagementService`
- `TokenService` (status token generation)

**Features**:

- Guest mode: Manual input, status token tracking
- Staff mode: Auto-fill from profile, dashboard history
- Form reference code: PK.(S).MOTAC.07.(L1)

### 2. Asset Loan Module (True Hybrid)

**Models**:

- `LoanApplication` (nullable user_id FK, form_reference_code, responsible_officer fields)
- `LoanItem`, `LoanTransaction`, `LoanTransactionAccessory` (v3.5.0)
- `LoanApproval`

**Controllers**: `LoanController` (guest + staff routes)  
**Livewire**:

- `Guest\LoanApplicationWizard` (hybrid with Auth::check() logic)
- `Staff\LoanHistory`, `Staff\LoanDetail`

**Services**:

- `LoanService` (hybrid user_id logic, asset availability)
- `ApprovalService` (email-based approval workflow)
- `ResponsibleOfficerService` (v3.5.0)
- `AccessoryTrackingService` (v3.5.0)

**Features**:

- Guest mode: Manual input, email approval, status token
- Staff mode: Auto-fill, dashboard history, account linking
- Responsible Officer: Separate designation from Applicant
- Accessory Tracking: Check-out/check-in with discrepancy detection
- Form reference code: PK.(S).MOTAC.07.(L3)

### 3. Admin Panel (Filament 4.1.10)

**Resources**:

- `HelpdeskTicketResource` (SLA indicators, assignment)
- `LoanApplicationResource` (approval chain, check-out/check-in with accessories)
- `AssetResource`, `UserResource`

**Pages**:

- `Dashboard` (performance widgets)
- `UnifiedAuditLog` (dual audit system view)
- `SLAThresholdManagement` (superuser config)
- `EmailTemplateManagement` (superuser config)

**Widgets**:

- `HelpdeskStatsWidget`, `LoanStatsWidget`
- `PerformanceMetricsWidget` (Laravel Pulse)
- `SystemHealthWidget` (CPU, memory, disk)
- `RecentActivityWidget` (real-time via Reverb)

**Access Control**:

- admin: Operational management (tickets, loans, assets)
- superuser: System config, audit review, Laravel Telescope access

### 4. Staff Dashboard & Profile

**Components**:

- `Staff\Dashboard` (submission history, notifications)
- `Staff\ProfileSettings` (edit profile, notification preferences)
- `Staff\AccountLinking` (link historical guest submissions)

**Services**:

- `AccountLinkingService` (find and link unlinked submissions)
- `NotificationPreferenceService` (email frequency, in-app toggle)

**Features**:

- Combined history: Helpdesk tickets + Asset loans
- Optional linking: Retrospectively link past guest submissions
- Notification preferences: Immediate, daily, weekly digest

### 5. Authentication & Authorization (True Hybrid)

**Models**:

- `User` (role enum: staff, admin, superuser)
- Spatie Permission: `Role`, `Permission`

**Authentication**:

- Laravel Breeze 2.3.8 (email/password)
- Self-registration (@motac.gov.my validation)
- Flexible login (email OR username)
- Google Workspace SSO (optional, v3.5.0)

**Middleware**: `auth`, `role`, `permission`, `signed` (approval links)  
**Policies**: `TicketPolicy`, `AssetPolicy`, `UserPolicy`, `AuditPolicy`

**Features**:

- Self-registration with email verification
- Flexible login: `user@motac.gov.my` OR `user`
- 2FA (TOTP) for superuser accounts
- Google OAuth 2.0 (optional, @motac.gov.my only)

### 6. Dual Audit System (v3.5.0)

**Compliance Audit** (owen-it/laravel-auditing v14.x):

- Field-level tracking (old/new values)
- 7-year retention for PDPA compliance
- Immutable records (no updates/deletes)
- IP address hashing for privacy

**Operations Log** (spatie/laravel-activitylog v4.x):

- User activity logging
- Dashboard and operational reports
- Subject and causer tracking
- Flexible retention policies

**Unified View**:

- `UnifiedAuditLog` Filament page (superuser only)
- Combined filtering and export (CSV, PDF)
- Real-time updates via Reverb

### 7. Performance Monitoring (Laravel Pulse v1.3.0)

**Features**:

- Slow query detection (>500ms threshold)
- Queue job metrics (success/failure rates)
- Request response times
- Server health (CPU, memory, disk)
- Cache hit/miss rates

**Access Control**:

- `/pulse` route restricted to admin + superuser
- 7-day data retention with automatic pruning
- Real-time dashboard updates

**Integration**:

- `PerformanceMetricsWidget` in Filament dashboard
- `SystemHealthWidget` with color-coded indicators
- Alert triggering for performance thresholds

### 8. API Authentication (Laravel Sanctum v4.0)

**Features**:

- Token-based API authentication
- Configurable abilities: `read:tickets`, `write:tickets`, `read:loans`, `write:loans`, `admin:all`
- Token expiration management (default: 30 days)
- Usage logging for audit trail
- Rate limiting: 60 requests/minute

**Components**:

- `ApiTokenService` (create, revoke, validate tokens)
- `ApiTokenResource` (Filament management interface)
- `ApiTokenUsageLog` model (audit trail)
- API routes in `routes/api.php`

### 9. Compliance Services

**Services**:

- `AccessibilityComplianceService`: WCAG 2.2 AA validation
- `StandardsComplianceChecker`: Code quality checks
- `PerformanceMonitoringService`: Core Web Vitals tracking
- `AuditService`: Dual audit system coordination

## Data Flow Examples (v3.5.0 True Hybrid)

### Helpdesk Ticket Submission (Hybrid Flow)

**Guest Mode:**

```text
1. Guest accesses /helpdesk/create (no login)
2. Livewire component loads (Auth::check() = false)
3. Manual input: name, email, phone, division, grade
4. reCAPTCHA validation
5. Form validation (Form Request)
6. HelpdeskService creates ticket (user_id = NULL)
7. Status token generated (SHA-512 hash)
8. Dual audit: owen-it (field-level) + spatie (activity)
9. Event dispatched (TicketCreated)
10. Listener queues job (SendTicketNotification)
11. Job sends email with status token link
12. Broadcast to admin panel via Reverb (WebSocket)
```text

**Staff Mode:**

```text
1. Staff logs in via Laravel Breeze
2. Accesses /helpdesk/create (Auth::check() = true)
3. Livewire auto-fills: name, email, phone from user profile
4. Staff completes: category, priority, description
5. Form validation (Form Request)
6. HelpdeskService creates ticket (user_id = {user.id})
7. Dual audit: owen-it + spatie (with user_id)
8. Event dispatched (TicketCreated)
9. Listener queues job (SendTicketNotification)
10. Job sends email confirmation
11. Ticket appears in Staff Dashboard
12. Broadcast to admin panel via Reverb
```text

### Asset Loan Application (Hybrid Flow with Responsible Officer)

**Guest Mode:**

```text
1. Guest accesses /loan/apply (no login)
2. LoanApplicationWizard loads (Auth::check() = false)
3. Step 1: Manual input applicant details
4. Step 2: Responsible Officer section
   - Checkbox: "Applicant is same as Responsible Officer" (default: checked)
   - If unchecked: Manual input RO name, grade, phone
5. Step 3: Asset selection with real-time availability check
6. Step 4: Date range selection with conflict detection
7. Step 5: Purpose and acknowledgement
8. Form validation (Form Request)
9. LoanService creates application (user_id = NULL)
10. ResponsibleOfficerService stores RO data
11. Approval token generated (signed URL, 72h expiry)
12. Dual audit: owen-it + spatie
13. Event dispatched (LoanRequested)
14. Email sent to approver (Grade 41+) with signed link
15. Email confirmation sent to applicant with status token
```text

**Staff Mode:**

```text
1. Staff logs in and accesses /loan/apply
2. LoanApplicationWizard loads (Auth::check() = true)
3. Step 1: Auto-fill applicant details from profile
4. Step 2: Responsible Officer section (same logic)
5. Steps 3-5: Same as guest mode
6. LoanService creates application (user_id = {user.id})
7. ResponsibleOfficerService stores RO data
8. Approval workflow same as guest mode
9. Application appears in Staff Dashboard
10. Optional: Link to previous guest submissions
```text

**Approval Flow (Email-Based, No Login Required):**

```text
1. Approver receives email with signed URL
2. Clicks link → ApprovalController validates token
3. Displays application summary with RO details
4. Approver selects APPROVE/REJECT + remarks
5. ApprovalService records decision (IP hash, timestamp)
6. Dual audit: owen-it + spatie
7. Event dispatched (LoanApproved/LoanRejected)
8. Email sent to applicant (guest or staff)
9. If approved: Asset status updated to RESERVED
10. Broadcast to admin panel via Reverb
```text

**Check-Out Flow (Admin Panel with Accessory Tracking):**

```text
1. Admin accesses LoanApplicationResource in Filament
2. Selects approved application → Check-Out action
3. Accessory checklist displayed:
   - Power Adapter, Bag, Mouse, USB Cable, HDMI/VGA Cable, Remote, Others
4. Admin marks each as "Included" or "Not Included"
5. Condition notes for each accessory
6. Custom name for "Others" category
7. AccessoryTrackingService stores check-out data
8. LoanTransaction created (transaction_type = CHECK_OUT)
9. Asset status updated to ON_LOAN
10. Dual audit: owen-it + spatie
11. Email sent to borrower with return date reminder
```text

**Check-In Flow (Admin Panel with Discrepancy Detection):**

```text
1. Admin accesses active loan → Check-In action
2. Accessory checklist pre-populated from check-out
3. Admin verifies each accessory:
   - Present/Missing
   - Condition notes
4. System highlights discrepancies (missing items, condition changes)
5. If damage reported: Condition notes + photos
6. AccessoryTrackingService stores check-in data
7. LoanTransaction created (transaction_type = CHECK_IN)
8. Asset status updated to AVAILABLE
9. If damage: Automatic maintenance ticket created
10. Dual audit: owen-it + spatie
11. Email sent to borrower (confirmation)
```text

### Admin Report Generation (Unified Audit)

```text
1. Superuser accesses UnifiedAuditLog page (Filament)
2. Selects filters: date range, user, action type, entity
3. Tabs: All, Compliance (owen-it), Activity (spatie)
4. Service queries both audit tables
5. Data merged and sorted by timestamp
6. Export action: CSV or PDF
7. ReportService formats data
8. PDF generated (DomPDF) with MOTAC letterhead
9. File streamed to browser
10. Audit log entry created (export action)
```text

### Performance Monitoring (Laravel Pulse)

```text
1. Admin/Superuser accesses /pulse dashboard
2. PulseServiceProvider validates role (admin/superuser only)
3. Dashboard displays:
   - Slow queries (>500ms threshold)
   - Queue job metrics (success/failure rates)
   - Request response times
   - Server health (CPU, memory, disk)
4. Real-time updates via Reverb (WebSocket)
5. PerformanceMonitoringService checks thresholds
6. If threshold exceeded: Alert triggered
7. Notification sent to superuser
8. Automatic data pruning (7-day retention)
```text

### API Authentication (Laravel Sanctum)

```text
1. Admin creates API token via ApiTokenResource (Filament)
2. Selects abilities: read:tickets, write:tickets, etc.
3. Sets expiration (default: 30 days)
4. ApiTokenService generates token
5. Token displayed once (copy to clipboard)
6. External system uses token in Authorization header
7. API request: GET /api/v1/tickets
8. Sanctum middleware validates token
9. Checks token abilities (read:tickets required)
10. ApiTokenUsageLog records request (audit trail)
11. Rate limiter checks (60 requests/minute)
12. Response returned with ticket data
```text

## Integration Points

### External Services

- **Email**: SMTP (Mailtrap for dev, production SMTP)
- **Storage**: Local filesystem, S3-compatible (optional)
- **Queue**: Redis (production), database (fallback)
- **Broadcasting**: Laravel Reverb (WebSocket server)

### Internal APIs

- **REST API**: `/api/helpdesk`, `/api/assets`
- **GraphQL**: Not implemented (future consideration)
- **MCP**: Laravel Boost for AI agent integration

### Third-Party Packages

- **Filament**: Admin panel framework
- **Livewire**: Frontend reactivity
- **Spatie Permission**: RBAC
- **Laravel Auditing**: Activity logs
- **DomPDF**: PDF generation
- **Maatwebsite Excel**: Excel exports

## Deployment Structure

### Docker Containers

- **app**: PHP-FPM + Laravel application
- **web**: Nginx web server
- **db**: MySQL 8.0 database
- **redis**: Redis cache and queue
- **reverb**: WebSocket server

### Environment Files

- `.env`: Main configuration
- `.env.docker`: Docker-specific settings
- `.env.testing`: Test environment
- `.env.staging`: Staging environment

## Key Design Decisions (v3.5.0)

### Architecture Decisions

1. **True Hybrid Architecture**: Flexible access (guest OR authenticated staff) with nullable user_id FK
2. **Self-Registration**: Staff can register independently with @motac.gov.my email validation
3. **Optional Account Linking**: Retrospectively link historical guest submissions to new staff accounts
4. **Dual Audit System**: Compliance (owen-it) + Operations (spatie) for comprehensive tracking
5. **Email-Based Approval**: Token-based workflow without requiring approver login

### Technology Decisions

6. **Livewire 3.7.0 over Vue/React**: Reduced complexity, server-side rendering, real-time reactivity
7. **Filament 4.1.10 for Admin**: Rapid development, Laravel-native, extensive ecosystem
8. **Laravel Reverb 1.6.2**: Native WebSocket server for real-time notifications
9. **Laravel Pulse 1.3.0**: Built-in performance monitoring without external dependencies
10. **Laravel Sanctum 4.0**: Token-based API authentication for future integrations

### Development Decisions

11. **Service Layer**: Separation of concerns, testability, reusable business logic
12. **Queue Jobs (Redis)**: Async processing, better UX, scalable background tasks
13. **Bilingual Support**: Bahasa Melayu (primary), English (fallback) per D15
14. **WCAG 2.2 AA**: Accessibility compliance from start (4.5:1 text, 3:1 UI contrast)
15. **Docker**: Consistent dev/prod environments, easy deployment
16. **MCP Integration**: AI-assisted development with Laravel Boost

### Security Decisions

17. **Rate Limiting**: 60 requests/minute for guest forms, API endpoints
18. **reCAPTCHA Enterprise**: Invisible mode for spam prevention
19. **Token Hashing**: SHA-512 for status/approval tokens
20. **2FA (TOTP)**: Required for superuser accounts
21. **IP Hashing**: Privacy-compliant audit logging

### Compliance Decisions

22. **PDPA 2010**: 7-year audit retention, data minimization, consent tracking
23. **ISO 8000**: Data quality standards, validation rules
24. **MyGOV Digital Service Standards v2.1.0**: Government digital service compliance
25. **MOTAC Branding**: Official logos, color palette, form reference codes
26. **MyGovEA Design Principles**: Citizen-centric, minimalist, error prevention

### Performance Decisions

27. **Core Web Vitals**: LCP <2.5s, FID <100ms, CLS <0.1
28. **Lazy Loading**: Images, components, dashboard widgets
29. **Query Optimization**: Eager loading, indexes, caching
30. **Asset Optimization**: Vite 7.0.7, Tailwind CSS 4.1.17 JIT, WebP images

---

## v3.5.0 True Hybrid Architecture Features

### 1. User Access Modes

**Guest Mode:**

- No login required
- Manual input for all fields
- Status token for tracking (SHA-512 hash)
- Email notifications only
- `user_id = NULL` in database

**Authenticated Staff Mode:**

- Self-registration with @motac.gov.my email
- Email verification required
- Flexible login: full email OR username
- Auto-fill from user profile
- Dashboard with submission history
- Notification preferences (email frequency, in-app)
- Optional account linking for historical submissions
- `user_id = {user.id}` in database

**Admin/Superuser Mode:**

- Full system access via Filament 4.1.10
- Role-based permissions (admin vs superuser)
- Laravel Telescope access (superuser only, unrestricted)
- Laravel Pulse dashboard (admin + superuser)
- Unified Audit Log (superuser only)
- SLA and email template management (superuser only)

### 2. Database Schema (True Hybrid Support)

**Key Tables:**

```sql
-- Users table with hybrid support
users (
  id, name, email, phone, department_id, grade, staff_number,
  role ENUM('staff', 'admin', 'superuser'),
  google_id, -- v3.5.0 Google OAuth
  locale ENUM('ms', 'en'),
  notify_email_frequency ENUM('immediate', 'daily', 'weekly'),
  notify_in_app BOOLEAN,
  guest_submissions_linked INTEGER,
  last_login_at, last_login_ip,
  two_factor_secret, two_factor_confirmed_at
)

-- Helpdesk tickets with nullable user_id FK
helpdesk_tickets (
  id, ticket_number, form_reference_code,
  user_id NULLABLE FK → users.id,  -- NULL = Guest, NOT NULL = Staff
  submitter_name, submitter_email, submitter_phone,
  submitter_division_code, submitter_grade,
  category, priority, description, asset_tag,
  status, assigned_admin_id, sla_due_at,
  status_token_hash, -- SHA-512 for guest tracking
  created_at, updated_at
)

-- Loan applications with nullable user_id FK and Responsible Officer
loan_applications (
  id, reference_number, form_reference_code,
  user_id NULLABLE FK → users.id,  -- NULL = Guest, NOT NULL = Staff
  applicant_name, applicant_email, applicant_phone,
  applicant_division_code, applicant_grade,
  is_applicant_responsible BOOLEAN,  -- v3.5.0
  responsible_officer_name,          -- v3.5.0
  responsible_officer_grade,         -- v3.5.0
  responsible_officer_phone,         -- v3.5.0
  responsible_officer_acknowledgement BOOLEAN,  -- v3.5.0
  start_date, end_date, purpose,
  status, approval_token_hash, status_token_hash,
  created_at, updated_at
)

-- Loan transaction accessories (v3.5.0)
loan_transaction_accessories (
  id, loan_transaction_id FK,
  accessory_type ENUM('POWER_ADAPTER', 'BAG', 'MOUSE', 'USB_CABLE', 
                      'HDMI_VGA_CABLE', 'REMOTE', 'OTHERS'),
  accessory_name VARCHAR(100),  -- For OTHERS category
  present_at_checkout BOOLEAN,
  present_at_checkin BOOLEAN,
  condition_notes TEXT,
  created_at, updated_at
)

-- Dual Audit System
audits (  -- owen-it/laravel-auditing (compliance)
  id, user_type, user_id, event, auditable_type, auditable_id,
  old_values JSON, new_values JSON,
  url, ip_address, user_agent,
  created_at  -- Immutable, no updates/deletes
)

activity_log (  -- spatie/laravel-activitylog (operations)
  id, log_name, description, subject_type, subject_id,
  causer_type, causer_id, event,
  properties JSON,
  created_at, updated_at
)

-- Laravel Pulse (v3.5.0)
pulse_entries (
  id, timestamp, type, key, value, created_at
)

pulse_aggregates (
  id, bucket, period, type, key, aggregate, value, count
)

pulse_values (
  id, timestamp, type, key, value
)

-- Laravel Sanctum (v3.5.0)
personal_access_tokens (
  id, tokenable_type, tokenable_id, name, token,
  abilities JSON, last_used_at, expires_at,
  created_at, updated_at
)

api_token_usage_logs (
  id, personal_access_token_id FK, user_id FK,
  action, endpoint, ip_hash, user_agent, response_status,
  created_at
)
```text

### 3. Service Layer Architecture

**Core Services:**

```php
// Hybrid data association
HelpdeskService::createTicket(array $data, ?User $user)
  → user_id = $user?->id ?? null

LoanService::createApplication(array $data, ?User $user)
  → user_id = $user?->id ?? null

// Self-registration
RegistrationService::register(array $data)
  → validateEmailDomain('@motac.gov.my')
  → sendVerificationEmail()

// Account linking
AccountLinkingService::findUnlinkedSubmissions(string $email)
  → helpdesk_tickets WHERE user_id IS NULL AND submitter_email = $email
  → loan_applications WHERE user_id IS NULL AND applicant_email = $email

AccountLinkingService::linkSubmissions(User $user, array $submissionIds)
  → UPDATE helpdesk_tickets SET user_id = $user->id WHERE id IN (...)
  → UPDATE loan_applications SET user_id = $user->id WHERE id IN (...)
  → INCREMENT users.guest_submissions_linked

// Token management
TokenService::generateStatusToken()
  → random_bytes(32) → hash('sha512', $token)

TokenService::generateApprovalToken(LoanApplication $loan)
  → URL::signedRoute('loan.approve', ['loan' => $loan->id], now()->addHours(72))

// Responsible Officer (v3.5.0)
ResponsibleOfficerService::setResponsibleOfficer(LoanApplication $loan, array $data)
  → is_applicant_responsible = false
  → responsible_officer_name, grade, phone

ResponsibleOfficerService::copyApplicantAsResponsibleOfficer(LoanApplication $loan)
  → is_applicant_responsible = true
  → Copy applicant data to RO fields

// Accessory Tracking (v3.5.0)
AccessoryTrackingService::recordCheckoutAccessories(LoanTransaction $transaction, array $accessories)
  → Create LoanTransactionAccessory records

AccessoryTrackingService::getAccessoryDiscrepancies(LoanTransaction $checkoutTx, LoanTransaction $checkinTx)
  → Compare checkout vs checkin accessories
  → Highlight missing items, condition changes

// API Token Management (v3.5.0)
ApiTokenService::createToken(User $user, string $name, array $abilities, ?Carbon $expiresAt)
  → PersonalAccessToken::create()
  → Return plain-text token (shown once)

ApiTokenService::logTokenUsage(PersonalAccessToken $token, Request $request, int $status)
  → ApiTokenUsageLog::create()

// Performance Monitoring (v3.5.0)
PerformanceMonitoringService::getSlowQueries(int $threshold = 500)
  → Query pulse_entries WHERE type = 'slow_query' AND value > $threshold

PerformanceMonitoringService::checkPerformanceThresholds()
  → If slow queries > 100/hour → triggerPerformanceAlert()

// Google SSO (v3.5.0)
GoogleSsoService::handleGoogleCallback(string $code)
  → validateGoogleDomain('@motac.gov.my')
  → findOrCreateUser() OR linkGoogleAccount()
```text

### 4. Livewire Component Patterns

**Hybrid Form Logic:**

```php
// resources/views/livewire/helpdesk/ticket-form.blade.php
class TicketForm extends Component
{
    public function mount()
    {
        if (Auth::check()) {
            // Auto-fill from user profile
            $this->name = Auth::user()->name;
            $this->email = Auth::user()->email;
            $this->phone = Auth::user()->phone;
            $this->division = Auth::user()->department->code;
            $this->grade = Auth::user()->grade;
        }
        // Else: Manual input (guest mode)
    }

    public function submit()
    {
        $this->validate();
        
        $ticket = $this->helpdeskService->createTicket(
            $this->all(),
            Auth::user()  // null if guest
        );
        
        if (Auth::check()) {
            return redirect()->route('staff.dashboard')
                ->with('success', __('Ticket created successfully'));
        } else {
            return redirect()->route('helpdesk.status', ['token' => $ticket->status_token])
                ->with('success', __('Ticket submitted. Save this link to check status.'));
        }
    }
}
```text

**Responsible Officer Section (v3.5.0):**

```php
// resources/views/livewire/loan/application-wizard.blade.php
class LoanApplicationWizard extends Component
{
    public bool $isApplicantResponsible = true;
    public ?string $responsibleOfficerName = null;
    public ?string $responsibleOfficerGrade = null;
    public ?string $responsibleOfficerPhone = null;

    public function updatedIsApplicantResponsible($value)
    {
        if ($value) {
            // Copy applicant data to RO fields
            $this->responsibleOfficerName = $this->applicantName;
            $this->responsibleOfficerGrade = $this->applicantGrade;
            $this->responsibleOfficerPhone = $this->applicantPhone;
        } else {
            // Clear RO fields for manual input
            $this->responsibleOfficerName = null;
            $this->responsibleOfficerGrade = null;
            $this->responsibleOfficerPhone = null;
        }
    }
}
```text

### 5. Filament Resource Patterns

**Unified Audit Log (Superuser Only):**

```php
// app/Filament/Pages/UnifiedAuditLog.php
class UnifiedAuditLog extends Page
{
    protected static ?string $navigationIcon = 'heroicon-o-shield-check';
    protected static ?string $navigationGroup = 'System';
    
    public static function shouldRegisterNavigation(): bool
    {
        return Auth::user()?->hasRole('superuser') ?? false;
    }
    
    public function getUnifiedRecords(): Collection
    {
        $audits = Audit::with('user')->latest()->limit(100)->get()
            ->map(fn($audit) => [
                'source' => 'compliance',
                'created_at' => $audit->created_at,
                'user_name' => $audit->user?->name ?? 'System',
                'action' => $audit->event,
                'entity_type' => class_basename($audit->auditable_type),
                'description' => $audit->changes_summary,
            ]);
        
        $activities = Activity::with('causer')->latest()->limit(100)->get()
            ->map(fn($activity) => [
                'source' => 'activity',
                'created_at' => $activity->created_at,
                'user_name' => $activity->causer?->name ?? 'System',
                'action' => $activity->event ?? $activity->log_name,
                'entity_type' => $activity->subject_type ? class_basename($activity->subject_type) : '',
                'description' => $activity->description,
            ]);
        
        return $audits->concat($activities)->sortByDesc('created_at')->take(100);
    }
}
```text

**Accessory Tracking in Check-Out Action (v3.5.0):**

```php
// app/Filament/Resources/LoanApplicationResource.php
Action::make('checkOut')
    ->form([
        Repeater::make('accessories')
            ->schema([
                Select::make('accessory_type')
                    ->options([
                        'POWER_ADAPTER' => 'Power Adapter',
                        'BAG' => 'Bag',
                        'MOUSE' => 'Mouse',
                        'USB_CABLE' => 'USB Cable',
                        'HDMI_VGA_CABLE' => 'HDMI/VGA Cable',
                        'REMOTE' => 'Remote',
                        'OTHERS' => 'Others',
                    ])
                    ->required(),
                TextInput::make('accessory_name')
                    ->visible(fn(Get $get) => $get('accessory_type') === 'OTHERS'),
                Toggle::make('present_at_checkout')
                    ->label('Included')
                    ->default(true),
                Textarea::make('condition_notes'),
            ])
            ->defaultItems(7)  // Pre-populate all standard accessories
    ])
    ->action(function (LoanApplication $record, array $data) {
        $transaction = LoanTransaction::create([
            'loan_application_id' => $record->id,
            'transaction_type' => 'CHECK_OUT',
            'admin_id' => Auth::id(),
        ]);
        
        $this->accessoryTrackingService->recordCheckoutAccessories(
            $transaction,
            $data['accessories']
        );
        
        $record->update(['status' => 'ACTIVE']);
    });
```text

### 6. Testing Strategy (PHPUnit 11.5.44)

**Property-Based Testing (100 Correctness Properties):**

```php
// tests/Feature/Helpdesk/HelpdeskHybridTest.php
test('guest submission creates ticket with null user_id', function () {
    $data = HelpdeskTicket::factory()->make()->toArray();
    
    $response = $this->post(route('helpdesk.store'), $data);
    
    $response->assertRedirect();
    $this->assertDatabaseHas('helpdesk_tickets', [
        'submitter_email' => $data['submitter_email'],
        'user_id' => null,  // Guest submission
    ]);
});

test('staff submission creates ticket with user_id', function () {
    $user = User::factory()->create(['role' => 'staff']);
    $data = HelpdeskTicket::factory()->make()->toArray();
    
    $response = $this->actingAs($user)->post(route('helpdesk.store'), $data);
    
    $response->assertRedirect(route('staff.dashboard'));
    $this->assertDatabaseHas('helpdesk_tickets', [
        'submitter_email' => $user->email,
        'user_id' => $user->id,  // Staff submission
    ]);
});

// tests/Feature/Loan/ResponsibleOfficerTest.php
test('responsible officer auto-populates when checkbox checked', function () {
    $data = [
        'applicant_name' => 'John Doe',
        'applicant_grade' => '41',
        'applicant_phone' => '0123456789',
        'is_applicant_responsible' => true,
    ];
    
    $loan = LoanApplication::create($data);
    
    $this->responsibleOfficerService->copyApplicantAsResponsibleOfficer($loan);
    
    expect($loan->refresh())
        ->responsible_officer_name->toBe('John Doe')
        ->responsible_officer_grade->toBe('41')
        ->responsible_officer_phone->toBe('0123456789');
});

// tests/Feature/Audit/DualAuditTest.php
test('ticket update creates both audit records', function () {
    $ticket = HelpdeskTicket::factory()->create(['status' => 'OPEN']);
    
    $ticket->update(['status' => 'IN_PROGRESS']);
    
    // owen-it audit (compliance)
    $this->assertDatabaseHas('audits', [
        'auditable_type' => HelpdeskTicket::class,
        'auditable_id' => $ticket->id,
        'event' => 'updated',
    ]);
    
    // spatie activity log (operations)
    $this->assertDatabaseHas('activity_log', [
        'subject_type' => HelpdeskTicket::class,
        'subject_id' => $ticket->id,
        'description' => 'updated',
    ]);
});
```text

### 7. Deployment Architecture

**Docker Compose Stack:**

```yaml
services:
  app:
    image: ictserve:3.5.0
    environment:
      - APP_ENV=production
      - DB_CONNECTION=mysql
      - REDIS_HOST=redis
      - REVERB_HOST=reverb
      - PULSE_ENABLED=true
      - SANCTUM_STATEFUL_DOMAINS=ictserve.motac.gov.my
  
  web:
    image: nginx:1.24
    depends_on:
      - app
  
  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
  
  redis:
    image: redis:7.0
    volumes:
      - redis_data:/data
  
  reverb:
    image: ictserve:3.5.0
    command: php artisan reverb:start
    environment:
      - REVERB_HOST=0.0.0.0
      - REVERB_PORT=8080
  
  queue:
    image: ictserve:3.5.0
    command: php artisan queue:work --tries=3
    depends_on:
      - redis
  
  pulse:
    image: ictserve:3.5.0
    command: php artisan pulse:work
    depends_on:
      - redis

volumes:
  mysql_data:
  redis_data:
```text

---

## Migration from v3.4.0 to v3.5.0

### Database Changes

**Step 1: Add Google OAuth fields to users table:**

```sql
ALTER TABLE users ADD COLUMN google_id VARCHAR(255) NULL UNIQUE;
ALTER TABLE users ADD COLUMN google_token TEXT NULL;
ALTER TABLE users ADD COLUMN google_refresh_token TEXT NULL;
```

**Step 2: Add form reference codes:**

```sql
ALTER TABLE helpdesk_tickets ADD COLUMN form_reference_code VARCHAR(50) DEFAULT 'PK.(S).MOTAC.07.(L1)';
ALTER TABLE loan_applications ADD COLUMN form_reference_code VARCHAR(50) DEFAULT 'PK.(S).MOTAC.07.(L3)';
```

**Step 3: Add Responsible Officer fields:**

```sql
ALTER TABLE loan_applications ADD COLUMN is_applicant_responsible BOOLEAN DEFAULT TRUE;
ALTER TABLE loan_applications ADD COLUMN responsible_officer_name VARCHAR(255) NULL;
ALTER TABLE loan_applications ADD COLUMN responsible_officer_grade VARCHAR(50) NULL;
ALTER TABLE loan_applications ADD COLUMN responsible_officer_phone VARCHAR(30) NULL;
ALTER TABLE loan_applications ADD COLUMN responsible_officer_acknowledgement BOOLEAN DEFAULT FALSE;
```

**Step 4: Create loan_transaction_accessories table:**

```sql
CREATE TABLE loan_transaction_accessories (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  loan_transaction_id BIGINT NOT NULL,
  accessory_type ENUM('POWER_ADAPTER', 'BAG', 'MOUSE', 'USB_CABLE', 'HDMI_VGA_CABLE', 'REMOTE', 'OTHERS'),
  accessory_name VARCHAR(100) NULL,
  present_at_checkout BOOLEAN DEFAULT TRUE,
  present_at_checkin BOOLEAN NULL,
  condition_notes TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (loan_transaction_id) REFERENCES loan_transactions(id) ON DELETE CASCADE
);
```

**Step 5: Install Laravel Pulse:**

```bash
composer require laravel/pulse
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
php artisan migrate
```

**Step 6: Install Laravel Sanctum:**

```bash
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate
```

**Step 7: Install Laravel Socialite (optional):**

```bash
composer require laravel/socialite
```

### Configuration Changes

**Update .env with new variables:**

```env
# Laravel Pulse
PULSE_ENABLED=true
PULSE_INGEST_DRIVER=redis
PULSE_STORAGE_DRIVER=database

# Laravel Sanctum
SANCTUM_STATEFUL_DOMAINS=ictserve.motac.gov.my

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=https://ictserve.motac.gov.my/auth/google/callback
```

**Update config/services.php:**

```php
'google' => [
    'client_id' => env('GOOGLE_CLIENT_ID'),
    'client_secret' => env('GOOGLE_CLIENT_SECRET'),
    'redirect' => env('GOOGLE_REDIRECT_URI'),
],
```

### Code Changes

- Update service constructors with new dependencies
- Add Responsible Officer logic to LoanApplicationWizard
- Add Accessory Tracking to Check-Out/Check-In actions
- Create UnifiedAuditLog Filament page
- Create ApiTokenResource Filament resource
- Add Google SSO routes and controller

### Testing

- **Run migration:** `php artisan migrate`
- **Run tests:** `php artisan test`
- **Run E2E tests:** `npx playwright test`
- **Verify Pulse dashboard:** Access `/pulse` as admin/superuser
- **Test API authentication:** Create token, test endpoints
- **Test Google SSO:** Login with @motac.gov.my account (if enabled)

---

**Document Version:** 3.5.0  
**Last Updated:** December 3, 2025  
**Status:** Active - True Hybrid Architecture
