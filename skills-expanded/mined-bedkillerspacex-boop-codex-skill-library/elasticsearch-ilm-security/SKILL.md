---
name: elasticsearch-ilm-security
description: >
  Secure Elasticsearch/OpenSearch lifecycle and access together: ILM policies,
  rollover aliases, snapshot isolation, roles/API keys for ILM and restore, and
  field/document security basics. Use on owned clusters when ILM, hot-warm-cold,
  snapshot repos, or least-privilege retention. Complements
  elasticsearch-security-basics; not general query performance alone.
---

# Elasticsearch ILM Security

## Scope And Authorization

- **In scope:** Elasticsearch or OpenSearch clusters you own (self-managed, ECK, Elastic Cloud) with change control.
- **Out of scope:** Altering retention or snapshots on third-party clusters without authorization.
- ILM deletes and freezes data—confirm legal hold / compliance before aggressive delete phases.
- Snapshot repositories hold full data copies; isolate credentials and bucket policies.
- Redact connection strings and API keys from notes.

## When To Use

- Designing or auditing ILM policies (hot → warm → cold → delete) with security roles.
- Ensuring search users cannot manage ILM or restore arbitrary snapshots.
- Separating snapshot repository credentials from app users.
- Aligning retention with GDPR/deletion and security log keep requirements.
- Preventing privilege escalation via overly broad `manage_ilm` / `manage` cluster privileges.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cluster TLS, anonymous disable, network exposure | `elasticsearch-security-basics` |
| Expensive query / circuit breakers | `elasticsearch-query-dsl-safety` |
| Runtime field cost control | `elasticsearch-runtime-fields` |
| Secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| ILM | Explicit policies; test rollover on non-prod; min_age aligned to compliance |
| Aliases | Write alias + rollover; apps never write to concrete index names if avoidable |
| Roles | Split: ingest, read, ilmmgr, snapshot_admin |
| Snapshots | Dedicated repo IAM; readonly restore roles ≠ delete repo |
| FLS/DLS | Field/document security for multi-tenant indices |
| Delete | Soft-confirm delete phase; protect security/audit indices longer |

## Workflow

### 1. Confirm scope and success criteria

1. Data classes (logs, metrics, product, audit) and required retention per class.
2. Success: ILM attached to all write aliases; no app role can delete snapshots or change ILM cluster-wide; restore tested.

### 2. Inventory ILM and security

```bash
# Adjust auth: -u user:pass or API key header
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_ilm/policy?pretty" | head
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_ilm/status?pretty"
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_cat/templates?v"
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_snapshot?pretty"
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_security/role?pretty" | head
```

1. List indices missing policy: `_cat/indices` + settings `index.lifecycle.name`.
2. Note who holds `superuser` or broad `manage` cluster privileges.

### 3. Baseline risk

1. Indices with infinite retention or no ILM.
2. Snapshot repos shared across prod/non-prod.
3. API keys that combine write + manage_ilm + snapshot.

### 4. Define ILM policy and templates

```json
PUT _ilm/policy/logs-secure-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": { "max_primary_shard_size": "50gb", "max_age": "1d" },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "3d",
        "actions": { "shrink": { "number_of_shards": 1 }, "forcemerge": { "max_num_segments": 1 } }
      },
      "delete": {
        "min_age": "30d",
        "actions": { "delete": {} }
      }
    }
  }
}
```

1. Attach via index template / component template to data streams when possible.
2. Keep **audit/security** indices on longer policies with restricted delete.
3. Validate rollover in stage with accelerated timings first, then production ages.

### 5. Least-privilege roles for ILM and snapshots

```json
PUT _security/role/logs_ingest
{
  "indices": [{
    "names": ["logs-*-*"],
    "privileges": ["create_doc", "auto_configure"]
  }]
}

PUT _security/role/logs_reader
{
  "indices": [{
    "names": ["logs-*-*"],
    "privileges": ["read", "view_index_metadata"],
    "field_security": { "grant": ["@timestamp", "message", "service.*"] }
  }]
}

PUT _security/role/ilm_operator
{
  "cluster": ["manage_ilm", "monitor"],
  "indices": [{
    "names": ["logs-*-*"],
    "privileges": ["manage"]
  }]
}
```

1. App keys: ingest or read only—not `manage_ilm`.
2. Snapshot admin: separate human break-glass; repository bucket policy denies non-backup roles.
3. Restore into designated indices only; practice restore in DR drills.

### 6. Verify with evidence

```bash
curl -sS -u "$ES_USER:$ES_PASS" "$ES/logs-*/_settings/index.lifecycle?pretty" | head
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_ilm/explain/logs-*?pretty" | head
# Negative: app API key cannot put ILM policy
curl -sS -o /dev/null -w "%{http_code}\n" -H "Authorization: ApiKey $APP_KEY" \
  -X PUT "$ES/_ilm/policy/evil" -H 'Content-Type: application/json' -d '{"policy":{"phases":{}}}'
```

1. Confirm explain shows expected phase for sample indices.
2. Confirm delete phase does not apply to legal-hold indices.
3. Snapshot create/restore dry-run with least-privilege users.

### 7. Hand off

1. Runbook: stalled ILM steps, how to retry, who may `_ilm/move`.
2. Monitor: ILM errors, snapshot failures, unexpected index growth.
3. Review API keys quarterly; rotate snapshot credentials.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| App privileges | create_doc on data stream | superuser API key in Beats |
| Retention | Policy per data class | No delete phase forever |
| Snapshots | Isolated repo + IAM | Public S3 repo ACLs |
| FLS | Grant only needed fields | Full read for all support staff |
| Changes | Stage policy first | Edit prod delete min_age blindly |

## Output Checklist

- [ ] Retention requirements per data class recorded
- [ ] ILM policies and templates cover write paths
- [ ] Roles split ingest / read / ILM / snapshot
- [ ] Snapshot repo isolation verified
- [ ] Negative auth tests for manage_ilm
- [ ] `_ilm/explain` evidence captured
- [ ] Legal hold / audit exceptions documented with owner
- [ ] Monitoring for ILM/snapshot failures
- [ ] Residual risk and review date noted

## Rules

- Owned clusters only; respect compliance before delete phases.
- Least privilege for automation keys.
- Never store snapshot cloud secrets in application config repos.
- Use `elasticsearch-security-basics` for cluster-wide auth/TLS first if missing.
