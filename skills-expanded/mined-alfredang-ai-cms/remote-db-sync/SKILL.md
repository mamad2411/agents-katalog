---
name: remote-db-sync
description: Push local DB content (menus, settings, taxonomy, pages, posts) to the production database via bearer-token-protected sync APIs. Use when the user wants to publish local CMS/admin edits to the live site without logging into the production admin UI, or to extend the sync surface for new tables. Triggers — "push to production", "sync to remote", "deploy menu/settings/page/post", "the live site doesn't show my change".
---

# Remote DB Sync — Tertiary Infotech

This site renders most CMS content from Postgres (menu items, settings, pages, posts, categories, tags). Production runs on a Coolify-provisioned DB that's separate from local development. This skill covers the sync layer that lets you push local DB rows to production over HTTPS.

## Architecture

```
Local Postgres ──► scripts/push-to-remote.ts ──► HTTPS + Bearer token ──► /api/admin/sync/* ──► Remote Postgres
```

- **API surface** (Next.js route handlers, all under [src/app/api/admin/sync/](../../../src/app/api/admin/sync/)):
  - `POST /api/admin/sync/menus` — replaces all items for one menu location.
  - `POST /api/admin/sync/settings` — upserts `(key, value)` rows in the `settings` table.
  - `POST /api/admin/sync/taxonomy` — upserts `categories` and `tags` by `slug`.
  - `POST /api/admin/sync/pages` — upserts `pages` by `slug`; resolves `authorId` by email.
  - `POST /api/admin/sync/posts` — upserts `posts` by `slug`; resolves `authorId` by email, `categoryId` and `tagSlugs` by slug; rewrites `post_tags`.
- **Auth**: all endpoints require `Authorization: Bearer $SYNC_API_TOKEN`. Comparison is constant-time. If `SYNC_API_TOKEN` is unset on the server, the API fails closed (401).
- **CLI**: [scripts/push-to-remote.ts](../../../scripts/push-to-remote.ts) reads the local DB, builds payloads (resolving FKs to portable identifiers — emails for authors, slugs for categories/tags), and POSTs to the production endpoints.

## Setup

1. Generate one shared token:
   ```bash
   openssl rand -hex 32
   ```
2. Set it on **both** local and production:
   - **Local** `.env`:
     ```
     SYNC_API_TOKEN=<token>
     REMOTE_SYNC_URL=https://www.tertiaryinfotech.com
     ```
   - **Production** (Coolify env vars):
     ```
     SYNC_API_TOKEN=<same token>
     ```
3. Redeploy production so the new env var is loaded.

## Usage

```bash
# Single resource
npx tsx scripts/push-to-remote.ts menus
npx tsx scripts/push-to-remote.ts settings
npx tsx scripts/push-to-remote.ts taxonomy
npx tsx scripts/push-to-remote.ts pages
npx tsx scripts/push-to-remote.ts posts

# Multiple
npx tsx scripts/push-to-remote.ts taxonomy posts

# Everything (runs in dependency order: taxonomy → settings → menus → pages → posts)
npx tsx scripts/push-to-remote.ts all
```

The slash command `/push-to-remote` wraps this with safety prompts. See [.claude/commands/push-to-remote.md](../../commands/push-to-remote.md).

## Conventions & Safety

- **Idempotent**: every endpoint upserts. Re-running the same push is a no-op (apart from `updatedAt`).
- **Menus replace, others upsert**: `/api/admin/sync/menus` deletes all items for the target menu before inserting the new set — so local is the source of truth for nav order. Other endpoints upsert by natural key (`slug` or settings `key`) and never delete remote rows.
- **FK portability**: authors are resolved by email, categories and tags by slug. This means the remote DB must have the user account (email) before posts/pages referencing it are pushed. Categories/tags are auto-created by the `taxonomy` endpoint — push that first.
- **No leads, users, or media sync**: leads belong to production only; users are seeded separately for security; media files are binary and need their own pipeline (upload to remote `/api/upload` instead). This skill explicitly stops at content/config tables.
- **Confirmation before pushing destructive operations**: `/menus` is destructive (replace). Always show a diff or summary to the user and confirm before invoking it against production.
- **Bidirectional? No.** This is one-way: local → remote. If production has been edited via the admin UI and you push local on top, you will overwrite those edits. Treat production admin UI as authoritative for ad-hoc fixes; treat local + sync as the canonical pipeline for bulk/scripted changes.

## Extending the API

To sync a new table:

1. Decide the natural key (must be unique and stable — `slug`, `key`, `email`, etc.).
2. Add `src/app/api/admin/sync/<resource>/route.ts`:
   - Import `syncAuthorized` from `@/lib/sync-auth` and guard the handler.
   - Define a Zod schema for the payload. Required string-length and array-size caps; never accept unbounded input.
   - Resolve FKs by natural key, not by numeric id.
   - Use `db.insert(...).onConflictDoUpdate({ target: <unique col>, set: {...} })`.
3. Add a handler in [scripts/push-to-remote.ts](../../../scripts/push-to-remote.ts) and register it in `HANDLERS` + `ORDER` (mind FK dependency order).
4. Document the new resource in this skill file and in [.claude/commands/push-to-remote.md](../../commands/push-to-remote.md).

## Common failure modes

- **`401 Unauthorized` from the endpoint**: the token isn't set on production, or local/prod tokens drift. Verify both env vars and redeploy production.
- **`404 No menu found for location='header'`**: the production DB hasn't been seeded yet. Run `npx tsx scripts/reset-header-menu.ts` against production once (via Coolify's terminal) to create the menu shell, then re-run sync.
- **Post sync silently drops tags**: the tag's `slug` doesn't exist on production. Push `taxonomy` first.
- **`net::ERR_CONNECTION_REFUSED` against localhost**: you forgot to set `REMOTE_SYNC_URL`. The default is *not* localhost — the script will throw if unset.
