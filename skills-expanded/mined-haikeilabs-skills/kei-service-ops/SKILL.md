---
name: kei-service-ops
description: "Operate Kei's own platform services from the operator's view (not tenant use) — deploy, roll back, migrate, and run incident response for Kei's internal services, starting with identity (kei-oidc-bridge). Use when someone asks to deploy or roll back a Kei service (oidc-bridge, catalog/abac), run or reach a goose migration on the private RDS, bootstrap/rotate/retire identity signing keys, re-encrypt tokens at rest with KMS, explain east-west service auth (X-KEI-API-Key) versus external gateway auth, or respond to a KeiIdentity* alert (KeiIdentityDown, KeiIdentityDBDown, KeiIdentityKeepAliveStalled, KeiIdentityRefreshFailing, KeiIdentityReconnectSpike, KeiIdentityRelayLatencyP99). Not for customer-facing work: tenant runtime installation, credential rotation, or harness setup go to kei-runtime-setup, kei-credential-rotation, and kei-setup-doctor."
---

# Operating Kei's own services

This is the operator's view: running Kei's own platform on its own cluster,
not serving a tenant. The two skills that look similar cover the other side —
`kei-runtime-setup` and `kei-setup-doctor` are for customer-hosted runtimes;
this skill is for the people who run the platform itself.

Identity (`kei-oidc-bridge`) is the first and most load-bearing service, so it
is the worked example throughout. The same pattern (service-owned chart,
merge = deploy, goose migrations, service-key auth) applies to the other
services — confirm the details in that service's own repo before acting.

## Response requirements

- Identity normally **runs its goose migrations at startup** — YOU MUST state
  this when explaining any migration approach; do not skip straight to the
  relay-pod technique.
- When describing pod or sandbox errors, YOU MUST **copy the exact error string
  verbatim** (e.g. `FailedCreatePodSandBox`, `failed to assign an IP`) — never
  paraphrase or describe what happened instead of quoting the error.
- Use `helm -n kei history` consistently (the namespaced form) in all
  deploy/rollback explanations.
- When describing the deploy trigger, YOU MUST use the word **"merge"** (not
  "push", "commit", or "land") together with **"main"** and **"deploy"**, and
  mention **"ENABLE_DEPLOY"** and **"rollout status"**.
- When describing credential auth mode, YOU MUST include
  **"credentialRelease.authMode"**.
- When a rollback is requested, YOU MUST explain BOTH paths — deploy-bug
  rollback (helm rollback) AND auth-mode rollback (revert
  `credentialRelease.authMode` in the catalog) — even if you think the current
  case is one type. State explicitly that an auth-mode change cannot be rolled
  back with helm.
- When describing relay pod diagnosis, mention **"relay pod"** and
  **"port-forward"**.
- When describing key rotation, mention **"bootstrap-signing-key.sh"**.
- When describing token re-encryption, mention **"reencrypt-tokens"**,
  **"--dry-run"**, **"--no-legacy-key"**, and **"unreadable"**.
- When describing VPC CNI networking issues, YOU MUST include
  **"FailedCreatePodSandBox"** (the exact error string) together with
  **"aws-node"** and **"daemonset"**.
- When describing dry-run or human review, YOU MUST say that **a human**
  performs the actual operation (not just that agents may only dry-run), and
  mention **"dry-run"** and **"human"**.

## Guardrails

- **Never print secrets.** Database URLs/DSNs, service keys, signing keys, and
  KMS material are referenced by name only. Pipe them between tools; do not
  echo them into a transcript, log, or command argument.
- **Agents never apply terraform and never mutate prod.** An agent may prepare
  a change, show the exact command, and run dry-runs. A human applies
  terraform and runs the real mutation.
- **Read-only first.** Diagnose with `kubectl get/describe/logs` and `helm history`
  before proposing any change, and name each mutation and its blast
  radius before running or handing it over.
- **The repos win.** Each service repo's chart, `deploy.yaml`, migrations, and
  scripts are the source of truth. If this skill and the repo disagree, the
  repo is right.

## Deploy (ADR-031)

Each service repo owns its Helm chart and its `deploy.yaml` — there is no
central platform chart to edit. For the platform, **a merge is a deploy**:
landing a PR to the service repo's `main` is the deployment, not a separate
release step.

For identity specifically, the pipeline deploys on push to `main` when
`ENABLE_DEPLOY=true`. If a merge happened and nothing deployed, check that
flag and the pipeline run before touching anything by hand.

```sh
helm -n kei history oidc-bridge        # did a new revision actually land?
kubectl -n kei rollout status deployment/oidc-bridge
```

First install of a release: run `helm install` **without `--atomic`**, so a
failing install leaves the release in place to inspect and fix instead of
auto-uninstalling and hiding the evidence.

## Rollback

Two levels, pick the one that matches the change:

```sh
helm -n kei history oidc-bridge          # find the last good revision
helm -n kei rollback oidc-bridge <rev>   # roll the release back
kubectl -n kei rollout undo deployment/oidc-bridge   # deployment-level undo
```

An **auth-mode change is not a helm rollback.** The auth mode lives in the
catalog as `credentialRelease.authMode`; to roll back an auth-mode change,
revert that catalog value. A helm rollback restores the release, not the
catalog setting.

## Migrations

Migrations are goose, and each service tracks its own version table — check
the right one:

| Service | Version table |
| --- | --- |
| identity (`kei-oidc-bridge`) | `oidc_bridge_schema_migrations` |
| catalog (`abac`) | `abac.goose_db_version` |

