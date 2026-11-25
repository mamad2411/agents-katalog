---
name: pocketbase-backend
description: Single-file backend with PocketBase
version: 1.0.0
tags: [backend, database, auth, realtime]
---

# PocketBase – Single-File Backend

PocketBase is a Go-based backend in a single executable with
embedded database, authentication, file storage, and admin UI.

- **GitHub**: github.com/pocketbase/pocketbase (45 000+ ⭐)
- **License**: MIT
- **Security**: Single binary — minimal attack surface. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{POCKETBASE_URL}}` | Base URL of PocketBase |

## Usage Examples

### List records

```bash
curl -s "{{POCKETBASE_URL}}/api/collections/tasks/records"
```

### Create a record

```bash
curl -s -X POST "{{POCKETBASE_URL}}/api/collections/tasks/records" \
  -H "Content-Type: application/json" \
  -d '{"title": "New task", "status": "pending"}'
```

### Authenticate

```bash
curl -s -X POST "{{POCKETBASE_URL}}/api/collections/users/auth-with-password" \
  -H "Content-Type: application/json" \
  -d '{"identity": "user@example.com", "password": "secret"}'
```

## AI Agent Tips

- Single ~15MB executable — zero dependencies.
- Built-in SQLite database with full-text search.
- Real-time subscriptions via SSE.
- Admin dashboard at /_/ for managing collections.
