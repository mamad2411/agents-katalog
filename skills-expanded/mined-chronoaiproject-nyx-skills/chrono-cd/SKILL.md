---
name: chrono-cd
description: Deploy a user's application to the ChronoAI cluster with chrono-cd through NyxID, either with the CLI (`nyxid proxy request chrono-cd ...`) or, for agents without a shell such as the NyxID Assistant and NyxBot on Telegram or Lark, with their NyxID proxy request tool (service `chrono-cd`, method, path, body). Covers the whole flow an agent runs for the user - check the account and quota, pick a personal or organization scope, write the app spec (one or more ghcr.io images with ports, routes, env, config files, volumes and an optional MongoDB add-on), create or update the app, set its secrets, watch status and logs, query stored metrics and logs for any window up to 31 days (presets or PromQL and LogsQL), restart, roll back by re-deploying a tag, delete, and ask for more quota. Use whenever the user wants to deploy, update, inspect or remove an app on the ChronoAI platform (hostnames under apps.nyxid.ai, older apps under apps.chrono-ai.fun), or asks what chrono-cd needs from them. Every request body and response shape is given, so the agent never guesses.
compatibility: Needs one of two transports. A shell with the nyxid CLI, logged in with `nyxid login`; or a NyxID proxy request tool that takes a service slug, a method, a path and a body (the NyxID Assistant, NyxBot on Telegram or Lark, Aevatar agents). The NyxID service `chrono-cd` is added to every account automatically. Private GitHub packages need a classic GitHub token with read:packages, sent once as registry_credential. Verified 2026-10-27 against chrono-cd on the live platform.
version: "2.11"
license: Apache-2.0
metadata:
  category: tool-based
  tool-list:
    - Bash
    - nyxid_proxy
  tag:
    - chrono-cd
    - nyxid
    - deploy
    - kubernetes
    - ghcr
    - apps
---

# Deploy an app with chrono-cd

chrono-cd runs container images from GitHub Packages (`ghcr.io`) on the ChronoAI cluster
and gives each app a public hostname `https://APP-SLUG.apps.nyxid.ai`, where SLUG is
a hash for a person and the organization's NyxID slug for an organization. Apps created
before 2026-10-27 keep their `apps.chrono-ai.fun` hostname; always give the user the
`url` from the app view rather than building it yourself. It is
registered in NyxID as the service `chrono-cd`. Every call goes through NyxID, which
checks the user's login and tells chrono-cd who is calling. There is no other credential
to manage. Responses are plain JSON objects, errors are
`{"error": "KEY", "error_code": N, "message": "..."}`.

"You" below means the agent. "The user" is the person you act for.

## Two ways to call, same API

Look at what you have. Use exactly one of these transports for the whole conversation.

**With a shell** (Claude Code, Codex, a CI job): the NyxID CLI.

```bash
nyxid proxy request chrono-cd api/v1/PATH [--method PUT|PATCH|POST|DELETE] [--data 'JSON'] --output json
```

**Without a shell** (the NyxID Assistant, NyxBot on Telegram or Lark, an Aevatar agent):
your NyxID proxy request tool. You give it a service slug, an HTTP method, a path and an
optional JSON body; NyxID routes the call and adds the identity. For every call in this
skill:

- Service: `chrono-cd`
- Method: `GET`, `PUT`, `PATCH`, `POST` or `DELETE`, as the step says
- Path: the `api/v1/...` path of the step, with a leading slash: `/api/v1/account`.
  Query parameters stay in the path: `/api/v1/projects/P/apps/A/logs?service=web&tail=200`
- Body: the JSON object of the step, only for `PUT`, `PATCH` and `POST`

The base URL is the service root, so the path always starts with `/api/v1/`. A `404
route` with the right path usually means the `/api/v1` prefix was dropped. Never
compose an HTTP request yourself: that runtime has no HTTP tool and no token.

If you have neither the CLI nor a proxy request tool that accepts `chrono-cd`, say so
plainly: the service has to be exposed to this agent in NyxID. Do not pretend a call
was made.

Every step below shows the CLI line; the proxy tool call is the same method, path and
body.

