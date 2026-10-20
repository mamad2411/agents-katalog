---
name: sub2api-fork-deploy
description: "Build and safely deploy an exact commit from a Sub2API GitHub fork to an existing Docker Compose server, then converge back to an official tagged image when the release catches up. Use when official Sub2API images lag a fork or main branch, when a custom linux/amd64 or linux/arm64 image must be built and transferred, when an official release now contains the deployed fork commit, when updating only the Sub2API application while preserving PostgreSQL, Redis, data, configuration, backups, health evidence, and a tested rollback path, or when publishing the deployment through a Cloudflare Tunnel and debugging public 502 Bad Gateway errors from a containerized cloudflared."
---

# Sub2API Fork Deploy

Use this runbook for an existing Sub2API Docker Compose deployment. Treat source build and production deployment as separate trust boundaries.

## Operating Contract

- Lock the source to a full commit SHA before building. Never deploy a moving branch name directly.
- Treat official catch-up as image convergence, not rollback. Prove the official release commit relationship before switching images.
- Discover the live Compose working directory, config file, service names, mounts, and database identity. Do not assume an upstream filename such as `docker-compose.local.yml` exists on the server.
- Preserve the production Compose file, `.env`, volumes, and data layout. Change only the application image unless the user explicitly approves more.
- Back up PostgreSQL and deployment configuration before replacing the application container.
- Restart only the Sub2API application with `--no-deps --pull never`. Do not restart or recreate PostgreSQL or Redis for an application-image update.
- Never persist SSH passwords, API keys, `.env` contents, database passwords, or registry credentials in this skill, prompts, source control, logs, or final answers. Prefer SSH keys. For password-only access, pass the password through an approved environment/session mechanism such as `sshpass -e`, never `sshpass -p`.
- Keep image builds off small production hosts. A one-core, roughly 2 GiB host without swap should receive a prebuilt image rather than compiling Node and Go locally.
- Keep backups and rollback image tags until the user explicitly approves cleanup.

If the user explicitly requests `$codex-luna`, load that skill too. Freeze the exact build plan and let Luna operate only in an isolated source checkout. Keep SSH credentials, backups, Compose changes, deployment, rollback, and final verification in the coordinator session. Forbid recursive delegation.

## Required Inputs

Obtain or discover:

- Fork clone URL, such as `https://github.com/<owner>/sub2api.git`.
- Source ref and the exact full commit SHA selected from it.
- SSH target and authentication method.
- Live application container name, normally `sub2api`.
- Live Compose project directory and config path.
- PostgreSQL container, database user, and database name.
- Target platform from the production host (`amd64` or `arm64`).
- Image delivery route: registry push or direct `docker save` transfer.
- For official convergence: exact release tag, tag commit SHA, registry manifest digest, and current deployed custom commit SHA.

Do not ask for values that can be read safely from Git, Docker labels, Compose config, or the remote host.

## 1. Inspect Before Mutation

Keep the first pass read-only. Record the current container/image state and dependency start times:

```bash
docker inspect <app-container> --format \
  'image={{.Config.Image}} image_id={{.Image}} started={{.State.StartedAt}} status={{.State.Status}} health={{if .State.Health}}{{.State.Health.Status}}{{end}}'

docker inspect <app-container> --format \
  'working_dir={{index .Config.Labels "com.docker.compose.project.working_dir"}} config_files={{index .Config.Labels "com.docker.compose.project.config_files"}} project={{index .Config.Labels "com.docker.compose.project"}} service={{index .Config.Labels "com.docker.compose.service"}}'

docker inspect <postgres-container> <redis-container> --format \
  '{{.Name}} id={{.Id}} started={{.State.StartedAt}} status={{.State.Status}}'

uname -m
nproc
free -h
df -h / /var/lib/docker
docker compose version
```

Inspect the resolved Compose model without printing `.env`:

```bash
cd <compose-working-dir>
docker compose -f <compose-file> config --services
docker compose -f <compose-file> config --images
```

Confirm the application, PostgreSQL, and Redis volumes before continuing. Never replace the live file with an upstream example Compose file.

## 2. Lock and Inspect the Fork

Use an isolated checkout so unrelated worktrees remain untouched:

```bash
git clone --filter=blob:none --no-checkout <fork-url> <isolated-dir>
git -C <isolated-dir> checkout --detach <full-commit-sha>
git -C <isolated-dir> rev-parse HEAD
git -C <isolated-dir> remote get-url origin
git -C <isolated-dir> status -sb
```

