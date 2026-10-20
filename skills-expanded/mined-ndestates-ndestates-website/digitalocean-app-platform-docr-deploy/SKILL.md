---
name: digitalocean-app-platform-docr-deploy
description: >
  Full skill for ndestates-io hosting on DigitalOcean (droplet for control and/or App Platform for managed) including CI deployment (GitHub Actions), safe database updates/migrations, and integrated drift avoidance (via project-drift-guardian, model-schema-check, schema-audit, evals). Covers hardened containers to DOCR, token scopes, pre/post checks, backups, verification. Use for initial setup, troubleshooting, workflow creation, or any deploy/DB task. Enforces "avoid drift at all costs".
argument-hint: 'Task (e.g. "setup CI for App Platform + droplet option", "safe DB migrate before deploy", "debug image drift on DO", "create droplet provisioning")'
user-invocable: true
disable-model-invocation: false
---

# DigitalOcean Hosting, CI Deploy & DB Update for ndestates-io (with No-Drift Guards)

**Goal for ndestates-io:** Reliable hosting of the Laravel e-sign platform (canvas signatures, PDF embed/audit, token roundtrips, Filament admin) on DigitalOcean. Support both:
- **Droplet** (traditional VM: full control, e.g. Docker or native PHP-FPM + nginx + managed or local DB; more ops but flexible).
- **App Platform** (managed: easy auto-deploys from DOCR containers, scaling, built-in features; use limited-scope tokens, pair with managed DB or separate).

**Core mandate:** Every change (code, container, DB schema/migration, infra) goes through drift detection gates (project-drift-guardian for scope/code/container, model-schema-check + schema-audit-agent for DB, pre/post evals). CI + deploys + DB updates are never ad-hoc. Always cache-first, use guardrails, backup before DB, verify after, log everything.

This skill supersedes/enhances the prior stub version. It is self-contained, references existing ndestates-io skills (prod-db-maintenance, git-workflow-guardrails, github-expert, security-audit-agent, eval/maintenance-task, ddev-local-runtime for prep, cache-efficient/load for efficiency), and provides full CI yaml examples (create in .github/workflows/ since none exist yet), one-liners, procedures for both hosting targets, and drift integration.

## Mandatory Start (cache + context, per all ndestates-io skills)
1. `.github/prompts/load-project-cache-first.prompt.md` (or cache-efficient) — load INDEX, docs/codebase/ (especially ARCHITECTURE, STRUCTURE, CONCERNS for e-sign flows + hosting risks, INTEGRATIONS/STACK for DO/PDF), TODO-2026-06-14.md, prior evals.
2. `.github/skills/project-drift-guardian/SKILL.md` (or drift-check) — run scope/branch/requirements alignment. This is non-negotiable for "avoid drift at all costs".
3. Cross-load: branch-context-agent, github-expert (for workflows/CI), git-workflow-guardrails (before any push), prod-db-maintenance or DB skill (for updates), model-schema-check + schema-audit-agent (DB drift), security-audit-agent (e-sign PII, tokens, uploads), ai-engineering-maturity (track progress to Stage 6 agent slots for deploys).
4. Confirm current state: git status --short (baseline), current DO target (droplet ID or App Platform app ID from doctl or .env), last known clean DB state (from cache/TODO).

Never proceed without these. Update shared assets (TODO, requirements in drift DB, docs/codebase/) after.

## ndestates-io Hosting Options on DO
**App Platform (recommended starting point for simplicity):**
- Containerized (hardened image pushed to DOCR = DigitalOcean Container Registry).
- Auto-deploy on image push or GitHub integration.
- Pair with App Platform managed DB (Postgres/MySQL) or separate (to limit token scopes — see below).
- Pros: managed runtime, easy scaling, built-in certs/monitoring.
- Cons: less "bare metal" control than droplet; watch for cold starts or limits.

**Droplet (for full control or cost/custom needs):**
- VM (Ubuntu etc.) with Docker (compose for app + optional sidecars) or native (php-fpm, nginx, supervisor).
- Provision via doctl compute droplet create + user-data/cloud-init (or existing image).
- Deploy: push image or code (prefer container for parity with App path), pull/restart on droplet (use doctl or limited SSH; prefer no-ssh patterns from facebook-stats/google-stats skills).
- DB: managed DO DB (connect via private network) or self-managed on droplet (less ideal for prod).
- Pros: full control, can run exactly like local DDEV parity.
- Cons: you manage OS, updates, scaling, backups, monitoring, uptime.

**Shared principles (no drift):**
- Same container/image where possible (build once, run on droplet or push to DOCR for App).
- CI is the single path to prod (never manual `doctl apps deploy` or `scp` without going through checks).
- DB changes: only via migrations + guarded update (never direct prod edit). Always backup + pre-schema check + post-verify (signature data integrity samples) + eval.
- Token scopes: for App + registry only (r/w). Avoid broad account or full DBaaS tokens (use the pattern that isolates).
- Drift blocks: any mismatch (code vs requirements DB, model vs live schema, running image tag vs expected, unapproved scope in deploy) stops the pipeline.
- Hardening: non-root, minimal layers, HEALTHCHECK, vendor prune, SBOM + Trivy in CI, Cosign if possible.
- Observability: DO monitoring/alerts + app logs (signing failures, token usage). Post-deploy reports.

