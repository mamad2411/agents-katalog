---
name: follow-service-instantdb-config-instantdb
description: Set/edit InstantDB configuration — `instant.schema.ts`, `instant.perms.ts`, env vars, and push/pull — without clobbering the existing schema
related:
  - follow-service-instantdb
---

## Goal

Set/edit InstantDB configuration — `instant.schema.ts`, `instant.perms.ts`, env vars, and push/pull — without clobbering the existing schema

## Scope

- Edit entities, fields, links, rooms in `instant.schema.ts`
- Define `allow`/`bind` rules in `instant.perms.ts`
- Manage the env app id and `instant-cli push/pull`
- Does not cover SDK install/init → use `workflows/setup-instantdb/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Know the current schema/perms before editing

1. Read the existing `instant.schema.ts` and `instant.perms.ts`
2. Do `/check-secrets env-vars` to identify missing or wrongly prefixed app id vars
3. Run `npx instant-cli@latest pull` if the latest config must be synced from the server before editing
4. If no config files exist at all → do `workflows/setup-instantdb/SKILL.md` instead

### 2. Update Schema

> Goal: Add/edit the data model type-safely

1. Edit `instant.schema.ts` adding entities, fields, links, rooms only where needed — merge, never rewrite the whole file
2. Use `i.entity({ ... })`, `i.string()`, `i.number()`, `i.boolean()`, `i.date()`, and `i.any()` per the docs
3. Mark `.unique()`, `.indexed()`, `.optional()` as required
4. Define links with explicit `forward`/`reverse` labels

### 3. Update Permissions

> Goal: Protect data access with rules

1. Edit `instant.perms.ts` with per-entity, per-action `allow`/`bind` rules (`view`, `create`, `update`, `delete`)
2. Use `auth.id`, `auth.email` in rules — deny by default for sensitive data
3. Bind rules to links such as `data.user` when checking ownership
4. Review rules before push — never expose data accidentally

### 4. Push And Verify

> Goal: apply config and confirm typecheck passes

1. Run `npx instant-cli@latest push schema` when the schema changes
2. Run `npx instant-cli@latest push perms` when permissions change
3. Run `bunx tsc --noEmit` or `bun run build` to typecheck schema types
4. Run `npx instant-cli@latest status` to confirm the connection — if it fails → `resolve-errors` max 3 rounds
5. If new links/rooms exist → update the parent's references and do `/update-references`

## Rules

- Merge only the necessary keys — never overwrite whole schema/perms files
- Never push schema/perms without reviewing the diff first
- Use generated types from `InstaQLEntity<typeof schema, "...">` for type safety
- Never hardcode app id/secrets — use env vars with the framework prefix
- If unsure about a field type/rule syntax → check official docs `https://www.instantdb.com/docs`

## Expected Outcome

- `instant.schema.ts` and `instant.perms.ts` merged and pushed successfully
- Typecheck passes and rules protect sensitive data correctly
- Env vars correct per framework
