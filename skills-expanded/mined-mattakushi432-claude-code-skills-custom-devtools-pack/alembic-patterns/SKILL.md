---
name: alembic-patterns
description: "When to activate: Alembic, database migrations, schema changes, migration scripts, rollback, multi-head"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Alembic Migration Patterns

## Setup with SQLAlchemy async
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models import Base
from app.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    engine = create_async_engine(settings.database_url, poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()

def run_migrations_online() -> None:
    import asyncio
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Common Commands
```bash
# Generate migration (auto-detect model changes)
alembic revision --autogenerate -m "add_users_table"

# Apply migrations
alembic upgrade head       # apply all pending
alembic upgrade +1         # apply next one
alembic upgrade <rev_id>   # apply up to specific revision

# Rollback
alembic downgrade -1       # roll back one
alembic downgrade base     # roll back all

# Inspect
alembic history --verbose  # show history
alembic current            # show current revision
alembic show <rev_id>      # show migration details
```

## Safe Migration Patterns

### Adding nullable column (zero-downtime)
```python
# Step 1: Add as nullable
def upgrade() -> None:
    op.add_column("users", sa.Column("phone", sa.String(20), nullable=True))

# Step 2 (separate migration): backfill data
def upgrade() -> None:
    op.execute("UPDATE users SET phone = '' WHERE phone IS NULL")

# Step 3 (separate migration): make not-null after backfill complete
def upgrade() -> None:
    op.alter_column("users", "phone", nullable=False)
```

### Renaming a column (zero-downtime)
```python
# Step 1: Add new column, copy data
def upgrade() -> None:
    op.add_column("users", sa.Column("full_name", sa.String(200)))
    op.execute("UPDATE users SET full_name = name")

# Step 2 (after code deployed reading both): drop old column
def upgrade() -> None:
    op.drop_column("users", "name")
```

### Adding index without table lock
```python
def upgrade() -> None:
    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        postgresql_concurrently=True,  # CONCURRENTLY avoids table lock
    )
```

## Anti-Patterns
- Editing committed migrations (use a new migration instead)
- Data migrations in schema migrations (separate them)
- `op.drop_column` without confirming no code reads it
- `nullable=False` without a default or backfill
- Using `--autogenerate` and not reviewing the generated migration