## CI Deployment (GitHub Actions — create these in .github/workflows/)
No workflows exist yet in ndestates-io (as of scan). This skill provides the foundation. Create:
- `.github/workflows/ci-ndestates-io.yml` (tests + checks + build).
- `.github/workflows/deploy-ndestates-io.yml` (or combined; triggered on main or manual with guards).

**Example ci-ndestates-io.yml skeleton (adapt; put real version in repo):**
```yaml
name: CI ndestates-io
on: [push, pull_request]
jobs:
  test-and-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Drift / scope gate (project-drift-guardian)
        run: |
          # Simulate or use script; in practice call equivalent or have job that runs the sh with DB
          ./.github/skills.github/skills/project-drift-guardian/SKILL.md/scripts/drift-check.sh --branch ${{ github.ref_name }} --scope "e-sign + CI"
          # Fail on drift
      - name: PHP/Laravel setup + DDEV-like checks (or direct)
        # Use setup-php, composer install --no-dev, etc.
      - name: Schema / model drift (model-schema-check equivalent)
        run: php artisan migrate:fresh --seed && php artisan test or custom check
      - name: Pest tests + security basics
        run: ./vendor/bin/pest
      - name: Security audit (security-audit-agent context)
        run: composer audit || true
      - name: Build hardened image (for DOCR or droplet)
        run: |
          docker build -t ndestates-io:${{ github.sha }} -f Dockerfile .
          # Trivy, SBOM, etc.
      - name: (Optional for App) Push to DOCR (needs secrets)
        # Only on main or protected
```

**Example deploy-ndestates-io.yml skeleton (guarded, with DB option):**
```yaml
name: Deploy ndestates-io (App + optional droplet path)
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      target:
        description: 'droplet or app-platform'
        required: true
        default: 'app-platform'
      run_db_update:
        description: 'Run safe DB update first?'
        required: false
        default: 'false'
jobs:
  drift-and-prep:
    # ... run project-drift-guardian, model-schema-check, git-workflow-guardrails checks ...
  build-push:
    needs: drift-and-prep
    # build hardened, push to DOCR (for App) or prepare for droplet
    # Use production env secrets only
  db-update-if-needed:
    if: github.event.inputs.run_db_update == 'true'
    needs: build-push
    # Call pattern from prod-db-maintenance: backup first (doctl or managed), pre-check, apply migration, post-verify + .github/skills/eval/maintenance-task/SKILL.md equivalent
    # Never on un-gated paths
  deploy-app:
    if: needs... && target == 'app-platform'
    # doctl apps deploy $DO_APP_ID --wait  (or GitHub integration)
    # Or trigger via registry push if using deploy_on_push
  deploy-droplet:
    if: ... target == 'droplet'
    # doctl compute or limited deploy (e.g. docker pull + restart via user-data or agent)
    # Prefer patterns from digitalocean-no-ssh-hardened-deploy in other projects
  post-deploy:
    # Run drift re-check, eval-maintenance-task (for DB or general), security spot check, update requirements DB via guardian, notify
    # Fail the workflow (and block future) if post-checks show new drift
```

**Key CI/deploy rules (enforce via this skill + guardrails):**
- All deploys from main (or explicit dispatch with approvals).
- Mandatory gates before any image push or deploy: project-drift-guardian (scope + code + container), model/schema checks, tests, security-audit.
- For DB: separate guarded job (see below). Require explicit input or label. Always backup + verify.
- Image: hardened (see below), pinned or controlled tag (avoid pure floating in critical paths; use git-sha + promote to production-latest only after gates).
- Secrets: only in protected envs (production). Use `gh secret set` safely.
- Token scopes: registry+app (read/write). No full account or unnecessary DBaaS in the deploy token.
- Observability: jobs must produce reports (drift report, eval output) logged/attached.
- Rollback: easy revert via previous image/tag or DB backup restore. Document in runbooks.
- After any change to these workflows or Dockerfile: run git-workflow-guardrails.