## The model, in four words

| Level | What it is | Example |
|---|---|---|
| owner | the user, or one of their organizations; one namespace and one quota | `acme` |
| project | a plain group of apps; exists while it has an app | `chronoai` |
| app | one deployable application: one hostname, services, add-ons | `chrono-pod` |
| service | one container inside the app | `api`, `worker` |

App names and service names are unique per owner, across projects. Services of the same
owner reach each other by name, `http://SERVICE:PORT`, in any project.

## Rules that matter

- **Never ask the user for a NyxID token.** `nyxid login` is the only credential step
  for the CLI; an agent with a proxy tool has nothing to log in to.
- **Images must be on `ghcr.io`** and run as a non-root user. An image that must start as
  root, or as a named user such as distroless `nonroot`, fails with
  `CreateContainerConfigError` in status; tell the user to rebuild it with a numeric
  `USER 65532:65532`.
- **Private packages** need a pull credential, sent once in the `PUT` body as
  `"registry_credential": {"username": "<github login>", "token": "<token>"}`. The token
  is a GitHub personal access token (classic) with the `read:packages` scope; fine-grained
  tokens and GitHub App tokens do not work with ghcr.io. chrono-cd stores it only as a
  Kubernetes pull Secret and reuses it on later deploys, so it is sent once. Ask the user
  to put it in a file or an environment variable rather than typing it into the chat.
  Public packages need nothing.
- **Secrets never go in the spec, in chat or in logs.** Declare the names in
  `secret_keys`, then set the values with the secrets endpoint. Responses only ever show
  names.
- **`PUT` is declarative, `PATCH` is partial.** A `PUT` body replaces the whole spec;
  anything you leave out is gone. To change one thing, such as the image tag, `PATCH`
  with only that field: `{"services":{"web":{"image":"...:TAG"}}}`. `PATCH` is pinned to
  the generation it read, so it never overwrites a deploy that landed in between. When
  you must `PUT` an app you did not write, read it first and send `If-Match: <generation>`.
- **A `port` is immutable** and so is a service name. To change a port, add the service
  under a new name and remove the old one.
- **Replicas are at most 3; a service with a `pvc` volume runs 1.**
- **Quota is per owner**: default 2 CPU, 4Gi, 10 pods, 20Gi for a person and 8 CPU, 16Gi,
  40 pods, 80Gi for an organization, summed over all apps as replicas times requests plus
  one surge pod. `409 quota_exceeded` says by how much. The
  user can only request more; a platform admin approves.
- **Apps per owner are capped**: 20 for a person, 50 for an organization, shown as
  `quota.apps` (the cap) and `usage.apps` (the count) on `/account`. Every app counts,
  also one with no replicas. Only creating an app checks it: updating or deleting never
  fails on it. `409 quota_exceeded` "apps: N of CAP in use" means delete an app the user
  no longer needs, or ask for a higher cap.
- **MongoDB add-ons are limited platform-wide**: the platform holds a limited number in
  total, for all users together. When it is full, adding one (a new app with it, or an
  app gaining it) answers `409 conflict`. That is not the user's quota and a quota
  request cannot fix it: tell the user to contact the platform team. Apps that already
  have the add-on keep working and can be updated.
- **Organization scope:** the user must be an `admin` of the organization to deploy;
  `member` and `viewer` can only read. Pass `org_id` on every call for that scope.
- **Permissions:** every call here needs `can_deploy` on `/account` (the NyxID role
  `chrono-cd-user`, which every user has by default). People with `can_internal` can
  also deploy the platform's own internal apps; that is the `chrono-cd-internal` skill.

## Step 0: check the account

```bash
nyxid proxy request chrono-cd api/v1/account --output json
```

Proxy tool: `chrono-cd`, `GET`, `/api/v1/account` (add `?org_id=ID` for an organization).

Returns `can_deploy`, `slug`, `host_slug` (the hostname suffix), `quota`, `usage`, `apps` and
`organizations` with the user's role in each. If `can_deploy` is false, stop: the user
lacks the NyxID role `chrono-cd-user` and every other call answers `403`; a platform
admin can grant it. If the user wants to deploy for an organization, pick its `id` and add
`?org_id=ID` to every path below. If they are not `admin` there, stop and say so.

