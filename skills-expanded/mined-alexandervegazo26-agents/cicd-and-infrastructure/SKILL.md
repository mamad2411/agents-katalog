---
name: cicd-and-infrastructure
version: 1.0.0
description: Pipeline design, Infrastructure as Code practices, environment management, deployment strategies, and environment promotion. Load when building/changing a CI/CD pipeline, writing IaC, or planning how a change moves from dev to production.
---

# CI/CD & Infrastructure

## Pipelines

Every stage should have one clear purpose (build, test, security scan, deploy) and fail fast — cheap checks (lint, unit tests) before expensive ones (integration, E2E, load). A pipeline that's green but skips a stage silently is worse than a red one; make skips visible in the output.

Detect which CI system and command runner actually apply the same way `qa-tooling` detects a test runner — from the config files and scripts already present (`.github/workflows`, `azure-pipelines.yml`, `.gitlab-ci.yml`, a `Makefile`, package-manager scripts) — rather than assuming a toolchain or introducing a second one for the same job.

## Infrastructure as Code

Everything that defines an environment (compute, network, config) lives in version control, not in a console click history. Treat IaC changes with the same review rigor as application code — a bad Terraform apply can be as destructive as a bad migration. Plan before apply, always review the plan output for unexpected deletions/replacements.

## Environments

Keep dev/staging/production parity as high as practical — the closer staging matches production, the more a pre-prod test result actually predicts production behavior. Name and track parity gaps explicitly rather than discovering them during an incident.

## Deployment strategies

Match strategy to risk: rolling deploy for routine low-risk changes, canary or blue-green for anything with real user impact or uncertainty, feature-flagged dark launch when decoupling deploy from release matters. Avoid flag-day cutovers unless genuinely unavoidable.

## Environment promotion

A build artifact promoted through environments should be the *same* artifact at every stage — rebuilding at each stage reintroduces the risk that what's tested isn't what ships. Promotion gates (automated tests, manual approval) should be explicit and enforced by the pipeline, not by convention.
