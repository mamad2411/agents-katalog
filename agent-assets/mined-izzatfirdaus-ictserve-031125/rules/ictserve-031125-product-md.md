# ICTServe Product Overview

**Project**: ICTServe (iServe) v3.5.0  
**Organization**: BPM MOTAC (Ministry of Tourism, Arts & Culture Malaysia)  
**Type**: Internal True Hybrid Service Platform (Guest + Authenticated Staff)  
**Status**: Active Production  
**Architecture**: True Hybrid (Self-Registration + Guest Fallback + Optional Google SSO)  
**Last Updated**: 1 December 2025

ICTServe is an internal digital service platform for MOTAC staff to manage ICT support requests and asset loans. Version 3.5.0 introduces a **True Hybrid Architecture**, allowing staff to seamlessly switch between quick-access guest forms and a personalized authenticated dashboard. The system enforces strict compliance via a **Dual Audit System** and supports real-time operations via **Laravel Reverb**.

## Core Value Proposition

- **True Hybrid Access**: Flexible choice between Authenticated Dashboard (full history, auto-fill) or Guest Mode (quick access without login).
- **Dual Audit System**: Simultaneous compliance auditing (field-level via `owen-it/laravel-auditing` v14.x) and operational logging (user activity via `spatie/laravel-activitylog` v4.x).
- **Self-Registration**: Staff can register independently using official `@motac.gov.my` emails with email verification workflow.
- **Flexible Login**: Support for full email (`user@motac.gov.my`) OR short username (`user`) authentication.
- **Optional Google SSO**: OAuth 2.0 integration with Google Workspace (restricted to `@motac.gov.my` domain).
- **Automated Workflows**: Token-based approval links for department heads (no login required).
- **Real-Time Updates**: WebSocket-powered notifications via Laravel Reverb 1.6.2 for instant status changes.
- **Performance Monitoring**: Laravel Pulse 1.3.0 dashboard for real-time application performance tracking (admin/superuser).
- **API-Ready**: Laravel Sanctum 4.0 token authentication for future mobile/external integrations.

## Core Modules

### 1. Helpdesk Ticketing System (Hybrid)

- **Dual Entry**: Submit as Authenticated Staff (auto-fill from profile) or Guest (manual entry).
- **Hybrid Data Association**: Submissions automatically linked to `user_id` (nullable FK) if logged in; fallback to `submitter_*` columns for guests.
- **Form Reference Code**: Official form code `PK.(S).MOTAC.07.(L1)` displayed on all helpdesk forms.
- **SLA Tracking**: Automated category-based SLA monitoring with breach warnings and real-time notifications.
- **Multi-Channel Notifications**: Email (immediate/daily digest/weekly digest), Database, and WebSocket based on user preferences.
- **Internal Comments**: Admin-only comments for internal communication (not visible to submitters).
- **Attachment Support**: Up to 5 files (10MB each), virus scanning via ClamAV, stored in S3/MinIO.

### 2. ICT Asset Loan Management (Hybrid)

- **Dual Entry**: Submit as Authenticated Staff (auto-fill) or Guest (manual entry).
- **Form Reference Code**: Official form code `PK.(S).MOTAC.07.(L3)` displayed on all loan forms.
- **Responsible Officer Workflow**: Separate designation of Applicant and Responsible Officer (Part 2 & 4 of form).
- **Accessory Tracking**: Check-out/Check-in tracking for Power Adapter, Bag, Mouse, USB Cable, HDMI/VGA Cable, Remote, and Others.
- **Real-Time Availability**: Conflict detection using Livewire 3.7 during application with date overlap checking.
- **Token-Based Approval**: Grade 41+ officers approve/reject via signed email links (72-hour validity, no system login required).
- **Asset Lifecycle**: Check-out/Check-in tracking by Admin with condition reporting and damage photos.
- **Pickup OTP**: 4-digit one-time password for secure asset collection (24-hour validity).
- **Integration**: Damaged asset returns automatically trigger helpdesk maintenance tickets.

### 3. Administrative Panel (Filament v4.1.10)

