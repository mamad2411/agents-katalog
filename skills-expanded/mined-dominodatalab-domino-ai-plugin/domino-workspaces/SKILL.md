---
name: domino-workspaces
description: Work with Domino Workspaces - interactive sessions running Jupyter, JupyterLab, VS Code or RStudio on a hardware tier with a compute environment. Covers launching and configuring a Workspace, what persists across stop and resume, file paths and syncing for DFS and Git-based Projects, package and home-directory persistence, SSH access from a local IDE, the Workspace API routes, and troubleshooting. Use when setting up or debugging an interactive development session in Domino.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino Workspaces

Applies to Domino 6.3 and Domino Cloud.

A Workspace is a durable interactive session: a container on a hardware tier running an IDE from the selected compute environment, with a persistent volume for the Project files. IDEs (Jupyter, JupyterLab, VS Code, RStudio, custom tools) come from the environment's Pluggable Workspace Tools ([domino-environments](../domino-environments/SKILL.md)); batch work: a Job ([domino-jobs](../domino-jobs/SKILL.md)).

Docs: https://docs.domino.ai/cloud/platform-capabilities/core-concepts/workspaces (same paths under `/6.3/`).

## Launch a Workspace (UI)

1. **Workspaces** > **+ Create New Workspace**, name it.
2. **Compute Environment**; **Change** pins a revision (the owner's active revision is recommended; restricted Projects limit the choice).
3. **IDE**: the list depends on the environment.
4. **Volume Size** if provisioning recommendations are enabled (Git-based Projects use the Project setting on first launch).
5. **Next**: **Hardware Tier** (by data plane on Nexus; smallest that fits), then only the Datasets, NetApp Volumes and external volumes you need (per-asset snapshot pins).
6. **Next**: optional Spark, Ray, Dask, MPI ([domino-distributed-computing](../domino-distributed-computing/SKILL.md)) or Slurm ([domino-hpc-slurm](../domino-hpc-slurm/SKILL.md)) cluster.
7. Additional settings: **Enable SSH access**, **Package Persistence**, **Home Directory Persistence**; **Launch**. Default limit: four Workspaces per user per Project.

**Settings > Edit Settings** changes tier or environment (**Save & Restart**); by API, [API.md](./API.md).

## Paths and what persists

| | DFS Project | Git-based Project |
|---|---|---|
| `DOMINO_WORKING_DIR` | `/mnt` (Project files) | `/mnt/code` (main repository) |
| Artifacts (DFS-tracked) | part of `/mnt` | `/mnt/artifacts` |
| Imported repos / Projects | `/mnt/imported/...` | `/mnt/imported/...` |
| Datasets | `/domino/datasets/local/<name>` | `/mnt/data/<name>` |

- Stop/resume keeps files under `/mnt` (Git-based: `/mnt/code`, `/mnt/artifacts`, `/mnt/imported`, not loose files in `/mnt` itself). Anything outside `/mnt`, including installed packages, is lost unless persistence is on.
- Saving in the IDE does not sync. Use **File Changes**: **Sync to Domino** / **Sync All Changes** (DFS; only `/mnt` is synced) or **Sync to Git** and **Pull** (Git-based). A Workspace launched from a commit is in detached HEAD: `git checkout -b <branch>` before syncing.
- Auto-shutdown of long-running Workspaces (admin period; shorten under **Account Settings > Workspace Settings**) auto-commits saved files but does not push linked Git repositories.
- Every sync creates a checkpoint; **Workspaces > History > Open** recreates a Workspace from one on a new branch.

## Package and home-directory persistence

- Environment owners tick **Enable Package Persistence** on a revision; the Workspace then offers the **Package Persistence** toggle at launch and restart. `pip install` and `install.packages()` persist, and `requirements.txt` skips packages already present. Custom images need `uv` (Python) and `renv` (R).
- **Home Directory Persistence** keeps `$HOME` (`/home/ubuntu`): IDE settings, `.ssh`, coding-assistant logins; needs `rsync` in the environment.
- On Domino 6.3 both also need the admin configuration records `com.cerebro.domino.workbench.workspace.persistence.packages.enabled` and `...persistence.directories.enabled`.
- Permanent dependencies belong in the environment Dockerfile; `requirements.txt` reinstalls on every start.

## SSH from a local IDE

1. The environment needs `openssh-server` (the DSE has it; custom image: `USER root` / `apt-get install -y openssh-server` / `mkdir -p /var/run/sshd` / `USER ubuntu`).
2. Launch with **Enable SSH access**. Missing checkbox: on 6.3 the admin sets `com.cerebro.domino.workbench.workspace.ssh.enabled`; on Cloud contact Domino support.
3. In the running Workspace open **Settings** > **SSH connection** and install the **Dom CLI** from the link (not the Domino CLI, [domino-cli](../domino-cli/SKILL.md)). Note the **Workspace ID** (also in the URL).
4. Locally: `dom connect <workspace_id> --domino-api-host=https://<browser URL> -l ubuntu` (add `--port 2223` for PyCharm). Add `Include ~/.domino/ssh/config` to `~/.ssh/config`, then connect from VS Code **Remote Explorer > SSH** or PyCharm **Remote Development > SSH** (host = workspace id, user `ubuntu`).

## Workspace sessions over the API

- Resume a stopped Workspace: `POST /api/projects/v1/projects/{projectId}/workspaces/{workspaceId}/sessions` with `{"externalVolumeMounts": [], "netAppVolumeMounts": []}` -> `{"workspaceSession": {"id", "executionId"}, "metadata"}`. `workspaceId` is in the Workspace URL or **Show Details**.
- Create, list, read, update, stop, delete: no public route; the Internal API covers them (`POST /v4/workspace/project/{projectId}/workspace` and the rest in [API.md](./API.md); non-public route; may change in a future Domino version); python-domino has none.
- Authentication: [domino-api-intro](../domino-api-intro/SKILL.md).

### Which path applies

Read `GET $DOMINO_API_HOST/version`. On `6.3.x` use the paths table above. On 6.4 and later (including Domino Cloud) `GET /api/workspace/v1/workspace/{workspaceId}/writable-project-mounts` returns `mainDfsMount`, `mainGitMount`, `importedGitMounts` (`404` = absent).

## Manage Workspaces

**Workspaces > My / All / Deleted** in a Project, or **Develop > Workspaces** globally. **Stop** (storage persists and still bills), **Start** to resume (restricted Projects use the current restricted revision), **Delete** only after stopping and syncing. Auto-deletion, if enabled, follows admin-configurable periods (10 days stopped, 30 days of grace). Per Workspace: **Logs**, **Usage**, **History** (sessions, commits, support bundle).

## Coding assistants and extra apps

- The DSE ships AI coding-assistant VS Code extensions and CLI agents; sign in once and Home Directory Persistence keeps the login. If the LLM Gateway 2.0 Extension is installed, offer to route the assistant through it, never by default ([domino-llm-gateway](../domino-llm-gateway/CODING-ASSISTANTS.md)). Docs: https://docs.domino.ai/cloud/platform-capabilities/features/coding-assistants
- Only the IDE port (8888) is proxied; jupyter-server-proxy (in the DSE) exposes other ports at `https://<browser URL>/<owner>/<project>/notebookSession/$DOMINO_RUN_ID/proxy/<port>/`. App Preview is the way to develop a Domino App.

## Troubleshooting

- **Will not start / queued**: tier capacity or quota, failed environment build (build logs), volume too small, four-Workspace limit.
- **Lost work**: only synced changes reach Domino; check `/mnt` after resume and the **History** checkpoints.
- **Packages gone after restart**: install in the environment or enable Package Persistence.
- **Slow start**: Project files are copied to the volume; put bulk data in a Dataset.

## Reference files

- [JUPYTER.md](./JUPYTER.md): Jupyter and JupyterLab specifics, data paths in notebooks, notebooks as Jobs.
- [VSCODE.md](./VSCODE.md): VS Code in the browser, extensions, settings persistence, Remote-SSH.
- [API.md](./API.md): Workspaces over the API (create, update, stop, resume, delete, clusters).