## Step 1: write the spec

Ask the user only for what has no default: the image, the port, and whether the service
is public. Everything else defaults. The smallest public app:

```json
{"services": {"web": {"image": "ghcr.io/OWNER/PACKAGE:TAG", "port": 8080, "routes": ["/"]}}}
```

Per service:

| Field | Required | Default or rule |
|---|---|---|
| `image` | yes | `ghcr.io/owner/package:tag` or `@sha256:...`; resolved to a digest at every apply |
| `port` | unless `expose: none` | 1-65535, immutable |
| `routes` | for a public service | path prefixes on the app hostname, e.g. `["/"]` or `["/api", "/auth"]`; longest prefix wins; unique across the app |
| `expose` | no | `public` when routes are given, `internal` otherwise, `none` for a worker with no port |
| `health_path` | no | `/`; probes and the load balancer use it |
| `replicas` | no | 1, max 3 |
| `resources` | no | `{"cpu_request": "100m", "memory_request": "128Mi", "cpu_limit": "500m", "memory_limit": "512Mi"}` |
| `env` | no | plain variables, `{"KEY": "value"}`, 60 keys of 4 KiB |
| `secret_keys` | no | names of secret variables, set later; the service waits until all exist |
| `addon_env` | no | `{"mongodb": {"uri": "MONGODB_URI", "database": "MONGODB_DATABASE"}}` |
| `files` | no | plain config files `[{"path": "/etc/app/config.yaml", "content": "..."}]`, 16 of 64 KiB |
| `volumes` | no | up to 4: `{"name": "data", "mount_path": "/data", "type": "pvc", "size": "5Gi"}` or `"type": "emptydir"`; a `pvc` mount is group-writable (`fsGroup` 1000), so a non-root image can write to it |
| `egress`, `ingress_from` | no | `"none"` blocks all egress; `["api"]` lets only those sibling services in |
| `ingress_from_namespaces` | no | `["monitoring"]` lets pods of those namespaces reach this service's port; siblings unaffected |
| `metrics` | no | `{"port": 9090, "path": "/metrics"}` if the image serves Prometheus metrics; they then show up in the telemetry routes and `schema` |

Per app, outside `services`: `addons` (`{"mongodb": {}}` gives the app one database and a
scoped user; wire it with `addon_env`), `registry_credential` (see the rules), and
`target_org_id` (same as `org_id`).

A multi-service app, with a frontend, an API behind `/api`, and a worker:

```json
{
  "addons": {"mongodb": {}},
  "services": {
    "web":    {"image": "ghcr.io/acme/shop-web:1.4", "port": 8080, "routes": ["/"]},
    "api":    {"image": "ghcr.io/acme/shop-api:1.4", "port": 8080, "routes": ["/api"],
               "health_path": "/readyz",
               "metrics": {"port": 9090, "path": "/metrics"},
               "env": {"LOG_LEVEL": "info"},
               "secret_keys": ["JWT_KEY"],
               "addon_env": {"mongodb": {"uri": "MONGODB_URI", "database": "MONGODB_DATABASE"}}},
    "worker": {"image": "ghcr.io/acme/shop-api:1.4", "port": 8080, "expose": "none",
               "env": {"ROLE": "worker"},
               "addon_env": {"mongodb": {"uri": "MONGODB_URI"}},
               "volumes": [{"name": "cache", "mount_path": "/var/cache", "type": "pvc", "size": "5Gi"}]}
  }
}
```

With the CLI, write the spec to a file and send it with `--data "$(cat spec.json)"`.
With the proxy tool, the spec object is the body.

## Step 2: create or update the app

```bash
nyxid proxy request chrono-cd api/v1/projects/PROJECT/apps/APP --method PUT \
  --data "$(cat spec.json)" --output json
```

Proxy tool: `chrono-cd`, `PUT`, `/api/v1/projects/PROJECT/apps/APP`, body: the spec.

