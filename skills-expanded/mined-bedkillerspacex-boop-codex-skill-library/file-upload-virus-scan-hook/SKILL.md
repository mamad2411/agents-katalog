---
name: file-upload-virus-scan-hook
description: >
  Integrate antivirus or malware content scanning into upload pipelines: async worker
  hooks, quarantine buckets, ClamAV/ICAP/cloud scanners, fail modes, and user UX for
  pending/clean/infected states. Use when designing or reviewing owned upload systems
  that must scan objects before promotion or download.
---

# File Upload Virus Scan Hook

## Scope And Authorization

- **In scope:** upload pipelines and scanners you operate; lab EICAR tests.
- **Out of scope:** distributing real malware samples outside a controlled lab; scanning systems without authorization.
- Prefer EICAR (or vendor safe test files) over live malware.
- Redact object keys that encode PII; never paste scanner API keys.
- Pair worker code with `code-quality-standards`.

## When To Use

- Adding **AV/malware scan** after accept, before clean serving.
- Choosing sync vs async scan and quarantine promotion.
- Integrating ClamAV, ICAP appliances, or cloud malware APIs (e.g. bucket event → Lambda/Functions).
- Defining infected object disposal and audit logs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full upload checklist | `file-upload-security-checklist` |
| Storage keys/ACLs/domains | `file-upload-secure-storage` |
| Polyglot/XSS content issues | `file-upload-polyglot-detection` |
| Zip slip | `zip-slip-path-safety` |
| Secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Component | Role |
| --- | --- |
| Ingress | App or presigned PUT → quarantine store |
| Event | ObjectCreated / queue message / DB job row |
| Scanner | ClamAV daemon, ICAP, cloud API |
| Decision | clean / infected / error / unscannable |
| Egress | Promote to clean prefix/bucket or signed download gate |
| UX | pending state; block download until clean if policy requires |

## Fail modes

| Scanner result | Recommended default (high-risk) |
| --- | --- |
| Clean | Promote; allow download |
| Infected | Isolate/delete; alert; do not serve |
| Timeout/error | Keep quarantine; retry; **do not** fail-open to public |
| Too large / encrypted archive | Mark unscannable; policy deny or manual review |

## Workflow

### 1. Confirm scope and success criteria

1. Data risk tier; compliance needs (e.g. block until clean).
2. Success: EICAR never served; clean files available; scanner outage does not publish unscaned objects if policy forbids.
3. RPO for scan queue lag defined.

### 2. Inventory pipeline

```text
Upload → quarantine object + job → scan → tag/DB status → promote or dispose
```

1. Note timeouts, max object size, archive depth limits.
2. Credentials for scanner API in secret manager only.

### 3. Baseline with safe test file

```bash
# EICAR standard test string (safe) — create only in lab
printf '%s' 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.com
# Upload via owned API; expect infected handling
```

1. Confirm detection name logged.
2. Confirm download API returns 403/404 for infected.

### 4. Implement hook

```python
# Conceptual async worker
def handle_object_created(bucket: str, key: str) -> None:
    data = get_object(bucket, key)
    result = clamav_scan(data)  # or stream to clamd
    if result == "infected":
        tag(bucket, key, status="infected")
        quarantine_move(bucket, key)
        notify_security(key, result)
        return
    if result == "clean":
        promote_to_clean(bucket, key)
        tag(bucket, key, status="clean")
        return
    tag(bucket, key, status="error")
    schedule_retry(key)
```

```bash
# clamd example (owned host)
clamdscan --fdpass /path/to/quarantine/file
# Or clamd INSTREAM from worker
```

1. **Idempotent** workers; poison-queue after N failures.
2. Stream scan when possible to avoid double full-buffer memory spikes.
3. For cloud: event → queue → worker (avoid synchronous user request holding 60s scans when large).
4. Store scan vendor, signature version, timestamp for forensics.

### 5. Gate downloads

```python
def authorize_download(user, file_row) -> None:
    if file_row.status != "clean":
        raise Forbidden("file_not_available")
    assert_tenant_access(user, file_row)
```

1. Never expose quarantine bucket publicly.
2. Presigned GET only issued for clean objects.

### 6. Verify with evidence

| Case | Expect |
| --- | --- |
| EICAR upload | status infected; not downloadable |
| Clean PNG | status clean; downloadable |
| Scanner down | status pending/error; not downloadable if fail-closed |
| Retry after AV up | eventual clean promote |

```bash
curl -sS -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $T" \
  "https://app.example/files/$INFECTED_ID/content"
# Expect 403
```

### 7. Observe and hand off

1. Metrics: scan_latency, infected_total, queue_depth, scanner_errors.
2. Alert on scanner_errors sustained and on infected_total spikes.
3. Document signature update cadence for self-hosted ClamAV.
4. Link storage + checklist skills; apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Placement | Quarantine then scan | Serve then scan “later maybe” |
| Outage | Fail closed | Fail open public |
| Test | EICAR in lab | Real ransomware samples on prod |
| UX | Pending state clear | Infinite spinner no status |
| Secrets | Managed identity to scanner | Clam API key in repo |
| Scope | AV for malware | AV as only upload control |

## Output Checklist

- [ ] Pipeline diagram with quarantine/clean
- [ ] Scanner choice and version/signature update process
- [ ] Fail-closed policy documented
- [ ] EICAR and clean file evidence
- [ ] Download gate enforces clean status
- [ ] Retries/DLQ configured
- [ ] Metrics and alerts live
- [ ] Cross-links to storage/checklist
- [ ] `code-quality-standards` applied

## Rules

- Authorized pipelines only; use EICAR for functional tests.
- AV is necessary but not sufficient—still validate types and storage.
- Do not fail open on scanner errors for high-risk data.
- Keep this skill focused on scan hooks and promotion gates.