Inspect `Dockerfile`, `backend/cmd/server/VERSION`, `backend/scripts/resolve-version.sh`, and `deploy/docker-entrypoint.sh`. Confirm that the root Dockerfile accepts `VERSION`, `COMMIT`, and `DATE` build arguments.

Derive an unambiguous version, for example:

```text
<base-version>-main.<short-sha>
```

Set the full commit explicitly. Without build arguments, a main-branch image may still report the last release version and become operationally indistinguishable from the official image.

## 3. Build the Exact Image

Map `x86_64` to `amd64` and `aarch64` to `arm64`. Build for the production architecture even when the local Docker host uses another architecture:

```bash
docker buildx build \
  --platform linux/<target-arch> \
  --load \
  --build-arg VERSION=<base-version>-main.<short-sha> \
  --build-arg COMMIT=<full-commit-sha> \
  --build-arg DATE=<commit-or-build-utc-timestamp> \
  -t <owner>/sub2api:main-<short-sha> \
  .
```

Do not modify source merely to make the frozen build pass. Investigate and report the real failure.

Verify the built artifact independently:

```bash
docker image inspect <image> --format \
  'id={{.Id}} os={{.Os}} arch={{.Architecture}} size={{.Size}} created={{.Created}}'

docker run --rm \
  --platform linux/<target-arch> \
  --network none \
  --entrypoint /app/sub2api \
  <image> --version 2>&1 | grep -m1 'Sub2API '
```

The isolated probe may exit after the version line because databases are unavailable. Do not run `/app/sub2api --version` inside the live `sub2api` container: this binary may start a second server process and fail with an address-in-use error.

Before production access, confirm the checkout has no tracked changes and the reported version contains the expected short SHA while the commit field contains the full SHA.

## 4. Create a Recoverable Backup

Resolve `<db-user>` and `<db-name>` from the live deployment without exposing passwords. Create a mode-`700` backup directory under the deployment path:

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP=<compose-working-dir>/backups/pre-main-<short-sha>-$STAMP
install -d -m 700 "$BACKUP"

cp -a <compose-working-dir>/.env "$BACKUP/.env"
cp -a <compose-file> "$BACKUP/docker-compose.yml"
docker inspect <app-container> >"$BACKUP/sub2api-container-inspect.json"
docker image inspect <current-image> >"$BACKUP/sub2api-image-inspect.json"

docker exec <postgres-container> \
  pg_dump -U <db-user> -d <db-name> --format=custom \
  >"$BACKUP/sub2api.pgdump"

docker exec -i <postgres-container> \
  pg_restore --list \
  <"$BACKUP/sub2api.pgdump" \
  >"$BACKUP/sub2api.pgdump.list"

test -s "$BACKUP/sub2api.pgdump"
test -s "$BACKUP/sub2api.pgdump.list"
sha256sum "$BACKUP/sub2api.pgdump" >"$BACKUP/SHA256SUMS"
sha256sum -c "$BACKUP/SHA256SUMS"
```

Pin the current application image under a rollback tag before a future `pull` can move a floating tag:

```bash
docker tag <current-image-id-or-tag> <rollback-image-tag>
docker image inspect <rollback-image-tag> --format '{{.Id}}'
```

Stop if the dump, `pg_restore --list`, checksum, configuration copy, or rollback tag fails.

## 5. Deliver the Image

Prefer a commit-pinned GHCR or Docker Hub tag for repeatable operations. When no registry credentials are available, transfer the image directly:

```bash
docker save <image> | gzip -1 | ssh <ssh-target> 'gzip -d | docker load'
```

After transfer, verify the image on the remote host with `docker image inspect` and the isolated version probe. Image IDs can differ across Docker storage backends after transfer; trust the remote architecture plus embedded version and full commit proof, not a local/remote ID equality assumption.

A directly loaded image is local-only. Server reboot is safe because the image remains in Docker storage, but `docker compose pull` will fail until that exact tag is published to a registry. State this clearly in the handoff.

## 6. Return to an Official Image

Treat official catch-up as image convergence, not rollback. Do not switch merely because `latest` changed.

Do not invoke Luna or rebuild an image for same-commit convergence. Verify and deploy the existing official artifact instead.

Resolve the official release tag, its exact commit SHA, and the registry manifest digest from official GitHub and registry metadata. Compare that commit with the currently deployed custom commit in a checkout containing both commits:

```bash
DEPLOYED_SHA=<full-custom-commit-sha>
OFFICIAL_SHA=<full-release-tag-commit-sha>

