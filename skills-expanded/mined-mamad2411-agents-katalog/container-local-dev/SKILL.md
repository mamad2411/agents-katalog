---
name: container-local-dev
description: Docker multi-stage builds and Compose for Next.js on Node LTS with pnpm plus Postgres Redis sidecars and dockerignore hygiene
tags:
  - docker
  - nextjs
  - devops
version: 1.0.0
category: development
outcomes:
  - Multi-stage Dockerfile outline deps build runner non root user
  - compose yaml services app db cache volumes env file not committed
  - dockerignore node_modules git next cache reduce context size
stack:
  - docker
  - pnpm
  - next
last_reviewed: 2026-05-19
risk_level: low
tools_allowed: suggest-shell
requires_user_approval: false
compatibility:
  - generic-markdown
  - skills-sh
  - cursor
  - claude-code
  - antigravity
  - codex
  - github-copilot
  - windsurf
  - gemini-cli
  - cline
  - amp
  - opencode
  - roo
  - goose
  - kilo
  - kiro-cli
  - droid
  - openclaw
  - trae
references:
  - references/stack-nextjs.md
  - references/skill-safety.md
---

# Instructions

## When to Use

- Use for Dockerfile + Compose for Next on Node LTS.
- Prefer `monorepo-tooling` for workspace package graphs first.
- Prefer `env-config-agent` for compose secret naming.

Add **Docker** and **Compose** for **local** and **CI-like** runs of **Next.js** (Node **20/22** LTS, **pnpm**).

1. **`.dockerignore`:** exclude `.git`, `node_modules`, `.next`, `dist`, `.env*` (use build args or runtime mount for secrets in dev only).
2. **Multi-stage:** `deps` (pnpm fetch/install) → `builder` (`pnpm build`) → `runner` (minimal: `node_modules` prod slice + `.next/standalone` if user enabled standalone output - match their `next.config`).
3. **User:** non-root `USER node` or numeric uid in final stage.
4. **Compose:** `app` + `postgres` + optional `redis`; healthchecks; named volumes; **no secrets in compose YAML** - `.env` local only gitignored.
5. **Dev vs prod:** `docker compose -f compose.yaml -f compose.override.yaml` pattern for hot reload optional - keep prod Dockerfile lean.
6. **CI:** same Dockerfile build in GitHub Actions to prove reproducibility - link **`github-actions-ci`**.
## Outcomes

- File list + Dockerfile stage names + compose service graph (bullets).

## Output Rules

suggest-shell: `docker build` / `compose up` commands; user runs them.

## Scope and boundaries

- **In scope:** local dev containers, small prod-oriented images.
- **Out of scope:** Kubernetes manifests, service mesh, HIPAA hosting.

## Safety

- Never print `.env` contents; use `env_file: .env.local` documentation only.

## Troubleshooting

- **ARM vs x86:** buildx platforms for M-series Mac deploying to amd64 cloud.
- **Huge context:** fix `.dockerignore` before chasing layer cache.

## Related skills

- [`monorepo-tooling`](../monorepo-tooling/SKILL.md) - multi-package Docker contexts
- [`github-actions-ci`](../github-actions-ci/SKILL.md) - CI image build/cache
- [`env-config-agent`](../env-config-agent/SKILL.md) - compose env files

**GitHub:** https://github.com/bh611627/skillcodex/tree/main/skills/container-local-dev/SKILL.md  
**npm:** https://www.npmjs.com/package/@skillcodex/skills
