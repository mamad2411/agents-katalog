# AI School Assistant - Copilot Instructions

# Product Positioning

EduFlow is an AI-powered school communication platform.

This is NOT a traditional ERP system.

Generated features should prioritize:

* communication automation
* teacher productivity
* operational efficiency
* AI-assisted workflows
* parent engagement
* mobile-first workflows

Avoid unnecessary ERP-style complexity unless explicitly requested.

---

# Project Architecture

This project consists of:

## Frontend

* Ionic 8
* Angular 19
* TypeScript 5.8
* RxJS 7
* NgRx Store + Effects
* Reactive Forms only
* Angular Router
* Standalone Components
* TailwindCSS

## Backend

* NestJS 10
* Prisma ORM 5
* PostgreSQL
* JWT Authentication
* REST APIs
* BullMQ queues
* Socket.IO support

---

# General Development Rules

* Use strict TypeScript typing.
* Prefer reusable services over duplicated logic.
* Follow existing folder structure and architecture.
* Do not introduce breaking changes unless explicitly requested.
* Preserve existing authentication and authorization flow.
* Avoid unnecessary refactors.
* Keep components modular and maintainable.
* Reuse existing implementations before creating new abstractions.
* Keep generated code production-ready.
* Preserve backward compatibility where possible.

---

# Multi-Tenant Architecture Rules

* All business data must remain tenant-isolated.
* Never trust tenantId directly from frontend payloads.
* Prefer extracting tenantId from authenticated JWT user context.
* All Prisma queries involving business data should filter by tenantId where applicable.
* Prevent cross-tenant data access.
* Maintain school-level isolation for:

  * students
  * teachers
  * parents
  * communication logs
  * attendance
  * analytics
  * homework
  * notices

---

# Frontend Rules (Angular + Ionic)

## Angular Standards

* Use standalone Angular components where applicable.
* Use Reactive Forms only.
* Use RxJS observables properly.
* Avoid nested subscriptions.
* Prefer async pipe when possible.
* Prefer service-based API communication.
* Use typed interfaces/models.
* Keep components focused and lightweight.

## Frontend Architecture Constraints

Avoid business logic inside pages/components.

Prefer:

* feature services
* facade services
* reusable shared components
* centralized API handling
* reusable utility helpers

Keep pages focused on:

* presentation
* orchestration
* user interaction

## Ionic UI Standards

* Use Ionic components consistently.
* Maintain mobile-first responsive layouts.
* Preserve existing styling conventions.
* Use loaders/spinners for async operations.
* Show user-friendly error messages.
* Maintain consistent spacing and layout patterns.
* Keep UI clean and operationally focused.

---

# Mobile UX Standards

This application is mobile-first.

Generated UI should:

* prioritize thumb-friendly interactions
* minimize typing effort
* avoid overcrowded screens
* support fast teacher workflows
* use large tap targets
* preserve responsive layouts
* avoid desktop-heavy UI patterns

Preferred interaction patterns:

* bottom sheets
* floating action buttons
* quick actions
* swipe-friendly cards
* mobile-friendly action menus

---

# Routing Rules

# Routing Architecture Rules

This application uses Angular standalone route configuration with lazy-loaded components.

## Current Routing Pattern

Routes are organized by feature/domain, including:

* dashboard
* communication
* homework
* notices
* attendance
* students
* teachers
* parents
* authentication

## Route Guidelines

* Keep routes feature-oriented and modular.
* Prefer grouping related routes under parent feature paths where appropriate.
* Use lazy-loaded standalone components with `loadComponent`.
* Preserve existing route naming conventions.
* Avoid unnecessary root-level routes when a feature parent route exists.

## Examples

Preferred:

* /teacher/onboard-student
* /teacher/onboard-parent
* /student/:id
* /communication-center

Avoid:

* deeply nested unnecessary routes
* duplicate feature routes
* inconsistent naming patterns

## Route Protection

* Protected pages should use `AuthGuard`.
* Authentication pages should remain publicly accessible.
* Preserve existing authorization behavior.

## Navigation

When adding new pages:

* Add navigation links where appropriate.
* Update menus/dashboard shortcuts if related to user workflows.
* Preserve mobile-friendly navigation patterns.

## Redirects

* Preserve default dashboard redirect behavior.
* Preserve wildcard route fallback handling.

## Lazy Loading

All feature pages should continue using:

* `loadComponent`
* dynamic imports
* standalone page architecture

---

# State Management

* Use NgRx patterns where already implemented.
* Do not introduce new state management libraries.
* Preserve existing store architecture.
* Avoid unnecessary global state.

---

# Forms

All forms must:

* include validation
* show validation errors
* use FormBuilder
* strongly type payloads
* sanitize inputs where appropriate

