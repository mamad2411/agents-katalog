---
name: devops-delivery
description: Set up CI/CD, Docker, and deploy pipelines. Covers GitHub Actions, Dockerfiles and compose, PaaS deploys (Vercel, Render, Fly), Kubernetes and Terraform for advanced needs, environments, secrets in pipelines, and rollback plans. Use this skill whenever the user mentions CI/CD, Dockerfile, Kubernetes, Terraform, deploy, pipeline, environments, staging, production, rollback, GitHub Actions, or asks how to get the app running somewhere, even if they only say "put this online" or "automate the release". Not for app code (see stack skills), system architecture (see system-design), or app-level security bugs (see security-review).
---

# DevOps delivery

You ship reproducibly or not at all. Every deploy plan ends with: how it rolls back, and how we know it worked.

## Workflow

1. **Pick the simplest target** from `references/pipelines.md` that fits (PaaS first; containers when you need them; orchestrators last). Ask at most two questions (traffic shape, compliance needs), then recommend one target with the reason.
2. **Run `scripts/container-check.sh`** if the repo has a Dockerfile or compose file. Fix FAILs before writing new pipeline code.
3. **Build the pipeline:** lint → type-check/test → build → scan → deploy to staging → promote to production. See `templates/ci.yml`. Staging must exist before production automation — no direct-to-prod pipelines.
4. **Wire secrets properly:** CI secrets / secret manager, never in repo, compose files, or build logs. One identity per environment.
5. **Define done:** healthcheck green, smoke test against the deployed URL, rollback path written down (previous image tag or instant-revert mechanism), owner for the first 24h named.

## Hard rules

- Reproducible builds: lockfiles committed, images pinned by digest or exact tag (never `latest` in production), one build artifact promoted through environments — never rebuilt per environment.
- Every production deploy names its rollback path *before* merging. "Redeploy the previous tag" counts if the tag is recorded; hope is not a plan.
- Migrations run as a separate step with a backward-compatible window (expand → migrate → contract). Code and schema changes that break each other must never deploy together.
- No secrets in images, compose files, logs, or pipeline definitions. If a secret touched any of those, rotate it.
- State plainly what you did not verify (e.g. "no staging environment to test promotion against").

## Output style

Exact commands and file paths, in run order. Separate one-time setup (run once, check off) from per-deploy behavior. When rejecting a heavier option (K8s, multi-region), one line why.
