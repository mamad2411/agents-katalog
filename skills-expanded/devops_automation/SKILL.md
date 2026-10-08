---
name: devops-automation
description: DevOps automation covering CI/CD, container orchestration, and infrastructure as code.
---

# DevOps Automation

End-to-end DevOps pipeline automation.

## CI/CD Pipelines
- **GitHub Actions**: Reusable workflows, composite actions, matrix builds, caching
- **GitLab CI**: DAG pipelines, auto-devops, review apps
- **Jenkins**: Declarative pipelines, shared libraries, agents
- **CircleCI**: Orbs, workflows, executors, contexts

## Container Orchestration
- **Docker**: Multi-stage builds, BuildKit, layer caching, distroless images
- **Kubernetes**: Deployments, services, ingress, configmaps, secrets, HPAs
- **Helm**: Chart templating, values hierarchy, subcharts
- **Kustomize**: Overlays, patches, bases

## Infrastructure as Code
- **Terraform**: Modules, workspaces, state management, policy as code
- **Pulumi**: Component resources, stacks, cross-stack references
- **Ansible**: Roles, playbooks, inventory, dynamic inventory
- **Packer**: Image building, post-processors, variable injection

## Observability
- **Metrics**: Prometheus, Grafana, custom metrics, SLO/SLI
- **Logs**: Loki, ELK, structured logging, log aggregation
- **Traces**: Jaeger, OpenTelemetry, distributed tracing
- **Alerting**: Alertmanager, Opsgenie, PagerDuty integration

## GitOps
- **ArgoCD**: Application sets, sync waves, health checks
- **Flux**: Kustomize, Helm, notifications, image reflection
- **Pipeline**: PR-based deployment, auto-merge, rollback

## Automation Scripts
```bash
# Zero-downtime deploy pattern
1. Build new image → push to registry
2. Deploy new version (canary or blue-green)
3. Health check new instances
4. Drain and remove old instances
5. Verify metrics and rollback if needed
```
