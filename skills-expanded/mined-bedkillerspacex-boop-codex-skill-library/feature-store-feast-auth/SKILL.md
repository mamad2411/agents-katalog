---
name: feature-store-feast-auth
description: >
  Harden Feast feature-store authentication and authorization: registry/online/offline
  store access, project-scoped permissions, service-account and OIDC patterns, and
  least-privilege materialization jobs. Use when reviewing or implementing Feast
  authn/authz on owned feature platforms, preventing cross-project feature leakage,
  locking down gRPC/HTTP serving endpoints, or auditing who can write FeatureViews
  and read online features in lab or authorized environments.
---

# Feature Store Feast Auth

## Scope And Authorization

- **In scope:** Feast deployments you own/operate (registry, offline store, online store, feature server), lab clusters, or engagements with written authorization.
- **Out of scope:** probing third-party feature stores, stealing service-account keys, or bypassing access controls without authorization.
- Prefer non-production validation; production changes need change windows and rollback.
- Redact connection strings, warehouse credentials, tokens, and customer feature values from tickets.
- Pair code/config changes with `code-quality-standards`.

## When To Use

- Designing or reviewing **Feast** auth for registry, materialization, and online serving.
- Preventing unauthorized `get_online_features` / `get_historical_features` across projects.
- Binding Feast feature server to IAM, OIDC, mTLS, or API keys with least privilege.
- Auditing who can push FeatureViews, Entities, and OnDemandFeatureViews to the registry.
- Hardening Spark/Beam materialization jobs that hold warehouse and Redis/Dynamo credentials.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General secrets hygiene / rotation | `secrets-management-hygiene` |
| Redis bind/AUTH/ACL only | `redis-security-misconfig` |
| BigQuery row-level access | `gcp-bigquery-row-access` |
| API JWT abuse patterns | `api-auth-and-jwt-abuse` |
| Implementation quality baseline | `code-quality-standards` |
| Engagement recon methodology | `recon-and-methodology` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Feast components | registry (SQL/GCS/S3), offline (BQ/Snowflake/Redshift/file), online (Redis/Dynamo/Datastore), feature server |
| Auth surfaces | registry write, materialization SA, online store credentials, HTTP/gRPC feature server |
| Isolation unit | Feast project + environment (dev/stage/prod) + data domain |
| High risk | shared Redis without key prefix isolation; world-readable registry; long-lived warehouse keys in CI |
| Verify | denied cross-project reads; server rejects unauthenticated; SA cannot write registry if read-only |

## Feast auth model (practical)

| Actor | Needs | Must not get |
| --- | --- | --- |
| Feature engineer (dev) | registry write in dev project; offline sample reads | prod online credentials; other tenants’ projects |
| Training pipeline | historical features (offline); limited registry read | online store write; arbitrary SQL outside feature views |
| Online inference service | `get_online_features` for its feature services only | registry write; other projects’ keys; materialization |
| Materialization job | offline read + online write for assigned views | warehouse admin; registry delete-all |
| Platform admin | project create, permission grants, secrets rotation | unchecked production without audit |

## Workflow

### 1. Confirm scope and success criteria

1. Record Feast version, deployment mode (local / Kubernetes / managed), projects, and data classification of features.
2. Success examples: unauthenticated feature server returns 401/403; project A identity cannot read project B online features; materialization SA scoped to one online store prefix.
3. Identify break-glass (admin registry access) and secret rotation owners.

### 2. Inventory Feast surfaces

1. Locate `feature_store.yaml` for each env: `project`, `registry`, `provider`, `online_store`, `offline_store`.
2. List feature server exposure (ClusterIP / Ingress / public URL) and auth middleware if any.
3. Inventory identities: CI OIDC, Kubernetes SAs, cloud IAM roles, static keys in env vars or Secret Manager.
4. Map which FeatureServices are consumed by which applications.

```bash
# Inventory (owned cluster/repo) — paths vary
find . -name 'feature_store.yaml' -o -name 'feature_store.yml'
grep -R "online_store\|offline_store\|registry" --include='*.yaml' --include='*.yml' .
```

### 3. Baseline access and leakage risks

1. Attempt (authorized lab) unauthenticated and wrong-project calls to the feature server.
2. Confirm online store key naming / prefix isolation if multiple projects share Redis.
3. Check registry object ACLs (GCS/S3 bucket policy; SQL grants) for public or overly broad read/write.
4. Capture current IAM bindings for warehouse and online store.

