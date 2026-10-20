---
name: deployment-platforms
description: Select and operate edge/serverless/container hosting (Cloudflare, Netlify, Render, Vercel, Fly.io) with preview environments, secret hygiene, and safe rollout. Use when choosing a hosting model, standardizing previews, or hardening release workflows.
---

# Deployment Platforms

Pick the smallest platform that fits the workload, then make every deploy reproducible, previewable, and reversible. The platform is a constraint, not a strategy — keep build, runtime, and rollout decoupled so migration stays cheap.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Edge / static + functions | Cloudflare Workers + Pages, Netlify, Vercel |
| Container PaaS | Render, Fly.io, Railway, Azure Container Apps |
| Build runtime | Node 22 LTS, pnpm 10, Bun 1.2 (where supported) |
| Previews | One environment per PR, isolated secrets |
| Secrets | Platform vault + OIDC from CI (no long-lived tokens) |
| IaC | Terraform / OpenTofu providers, Pulumi, sst v3 |
| Observability | OpenTelemetry export, platform logs shipped to a single backend |
| Rollback | Immutable versioned deployments, instant alias swap |

## When to Use
- Choosing between edge, serverless, and container hosting for a new service.
- Replacing dashboard-clicked deploys with reproducible CI flows.
- Adding preview environments per PR without leaking production secrets.
- Establishing a rollback contract before a launch.

## Prerequisites
- Source in Git with branch protection on `main`.
- CI provider that supports OIDC federation (GitHub Actions, GitLab CI).
- A health check endpoint and a smoke test suite.
- Owners assigned to production environment + on-call rotation.

## Inputs the Agent Should Gather
- Workload shape: static, SSR, API, background worker, websocket, stateful.
- Region / data-residency constraints.
- Cold-start tolerance (ms) and request volume profile.
- Database location (co-locate compute with primary).
- Compliance scope (SOC 2, HIPAA, GDPR data boundary).

## Instructions

### 1. Match workload to platform primitive

| Workload | Best fit | Avoid |
| --- | --- | --- |
| Static site + light API | Cloudflare Pages, Netlify, Vercel | Container PaaS (overkill) |
| SSR / RSC framework | Vercel, Netlify, Cloudflare (Workers + Pages) | Pure static hosts |
| Long-running API / websockets | Render, Fly.io, Container Apps | Edge functions (timeouts) |
| Background jobs / cron | Render Workers, Fly Machines, Cloudflare Queues + Workers | Static hosts |
| Globally distributed low-latency reads | Cloudflare Workers + KV/D1, Fly.io multi-region | Single-region container |
| Stateful (Postgres, Redis) | Managed DB + container PaaS in same region | Edge runtimes |

### 2. Standardize the deploy via OIDC from CI
```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  pull_request:
  push: { branches: [main] }
permissions:
  id-token: write   # OIDC
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 10 }
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
      - name: Deploy preview
        if: github.event_name == 'pull_request'
        run: npx wrangler deploy --env preview --name pr-${{ github.event.number }}
      - name: Deploy production
        if: github.ref == 'refs/heads/main'
        run: npx wrangler deploy --env production
```
No static API tokens. Use `cloudflare/wrangler-action`, `vercel`, `netlify deploy --build` with OIDC where available; otherwise scope tokens per environment.

### 3. Preview environments per PR
- Unique URL per PR (`pr-123.preview.example.com`).
- Separate secrets bucket; never share production database.
- Auto-teardown on PR close (TTL job or platform hook).
- Post the preview URL back to the PR via a bot comment.

### 4. Promote, don't rebuild
Build once, deploy the same artifact to staging then production. On Vercel/Netlify use `--prebuilt`; on Cloudflare use Versions + Deployments; on container PaaS push an immutable image digest.

### 5. Make rollback a one-command operation
```bash
# Cloudflare Workers
wrangler deployments list
wrangler rollback <deployment-id>

# Vercel
vercel alias set <previous-deployment> production.example.com

# Render (image tag rollback via API)
curl -X POST https://api.render.com/v1/services/$SVC/deploys \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -d '{"imageUrl":"ghcr.io/org/app@sha256:<previous>"}'
```
Document the exact command in the runbook. Practice it in a game day.

### 6. Wire observability before launch
- Ship platform logs to one backend (Datadog, Grafana Cloud, Honeycomb).
- Export OpenTelemetry traces from app code; rely on platform metrics only as a backup.
- Define the SLI per route; alert on burn rate (see `../../architect/quality-attributes/slo-error-budgets/SKILL.md`).

## Common Pitfalls

| Pitfall | Why it bites | Fix |
| --- | --- | --- |
| Long-lived API tokens in CI | Rotation is forgotten; leaks live forever | OIDC federation, scoped per env |
| Single environment for previews | One PR breaks everyone | One env per PR with isolated secrets |
| Edge runtime for DB-heavy workload | N hops to origin region per query | Co-locate compute with primary DB |
| Dashboard-only config | Drift between envs, no audit trail | Terraform / platform-as-code |
| Rebuilding for each env | Different artifacts → "works in staging" | Build once, promote artifact |
| No rollback drill | First rollback happens during the incident | Practice quarterly |

## Output Format
When recommending a platform, deliver:
1. Selected platform + one-line rationale tied to workload shape.
2. Build + deploy workflow file (CI YAML).
3. Preview env strategy (URL pattern, secret scope, teardown).
4. Rollback command, verified.
5. Observability wiring (log destination, trace exporter, SLI).
6. Cost estimate at expected RPS and the next pricing cliff.

## Abort Criteria
- Workload requires features the platform doesn't offer (e.g., raw TCP on Vercel) — recommend container PaaS instead.
- Compliance scope exceeds platform attestations — escalate to `../../security/compliance-governance/SKILL.md`.
- No telemetry exists — bootstrap observability first.

## Related Skills
- `../cloud-solution-architect/SKILL.md` — broader architecture patterns
- `../../architect/quality-attributes/slo-error-budgets/SKILL.md` — reliability targets
- `../../security/secure-development/SKILL.md` — secret handling, OIDC
- Provider leaves under `../../api-key-required/`

## Authoritative References
- Cloudflare Workers / Pages docs — versions & deployments, Wrangler OIDC
- Vercel docs — Deployments, Aliases, OIDC for GitHub Actions
- Netlify docs — Deploy contexts, build plugins, env scoping
- Render docs — Blueprints, image-based services, rollback API
- Fly.io docs — Machines, multi-region, secrets
- GitHub Docs — OIDC for cloud providers
