---
name: dwara-migration
description: Migrate existing API gateway or API definitions to Dwara - import NGINX, Kong, Envoy, or OpenAPI configs into dwara.yaml (including a fully mocked API from OpenAPI examples), adopt Dwara alongside Terraform workflows (export/plan/apply state over the admin API), and run the Kubernetes Gateway API translator. Use when the task is moving an existing gateway config to Dwara, scaffolding routes from an OpenAPI spec, or managing Dwara with Terraform-style state.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Needs dwara-cli on PATH; Kubernetes translation needs a cluster.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.1"
---

# Migrating to Dwara

Dwara ships importers that convert foreign gateway configs into
`dwara.yaml` (NGINX, Kong, Envoy, Traefik, HAProxy, OpenAPI). **Every
importer appends unsupported-construct warnings as
YAML comments** and its output always passes `dwara-cli validate` - the
migration loop is: import -> read the warnings -> fill the gaps by hand ->
validate -> lint -> diff against reality.

```sh
dwara-cli import nginx   nginx.conf    --output dwara.yaml
dwara-cli import kong    kong.yaml     --output dwara.yaml
dwara-cli import envoy   envoy.yaml    --output dwara.yaml
dwara-cli import traefik traefik.yml   --output dwara.yaml
dwara-cli import haproxy haproxy.cfg   --output dwara.yaml
dwara-cli import openapi petstore.yaml --output dwara.yaml [--mock]
```

## What converts, what doesn't (the short table)

| Source | Converts | Does NOT convert (manual follow-up) |
| --- | --- | --- |
| NGINX | `server`/`location` + `proxy_pass` -> routes/services; `upstream` blocks -> upstreams | `if`, `rewrite`, `auth_basic`, `limit_req`, `try_files` |
| Kong (decK YAML/JSON) | services, routes, upstreams, consumers | plugins (any), key-auth credentials, ACL groups |
| Envoy (static config) | listeners, clusters, routes | HTTP filters (ext_authz/ratelimit/RBAC), network filters (tcp_proxy), TLS contexts |
| OpenAPI 3.x | one route per unique path (+ `openapi` metadata extension per route); with `--mock`: mock actions from response examples | real upstream wiring (placeholder `127.0.0.1:9000`) |

Per-source mapping details and the post-import checklist:
[references/importers.md](references/importers.md).

## OpenAPI mock mode - instant sandbox API

`--mock` reads each operation's response examples and emits
`action.type: mock` routes (`status`/`body`/`headers` + `delay_ms`; or
`body_file` read at publish time). The result is a fully functional mocked
API with **no backend** - ideal for front-end development, contract
testing, and demos. Pair with `request_validation.body_schema` (mismatch ->
`400 validation_failed`) to enforce the contract on the way in.

## Terraform-shaped state over the admin API

```sh
dwara-cli tf export --admin https://gw:2019 --out-state dwara.tfstate --out-hcl dwara.tf
dwara-cli tf plan   --admin https://gw:2019 --state dwara.tfstate      # exit 0 = no diff, 1 = diff
dwara-cli tf apply  --admin https://gw:2019 --state dwara.tfstate [--config desired.yaml]
dwara-cli tf apply-crud --admin ... --state ...                        # per-entity CRUD instead of full-doc PATCH
```

Resource types: `dwara_listener`, `dwara_route`, `dwara_service`,
`dwara_upstream`, `dwara_consumer`. `apply` pushes via full-document
`PATCH /config`; `apply-crud` uses the entity CRUD endpoints (listeners
excluded - they are file/PATCH-managed). Details:
[references/terraform-k8s.md](references/terraform-k8s.md).

## Kubernetes Gateway API

The translator reconciles `Gateway`/`HTTPRoute`/`GatewayClass` (+ Ingress)
into a Dwara config file the gateway hot-reloads - a two-container pattern
(controller + gateway). Environment knobs:
`DWARA_K8S_CONTROLLER_NAME` (default `shristilabs.com/dwara`),
`DWARA_K8S_INGRESS_CLASS` (`dwara`), `DWARA_K8S_OUTPUT_CONFIG`
(`/etc/dwara/dwara.yaml`), `DWARA_K8S_NAMESPACE`. The
`dwara-cli k8s conformance-report` subcommand emits the upstream conformance
report YAML (check `dwara-cli k8s --help` in your build for availability).
Details: [references/terraform-k8s.md](references/terraform-k8s.md).

## Migration workflow that works

1. **Inventory** the source config; note constructs in the "does not
   convert" column - they become your worklist, not surprises.
2. **Import** to a branch, read every warning comment in the output.
3. **Close the gaps** with native Dwara equivalents:
   - NGINX `limit_req` -> `policies[].rate_limit` (+ attach)
   - NGINX `auth_basic` / Kong key-auth -> consumers with `api_key`
     credentials (+ admin-issued keys)
   - Envoy ext_authz -> built-in authorization chain (see dwara-security)
   - Envoy ratelimit filter -> rate-limit policies
   - Kong plugins generally -> routes/policies/consumers equivalents; some
     have no analogue - decide explicitly.
4. **Validate + lint + explain**:
   `dwara-cli validate && dwara-cli lint`, then
   `dwara-cli explain` spot-checks on the source system's top paths.
5. **Dry-run in shadow**: mirror production traffic at a small percentage
   (`mirror.percentage`) and compare; or `dwara replay capture` on the old
   edge and `replay run --diff` against the new config.
6. **Cut over** with a config you can `diff` on rollback; keep the old
   config files around.

## Gotchas

- Importers produce a **starting point**, never parity - budget time for
  the warning-comment worklist.
- The OpenAPI importer emits a placeholder upstream (`127.0.0.1:9000`) -
  replace it before real traffic; with `--mock` it's intentionally left.
- `tf apply` is full-document PATCH semantics: concurrent file edits and
  applies will race - pick one source of truth per environment (file +
  SIGHUP/PATCH-by-file, or Terraform state - not both).
- Kong ACL groups import as warnings, but Dwara `groups` on consumers +
  `allowed_groups`/`denied_groups` authz is usually the direct replacement.