```python
# Prove project isolation for online reads (lab / owned)
from feast import FeatureStore

store_a = FeatureStore(repo_path="repos/project_a")
# Expect failure when using project_a credentials against project_b feature refs
try:
    store_a.get_online_features(
        features=["project_b_view:amount"],
        entity_rows=[{"user_id": 1}],
    ).to_dict()
except Exception as e:
    print("expected_deny:", type(e).__name__)
```

### 4. Apply Feast-focused controls

1. **Separate projects and registries** per environment and tenant; never share prod registry write with training notebooks.
2. **Feature server auth:** terminate TLS; require OIDC/JWT or mTLS; authorize by FeatureService / project claim, not only network ACL.
3. **Credential binding:** materialization jobs get offline-read + online-write only; inference gets online-read only; no shared “god” SA.
4. **Online store:** Redis AUTH/ACL or cloud IAM; distinct key prefixes or separate instances per sensitivity tier.
5. **Registry:** encrypt at rest; deny anonymous; version and audit writes of FeatureViews.
6. **Network:** feature server and online store private; no public Redis; egress restrict materialization to warehouse endpoints.
7. **CI:** short-lived OIDC to cloud; no long-lived warehouse keys without rotation.

```yaml
# Conceptual feature_store.yaml notes — inject secrets at runtime
project: payments_prod
provider: gcp
registry: gcs://feast-reg-prod/registry.pb
online_store:
  type: redis
  connection_string: redis://:${REDIS_PASSWORD}@redis-prod:6379
```

```python
# Middleware sketch: reject missing bearer on feature server (app-owned)
def require_auth(request, expected_aud="feast-feature-server"):
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        return 401, {"error": "missing_token"}
    token = auth.split(" ", 1)[1]
    claims = verify_jwt(token, audience=expected_aud)  # org library
    if claims.get("feast_project") != current_project():
        return 403, {"error": "project_mismatch"}
    return 200, claims
```

### 5. Verify with evidence

```bash
# Unauthenticated should fail (owned URL)
curl -sS -o /dev/null -w "%{http_code}\n" \
  -X POST "https://feast.example.internal/get-online-features" \
  -H "Content-Type: application/json" \
  -d '{"features":["fv:f1"],"entities":{"user_id":[1]}}'

# Wrong project token should fail
curl -sS -o /dev/null -w "%{http_code}\n" \
  -X POST "https://feast.example.internal/get-online-features" \
  -H "Authorization: Bearer $WRONG_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"features":["fv:f1"],"entities":{"user_id":[1]}}'
```

1. Prove materialization SA cannot admin-alter warehouse schemas beyond need.
2. Prove registry bucket/SQL is not world-readable.
3. Keep allow/deny log samples redacted.

### 6. Observe and harden

1. Metrics: auth failures on feature server, materialization failures, online store connection errors.
2. Alert on spikes of 401/403 and on registry writes outside change windows.
3. Periodic access review: FeatureServices vs consuming apps; remove orphaned credentials.

### 7. Hand off

1. Document project → identity → store mapping in the runbook.
2. Link secret rotation tickets; note residual shared-store risks.
3. Apply `code-quality-standards` for any server middleware or IaC shipped.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Projects | One Feast project per tenant/env | Single shared project for all apps |
| Feature server | JWT/mTLS + TLS + private network | Open Ingress with no auth |
| Online store | ACL + prefix/instance isolation | Shared Redis, no AUTH |
| Materialization | Job SA least privilege | Engineer laptop keys in prod |
| Registry | Audited, private object store | Public GCS/S3 registry.pb |
| Verification | Cross-project deny evidenced | “VPC so we’re fine” |

## Output Checklist

- [ ] Scope, owner, Feast version, projects, authorization recorded
- [ ] `feature_store.yaml` / registry / online / offline inventory complete
- [ ] Feature server auth mode documented (OIDC/mTLS/API key/network-only)
- [ ] Identities mapped: inference, materialization, engineers, CI
- [ ] Cross-project and unauthenticated denials demonstrated
- [ ] Online store and registry ACLs reviewed
- [ ] Secrets short-lived or rotated; not in git
- [ ] Monitoring for auth failures and registry writes
- [ ] Exceptions have owner + expiry
- [ ] `code-quality-standards` applied if code/IaC shipped

## Rules

- Authorized / owned feature platforms only.
- Treat feature values and entity keys as sensitive data (PII risk).
- Never commit warehouse or Redis passwords; inject at runtime.
- Prefer project and credential isolation over “trust the VPC.”
- Keep focus on Feast authz/authn; route pure Redis hardening or BQ RLS to neighbor skills.
- Evidence over assumptions: show deny paths, not only allow paths.
