---
description: Keep old workout export/backup files importable forever. Apply when changing portable format, backup parse, or restore.
globs: src/lib/workout-backup.ts,src/lib/workout-export.ts,src/lib/account-backup.ts,src/lib/import-compat.test.ts,src/lib/fixtures/import-compat/**,backend/schemas/portable.ts,backend/lib/portableTemplates.ts,mobile/src/data/local/backup.ts
alwaysApply: false
---

# Import / backup compatibility

People keep `.json` backups and `WKT1-` codes for months. A parser change that
requires a new field, or that rejects a missing one, strands them.

## Rules

1. **New fields are optional.** Default them in `parseBackup` / `parseBundle` /
   `validateBundle`. Never fail the file because a key from a later version is
   absent.
2. **Do not edit frozen fixtures.** Files in `src/lib/fixtures/import-compat/`
   are historical payloads. If you ship a new shape, add a *new* fixture and a
   new case in `src/lib/import-compat.test.ts`.
3. **`portableBundleValidator`** is what Convex import accepts. Extra keys fail
   the server. Required keys fail old files. Add only `v.optional(...)`.
   `import-compat.test.ts` runs that validator on every parsed fixture, so a
   new required field fails the commit, not a user with a two-month-old file.
4. **Restore** (`restoreLocalBackup`) must tolerate `places` / `machines` /
   `placeWeights` missing (`?? []`) and `placeId` / `lastPlaceId` / `machineId`
   null.
5. After changing any of the globs above, run `pnpm test:import-compat`. It
   also runs on every commit via `.husky/pre-commit`. Do not Prettier-format
   the fixture folder — it is in `.prettierignore` on purpose.
