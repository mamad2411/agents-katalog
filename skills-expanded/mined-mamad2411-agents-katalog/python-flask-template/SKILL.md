# Cursor Instructions — python-flask-template

This is the canonical Python service template for the `pci-tamper-protect` organization.
See `docs/SDLC.md` for the full SDLC reference. Key points are summarized below.

## Repository Topology

Shared work belongs in upstream repos — never duplicate across service repos:
- `pcioasis-ops/gcp/` and `pcioasis-ops/github/` — infra and ops scripts
- `pcioasis-ops/secrets/` — dotenvx support scripts and key rotation tooling
- `ptp-shared-lib` — shared Python: data models (Pydantic), HTTP clients, logging utils
- Individual repos import from shared libs; they wrap, not duplicate

## Directory Structure

```
app/               Flask application (default)
app_fastapi/       FastAPI alternative scaffold
agents/            Agentic workflow scripts
deploy/cloudrun/   Cloud Run service definitions and deploy scripts
docs/              Documentation including SDLC.md
tests/             pytest suite
.env.dev/.stg/.prd Encrypted dotenvx files (committed to git)
.env.keys          dotenvx private keys (NEVER commit — in .gitignore)
CLAUDE.md          Claude Code project context
```

## Framework Options

- **Flask** (default, this template): use for standard REST APIs
- **FastAPI** (`app_fastapi/`): use for async, high-throughput, or typed APIs; reference: `ptp-crawl`

## Environment & Secrets

```bash
# dotenvx encrypted env files are committed to git
dotenvx encrypt -f .env.dev
dotenvx run -- python run.py  # decrypt at runtime

# Private keys
# - local: .env.keys (gitignored)
# - CI/CD: DOTENV_PRIVATE_KEY_DEV/STG/PRD in GitHub Actions secrets
# - Cloud Run: dotenv-private-key-<env> in GCP Secret Manager
```

Environments: `dev` / `stg` / `prd` (never `development`, `staging`, `production`)

## Deployment

```bash
./deploy/cloudrun/deploy.sh stg    # build + push + deploy to staging
./deploy/cloudrun/deploy.sh prd    # requires typed confirmation
```

Primary: GCP Cloud Run. Public: Cloud Run behind Cloudflare.
Container registry: `us-central1-docker.pkg.dev/pcioasis-operations/containers`

## Naming Conventions

- Service name: `<service>-[<grouping>]-[<type>]-<env>`
  - e.g., `profile-accounts-api-stg`, `payments-data-dev`
- Types: `api` / `svc` / `data`

## API Design

- All routes under `/api` prefix
- Health: `GET /api/health` (liveness), `GET /api/ready` (readiness)
- Proper HTTP status codes; structured JSON error responses
- Validate all external input at boundaries (Pydantic or marshmallow)

## Agentic Flows

- Claude (local / high-level): complex reasoning, orchestration
- Azure AI Foundry: parallelizable lower-level tasks (reference: `ptp-crawl`)
- Scripts in `agents/`; SDLC review agent: `agents/sdlc_review.py`

## Real-time Patterns

- **Pub/Sub**: service-to-service events, async processing
- **Firestore**: document state synced across cold starts or to clients

## Git & CI

- `main` is branch-protected; requires CI pass + 1 review
- Pre-commit: `black`, `isort`, `flake8`, `mypy`, `pytest`
- GitHub Actions: `ci.yml` (lint+test on PR), `deploy.yml` (build+deploy on merge to main)
- GCP auth in CI: Workload Identity Federation only (no service account key files)

## Security

- Never commit plaintext secrets; always encrypt with dotenvx or use GCP Secret Manager
- `CORS_ORIGINS=*` is forbidden in `stg` and `prd`
- Non-root container user (`appuser`)
- Run `pip audit` or `safety check` in CI
