---
name: domino-projects
description: Work with Domino Projects, covering Git-based vs Domino File System (DFS) projects, creating projects (UI and API), Git credentials and repositories, file paths in runs, syncing and branches, collaborator roles and visibility, project settings (default environment, hardware tier, environment variables), copying, importing, archiving, goals and status. Use when creating or configuring a project, connecting a Git repository, adding collaborators, finding where code, data and artifacts are mounted, or automating project operations over REST or python-domino.
compatibility: Domino 6.3 and Domino Cloud. API calls need DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. Public visibility and project forking exist on Domino 6.3 only; Domino Cloud is Private or Searchable and uses copies instead of forks.
---

# Domino projects

Applies to Domino 6.3 and Domino Cloud.

A project holds the code, data links, artifacts and people for one piece of work; Apps, endpoints, Launchers and scheduled Jobs publish from it. REST and SDK details with request bodies: [PROJECTS-API.md](./PROJECTS-API.md); the python-sdk catalog: [API-PROJECTS.md](../domino-python-sdk/API-PROJECTS.md). Auth and base URL: [domino-api-intro](../domino-api-intro/SKILL.md#authentication).

## Project types

| | Git-based (recommended) | DFS |
|---|---|---|
| Code lives | Your Git provider (GitHub, GitLab, Bitbucket, others over HTTPS or SSH) | Domino's internal repository, auto-versioned on sync |
| Code path in a run | `/mnt/code` | `/mnt` (`$DOMINO_WORKING_DIR`; becomes `/mnt/<owner>/<project>` once this project imports another project) |
| Artifacts | `/mnt/artifacts` (stored in DFS, separate from Git) | Alongside the code in the working directory |
| Project Datasets | `/mnt/data/<dataset>` | `/domino/datasets/local/<dataset>` |
| Imported Git repositories | `/mnt/imported/code/<repo>` | `/repos/<repo>` |
| Sync | You push code; Domino auto-syncs only artifacts after a Job | **Sync to Domino** records a new revision |
| Copy | Deep copy (new repository) or reference copy (shared repository, API only) | Copy from the overview page |

Git LFS is not supported; files over 2 GB in a repository can break Workspace setup. Keep bulk data in Datasets, not in code or artifacts (projects hold at most 10,000 files by default).

From a laptop, the Domino CLI syncs a DFS project's files (`domino get`, `sync`, `download`, `upload`) and starts its Jobs (`domino run`); on a Git-based project it syncs only the Artifacts, while code goes through git and Jobs through the UI or API: [domino-cli](../domino-cli/SKILL.md).

## Create a project

UI: **Develop** > **Projects** > **Create Project**: name, template or none, **Visibility**, then the Git provider (credentials, an existing repository URL, or a repository Domino creates) or **Domino (local hosting)** for DFS. Private repositories, pushes and SSH need Git credentials: **Account Settings** > **Git Credentials**, or `POST /v4/accounts/{userId}/gitcredentials` (non-public route; may change in a future Domino version, see [route types](../domino-api-intro/SKILL.md#route-types); bodies in PROJECTS-API.md), with an SSH key, a personal access token, or username and password (Bitbucket Data Center: username plus token; Bitbucket Cloud: an app password).

API: `POST /api/projects/v2/projects` (6.3 and Cloud) with `name`, `description`, `visibility` (`private`, `searchable`; `public` on 6.3 only) and optional `mainRepository{uri, serviceProvider, gitCredentialId, defaultRef}`, `repoToCreate`, `templateDetails`, `ownerId`, `billingTag`, `isRestricted`. Examples in [PROJECTS-API.md](./PROJECTS-API.md).

## Collaboration

Project roles are independent of a user's Domino role. There is no "Admin" project role.

| Role | Can |
|------|-----|
| Owner | Everything below, plus rename, transfer, archive, change visibility, change collaborator roles |
| Contributor | Read and write files, start runs and Workspaces, set environment variables, invite collaborators, change the default environment and tier, publish endpoints and Apps, create Launchers |
| Results Consumer | Read files, view completed runs and Workspaces, use published Apps |
| Launcher User | Run Launchers and see their results; no file access |
| Project Importer | Import the project's exported files or variables; nothing else |

Add collaborators under **Settings** > **Access & Sharing** (username, email or organization, role, notification preference). API: `POST /api/projects/v1/projects/{projectId}/collaborators` with `{"id": "<user or organization id>", "role": "contributor|resultsConsumer|launcherUser|projectImporter"}`; remove with `DELETE .../collaborators/{collaboratorId}`.

Visibility (**Settings** > **Access & Sharing**, or `PATCH /v4/projects/{projectId}/visibility`, non-public route; may change in a future Domino version; see PROJECTS-API.md): **Private** (collaborators only) or **Searchable** (name and description in search; contents for collaborators). **Public** (anyone with the URL, even without an account) exists on Domino 6.3 only.

## Settings

- **Hardware & Environment**: default hardware tier, default environment and volume size (default 10 GiB) for every Workspace and Job; contributors can change them, in the UI or with `GET`/`PUT /v4/projects/{projectId}/settings` (non-public route; may change in a future Domino version; PROJECTS-API.md). Environment details: `domino-environments`.
- **Environment variables**: project-level key/value pairs injected into runs (values up to 64 K), visible to all collaborators, for credentials that must stay out of code. Endpoints do not inherit them.
- Default Git branch (Git-based): owners set it in settings; by API, `PUT .../repositories/{repositoryId}/default-ref` (Domino Cloud only; `_` for the main repository).
- **Results**: save run results on the main line or in isolated branches. **Exports**: let other projects import files, environment variables or a code package.

## Lifecycle

- **Rename** (owner, **Settings** > **Access & Sharing**): endpoints are unpublished and get new URLs; local CLI copies must be re-cloned.
- **Copy**: DFS from the overview copy icon; Git-based with **Copy** (deep copy) or `POST /api/projects/v1/projects/{projectId}/copy-project` with `deepCopy` or `referenceCopy`. Collaborators, run history and published assets are not copied; `copyDatasets: true` copies Datasets (API only).
- **Fork**: 6.3 DFS projects only (**Fork** on the overview). Domino Cloud has no forks; copy instead, or use Git branches.
- **Import** another project's exports: **Code** > **Other Projects** > **Import a Project** (`<username>/<project>`), mounted read-only at `/mnt/<username>/<project>`.
- **Transfer ownership** (**Settings** > **Archive Project or Transfer Ownership**): endpoints stop serving until the new owner re-publishes them.
- **Archive**: stops scheduled and running executions, blocks CLI transfers, removes discoverable Apps. API: `DELETE /api/projects/beta/projects/{projectId}`. Unarchiving needs Domino support.
- **Status and goals**: `PUT .../status` (`active` or `complete`, `isBlocked`, `blockedReason`), `GET` and `POST .../goals`.

## Which path applies

```bash
curl -s "$DOMINO_API_HOST/version"   # "version": "6.3.x" self-managed; "6.4.x" or later on Domino Cloud
```

6.3: `public` visibility and DFS forks exist. Cloud: visibility is `private` or `searchable`, there are no forks, and the extra routes `.../repositories/{repositoryId}/default-ref`, `/readme`, `/file-metadata` and `/rendered-file` are available.

## Documentation

- https://docs.domino.ai/cloud/platform-capabilities/core-concepts/projects/index (create, manage, settings, Git-based, DFS, files, collaborate)
- 6.3: https://docs.domino.ai/6.3/platform-capabilities/core-concepts/projects/index
