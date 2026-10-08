# Skill: db-migration

Safely generates, reviews, and applies Alembic database migrations.

## When to Use
- Adding new tables or columns
- Renaming columns (with a deprecation plan)
- Adding indexes or constraints
- Removing deprecated columns (after safe deprecation window)

## Steps

1. **Understand the schema change**
   - What model changed in `app/models/`?
   - Is this additive (safe) or destructive (risky)?

2. **Generate the migration**
   ```bash
   alembic revision --autogenerate -m "description_of_change"
   ```

3. **Review the generated file** (never skip this)
   - Check `upgrade()` matches what you intend
   - Check `downgrade()` is correct and reversible
   - Watch for: dropped columns, renamed columns, changed types
   - Autogenerate misses: partial indexes, custom constraints, enum changes

4. **Test the migration**
   ```bash
   alembic upgrade head      # apply
   alembic downgrade -1      # verify rollback works
   alembic upgrade head      # re-apply
   ```

5. **Run tests** after applying migration:
   ```bash
   pytest -x -v
   ```

## Safety Rules
- Never apply a migration that lacks a working `downgrade()`
- Never drop a column that is still referenced in code
- Rename columns in two releases: add new → migrate data → remove old
- Large table migrations (>1M rows) need `--lock-timeout` and offline strategy

## Output
Report: migration filename, what it does, whether downgrade was tested, any risks.
