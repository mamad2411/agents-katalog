---
name: earthly-ci-basics
description: >
  Earthly CI basics for owned repos: Earthfile targets, caching, multi-platform
  builds, secrets/ARG hygiene, and wiring Earthly into GitHub Actions/GitLab CI.
  Use when Earthfile, earthly build, WITH DOCKER, SAVE IMAGE, LOCALLY, or
  reproducible containerized CI pipelines. Not a general Docker tutorial alone.
---

# Earthly CI Basics

## Scope And Authorization

- **In scope:** repositories and registries you own; CI runners you control.
- **Out of scope:** pushing images or secrets into third-party accounts without permission.
- Keep production deploy credentials in the CI secret store, not in the Earthfile.
- Prefer ephemeral runners and short-lived registry tokens.
- Pair Dockerfile/Earthfile changes with `code-quality-standards` and container security skills when relevant.

## When To Use

- Introducing Earthly so local and CI run the same targets.
- Replacing ad-hoc `docker build && docker run` CI steps with cached Earthfile recipes.
- Multi-stage builds, monorepo target graphs, or `WITH DOCKER` integration tests.
- Passing secrets safely (`--secret`) without baking them into image layers.
- Debugging cache misses, base image pins, and target dependency graphs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic Dockerfile hardening | container/image security skill in catalog |
| Kubernetes deploy/GitOps | deploy/GitOps skills |
| AWS ECR scan gates | `ecr-image-scanning` |
| Secrets inventory program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |
| Full SDLC process | `secure-sdlc-checklist` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Earthfile | Versioned syntax; explicit targets; pin base images by digest when possible |
| Caching | Layer/cache mounts; avoid busting cache with unneeded COPY of whole repo |
| Secrets | `--secret id=...` / `RUN --secret`; never `ENV SECRET=...` from plaintext ARG |
| Artifacts | `SAVE ARTIFACT` for reports; `SAVE IMAGE` for pushable images |
| CI | Same `earthly +target` locally and in pipeline; store Earthly version pin |
| Isolation | Prefer containerized targets over `LOCALLY` for reproducibility |

## Workflow

### 1. Confirm scope and success criteria

1. List what must be reproducible: unit tests, image build, integration tests, lint.
2. Name registries, platforms (`linux/amd64`, `linux/arm64`), and who can push.
3. Define success: same target green locally and in CI; secrets never in history/layers.

### 2. Inventory current build path

1. Existing Dockerfile(s), Makefile, and CI YAML that Earthly will replace or wrap.
2. Earthly version on developer machines and runners (`earthly --version`).
3. Cache backend (inline, registry cache, or Earthly Cloud if used).

### 3. Baseline

1. Time current CI job wall clock and note flaky steps.
2. Record image tags and whether digests are used.
3. List secrets currently injected as env vars into Docker builds.

### 4. Author a minimal Earthfile

```dockerfile
VERSION 0.8
FROM golang:1.22-alpine
WORKDIR /src

deps:
    COPY go.mod go.sum ./
    RUN go mod download
    SAVE IMAGE --cache-hint

build:
    FROM +deps
    COPY . .
    RUN go test ./...
    RUN CGO_ENABLED=0 go build -o /bin/app ./cmd/app
    SAVE ARTIFACT /bin/app AS LOCAL build/app

image:
    FROM gcr.io/distroless/static:nonroot
    COPY +build/app /app
    ENTRYPOINT ["/app"]
    SAVE IMAGE --push my.registry.example/app:dev
```

1. Split **deps → build → image** so dependency layers cache independently.
2. Prefer `COPY` of lockfiles before full source for language package managers.
3. Use `SAVE ARTIFACT` for binaries/reports consumed by later targets or host.

### 5. Secrets, ARGs, and WITH DOCKER

```bash
# Pass CI token without embedding in image
earthly --secret REGISTRY_TOKEN=$REGISTRY_TOKEN +image

# Multi-platform (when builder supports)
earthly --platform=linux/amd64 --platform=linux/arm64 +image
```

```dockerfile
# Inside a target (illustrative)
RUN --secret REGISTRY_TOKEN=REGISTRY_TOKEN \
    echo "$REGISTRY_TOKEN" | docker login my.registry.example -u ci --password-stdin
```

1. Use build `ARG` only for non-secret configuration (version labels, feature flags).
2. For integration tests needing a daemon: `WITH DOCKER --load=...` and pull pinned service images.
3. Avoid `LOCALLY` for anything that must match CI; reserve for thin wrappers.

### 6. Wire CI

```yaml
# GitHub Actions excerpt
- uses: earthly/actions-setup@v1
  with:
    version: "0.8.15"   # pin
- name: Build and test
  run: earthly --ci +build
- name: Push image
  if: github.ref == 'refs/heads/main'
  env:
    EARTHLY_PUSH: "true"
  run: earthly --push --secret REGISTRY_TOKEN=${{ secrets.REGISTRY_TOKEN }} +image
```

1. Set `--ci` for non-interactive, consistent logging.
2. Cache Earthly and base layers per runner policy.
3. Fail the job if unexpected `SAVE IMAGE --push` targets run on PRs.

### 7. Verify and hand off

```bash
earthly +build
earthly --no-cache +build    # when debugging stale cache
earthly prune -a             # local reclaim (careful on shared builders)
```

1. Confirm image does not contain secrets: inspect history / scan layers.
2. Document target graph for the team (`+lint`, `+test`, `+image`).
3. Apply `code-quality-standards` to any scripts invoked from the Earthfile.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Base images | Pin tag + digest for prod | `FROM ubuntu:latest` forever |
| Secrets | `--secret` at RUN time | `ARG SECRET` then `ENV` in image |
| Targets | Small composable graph | One mega-target always rebuilds all |
| CI parity | Same `earthly +test` local/CI | “Works on my laptop” shell scripts only |
| Push | Push only on protected branches | PR pipelines push `:latest` to prod |

## Output Checklist

- [ ] Earthfile targets cover test/build/image with clear deps
- [ ] Earthly version pinned in CI
- [ ] Secrets via secret mounts; not layer-baked
- [ ] Cache-friendly COPY order documented
- [ ] Local and CI runs of the same targets succeed
- [ ] Push policy and registry auth documented
- [ ] Artifact/report paths known to consumers
- [ ] Residual risks (shared cache poisoning, privileged WITH DOCKER) noted

## Rules

- Owned registries and repos only.
- Prefer reproducible containerized targets over host-dependent `LOCALLY`.
- Never commit registry passwords or cloud keys into Earthfiles.
- Keep this skill on Earthly CI patterns; deep image hardening routes to container security skills.
- Evidence: command logs and CI job links, redacted.