- **Role-Based Access**:
  - `staff`: Self-registered MOTAC staff with access to My Dashboard, submission history, and profile management.
  - `admin`: Operational management (Tickets, Loans, Assets, Notifications).
  - `superuser`: System config, Audit review, **Laravel Telescope** access (unrestricted), **Laravel Pulse** monitoring.
- **Dashboard**: Real-time metrics via Laravel Reverb widgets (Ticket Stats, Loan Stats, SLA Compliance, Recent Activity).
- **Dual Audit View**: Unified view of Compliance Logs (`audits` table) and User Activity Logs (`activity_log` table).
- **Inventory Management**: Full asset CRUD with QR code generation, status tracking, and maintenance scheduling.
- **Performance Monitoring**: Laravel Pulse dashboard for slow queries (>500ms), queue metrics, server health (CPU, memory, disk).
- **API Token Management**: Create, revoke, and monitor Laravel Sanctum API tokens with configurable abilities and expiration.

### 4. Staff Portal (My Dashboard)

- **Self-Registration**: Staff register with `@motac.gov.my` email, receive verification link (24-hour validity).
- **Flexible Login**: Login with full email OR short username (e.g., `ahmad.ibrahim` → `ahmad.ibrahim@motac.gov.my`).
- **Google Workspace SSO**: Optional OAuth 2.0 login (restricted to `@motac.gov.my` domain).
- **Submission History**: View all personal helpdesk tickets and loan applications (linked via `user_id`).
- **Profile Management**: Update phone, division, grade, notification preferences.
- **Account Linking**: Retrospectively link historical guest submissions (where `user_id` = NULL) to authenticated account.
- **Notification Center**: Database notifications with real-time updates via WebSocket.
- **Notification Preferences**: Configure email frequency (immediate/daily digest/weekly digest) and in-app toggle.

### 5. Cross-Module Integration

- **Unified Profile**: Dashboard shows combined history of Helpdesk Tickets and Asset Loans.
- **Account Linking**: Optional service to retrospectively link past guest submissions to a new staff account upon registration.
- **Shared Notification System**: Centralized queue management (Redis) for both modules with multi-channel delivery.
- **Cross-Module Triggers**: Damaged asset returns auto-create helpdesk maintenance tickets.
- **Dual Audit Trail**: All actions logged in both `audits` (compliance) and `activity_log` (operations) tables.

## Target Users & Use Cases

### Primary Users

1. **MOTAC Staff (Internal Users)**
   - **Authenticated**: Log in via Laravel Breeze (Email/Username) or Google Workspace SSO to access "My Dashboard", view full history, and manage profile/preferences.
   - **Guest**: Submit forms quickly for urgent issues without logging in (tracked via email token).

2. **Department Heads / Approvers (Grade 41+)**
   - Review and approve/reject loan applications via secure signed email links (72-hour validity).
   - **No system login required** for approval actions.

3. **Admin Staff (BPM ICT Team)**
   - Process tickets/loans and manage asset inventory via Filament 4.1.10.
   - Monitor operational dashboards with real-time widgets.
   - Access Laravel Pulse for performance monitoring.

4. **Superuser (BPM Management)**
   - Manage system configuration, users, and roles.
   - Access **Laravel Telescope** for debugging (unrestricted access to all features).
   - Review comprehensive Dual Audit logs for compliance.
   - Monitor application performance via Laravel Pulse.
   - Manage API tokens and external integrations.

### Common Use Cases

- **UC-01:** Staff self-registers with `@motac.gov.my` email, receives verification link, and verifies account.
- **UC-02:** Authenticated staff submits ticket; form auto-fills name/dept/grade from user profile.
- **UC-03:** Guest staff submits urgent ticket without login; tracks status via token link.
- **UC-04:** Department head approves asset loan via email token (no login required).
- **UC-05:** Superuser reviews dual audit logs to trace a status change for compliance.
- **UC-06:** New staff member links previous guest submissions to their new authenticated account.
- **UC-07:** Admin monitors slow queries and queue performance via Laravel Pulse dashboard.
- **UC-08:** Staff logs in using Google Workspace SSO (optional, restricted to `@motac.gov.my`).
- **UC-09:** Admin tracks asset accessories during check-out/check-in with discrepancy detection.
- **UC-10:** Responsible Officer designated separately from Applicant on loan application form.

