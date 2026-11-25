---
name: domino-environments
description: Create and customize Domino Compute Environments - the Docker images that Workspaces, Jobs, Apps and endpoints run in. Covers Domino Standard, Core, Minimal, GPU and cluster environments, creating environments, Dockerfile instructions, pre/post scripts, environment variables, Pluggable Workspace Tools, revisions and build propagation, requirements.txt versus preloaded packages, the environments REST API, and build troubleshooting. Use when installing dependencies, adding IDEs or tools, or fixing environment build failures.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino Compute Environments

Applies to Domino 6.3 and Domino Cloud.

An Environment is a Docker image plus Domino metadata (tools, scripts, variables, supported clusters). Each build creates a numbered **revision**; executions use the environment's **Active** revision unless they pin another. Containers run as the `ubuntu` user; files Domino tracks live under `/mnt`.

Docs: https://docs.domino.ai/cloud/platform-capabilities/core-concepts/compute-environments (same paths under `/6.3/`).

## Domino-provided environments

| Environment | Image (`quay.io/domino/...`, tag changes per release) | Use |
|---|---|---|
| Domino Standard Environment (DSE) | `domino-standard-environment` (`-no-assistants` variant) | Python, R, Jupyter, JupyterLab, VS Code, RStudio, coding assistants |
| Domino Core Environment (DCE) | `domino-core-environment` | minimal base for custom builds; Jupyter and JupyterLab only |
| Domino Minimal Environment (DME) | `domino-minimal-environment` | lighter DSE |
| Domino GPU Environment (DGE) | `domino-gpu-environment` | CUDA and GPU libraries for GPU tiers |
| Cluster environments | `domino-{spark,ray,dask,mpi}-environment` (execution), `{spark,ray,dask,mpi}-cluster-environment` (nodes) | [domino-distributed-computing](../domino-distributed-computing/SKILL.md); a DSE cannot be a cluster node |

Exact tags and partner images: https://docs.domino.ai/cloud/platform-capabilities/core-concepts/compute-environments/manage-compute-environments/8-compute-environment-catalog.

## Create an environment (UI)

**Govern > Environments > + Create Environment**: name, description, then the base:

- **Start from an existing Environment** with **Active (auto-rebuilds)** (follows the base's active revision) or a pinned revision.
- **Start from a custom base image**: an image URI; keep **Automatically make compatible with Domino** unless it is already a Domino image (absent once a cluster type is selected).

Then **Supported Clusters** (cluster-node environments only), **Visibility** (Private, an Organization, or Global for admins), the revision toggle, and **Create Environment** or **Customize before building**. Later: **Edit Definition** > **Build**; base image and supported clusters cannot change afterwards (duplicate instead). Archive from the environment menu (not while it is a Project default). Project default: **Settings > Hardware & Environment** or `PUT /v4/projects/{projectId}/settings` (non-public route; may change in a future Domino version; [API.md](./API.md#project-default-environment-and-tier)).

## Edit Definition

**Dockerfile Instructions**: no `FROM` (Domino adds it), no access to Project files or user variables at build time, 127-layer limit. Install as root and switch back:

```dockerfile
USER root
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev graphviz \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pandas==2.3.2 scikit-learn==1.7.2   # the DSE's own versions
RUN R --no-save -e "install.packages(c('tidyverse','caret'), repos='https://cloud.r-project.org')" \
    && chown -R ubuntu:ubuntu /usr/local/lib/R/site-library
ENV MODEL_PATH=/mnt/artifacts/model.pkl
USER ubuntu
```

One `pip install` per set of packages, pinned versions, `&&` to merge layers, `ARG NAME` + `ENV NAME=$NAME` to carry a variable into the build. Private Git packages: install at runtime via `requirements.txt` through Domino's Git integration (credential under **Account Settings** > **Git Credentials**), never with credentials in the Dockerfile or in `requirements.txt`.

**Pluggable Workspace Tools**: YAML defining the IDEs offered at launch; [WORKSPACE-TOOLS.md](./WORKSPACE-TOOLS.md).

**Scripts** (bash, run as root at execution time, never on cluster nodes), in order: pre-setup, `requirements.txt` install, post-setup and pre-run, your execution, post-run after it stops. Pre-run script: per-launch setup such as `code-server --install-extension ...` or RStudio preferences.

**Environment variables**: visible in every execution; precedence environment < Project < user. Never use names starting with `DOMINO_` (reserved); no secrets in Dockerfile `ENV`. **Enable VPN Networking** and a revision note complete the form.

## Packages: where to install

| Method | When | Cost |
|---|---|---|
| Dockerfile `RUN pip install ...` | anything used regularly | one build; fastest starts |
| `requirements.txt` in the Project root (`/mnt` on DFS, `/mnt/code` on Git-based) | per-Project extras | reinstalled every start |
| `install.R` + `source('install.R')` | R equivalents | per session |
| Package Persistence (Workspaces) | interactive installs kept across sessions | enable on the revision; custom images need `uv` and `renv` |
| `!pip install --user ...` in a notebook | one-off | lost on restart |

Keep images small; dependency-file packages cost startup time.

## Revisions

- Each build is a revision with build logs (**Revisions** tab > three dots, or by API: [API.md](./API.md#build-logs)). **Auto-assign next new revision as Active** on uses the latest successful build; off pins the Active revision for testing.
- Environments based on **Active (auto-rebuilds)** rebuild when the base's Active revision changes (build propagation; see the **Dependency Tree** tab). Archived environments are not rebuilt.
- Workspaces and Jobs can pin a revision. API: `environmentRevisionSpec` = `ActiveRevision`, `LatestRevision` or `SomeRevision(<revisionId>)`.
- On 6.4+ revisions may declare CPU architectures (`amd64`, `arm64`); a mismatched hardware tier is rejected.

## REST API

Both specs: `GET /api/environments/beta/environments` (list), `GET /api/environments/v1/environments/{environmentId}`, `POST /api/environments/beta/environments`, `POST .../beta/environments/{environmentId}/revisions`, `PATCH .../revisions/{revisionId}` (restricted flag), `DELETE /api/environments/v1/environments/{environmentId}` (archive). Bodies: [API.md](./API.md). Authentication: [domino-api-intro](../domino-api-intro/SKILL.md).

### Which path applies

Read `GET $DOMINO_API_HOST/version`. On `6.3.x` only the routes above exist. On 6.4 and later (including Domino Cloud) `POST /api/environments/v2/environments`, `POST .../v2/environments/{environmentId}/revisions` (preferred there) and `PUT .../v1/environments/{environmentId}/name` / `/description` also exist (`404` = absent).

## Troubleshooting builds

- **Permission denied**: `USER root` before the command, `USER ubuntu` after; `chown -R ubuntu:ubuntu` directories the user must write.
- **Package not found**: wrong name (`scikit-learn`, not `sklearn`), missing apt dependency, or no network from the builder.
- **Build never finishes / killed**: too many layers or packages; split into base and derived environments; read the build log ([API.md](./API.md#build-logs)).
- **IDE missing at launch**: no Pluggable Workspace Tools entry or start script ([WORKSPACE-TOOLS.md](./WORKSPACE-TOOLS.md)).

## Reference files

- [WORKSPACE-TOOLS.md](./WORKSPACE-TOOLS.md): workspace tools YAML, native tool start scripts, VS Code extensions, RStudio preferences, jupyter-server-proxy, SSH.
- [API.md](./API.md): environments REST routes, request bodies, version differences.
