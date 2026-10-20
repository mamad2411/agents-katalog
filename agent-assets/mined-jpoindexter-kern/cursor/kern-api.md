---
description: API route conventions and endpoints
globs: src/app/api/**,app/api/**,pages/api/**
---

# API Rules

- Use Route Handlers (GET, POST, PUT, DELETE exports).
- Validate request bodies with Zod.
- Return NextResponse.json() with proper status codes.
- Check authentication before processing protected routes.

## Endpoints

- `GET` `/api/auth/session` [AUTH]
- `POST` `/api/contact`
- `GET` `/api/dashboard` [AUTH]
- `POST` `/api/slack/interactions`
- `GET, POST` `/api/teams` [AUTH]
- `GET` `/api/teams/:id/audit-log` [AUTH]
- `GET, POST, PATCH` `/api/teams/:id/exceptions` [AUTH]
- `GET, POST, PATCH, DELETE` `/api/teams/:id/members` [AUTH]
- `GET, POST` `/api/teams/:id/projects` [AUTH]
- `GET, PATCH, DELETE` `/api/teams/:id/projects/:projectId` [AUTH]
- `POST` `/api/teams/:id/projects/:projectId/report` [AUTH]
- `GET, POST` `/api/teams/:id/projects/:projectId/scans` [AUTH]
- `GET` `/api/teams/:id/projects/:projectId/scans/latest` [AUTH]
- `GET` `/api/teams/:id/report` [AUTH]
