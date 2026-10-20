# copilot-instructions.md

This file provides guidance to Copilot when working with code in this repository.

## Commands

```bash
# Development
npm run dev           # Start Next.js dev server
npm run build         # Production build
npm run start         # Run production server

# Code quality
npm run format        # Biome formatting
npm run lint          # ESLint
npm run lint:biome    # Biome lint with auto-fix
npm run check         # Biome full check (format + lint)

# Database
npx prisma generate               # Regenerate Prisma client after schema changes
npx prisma db pull                # Sync local schema from remote Supabase DB
npx next-openapi-gen generate     # Rebuild OpenAPI docs

# Dev workflow shortcuts (Makefile)
make sync     # git pull + npm install + prisma db pull + prisma generate + openapi-gen
make clean    # Wipe node_modules and caches
```

Node version: **24.11.0** (see `.nvmrc`). Install deps with `npm ci` (lockfile-based).

## Architecture Overview

**Akomi** is a dormitory accommodation management system for UPLB (University of the Philippines Los Baños). It is a full-stack Next.js 16 (App Router) monolith using TypeScript, built as an academic project for CMSC 128 A2-3L by The Haven Co.

### Three User Roles

| Role | Routes | Responsibilities |
|------|--------|-----------------|
| `STUDENT` | `/browse`, `/my-dashboard`, `/my-application` | Browse dorms, submit applications, upload documents, track status, view billing |
| `MANAGER` | `/screening`, `/manager`, `/occupancy` | Initial screening of applications, document verification, occupancy/move-in-out tracking |
| `ADMIN` | `/admin/*` | Final approval + room/bed assignment, dorm/room/user management, billing verification, reports |

New Google SSO signups receive `NEW_USER` type and are redirected to `/onboarding` to capture student number and college before granting full access.

### Two-Step Approval Pipeline

Applications move through a strict sequential workflow:

```
Pending Screening
  → (Manager: Initial Approve) → Pending Final Approval
  → (Admin: Grant Final Approval + assign room/bed) → Approved Assigned
  → (Manager: Record move-out date) → Completed

  Manager can also: Reject | Waitlist (from Pending Screening)
  Admin can also: Return to Manager | Override existing Approved Assigned record
```

Key business rules enforced in code:
- A student may only have **one active application** at a time
- Applications are scoped to a specific dormitory; managers only see applications for their assigned facility
- Room/bed assignment happens exclusively at the Admin final approval step; managers handle intra-room details only after assignment
- Application submissions are gated by **application window dates** set by admins

### Out of Scope (do not implement)

- Digital contract parsing or e-signature integration — documents are static PDFs reviewed manually
- Offline functionality

### Feature Parking Lot (deferred, not yet planned)

Features explicitly deferred from the current version — do not build unless instructed:

- **Payment gateway / automated billing** — current implementation is manual receipt upload + admin verification only
- **Map view for Browse Dormitories** — dorm catalog is currently a filtered grid/list only

### Middleware & RBAC

`proxy.ts` (Next.js middleware) handles all routing logic:
- Unauthenticated requests → `/login`
- Authenticated users routed to role-appropriate pages
- Path-level access enforcement via `lib/rbac.ts`

### Directory Structure

```
app/
  (auth)/login/                  # Login page
  (main)/
    (dormer)/                    # Student-facing pages
    (manager)/                   # Manager-facing pages
    (admin)/                     # Admin-facing pages
  api/                           # Next.js route handlers
  components/
    ui/                          # shadcn/ui primitives
    dormitories/ student/ manager/ admin/ layout/
  generated/prisma/              # Prisma client output (do not edit)
lib/
  auth.ts                        # Better Auth server config
  auth-client.ts                 # Client-side auth hooks
  db.ts                          # Prisma client singleton
  rbac.ts                        # Role/path access rules
  errors.ts                      # Custom error classes
  schemas/                       # Zod validation schemas
  store/                         # Zustand client stores
  services/                      # Business logic layer
  supabase/storage.ts            # File upload/download helpers
hooks/                           # Custom React hooks (API + store wrappers)
types/                           # Shared TypeScript types
prisma/schema.prisma             # Database schema
```

### API Pattern

Route handlers in `app/api/` follow this pattern:
- Validate request with Zod schemas from `lib/schemas/`
- Call service functions in `lib/services/`
- Services use Prisma for DB queries and `lib/supabase/storage.ts` for files
- Respond with `{ success, data, error }` JSON
- JSDoc OpenAPI decorators enable auto-generated API docs

### State Management

- **Zustand** stores in `lib/store/` for client-side state (dorm catalog, screening queue, dashboard metrics)
- Custom hooks in `hooks/` wrap Zustand + fetch calls into unified interfaces
- **React Hook Form** + Zod for all form state and validation

### Authentication

- **Better Auth** with Google SSO (restricted to UP Mail `@up.edu.ph` domain)
- User type stored in `user.type`: `STUDENT | MANAGER | ADMIN | NEW_USER`
- Server: validate session with `auth.api.getSession()` in route handlers
- Client: use `authClient` from `lib/auth-client.ts`

### Database

- PostgreSQL via **Supabase**, accessed through Prisma ORM
- Prisma adapter: `@prisma/adapter-pg` (connection pooling)
- Generated client output path: `app/generated/prisma` (configured in `schema.prisma`)
- After any schema change: run `npx prisma generate`

### Key Technologies

- **UI**: shadcn/ui (Radix Nova style) + Tailwind CSS 4 + Lucide icons
- **File storage**: Supabase Storage (dorm images, applicant documents)
- **Code style**: Biome (120-char line width, 4-space indent, git-aware)
- **API docs**: Zod-to-OpenAPI + Scalar (auto-generated via `next-openapi-gen`)