`PROJECT` and `APP` are 1-40 lowercase letters, digits and inner hyphens; the user picks
them. `201` on create, `200` on update. The response is the app view: `hostname`, `url`,
the normalized `spec` with `image_digest` per service, `generation`, `revision`, `status`.

Expected non-200 answers and what to do:

| Answer | Do |
|---|---|
| `422 missing_secret_keys` | Normal when the spec declares secrets. The app is stored and everything else is deployed. Go to step 3. |
| `400 image_unauthorized` | Private package without a usable credential. Ask for a classic token with `read:packages` and send `registry_credential`. |
| `400 image_not_found` | Wrong owner, package or tag. Check with the user. |
| `409 quota_exceeded` | Lower replicas or requests, or go to "Ask for more quota". For "apps: N of CAP in use", delete an unused app or ask for a higher `apps`. |
| `409 conflict`, MongoDB add-ons at the platform-wide capacity limit | Not the user's quota; do not ask for quota. Deploy without `addons`, or tell the user to contact the platform team. Nothing was created. |
| `409 service_name_taken` | Another app of this owner uses that service name. Rename the service. |
| `409 app_exists` | The app lives in another project. Use that project path. |
| `502 reconcile_failed` | Stored but not applied. Read `GET .../status`, fix the cause, send the same `PUT` again. |

## Step 3: set the secrets

Ask the user for each value named in `secret_keys`, in a way that keeps it out of the
transcript when possible (a file, an environment variable). Then, per service:

```bash
nyxid proxy request chrono-cd api/v1/projects/PROJECT/apps/APP/services/SERVICE/secrets \
  --method PUT --data '{"JWT_KEY": "..."}' --output json
```

Proxy tool: `chrono-cd`, `PUT`, `/api/v1/projects/PROJECT/apps/APP/services/SERVICE/secrets`,
body `{"JWT_KEY": "..."}`.

Returns `{"service": "api", "keys": ["JWT_KEY"]}`. Setting secrets applies the app again
and starts the waiting service. Secret files work the same way at
`.../services/SERVICE/secret-files` with `{"files": [{"path": "/etc/app/key.pem", "content": "..."}]}`.
Delete one key with `DELETE .../secrets/KEY`.

## Step 4: wait for it

```bash
nyxid proxy request chrono-cd api/v1/projects/PROJECT/apps/APP/status --output json
```

Proxy tool: `chrono-cd`, `GET`, `/api/v1/projects/PROJECT/apps/APP/status`.

`phase` is `ready`, `progressing`, `degraded`, `error` or `deleting`. Poll every 15
seconds for up to 8 minutes. `ready` means the public edge answers for the hostname:
the pods can be up while `route.serving` is still `false`, because the load balancer
needs a few minutes after a new hostname's route is accepted. Do not tell the user the
app is live before `phase` is `ready`. `services.NAME.pods[].reason` carries the container's own
words when something is wrong: `ImagePullBackOff` (image or credential),
`CrashLoopBackOff` (read the logs), `OOMKilled` (raise `memory_limit`),
`CreateContainerConfigError` (image runs as root). When `phase` is `ready`, give the user
the `url` from the app view.

Logs:

```bash
nyxid proxy request chrono-cd api/v1/projects/PROJECT/apps/APP/logs?service=SERVICE\&tail=200 --output json
```

Proxy tool: `chrono-cd`, `GET`, `/api/v1/projects/PROJECT/apps/APP/logs?service=SERVICE&tail=200`.

## Everyday operations

Method and path are the same for the CLI and the proxy tool; `...` stands for
`api/v1/projects/PROJECT/apps/APP`.

| Want | Call |
|---|---|
| everything deployed, personal and every organization, in one call | `GET api/v1/apps` (add `?scope=personal` or `?scope=organization` for one kind) |
| list projects | `GET api/v1/projects` |
| list apps of a project | `GET api/v1/projects/PROJECT/apps` |
| read an app | `GET api/v1/projects/PROJECT/apps/APP` |
| new image tag | `PATCH ...` with `{"services":{"NAME":{"image":"...:TAG"}}}`; nothing else changes, pods roll without downtime |
| roll back | `PATCH` the same way with the previous tag (`GET .../revisions` lists them) |
| change the whole spec | `PUT` the full spec; it replaces everything, so read the app first and send `If-Match: <generation>` |
| restart | `POST .../restart?service=NAME` (all services when omitted); no body |
| rotate the database password | `POST .../addons/mongodb/rotate`; no body |
| delete | `DELETE api/v1/projects/PROJECT/apps/APP`; add `?purge=true` to drop the add-on data too |
| live log tail of running pods | `GET .../logs?service=NAME&tail=200` |
| stored metrics and logs, any window | `GET .../telemetry/metrics`, `GET .../telemetry/logs`, see below |

