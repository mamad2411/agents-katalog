---
name: file-upload-secure-storage
description: >
  Design and review secure storage for user file uploads: random object keys, cookie-less
  separate domain, content-type enforcement, size quotas, non-executable permissions, and
  presigned PUT policies. Use when implementing or auditing upload landing zones, object-store
  keys, disk mounts, or hardening post-accept storage for owned apps and authorized assessments.
---

# File Upload Secure Storage

## Scope And Authorization

- **In scope:** storage backends and apps you own (S3/GCS/Azure Blob, NFS, local disk), authorized reviews.
- **Out of scope:** accessing other tenants’ buckets or production customer objects without need.
- Prefer staging buckets for tests; never make real PII public for “proof.”
- Redact presigned URLs and access keys from tickets.
- Pair IaC/app changes with `code-quality-standards`.

## When To Use

- Designing **where and how** accepted uploads live after validation.
- Fixing public ACLs, guessable keys, or same-origin hosting of user content.
- Presigned upload/download URL policies (expiry, content-length, content-type).
- Separating quarantine vs clean buckets and encryption settings.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| End-to-end upload security checklist | `file-upload-security-checklist` |
| Polyglot detection / re-encode | `file-upload-polyglot-detection` |
| AV scan integration | `file-upload-virus-scan-hook` |
| Path traversal / AFR | `file-access-vuln` / `path-traversal-lfi` |
| Zip slip extract | `zip-slip-path-safety` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concern | Guidance |
| --- | --- |
| Key design | Unpredictable object keys (UUIDv4/ULID); never user filename as sole key |
| ACL | Private by default; no public-read on raw uploads |
| Serving | Cookie-less file domain or signed GET; not session origin |
| Encryption | SSE-S3/SSE-KMS or equivalent; restrict KMS key users |
| Execution | No script execution on storage (bucket website carefully; no webroot PHP) |
| Quotas | Per-user size/count limits; lifecycle delete |

## Storage layout patterns

| Pattern | Use |
| --- | --- |
| `uploads/{tenant}/{yyyy}/{uuid}` | Multi-tenant isolation prefix |
| `quarantine/{uuid}` → `clean/{uuid}` | After AV/inspection promote |
| Presigned PUT to quarantine only | Browser never talks to clean bucket with write |
| Separate account/project for files | Blast-radius limit |

## Workflow

### 1. Confirm scope and success criteria

1. Record cloud/disk backend, tenants, data classes, retention.
2. Success: objects private; keys unguessable; downloads authorized; no XSS via same-site session cookies on file host.
3. Owners for KMS keys and bucket policies named.

### 2. Inventory current storage

```bash
# Examples — owned env only
aws s3api get-bucket-acl --bucket YOUR_BUCKET
aws s3api get-bucket-policy --bucket YOUR_BUCKET
gsutil iam get gs://YOUR_BUCKET
# Local
find /var/app/uploads -maxdepth 2 -type d
```

1. Check public access blocks, website hosting, CORS on buckets.
2. Sample object keys for predictability (`user/report.pdf` vs random).
3. Map who can `s3:PutObject` / `GetObject` / `ListBucket`.

### 3. Baseline abuse cases (authorized)

1. Guess sequential keys if any.
2. Upload then request via main app origin vs file domain—note cookie sending.
3. Check if listing bucket is possible anonymously.

### 4. Apply secure storage design

```text
# Presigned PUT constraints (conceptual)
# - expire 5–15 minutes
# - exact Content-Type allowlist
# - content-length-range min/max
# - key prefix forced server-side (not client-chosen path escape)
```

```python
import uuid
from pathlib import PurePosixPath

def object_key(tenant_id: str, original_name: str) -> str:
    # Keep extension only if allowlisted; never trust full filename path
    ext = PurePosixPath(original_name).suffix.lower()
    if ext not in {".jpg", ".png", ".pdf"}:
        ext = ""
    return f"{tenant_id}/{uuid.uuid4().hex}{ext}"
```

```nginx
# Cookie-less file vhost sketch
server {
  server_name files.example.com;
  # no session cookies set here
  add_header X-Content-Type-Options nosniff always;
  # root proxy to object store or local clean volume
}
```

1. Block public ACLs; enable account-level public access block where applicable.
2. Encrypt with KMS; least-privilege app roles (no `s3:*` on `*`).
3. Lifecycle rules: abort incomplete multipart; expire quarantine rejects.
4. Disk: mount `noexec,nodev,nosuid` when applicable; app user-only permissions.

### 5. Verify with evidence

```bash
# Anonymous get should fail
curl -sS -o /dev/null -w "%{http_code}\n" "https://BUCKET.s3.amazonaws.com/guessable-key"
# Authorized signed URL works briefly then expires
```

1. Confirm main site cookies not sent to file host (different site).
2. Confirm user A cannot GET user B object without authz check.

### 6. Observe and harden

1. Access logs on bucket; alert on ListBucket from unexpected principals.
2. Metrics: presign issue rate, 403 download rate.
3. Periodic public exposure scan (owned).

### 7. Hand off

1. Diagram quarantine→clean; IAM matrix; key format.
2. Link checklist and AV skills for pre-storage steps.
3. Apply `code-quality-standards` for signing code/IaC.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | Random per object | `/uploads/{username}/{filename}` only |
| ACL | Private + signed GET | Public-read “so email works” |
| Domain | files.example without cookies | /media on app.example session |
| IAM | Prefix-scoped roles | Admin keys in web pods |
| Disk | noexec volume | Webroot world-writable |
| CORS | Tight methods/origins | `*` with credentials confusion |

## Output Checklist

- [ ] Backend, tenants, encryption documented
- [ ] Key scheme unguessable; path traversal impossible
- [ ] Public access disabled; verified
- [ ] Serving domain and headers reviewed
- [ ] Presign constraints (type/size/TTL) enforced
- [ ] Quarantine/clean promotion path defined
- [ ] IAM least privilege evidenced
- [ ] Logging/alerts for anomalous access
- [ ] `code-quality-standards` applied

## Rules

- Owned storage only; minimize exposure of real user files during tests.
- Storage security does not replace upload validation—compose with checklist/polyglot/AV skills.
- Never commit long-lived cloud keys; prefer instance roles/OIDC.
- Treat listable buckets as critical findings.
