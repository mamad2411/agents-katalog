---
name: cloud-platforms
description: Use this skill when authoring or running a workflow that needs cloud-platform-specific commands, or when reviewing such workflows for platform coverage — as a knowledge module (not a workflow itself) providing platform-specific CLI commands, managed service patterns, networking, IAM, observability, and operational procedures across GCP, Azure, and AWS. Loaded by `/analyze-prod`, `/infra-change`, `/deploy-production`, and similar workflows.
disable-model-invocation: true
---

# Cloud Platforms

Pluggable cloud platform knowledge modules. Each resource file contains platform-specific patterns for one cloud provider.

## How It Works

1. **Detect platform**: Read the project's `CLAUDE.md` tech stack declaration to identify which cloud platform(s) are in use
2. **Load the right module**: Read the corresponding resource file(s) below
3. **Apply patterns**: Use platform-specific CLI commands, service names, and operational patterns from the loaded module

## Platform Detection Signals

| Signal in CLAUDE.md / Project | Platform | Resource File |
|---|---|---|
| GCP, Google Cloud, GKE, Cloud SQL, Cloud Build, gcloud, Artifact Registry | **Google Cloud Platform** | `gcp-reference.md` |
| Azure, AKS, Azure SQL, Azure DevOps, az CLI, ACR, Azure Monitor | **Microsoft Azure** | `azure-reference.md` |
| AWS, EKS, RDS, CodePipeline, aws CLI, ECR, CloudWatch | **Amazon Web Services** | `aws-reference.md` |

If CLAUDE.md does not declare a cloud platform, ask the user before proceeding with platform-specific operations.

If the project uses **multi-cloud**, load all relevant modules and apply patterns per service based on where it runs.

## Module Structure

Each reference file follows a consistent structure:

1. **Core Platform** — account/project structure, IAM, networking, secrets, tagging
2. **Container Orchestration** — managed Kubernetes (GKE/AKS/EKS) patterns
3. **Managed Database** — managed SQL service patterns and reliability
4. **CI/CD** — platform-native build and deploy services
5. **Observability** — monitoring, logging, alerting, dashboards
6. **CLI Reference** — essential CLI commands for diagnostics and operations
7. **Security and Compliance** — audit logging, encryption, network security

## Integration

- **Used by roles**: `Agent(devops-engineer)`, `Agent(sre-engineer)`, `Agent(cloud-architect)`
- **Used by workflows**: `/analyze-prod`, `/bugfix`, `/infra-change`, `/deploy-production`
- **Complements**: `deployment-procedures` skill (rollback procedures)
