---
title: "DevOps Development — v1"
description: "DevOps and CI/CD development best practices"
globs: ["**/*.yml", "**/*.yaml", "**/*.sh", "Dockerfile*", "docker-compose*"]
alwaysApply: false
priority: medium
---

# DevOps Development Rules

## Technology Stack
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins
- **Containers**: Docker, Kubernetes
- **Infrastructure**: Terraform, CloudFormation
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack, Fluentd

## Core Principles
- Implement infrastructure as code
- Use continuous integration and deployment
- Implement proper monitoring and logging
- Follow security best practices
- Use automation for repetitive tasks

## Project Structure
.github/               # GitHub Actions
├─ workflows/         # CI/CD workflows
├─ actions/           # Custom actions
└─ templates/         # Workflow templates
docker/               # Docker files
├─ Dockerfile         # Application Dockerfile
├─ docker-compose.yml # Local development
└─ .dockerignore      # Docker ignore file
infrastructure/        # Infrastructure code
├─ terraform/         # Terraform configurations
├─ kubernetes/        # Kubernetes manifests
└─ scripts/           # Infrastructure scripts

## Coding Standards
- Use kebab-case for file names
- Use descriptive names for resources
- Follow YAML/JSON conventions
- Use proper indentation (2 spaces for YAML)
- Use consistent naming conventions

## Best Practices
- Implement infrastructure as code
- Use proper version control
- Implement proper testing
- Use proper security measures
- Implement proper monitoring

## Common Patterns
- CI/CD pipelines
- Infrastructure as code
- Container orchestration
- Monitoring and alerting
- Security and compliance

## Testing Strategy
- Test infrastructure code
- Implement proper validation
- Use proper testing tools
- Test security measures
- Maintain high test coverage
