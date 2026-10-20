# Wolf Goat Pig

Golf wagering app with FastAPI backend and React frontend.

## Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL (Cloud Run + Cloud SQL on GCP)
- **Frontend**: React with hooks, JavaScript/JSX (Firebase Hosting on GCP)
- **Auth**: Auth0
- **Testing**: Jest (frontend), pytest (backend)

## Build & Test

```bash
# Frontend
cd frontend && npm run build
cd frontend && npx vitest run

# Backend env (one venv — `backend/venv`; do NOT use backend/.venv):
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-testing.txt

# Backend
cd backend && pytest

# Type checking
cd backend && mypy app          # advisory only (pre-existing errors)
cd frontend && npm run typecheck
```

## Definition of done — REQUIRED before every push

Pushing to main auto-deploys to GCP when `GCP_AUTO_DEPLOY=true`. The local gate must mirror CI
**exactly** — a subset is not a gate. Run ALL of these and check real exit
codes (don't pipe away failures):

```bash
# Frontend changes (mirrors .github/workflows/frontend-ci.yml):
cd frontend && npm run typecheck && npx vitest run && npm run build
# ⚠️ typecheck is NOT optional — esbuild/vite tolerate syntax tsc rejects,
#    so "build passed" alone has shipped broken code before.

# Backend changes (mirrors .github/workflows/backend-ci.yml):
cd backend && ruff check app/ tests/ && ruff format --check app/ tests/ \
  && python scripts/export_openapi.py --check \
  && pytest tests/ --ignore=tests/manual --ignore=tests/_diagnostic
# If OpenAPI --check fails: ./scripts/sync_openapi.sh then commit both artifacts.
```

Editing rules that prevent past deploy failures:
- NEVER edit source files via shell heredocs/perl when the code contains `!`
  — zsh mangles it to `\!` silently. Use the Edit/Write tools, or a Python
  script written to a file first.
- After any sed/perl/python bulk edit, grep the file for the literal `\!`
  and re-run typecheck.

## Deployment

- Production is GCP: FastAPI → Cloud Run, SPA → Firebase Hosting, booking
  agent → Cloud Run (`wgp-booking`). Auto-deploys via `.github/workflows/deploy-gcp.yml`
  when `GCP_AUTO_DEPLOY=true` (see `deploy/gcp/README.md`).
- Vercel + Render are decommissioned leftovers — do not re-enable
  (`deploy/gcp/DECOMMISSION.md`).
- Local Docker setup via `docker-compose.yml`
- After backend deploys, verify:
  `curl https://wolf-goat-pig-api-i5v2shrpoa-uc.a.run.app/health`
  (`environment` must be `production`; junk Bearer token to `/players/me`
  should return 401, not 500)

## File Organization

- `backend/` - FastAPI application
- `frontend/` - React SPA
- `scripts/` - Deployment, development, diagnostics, and testing scripts

## Code Style

- Modular design: files under 500 lines
- Never hardcode secrets
- No `console.log` in production code
- Separate concerns with clean architecture

## Worktrees — Orca only

Orca is the only owner of checkouts for this repo. Do not create, move, or
remove a worktree any other way.

Never:

- `git worktree add|remove|prune`, `wt`, `.claude/worktrees`, or EnterWorktree
- a session or subagent with `isolation: "worktree"`
- a feature branch checked out in this directory (this checkout stays on main)

If Orca is not running, stop and tell the human. Do not fall back to git.

Start (related to the current task):

```bash
orca worktree create --name <task> --parent-worktree active --base-branch main --json
```

Unrelated work: add `--no-parent` and omit `--base-branch`.

Do all commits and the `gh pr create` inside that checkout. Push the branch
before opening the PR.

Finish, in this order, and do not stop between steps:

1. Working tree clean, branch pushed, PR open. No local-only commits.
2. `cd` back to the main checkout.
3. `orca worktree rm --worktree path:<that-checkout> --json`
4. Confirm with `git worktree list` that only the main checkout remains,
   plus any checkout whose PR is still open.

`--force` only for generated dirt (`frontend/node_modules`, `.ctk/ledger.json`).
Never force-delete a checkout with unpushed commits or an untracked file you
did not generate. If `orca worktree rm` fails, leave the checkout in place and
report the error. A half-removed worktree is the mixed state this rule exists
to prevent.