**Hardened Dockerfile expectations (for both paths):**
- Multi-stage, non-root user, minimal base (alpine or slim + explicit libc), vendor prune for prod, HEALTHCHECK, labels for SBOM/tracing.
- Example (adapt from existing digitalocean skill + other projects' hardened ones):
  (Provide a solid example in the actual repo; skill can reference or inline a template.)
- CI must run Trivy/SBOM/cosign (keyless where possible) and fail on critical vulns.

## Database Updates (safe, integrated, no-drift)
Use /prod-db-maintenance (or the specific safe-db skill you create) as the agent slot for updates/imports.

**Procedure (never skip):**
1. Prep locally (ddev exec per ddev-local-runtime): make migration, test in DDEV (test DB), `ddev export-db --gzip --file=backups/ndestates-io-$(date +%F).sql.gz`.
2. Run guardian + schema checks (project-drift-guardian + model-schema-check + schema-audit-agent) against current prod state (via doctl dump or connection).
3. In CI or controlled one-liner (from host with doctl): backup prod first (managed DB snapshot or export), apply migration (artisan migrate in the running container or via job), verify (row counts on key tables, sample signature hashes/records for integrity, no unexpected changes).
4. Invoke eval ( .github/skills/eval/maintenance-task/SKILL.md db-update or equivalent ) — must PASS (define "clean" in cache: expected tables, recent signatures present, no data loss).
5. Log to guardian DB + TODO. Update docs/codebase/CONCERNS if new risks.
6. Only then proceed with code deploy if the DB change was a prerequisite.

**One-liner pattern (adapt from current prod-db-maintenance + ndestates-io notes):**
```bash
# From host with DO creds + .env (DO_APP_ID or cluster, TARGET_*, SSL_CA, CONFIRM_OVERWRITE=YES if full import)
bash .github/skills/.../import_or_migrate.sh  # wrapper that does backup + guarded apply
# Then:
# .github/skills/eval/maintenance-task/SKILL.md --task=db-update --apply-run=true
```
See the existing prod-db-maintenance SKILL.md for the full agent-slot thinking, cache loading, and "one-liner friendly" output. Extend it with ndestates-io specifics (signature data verification, audit table checks).

For initial App Platform DBaaS: use limited tokens; prefer separate managed DB for stricter scopes. For droplet: connect via private network or VPC.

**Drift avoidance for DB:** Any direct prod edit or un-migrated schema change = immediate drift flag + remediation required before further deploys.

## DigitalOcean Specifics & Token Safety
- **DOCR (for App + reusable for droplet):** Push only from CI with limited registry token. Use `production-latest` or sha promotion after all gates (including this guardian + evals).
- **App Platform:** `doctl apps deploy $APP_ID` or GitHub DO integration (point at DOCR). Limited token (registry + app; avoid DBaaS if using separate DB).
- **Droplet:** `doctl compute droplet create ... --user-data cloud-init.yml` (for initial; include docker or php setup). For updates: image pull + restart (container preferred for parity). Monitor with DO agent.
- **Secrets:** Use GitHub env secrets + `gh secret set --env production`. For runtime: App Platform env or droplet user-data / 1password / DO secrets manager.
- **Networking:** Private for DB where possible. VPC for droplets.
- **Cost/observability:** Note in reports. Use DO monitoring + alerts for app health / signing volume anomalies.
- Failure modes (common, from skill): token scope errors (too broad or insufficient), image pull failures (tag drift), DB connection (wrong CA or network), cold starts on App, drift after manual edits.

Reference the "common failure modes table" from source patterns + add ndestates-io specifics (e.g., signature data loss on bad migrate, token roundtrip breakage on deploy misconfig).

## Procedures Summary (end-to-end with drift)
1. Work on feature branch. Run guardian + cache load early.
2. Make change (code, migration, Dockerfile, workflow).
3. Local verify (DDEV, tests, schema checks).
4. Push PR: CI runs full gates (tests + drift + schema + security).
5. Approve + merge (guardrails).
6. (If DB) Run guarded update (backup + check + apply + verify + eval).
7. CI/deploy job: build/push (DOCR or prepare), deploy (App or droplet), post checks (re-guardian, eval, security spot).
8. Log everything. Update requirements/TODO. Re-run guardian to confirm clean state.
9. Monitor (DO + app logs). Any anomaly → treat as potential drift.

All one-liners and steps must come from (or be validated by) this skill + the called specialists after cache load.

## After Any Change to This Area
- Run git-workflow-guardrails.
- Update this skill + docs/codebase/ + drift requirements DB.
- Test the full path (perhaps with a staging App or test droplet).

## References & Integration
- Existing ndestates-io: prod-db-maintenance (DB), git-workflow-guardrails + github-expert (CI/delivery), model-schema-check + schema-audit-agent + security-audit-agent (drift + safety), eval/maintenance-task (verification), cache-efficient + load-project-cache-first, ddev-local-runtime (local prep), project-drift-guardian (this + scope/code/container).
- DO docs + doctl.
- Patterns from facebook-stats/google-stats (hardened/no-ssh deploys), lightstone/mailchimp (drift + push guardrails), jerseyhouseprices origin (prod-db + eval).
- Create supporting .github/workflows/ using the examples above.
- Hardened Dockerfile + any runbooks in docs/.

This makes ndestates-io's journey to DigitalOcean (droplet and/or App) safe, repeatable, and drift-free by design. Invoke this skill for any related task. Combine with the project-drift-guardian for the "at all costs" enforcement.

(Full content draws from inspected patterns across projects while being specific to ndestates-io's e-sign needs, current skills, and "droplet and/or app" + CI + DB + no-drift requirements.)