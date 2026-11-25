---
name: migration-skill
description: Handle framework migrations (JS→TS, REST→GraphQL), database migrations, and version upgrades with safe rollback strategies. Use when the user mentions "Migrate to TypeScript", "Upgrade framework", or related tasks.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Migration Skill

Handle database migrations, framework upgrades, and schema changes with safe rollback strategies across NestJS (Prisma) and Python/Django services.

## When to Use

- Adding, altering, or removing database tables/columns
- Running or generating Prisma or Django migrations
- Upgrading NestJS, Django, or major dependency versions
- Converting between paradigms (JS to TS, REST to GraphQL)
- Resolving migration drift or conflicts between environments

## Prisma Migrations (NestJS / Core Service)

### Generate and apply a migration (development)

```bash
cd services/core-service
npx prisma migrate dev --name add_user_email_verified
```

### Apply pending migrations (production / CI)

```bash
npx prisma migrate deploy
```

### Handling drift

When the database schema diverges from the migration history:

```bash
# Compare current DB state with migration history
npx prisma migrate diff --from-migrations ./prisma/migrations --to-schema-datamodel ./prisma/schema.prisma

# Reset only in development — NEVER in production
npx prisma migrate reset
```

## Django Migrations (AI Service)

### Standard workflow

```bash
cd services/ai-service
python manage.py makemigrations app_name
python manage.py migrate
```

### Data migrations (separate from schema migrations)

```bash
python manage.py makemigrations --empty app_name -n populate_default_categories
```

```python
# In the generated migration file
from django.db import migrations

def forwards(apps, schema_editor):
    Category = apps.get_model("app_name", "Category")
    Category.objects.bulk_create([
        Category(name="General"),
        Category(name="AI"),
    ])

def backwards(apps, schema_editor):
    Category = apps.get_model("app_name", "Category")
    Category.objects.filter(name__in=["General", "AI"]).delete()

class Migration(migrations.Migration):
    dependencies = [("app_name", "0005_add_category_model")]
    operations = [migrations.RunPython(forwards, backwards)]
```

### Squash migrations when history grows long

```bash
python manage.py squashmigrations app_name 0001 0010
```

## Safe Migration Patterns (Zero-Downtime)

Follow a multi-step deploy strategy for any non-trivial schema change:

1. **Add column as nullable** (no default constraint yet)
2. **Deploy code** that writes to the new column
3. **Backfill** existing rows in batches
4. **Add constraint** (NOT NULL, unique, etc.) once all rows are populated

### Avoid table locks on large tables

```sql
-- BAD: locks the entire table
ALTER TABLE users ADD COLUMN bio TEXT NOT NULL DEFAULT '';

-- GOOD: add nullable first, backfill, then set NOT NULL
ALTER TABLE users ADD COLUMN bio TEXT;
-- backfill in batches of 1000
UPDATE users SET bio = '' WHERE bio IS NULL AND id BETWEEN $1 AND $2;
ALTER TABLE users ALTER COLUMN bio SET NOT NULL;
```

For PostgreSQL indexes, always use `CONCURRENTLY`:

```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);
```

## Rollback Strategies

| Scenario | Prisma | Django |
|----------|--------|--------|
| Dev reset | `prisma migrate reset` | `python manage.py migrate app_name zero` |
| Reverse one migration | Not natively supported; write a counter-migration | `python manage.py migrate app_name 0004` |
| Production rollback | Deploy previous code + counter-migration | Deploy previous code + reverse migration |

Always test rollback in staging before applying to production.

## Framework Upgrades

### NestJS version bump

```bash
cd services/core-service
npx npm-check-updates -u --target minor   # minor bumps first
npm install
npm test                                    # verify nothing broke
npx npm-check-updates -u --target latest   # then major bumps
npm install
npm test
```

### Django version bump

```bash
cd services/ai-service
pip install Django==5.x --upgrade
python manage.py check --deploy
pytest
```

### Dependency audit

```bash
# NestJS
npm audit
npx npm-check-updates --doctor  # runs tests after each upgrade

# Python
pip-audit
safety check
```

## Anti-Patterns

- **Destructive migrations without backup** -- always snapshot the database before running `DROP` or `ALTER` in production
- **Skipping migration tests** -- run `prisma migrate deploy` or `python manage.py migrate` in CI against a test database
- **Mixing schema and data in one migration** -- separate them so rollbacks are clean
- **Running `prisma migrate reset` in production** -- this drops and recreates the database
- **Renaming columns directly** -- use add-copy-drop pattern to avoid breaking running instances
- **Large backfills in a single transaction** -- batch updates to avoid long-running locks

## Checklist

- [ ] Migration file generated and reviewed
- [ ] Reverse/rollback migration tested locally
- [ ] No destructive changes without a backup plan
- [ ] Schema and data migrations are in separate files
- [ ] Large table changes use `CONCURRENTLY` or batched updates
- [ ] CI pipeline runs migrations against a test database
- [ ] Framework upgrade includes full test suite pass
- [ ] Dependency audit shows no critical vulnerabilities
