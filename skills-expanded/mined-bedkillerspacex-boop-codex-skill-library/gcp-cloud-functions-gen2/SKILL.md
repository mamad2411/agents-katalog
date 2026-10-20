---
name: gcp-cloud-functions-gen2
description: >
  Deploy and harden Cloud Functions 2nd gen (based on Cloud Run): entrypoints, event
  triggers, IAM invokers, secrets, concurrency/CPU, VPC connectors, and min instances.
  Use when building or reviewing owned gen2 functions and distinguishing them from gen1
  behaviors.
---

# GCP Cloud Functions Gen2

## Scope And Authorization

- **In scope:** Cloud Functions gen2 in GCP projects you own.
- **Out of scope:** invoking or modifying other customers’ functions without authorization.
- Prefer non-prod for experiments; guard public invokers.
- Redact function URLs with tokens and secret values.
- Pair code with `code-quality-standards`.

## When To Use

- Creating **2nd gen** HTTP or event-driven functions.
- Migrating gen1 → gen2 (Cloud Run underpinnings).
- Setting IAM `roles/run.invoker`, secrets, VPC egress, and scaling.
- Reviewing gen2-specific networking and concurrency.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cloud Run Jobs batch | `gcp-cloud-run-jobs` |
| Cloud SQL IAM auth | `gcp-cloud-sql-iam-auth` |
| Binary Authorization | `gcp-binary-authorization` |
| Secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Gen2 notes |
| --- | --- |
| Runtime base | Runs on Cloud Run services |
| HTTP auth | Invoker IAM; avoid `allUsers` unless intentional public |
| Events | Eventarc triggers common |
| Concurrency | Multiple requests per instance possible—write thread-safe code |
| Secrets | Secret Manager volume/env integrations |
| Networking | VPC access / Direct VPC egress options per current product |

## Workflow

### 1. Confirm scope and success criteria

1. Runtime language, trigger type, data sensitivity, max latency/cost.
2. Success: least-privilege invokers; secrets not in source; private networking if required; gen2 settings explicit in IaC.
3. Rollback: previous revision traffic.

### 2. Inventory

```bash
gcloud functions list --gen2 --project=PROJECT --regions=REGION
gcloud functions describe NAME --gen2 --region=REGION --project=PROJECT
```

1. Check IAM policy on underlying Cloud Run service.
2. List env vars for plaintext secrets.

### 3. Implement securely

```bash
gcloud functions deploy NAME \
  --gen2 \
  --runtime=python312 \
  --region=REGION \
  --source=. \
  --entry-point=handler \
  --trigger-http \
  --no-allow-unauthenticated
```

```python
# handler sketch
import os
def handler(request):
    # validate auth already via IAM; still validate input
    return ("ok", 200)
```

1. **Never** embed service account keys; use function SA.
2. Grant only required roles to function SA (e.g. specific secret accessor).
3. For public HTTP: WAF/Cloud Armor, rate limits, app auth still required.
4. Set max instances to bound cost/DoS blast radius.
5. Use Secret Manager; prefer mount over plaintext env when suitable.
6. Enable ingress restrictions (internal-only) when only GCP callers needed.

### 4. Event-driven specifics

1. Eventarc trigger principals limited.
2. Validate event payload schema; idempotent handlers.
3. Poison-message strategy for bad events.

### 5. Verify with evidence

```bash
# Unauthenticated should fail if not public
curl -sS -o /dev/null -w "%{http_code}\n" "https://FUNCTION_URL"
# Authenticated
curl -sS -H "Authorization: Bearer $(gcloud auth print-identity-token)" "https://FUNCTION_URL"
```

| Check | Expect |
| --- | --- |
| allUsers invoker | Absent unless intended |
| Secret in source | None |
| Revision rollback | Documented |
| VPC path | Works for private SQL if required |

### 6. Observe and harden

1. Logs/metrics via Cloud Logging; alert on 5xx and instance thrash.
2. Review IAM quarterly.
3. Pin runtime versions; patch dependencies.

### 7. Hand off

1. Function SA role list; trigger diagram; scaling params.
2. Distinguish from Cloud Run Jobs for batch work.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | Invoker IAM + app checks | Public + no app auth |
| Secrets | Secret Manager | Hardcoded in repo |
| SA | Least roles | Project editor SA |
| Concurrency | Safe code / set concurrency | Global mutable state races |
| Ingress | Internal when possible | Public default unaware |
| Gen | Explicit `--gen2` IaC | Mixed gen1/gen2 confusion |

## Output Checklist

- [ ] Gen2 functions inventoried
- [ ] Trigger and IAM documented
- [ ] Secrets storage verified
- [ ] SA least privilege
- [ ] Scaling/concurrency set
- [ ] Network path verified if private resources used
- [ ] Authz tests evidenced
- [ ] `code-quality-standards` applied

## Rules

- Owned projects only.
- Gen2 shares Cloud Run security model—review invokers carefully.
- Prefer identity-based invocation over shared secrets in URLs.
- Keep function code pure enough for safe concurrency or set concurrency=1 when required.
