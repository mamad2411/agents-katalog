---
name: regen-api
description: Regenerate openapi.json and the frontend types after a change to a route or schema of the Django API (django-ninja). Use as soon as a schema or a route changes.
---

In a repo not yet updated to ion-repo, these variables are still named `KILN_…` (`KILN_VPS` for `ION_REPO_VPS`): use the one that is set.
Repo settings: !`env | grep -E '^(KILN_(BACKEND_DIR|FRONTEND_DIR|TEST_ENV)|PROJET_(BACK|FRONT|ENV_TEST))=' | sort`
(`PROJET_BACK`, `PROJET_FRONT`, `PROJET_ENV_TEST` in repos generated before kiln 0.4.)

From the root of the repo (or of the current worktree):
1. `cd $ION_REPO_BACKEND_DIR && set -a && . ../$ION_REPO_TEST_ENV && set +a && uv run python manage.py export_openapi --output ../openapi.json`
2. `cd $ION_REPO_FRONTEND_DIR && pnpm generate:api` (regenerates the frontend types and constraints).
3. Show `git diff --stat openapi.json $ION_REPO_FRONTEND_DIR` and point out added or removed routes.
   Commit these files with the backend change: CI fails otherwise.