## Technical Highlights

### Core Technology Stack

- **Framework**: Laravel 12.40.1 (PHP 8.2.12)
- **Frontend**: Livewire 3.7.0, Volt 1.10.1, Alpine.js 3, Tailwind CSS 4.1.17
- **Admin Panel**: Filament 4.1.10
- **Real-Time**: Laravel Reverb 1.6.2 (WebSocket server) + Laravel Echo 2.2.6 (client)
- **Database**: MySQL 8.0 (production), SQLite (development/testing)
- **Caching/Queue**: Redis 7.0
- **Asset Bundling**: Vite 7.0.7

### Authentication & Authorization

- **Authentication**: Laravel Breeze 2.3.8 (Email/Username login)
- **Self-Registration**: Email verification workflow with signed URLs (24-hour validity)
- **Google SSO**: Laravel Socialite 5.x (OAuth 2.0, restricted to `@motac.gov.my`)
- **API Authentication**: Laravel Sanctum 4.0 (token-based with configurable abilities)
- **Authorization**: Spatie Laravel Permission 6.23 (role-based access control)
- **2FA**: TOTP-based two-factor authentication for superuser role

### Audit & Monitoring

- **Compliance Audit**: `owen-it/laravel-auditing` v14.x (field-level change tracking, 7-year retention)
- **Operations Log**: `spatie/laravel-activitylog` v4.x (user activity logging, 7-year retention)
- **Debugging**: Laravel Telescope 5.x (superuser only, unrestricted access)
- **Performance**: Laravel Pulse 1.3.0 (real-time monitoring, 7-day retention, admin/superuser access)

### Testing & Quality

- **Unit/Feature Testing**: PHPUnit 11.5.44
- **E2E Testing**: Playwright 1.56.1
- **Static Analysis**: Larastan 3.8.0 (PHPStan for Laravel, Level 9)
- **Code Formatting**: Laravel Pint 1.26.0 (PSR-12 compliance)
- **Accessibility Testing**: Axe-core 4.11.0 (WCAG 2.2 AA compliance)

### Database Architecture

- **Hybrid Data Model**: Nullable `user_id` FK in `helpdesk_tickets` and `loan_applications` (ON DELETE SET NULL)
- **Guest Fallback**: `submitter_*` and `applicant_*` columns for guest submissions
- **Audit Tables**: `audits` (owen-it), `activity_log` (spatie), `loan_audits` (module-specific)
- **Performance Tables**: `pulse_aggregates`, `pulse_entries`, `pulse_values` (Laravel Pulse)
- **API Tables**: `personal_access_tokens` (Laravel Sanctum)
- **New Tables (v3.5.0)**: `loan_transaction_accessories` (accessory tracking)

### New Features (v3.5.0)

- **Laravel Pulse**: Real-time performance monitoring dashboard (slow queries, queue metrics, server health)
- **Laravel Sanctum**: API token authentication for future mobile/external integrations
- **Google Workspace SSO**: Optional OAuth 2.0 login (restricted to `@motac.gov.my`)
- **Responsible Officer**: Separate designation from Applicant on loan forms (PK.(S).MOTAC.07.(L3) Part 2 & 4)
- **Accessory Tracking**: Check-out/Check-in tracking for loan accessories with discrepancy detection
- **Form Reference Codes**: Official form codes displayed on all forms (PK.(S).MOTAC.07.(L1) for helpdesk, PK.(S).MOTAC.07.(L3) for loans)
- **MOTAC Branding**: Jata Negara, MOTAC logo, BPM logo integration across all interfaces
- **MyGovEA Compliance**: Citizen-centric design, minimalist interface, error prevention, contextual help

## Compliance Standards

