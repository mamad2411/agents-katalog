---
name: kong-configuration-validation
description: >
  Validates Kong's declarative configuration (`kong.yml`) and
  Kubernetes CRDs (`KongPlugin`, `KongIngress`, `KongConsumer`) before
  they reach production — schema-checking with `deck validate`,
  diffing against the live gateway state with `deck diff`, and
  confirming a route/plugin actually behaves as intended rather than
  just parsing. Use when a user asks to "validate kong.yml before
  deploying," "check what a deck sync will actually change," "why
  isn't my Kong plugin taking effect," "lint Kong config in CI," or
  "test a rate-limiting or auth plugin before it goes live."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Kong Configuration Validation

## Purpose

A `kong.yml` file or `KongPlugin` CRD that parses successfully can still
be a no-op in production: a plugin attached to the wrong Route or
Service name (a typo Kong's schema validator has no way to catch,
because it's just a string reference), a rate-limiting plugin left on
the default `local` counting policy that silently multiplies across
nodes, or a `deck sync` that removes a Route nobody meant to touch
because it wasn't present in the source file. None of these fail
loudly — the sync succeeds, the plugin exists, and the gap is only
visible once real traffic hits it (or doesn't). This skill covers the
validation commands that catch these before (or immediately after)
applying, distinct from
[kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md),
which covers writing the Service/Route/Plugin configuration in the
first place.

## When to use

- Before running `deck sync` (or applying Kong CRDs) against a
  production Kong instance, to confirm the change is exactly what's
  intended and nothing else.
- Confirming a plugin (rate-limiting, auth, transformation) attached in
  `kong.yml` or a `KongPlugin` CRD actually resolves to the Route/
  Service/Consumer you meant, not a similarly-named one.
- Diagnosing why a plugin that's clearly present in the config doesn't
  appear to be affecting real traffic.
- Wiring Kong config validation into CI so a declarative sync or CRD
  change that would silently delete an existing Route, misattach a
  plugin, or leave rate-limiting on a per-node counting policy is caught
  in review, not after it reaches the gateway.
- Auditing an existing Kong deployment's Admin API exposure and plugin
  attachment levels before a security review.

## Prerequisites & environment

- `deck` (decK) matching (or compatible with) the target Kong version,
  with network access to the Admin API of the instance being validated
  against (or a disposable/staging Kong instance for CI).
- Read access to the Kong Admin API (`GET /services`, `/routes`,
  `/plugins`, `/consumers`) for anything beyond static file schema
  checking — confirming a plugin's real, effective configuration
  requires reading it back from the running gateway, not just the
  source file.
- On Kubernetes: `kubectl` access to `KongPlugin`, `KongClusterPlugin`,
  `KongIngress`, and `KongConsumer` CRDs, plus the Kong Ingress
  Controller's own logs/status for confirming a CRD was actually
  reconciled (CRD acceptance by the Kubernetes API server doesn't
  guarantee KIC successfully applied it to Kong).
- For CI-integrated validation: a disposable Kong instance (Docker,
  DB-less mode is fastest to spin up) that `deck sync --dry-run` or a
  real `deck sync` can target without risk to production.

## Step-by-step guidance

1. **Validate `kong.yml` schema before diffing or syncing anything**,
   catching structural errors (unknown plugin config field, malformed
   YAML) early:
   ```bash
   deck validate -s kong.yml
   ```
   This confirms the file is well-formed and every plugin's `config`
   block matches that plugin's schema — it cannot confirm a Route
   reference actually exists or that a plugin is attached at the
   intended level, which is what the next steps are for.

2. **Always run `deck diff` before `deck sync`**, and treat its output
   as a change to review, not a formality:
   ```bash
   deck diff --kong-addr https://kong-admin.internal:8444 -s kong.yml
   ```
   `deck diff` shows exactly what will be created, updated, or
   **deleted** — a `kong.yml` that's missing a Route present in the
   live gateway will show it as a deletion, which is easy to miss if the
   diff output isn't actually read before running `sync`.

3. **Confirm a plugin resolves to the intended Route/Service/Consumer**,
   not just that it exists somewhere in the config, since a plugin
   `config` block gives no compile-time guarantee its `route`/`service`/
   `consumer` reference is the one you meant:
   ```bash
   curl -s https://kong-admin.internal:8444/routes/payments-api-route/plugins | jq
   curl -s https://kong-admin.internal:8444/services/payments-api/plugins | jq
   ```
   Cross-check the returned plugin list's `name` and `config` against
   what you intended for that specific Route/Service — a plugin
   attached one level higher or lower than intended is accepted without
   error at apply time.

4. **Confirm rate-limiting's counting policy explicitly**, since the
   difference between `local` and `redis`/`cluster` has no effect on
   whether `deck sync` succeeds, only on whether the limit is enforced
   correctly at runtime:
   ```bash
   curl -s https://kong-admin.internal:8444/plugins?name=rate-limiting | \
     jq '.data[].config.policy'
   ```
   Any result showing `local` on a multi-node deployment is a real
   finding, not a stylistic choice — flag it before this reaches
   production. See
   [api-gateway-rate-limiting-and-quota-management](../api-gateway-rate-limiting-and-quota-management/SKILL.md)
   for why this matters at the strategy level.

5. **Test auth and rate-limiting plugins against real requests in
   staging**, not just by reading the config back, since a
   syntactically-correct plugin can still be misconfigured in a way
   only visible under live traffic (wrong header name, wrong `limit_by`
   scope):
   ```bash
   curl -i https://kong-staging.internal/v1/payments -H "apikey: <TEST_KEY>"
   # expect 200 with a valid key
   curl -i https://kong-staging.internal/v1/payments
   # expect 401 with no key
   for i in $(seq 1 105); do curl -s -o /dev/null -w "%{http_code}\n" \
     https://kong-staging.internal/v1/payments -H "apikey: <TEST_KEY>"; done | sort | uniq -c
   # expect a mix of 200s followed by 429s once the configured limit is exceeded
   ```

6. **For Kubernetes CRDs, confirm KIC actually reconciled the change**,
   not just that `kubectl apply` succeeded:
   ```bash
   kubectl apply --dry-run=server -f kongplugin-rate-limit.yaml
   kubectl apply -f kongplugin-rate-limit.yaml
   kubectl get kongplugin rate-limit-payments -o yaml | grep -A5 status
   kubectl logs -n kong deploy/kong-ingress-controller --tail=100 | grep -i payments
   ```
   A `KongPlugin` CRD with no corresponding entry in Kong's Admin API
   (`GET /plugins`) means KIC failed to reconcile it — check the
   controller's logs for the actual reason (often a missing
   `konghq.com/plugins` annotation on the target Ingress) rather than
   assuming the plugin is active because the CRD exists.

7. **Wire into CI as a gate**: fail the pipeline on a non-zero
   `deck validate` exit, and on any `deck diff` showing an unreviewed
   deletion or a rate-limiting plugin whose `policy` isn't
   `redis`/`cluster` in a multi-node target:
   ```bash
   deck validate -s kong.yml || exit 1
   deck diff --kong-addr "$KONG_ADMIN_ADDR" -s kong.yml > diff.txt
   grep -q "^- " diff.txt && { echo "unexpected deletions in diff"; cat diff.txt; exit 1; }
   ```

8. **Audit Admin API exposure as part of validation**, not just
   plugin/route correctness — an unauthenticated Admin API reachable
   outside a trusted network is a standing risk regardless of how
   correct the Route/Plugin config itself is:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://kong-admin.internal:8444/status
   # from outside the trusted network — expect connection refused/timeout,
   # not a 200
   ```

## Best practices

- Never run `deck sync` without first reading the `deck diff` output —
  a missing Route/Service in the source file is a silent deletion, not
  a validation error, and `sync` will happily remove it.
- Confirm every plugin's actual runtime attachment (`GET
  /routes/<name>/plugins`, `/services/<name>/plugins`) after syncing,
  not just that `deck validate`/`deck sync` exited zero — schema
  validity and correct attachment level are different guarantees.
- Treat a rate-limiting plugin's `policy` field as a required check,
  not an optional detail — `local` on a multi-node Kong deployment is a
  functional bug, not a valid alternative configuration, unless the
  deployment is genuinely single-node.
- For Kubernetes, always check KIC's own reconciliation status/logs
  after applying a CRD — CRD acceptance by the Kubernetes API server is
  necessary but not sufficient evidence the plugin is live in Kong.
- Test auth and rate-limiting plugins against real HTTP requests in
  staging (expect 401 without credentials, 429 past the limit) before
  trusting a config read-back alone — a plugin can be present and
  correctly attached while still using the wrong header name or scope.
- Periodically audit Admin API network exposure independent of any
  specific config change — it's a standing risk that doesn't show up in
  a `kong.yml`/CRD diff at all.

## Common pitfalls

- **Symptom:** `deck sync` runs cleanly, but a Route that existed
  yesterday returns `404 Not Found` today, and nobody remembers
  deleting it.
  **Fix:** The Route was simply absent from the `kong.yml` used for the
  sync (e.g. an incomplete export, a merge that dropped a section), and
  `deck sync` treats "not in the source" as "delete it." Always read
  `deck diff` output before syncing, and keep the full declarative
  config in version control so an incomplete file is caught by a
  smaller-than-expected diff, not discovered as a production 404.

- **Symptom:** A `rate-limiting` plugin's config looks correct and
  `deck validate` passes, but the effective limit in production is far
  higher than configured.
  **Fix:** Check `config.policy` via the Admin API
  (`GET /plugins?name=rate-limiting`) — `local` counts per Kong node
  independently, so the true cluster-wide limit is the configured value
  multiplied by node count. Switch to `redis`/`cluster` and confirm via
  the same query that the change took effect.

- **Symptom:** A `KongPlugin` CRD applies with no `kubectl` errors, but
  the plugin never shows up when querying Kong's Admin API directly.
  **Fix:** CRD acceptance by the Kubernetes API server only confirms
  schema validity — it does not confirm the Kong Ingress Controller
  successfully reconciled it into Kong. Check the CRD's `status` field
  and the KIC pod's logs for a reconciliation error, most commonly a
  missing `konghq.com/plugins: <plugin-name>` annotation on the target
  `Ingress` that the plugin is supposed to attach to.

- **Symptom:** An `key-auth`/`jwt` plugin is confirmed present and
  correctly attached, but requests with valid credentials still return
  `401 Unauthorized`.
  **Fix:** Check the plugin's `config` for the exact header/claim name
  expected (`key_names`, JWT claim mappings) against what the client
  is actually sending — a plugin can be perfectly attached to the right
  Route while still expecting a different header name than the one the
  client uses; confirm with a real `curl` test in staging rather than
  assuming attachment correctness implies behavioral correctness.

- **Symptom:** To unblock testing during an incident, someone
  temporarily removes the `key-auth`/rate-limiting plugin from a
  production Route via a direct Admin API call, confirms traffic now
  flows, and it's still missing hours later.
  **Fix:** This is a real, unmanaged security/availability gap once
  left in place — the change bypassed the declarative source of truth
  entirely, so the next `deck sync` from the (unchanged) `kong.yml`
  would silently restore it, but until then the Route has neither auth
  nor rate-limiting. Treat any direct Admin API change as strictly
  temporary and tracked, and re-run `deck diff`/`deck sync` from the
  reviewed source immediately once the incident's real cause is found.

## Worked example

**Scenario:** Validate the `payments-api` `kong.yml` (Service, Route,
`key-auth`, and Redis-backed `rate-limiting` plugin) from the worked
example in
[kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md)
before syncing it to production.

```bash
# 1. Schema validation
deck validate -s kong.yml

# 2. Diff against the live gateway — read this output, don't skim it
deck diff --kong-addr https://kong-admin.internal:8444 -s kong.yml

# 3. Sync to a staging Kong instance first
deck sync --kong-addr https://kong-staging-admin.internal:8444 -s kong.yml

# 4. Confirm plugin attachment and policy on staging
curl -s https://kong-staging-admin.internal:8444/routes/payments-api-route/plugins | \
  jq '.data[] | {name, config}'
# expect: key-auth and rate-limiting plugins listed, rate-limiting config.policy == "redis"

# 5. Behavioral test against staging
curl -i https://kong-staging.internal/v1/payments -H "apikey: <TEST_KEY>"
curl -i https://kong-staging.internal/v1/payments
# expect 200 with the key, 401 without it
```

Only once the diff shows only the intended additions (no unexpected
deletions), the plugin query confirms `policy: redis` (not `local`), and
the 200/401 behavioral test passes against staging, is the same
`kong.yml` synced to the production Admin API — followed by re-running
step 4's plugin query and step 5's behavioral test against production to
confirm parity before the change is considered complete.

## Cross-references

- [kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md) — writing the Service/Route/Plugin configuration this skill validates.
- [api-gateway-rate-limiting-and-quota-management](../api-gateway-rate-limiting-and-quota-management/SKILL.md) — why the `policy` field on a rate-limiting plugin matters, checked for correctness in step 4 above.
- [consul-configuration-validation](../consul-configuration-validation/SKILL.md) — the equivalent validation discipline (dry-run, then confirm real effect) applied to Consul's config entries and intentions, useful for comparing pre-production check patterns across tools.
