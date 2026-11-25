---
name: checklists
description: Universal quality checklists for every development action — feature addition, API endpoint, data model change, logging, secrets, auth. Auto-apply the relevant checklist whenever one of these actions is taken.
user-invocable: false
paths:
  - "**/*"
---

Full checklists in [checklists.md](checklists.md).

**When to apply each checklist — trigger automatically:**

| Action | Checklist |
|---|---|
| Adding any new feature or behaviour | **Feature Addition** |
| Creating or modifying an API endpoint | **API Endpoint** |
| Changing the data model / schema | **Data Model Change** |
| Adding any log statement | **Logging** |
| Adding any secret or credential handling | **Secrets & Credentials** |
| Any code touching authentication or authorisation | **Auth & Authorisation** |

Apply the checklist **before marking work as done**. Every unchecked item is a gap that needs addressing or an explicit decision to skip with a documented reason.

**For tech-specific checklists, see your installed layer skills:**
- React components → `layers/frontend/react/react-standards`
- Express API endpoints → `layers/backend/node-express/nodejs-standards`
- Prisma schema changes → `layers/database/postgres-prisma/database-sql`
- Neon migrations and connection setup → `layers/database/neon`
- Cognito auth → `layers/auth/cognito/cognito-auth`
