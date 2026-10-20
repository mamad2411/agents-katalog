---
name: fluent-bit-pipeline-security
description: >
  Secure Fluent Bit logging pipelines: input trust boundaries, filter-based redaction,
  output authentication/TLS, config injection risks, and least-privilege runtime. Use when
  deploying or reviewing owned Fluent Bit DaemonSets/sidecars that ship logs/metrics to
  remote backends.
---

# Fluent Bit Pipeline Security

## Scope And Authorization

- **In scope:** Fluent Bit agents and log backends you operate.
- **Out of scope:** scraping logs from systems without authorization or exfiltrating third-party data.
- Log pipelines often see secrets—redaction is mandatory before centralization when possible.
- Protect output credentials; never commit them in ConfigMaps plaintext if avoidable.
- Pair config/IaC with `code-quality-standards`.

## When To Use

- Designing **inputs → filters → outputs** for Fluent Bit.
- Preventing secret leakage (tokens, passwords, Authorization headers) into Elasticsearch/Loki/S3.
- Hardening outputs with TLS, API tokens, IAM roles.
- Multi-tenant clusters where agents must not read arbitrary secrets from disk.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Broader observability strategy | `observability-metrics-tracing` |
| Secrets management program | `secrets-management-hygiene` |
| K8s RBAC generally | cluster security skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Stage | Security notes |
| --- | --- |
| Input | tail paths allowlist; avoid world-readable secret volumes |
| Parser | Do not execute untrusted configs from users |
| Filter | nest/grep/modify/lua for redaction; drop noisy sensitive debug |
| Output | TLS verify; auth; endpoint allowlist |
| Runtime | non-root; readOnlyRootFilesystem where possible; limited hostPath |

## High-risk anti-patterns

| Pattern | Risk |
| --- | --- |
| `hostPath: /` tail | Reads everything including cloud keys |
| Lua from untrusted source | Code execution in agent |
| Output HTTP without TLS | Credential/log interception |
| Ship `Authorization: Bearer` lines | Token centralization breach |
| Shared output creds across tenants | Cross-tenant blast radius |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster/hosts, log types, destinations, retention, compliance (PII).
2. Success: only intended paths read; secrets redacted; backend auth works; agent cannot write arbitrary cluster state.
3. Owners for parsers and redaction rules.

### 2. Inventory pipeline

```bash
# K8s example
kubectl -n logging get cm,ds,deploy -l app.kubernetes.io/name=fluent-bit
# Local
rg -n "\[INPUT\]|\[FILTER\]|\[OUTPUT\]" fluent-bit*.conf
```

1. List all inputs (tail, systemd, forward, http).
2. List outputs and credential sources.
3. Note any `exec` or unbound hostPath mounts.

### 3. Baseline leakage test

1. Emit a canary log line containing a fake secret pattern in a monitored app.
2. Confirm central store shows redacted form or drop.
3. Confirm real secrets (injected as env) are not tailed from `/proc` accidentally.

### 4. Apply secure pipeline patterns

```ini
[SERVICE]
    Flush        5
    Daemon       Off
    Log_Level    info
    HTTP_Server  Off

[INPUT]
    Name              tail
    Path              /var/log/containers/*_app-prod_*.log
    Parser            cri
    Tag               kube.*
    Mem_Buf_Limit     50MB
    Skip_Long_Lines   On

[FILTER]
    Name    kubernetes
    Match   *
    # rewrite rules: redact bearer tokens, AWS keys, etc. (tune carefully)

[FILTER]
    Name    nest
    Match   *
    # optional structure

[OUTPUT]
    Name            es
    Match           *
    Host            logs.example.internal
    Port            443
    TLS             On
    TLS.Verify      On
    HTTP_User       ${ES_USER}
    HTTP_Passwd     ${ES_PASS}
```

1. **Path allowlists** for tail; never entire node root.
2. Prefer cloud IAM (IRSA/Workload Identity) over static output passwords when supported.
3. Turn off unnecessary HTTP monitor or bind to localhost with auth.
4. Drop debug inputs in prod; limit multiline buffer sizes (DoS).
5. Validate config in CI (`fluent-bit -c conf -v` dry patterns) before roll out.
6. Separate pipelines for high-sensitivity namespaces if multi-tenant.

### 5. Verify with evidence

```bash
fluent-bit --version
# After deploy: search backend for canary secret string — expect zero hits
# Wrong output password — agent errors without crashing node disk full loops carefully monitored
```

| Check | Expect |
| --- | --- |
| Canary secret | Redacted/dropped |
| TLS verify off | Not used in prod |
| hostPath scope | Minimal |
| RBAC | Agent SA cannot get secrets cluster-wide unless required |

### 6. Observe and harden

1. Metrics: input bytes, dropped records, output retries, retry-failed.
2. Alert on output auth failures and sudden volume spikes.
3. Review new filter rules like code (PR).

### 7. Hand off

1. Document redaction catalog and owners.
2. Credential rotation runbook for outputs.
3. Apply `code-quality-standards` for any Lua/scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Inputs | App log paths only | Tail `/var/lib/kubelet/pods/**/secrets/**` |
| Secrets out | IAM + TLS | Token in ConfigMap + HTTP |
| Redaction | Filter before output | “SIEM will fix later” |
| Config | Git reviewed | Live edit on nodes |
| Runtime | non-root | privileged + hostPID casual |
| Multi-tenant | Split pipelines | One `*` match all to one index without ACLs |

## Output Checklist

- [ ] Inputs/filters/outputs inventoried
- [ ] Path mounts least privilege
- [ ] Redaction rules tested with canaries
- [ ] Output TLS and auth verified
- [ ] Credentials not in git plaintext
- [ ] Agent privileges reviewed
- [ ] Metrics/alerts for pipeline health
- [ ] `code-quality-standards` applied

## Rules

- Owned logging stacks only.
- Assume logs contain secrets until redaction proves otherwise.
- Prefer deny-by-default input paths.
- Keep Fluent Bit config as reviewed code, not tribal node edits.
