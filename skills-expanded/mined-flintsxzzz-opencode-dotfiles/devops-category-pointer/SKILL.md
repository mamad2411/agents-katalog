---
name: devops-category-pointer
description: "Pointer to a library of 38 specialized Devops skills. Use when working on devops-related tasks."
risk: none
---

# Devops Capability Library 🎯

This is a **pointer skill**. The 38 specialized Devops skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **aegisops-ai** — Autonomous DevSecOps & FinOps Guardrails. Orchestrates Gemini 3 Flash to audit Linux Kernel patches, Terraform cost drifts, and K8s compliance.
- **apple-container** — Build, run, and manage OCI/Linux containers as lightweight per-container VMs on Apple-silicon macOS using Apple's open-source container CLI, no Docker daemon required.
- **brendangregg-use-tsa** — Methodical performance troubleshooting and root-cause analysis with Brendan Gregg's USE and TSA methods, plus evidence-backed RCA and postmortem reports.
- **cron-doctor** — Diagnose and validate cron expressions before they ship. Catches the five silent death-traps: impossible dates that never fire, OR-semantics that fire too often, midnight spikes, uneven step drift, and leap-year February 29.
- **deploy-to-vercel** — Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment".
- **deployment-engineer** — Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation.
- **deployment-pipeline-design** — Architecture patterns for multi-stage CI/CD pipelines with approval gates and deployment strategies.
- **deployment-procedures** — Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts.
- **deployment-validation-config-validate** — You are a configuration management expert specializing in validating, testing, and ensuring the correctness of application configurations. Create comprehensive validation schemas, implement configurat
- **devops-deploy** — DevOps e deploy de aplicacoes — Docker, CI/CD com GitHub Actions, AWS Lambda, SAM, Terraform, infraestrutura como codigo e monitoramento.
- **devops-troubleshooter** — Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability.
- **docker-expert** — You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns, and production deployment strategies based on current industry best practices.
- **fedora-hyprland-installer** — Install, configure, verify, repair, update, and uninstall Hyprland on Fedora Linux with GPU-aware detection (NVIDIA/AMD/Intel).
- **github-actions-advanced** — Design, debug, and harden GitHub Actions CI/CD workflows, including reusable workflows, matrix builds, self-hosted runners, OIDC authentication, caching, environments, secrets, and release automation.

- **github-actions-debugger** — Specialized skill for diagnosing, analyzing, and fixing failing GitHub Actions workflows by parsing run logs and pipeline definitions.
- **gitops-workflow** — Complete guide to implementing GitOps workflows with ArgoCD and Flux for automated Kubernetes deployments.
- **grafana-dashboards** — Create and manage production-ready Grafana dashboards for comprehensive system observability.
- **helm-chart-scaffolding** — Comprehensive guidance for creating, organizing, and managing Helm charts for packaging and deploying Kubernetes applications.
- **incident-response-incident-response** — Use when working with incident response incident response
- **incident-response-smart-fix** — [Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observability platforms to systematically diagnose and res
- **incident-runbook-templates** — Production-ready templates for incident response runbooks covering detection, triage, mitigation, resolution, and communication.
- **k8s-manifest-generator** — Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims.
- **k8s-security-policies** — Comprehensive guide for implementing NetworkPolicy, PodSecurityPolicy, RBAC, and Pod Security Standards in Kubernetes.
- **kubernetes-architect** — Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration.
- **kubestellar-console** — Multi-cluster Kubernetes dashboard with AI-powered operations via MCP server and 10+ built-in agent skills
- **mise-configurator** — Generate production-ready mise.toml setups for local development, CI/CD pipelines, and toolchain standardization.
- **monte-carlo-analyze-root-cause** — Investigate data incidents and find root causes using Monte Carlo's observability data. Guides the agent through systematic investigation: alert lookup, lineage tracing, ETL checks, query analysis, and data profiling.
- **observability-and-instrumentation** — Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when shipping any feature that runs in production and you need evidence it works.
- **observability-monitoring-monitor-setup** — You are a monitoring and observability expert specializing in implementing comprehensive monitoring solutions. Set up metrics collection, distributed tracing, log aggregation, and create insightful da
- **observability-monitoring-slo-implement** — You are an SLO (Service Level Objective) expert specializing in implementing reliability standards and error budget-based engineering practices. Design comprehensive SLO frameworks, establish meaningful SLIs, and create monitoring systems that balance reliability with feature velocity.
- **service-mesh-observability** — Complete guide to observability patterns for Istio, Linkerd, and service mesh deployments.
- **shipping-and-launch** — Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.
- **sshepherd** — Zero-knowledge SSH ops CLI — server health checks, docker/systemd control, log tailing, Postgres introspection, and declarative deploys, without ever exposing credentials to the agent.
- **terraform-aws-modules** — Terraform module creation for AWS — reusable modules, state management, and HCL best practices. Use when building or reviewing Terraform AWS infrastructure.
- **terraform-module-library** — Production-ready Terraform module patterns for AWS, Azure, and GCP infrastructure.
- **terraform-skill** — Terraform infrastructure as code best practices
- **terraform-specialist** — Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructure patterns.
- **vibecode-production-qa-validator** — 13-phase production QA for fullstack Next.js apps: build verification, SEO tags, OG images, favicon, route regression, API auth, page speed, lazy load, vulnerability scan, UI/UX cards, error boundaries, database, secure rendering, and cleanup.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/devops/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/devops`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
