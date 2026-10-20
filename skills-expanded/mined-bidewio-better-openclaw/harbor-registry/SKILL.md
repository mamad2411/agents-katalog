---
name: harbor-registry
description: Container image registry with Harbor
version: 1.0.0
tags: [containers, registry, docker, security]
---

# Harbor – Enterprise Container Registry

Harbor is a CNCF graduated container registry with vulnerability scanning,
RBAC, replication, and image signing.

- **GitHub**: github.com/goharbor/harbor (25 000+ ⭐)
- **License**: Apache-2.0
- **Security**: CNCF graduated project. Built-in Trivy scanning. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{HARBOR_URL}}` | Base URL of the Harbor instance |
| `{{HARBOR_USER}}` | Username |
| `{{HARBOR_PASSWORD}}` | Password |

## Usage Examples

### List projects

```bash
curl -s -u "{{HARBOR_USER}}:{{HARBOR_PASSWORD}}" \
  "{{HARBOR_URL}}/api/v2.0/projects"
```

### Search repositories

```bash
curl -s -u "{{HARBOR_USER}}:{{HARBOR_PASSWORD}}" \
  "{{HARBOR_URL}}/api/v2.0/search?q=myapp"
```

## AI Agent Tips

- Built-in Trivy vulnerability scanning for container images.
- RBAC per project with LDAP/OIDC integration.
- Image replication across registries for DR and geo-distribution.
- Content trust via Notary for signed images.
