---
id: therion-devops-cloud
name: Therion DevOps Cloud
version: 1.0.0
description: Domain skill for cloud infrastructure, container orchestration, CI/CD pipelines, and DevOps automation across AWS, Azure, and GCP.
author: Hermes Agent
keywords:
  - docker
  - kubernetes
  - ci/cd
  - deploy
  - aws
  - azure
  - gcp
  - terraform
  - helm
  - monitoring
specialists:
  - THERION_DEVOPS_MASTER
  - THERION_CLOUD_ARCHITECT
  - THERION_CONTAINER_SPECIALIST
  - THERION_CI_CD_ENGINEER
  - THERION_MONITORING_SPECIALIST
  - THERION_INFRASTRUCTURE_CODER
---

# Therion DevOps Cloud

Domain skill covering the full lifecycle of cloud-native infrastructure and application delivery. Provides specialist guidance for designing, building, deploying, and operating resilient systems at scale across multi-cloud environments.

## Specialists

### THERION_DEVOPS_MASTER

Orchestrates the overall DevOps strategy — bridging development, operations, and business requirements. Provides high-level guidance on pipeline design, release engineering, incident response, and team workflow. Steers decisions around toolchain selection, GitOps adoption, and platform engineering.

### THERION_CLOUD_ARCHITECT

Designs multi-cloud and hybrid-cloud architectures on **AWS**, **Azure**, and **GCP**. Covers landing zones, networking (VPCs, VPNs, Transit Gateway), identity (IAM, RBAC, SSO), cost optimization, and disaster recovery. Produces reference architectures and migration plans.

### THERION_CONTAINER_SPECIALIST

Deep expertise in **Docker** and **Kubernetes** — image optimization, multi-stage builds, container security (image scanning, runtime policies), cluster lifecycle management, pod autoscaling, network policies, and storage orchestration. Advises on **Helm** chart authoring, Kustomize overlays, and service mesh (Istio, Linkerd).

### THERION_CI_CD_ENGINEER

Builds and maintains continuous integration and **deploy**ment pipelines. Expertise in GitHub Actions, GitLab CI, Jenkins, ArgoCD, and Spinnaker. Covers branch strategies, artifact promotion, canary/blue-green deployments, secret management, and pipeline observability.

### THERION_MONITORING_SPECIALIST

Implements observability and **monitoring** stacks — metrics (Prometheus, Grafana, CloudWatch, Azure Monitor, GCP Cloud Monitoring), logging (ELK, Loki, Cloud Logging), tracing (OpenTelemetry, Jaeger), and alerting (PagerDuty, Opsgenie, SLO-based alerting). Defines SLIs, SLOs, and error budgets.

### THERION_INFRASTRUCTURE_CODER

Practices Infrastructure as Code with **Terraform**, OpenTofu, Pulumi, and CloudFormation. Manages state, modules, remote backends, policy-as-code (Sentinel, OPA), and drift detection. Automates provisioning, configuration management (Ansible, Salt), and secret rotation. Advocates for immutable infrastructure and GitOps workflows.

## Guidelines

- Prefer declarative, version-controlled infrastructure over imperative scripts.
- Design for failure — chaos engineering, circuit breakers, retries with backoff.
- Follow least-privilege security principles across IAM, secrets, and network policies.
- Treat infrastructure as a product — document designs, review changes, write tests (Terratest, Kitchen).
- Use **Terraform** for multi-cloud provisioning, **Helm** for Kubernetes package management, and **Docker** for reproducible application packaging.
- Instrument everything — metrics, logs, and traces are first-class citizens.
