---
name: infra-container-build-review
description: "Review image-build changes to bases, layers, secrets, SBOMs, runtime user, or scan gates."
---

# Infra Container Build Review

Review image reproducibility, size, base image risk, secrets in builds, non-root runtime, SBOM/provenance, and scan gates.

## Trigger boundary

Use this skill when a Dockerfile or image build changes base images, layers, build secrets, reproducibility, SBOM/provenance, runtime user, image contents, or vulnerability-scan gates.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no image-build, artifact, secret, or scan impact; follow the repository's established convention directly.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Artefakty i wersjonowanie; Budowanie obrazów Dockerowych; Rozmiar obrazu i cache builda
- [Shared infrastructure review checklist](../_shared/references/infrastructure/container-review-checklist.md) - wspólne fakty i bramka review; zastosuj je do zakresu builda opisanego wyżej
