---
name: directus-cms
description: Headless CMS and data platform with Directus
version: 1.0.0
tags: [cms, database, api, headless]
---

# Directus – Open Data Platform

Directus wraps any SQL database with a real-time REST/GraphQL API,
admin dashboard, and authentication — an instant headless CMS.

- **GitHub**: github.com/directus/directus (30 000+ ⭐)
- **License**: BSL → GPL-3.0 (after 3 years)
- **Security**: Enterprise-grade. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{DIRECTUS_URL}}` | Base URL |
| `{{DIRECTUS_TOKEN}}` | Static or bearer access token |

## Usage Examples

### List items

```bash
curl -s "{{DIRECTUS_URL}}/items/articles" \
  -H "Authorization: Bearer {{DIRECTUS_TOKEN}}"
```

### Create an item

```bash
curl -s -X POST "{{DIRECTUS_URL}}/items/articles" \
  -H "Authorization: Bearer {{DIRECTUS_TOKEN}}" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Article", "body": "Content here"}'
```

## AI Agent Tips

- Auto-generates REST and GraphQL APIs from any SQL database.
- Admin app provides no-code data management.
- Flows system for event-triggered automation.
- Supports PostgreSQL, MySQL, SQLite, MSSQL, OracleDB.
