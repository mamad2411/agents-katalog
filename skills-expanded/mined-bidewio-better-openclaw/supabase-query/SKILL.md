---
name: supabase-query
description: Interact with Supabase for database, auth, and storage
version: 1.0.0
tags: [database, auth, storage, api, postgres]
---

# Supabase – Open-Source Firebase Alternative

Supabase provides a PostgreSQL database, authentication, instant APIs,
edge functions, realtime subscriptions, and file storage.

- **GitHub**: github.com/supabase/supabase (80 000+ ⭐)
- **License**: Apache-2.0
- **Security**: SOC 2 compliant. Active bug bounty programme. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{SUPABASE_URL}}` | Project API URL |
| `{{SUPABASE_ANON_KEY}}` | Anonymous / public API key |
| `{{SUPABASE_SERVICE_KEY}}` | Service-role key (server-side only) |

## Usage Examples

### Query a table via REST

```bash
curl -s "{{SUPABASE_URL}}/rest/v1/users?select=*" \
  -H "apikey: {{SUPABASE_ANON_KEY}}" \
  -H "Authorization: Bearer {{SUPABASE_ANON_KEY}}"
```

### Insert a row

```bash
curl -s -X POST "{{SUPABASE_URL}}/rest/v1/users" \
  -H "apikey: {{SUPABASE_SERVICE_KEY}}" \
  -H "Authorization: Bearer {{SUPABASE_SERVICE_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

### Upload a file to storage

```bash
curl -s -X POST "{{SUPABASE_URL}}/storage/v1/object/public/avatars/photo.png" \
  -H "Authorization: Bearer {{SUPABASE_SERVICE_KEY}}" \
  -H "Content-Type: image/png" \
  --data-binary @photo.png
```

## AI Agent Tips

- Use the REST API for CRUD; use RPC for custom Postgres functions.
- The anon key is safe for client-side; the service key bypasses Row Level Security.
- Realtime subscriptions require WebSocket connections.
- Edge Functions run Deno on the server side for custom logic.
