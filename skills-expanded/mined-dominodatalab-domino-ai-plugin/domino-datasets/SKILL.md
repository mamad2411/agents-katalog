---
name: domino-datasets
description: Create, upload to, mount and read a Domino Dataset; take, list, read or restore (copy to a new Dataset) a snapshot; tag snapshots; share a Dataset with another Project or user. Covers mount paths (/domino/datasets/local/<name> in DFS Projects, /mnt/data/<name> in Git-based Projects), the UI and domino CLI steps, and the /api/datasetrw REST routes with request bodies, including how to read a snapshot you just took from the same run. Use whenever a task mentions a Dataset, a snapshot, a dataset mount path, versioned or shared data in Domino, or reading, counting or writing files under /domino/datasets or /mnt/data.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino Datasets

Applies to Domino 6.3 and Domino Cloud.

A Dataset is Domino-managed, versioned filesystem storage. Executions mount it as an ordinary
directory: live data is read-write for Dataset Owners and Editors, read-only for Readers, and
every snapshot is a read-only directory beside it. Sharing is zero-copy; Domino sets no size or
file-count cap. Object storage: domino-data-sdk skill; NetApp ONTAP: netapp-volumes skill.

## Paths

| | DFS Project | Git-based Project |
|---|---|---|
| Dataset of this Project (RW) | `/domino/datasets/local/<name>` | `/mnt/data/<name>` |
| Its snapshots (RO) | `/domino/datasets/local/snapshots/<name>/<n>` and `/<tag>` | `/mnt/data/snapshots/<name>/<n>` and `/<tag>` |
| Dataset shared from another Project | `/domino/datasets/<name>` | `/mnt/imported/data/<name>` |
| Its snapshots (RO) | `/domino/datasets/snapshots/<name>/<n>` and `/<tag>` | `/mnt/imported/data/snapshots/<name>/<n>` and `/<tag>` |

`<n>` is the snapshot number, `<tag>` the most recently added tag. Every Project starts with a
default Dataset named after the Project (`/mnt/data/churn` Git-based, `/domino/datasets/local/churn`
DFS). Detect the layout from the injected variables:

```python
import os
import pandas as pd

root = os.environ["DOMINO_DATASETS_DIR"]          # /mnt/data or /domino/datasets
git_based = os.environ.get("DOMINO_IS_GIT_BASED") == "true"
local = root if git_based else f"{root}/local"
df = pd.read_csv(f"{local}/{os.environ['DOMINO_PROJECT_NAME']}/raw/customers.csv")
```

Full trees, pinned snapshots, tags and read examples: [MOUNT-PATHS.md](./MOUNT-PATHS.md). The
UI lists mounted paths under **Data > Datasets** (Workspace) and **Details > Data** (Job).

## Create a Dataset

- **UI**: in the Project, **Data > Domino Datasets > Create New Dataset**; name, description,
  then users or organizations with a Dataset role (or **Add all project members**), **Finish**.
