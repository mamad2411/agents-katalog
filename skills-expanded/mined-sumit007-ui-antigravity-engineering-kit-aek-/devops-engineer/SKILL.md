---
name: devops-engineer
description: Architect production DevOps pipelines, multi-stage Docker containers, Kubernetes deployments, and GitHub Actions CI/CD workflows. Enforces immutable infrastructure and secret hygiene.
---

# DevOps Engineer Skill

## Purpose
Directs infrastructure-as-code, containerization, automated testing pipelines, and production release reliability.

## When to Use
- Authoring multi-stage `Dockerfile` definitions targeting minimal image size (distroless / alpine).
- Creating GitHub Actions CI/CD matrix workflows with dependency caching.
- Setting up Prometheus, Grafana, and OpenTelemetry observability instrumentation.

## Engineering Workflow
1. **Container Security**: Run containers as non-root users; pin base image SHA256 digests.
2. **CI Pipeline**:
   - Lint -> Test -> Security Scan (Trivy) -> Build Artifact -> Verification.
3. **Verification**:
   - `hadolint Dockerfile`
   - `actionlint .github/workflows/*.yml`

