---
name: migration
description: Change the Django database schema - one new numbered migration per change, never a rewrite of a merged migration. Use as soon as a model changes.
---

In a repo not yet updated to ion-repo, these variables are still named `KILN_…` (`KILN_VPS` for `ION_REPO_VPS`): use the one that is set.
Repo settings: !`env | grep -E '^(KILN_(BACKEND_DIR|TEST_ENV)|PROJET_(BACK|ENV_TEST))=' | sort`
(`PROJET_BACK`, `PROJET_ENV_TEST` in repos generated before kiln 0.4.)
Repo rules: those of its instructions (`CLAUDE.md`, `.claude/rules/`) take precedence over these.

Every model change comes with its numbered migration, applied at deployment without emptying the
database. Environment: `set -a && . ../$ION_REPO_TEST_ENV && set +a` from `$ION_REPO_BACKEND_DIR/`.

1. Change the model.
2. In `$ION_REPO_BACKEND_DIR/`: `uv run python manage.py makemigrations <app> --name <meaningful_name>`
   (English, snake_case: `riding_profile`, `station_photo`). The file takes the app's next number.
3. **Never edit or delete a migration already merged into the integration branch**: production
   may have applied it. A mistake is fixed by a new migration. A migration still only on the
   branch can be regenerated.
4. Seed data or data backfill: a data migration (`RunPython`) with its reverse function, in a
   file separate from the schema change.
5. Column removed or renamed while the deployed code still reads it: two deliveries (the code
   stops reading it, then the migration removes it).
6. Check: `uv run python manage.py makemigrations --check --dry-run` (nothing to generate),
   `uv run python manage.py migrate` on the local database, then `charter check` from the root.
7. If an API schema changes too: skill `/django:regen-api`.
