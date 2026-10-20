---
name: sync-versions
description: Sync SOFTWARE_VERSIONS.md with container image versions defined in blueprint_files.tf. Run this before deploying to ensure the versions doc is current. Run this skill before /deploy-and-test or /integration-test to keep versions in sync.
user-invocable: true
allowed-tools: Read, Grep, Edit, Write, Bash
---

# Sync Software Versions

Parse `ai-accelerator-tf/blueprint_files.tf` to extract all container image references, then update `SOFTWARE_VERSIONS.md` to match.

## Process

### Step 1: Extract image versions from blueprint_files.tf

Read `ai-accelerator-tf/blueprint_files.tf` and extract every container image reference. Images appear in patterns like:

```
"container_image": "nvcr.io/nvidia/cuopt/cuopt:25.10.0-cuda12.9-py3.13"
"image": "docker.io/elasticsearch:9.1.2"
```

Use Grep to find them:

```bash
grep -E '"(container_image|image)"\s*:\s*"[^"]+:[^"]+"' ai-accelerator-tf/blueprint_files.tf
```

Also check for image references in Helm values:
```bash
grep -rE '^\s+repository:|^\s+tag:' ai-accelerator-tf/helm-values/
```

Organize extracted images by starter pack (cuopt, vss, paas_rag, enterprise_rag, enterprise_rag_aiq) and size (small, medium). The starter pack context is determined by the surrounding `local.starter_pack_blueprints["<category>"]["<size>"]` block.

### Step 2: Compare with SOFTWARE_VERSIONS.md

Read `SOFTWARE_VERSIONS.md` and compare each row's image + version against what was extracted. Flag:

- **Version changed** — the image exists in both but the tag differs
- **New image** — present in blueprint_files.tf but missing from SOFTWARE_VERSIONS.md
- **Removed image** — present in SOFTWARE_VERSIONS.md but no longer in blueprint_files.tf

### Step 3: Update SOFTWARE_VERSIONS.md

Apply changes:

- Update version tags for images that changed
- Add rows for new images (in the correct pack/size section)
- Remove rows for images that no longer exist

Preserve the existing table structure and section headings. Do not change rows that are already correct.

### Step 4: Report changes

After updating, print a summary:

```
Updated SOFTWARE_VERSIONS.md:
  - cuopt small: cuopt 25.10.0 → 25.11.0
  - enterprise_rag small: Milvus v2.5.17 → v2.5.18 (new)
  - paas_rag small: llama-stack-oci removed (no longer in blueprint)
No changes needed for: vss, enterprise_rag_aiq
```

## Notes

- If an image is in an internal OCIR registry (`*.ocir.io/`), still update it — don't skip internal images.
- For images with no explicit version tag (e.g., `latest` or no tag), note them in the report but do not alter SOFTWARE_VERSIONS.md for those rows unless the image path itself changed.
- This skill does **not** deploy anything. It only reads source files and updates the doc.