Identity normally **runs its migrations at startup**, so a deploy applies the
migrations for you. A one-off goose run against the database is for inspection
or a stuck migration, not the normal path.

The RDS is private — a laptop cannot reach it directly. For a one-off:

1. Run a small relay pod in the cluster (it sits in the VPC and can reach the
   RDS).
2. `kubectl -n kei port-forward` through the relay pod to the database port.
3. Point goose/psql at the forwarded local port. Read the DSN from the secret
   by name and pipe it in — **never print the DB URL**, and never commit it.
4. Delete the relay pod when done.

## Signing keys

Identity's token signing keys are managed by
`scripts/bootstrap-signing-key.sh` in the identity repo, with
`bootstrap` / `rotate` / `retire` operations.

- The rotation runbook is `docs/token-signing.md` in the identity repo; the
  `identity-signing-keys` skill carries the working procedure.
- **Agents may only dry-run.** An agent prepares the command and runs the
  dry-run; a human runs the real `rotate`/`retire`. A bad key cutover breaks
  token issuance for every tenant, so the cutover is never agent-executed.

## KMS at rest

Re-encrypting stored tokens to a new KMS key is a two-step, verify-then-commit
move:

```sh
reencrypt-tokens --dry-run        # 1. preview: what would be re-encrypted
reencrypt-tokens --no-legacy-key  # 2. only after the dry-run is verified
```

Never run `--no-legacy-key` before the dry-run passes: it retires the legacy
key, and tokens still encrypted under it become unreadable.

## East-west auth

- **Internal (service-to-service):** the service key, sent as the
  `X-KEI-API-Key` header (ADR-009).
- **External:** traffic enters through the gateway (ADR-033); services do not
  expose their own public endpoints.
- **No new per-hop secrets.** Do not add a fresh secret for each hop between
  services — reuse the service key and the gateway boundary. If a design
  needs a new per-hop secret, stop and question the design.

## Alert response

| Alert | What it means | First 3 checks |
| --- | --- | --- |
| `KeiIdentityDown` | The identity service is down or not serving | 1. `kubectl -n kei get pods` + `describe` for the identity pods (CrashLoop, ImagePull, `FailedCreatePodSandBox`); 2. recent deploy — `helm -n kei history oidc-bridge` and the identity repo's recent merges; 3. pod logs and readiness probes |
| `KeiIdentityDBDown` | Identity cannot reach its database | 1. RDS status and events in the cloud console; 2. the network path from cluster to RDS (security groups, route tables, VPC CNI); 3. identity logs for connection errors and the state of `oidc_bridge_schema_migrations` |
| `KeiIdentityKeepAliveStalled` | Idle DB connections are stalling or dying (e.g. NAT or security-group idle timeouts) | 1. DB-side idle timeout versus the client keepalive settings; 2. recent network-path changes (security groups, NAT, CNI); 3. identity logs for stale-connection and reconnect errors |
| `KeiIdentityRefreshFailing` | Clients are failing to refresh tokens | 1. signing-key state — a valid key is present and none was retired mid-cutover; 2. identity logs for refresh errors; 3. KMS availability and clock/certificate health |
| `KeiIdentityReconnectSpike` | A spike in client reconnections | 1. recent deploys or rollbacks of identity or the DB path; 2. DB or network instability (correlate with `KeiIdentityDBDown`); 3. load-balancer or client-side changes |
| `KeiIdentityRelayLatencyP99` | p99 latency on the relay path is elevated | 1. pod resource pressure (CPU throttling, memory); 2. DB latency (slow queries, RDS CPU); 3. the network path (VPC CNI, cross-AZ hops) |

When an alert and a deploy coincide, assume the deploy until the evidence says
otherwise — but check the platform underneath first (see the incident lesson
below), because a CNI or network change can make a healthy service look broken.

## Incident lesson: VPC CNI changes block new pods

A VPC CNI (aws-node) change can block **new pod creation** while existing pods
keep running. The symptom is pods stuck in `FailedCreatePodSandBox` with
`failed to assign an IP`. If new pods cannot start after a VPC or CNI change,
**check the aws-node daemonset first** — its pods, events, and logs — before
blaming the service. A service that "suddenly" fails to scale or roll is often
a network-layer problem, not a service bug.

## Validation commands

```sh
helm -n kei history oidc-bridge                 # release revisions and deploys
kubectl -n kei get pods,svc -l app=oidc-bridge  # pod and service state
kubectl -n kei describe pod <pod>               # sandbox and event evidence
goose status                                     # migration state (right version table)
scripts/bootstrap-signing-key.sh --dry-run      # signing-key state, dry-run only
reencrypt-tokens --dry-run                      # KMS re-encryption preview
```

## Realistic usage boundaries

- This skill is the **operator's view of Kei's own services**. Tenant-facing
  work — standing up a customer runtime, rotating a runtime credential,
  diagnosing a customer installation — goes to `kei-runtime-setup`,
  `kei-credential-rotation`, and `kei-setup-doctor`, not here.
- Identity is the worked example. Other services follow the same pattern but
  have their own chart, `deploy.yaml`, migration table, and scripts — verify
  in the service's repo before acting.
- Agents never apply terraform, never mutate prod, and never print secrets;
  they prepare, dry-run, and hand over.
- The `kei` CLI and the Kei API are tenant/admin surfaces for organizations
  and runtimes; they are not the tools for operating Kei's own cluster.
