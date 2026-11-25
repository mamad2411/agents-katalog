---
name: netapp-volumes
description: Work with Domino Volumes for NetApp ONTAP (NetApp Volumes) - shared, multi-terabyte storage with near-instant snapshots. Covers creating volumes, attaching them to projects, mount paths (/mnt/netapp-volumes/ or /domino/netapp-volumes/), snapshots and tags, roles, deletion, mounting volumes in jobs, and the NetApp Volumes REST API (/remotefs/v1). Use when managing large-scale shared data, taking fast no-copy snapshots, or integrating NetApp ONTAP storage with Domino.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. An administrator must have registered a NetApp ONTAP filesystem.
---

# Domino NetApp Volumes

Applies to Domino 6.3 and Domino Cloud.

Domino Volumes for NetApp ONTAP mount NetApp ONTAP filesystems directly into Domino
Workspaces, Jobs, Apps and Launchers. They are global entities (not scoped to a project)
that you attach to any project that needs them. Product docs:
https://docs.domino.ai/cloud/platform-capabilities/core-concepts/data/netapp-volumes.
Auth: [domino-api-intro](../domino-api-intro/SKILL.md#authentication); in a run the
`/remotefs/v1` routes answer only on `DOMINO_REMOTE_FILE_SYSTEM_HOSTPORT` with a bearer
([API-NETAPP-VOLUMES.md](./API-NETAPP-VOLUMES.md#authentication-and-base-urls)).

## NetApp Volumes or Domino Datasets?

NetApp Volumes cover nearly the same ground as Datasets and are recommended wherever the
organization runs ONTAP. Differences:

- Snapshots are near-instant regardless of size (about 3 seconds) and use
  redirect-on-write, so they consume no extra storage at creation; a Dataset snapshot
  duplicates the data.
- Datasets can be cloned from a snapshot into a new Dataset; a NetApp Volume snapshot
  cannot be cloned into a new volume (volumes can be copied for Project Templates).
- NetApp Volumes need ONTAP infrastructure and an administrator-registered filesystem;
  Domino sets no volume size limit (the ONTAP volume type does). There are limits on
  snapshots per volume (`maxSnapshots` on the volume record) and volumes per filesystem.

Comparison and examples: [DATA-ACCESS.md](./DATA-ACCESS.md).

## Prerequisites

An administrator registers an ONTAP filesystem (data plane, storage class, root PVC) before
anyone can create volumes: https://docs.domino.ai/cloud/admin/data-administration/netapp-volumes.
List registered filesystems with `GET /remotefs/v1/filesystems`
([API-NETAPP-VOLUMES.md](./API-NETAPP-VOLUMES.md#filesystems)).

## Create a volume

From Domino (then add it to projects manually) or from inside a project (auto-attached):

1. **Data > NetApp Volumes** (toolbar, or a project's left panel).
2. **Add NetApp Volume > Create Volume**.
3. **Name** (letters, numbers, underscores, hyphens), **Description**, **Data Plane**,
   **NetApp Filesystem**, **Capacity**. Click **Next**.
4. Add users or organizations with a **Reader**, **Editor** or **Owner** role. **Finish**.

REST: `POST /remotefs/v1/volumes` with `name`, `filesystemId`, `capacity` (bytes) and
`grants` ([API-NETAPP-VOLUMES.md](./API-NETAPP-VOLUMES.md#create-a-volume)).

## Attach, detach, delete

- **Attach**: **Data > NetApp Volumes**, three-dot menu on the volume, **Add to project**.
  REST: `POST /remotefs/v1/rpc/attach-volume-to-project`.
- **Detach**: in the project, **Data > NetApp Volumes**, **Remove from project**. Only the
  attachment goes; data and other projects are unaffected. REST:
  `POST /remotefs/v1/rpc/detach-volume-from-project`.
- **Delete**: **Delete Volume** (if your admin enabled it for your role) or **Mark for
  deletion** (requests that an admin delete it). Deletion is permanent. REST:
  `POST /remotefs/v1/rpc/delete-volume` (no need to mark first) or
  `/rpc/mark-volume-for-deletion` (undo: `/rpc/restore-volume`).

## Mount paths

Paths mirror the Dataset scheme; volumes are global, so there is no local/imported split.

| Project type | Read-write volume | Snapshot by number | Tagged snapshot |
|--------------|-------------------|--------------------|-----------------|
| DFS | `/domino/netapp-volumes/<name>` | `/domino/netapp-volumes/snapshots/<name>/<number>` | `/domino/netapp-volumes/snapshot-tags/<name>/<tag>` |
| Git-based | `/mnt/netapp-volumes/<name>` | `/mnt/netapp-volumes/snapshots/<name>/<number>` | `/mnt/netapp-volumes/snapshot-tags/<name>/<tag>` |

`<number>` is the snapshot's `version` from the API. Owners and Editors mount read-write;
Readers mount read-only; Apps mount with the App owner's permission. If a snapshot has several tags, only the most
recently added tag is mounted. Renaming a volume changes its mount path. At launch you can
pin a volume to one snapshot (**Data Plane & Hardware** tab); it then mounts read-only at
the read-write path and `snapshots/<name>` is disabled. Details:
[DATA-ACCESS.md](./DATA-ACCESS.md).

## Snapshots and tags

Owners and Editors take snapshots: open the volume, **Files** tab, **Take Snapshot**
(all files or selected files), optionally add a commit message and one or more tags.
Tag names: letters, numbers, underscores and hyphens only (no dots), unique within the
volume. The button is unavailable once the volume
reaches its maximum snapshot count. Deleting a snapshot is permanent and needs delete
permission on the volume. Docs:
https://docs.domino.ai/cloud/platform-capabilities/core-concepts/data/datasets/version-data-with-snapshots.

REST: `POST /remotefs/v1/snapshots` (`volumeId`, `description` as the commit message,
`tagNames`), `POST /remotefs/v1/snapshots/{id}/tags`, `PUT /remotefs/v1/snapshots/{id}`,
`/rpc/restore-snapshot`, `/rpc/delete-snapshot`
([API-NETAPP-VOLUMES.md](./API-NETAPP-VOLUMES.md#snapshots)). `/rpc/create-snapshot-from-run`
is super-user only (403 otherwise); to snapshot at the end of a job use
`snapshotNetAppVolumesOnCompletion` where enabled, or `POST /remotefs/v1/snapshots` from
the job.

## Roles

| Role | API value | Capabilities |
|------|-----------|---------------------|
| Reader | `VolumeReader` | Read data and view snapshots; attach to projects read-only; can only mark a snapshot for deletion |
| Editor | `VolumeEditor` | Reader plus write data, edit the description, take and delete snapshots, mount, mark for deletion or restore |
| Owner | `VolumeOwner` | Editor plus change who has access and their roles (grants), request volume deletion |

Edit permissions: three-dot menu on the volume, **Edit permissions**, or **Share** on the
details page. REST: `PUT /remotefs/v1/volumes/{id}/grants`.

## Volumes in Jobs

`POST /api/jobs/v1/jobs` takes `netAppVolumeIds` (volume ids to mount) and
`snapshotNetAppVolumesOnCompletion: true` to snapshot every mounted volume when the job
ends; the latter needs a deployment feature flag and is rejected with 400 where it is
off. Body: [API-NETAPP-VOLUMES.md](./API-NETAPP-VOLUMES.md#mount-volumes-in-a-job).

## Reference files

- [API-NETAPP-VOLUMES.md](./API-NETAPP-VOLUMES.md): REST API with request bodies (volumes, filesystems, attach/detach, snapshots, tags, grants, deletion, listing, files, jobs)
- [DATA-ACCESS.md](./DATA-ACCESS.md): comparison with Datasets, mount paths, snapshot mounting, read/write examples, best practices
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md): missing mounts, permission errors, tag paths, no filesystems, slow reads

## Documentation

- https://docs.domino.ai/cloud/platform-capabilities/core-concepts/data/netapp-volumes (overview, create, add/remove, view/edit)
- https://docs.domino.ai/cloud/reference/api/domino-volumes-api (API served at `/remotefs/v1`)
- https://docs.domino.ai/cloud/admin/data-administration/netapp-volumes (administrator setup)
- Specs: [API-SPECS.md](../domino-api-intro/API-SPECS.md); per-deployment service document `/docs/openapi/data_remotefs_service-swagger.json`