---

# Communication Module Standards

This application prioritizes communication automation workflows.

Primary communication channels include:

* WhatsApp
* in-app notifications
* notices
* homework broadcasts
* attendance alerts
* fee reminders

Generated features should:

* prioritize teacher/admin efficiency
* minimize typing effort
* support mobile-first workflows
* support bulk communication patterns
* preserve communication history
* support delivery tracking where applicable

---

# WhatsApp Integration Standards

* Use Meta WhatsApp Cloud API architecture.
* Keep provider logic isolated inside dedicated services.
* Avoid direct WhatsApp API calls from controllers.
* Preserve reusable provider abstraction patterns.
* All messaging operations should support:

  * logging
  * retries
  * error handling
  * delivery status tracking
* Sanitize phone numbers before sending.
* Preserve async-safe messaging flows.

---

# AI Service Standards

AI features should use centralized reusable services.

Avoid embedding AI prompt logic directly inside components.

Preferred AI responsibilities:

* homework formatting
* notice generation
* message improvement
* translation
* communication tone adjustment
* parent-friendly communication formatting

AI service methods should remain:

* modular
* reusable
* provider-agnostic
* scalable

---

# Backend Rules (NestJS + Prisma)

## NestJS Standards

* Follow module/service/controller architecture.
* Keep business logic inside services.
* Controllers should remain lightweight.
* Use DTOs with class-validator.
* Use dependency injection properly.
* Prefer feature-based modular architecture.

## Prisma Standards

* Use Prisma ORM only.
* Avoid raw SQL unless necessary.
* Keep schema relations clean.
* Generate migrations carefully.
* Preserve relation integrity.
* Use proper indexes where needed.

## API Standards

* Follow REST conventions.
* Use proper HTTP status codes.
* Add validation and error handling.
* Return consistent API response structures.
* Use DTO validation for request payloads.

## Authentication

* Preserve JWT authentication flow.
* Do not bypass guards unless explicitly requested.
* Respect existing role-based access logic.
* Prefer extracting user context from JWT instead of trusting frontend payloads.

---

# Queue & Background Job Standards

Use BullMQ for:

* scheduled messaging
* bulk communication
* retries
* background processing
* delayed notifications

Avoid long-running synchronous API operations.

---

# Logging Standards

Critical operations should include logging:

* WhatsApp messaging
* authentication events
* scheduling operations
* AI generation failures
* communication delivery status
* bulk operations

Avoid silent failures.

---

# Error Handling

When fixing bugs:

1. First identify root cause.
2. Explain probable cause briefly.
3. Implement minimal safe fix.
4. Avoid unrelated code changes.

For API issues:

* Verify frontend endpoint URLs
* Verify backend controller routes
* Verify DTO validation
* Verify Prisma schema compatibility
* Verify authentication guards
* Verify tenant isolation logic

---

# Database Rules

Before modifying Prisma schema:

* Check existing relationships
* Avoid destructive schema changes
* Preserve existing data compatibility

When adding fields:

* Update:

  * Prisma schema
  * DTOs
  * Services
  * API payloads
  * Angular forms
  * Interfaces/types

---

# Environment Variable Standards

Secrets must remain environment-driven.

Never hardcode:

* JWT secrets
* API keys
* database credentials
* WhatsApp tokens
* OpenAI keys

Use ConfigService for backend configuration access.

---

# Code Quality Expectations

Generated code should:

* compile successfully
* avoid TypeScript errors
* avoid unused imports
* follow existing naming conventions
* include proper null/undefined handling
* remain readable and maintainable

---

# Preferred Patterns

## Angular API Calls

* Use dedicated API services.
* Do not call HTTP directly from components unless already following that pattern.

## Backend Validation

* Use DTO validation decorators.
* Validate request payloads properly.

## Async Handling

* Use try/catch in backend services.
* Handle loading and error states in frontend.

## Reusability

* Prefer reusable components/services.
* Avoid duplicated logic.
* Keep abstractions practical.

---

# Important Constraints

* Do not change package versions unless explicitly requested.
* Do not migrate architecture/frameworks.
* Do not remove existing functionality.
* Do not introduce unnecessary dependencies.
* Avoid introducing breaking API changes.

---

# Common Application Domains

This application manages:

* teachers
* students
* parents
* onboarding
* attendance
* activities
* analytics
* classroom workflows
* communication automation
* notices
* homework broadcasting

Generated features should align with school communication workflows.

---

# Expected AI Behavior

When implementing tasks:

1. Analyze existing implementation first.
2. Reuse existing patterns.
3. Modify only necessary files.
4. Keep changes production-ready.
5. Explain important architectural decisions briefly.
6. Preserve existing UX patterns.
7. Avoid overengineering.