if [ "$DEPLOYED_SHA" = "$OFFICIAL_SHA" ]; then
  echo "same source commit: packaging convergence"
elif git merge-base --is-ancestor "$DEPLOYED_SHA" "$OFFICIAL_SHA"; then
  echo "official release contains deployed commit: normal forward upgrade"
else
  echo "official release is behind or diverged; stop" >&2
  exit 1
fi
```

Interpret the result strictly:

- Same commit: the application source is already equivalent. Switch only to restore official version metadata, registry availability, and maintainable future pulls.
- Official descendant: inspect every intervening commit and migration, then follow the full backup and upgrade workflow.
- Official ancestor or diverged history: stop. Switching would discard fork changes or move to unrelated code.

Use `latest` for discovery only. Production Compose must use an exact official version tag such as `weishaw/sub2api:<version>`; record its manifest digest, and use a tag-plus-digest reference when immutable pinning is required.

Pull and verify only the official application image before editing Compose:

```bash
OFFICIAL_IMAGE=weishaw/sub2api:<version>
docker pull "$OFFICIAL_IMAGE"
docker image inspect "$OFFICIAL_IMAGE" --format \
  'id={{.Id}} os={{.Os}} arch={{.Architecture}} created={{.Created}} repo_digests={{json .RepoDigests}}'

docker run --rm \
  --platform linux/<target-arch> \
  --network none \
  --entrypoint /app/sub2api \
  "$OFFICIAL_IMAGE" --version 2>&1 | grep -m1 'Sub2API '
```

Require the reported official version and commit to match the selected release. Pin the currently deployed custom image under a rollback tag before changing Compose. Reuse the backup workflow; do not skip the PostgreSQL backup merely because the source commit is equal.

Patch only `services.<app-service>.image` to the exact official tag, validate the one-line diff, and run the normal app-only command with `--no-deps --pull never`. The explicit `docker pull` above fetches the approved app image; `--pull never` prevents Compose from pulling or replacing dependencies during the restart.

After convergence, verify the official image tag, version, health, real traffic, migrations, and unchanged dependency IDs/start times. Keep the custom image until the official image passes the agreed soak period. The handoff must state that future app-only pulls work again because the configured image is registry-backed.

## 7. Patch Only the Application Image

Start from a copy of the live Compose file. Change only `services.<app-service>.image`; do not replace the file with a fork or upstream Compose example.

Upload the candidate as `<compose-file>.new`, then validate it from the live working directory so the real `.env` is resolved:

```bash
cd <compose-working-dir>
docker compose -f <compose-file>.new config -q

docker compose -f <compose-file>.new config --format json \
  | jq -er --arg image '<new-image>' \
    '.services["<app-service>"].image == $image'
```

Do not validate with `config --images | head -1`; image order is not service order and may return PostgreSQL first.

Compare old and candidate files. The expected diff is exactly one application image line. After validation, install the candidate atomically and recreate only the app:

```bash
install -m 0644 <compose-file>.new <compose-file>
rm <compose-file>.new

docker compose -f <compose-file> up -d \
  --no-deps \
  --pull never \
  <app-service>
```

Do not run an unscoped `docker compose up -d`; updated PostgreSQL or Redis images can cause dependency containers to be recreated unnecessarily.

## 8. Verify Production

Wait for application health with a bounded loop, then verify:

```bash
docker compose -f <compose-file> ps
docker inspect <app-container> --format \
  'image={{.Config.Image}} image_id={{.Image}} started={{.State.StartedAt}} status={{.State.Status}} health={{.State.Health.Status}} restarts={{.RestartCount}}'

curl -fsS --max-time 8 http://127.0.0.1:<port>/health
curl -sS -o /dev/null -w '%{http_code}\n' --max-time 8 http://127.0.0.1:<port>/

docker logs --since <new-app-start-time> <app-container> 2>&1 \
  | grep -Ei 'panic|fatal|migration.*(fail|error)|\tERROR\t' \
  | head -40 || true
