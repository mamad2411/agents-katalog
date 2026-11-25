---
name: ci-cd-pipeline
description: Design, audit, and optimize CI/CD pipelines with build caching, test parallelism, secret boundaries, and automated gates.
category: development
aliases:
- github-actions-pipeline
- ci-cd-workflow
- continuous-integration
- pipeline-builder
triggers:
- build a CI/CD pipeline
- create GitHub Actions workflow
- optimize build pipeline caching
- audit CI security and test stages
- automate deployment pipeline
keywords:
- ci
- cd
- github-actions
- workflow
- pipeline
- build
- test
- cache
- deploy
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- pipeline-authoring
- cache-optimization
- matrix-testing
- secret-isolation
inputs:
- project_tech_stack
- test_commands
- deploy_target
outputs:
- workflow_yaml
- security_review
- cache_strategy
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- development
- github-actions
- pipeline
- workflow
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# CI/CD Pipeline

## Purpose
Designs, implements, audits, and accelerates Continuous Integration and Continuous Deployment (CI/CD) pipelines. Maximizes test parallelism and build caching while strictly preserving secret isolation and deployment gates.

## When to Use
- Setting up GitHub Actions, GitLab CI, or Cloudflare deployment workflows for a new project.
- Slow CI builds requiring dependency caching, artifact reuse, and matrix job optimization.
- Hardening CI workflows against supply chain attacks, untrusted PR execution, and secret leaks.
- Automating test execution, linting, Docker packaging, and staging deployments.

## When NOT to Use
- Writing local application business logic or unit test assertions.
- Manually deploying one-off temporary files to sandbox machines.

## Capabilities
- **Workflow Synthesis**: Generate production-grade YAML configurations (GitHub Actions, GitLab CI).
- **Cache Optimization**: Implement intelligent layer and package manager caching (pip, npm, cargo, docker).
- **Security Hardening**: Enforce read-only default permissions (`permissions: contents: read`), pin actions by SHA.
- **Matrix Parallelism**: Configure multi-OS (Linux, macOS, Windows) and multi-version test matrices.

## Inputs
- `tech_stack` (required) — Programming language, package manager, and framework.
- `pipeline_goals` (optional) — Test only, publish package, deploy Docker container, or serverless worker.
- `secrets_required` (optional) — Required external tokens or credentials.

## Workflow
1. Identify project build, lint, and test commands.
2. Structure the pipeline stages: lint/validate -> test matrix -> security scan -> build -> deploy.
3. Configure high-efficiency caching keys for dependency trees.
4. Apply least-privilege token permissions to each job.
5. Validate workflow YAML against syntax and schema specifications.

## Tools
- YAML schema linters and GitHub Actions syntax checkers.

## Examples
- "Create a GitHub Actions workflow for testing on Python 3.10 and 3.11 with pip caching."
- "Optimize our CI pipeline to reduce build times from 15 minutes to under 3 minutes."
- "Audit this deployment workflow for security vulnerabilities and secret leaks."

## Safety
- Never execute untrusted pull request code with write access or access to production secrets (`pull_request_target` safeguards).
- Always pin third-party actions to full commit hashes rather than mutable branch tags.

## Source
Custom skill maintained in this library following modern DevSecOps standards.

## Notes
Composes directly with `development.docker-manager` and `security.npm-auditor`.
