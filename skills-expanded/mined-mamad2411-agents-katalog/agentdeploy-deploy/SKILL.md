---
name: agentdeploy-deploy
description: Create or update AgentDeploy SharedInfra and Service YAML files, validate them, deploy apps with the agentdeploy CLI and Platform API, poll status and explain output, and debug structured deployment failures. Use when a user wants to deploy, redeploy, or troubleshoot an app on an AgentDeploy installation.
license: Apache-2.0
metadata:
  author: elementx
  version: "0.17.4"
---

# AgentDeploy Deploy

Use this skill when the user wants an application deployed onto AgentDeploy, or when an existing AgentDeploy deployment needs to be updated or debugged.

## What this skill covers

- infer the right split between `SharedInfra` and `Service`
- choose the correct workload type and minimum infrastructure
- validate and dry-run before changing live state
- deploy with `agentdeploy` through the Platform API when available, then poll structured status
- debug policy, auth, infrastructure, and rollout failures

Read [references/service-contract.md](references/service-contract.md) when writing or editing `SharedInfra` or `Service`.
Read [references/operations.md](references/operations.md) when running the CLI or handling failures.

Use the templates in `assets/` as the starting point:

- `assets/shared-infra.yaml`
- `assets/service-web.yaml`
- `assets/service-api.yaml`
- `assets/service-worker.yaml`
- `assets/service-cron.yaml`

## Prerequisite: CLI availability

Before using this skill, make sure `agentdeploy` is installed and on `PATH`.

Current supported user install path:

```bash
command -v brew
# if brew is missing, stop and ask the user to install Homebrew themselves from:
# https://brew.sh/
# continue only after brew is available on PATH

command -v gh
# if gh is missing:
brew install gh

gh auth login
gh auth setup-git
gh auth status

brew tap elementx-ai/tap https://github.com/elementx-ai/homebrew-tap
brew install --HEAD elementx-ai/tap/agentdeploy
# or, if it is already installed:
brew upgrade --fetch-HEAD elementx-ai/tap/agentdeploy
```

