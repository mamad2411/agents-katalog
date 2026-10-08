---
name: combine-docs
description: Combine documentation from multiple NeuronSphere repositories
version: "1.0"
author: HMD Labs
requires:
  - hmd-cli-bartleby
tags:
  - documentation
  - sources
  - multi-repo
  - manifest
  - artifacts
---

# Combine Docs

Combine documentation from multiple NeuronSphere repositories into a single Bartleby build using pre-build artifacts and the `bartleby.sources` manifest configuration.

## Instructions

When the user invokes this skill, follow these steps:

### Step 1: Gather Requirements

Ask the user:
1. **Which repositories** should be included? (e.g., `hmd-lib-auth`, `hmd-ms-gozer`)
2. **What versions** of each repository? (e.g., `~= 0.2`, `~= 1.0`)
3. **What titles** should appear in the combined table of contents for each source?

If the user is unsure about versions, check sibling directories or suggest using `~= 0.1` as a starting point.

### Step 2: Add Pre-Build Artifacts

Update `meta-data/manifest.json` to download documentation artifacts from each dependency before building. Add entries to `build.pre_build_artifacts`:

```json
{
  "build": {
    "commands": [["python"]],
    "pre_build_artifacts": [
      ["hmd-lib-auth@0.2:docs", "target/artifacts/hmd-lib-auth/"],
      ["hmd-ms-gozer@1.0:docs", "target/artifacts/hmd-ms-gozer/"]
    ]
  }
}
```

The artifact format is: `<repo-name>@<version>:<artifact-type>`

Common artifact types:
- `docs` — RST documentation from the `docs/` directory
- `python` — Built Python packages
- `docker` — Docker images

### Step 3: Add bartleby.sources Configuration

Add source entries to `meta-data/manifest.json` under `bartleby.sources`:

```json
{
  "bartleby": {
    "sources": {
      "hmd-lib-auth": {
        "artifact_path": "target/artifacts/hmd-lib-auth",
        "docs_root": "docs",
        "title": "Authentication Library"
      },
      "hmd-ms-gozer": {
        "artifact_path": "target/artifacts/hmd-ms-gozer",
        "docs_root": "docs",
        "title": "Gozer Microservice"
      }
    }
  }
}
```

Each source entry requires:
- `artifact_path` — Path to the downloaded artifact (relative to repo root)
- `docs_root` — Subdirectory within the artifact containing RST docs (usually `docs`)
- `title` — Display title for the toctree caption in the combined output

### Step 4: Add Sources Marker to index.rst

Check `docs/index.rst` for a `.. bartleby-sources::` directive. If not present, add it where source documentation should be injected:

```rst
.. HMD <repo-name> documentation master file

<repo-name>
===============================================================

.. toctree::

   install_and_run
   proposals/index

.. bartleby-sources::
```

The marker tells Bartleby exactly where to inject the source toctrees. If no marker is present, Bartleby uses fallback strategies:

1. **Marker replacement** (preferred): Replace `.. bartleby-sources::` with generated toctrees
2. **Before "Indices and tables"**: Insert before the standard Sphinx footer section
3. **Append**: Add to end of file if neither marker nor footer is found

### Step 5: Explain the Build Flow

The combined documentation build requires two steps:

```bash
# Step 1: Download pre-build artifacts (the -pdo flag runs only pre_build_artifacts)
hmd build -pdo

# Step 2: Build documentation (stages sources, injects toctrees, builds, then cleans up)
bartleby
```

Or as a single flow:

```bash
hmd build -pdo && bartleby
```

**What happens during the build:**

1. `hmd build -pdo` downloads artifacts from each source repo into `target/artifacts/`
2. `bartleby` reads `bartleby.sources` from the manifest
3. Source docs are staged into `docs/_sources/<key>/` (temporary copy)
4. Toctree entries are injected into `index.rst` (at the marker or using fallback)
5. Sphinx builds the combined documentation
6. Staged sources and injected toctrees are cleaned up (index.rst is restored)

### Step 6: Verify

After setup, offer to run the build and verify:

```bash
hmd build -pdo && bartleby html
```

Check `./target/bartleby/` for the rendered output containing all source documentation.

## Example

### Input

User: "Combine docs from hmd-lib-auth and hmd-ms-gozer into this repo's documentation"

### Generated manifest.json Changes

Before:
```json
{
  "name": "hmd-docs-platform",
  "build": {
    "commands": [["python"]]
  }
}
```

After:
```json
{
  "name": "hmd-docs-platform",
  "build": {
    "commands": [["python"]],
    "pre_build_artifacts": [
      ["hmd-lib-auth@0.2:docs", "target/artifacts/hmd-lib-auth/"],
      ["hmd-ms-gozer@1.0:docs", "target/artifacts/hmd-ms-gozer/"]
    ]
  },
  "bartleby": {
    "sources": {
      "hmd-lib-auth": {
        "artifact_path": "target/artifacts/hmd-lib-auth",
        "docs_root": "docs",
        "title": "Authentication Library"
      },
      "hmd-ms-gozer": {
        "artifact_path": "target/artifacts/hmd-ms-gozer",
        "docs_root": "docs",
        "title": "Gozer Microservice"
      }
    }
  }
}
```

### Generated index.rst Addition

```rst
.. toctree::

   install_and_run
   proposals/index

.. bartleby-sources::
```

### Build Commands

```bash
hmd build -pdo && bartleby html
```

The rendered HTML at `./target/bartleby/` will include the main repo's docs plus toctree sections for "Authentication Library" and "Gozer Microservice", each linking to the sourced documentation.
