---
name: tina-schema-sync
version: 1.0.0
description: Synchronize TinaCMS schema changes by regenerating local artifacts and committing them. Use when the Tina schema (tina/config.ts) has been modified, when adding new block types or collection fields, or when tinacms build fails with "Unable to seed" errors. Triggers on "sync tina", "rebuild tina", "tina schema changed", "regenerate tina artifacts", "tina lock file", or after any edit to tina/config.ts.
---

# TinaCMS Schema Sync

Regenerate TinaCMS artifacts locally and commit them after schema changes. This handles the hybrid deployment strategy where `tinacms build` is skipped on Vercel and artifacts are pre-committed.

## When to Use

- After editing `tina/config.ts` (adding fields, blocks, collections)
- After upgrading `@tinacms/cli`
- When `pnpm tina:build` fails with "Unable to seed" (content references unknown block types)
- When Vercel deploys succeed but new blocks don't render

## Prerequisites

- TinaCloud credentials in `.env.local`:
  ```
  NEXT_PUBLIC_TINA_CLIENT_ID="..."
  TINA_TOKEN="..."
  ```
- If `.env.local` doesn't exist, run `./scripts/pull-secrets.sh` or copy from `.env.example` and fill in values from TinaCloud dashboard.

## Procedure

### Step 1: Source credentials

```bash
source .env.local
```

Verify they're set:
```bash
echo $NEXT_PUBLIC_TINA_CLIENT_ID | head -c 10
echo $TINA_TOKEN | head -c 10
```

### Step 2: Run the dev server to regenerate artifacts

```bash
NEXT_PUBLIC_TINA_CLIENT_ID="$NEXT_PUBLIC_TINA_CLIENT_ID" \
TINA_TOKEN="$TINA_TOKEN" \
npx tinacms dev --noWatch --noTelemetry
```

Wait for "TinaCMS Dev Server is active" message, then stop the server (Ctrl+C or kill the process).

**Why `tinacms dev` instead of `tinacms build`?** The build command connects to TinaCloud for indexing. If the content already references new block types that TinaCloud's schema doesn't know about, the build fails with "Unable to seed." The dev server generates artifacts locally without requiring TinaCloud to re-index first.

### Step 3: Verify artifacts were regenerated

```bash
git status tina/
```

You should see changes in:
- `tina/__generated__/client.ts`
- `tina/__generated__/types.ts`
- `tina/tina-lock.json`

Also check `public/admin/` for changes.

### Step 4: Verify new types exist

If you added a new block type (e.g., `ContentTypes`):
```bash
grep "ContentTypes" tina/__generated__/types.ts
```

### Step 5: Commit all three artifact groups

```bash
git add tina/__generated__/ tina/tina-lock.json public/admin/
git commit -m "chore(tina): regenerate artifacts for [describe schema change]"
```

**Critical:** `tina/tina-lock.json` is the file TinaCloud reads to understand the schema on deploy. If you commit generated types but forget the lock file, deploys will fail or new block types will not render.

### Step 6: Push

```bash
git push
```

TinaCloud picks up the lock file from the pushed commit and indexes the schema correctly.

## Agentic Workflow & Vibe Coding

- **Iterative Syncing:** Do not expect the schema to sync perfectly on the first try if there are complex field dependencies. If the dev server throws an error or artifacts don't generate, isolate the specific schema error, fix exactly one collection or field definition, and rerun the sync process until successful.
- **Vibe Coding:** Create local, semantic commits for your working `tina/config.ts` changes *before* running the sync process, and then commit the generated artifacts separately once the sync succeeds. This ensures you can easily roll back if the generation fails.

## Troubleshooting

### "Unable to seed content/pages/home.mdx"
The content file references a block type the cloud schema doesn't know about. This is the exact scenario this skill handles. Use `tinacms dev` (Step 2), not `tinacms build`.

### Dev server won't start
- Check credentials are set (Step 1)
- Check port 4001 isn't in use: `lsof -i :4001`
- Check port 6970 isn't in use: `lsof -i :6970`

### Types generated but lock file unchanged
The schema change may not have been saved. Verify `tina/config.ts` was written before running the dev server.

## Checklist

Before pushing, verify:
- [ ] `tina/__generated__/client.ts` has changes
- [ ] `tina/__generated__/types.ts` has new type definitions
- [ ] `tina/tina-lock.json` has changes
- [ ] `public/admin/` updated (if applicable)
- [ ] All four are staged and committed together
