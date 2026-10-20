---
name: worktree-env-file-isolation
description: Per-git-worktree environment files (.env.worktree) with deterministically derived unique database names and ports, sharing one Postgres container.
category: devops
version: 1.0.0
tags: [git-worktree, env, dev-setup, postgres, makefile]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Multi-worktree workflow (several concurrent feature branches as parallel directories).
- You want one shared Postgres container but isolated DBs per worktree.
- You need deterministic port allocation (worktree always gets the same port) so bookmarks survive across days.

## Steps

1. Makefile logic prefers `.env` (main checkout) over `.env.worktree` (worktree checkout):
   ```makefile
   MAIN_ENV_FILE ?= .env
   WORKTREE_ENV_FILE ?= .env.worktree
   ENV_FILE ?= $(if $(wildcard $(MAIN_ENV_FILE)),$(MAIN_ENV_FILE),$(if $(wildcard $(WORKTREE_ENV_FILE)),$(WORKTREE_ENV_FILE),$(MAIN_ENV_FILE)))

   ifneq ($(wildcard $(ENV_FILE)),)
   include $(ENV_FILE)
   endif
   ```
2. Create a `scripts/init-worktree-env.sh` that derives unique values from the worktree path:
   ```bash
   WORKTREE_DIR="$(basename "$PWD")"
   SLUG="$(printf '%s' "$WORKTREE_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g; s/__*/_/g; s/^_//; s/_$//')"
   HASH="$(printf '%s' "$PWD" | cksum | awk '{print $1}')"
   PORT_OFFSET=$((HASH % 10000))
   cat > "$1" <<EOF
   POSTGRES_DB=myapp_${SLUG}_${PORT_OFFSET}
   POSTGRES_PORT=5432
   PORT=$((10000 + PORT_OFFSET))
   FRONTEND_PORT=$((13000 + PORT_OFFSET))
   DATABASE_URL=postgres://myapp:myapp@localhost:5432/myapp_${SLUG}_${PORT_OFFSET}?sslmode=disable
   EOF
   ```
3. Add a `make worktree-env` target that refuses to overwrite an existing file:
   ```makefile
   worktree-env:
       @bash scripts/init-worktree-env.sh .env.worktree
   ```
   Add a `FORCE=1` escape hatch inside the script for regeneration.
4. `scripts/ensure-postgres.sh` reads `POSTGRES_DB` from the selected env file and idempotently creates it:
   ```bash
   docker compose up -d postgres
   docker compose exec -T postgres psql -U myapp -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || \
     docker compose exec -T postgres psql -U myapp -d postgres -c "CREATE DATABASE \"$POSTGRES_DB\""
   ```
5. Document the hard rule in CONTRIBUTING: worktrees MUST NOT contain a `.env`. A stray `.env` in a worktree accidentally points it at the main DB.

## Example

```bash
git worktree add ../myapp-feat-x -b feat/x main
cd ../myapp-feat-x
make dev       # auto-runs worktree-env + setup + start
# Backend on port 18742, DB myapp_myapp_feat_x_742
```

Both main and worktree can run at the same time on different ports pointing at different DBs in the same shared Postgres container.

## Caveats

- Port offset uses `cksum % 10000`; collisions are theoretically possible if two worktrees produce the same hash — increase to `% 65535` and stop near the ephemeral range for real safety.
- `make worktree-env` must refuse overwrite by default so `make dev` in an existing worktree doesn't reshuffle ports.