- **REST**: `POST /api/datasetrw/v1/datasets` with
  `{"name": "...", "description": "...", "projectId": "<project-id>", "grants": []}`;
  `name` is required and unique in the Project; `snapshotId` instead of `projectId` copies a
  snapshot into a new Dataset. All routes and bodies: [API.md](./API.md); auth:
  [domino-api-intro](../domino-api-intro/SKILL.md#authentication).
- **python-domino**: `Domino.datasets_create(dataset_name, dataset_description)` (positional
  names, not `name=`/`description=`) creates it in the client's configured Project through the
  legacy `/dataset` routes (not Public API); prefer the REST route.

## Upload files

- **UI**: open the Dataset, **Upload files**: up to 50 GB or 50,000 files per upload;
  drag-and-drop keeps folders.
- **CLI** (larger uploads): `domino upload-dataset [--fileUploadSetting Ignore|Overwrite|Rename]
  [--targetRelativePath <dir>] <owner>/<project>/<dataset> <local-folder>`; flags and values
  are case-sensitive. Install and sign in: [domino-cli](../domino-cli/SKILL.md).
- **From code**: write to the mount path; it becomes a version when you snapshot.
- **python-domino**: `datasets_upload_files(dataset_id, local_path, ...)`; signature in
  [API.md](./API.md).

## Snapshots and tags

A snapshot is a read-only, immutable copy taken at a point in time. Do not modify files while
one is in progress; time scales with size.

A snapshot is mounted only in executions started after it became `active`. Read
one from the current run with `GET $DOMINO_API_PROXY/v4/datasetrw/snapshot/{snapshotId}/file/raw?path=<file>`
(non-public route; may change in a future Domino version, see [route types](../domino-api-intro/SKILL.md#route-types)). The docs list this route without `/v4`;
that form returns 404.

- **Create**: UI **Take Snapshot** (all or selected files, optional tag);
  `domino create-snapshot <owner>/<project>/<dataset>`; or
  `POST /api/datasetrw/v1/datasets/{datasetId}/snapshots` with `{"relativeFilePaths": ["*"]}`.
  `status` starts `pending` and becomes `active`; poll `GET /api/datasetrw/v1/snapshots/{id}`.
- **Read**: later executions mount it at `.../snapshots/<name>/<n>` or `/<tag>`. From the run
  that took it, use the route above (`path` is relative, no leading slash; list with
  `.../files/recursive?path=`, empty for the root), `DatasetClient` with
  `DatasetConfig(snapshot_id=...)`, or a new Job. Examples: [API.md](./API.md). Pinning a
  snapshot at launch mounts it read-only at the live path.
- **Iterate**: **Copy to New Dataset**, `POST .../datasets` with `snapshotId`, or
  `domino create-dataset-from-snapshot`.
- **Tags** name one snapshot (`snapshots/<name>/<tag>`); Owners and Editors manage them on the
  **Snapshots** page or with `POST .../datasets/{datasetId}/tags`
  `{"snapshotId": "...", "tagName": "production"}` and `DELETE .../tags/{tagName}`. Re-using a
  name returns 400, so to move a tag remove it, then add it.
- **Limits**: default 20 active snapshots per Dataset (6.3 record
  `com.cerebro.domino.dataset.quota.maxActiveSnapshotsPerDataset`; Domino Support on Cloud). At
  the limit an execution that would write a snapshot errors; a manual **Take Snapshot** warns
  and, if you proceed, marks the oldest for deletion (it stops mounting; an admin purges it).
  Delete, raise the limit, or exempt the Project: [BEST-PRACTICES.md](./BEST-PRACTICES.md).

## Share across Projects

Dataset roles are independent of Project roles: **Owner** (everything), **Editor** (upload,
snapshot, tag, update metadata), **Reader** (view and mount). Grant them on
the Dataset's permissions panel or with `POST /api/datasetrw/v1/datasets/{datasetId}/grants`
(`DatasetRwOwner`, `DatasetRwEditor`, `DatasetRwReader`). A user with a role mounts it in
another Project via **Data > Domino Datasets > Mount Shared Dataset** or
`POST /api/projects/v1/projects/{projectId}/shared-datasets`; it appears under the imported
paths. Reads without a mount (Apps, endpoints): `DatasetClient` in the domino-data-sdk skill.

## Delete

Owners mark for deletion; an admin purges. Dataset: UI **More Actions > Delete Dataset** or
`DELETE /api/datasetrw/v1/datasets/{datasetId}` (soft, cancellable, affects every Project
that mounts it; confirm first). Snapshot: UI, or
`DELETE /v4/datasetrw/snapshot/{snapshotId}` (non-public route; may change in a future Domino version); restore with `PUT` `{"status": "Active"}`. Details: [API.md](./API.md).

## Troubleshooting

| Symptom | Check |
|---|---|
| Path missing in the execution | `DOMINO_IS_GIT_BASED`; Dataset mounted in this Project; execution started after the mount |
| Permission denied writing | Dataset role (Reader is read-only); snapshot paths are always read-only; a pinned snapshot replaces the live mount |

## Reference files

- [MOUNT-PATHS.md](./MOUNT-PATHS.md): mount trees, detection, pinned snapshots
- [API.md](./API.md): routes, bodies, examples
- [BEST-PRACTICES.md](./BEST-PRACTICES.md): layout, formats, snapshot limits, large reads

Docs: https://docs.domino.ai/cloud/platform-capabilities/core-concepts/data/datasets,
https://docs.domino.ai/cloud/admin/data-administration/datasets,
https://docs.domino.ai/cloud/reference/cli/cli-reference (`/6.3/` for self-managed).
