---
name: elasticsearch-security-basics
description: >
  Authorized Elasticsearch security hardening: xpack.security (or OpenSearch
  security), HTTP/transport TLS, anonymous access disabled, users/roles/API keys,
  bind addresses, no public 9200/9300, and least-privilege snapshot/restore. Use
  when reviewing elasticsearch.yml, Elastic Cloud/ECK/self-managed clusters you
  own — not for unauthorized scanning of third-party ES.
---

# Elasticsearch Security Basics

## Scope And Authorization

- **In scope:** Clusters and Elastic Cloud deployments you own or are paid to assess with written scope.
- **Out of scope:** Internet-wide scanning for open 9200, credential stuffing third-party ES, or data exfiltration.
- Prefer staging for disruptive auth/TLS changes; have break-glass local admin recovery steps.
- Redact passwords, API keys, and certificate private keys from tickets.
- Pair ongoing ops with `elasticsearch-ilm-security` and query safety skills.

## When To Use

- Standing up or reviewing a new cluster’s security posture.
- Enabling `xpack.security.enabled` and TLS for HTTP and transport.
- Replacing anonymous / default passwords; introducing roles and API keys.
- Ensuring nodes are not bound to `0.0.0.0` on public networks without controls.
- Baseline before exposing Kibana or cross-cluster search.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ILM retention + snapshot isolation detail | `elasticsearch-ilm-security` |
| Expensive Query DSL controls | `elasticsearch-query-dsl-safety` |
| Runtime field costs | `elasticsearch-runtime-fields` |
| App-layer auth (JWT in API) | `api-auth-and-jwt-abuse` patterns |
| Secrets inventory program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Authn | Native realm / SSO; no anonymous; rotate built-in users |
| Authz | Least-privilege roles; avoid superuser for apps |
| TLS | HTTP for clients; transport for node-to-node |
| Network | Private subnets, SG/NACL, no public 9200 |
| Keys | API keys with short life and narrow indices |
| Audit | Enable audit logging for privileged actions where licensed/available |

## Workflow

### 1. Confirm scope and success criteria

1. Deployment model: self-managed, ECK, Elastic Cloud.
2. Success: unauthenticated access denied; TLS enforced; apps use non-superuser keys; management ports not Internet-open.

### 2. Inventory exposure and config

```bash
# From a trusted admin network only
curl -sS -o /dev/null -w "%{http_code}\n" "http://$ES_HOST:9200/"
curl -sS -u "$ES_USER:$ES_PASS" "https://$ES_HOST:9200/" 
# Node settings (auth required once security on)
curl -sS -u "$ES_USER:$ES_PASS" "https://$ES_HOST:9200/_nodes/settings?pretty" | head
```

1. Read `elasticsearch.yml` / ECK manifests / Elastic Cloud UI security settings.
2. List listeners, `network.host`, `http.port`, `transport.port`, `xpack.security.*`.
3. Cloud SG/firewall: who can reach 9200/9300/Kibana.

### 3. Baseline risks

| Finding | Severity |
| --- | --- |
| HTTP 200 on `/` without auth | Critical |
| Default `elastic` password unchanged | Critical |
| Transport TLS off multi-node | High |
| Public 9200 | Critical |
| App uses superuser | High |
| Snapshots to world-readable bucket | High |

### 4. Enable security and TLS (self-managed sketch)

```yaml
# elasticsearch.yml (illustrative)
xpack.security.enabled: true
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: certs/http.p12
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: certs/transport.p12
xpack.security.transport.ssl.truststore.path: certs/transport.p12
network.host: _site_
http.port: 9200
```

```bash
# Set passwords for built-in users after enable (version-specific tool)
bin/elasticsearch-reset-password -u elastic
bin/elasticsearch-create-enrollment-token -s kibana
```

1. Elastic Cloud: enforce HTTPS, reset passwords, enable traffic filters.
2. ECK: use operator TLS secrets; do not disable security for “simplicity.”
3. Disable anonymous access explicitly if any realm allows it.

### 5. Users, roles, API keys

```bash
curl -sS -u elastic:$ELASTIC_PASS "https://$ES_HOST:9200/_security/user/app_writer" \
  -H 'Content-Type: application/json' -d '{
  "password": "'"$TMP_PASS"'",
  "roles": ["app_writer_role"]
}'

curl -sS -u elastic:$ELASTIC_PASS "https://$ES_HOST:9200/_security/api_key" \
  -H 'Content-Type: application/json' -d '{
  "name": "ci-ingest",
  "expiration": "30d",
  "role_descriptors": {
    "v": {
      "indices": [{
        "names": ["logs-app-*"],
        "privileges": ["create_doc"]
      }]
    }
  }
}'
```

1. Map humans via SSO/SAML when available; local native for break-glass only.
2. Separate read, write, and admin roles.
3. Store API keys in a secrets manager—not in git.

### 6. Verify with evidence

```bash
# Unauthenticated must fail
curl -sS -o /dev/null -w "%{http_code}\n" "https://$ES_HOST:9200/"
# Authenticated cluster health
curl -sS -u "$ES_USER:$ES_PASS" "https://$ES_HOST:9200/_cluster/health?pretty"
# App key cannot call cluster settings
curl -sS -o /dev/null -w "%{http_code}\n" -H "Authorization: ApiKey $APP_KEY" \
  "https://$ES_HOST:9200/_cluster/settings"
```

1. External port scan from outside VPC should not show 9200 (authorized test only).
2. Confirm Kibana/session security and no embedded credentials in dashboards.
3. Snapshot role cannot delete arbitrary indices if policy requires separation.

### 7. Hand off

1. Runbook: password reset, cert rotation, break-glass superuser.
2. Monitor auth failures and anonymous attempts.
3. Schedule cert and API key rotation; link to `elasticsearch-ilm-security` for snapshot IAM.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Exposure | Private link + auth | Open 9200 to 0.0.0.0/0 |
| App identity | Narrow API key | elastic superuser in Beats |
| TLS | HTTP + transport | Cleartext multi-node |
| Passwords | Reset defaults immediately | `changeme` in prod |
| Evidence | curl status codes + SG rules | “Security enabled” checkbox only |

## Output Checklist

- [ ] Deployment model and owner recorded
- [ ] Unauthenticated access tested and denied
- [ ] TLS on HTTP (and transport for multi-node)
- [ ] Built-in users rotated; anonymous off
- [ ] App roles/API keys least privilege
- [ ] Network exposure reviewed (no public 9200)
- [ ] Break-glass recovery documented
- [ ] Residual risk and next review date noted

## Rules

- Authorized clusters only; no opportunistic Internet ES hunting.
- Evidence over assumptions—verify with curl and cloud policy.
- Never commit `elastic` passwords or p12 keys to git.
- Keep this skill on baseline cluster security; ILM/query/runtime have dedicated skills.
- Fail closed: prefer temporary outage over open anonymous access when enabling security.
