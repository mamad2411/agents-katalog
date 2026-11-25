---
name: ci-cd-pipelines
description: >-
  CI/CD pipeline design with GitHub Actions, GitLab CI, and Jenkins. Use when the user mentions CI/CD, continuous integration, continuous deployment, GitHub Actions, GitLab CI, Jenkins, Jenkinsfile, pipeline, workflow, build automation, reusable workflow, composite action, GitLab runner, pipeline security, OIDC, secrets management, matrix build, monorepo pipeline, environment promotion, build cache, or automating build/test/deploy workflows. Complements container-orchestration and infrastructure-as-code.
---

# CI/CD Pipelines

A production-grade skill for designing, implementing, and securing CI/CD pipelines across
GitHub Actions, GitLab CI, and Jenkins. Includes templates for common application types
and advanced patterns for enterprise-scale delivery.

## Quick Reference

| Platform | Config File | Reference |
|----------|------------|-----------|
| GitHub Actions | `.github/workflows/*.yml` | `references/github-actions.md` |
| GitLab CI | `.gitlab-ci.yml` | `references/gitlab-ci.md` |
| Jenkins | `Jenkinsfile` | `references/jenkins.md` |
| Security | All platforms | `references/pipeline-security.md` |
| Patterns | All platforms | `references/pipeline-patterns.md` |

## Core Workflow

1. **Identify the CI platform** — GitHub Actions, GitLab CI, or Jenkins?
2. **Identify the application type** — Node.js, Python, Go, Java, Docker, or other?
3. **Read relevant references:**
   - Platform-specific → `references/github-actions.md`, `gitlab-ci.md`, or `jenkins.md`
   - Patterns → `references/pipeline-patterns.md`
   - Security → `references/pipeline-security.md`
4. **Generate pipeline** using `scripts/generate_pipeline.py`

---

## Pipeline Design Principles

### 1. Fast Feedback
- Fail fast: run linting and unit tests first (cheapest, fastest)
- Parallelize independent stages
- Cache dependencies aggressively
- Target: PR pipeline < 10 minutes

### 2. Pipeline Stages (Standard)

```
┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌────────┐   ┌──────┐
│ Lint │──►│ Test │──►│Build │──►│ Scan │──►│ Deploy │──►│Verify│
│      │   │      │   │      │   │      │   │ (env)  │   │      │
└──────┘   └──────┘   └──────┘   └──────┘   └────────┘   └──────┘
  1 min     3 min      2 min      2 min       3 min       1 min
```

| Stage | What | Trigger | Fail Action |
|-------|------|---------|-------------|
| **Lint** | Code style, formatting | Every push | Block PR |
| **Test** | Unit + integration tests | Every push | Block PR |
| **Build** | Compile, package | Every push | Block PR |
| **Scan** | SAST, dependency vulnerabilities | Every push | Warn or block |
| **Deploy Staging** | Deploy to staging env | Merge to main | Alert team |
| **Deploy Prod** | Deploy to production | Tag or manual | Alert + rollback plan |
| **Verify** | Smoke tests, health checks | After deploy | Auto-rollback |

### 3. Branch Strategy Mapping

| Branch | Pipeline | Deploy To |
|--------|----------|-----------|
| Feature branch / PR | Lint + Test + Build | — (no deploy) |
| `develop` | Full + Deploy | Development env |
| `main` | Full + Deploy | Staging → Production |
| `release/*` | Full + Deploy | Staging (manual → Prod) |
| Tags (`v*`) | Full + Deploy | Production |

### 4. Artifact Flow

```
Build → Artifact (container image, binary, package)
         ↓
    Tag with commit SHA + semantic version
         ↓
    Push to registry (container, package, artifact store)
         ↓
    All deployments use the SAME artifact (never rebuild for different envs)
```

---

## Platform Comparison

| Feature | GitHub Actions | GitLab CI | Jenkins |
|---------|---------------|-----------|---------|
| Config format | YAML | YAML | Groovy (Jenkinsfile) |
| Runner management | GitHub-hosted + self-hosted | Shared + self-hosted | Self-hosted only |
| Secrets | Repository/Org/Env secrets | CI/CD Variables | Credentials plugin |
| Caching | `actions/cache` | `cache:` directive | Pipeline cache plugin |
| Artifacts | `actions/upload-artifact` | `artifacts:` directive | `archiveArtifacts` |
| Reusability | Reusable workflows, composite actions | `include:`, templates | Shared libraries |
| Matrix builds | `strategy.matrix` | `parallel: matrix` | `matrix` directive |
| Environments | Environments with protection rules | Environments | Stages with input |
| Container builds | `docker/build-push-action` | Built-in Docker support | Docker pipeline plugin |
| OIDC | Native support (AWS, GCP, Azure) | Native (some providers) | Plugin-based |
| Cost | Free for public repos; minutes-based | 400 min/month free | Self-hosted (infra cost) |
| Best for | Open source, GitHub-native teams | GitLab-native teams, enterprise | Legacy, complex orchestration |

---

## Scripts

### generate_pipeline.py

Generate complete pipeline configurations for any combination of platform and app type.

```bash
python scripts/generate_pipeline.py \
  --provider github|gitlab|jenkins \
  --app-type nodejs|python|go|java|docker \
  --features test,lint,build,scan,deploy,docker \
  --environments dev,staging,production \
  --output .
```

---

## Best Practices

1. **Build once, deploy everywhere** — same artifact across all environments
2. **Pin versions** — actions, images, tools (avoid `latest`)
3. **Fail fast** — cheapest checks first (lint → unit test → integration → deploy)
4. **Cache aggressively** — dependencies, Docker layers, build outputs
5. **Secrets never in code** — use platform secret management, never echo secrets
6. **Immutable artifacts** — tag with SHA, never overwrite
7. **Idempotent deploys** — running the pipeline twice produces the same result
8. **Observability** — log pipeline metrics, alert on failures, track DORA metrics
9. **Least privilege** — minimal permissions for each pipeline step
10. **Test your pipeline** — pipeline changes should go through PR review too



---