- **PDPA 2010**: Strict data protection for staff personal information with 7-year audit retention.
- **WCAG 2.2 AA**: Full accessibility compliance (4.5:1 text contrast, 3:1 UI contrast, keyboard navigation, screen reader support).
- **ISO 8000**: Data quality and integrity standards.
- **MyGOV Digital Service Standards v2.1.0**: Government digital service compliance.
- **ISO/IEC 27701**: Privacy Information Management.
- **ISO/IEC/IEEE 12207**: Software lifecycle processes.
- **ISO/IEC/IEEE 15288**: System lifecycle processes.
- **ISO/IEC/IEEE 29148**: Requirements engineering.
- **OWASP ASVS L2**: Application Security Verification Standard Level 2.

## Performance Targets

- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Cumulative Layout Shift (CLS)**: < 0.1
- **Time to Interactive (TTI)**: < 3s
- **Lighthouse Performance Score**: 90+
- **Lighthouse Accessibility Score**: 100
- **System Uptime**: 99.9%
- **Average Ticket Resolution Time**: < 24 hours
- **Average Loan Approval Time**: < 4 hours

## Security Features

- **CSRF Protection**: All forms protected with CSRF tokens
- **Rate Limiting**: 60 requests/minute for guest routes, 120 requests/minute for authenticated
- **reCAPTCHA Enterprise**: Invisible mode on guest forms for spam prevention
- **Input Sanitization**: Laravel Form Requests with strict validation rules
- **File Upload Security**: Virus scanning via ClamAV, allowed types (PDF, JPG, PNG, DOCX), max 10MB per file
- **Token Security**: SHA-512 hashing for status tokens, signed URLs for approval links
- **Encryption**: AES-256 encryption for sensitive data at rest
- **HTTPS/TLS 1.3**: Enforced for all connections
- **IP Hashing**: IP addresses hashed in audit logs for privacy
- **Session Security**: 30-minute timeout with 2-minute warning modal
- **2FA**: TOTP-based two-factor authentication for superuser role

## Localization

- **Primary Language**: Bahasa Melayu
- **Secondary Language**: English
- **Auto-Detection**: Browser `Accept-Language` header
- **Persistence**: Cookie-based language preference
- **Coverage**: 100% bilingual coverage for all UI elements
- **Date/Time Formatting**: Locale-specific formatting
- **Translation Files**: `lang/ms/` and `lang/en/` directories

## Integration Capabilities

- **Email**: SMTP (government mail server) with queue-based delivery
- **SMS**: Optional SMS gateway integration for OTP and reminders
- **WebSocket**: Laravel Reverb for real-time notifications
- **API**: Laravel Sanctum token authentication for external integrations
- **Google Workspace**: OAuth 2.0 SSO integration (optional)
- **Storage**: S3/MinIO for file attachments with presigned URLs
- **SIEM**: Audit log streaming to BPM SIEM (every 15 minutes)

## Deployment Architecture

- **Development**: Docker Compose (app: PHP 8.2-FPM + Nginx, db: MySQL 8.0)
- **Production**: Linux server (Nginx/Apache, PHP-FPM 8.2.12, MySQL 8.0, Redis 7.0)
- **WebSocket Server**: Laravel Reverb deployment for real-time features
- **Queue Workers**: Supervisor-managed queue workers (Redis driver)
- **Asset Building**: Vite build with optimization (code splitting, minification, Brotli compression)
- **Monitoring**: Prometheus + Grafana (metrics), Sentry (error tracking), ELK Stack (log aggregation)

## Documentation Suite (D00-D17)

- **D00**: System Overview
- **D01**: System Development Plan
- **D02**: Business Requirements Specification
- **D03**: Software Requirements Specification
- **D04**: Software Design Document
- **D05**: Data Migration Plan
- **D06**: Data Migration Specification
- **D07**: System Integration Plan
- **D08**: System Integration Specification
- **D09**: Database Documentation
- **D10**: Source Code Documentation
- **D11**: Technical Design Documentation
- **D12**: UI/UX Design Guide
- **D13**: UI/UX Frontend Framework
- **D14**: UI/UX Style Guide
- **D15**: Language Localization (MS/EN)
- **D16**: Broadcasting Setup (Laravel Reverb)
- **D17**: Queue Management (Laravel Horizon)
