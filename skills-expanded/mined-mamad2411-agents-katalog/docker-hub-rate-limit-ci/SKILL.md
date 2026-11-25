---
name: docker-hub-rate-limit-ci
description: >
  Diagnose and fix Docker Hub pull rate limits in CI: anonymous vs authenticated quotas,
  shared runner IPs, mirrors, private base caches, and registry migration. Use when CI fails
  with toomanyrequests, 429, Docker Hub rate limit, docker.io pulls flaky on GitHub
  Actions/GitLab/shared runners, or hardening image pulls against Hub throttling — hand
  Dockerfile structure to dockerfile-best-practices; hand pipeline secrets/OIDC to CI secrets skills.
---

# Docker Hub Rate Limit CI

## Scope And Authorization

- **In scope:** CI systems and registries for orgs you operate.
- **Out of scope:** Credential stuffing Hub accounts; abusing others’ pull tokens.
- Prefer org pull identity or mirrors over anonymous shared IP pulls.
- Redact Hub tokens/PATs in logs; use masked CI secrets.
- Pair with `dockerfile-best-practices`, `docker-multi-stage-builds`, and `drone-ci-secrets` / GitHub OIDC patterns.

## When To Use

- CI: `toomanyrequests: You have reached your pull rate limit`.
- Flaky builds on shared GitHub-hosted runners (shared egress IPs).
- Org wants deterministic base image pulls.
- Migrating hot bases to GHCR/ECR/GCR/Artifactory cache.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dockerfile best practices | `dockerfile-best-practices` |
| Multi-stage patterns | `docker-multi-stage-builds` |
| CI secret storage | `drone-ci-secrets` / secrets hygiene |
| Distroless adoption | `distroless-image-adoption` |
| Code quality baseline | `code-quality-standards` |

## Why CI hits limits

| Factor | Effect |
| --- | --- |
| Anonymous pull | Lower quota per IP |
| Shared runner IP | Many tenants share limit |
| Many stages/jobs | Parallel pulls multiply |
| Unpinned `latest` | Frequent unexpected pulls |
| No cache | Every job pulls full base |

## Workflow

### 1. Confirm scope and success criteria

1. CI platforms, average concurrent jobs, base images from docker.io.
2. Success: builds pull authenticated or via mirror; rate-limit errors near zero; secrets rotated.
3. Budget for private registry storage.

### 2. Confirm the failure mode

```text
# Log signatures
# toomanyrequests
# 429 Too Many Requests
# rate limit
```

1. Note whether failure is on base `FROM` or later layers.
2. Check if only peak hours fail (quota exhaustion).

### 3. Inventory docker.io usage

```bash
rg -n "FROM docker\\.io|FROM library/|FROM nginx|FROM node|FROM python|FROM ubuntu" -g 'Dockerfile*'
rg -n "image:.*(nginx|redis|postgres|docker\\.io)" -g '*compose*' -g '*.yml'
```

1. List unique bases and pull frequency.
2. Prefer already-internal copies if any.

### 4. Authenticated Hub pulls (quick win)

```yaml
# GitHub Actions sketch
- name: Login Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}  # access token, not password
```

1. Use **access token** with read-only pull scope; org seat if available.
2. One bot identity per org; monitor abuse.
3. Still can hit limits under huge concurrency—mirror next.

### 5. Mirror / pull-through cache (durable)

| Approach | Notes |
| --- | --- |
| Harbor/Artifactory/ECR pull-through | Cache docker.io; CI points to mirror |
| Mirror base to GHCR/ECR | `docker pull` + `retag` + `push` on schedule |
| GitHub Actions cache | BuildKit cache; reduces re-pulls |
| Vendor internal bases | Rebuild golden images weekly |

```bash
# Retag sketch (owned CI)
docker pull docker.io/library/python:3.12-slim
docker tag python:3.12-slim ghcr.io/org/cache/python:3.12-slim
docker push ghcr.io/org/cache/python:3.12-slim
```

```dockerfile
# Dockerfiles use internal cache
FROM ghcr.io/org/cache/python:3.12-slim
```

1. Pin digests for reproducibility.
2. Document refresh job and CVE rebuild cadence.

### 6. Reduce pull pressure

1. Fewer parallel cold jobs without cache.
2. Reuse warm runners carefully (security tradeoffs).
3. Multi-stage: still pulls each stage base—cache them all.
4. Avoid unnecessary `docker pull` in scripts when BuildKit would cache.

### 7. Verify and hand off

```bash
# CI after fix: green builds at peak concurrency
# Monitor Hub rate headers if available; registry 429s
```

1. Runbook: rotate Hub token; failover to mirror.
2. Metrics: pull failures by registry host.
3. Apply `code-quality-standards` to mirror automation.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | Org token in secrets | Anonymous on shared IP |
| Cache | Pull-through / GHCR | Every job hits docker.io |
| Dockerfile | Internal FROM | Random latest from Hub |
| Secrets | Read-only token | Password in plaintext log |
| Concurrency | Cache + mirror | 100x parallel cold builds |
| Ownership | Refresh job owned | Stale mirror forever |

## Output Checklist

- [ ] Rate-limit errors confirmed in CI logs
- [ ] docker.io image inventory complete
- [ ] Authenticated pull or mirror implemented
- [ ] Dockerfiles/compose point at durable sources
- [ ] Tokens scoped and masked
- [ ] Build cache enabled where appropriate
- [ ] Peak concurrency retested
- [ ] Refresh/CVE process for mirrored bases
- [ ] Alerts on registry 429
- [ ] Residual risk documented

## Rules

- Do not share personal Hub passwords in CI.
- Prefer org-controlled caches for reliability and supply-chain control.
- Pin images; rate limits are reliability and security hygiene.
- Owned CI only.
- Focus on Hub rate limits—not general Dockerfile style (neighbor).
