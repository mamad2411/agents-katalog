---
name: container-security
description: Audit Docker, Compose, Kubernetes or container deployment configuration. Use when a task touches Dockerfiles, Compose, images, networks, ports, secrets, CI deployment or production infrastructure.
---

# Container security

Containers are an isolation boundary, not a security policy. Inspect the deployment files and running topology before changing them.

## 1. Establish the boundary

Identify the public entrypoints, internal services, persistent volumes, image sources, secret sources and the user each process runs as. If these facts are missing, report them as unverified.

## 2. Check the deployment

- Images are pinned by immutable digest for production. Tags are acceptable only in local development.
- Processes run as a non-root user. Drop Linux capabilities, use `no-new-privileges`, a read-only root filesystem and temporary writable mounts when the image supports them.
- Databases, caches and queues have no host port unless a specific external consumer requires one.
- Separate public and internal networks. Privileged internal APIs validate both service credentials and source network or mTLS.
- Secrets come from server-side environment or a secret manager, never the image, repository, build arguments, logs or client code. Rotate a secret exposed in a chat, issue or commit.
- Persistent data has an explicit backup and restore procedure. Development volumes are never mistaken for production backups.
- Services have health checks, restart policy, CPU and memory limits appropriate to the host, structured logs and a defined upgrade/rollback procedure.
- Outbound integrations have an allowlisted destination, timeout, retry/backoff policy and no unnecessary personal data.

## 3. Safe verification

Prefer read-only evidence: `docker compose config`, `docker compose ps`, `docker inspect`, image digests, network inspection and application health endpoints. Do not run image scans, pull images, create external webhooks or load-test a production deployment without explicit authorization.

## 4. Report format

Read `../production-readiness/report-format.md` and use its P0/P1/P2 structure. Cite each finding with `file:line`, command output or an explicit unverified status.
