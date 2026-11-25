---
name: event-backend
description: >-
  Expert guide and runbook for the Hackathon Event Management backend system.
  Use this skill whenever working with, debugging, modifying, or extending backend API routes,
  Supabase database queries and schemas, authentication flows, Google Sheets synchronization
  (registration, attendance, and team rosters), team management logic (join, leave, kick, disband, merge),
  or track distribution algorithms.
---

# Hackathon Event Backend Skill

This skill provides comprehensive instructions, architectural guidelines, API references, and runbooks for the backend logic of the Hackathon Event Management platform.

## Architecture Overview

The backend is built on Next.js App Router (Node.js runtime) with Supabase (PostgreSQL + Auth) and Google Sheets API v4.

```
                  ┌─────────────────────────────────┐
                  │ Next.js App Router API Routes   │
                  │ (/app/api/*, /app/auth/*)       │
                  └────────┬───────────────┬────────┘
                           │               │
            ┌──────────────▼────┐    ┌─────▼──────────────────┐
            │  Supabase Client  │    │ Google Sheets API v4   │
            │  (PostgreSQL/Auth)│    │ (JWT Service Account)  │
            └───────────────────┘    └────────────────────────┘
```

### Core Components & Locations

- **Supabase Clients & Proxy**:
  - Server Client: [lib/supabase/server.js](file:///f:/shiii/init/init_hackathon/lib/supabase/server.js) — Cookie-based server auth client
  - Browser Client: [lib/supabase/client.js](file:///f:/shiii/init/init_hackathon/lib/supabase/client.js) — Client-side singleton
  - Session Refresh Proxy: [lib/supabase/proxy.js](file:///f:/shiii/init/init_hackathon/lib/supabase/proxy.js) & [proxy.js](file:///f:/shiii/init/init_hackathon/proxy.js)
  - Dashboard Helpers: [lib/dashboardHelpers.js](file:///f:/shiii/init/init_hackathon/lib/dashboardHelpers.js)
- **API Endpoints**:
  - Registration Verification: [app/api/registration/route.js](file:///f:/shiii/init/init_hackathon/app/api/registration/route.js)
  - Team Management: [app/api/team/route.js](file:///f:/shiii/init/init_hackathon/app/api/team/route.js)
  - Team Actions:
    - Kick: [app/api/team/kick/route.js](file:///f:/shiii/init/init_hackathon/app/api/team/kick/route.js)
    - Leave: [app/api/team/leave/route.js](file:///f:/shiii/init/init_hackathon/app/api/team/leave/route.js)
    - Disband: [app/api/team/disband/route.js](file:///f:/shiii/init/init_hackathon/app/api/team/disband/route.js)
    - Merge: [app/api/team/merge/route.js](file:///f:/shiii/init/init_hackathon/app/api/team/merge/route.js)
  - Scanner & Attendance:
    - Mark Attendance: [app/api/scanner/attendance/route.js](file:///f:/shiii/init/init_hackathon/app/api/scanner/attendance/route.js)
    - Check Attendance: [app/api/scanner/check-attendance/route.js](file:///f:/shiii/init/init_hackathon/app/api/scanner/check-attendance/route.js)
  - Admin Operations:
    - Track Auto-Distribution: [app/api/admin/tracks/distribute/route.js](file:///f:/shiii/init/init_hackathon/app/api/admin/tracks/distribute/route.js)
  - Auth Flow:
    - OTP Confirm Callback: [app/auth/route.js](file:///f:/shiii/init/init_hackathon/app/auth/route.js)

---

## Detailed References

For deep dives into specific subsystems, refer to the following documents:

1. **[API Endpoints Reference](./references/api_endpoints.md)**: Full request/response schemas, status codes, and query contracts.
2. **[Database Schema & Relations](./references/database_schema.md)**: Tables (`profiles`, `teams`, `tracks`, `submissions`, `updates`, `hackathon_settings`), constraints, and relationships.
3. **[Google Sheets Integration](./references/google_sheets_integration.md)**: Service account JWT authentication (RSA-SHA256), Sheet creation, range append, and batch updates.
4. **[Team Lifecycle & Business Rules](./references/team_management_lifecycle.md)**: Logic for team capacity, role transitions, kicker/disband guards, and 2-team merge flow.

---

## Key Backend Workflows & Runbooks

### 1. Handling User Authentication & Session Refresh
- User signs in via Supabase OTP / Magic Link.
- [app/auth/route.js](file:///f:/shiii/init/init_hackathon/app/auth/route.js) receives `GET /auth?token_hash=...&type=...` and invokes `supabase.auth.verifyOtp()`.
- Upon success, redirects user to `/dashboard/account`.
- All requests passing through Next.js proxy execute [lib/supabase/proxy.js](file:///f:/shiii/init/init_hackathon/lib/supabase/proxy.js) to refresh auth tokens and keep cookies in sync.

### 2. Team Management & Capacity Enforcement
- **Capacity Constraint**: Maximum team size is **6 members** (`TEAM_MEMBER_LIMIT = 6`).
- **Team Verification**: `POST /api/team` with `{ teamId, action: 'check' }` returns `{ ok: boolean, memberCount, limit: 6 }`.
- **Google Sheets Sync**: `POST /api/team` with `{ teamId, memberId, action: 'sync' }` verifies session, extracts user email, generates a Google JWT, and appends `[team.number, team.name, email, memberCount]` to the configured Google Sheet range `Teams!A:D`.
- **Team Merging**:
  - Validates neither team is already merged (`is_merged === false`).
  - Validates combined member count $\le 6$.
  - Target team leader authorization required.
  - Updates initiator team name (`"${initiator.name} + ${target.name}"`), marks target `is_merged: true`, moves target members to initiator team with role `'member'`, sets initiator team owner as `'leader'`, and batch-updates Google Sheets rows.

### 3. QR Attendance Scanning Flow
- QR code encodes `userId` (Supabase Profile UUID).
- Scanner scans QR $\rightarrow$ calls `POST /api/scanner/check-attendance` with `{ userId }`.
- If not present, calls `POST /api/scanner/attendance` with `{ userId, fullName, username, teamName, userRole }`.
- Endpoint automatically verifies if `Attendance` tab exists in the Google Spreadsheet; if not, creates sheet with headers `['User ID', 'Full Name', 'Username', 'Team Name', 'Role', 'Timestamp']`.
- Appends new row with ISO UTC timestamp.

### 4. Greedy Track Balancing Algorithm
- Admin endpoint [app/api/admin/tracks/distribute/route.js](file:///f:/shiii/init/init_hackathon/app/api/admin/tracks/distribute/route.js):
  - Fetches enabled tracks from `tracks` table.
  - Queries teams where `track IS NULL` (or all teams if `reassign: true`).
  - Computes track distribution frequencies and balances assignment by picking the track with the minimum team count iteratively.

---

## Required Environment Variables

Ensure these variables are set in `.env` / production deployment:

| Variable | Description |
| :--- | :--- |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project API URL |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Supabase public/publishable API key |
| `GOOGLE_SERVICE_ACCOUNT_EMAIL` | Google Cloud IAM service account email |
| `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY` | RSA Private key for Google Service Account (with `\n` handling) |
| `SHEET_ID` | Target Google Spreadsheet ID |
| `GOOGLE_API_KEY` | Google Cloud Public API key for read queries |
| `SHEET_RANGE` | Optional registration range (Default: `Sheet1!C:C`) |
| `TEAMS_SHEET_RANGE` | Optional teams range (Default: `Teams!A:D`) |

---

## Verification & Testing Scripts

- Inspect mock API request payloads in [examples/api_requests.json](./examples/api_requests.json).
- Inspect reusable database query snippets in [examples/backend_queries.js](./examples/backend_queries.js).
- Run the environment & backend health verification helper:
  ```bash
  node .agents/skills/event-backend/scripts/verify_backend.mjs
  ```
