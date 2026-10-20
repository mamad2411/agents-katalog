---
name: docker-29-build-quality
description: Reviews, designs, and hardens Docker Engine 29 Dockerfiles and image build workflows. Use when working with Dockerfile, .dockerignore, BuildKit, Buildx, image tags, build checks, cache strategy, SBOMs, provenance, reproducibility, secret handling, or release builds.
license: MIT
compatibility: Requires Docker Engine 29-compatible CLI for runtime validation. Static review works without Docker.
---

# Docker 29 Build Quality

This skill helps the agent design, review, and harden Dockerfiles and image build workflows for Docker Engine 29.

## When to Use

Use this skill for:

- Creating or refactoring Dockerfiles.
- Reviewing `.dockerignore`.
- Designing multi-stage builds.
- Running Dockerfile build checks.
- Preventing secrets from being baked into image layers.
- Reviewing non-root runtime behavior.
- Preparing reproducible image build, tag, and push commands.
- Debugging build cache, context, platform, or BuildKit issues.

## Operating Principles

1. Optimize for correctness and security before image size.
2. Keep runtime images minimal and non-root.
3. Separate build-time tooling from runtime outputs with multi-stage builds.
4. Avoid secrets in images, build arguments, environment variables, labels, files, and logs.
5. Keep build contexts small and deterministic.
6. Honor project lockfiles and avoid language-specific version policy in this Docker plugin.
7. Verify generated commands against Docker Engine 29 and the repository’s actual files.
8. Ask for approval before push, prune, delete, or privileged host access.

## Recommended Workflow Selection

- Use `workflows/dockerfile-hardening-workflow.md` when reviewing or rewriting a Dockerfile for security, size, and maintainability.
- Use `workflows/image-build-release-workflow.md` when preparing a build, tag, attestation, SBOM, scan, and push sequence.

Use `docker-29-build-debugging` for deep build failure or runtime container debugging.

## Resources and Examples

- `resources/dockerfile-review-checklist.md` contains the review checklist.
- `examples/dockerfile-secure-pattern.md` contains a language-neutral secure Dockerfile pattern.

## Scripts

Scripts are safe by default. Run with `--help` before use.

- `scripts/docker-29-project-check.sh`
  - Static Dockerfile and Compose checks.
  - Supports hook mode, changed-file mode, and scoped checks.
- `scripts/docker-29-dockerfile-security-check.sh`
  - Wrapper for Dockerfile security checks.
- `scripts/docker-29-secret-layer-check.sh`
  - Wrapper for secret-baking checks.
- `scripts/docker-29-nonroot-runtime-check.sh`
  - Wrapper for non-root runtime checks.
- `scripts/docker-29-healthcheck-check.sh`
  - Wrapper for Compose healthcheck checks.
- `scripts/docker-29-command-guard.sh`
  - Hook script that gates dangerous Docker commands.

## Review Checklist

When reviewing a Dockerfile, check:

- Base image trust, maintenance, tag pinning, and digest strategy.
- Multi-stage separation between build and runtime dependencies.
- `.dockerignore` coverage.
- User and filesystem permissions.
- Secret handling with BuildKit secret or SSH mounts when needed.
- Package manager cache cleanup.
- Signal handling and health/readiness behavior.
- Reproducibility, labels, SBOM, and provenance needs.
- CI validation and scan strategy.

## Command Guidance

Prefer read-only or validation commands first:

```bash
docker version
docker buildx version
docker build --check -f Dockerfile .
docker compose config
```

For release builds, adapt to the repository:

```bash
docker buildx build \
  --pull \
  --platform linux/amd64,linux/arm64 \
  --tag registry.example.com/team/app:${GIT_SHA} \
  --provenance=true \
  --sbom=true \
  --push \
  .
```

Do not run the release command until the user has approved the target registry, tag, platform list, and push action.
