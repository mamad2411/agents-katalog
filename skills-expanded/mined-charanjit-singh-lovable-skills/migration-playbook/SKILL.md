---
name: migration-playbook
description: >-
  Use when changing Supabase schema, adding columns, backfills, or production
  migrations that must not break existing apps. Not for client-only UI or
  seed data in local dev only.
---

# Migration playbook

## Principles

1. **Backward compatible** steps when app is live: add → backfill → switch → remove (later).
2. Never drop column/table in same release as code still reads it.
3. One migration per logical change; name clearly: `20240522_add_posts_status.sql`.

## Safe add column

```sql
ALTER TABLE public.posts ADD COLUMN status text DEFAULT 'draft';
-- backfill if needed
UPDATE public.posts SET status = 'draft' WHERE status IS NULL;
-- then NOT NULL if required, in later migration
```

## RLS

- New tables: enable RLS + policies in same migration.
- Policy changes: test with two users before deploy.

## Breaking changes

If unavoidable:

1. Ship code that reads **both** old and new shapes.
2. Migrate data.
3. Deploy code using new only.
4. Drop old in follow-up migration.

## Client types

- Regenerate TypeScript types after migration.
- Fix compile errors before marking done.

## Avoid

- `DROP COLUMN` on day one of rename.
- Destructive migrations without user confirmation in chat.
- Editing applied migration files in prod — add new file instead.

## Checklist

- [ ] Migration SQL idempotent where possible.
- [ ] RLS updated.
- [ ] Types regenerated.
- [ ] Rollback plan stated (even if "restore backup").
