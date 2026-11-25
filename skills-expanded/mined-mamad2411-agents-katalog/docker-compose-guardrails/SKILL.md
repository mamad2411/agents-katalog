---
name: docker-compose-guardrails
description: Create, modify, review, or deploy Docker Compose services with enforceable per-container limits, host-level minimum-resource protection, bounded builds, and production-ready startup behavior. Use when working with Dockerfiles, compose.yaml/docker-compose.yml files, container deployment configuration, host cgroups/systemd slices, or incidents involving container CPU, memory, OOM, process, restart, or build pressure.
---

# Docker Compose Guardrails

Treat an omitted resource limit as a deployment defect for every long-running service. Do not approve or deploy it until a documented exception exists.

## Resolve deployment policy

Before reviewing, changing, or deploying container resources, run:

```sh
uv run python <docker-compose-guardrails-skill-directory>/scripts/resolve.py \
  --cwd <project-root> \
  --task deploy
```

Read the returned instruction path once per new `instructions_id`. Without
project configuration, the resolver returns the generic deployment policy.
Projects may define topology, resource classes, budgets, and validation
commands under `.agents/skills-config/docker-compose-guardrails/`; see
[references/project_config.md](references/project_config.md).

## Set boundaries

For each long-running service, set all of the following on the service itself:

- `cpus`: finite CPU quota.
- `mem_limit`: finite memory quota.
- `pids_limit`: finite process limit.
- `restart`: use `unless-stopped` or `always` when appropriate; justify `no` or omission.

Prefer the service-level fields above because they map directly to the local Docker Compose runtime. Do not rely only on `deploy.resources`; support differs by deployment target. If `deploy.resources.limits` is used for an orchestrator, retain service-level limits for local Compose or document why the target guarantees enforcement.

Choose conservative initial limits from the service's known workload. Do not invent precision: if the workload is unknown, state that the values are provisional and name the metric or load test that will guide adjustment.

Allow an unbounded value only for a short-lived, manually invoked task with an explicit reason and owner. Never silently leave a long-running service unlimited.

Compose limits provide ceilings, not guaranteed minimums. When a deployment
must preserve minimum resources for selected containers, enforce the resolved
host-level cgroup policy in addition to these service limits. Do not claim that
`mem_limit`, `deploy.resources.reservations`, or CPU quota alone provides a
minimum guarantee.

## Build before runtime

Treat a build command in a long-running service's `command` or `entrypoint` as
a deployment defect. Build application artifacts in the Dockerfile, normally
with a multi-stage build, and make the Compose service start only the built
runtime artifact. This keeps build-resource demand separate from runtime
limits, makes the image reproducible, and prevents every restart from building
again.

The bundled static check rejects common startup build commands, including
`next build`, `pnpm build`, `npm run build`, and `yarn build`. Move the build
to the image build stage before deployment. A short-lived, manually invoked
build task is the only exception; do not give it a restart policy and document
its purpose and owner.

Treat builds as best-effort work. Bound the builder daemon and its executor
containers at the host cgroup layer; constraining only the `docker build` or
Compose client process is insufficient. A project may use a remote builder
instead. Stop or reject a build when its resolved admission or pressure gate
fails, and return a stable error that identifies the failed resource check.

## Review before deployment

Run the bundled static check:

```sh
python3 scripts/check_compose_guardrails.py -f compose.yaml
```

Resolve every error. Treat warnings as review items, especially services that use only `deploy.resources.limits`.

Render the exact Compose model used for deployment before reviewing it:

```sh
docker compose -f compose.yaml config
```

Run every preflight command declared by the resolved deployment policy before
changing live containers. Resolution only declares commands; it never executes
them.

## Verify the running container

After `docker compose up -d`, verify Docker's effective HostConfig rather than trusting YAML:

```sh
docker inspect <container> --format 'Memory={{.HostConfig.Memory}} NanoCPUs={{.HostConfig.NanoCpus}} PidsLimit={{.HostConfig.PidsLimit}} Restart={{.HostConfig.RestartPolicy.Name}}'
```

For constrained services, `Memory` and `NanoCPUs` must be non-zero; `PidsLimit` must not be `0` or absent. `0` means unlimited. Report the observed values in the deployment handoff.

For deployments with minimum-resource protection, also verify the effective
leaf cgroup and every relevant ancestor after containers start. Confirm the
resolved resource class, `memory.min`, `memory.low`, `memory.max`, CPU control,
and builder containment from the host. Recreated containers receive new
cgroups, so protection that is applied only once by hand is not durable.

## Review output

State, per service, its resource class and configured CPU, memory, PID, and
restart values; whether Docker and host-cgroup runtime verification passed; and
any compatibility note. Report the admission budget and builder boundary when
minimum-resource protection is enabled. List all exceptions explicitly with
their reason, owner, and expected duration.