This is the current private macOS install path. If `brew` is missing, direct the user to [brew.sh](https://brew.sh/) and wait for them to finish that install themselves before continuing. If `gh`, GitHub auth, or `agentdeploy` is still unavailable after that, stop and report the install blocker before attempting deploy commands.

Before debugging any feature mismatch between docs and the installed CLI, run:

```bash
agentdeploy version
```

The current CLI already carries the prototype Platform API URL and Entra scope by default. On the first API-backed command it will run its own Entra device-code login flow and cache the session token until it expires. You only need to set API flags or environment variables when overriding the installation defaults.

Treat `AGENTDEPLOY_CONFIG_REPO_REMOTE` as an explicit fallback only for intentional direct GitOps mode without the Platform API.

For the current ElementX prototype, the shared container registry is:

```text
acragdpelementxprototype.azurecr.io
```

Members of the managed deployers group `agentdeploy-elementx-prototype-deployers` should have Azure `AcrPush` on that registry. If the user wants to publish their own image instead of using a prebuilt digest or AgentDeploy `build:`, point them at that registry first. If a recent group membership change is not reflected yet, have them refresh their Azure login before debugging the push path further.

Recommended registry auth path for a human deployer:

```bash
az login --tenant edd2663e-acb4-4eb1-9cc3-51ce8979cc55
az account set --subscription ab282a21-8afb-4389-9fb0-4711a3a92450
az acr login --name acragdpelementxprototype
```

That ACR login flow is separate from `agentdeploy` CLI auth. The CLI no longer depends on Azure CLI, but Docker-to-ACR auth in this prototype still does. Only fall back to token-based `docker login` if `az acr login` is not viable in the user's environment.

## Workflow

1. Confirm the CLI is available, then inspect the app before writing contracts.
   - Run `command -v agentdeploy` before using the workflow.
   - Look for whether it serves HTTP, runs background work, or is purely scheduled.
   - Check whether it already expects `PORT`, `DATABASE_URL`, `REDIS_URL`, or migration commands.
   - Prefer reusing an existing immutable image digest. Use a `build:` block only when the user wants AgentDeploy to build from source.
   - If the user needs to push a custom image for the current prototype, prefer the shared registry `acragdpelementxprototype.azurecr.io`.

2. Choose the application shape.
   - If the app has exactly one service, no shared state, no `valueFrom.infrastructureRef`, and no `valueFrom.serviceRef`, a single `Service` is enough.
   - In that standalone shape, AgentDeploy can bootstrap `Namespace`, `ResourceQuota`, and `LimitRange` directly from the `Service` record.
   - If multiple services need to share a namespace, PostgreSQL, Redis, object storage, or service-to-service wiring, create a `SharedInfra` record first and then point each service at it through `metadata.application`.
   - Treat `SharedInfra` as the only place that owns built-in DB, Redis, or object-storage resources. Do not put `spec.infrastructure` on a `Service`; that model is gone.

3. Choose the workload shape for each service.
   - `web`: browser-facing app with HTTP ingress.
   - `api`: browser-consumed backend with HTTP ingress.
   - `worker`: no ingress, background process.
   - `cron`: scheduled job, no ingress.

4. Create or update the contracts.
   - Start from `assets/shared-infra.yaml` when the app needs shared DB/Redis or multiple services.
   - Start each service from the closest service template in `assets/`.
   - Keep the app name DNS-safe.
   - If the repo does not already declare deploy metadata, derive a unique app name and subdomain from the repo or directory name so the deployment does not collide with an existing app.
   - If `owner` is missing from repo context, prefer a real maintainer email from git config, docs, or project context. Only invent a synthetic owner for an explicit smoke test.
   - If `team` is missing from repo context, prefer an obvious team name from the repo, parent directory, or surrounding project docs. If none exists, choose a clearly temporary team name for a smoke test and call out the assumption.
   - Default to `dataClassification: internal` unless the user explicitly says the data is more sensitive.
   - Keep `metadata.application` explicit on services when more than one service shares the same app.
   - For a tiny standalone app, letting `metadata.application` default to `metadata.name` is fine.
   - Default to `visibility: internal` unless the user explicitly needs public reachability.
   - Default to `authorization.mode: group-based` unless the user explicitly wants `org-wide` and policy allows it.
   - Prefer dedicated Entra security groups for app access. Use broader team-wide groups only when the whole team should be able to use the app.
   - For smoke tests or lab installs without real group IDs, `org-wide` is acceptable only for `internal` apps and only when the installation policy allows it. Do not use it for sensitive data.
   - If the user explicitly wants a fully public app with no shared auth at all, warn them first that the app will be reachable anonymously on the public internet and will not receive any shared identity headers.
   - For that mode, use:
     - `spec.dataClassification: public`
     - `spec.access.auth: none`
     - `spec.access.authorization.mode: none`
   - In the current policy set, unauthenticated app access is allowed only for `dataClassification: public`. Call out that the app will not receive `X-Auth-Request-*` identity headers in that mode.
   - If the app needs PostgreSQL, declare it on `SharedInfra` under `spec.infrastructure.databases.<name>` and wire one of the DB env variants from `valueFrom.infrastructureRef`:
     - `DATABASE_URL` or `DATABASE_URL_SYNC` for libpq / sync clients
     - `DATABASE_URL_ASYNC` for common async Python stacks
   - If the app needs Redis, declare it on `SharedInfra` under `spec.infrastructure.redis.<name>` and wire `REDIS_URL` or `REDIS_URL_TLS` from `valueFrom.infrastructureRef`.
   - If the app needs shared upload or document handoff storage across services, declare it on `SharedInfra` under `spec.infrastructure.objects.<name>` and wire it from `valueFrom.infrastructureRef` with `kind: objectStorage`.
   - For split API/worker document flows, prefer object storage plus object keys over local-path handoff. Keep local disk only for scratch via `runtime.filesystem.writablePaths`.
   - If one service needs to call another service in the same application, wire that URL with `valueFrom.serviceRef` instead of hardcoding domains or patching manifests.
   - In the current prototype, Redis is only supported for `dataClassification: internal`.
   - Make sure the process actually listens on `runtime.port`. If the app expects a `PORT` env var, set it explicitly.
   - `runtime.command` and `runtime.args` are supported. Use them when the workload needs an explicit startup command instead of baking a wrapper image only for process launch.
   - If the app needs writable ephemeral directories, use `runtime.filesystem.writablePaths` instead of asking users to patch manifests by hand.
   - Only set `runtime.filesystem.readOnlyRootFilesystem: false` when the app genuinely cannot work with explicit writable mounts. Treat that as a security tradeoff and call it out.

5. Validate before deploying.
   - Prefer the API-owned path when the installation provides it. The current CLI already defaults to the prototype API URL and Entra scope, so only set flags or environment variables when you need to override those defaults.
   - Validate `SharedInfra` first when present, then validate each dependent `Service`.
   - Run `agentdeploy validate --file <contract>.yaml`.
   - If you intentionally want offline local-engine validation instead of the hosted API path, pass `--api-url=`.
   - Inspect `effective_service` or `effective_infra`, plus `manifest_files` and `warnings`, in the response. They are the fastest way to catch dropped or mismatched fields before a deploy.
   - For a standalone service-only app, `manifest_files` should include `namespace.yaml`, `resourcequota.yaml`, and `limitrange.yaml`. If those files are absent, the app is no longer on the standalone bootstrap path.
   - Treat `QUOTA_*` errors as pre-flight failures against the current rendered namespace limits, not as generic rollout failures.
   - Treat capacity-related warnings as best-effort scheduler signals. They do not block deploy by themselves, but they mean the cluster may be too full to place the new pods.
   - Fix errors by following the exact `field`, `allowed_values`, and `suggested_value` in the JSON response.
   - Then run `agentdeploy deploy --file <contract>.yaml --dry-run`.
   - In the current prototype, `deploy --dry-run` can still return `status: accepted` and an `operation_id`. Treat it as preview-only. Review `preview_only`, `effective_service` or `effective_infra`, `manifest_files`, and `warnings` rather than assuming a live deployment started.

6. Deploy for real.
   - Deploy `SharedInfra` first when present, then deploy each dependent `Service`.
   - Run `agentdeploy deploy --file <contract>.yaml`.
   - Capture `operation_id`, the reported record name, and the initial phase.
   - Do not assume `git_commit` or revision are returned immediately. Live deploys are queued and executed asynchronously.
   - If local CLI mode returns `DEPLOY_NO_LIVE_TARGET`, stop. Use the Platform API path or configure a real GitOps remote. Only use `AGENTDEPLOY_ALLOW_LOCAL_GITOPS=true` when the user explicitly wants local-only GitOps testing.
   - If the deploy returns `DEPLOY_MISSING_SHARED_INFRA`, the app is not a true standalone service. Either deploy `SharedInfra` first or remove the extra shared-state / service-ref coupling.
   - If the deploy is rejected with `DEPLOY_OPERATION_ALREADY_IN_PROGRESS`, check whether the active operation is still desirable. If it is stuck or obsolete, run `agentdeploy cancel <record>` and then submit the replacement deploy.
   - Poll with `agentdeploy status <record>` until the phase is `live` or an error is returned.

7. Verify the result.
   - Start with the aggregate application view for multi-service apps:
     - `agentdeploy applications`
     - `agentdeploy app-status <team> <application>`
     - `agentdeploy app-explain <team> <application>`
   - Use the aggregate view to confirm `SharedInfra` plus all dependent services are converging together before drilling into a single record.
   - Use the URLs returned by `status` or `explain` for services. Do not hardcode domains because each installation can differ.
   - For a complete state dump, run `agentdeploy explain <record>`.
   - For runtime debugging without `kubectl`, use:
     - `agentdeploy describe <record>` for pod names, restart counts, waiting or termination reasons, image digests, requests, limits, and service or endpoint visibility
     - `agentdeploy events <record>` for missing secrets, quota failures, probe failures, and scheduling errors
     - `agentdeploy logs <record> [--follow] [--previous] [--pod <name>] [--container <name>] [--tail N]` for live or previous container logs
   - In `explain`, inspect the live `infrastructureRef` and `serviceRef` sections when secret wiring or same-namespace traffic looks wrong.
   - Compare `requested_revision` against `observed_revision`. If they differ, the control plane has accepted a newer revision than ArgoCD has actually reconciled in the cluster.
   - Treat a stale-reconciliation warning as a real GitOps signal. The platform now requests a targeted Argo refresh automatically, and you can also run `agentdeploy refresh <app>` if the warning persists.
   - If the app depends on PostgreSQL, confirm `SharedInfra` is healthy, the service injects the DB variant it actually uses, and the app-level readiness check matches the app’s real dependencies.
   - If the app depends on Redis, confirm `SharedInfra` is healthy, the service injects `REDIS_URL` or `REDIS_URL_TLS`, and the app-level readiness check actually exercises Redis.
   - If the app depends on shared object storage, confirm `SharedInfra` is healthy and the service injects the object-store keys it actually uses. Prefer `OBJECT_STORE_*` for portable app wiring and fall back to `AZURE_STORAGE_*` only when the runtime still needs provider-specific compatibility.
   - Remember that `list`, `status`, and `explain` are usually filtered by team-scoped control-plane RBAC, not by app owner alone.

## Default decisions

- Prefer immutable image digests over tags.
- Prefer the smallest viable CPU and memory values; only raise them when the app clearly needs more.
- Prefer PostgreSQL only when the app actually needs persistent relational storage.
- Prefer Redis only when the app actually needs cache or ephemeral key-value state.
- Prefer one service per app unless there is a clear need for a multi-service application with shared namespace and shared infra.
- Prefer the standalone `Service` bootstrap only for a true one-service app. The moment the app needs shared state or a sibling service, switch to explicit `SharedInfra`.
- Prefer internal ingress and group-based authorization for enterprise apps.

## High-value gotchas

- Mutable image tags are rejected. Use `repo@sha256:...` or let AgentDeploy build the image.
- `allowedGroups` must contain stable group IDs, not human-readable names.
- Only `internal` data classification can be `public`.
- `confidential` and `restricted` cannot use `org-wide`.
- `api` means browser-consumed HTTP API in this platform, not general service-to-service auth.
- Public apps use shared auth by default, but an app can explicitly opt out with `spec.dataClassification: public`, `spec.access.auth: none`, and `spec.access.authorization.mode: none`.
- For `group-based` access, `allowedGroups` should be the stable Entra object IDs of the groups that should be able to pass the shared auth proxy.
- If more than one user set should be allowed, list all of their group object IDs in `allowedGroups` and keep the scope intentional. Prefer app-specific access groups over broad org-wide groups.
- The app receives identity through `X-Auth-Request-*` headers, not raw Entra bearer tokens, by default.
- The concrete headers are `X-Auth-Request-Email`, `X-Auth-Request-Groups`, `X-Auth-Request-Preferred-Username`, and `X-Auth-Request-User`.
- Shared ingress auth no longer forwards bearer `Authorization` headers into apps by default. If an app expects raw OAuth access tokens, call that out as a platform mismatch instead of assuming they will be present.
- `auth: none` means no shared ingress auth and no injected identity headers. In the current policy set, that is allowed only for `dataClassification: public`.
- If PostgreSQL is declared, it must live on `SharedInfra`, not `Service`. Wire the correct DB env variant with `valueFrom.infrastructureRef`. `DATABASE_URL` / `DATABASE_URL_SYNC` are libpq-style, while `DATABASE_URL_ASYNC` is meant for common async Python stacks.
- If Redis is declared, it must live on `SharedInfra`, not `Service`. Wire `REDIS_URL` or `REDIS_URL_TLS` with `valueFrom.infrastructureRef`. The platform now includes `ssl_cert_reqs=required`, so most `redis-py` and Celery clients should not need app-side query rewriting.
- If one service needs another service's base URL, use `valueFrom.serviceRef`. That resolves to a stable in-namespace URL like `http://expense-api/api` and avoids hardcoding installation domains.
- A single standalone `Service` can bootstrap its own namespace policy, but that only works when there are no `infrastructureRef` or `serviceRef` bindings and no other services in the same application.
- `DEPLOY_MISSING_SHARED_INFRA` means the app has outgrown the standalone path and now needs an explicit `SharedInfra` owner.
- In the current prototype, Redis is an `internal`-only infrastructure option and is exposed over TLS on port `6380`.
- `runtime.filesystem.writablePaths` creates `emptyDir` mounts at those paths. Existing image contents at those paths will be hidden at runtime.
- `runtime.filesystem.readOnlyRootFilesystem` defaults to `true`. Turning it off is a real security relaxation and should be deliberate.
- If the app does not listen on `runtime.port`, the deployment will roll out but ingress health and readiness will still fail.
- `validate`, `deploy --dry-run`, and `explain` expose the effective normalized contract. Use that output to verify that infrastructure ownership, env wiring, and runtime overrides survived normalization.
- In the intended product mode, deployers should use the Platform API path. They should not need direct Git push access or direct Kubernetes read access for normal lifecycle commands.
- Team visibility is usually team-scoped, not owner-scoped. A caller typically sees all apps for teams they can view.
- A second real deploy for the same app may be rejected while another non-terminal operation is queued or running.
- `agentdeploy cancel <app>` is the current escape hatch for a stuck or obsolete live operation. It cancels the active operation record so a replacement deploy can be accepted.
- `requested_revision` is the last revision the control plane accepted. `observed_revision` is the revision ArgoCD currently reports from the cluster. Treat them as different signals.
- `describe`, `events`, and `logs` depend on a recent hosted `platform-api` build when you are using `AGENTDEPLOY_API_URL`. If they return `HTTP_NOT_FOUND`, the CLI is newer than the live control plane.

## Debug loop

1. Read `agentdeploy status <record>` first.
2. If the phase is not obviously actionable, read `agentdeploy explain <record>`.
3. For rollout or runtime failures, read `agentdeploy describe <record>`.
4. If the cause still is not obvious, read `agentdeploy events <record>`.
5. Use `agentdeploy logs <record> --previous` for crash loops and `agentdeploy logs <record> --follow` for live request or worker debugging.
6. Use the error code prefix to choose the next action:
   - `SCHEMA_*`: fix the contract.
   - `POLICY_*`: change the requested shape or access mode.
   - `AUTH_*`: fix group IDs or auth assumptions.
   - `INFRA_*`: inspect database or Redis claim and secret readiness.
   - `DEPLOY_*`: inspect the workload rollout and health checks.
   - `QUOTA_*`: lower requests or ask for a higher app tier.

## Feedback loop

- If a real deployment exposes a high-value platform bug, contract gap, or reliability issue, raise that feedback rather than treating it as one-off local friction.
- If you have access to `elementx-ai/agentdeploy`, open or update a GitHub issue with:
  - the affected app, record type, and workload type
  - the relevant `SharedInfra` or `Service` shape
  - operation ID, requested revision, and observed revision when available
  - the exact failure mode, impact, and the smallest useful fix
- Prefer issues for meaningful fixes or improvements. Do not create noise for already-documented prototype limitations unless the observed behavior is worse than documented.

## Output expectations

When doing deployment work with this skill:

- keep the contracts small and explicit
- explain which workload type, application shape, and data classification you chose
- surface the exact CLI commands you ran
- quote the operation ID first, then the revision or Git commit once `status` or `explain` reports it
- prefer actionable remediation over generic advice
