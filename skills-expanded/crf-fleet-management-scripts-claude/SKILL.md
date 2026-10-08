# Scripts

Run with: `npx tsx scripts/<name>.ts`

## Rules for all scripts
1. **Idempotent** — safe to run multiple times. Use `CREATE TABLE IF NOT EXISTS`, `INSERT OR IGNORE`, `INSERT OR REPLACE`, or check before altering.
2. **Hardcode local DB** — scripts always target `file:./dev.db` directly (not via env vars).
3. **Document intent** at the top with a JSDoc comment: what it does, when to run it, usage.
4. **Migration scripts** — check for column/table existence before `ALTER TABLE`:
   ```ts
   const cols = await db.execute('PRAGMA table_info(Trip)');
   if (!cols.rows.some(r => r.name === 'newColumn')) {
     await db.execute('ALTER TABLE Trip ADD COLUMN newColumn TEXT');
   }
   ```
5. **Seed scripts** — use `INSERT OR IGNORE` so re-runs don't duplicate data.
6. **IDs** — always `crypto.randomUUID()` for new record IDs.

## Naming
- `add-<feature>.ts` — schema additions (new column/table)
- `migrate-<what>.ts` — data migrations
- `setup-<name>.ts` — environment setup
- `<service>-test.ts` — integration/smoke tests for external services

## After adding a migration script
If the script is a one-time migration that new devs also need, register it in the root `CLAUDE.md` Commands section and in `scripts/setup-dev.ts` if it should run on fresh installs.
