---
name: renovate-custom-regex-managers
description: Comment-annotation patterns for Renovate to track versions in YAML, Dockerfile, and devcontainer.json files — patterns from mmalyska/renovate-config
---

# Renovate Custom Regex Managers

## When to Use

Use these annotation patterns when a file contains version strings that Renovate's built-in managers don't detect — typically Helm values files, Ansible task files, raw Dockerfiles with ARG versions, or Kubernetes manifests that pin tool versions.

The patterns are provided by the `generic-regex-manager.json5` and `devcontainer-regex-manager.json5` presets in `mmalyska/renovate-config` (included in the base preset).

---

## Pattern 1: Generic Comment Annotation (YAML / Dockerfile)

Annotate a version field in any `.yaml`, `.yml`, or `Dockerfile` with a comment line directly above it:

```yaml
# renovate: datasource=github-releases depName=sigstore/cosign
cosign_version: v2.2.3
```

```yaml
# renovate: datasource=docker depName=docker.io/bitnami/kubectl
kubectl_image_tag: "1.29.2"
```

```yaml
# renovate: datasource=helm depName=prometheus-community/kube-prometheus-stack versioning=semver
chart_version: "57.2.0"
```

```yaml
# renovate: datasource=terraform-provider depName=hashicorp/aws
aws_provider_version: "~> 5.0"
```

The `versioning` field is optional; defaults to `semver` if omitted.

### versionTemplate for non-standard formats

When the version field has a prefix/suffix around the version number, use `versionTemplate`:

```yaml
# renovate: datasource=github-releases depName=aquasecurity/trivy versionTemplate=v{{version}}
TRIVY_VERSION: 0.50.0
```

### kustomize remote URL pattern

For kustomize remote references like `github.com/dep/dep/v1.0.0/folder`:

```yaml
# renovate-raw: datasource=github-releases depName=owner/repo
bases:
  - github.com/owner/repo/v1.0.0/path/to/base
```

---

## Pattern 2: Docker Image in YAML (with digest)

For YAML files containing `image:` fields that need digest pinning:

```yaml
# renovate-docker
  image: docker.io/cloudflare/cloudflared:2024.1.0@sha256:abc123...
```

```yaml
# renovate-docker
  image: ghcr.io/mmalyska/my-app:main@sha256:abc123...
```

The annotation must be on the line directly above the `image:` field. Renovate will update both the tag and the digest.

---

## Pattern 3: devcontainer.json Image

The `devcontainer-regex-manager.json5` preset matches the `"image"` field in `.devcontainer/devcontainer.json`:

```json
{
  "image": "ghcr.io/mmalyska/home-ops-devcontainer:main@sha256:abc123..."
}
```

No annotation comment needed — the manager matches the `"image":` key directly.

Renovate will open a PR to update the digest when a new image is pushed.

---

## Checking Your Annotations

To verify Renovate will pick up your annotations, run the Renovate debug command locally (requires a Renovate installation):

```bash
LOG_LEVEL=debug renovate --token $GITHUB_TOKEN --dry-run owner/repo 2>&1 | grep -A2 "customManagers"
```

Or check the Renovate Dashboard issue in the repo after pushing — any unmatched versions will appear as "no update found".

---

## Adding Custom Managers Beyond the Presets

If you need a regex manager the shared presets don't cover, add it in a local override file:

```json5
// .github/renovate/customManagers.json5
{
  "customManagers": [
    {
      "customType": "regex",
      "description": "Track Go toolchain version in .go-version",
      "fileMatch": ["^\\.go-version$"],
      "matchStrings": ["(?<currentValue>.+)"],
      "depNameTemplate": "golang/go",
      "datasourceTemplate": "github-releases",
      "versioningTemplate": "semver-coerced"
    }
  ]
}
```

Reference this in your `renovate.json5`:
```json5
"extends": [
  "github>mmalyska/renovate-config",
  "local>owner/repo//.github/renovate/customManagers.json5"
]
```
