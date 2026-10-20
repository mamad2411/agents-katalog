---
name: dwara-config
description: Author, validate, lint, format, diff, explain, and hot-reload Dwara API gateway configuration - the single strict YAML file (listeners, routes, services, upstreams, consumers, policies, ai, admin, analytics) and the dwara-cli tooling around it. Use whenever editing dwara.yaml, attaching policies, fixing validation errors, resolving ${ENV}/${file} secret references, or reasoning about config generations and reload behavior.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Needs the dwara-cli binary on PATH for validate/fmt/lint/diff/explain/schema (or `cargo run --bin dwara-cli` from the repo).
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.1"
---

# Dwara configuration

Dwara is configured by **one strict YAML file** (default `./dwara.yaml`,
override with `DWARA_CONFIG=/path/to/dwara.yaml`). "Strict" means
`deny_unknown_fields`: a typo'd or unknown key is a validation error that
names its exact path - never a silent ignore.

## The golden loop

Make every config change this way:

```sh
dwara-cli validate dwara.yaml    # 1. full Parse->Validate->Compile; prints ALL issues with paths
dwara-cli fmt dwara.yaml         # 2. (optional) normalize formatting in place
dwara-cli lint dwara.yaml        # 3. advisory rules; exit 0 clean, 2 = warnings, 1 = error
# 4. save/reload: the running gateway picks up file changes automatically
#    (atomic rename, debounced), or send SIGHUP, or PATCH /config.
```

Never skip validate. A config that fails the pipeline **never replaces the
running snapshot** - the gateway keeps serving the previous generation and
logs every issue.

**Ground truth rule:** if unsure a key exists, check the live schema -
`dwara-cli schema` prints the JSON Schema generated from the running code
(the repo's `config-reference.json` is the same output). Schema beats docs;
docs beat memory.

## Mental model

```
listeners  -> where traffic enters (ports, TLS, per-listener policy/authz)
routes     -> match (path/host/methods/headers/query/cookies/accept) + action
services   -> bind a route to upstream(s); traffic splits and sticky live here
upstreams  -> endpoint pools + transport, health, retries, timeouts, breaker
consumers  -> authenticated identities + credentials + quotas + AI budgets
policies   -> reusable bundles (rate_limit(s), timeouts, token_budget, anomaly, adaptive)
             attached at: consumer > route > service > listener > global_policies
```

Request-time composition: **route wins the path**; policies **AND together**
across all attachment levels; authorization denies at *any* level win.

Full key-by-key map: [references/config-map.md](references/config-map.md).
Complete CLI usage incl. `diff` and `explain`:
[references/cli-tooling.md](references/cli-tooling.md).
Reload semantics and secret references:
[references/reload-and-secrets.md](references/reload-and-secrets.md).

## The five-minute mental checklist for any edit

1. Which **entity** does the change belong to (route-level? upstream-level?
   gateway-level block?) - prefer the most specific place.
2. Does a **policy** already exist to reuse (`policies[]` referenced by
   name)? `dwara-cli lint` flags `policy-unused`, `consumer-unused`,
   `upstream-unreferenced`, `prefix-duplicate`,
   `regex-shadowed-by-exact`.
3. Are all names **referentially consistent** (route.service ->
   services[].name; service.upstream -> upstreams[].name; policy refs)?
4. Any secret inlined? Move it to `${ENV_VAR}` or `${file:/path}` - see
   reload-and-secrets reference for the exact forms.
5. `dwara-cli explain --config dwara.yaml --method GET --path /v1/x` to see
   the decision the gateway would make - catches match-precedence surprises
   (exact > regex > prefix; non-path criteria AND after path; misses are
   404s, not fall-through).

## Reserved paths and globals

- `/healthz`, `/readyz`, `/metrics` are gateway-served on every listener and
  exempt from `global_policies`.
- `global_policies` apply to every request *including unrouted 404s* (unlike
  the reserved paths).
- `max_concurrent_requests` caps concurrency gateway-wide; with
  `admission_queue.enabled: true` over-cap requests wait in a bounded
  priority-aware queue instead of being shed.
- `trusted_proxies` controls whose `X-Forwarded-For` is honored (empty =
  trust nobody; the effective client IP feeds rate-limit `ip` selectors,
  IP ACLs, and GeoIP).

## Config evolution

- `dwara-cli migrate dwara.yaml [--in-place]` upgrades the schema `version`
  (prints to stdout without `--in-place`; notes go to stderr).
- `dwara-cli diff old.yaml new.yaml` shows compiled
  route/upstream/consumer deltas as `+`/`-`/`~` - the right review artifact
  before a reload that matters.

## Gotchas that bite

- **Ent blocks are inert, pack blocks are rejected.** An enterprise block in
  an OSS build parses, validates, and is then ignored. But a block whose
  capability is not compiled into the build is *rejected at validation*.
  When validation rejects something the docs describe, check
  `dwara-cli schema` for whether the key exists in your build.
- Secret `${...}` references must resolve at config-build time: an env var
  that is unset fails the publish, it does not fall back to the literal
  text.
- In AI provider auth, the reference must span the **whole value** including
  any prefix: `value: ${OPENAI_AUTH_HEADER}` where the env var itself
  contains `Bearer sk-...`.
- `PATCH /config` is a **full-document replacement** - always GET, edit, PUT
  the whole thing (see the dwara-operations skill).
- Config passed through `GET /config` redacts secrets as
  `${redacted:sha256:...}`; patching a redacted placeholder back verbatim is
  a 400. Keep the source of truth on disk.
