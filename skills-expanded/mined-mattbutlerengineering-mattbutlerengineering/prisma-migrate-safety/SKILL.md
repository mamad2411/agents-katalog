# Skill: prisma-migrate-safety

Pre-flight checks before running `prisma migrate deploy` in the users service.

## Workflow

### Step 1: Staging Validation

```bash
# Validate migration against staging DB first
DATABASE_URL=$STAGING_DATABASE_URL npx prisma migrate deploy --preview
```

### Step 2: Migration Checks

```bash
# Check migration integrity
npx prisma migrate status
# Verify no destructive changes without marker
grep -r "DROP TABLE\|DROP COLUMN" prisma/migrations/*/migration.sql | grep -v "^-- DESTRUCTIVE:"
```

### Step 3: Deploy with Rollback Plan

```bash
# Tag current state before deploying
git tag "users-pre-migrate-$(date +%Y%m%d-%H%M%S)"
git push origin --tags
# Deploy
pnpm --dir services/users db:migrate:deploy
```

## Rollback Procedure

```bash
# If migration fails, revert to pre-migration tag
git checkout users-pre-migrate-<tag>
pnpm --dir services/users db:migrate:deploy
```
