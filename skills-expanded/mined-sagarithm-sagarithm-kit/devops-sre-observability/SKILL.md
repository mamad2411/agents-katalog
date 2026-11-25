<!-- SAGARITHM:START - DO NOT EDIT DIRECTLY -->
---
id: "devops.sre-observability"
name: "DevOps, SRE & Cloud Deployment Governance"
version: "1.2.0"
domain: "devops"
description: "Govern production deployment lifecycles, hermetic multi-stage containerization, CI/CD verification gates, OpenTelemetry observability, and zero-downtime releases."
triggers:
  - "Authoring Dockerfiles, container configurations, or Helm charts"
  - "Configuring CI/CD pipelines (GitHub Actions, GitLab CI, ArgoCD)"
  - "Setting up telemetry, OpenTelemetry tracing, Prometheus metrics, or Grafana alerts"
  - "Planning production release deployments, canaries, or rollback mechanisms"
prerequisites:
  - "delivery.shipping-and-launch"
  - "security.secure-development"
risk_profile: "high"
---

# DevOps, SRE & Cloud Deployment Governance

## Overview
This skill embodies the rigor of a Staff Site Reliability Engineer (SRE) and Principal Cloud Architect. It ensures all applications are containerized hermetically, deployments are automated with Zero Assumed Success, telemetry is standardized, and production outages trigger deterministic automated rollbacks.

## 🎯 Token Conservation & High-Yield Heuristics
1. **Declarative Configurations**: Provide clean, minimal, multi-stage Dockerfiles and YAML workflows without redundant explanatory commentary.
2. **Explicit Health Probes**: Define lightweight HTTP `/healthz` (liveness) and `/readyz` (readiness) endpoints rather than complex multi-query diagnostics on probe loops.
3. **Immutability Principle**: Build once, tag with Git SHA, and deploy the identical artifact across Staging, Pre-Prod, and Production. Never rebuild images per environment.

## 📐 Core Engineering Directives

### 1. Hermetic Multi-Stage Containerization
- **Multi-Stage Builds**: Separate build-time dependencies (compilers, devDependencies, SDKs) from the final runtime image. Final runtime images must contain only production artifacts.
- **Rootless Execution**: Never run container processes as `root` (`UID 0`). Always create and specify an unprivileged user (`USER node` or `USER 10001:10001`).
- **Minimal Base Images**: Use Alpine, Chainguard, or Distroless images (`gcr.io/distroless/nodejs20-debian12`) to eliminate attack surface and reduce CVE vulnerability scans.
- **Deterministic Pinning**: Pin base images and package dependencies by exact version or digest hash; never use `:latest`.

### 2. Deployment Strategies & Zero Downtime
- **Readiness vs. Liveness Probes**:
  - `readinessProbe`: Returns `200` only when internal caches are warm and database connections are established. Detaches failing pods from load balancer traffic without restarting.
  - `livenessProbe`: Returns `200` when process is responsive. Restarts deadlocked or unresponsive processes.
- **Canary & Blue-Green Deployments**: Never execute in-place rolling restarts without traffic splitting. Route 5% traffic to canary instances; monitor error rates for 5 minutes before progressing to 100%.
- **Automated Rollback Triggers**: Abort deployment and trigger automated rollback if:
  - HTTP 5xx error rate exceeds $1\%$ of total requests over 3 minutes.
  - P99 response latency exceeds $2{,}000\text{ms}$.
  - Pod readiness probe fails for $> 60$ seconds.

### 3. OpenTelemetry (O-Tel) & Observability Standards
- **Unified Telemetry**: Standardize on OpenTelemetry (OTel) instrumentation for Traces, Metrics, and Logs.
- **The Golden Signals**: Monitor and alert on:
  1. **Latency**: Duration taken to service requests (tracked as P50, P90, P99 histograms).
  2. **Traffic**: Demand placed on the system (requests per second).
  3. **Errors**: Rate of failed requests (HTTP 5xx, uncaught rejections).
  4. **Saturation**: Fraction of resource capacity utilized (CPU, memory, DB connection pool).
- **Service Level Objectives (SLOs)**: Define explicit SLIs, SLOs, and Error Budgets (e.g. 99.9% uptime over rolling 30 days = max 43.8 minutes total allowable downtime).

### 4. CI/CD Gate Enforcement
- **Zero Bypass Policy**: Every pull request must pass the automated CI pipeline:
  1. Static analysis & typechecking.
  2. Secret scanning (entropy $H < 4.5$).
  3. Automated unit and integration test suites.
  4. Container vulnerability scanning (`trivy` / `grype`).
  5. Multi-vector verification gate (`sagarithm verify`).

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | SRE & Cloud Reality | Mandatory Action |
|---|---|---|
| *"I'll run the container as `root` to avoid permission issues."* | Security violation. Container breakouts gain root access to the host node. | Create and enforce an unprivileged user and group in the Dockerfile. |
| *"I'll use `:latest` for the Docker image tag."* | Non-deterministic. Builds change unpredictably and break rollbacks. | Pin base images to immutable SHA256 digests or exact SemVer tags. |
| *"I don't need readiness probes; the server starts immediately."* | Traffic routes to pods while initialization, DB connections, or migrations are pending, returning 502/503 errors to users. | Implement an explicit `/readyz` probe returning `200` only after readiness checks pass. |
| *"I'll store secrets in environment variables in the Dockerfile."* | Secrets are baked into image layer metadata and leaked through image registries. | Inject secrets at runtime via cloud secret managers (AWS Secrets Manager, GCP Secret Manager, Vault). |

## ✅ DevOps & SRE Verification Checklist
- [ ] Multi-stage Dockerfile produces minimal runtime artifact running as non-root user.
- [ ] Liveness and readiness endpoints implemented and distinct.
- [ ] Distributed tracing context propagated with W3C `traceparent`.
- [ ] Automated rollback criteria configured for production deployment pipelines.
- [ ] CI pipeline validates tests, types, and security vectors before merge.
<!-- SAGARITHM:END -->
