---
name: gcp-devops
description: Expert DevOps for Docker containers, industry-standard CI/CD pipelines, and Google Cloud Platform infrastructure (Cloud Run, Cloud SQL, Cloud Storage, Artifact Registry, IAM, and more). Use when building or reviewing Dockerfiles/compose files, CI/CD workflows, or GCP infra/IaC. Always optimizes for speed, lightweight footprint, scalability, cost-efficiency, and security. Primary skill of the devops-engineer.
---

# GCP DevOps

Run `project-adaptation` first. Every decision here is judged against five non-negotiable goals:

> **Speed · Lightweight · Scalability · Cost-efficiency · Security**

If a choice trades one off, say so and pick the balance that fits the project's stage.

## Operating principles
- **Speed:** cache aggressively (layer + dependency cache); parallelize CI jobs; fast cold starts (small images, lazy init).
- **Lightweight:** minimal base images (distroless/alpine), multi-stage builds, drop build deps from the final image, `.dockerignore`.
- **Scalability:** stateless services, horizontal autoscaling, externalize state (DB/cache/storage), sane min/max instances and concurrency.
- **Cost-efficiency:** scale-to-zero where it fits, right-size CPU/memory, lifecycle/retention policies, prefer managed services, budget alerts.
- **Security:** least-privilege IAM + Workload Identity (no long-lived keys), secrets in Secret Manager, private networking, pinned/scanned images, never secrets in code or images.

## Containers
Multi-stage hardened images, **cross-platform local dev (macOS / Windows / Linux)**, and **one shared container setup for every environment** as the default: a single Dockerfile and a single `docker-compose.yml` for local/UAT/prod — **no per-environment Docker, compose, or `.env` files**. The same image is built once and promoted unchanged; configuration differs only via runtime-injected env vars (Secret Manager in the cloud, one gitignored local `.env` copied from a committed `.env.example`). Identical definition everywhere is what kills the "it works only in this environment" problem — only infrastructure and injected values stay isolated per env. See `references/docker-and-cicd.md`.

## CI/CD
Industry-standard pipeline: CI on every push/PR (build → lint → test → scan). **Every deploy/release to UAT and production requires a human manual-approval gate — never auto-deploy.** UAT and prod deploys cut **git tags + releases** (pre-release for UAT, final release for prod), versioned from Conventional Commits via `git-conventions`. Keep a one-command rollback. Templates and rules in `references/docker-and-cicd.md`.

## GCP infrastructure
Service-by-service guidance — Cloud Run, Cloud SQL, Cloud Storage, Artifact Registry, IAM/Workload Identity, networking, Secret Manager, observability — in `references/gcp-services.md`. Prefer Infrastructure-as-Code (Terraform) and isolate environments.
