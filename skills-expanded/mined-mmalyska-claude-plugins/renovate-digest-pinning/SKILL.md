---
name: devcontainer-renovate-digest-pinning
description: How to pin a devcontainer image to a digest and keep it automatically updated by Renovate — using mmalyska/renovate-config devcontainer preset and per-file automerge rule
---

# Devcontainer Renovate Digest Pinning

## When to Use

Use this skill when setting up automatic digest updates for a devcontainer image. It covers:
1. Writing the `"image"` field with a pinned digest
2. The Renovate preset that detects the digest
3. The automerge rule to merge digest updates without review

For the image build pipeline that publishes the image, see the `ghcr-image-pipeline` skill.

---

## Step 1: Pin the Image to a Digest

In `.devcontainer/devcontainer.json`, write the `"image"` field as `name:tag@sha256:digest`:

```json
{
  "image": "ghcr.io/owner/repo-devcontainer:main@sha256:190379025cb9f2537f50b0ac9dff75207e62c1a2d986b251eea4f1b8d0966b5a"
}
```

**Why pin to a digest?** Tags are mutable — `main` can point to a different image layer after a rebuild. Pinning to a digest guarantees reproducibility and lets Renovate detect exactly when a new image was published.

---

## Step 2: Get the Current Digest

When first setting up or after a manual publish:

```bash
# Pull the image and show its digest
docker pull ghcr.io/owner/repo-devcontainer:main
docker inspect ghcr.io/owner/repo-devcontainer:main --format '{{index .RepoDigests 0}}'
# Output: ghcr.io/owner/repo-devcontainer@sha256:abc123...

# Or use crane (no pull required)
crane digest ghcr.io/owner/repo-devcontainer:main
```

Use the `sha256:...` portion as the digest in the image reference.

---

## Step 3: Enable the Renovate Preset

Ensure your `renovate.json5` (or `renovate.json`) includes the base preset or the devcontainer-specific preset:

```json5
{
  "extends": [
    "github>mmalyska/renovate-config"   // includes devcontainer-regex-manager
  ]
}
```

The `devcontainer-regex-manager.json5` preset matches:

```json5
// Pattern it matches in devcontainer.json:
"image": "name:tag@sha256:digest"
// or (without digest):
"image": "name:tag"
```

---

## Step 4: Add the Per-File Automerge Rule

Add a `packageRule` scoped to `.devcontainer/devcontainer.json` so digest updates merge automatically without requiring review:

```json5
// .github/renovate/autoMerge.json5 (or inline in renovate.json5)
{
  "packageRules": [
    {
      "description": "Auto merge devcontainer image digest updates",
      "matchDatasources": ["docker"],
      "automerge": true,
      "automergeType": "branch",
      "matchUpdateTypes": ["digest"],
      "matchFileNames": [".devcontainer/devcontainer.json"],
      "ignoreTests": true
    }
  ]
}
```

`ignoreTests: true` is appropriate here because:
- The update is a digest change (same tag, new build)
- The devcontainer image change doesn't affect CI test results
- The purpose is purely to stay current with the latest published image

---

## Step 5: Trigger Renovate After Image Build

If using the `ghcr-image-pipeline` workflow, add a Renovate trigger job after the build:

```yaml
renovate:
  name: Trigger Renovate
  needs: build
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  uses: OWNER/REPO/.github/workflows/scheduled-renovate.yaml@main
  secrets: inherit
```

This immediately triggers Renovate to detect the new digest and open an update PR, rather than waiting for the next scheduled run.

---

## How It Works End-to-End

```
1. Push to main (or merge a PR changing .github/.devcontainer/)
   ↓
2. devcontainer-publish.yaml runs
   ↓
3. New image published to ghcr.io/owner/repo:main (new digest)
   ↓
4. Renovate triggered by post-build job
   ↓
5. Renovate detects the digest changed in .devcontainer/devcontainer.json
   ↓
6. Renovate opens/updates a PR with new digest
   ↓
7. automergeType: "branch" merges it automatically
   ↓
8. .devcontainer/devcontainer.json now pinned to the new digest ✓
```
