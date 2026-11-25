---
name: stateful-container-upgrades
description: "Use when upgrading stateful container apps safely."
version: 1.0.0
---

# Stateful Container Upgrades

Upgrade Podman/Docker Compose applications without losing databases, uploads, or private configuration. Applicable to source-tracked deployments whose runtime uses prebuilt images.

## Core invariant

An upgrade is complete only when all four are proven:

1. durable data was backed up and the backup passed integrity checks;
2. deployed source/image matches the intended upstream revision;
3. the application restarted on the same persistent volumes;
4. post-upgrade data and service checks match the pre-upgrade baseline.

Never equate `git pull`, a successful image pull, or a successful restart command with a completed upgrade.

## 1. Discover deployment state

Before changing anything, inspect:

- repository branch, dirty/untracked files, upstream, HEAD, and ahead/behind count;
- service manager unit and exact Compose invocation;
- running containers, image references, health, and persistent mounts;
- local override files and private env files that must remain untouched;
- existing backup command, retention, and timer;
- current HTTP response and a small, meaningful data baseline.

Treat untracked deployment overrides as intentional until proven otherwise. Do not clean, reset, stash, or overwrite them merely to update tracked source.

Confirm disruptive restart authorization unless the current request explicitly directs an upgrade whose normal execution necessarily includes restarting that same stack.

## 2. Establish a preservation baseline

Capture before-state in machine-comparable form:

- stable row counts for critical business tables;
- database migration count/version;
- persistent-storage file count and approximate byte size;
- volume names and mount destinations;
- current application revision and HTTP status.

Choose stable domain tables. Exclude ephemeral queues, sessions, caches, logs, and counters that can legitimately change during the upgrade.

## 3. Back up before pulling the trigger

Back up every durable plane, usually:

- transactional database: consistent logical dump (`--single-transaction` where supported);
- uploaded/private application storage: volume export or filesystem archive;
- optional deployment configuration, only through a secret-safe mechanism.

Use restrictive permissions. Write to a temporary directory, generate checksums, then atomically move completed artifacts into the backup directory.

Verify more than existence:

- backup service exit status;
- checksum recomputation;
- decompression/archive readability;
- nonzero sizes.

Do not expose env-file contents or credentials in logs.

## 4. Update source safely

Fetch first, inspect the delta, then use a fast-forward-only update when local history is not meant to diverge:

```bash
git fetch --prune origin
git rev-list --left-right --count HEAD...origin/main
git log --oneline HEAD..origin/main
git merge --ff-only origin/main
```

Preserve local untracked overrides. After updating, verify `HEAD` equals the intended upstream commit.

## 5. Resolve source revision to runtime image

A source checkout and a container image are separate artifacts. Updating one does not update the other.

For registries that publish a mutable tag such as `latest`:

1. pull the tag;
2. inspect OCI labels, especially `org.opencontainers.image.revision`;
3. require that revision to equal the selected Git commit;
4. capture the registry digest;
5. replace the deployment's mutable or old image reference with the immutable digest.

```bash
podman pull registry.example/app:latest
podman image inspect registry.example/app:latest \
  --format 'Digest={{.Digest}} Revision={{index .Labels "org.opencontainers.image.revision"}}'
```

Large pulls can take many minutes without new output. Run them as a bounded background process and wait for their real exit result rather than restarting duplicate pulls.

A multi-architecture index digest and a selected platform image digest can differ. Verify the configured image name/index digest plus the OCI revision label; do not flag that normal distinction as corruption.

## 6. Redeploy without deleting data

Edit only the image reference needed for the upgrade. Keep volume declarations, env files, port bindings, restart policies, and private overrides unchanged.

Use the deployment's established service manager. Avoid destructive Compose options such as volume removal. A normal `down`/`up` retains named volumes unless `--volumes`/`-v` is supplied.

Wait for the restart command to exit, then inspect state independently.

## 7. Verify the live result

Require all relevant checks:

- service manager reports success;
- database container is healthy;
- application container uses the intended immutable image;
- OCI revision matches the updated Git HEAD;
- volume names and destinations are unchanged;
- application startup logs show migrations/config/bootstrap completed;
- every supervised process or health component is running;
- local HTTP endpoint returns the expected status;
- external HTTPS endpoint returns the expected status with valid TLS;
- stable business-table counts match the saved baseline programmatically;
- migration changes are understood rather than blindly required to match;
- backup timer remains active.

Storage byte counts can shift slightly during bootstrap because symlinks, caches, or metadata are recreated. Same named volume + same meaningful file count + matching database baseline is stronger evidence than exact byte equality.

When local DNS resolution is unhealthy but the endpoint's IP and hostname are known, `curl --resolve host:port:ip https://host:port/` tests routing, SNI, and certificate validation without disabling TLS verification. Record the DNS warning separately; do not mistake it for application failure.

## Rollback readiness

Before restart, know the previous image digest and backup paths. If verification fails:

1. stop further writes if data integrity is uncertain;
2. restore the previous image digest first when schema remains compatible;
3. restore database/storage only when necessary and from a verified backup;
4. re-run the same baseline and endpoint checks.

Never claim rollback capability from an untested or unchecked archive.

## Supporting material

- See `references/podman-compose-finance-app.md` for a validated Podman Compose example with MySQL, named volumes, systemd user units, OCI revision matching, and external TLS verification.