```

Also prove:

- The running image tag is the exact fork commit tag.
- Restart count is `0` after stabilization.
- PostgreSQL and Redis container IDs and start times match the preflight evidence.
- The database migration expected from the selected commit exists and has the expected type or shape.
- The backup checksum still passes.
- The public health endpoint returns success.
- At least one representative authenticated API request succeeds when safe credentials and a non-destructive request are available. Otherwise, use observed post-deploy production `200` responses without exposing request bodies or keys.

If startup logs omit the version banner, verify the deployed image with an isolated `docker run --network none` probe. Do not start a second process inside the live container.

## 9. Roll Back

If health, migrations, or representative traffic fail:

1. Restore the backed-up Compose file or patch only the application image back to `<rollback-image-tag>`.
2. Validate the candidate with `docker compose config -q`.
3. Run `docker compose up -d --no-deps --pull never <app-service>`.
4. Re-run health, logs, and representative request checks.

Do not restore PostgreSQL automatically. First determine whether the new migration is additive and backward compatible. A database restore is a separate destructive recovery requiring an explicit maintenance window, stopped writes, and user approval.

## 10. Expose via Cloudflare Tunnel

When publishing the deployment through a token-based Cloudflare Tunnel, run cloudflared as its own container, detached and restart-safe:

```bash
docker run -d --name cloudflared --network host --restart unless-stopped \
  cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <tunnel-token>
```

Treat the tunnel token as a credential: never persist it in this skill, source control, or logs beyond the run command the operator supplies.

Two independent misconfigurations each produce an identical public `502 Bad Gateway`; distinguish them from `docker logs cloudflared`, not from the browser:

- `dial tcp 127.0.0.1:<port>: connect: connection refused` — network-namespace mismatch. On the default bridge network, `127.0.0.1` inside the cloudflared container is the container itself, never the host, so a dashboard route pointing at `127.0.0.1:<port>` cannot work. Fix with `--network host` (route URL stays `127.0.0.1:<port>`), or attach cloudflared to the Compose network and set the route URL to `http://<app-service>:<port>`.
- `tls: first record does not look like a TLS handshake` — protocol mismatch. Sub2API serves plain HTTP on its port; a route with Service Type `HTTPS` makes cloudflared attempt TLS against it. Set the route Service Type to `HTTP`. Browser-to-Cloudflare traffic remains HTTPS regardless; the type only governs the cloudflared-to-origin hop.

Prove the origin protocol from the host before configuring or blaming the route:

```bash
curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1:<port>/
curl -sk -o /dev/null -w '%{http_code}' -m 5 https://127.0.0.1:<port>/
```

A token-run tunnel is remotely managed: hostname, path, Service Type, and URL are editable only in the Zero Trust dashboard. Nothing on the server can change ingress, so a protocol or hostname fix requires the operator to edit the published application route there.

Success evidence, in order: the startup precheck table reports all `PASS`; the logs contain four `Registered tunnel connection` lines; a public `curl -s -o /dev/null -w '%{http_code}' https://<hostname>/` returns the application's expected status. Dashboard edits propagate within seconds; re-test rather than restarting cloudflared.

For multi-user traffic, clear the QUIC warning `failed to sufficiently increase receive buffer size` by raising UDP buffer limits, persisting them, and restarting cloudflared:

```bash
sysctl -w net.core.rmem_max=7500000 net.core.wmem_max=7500000
printf 'net.core.rmem_max=7500000\nnet.core.wmem_max=7500000\n' \
  >/etc/sysctl.d/99-quic-buffer.conf
docker restart cloudflared
```

Confirm the warning is absent from post-restart logs and the four connections re-register.

## Stop Conditions

Stop before production mutation when any of these is true:

- The fork, ref, or exact commit is ambiguous.
- The isolated checkout has unrelated tracked changes.
- The built image platform or embedded commit does not match production intent.
- The official release commit is neither equal to nor a descendant of the deployed custom commit.
- The live Compose directory/config cannot be proven from container labels or operator evidence.
- The candidate Compose diff changes anything beyond the approved application image.
- The PostgreSQL backup or restore-list validation fails.
- The rollback image tag cannot be resolved.

After deployment, roll back or escalate when health never becomes stable, restart count increases, critical logs appear, migrations fail, or real API traffic regresses.

## Handoff

Report:

- Fork URL, exact full SHA, displayed version, image tag, platform, and remote image ID.
- Which container restarted and which dependency containers did not.
- Health, restart count, public endpoint, migration, logs, and representative traffic evidence.
- Backup directory, dump size, and checksum result without secret contents.
- Rollback image tag and exact app-only rollback command shape.
- Whether the image is registry-published or local-only, including the `docker compose pull` consequence.
- For official convergence: release tag, release commit, manifest digest, commit relationship, and retained custom rollback tag.
- For tunnel exposure: cloudflared network mode, route Service Type and origin URL shape, registered connection count, sysctl buffer state, and the public hostname status code — without the tunnel token.
- Confirmation that unrelated local worktree changes were preserved.
