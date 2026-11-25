---
name: argocd-deploy
description: GitOps continuous deployment for Kubernetes with ArgoCD
version: 1.0.0
tags: [devops, kubernetes, gitops, cd]
---

# ArgoCD – GitOps for Kubernetes

ArgoCD is a declarative, GitOps-based CD tool for Kubernetes that
automatically syncs application state from Git repositories.

- **GitHub**: github.com/argoproj/argo-cd (18 000+ ⭐)
- **License**: Apache-2.0
- **Security**: CNCF graduated project. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{ARGOCD_URL}}` | Base URL of the ArgoCD server |
| `{{ARGOCD_TOKEN}}` | Authentication token |

## Usage Examples

### List applications

```bash
curl -s "{{ARGOCD_URL}}/api/v1/applications" \
  -H "Authorization: Bearer {{ARGOCD_TOKEN}}"
```

### Sync an application

```bash
curl -s -X POST "{{ARGOCD_URL}}/api/v1/applications/my-app/sync" \
  -H "Authorization: Bearer {{ARGOCD_TOKEN}}"
```

## AI Agent Tips

- Pulls desired state from Git and applies it to K8s clusters.
- Self-healing: auto-corrects configuration drift.
- Supports Helm, Kustomize, and plain YAML manifests.
- Integrates with Jenkins, GitHub Actions, and GitLab CI for full CI/CD.