Deleting is irreversible: confirm with the user before the `DELETE`, and again before
`purge=true`.

## Stored metrics and logs

The `logs` route only tails pods that are running now. For anything older, for pods that
crashed or were replaced, and for CPU, memory, restarts and network, use the telemetry
routes. They read the platform's stores (30 days of metrics, 90 days of logs). You never
have to build a query from scratch: start with the schema and the presets.

```bash
# 1. What exists for this app: metric names, labels, log fields, presets, limits.
nyxid proxy request chrono-cd api/v1/projects/PROJECT/apps/APP/telemetry/schema --output json

# 2. A preset over the last hour (the default window): cpu, memory, restarts, network_rx, network_tx.
nyxid proxy request chrono-cd 'api/v1/projects/PROJECT/apps/APP/telemetry/metrics?preset=memory' --output json

# 3. Error lines of one service over a day.
nyxid proxy request chrono-cd 'api/v1/projects/PROJECT/apps/APP/telemetry/logs?preset=errors&service=api&start=2026-10-20T00:00:00Z&end=2026-10-21T00:00:00Z' --output json
```

Proxy tool: `chrono-cd`, `GET`, and the same three paths with their query strings, for
example `/api/v1/projects/PROJECT/apps/APP/telemetry/metrics?preset=memory`.

Rules for writing your own query (`query=` instead of `preset=`):

- You only ever see this app's pods. chrono-cd pins every query to the owner's namespace
  and the app's pod names on the server, so do not add namespace or pod selectors yourself;
  group by `pod` or `container` instead.
- Metrics are PromQL. Use the names from `schema.metrics.names`; the useful ones are
  `container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`,
  `kube_pod_container_status_restarts_total`, `container_network_*_bytes_total`. A
  service that declared `metrics` in its spec adds its own names to that list. Add
  `{container!=""}` on `container_*` metrics to skip the pod sandbox. Rates need a range,
  for example `rate(...[5m])`. `step` defaults to at most 500 points over the window.
- Logs are LogsQL filters: a word or `"phrase"`, `i(word)` for case-insensitive,
  `AND`, `OR`, `NOT`, a field filter like `kubernetes.container_name:api`, and pipes such
  as `| stats count() as n` or `| fields _time, _msg`. The fields come from
  `schema.logs.fields`. Lines come newest first; `truncated: true` means more matched than
  `limit` (at most 10000): narrow the window or the query.
- Time is RFC 3339, `end` defaults to now, `start` to one hour before, the window is at
  most 31 days. `400 query_rejected` carries the store's own message: fix the query and
  retry. `501 telemetry_disabled` means this platform has no store.

Show the user numbers with units (cores, MiB, restarts) and the window you used. For a
"why did it crash" question, combine `restarts` with `preset=errors` around the restart.

## Ask for more quota

```bash
nyxid proxy request chrono-cd api/v1/quota-requests --method POST \
  --data '{"cpu_request": "4", "memory_request": "8Gi", "pods": 20, "storage": "40Gi", "reason": "..."}' --output json
```

Proxy tool: `chrono-cd`, `POST`, `/api/v1/quota-requests`, body: that object. Add
`"apps": 30` to ask for a higher app cap; without it the cap stays as it is.

One pending request per owner. A platform admin approves or rejects; `GET api/v1/quota-requests`
shows the state. Tell the user it is not instant.

## References

`references/api.md` is the full contract, every field and response. `references/errors.md`
lists every error key. Both are bundled with this skill; read them when something here is
not enough. If the API and this manual disagree, the API is right.
