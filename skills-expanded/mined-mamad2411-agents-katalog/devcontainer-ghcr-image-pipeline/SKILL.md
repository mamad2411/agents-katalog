---
name: devcontainer-ghcr-image-pipeline
description: GitHub Actions workflow for building and publishing a custom devcontainer image to GHCR using devcontainers/ci, with tag transformation and Renovate trigger — pattern from mmalyska/home-ops
---

# Devcontainer GHCR Image Pipeline

## When to Use

Use this skill when setting up a GitHub Actions workflow to automatically build and publish a custom devcontainer image to GHCR (`ghcr.io`). This is the pattern used in `mmalyska/home-ops`.

---

## Directory Layout

The devcontainer definition lives under `.github/.devcontainer/` (not the root `.devcontainer/`). This separates the repo's development environment from the published image's source:

```
.github/
├── .devcontainer/
│   ├── devcontainer.json    ← defines the image to build
│   └── Dockerfile           ← image definition (if custom build)
└── workflows/
    └── devcontainer-publish.yaml
.devcontainer/
    └── devcontainer.json    ← references the published ghcr.io image
```

---

## Complete Workflow

Create `.github/workflows/devcontainer-publish.yaml`:

```yaml
name: Devcontainer
on:
  workflow_dispatch:
    inputs:
      confirm:
        description: 'Type "yes" to confirm manual publish'
        required: true
        default: "no"
  pull_request:
    paths:
      - ".github/.devcontainer/**"
  push:
    branches:
      - "main"
    paths:
      - ".github/.devcontainer/**"

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: OWNER/REPO-devcontainer   # ← replace with actual owner/repo

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        # renovate: datasource=github-releases depName=docker/setup-buildx-action
        uses: docker/setup-buildx-action@v3

      - name: Log into registry
        if: github.event_name != 'pull_request'
        # renovate: datasource=github-releases depName=docker/login-action
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract Docker metadata
        id: meta
        # renovate: datasource=github-releases depName=docker/metadata-action
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      # The devcontainers/ci action needs just the tag portion, not the full image:tag string
      - name: Strip registry prefix from tags
        id: dcmeta
        run: |
          prefix="${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}"
          input_list="$DOCKER_METADATA_OUTPUT_TAGS"
          result_list="${input_list//${prefix}:/}"
          echo "tags=$result_list" >> "$GITHUB_OUTPUT"

      - name: Build and push devcontainer image
        # renovate: datasource=github-releases depName=devcontainers/ci
        uses: devcontainers/ci@v0.3
        with:
          imageName: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          imageTag: ${{ steps.dcmeta.outputs.tags }}
          cacheFrom: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          push: filter
          refFilterForPush: refs/heads/main
          eventFilterForPush: push
          subFolder: .github   # ← points to .github/.devcontainer/

  renovate:
    name: Trigger Renovate
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    uses: OWNER/REPO/.github/workflows/scheduled-renovate.yaml@main
    secrets: inherit
```

---

## Key Concepts

### Tag Transformation Step

`docker/metadata-action` outputs tags as `ghcr.io/owner/repo:main`, `ghcr.io/owner/repo:sha-abc123`, etc. The `devcontainers/ci` action expects **only the tag portion** (`main`, `sha-abc123`). The strip step removes the `ghcr.io/owner/repo:` prefix.

### Push Filter

The `push: filter` + `refFilterForPush: refs/heads/main` combination means:
- On PRs: the image is built but NOT pushed (validates the build)
- On push to main: the image is built AND pushed

### cacheFrom

```yaml
cacheFrom: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
```

Pulls the previously published image as a layer cache, dramatically speeding up builds.

### Renovate Trigger

After a new image is pushed, calling the `scheduled-renovate.yaml` workflow immediately causes Renovate to detect the new digest and open an update PR for `.devcontainer/devcontainer.json`. Without this step, Renovate waits for its next scheduled run.

---

## Referencing the Published Image

In `.devcontainer/devcontainer.json` (the developer-facing file):

```json
{
  "name": "my-project",
  "image": "ghcr.io/owner/repo-devcontainer:main@sha256:abc123..."
}
```

The digest (`@sha256:...`) ensures reproducibility. Renovate will keep this updated automatically via the `devcontainer-regex-manager` preset.

---

## Required Repository Settings

1. **Packages permission**: The workflow uses `packages: write`. The package must be connected to the repo or the GITHUB_TOKEN must have explicit package access.
2. **Branch protection**: If main is protected, ensure the Renovate bot is allowed to push directly (for `automergeType: "branch"`).
3. **Reusable workflow**: The Renovate trigger step assumes `scheduled-renovate.yaml` exists. Replace with `workflow_dispatch` on the Renovate app if using the cloud service.
