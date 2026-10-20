---
name: file-upload-security-checklist
description: >
  End-to-end secure file upload checklist: authentication, authorize, size/type limits,
  magic-byte checks, storage isolation, malware scan hooks, safe serving headers, and
  processing sandboxing. Use when implementing or reviewing upload features on owned
  applications, or as the primary routing skill before deeper polyglot/storage/AV skills.
---

# File Upload Security Checklist

## Scope And Authorization

- **In scope:** upload features on systems you own or are authorized to assess.
- **Out of scope:** uploading malware to third-party services or weapons testing without a lab.
- Use synthetic files in non-prod; redact customer content.
- Pair code changes with `code-quality-standards`.

## When To Use

- New or legacy **multipart/form-data** or presigned upload flows.
- Security review of avatar, attachment, import, or media pipelines.
- Need a single ordered checklist covering auth → validate → store → serve → process.
- Routing into specialized upload skills after gaps identified.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Polyglot-focused detection | `file-upload-polyglot-detection` |
| Bucket/key/domain storage design depth | `file-upload-secure-storage` |
| AV/async scan workers | `file-upload-virus-scan-hook` |
| Zip/tar extract path safety | `zip-slip-path-safety` |
| Arbitrary file read outside uploads | `file-access-vuln` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Stage | Controls |
| --- | --- |
| AuthN/Z | Login required; tenant quota; role can upload? |
| Transport | TLS; CSRF on cookie session forms |
| Validate | Size, count, extension allowlist, magic bytes, optionally active content strip |
| Store | Random keys; private; encrypt; quarantine |
| Scan | AV/YARA async; block until clean if high risk |
| Serve | nosniff; correct type; attachment; separate domain |
| Process | Sandbox thumbnails/office converters |

## Master checklist

### A. Product & abuse model

- [ ] Who may upload? Rate limits per user/IP?
- [ ] Max size and daily quota?
- [ ] Allowed media types (business-justified allowlist, not denylist)?
- [ ] Are files shared cross-tenant or public?

### B. Application validation

- [ ] Authenticated endpoint; CSRF protected if cookie auth
- [ ] Enforce size before full buffering (stream limits)
- [ ] Allowlist extensions **and** detected MIME/magic
- [ ] Reject double extensions / NUL / path characters in filename
- [ ] Server generates storage key; user filename only as metadata (sanitized)

### C. Storage & IAM

- [ ] Private objects; no public ACL
- [ ] Encryption at rest; least-privilege roles
- [ ] Quarantine vs clean separation if scanning
- [ ] See `file-upload-secure-storage`

### D. Malware & content risk

- [ ] AV or content inspection hook (`file-upload-virus-scan-hook`)
- [ ] Polyglot/re-encode strategy (`file-upload-polyglot-detection`)
- [ ] Block executable and server-side script types entirely

### E. Serving & browsers

- [ ] `X-Content-Type-Options: nosniff`
- [ ] Fixed Content-Type from allowlist map
- [ ] `Content-Disposition: attachment` when inline view not required
- [ ] Cookie-less file host for user content
- [ ] CSP on app origin does not need to trust upload origin scripts

### F. Downstream processing

- [ ] Image/video transcoder sandboxed, resource-limited
- [ ] Archive extract uses `zip-slip-path-safety`
- [ ] No privileged network from converters (SSRF risk)

## Workflow

### 1. Confirm scope and success criteria

1. Inventory all upload entry points (API, web, mobile, presign).
2. Success: checklist complete with evidence links; critical gaps ticketed.
3. Data classification sets how strict “block until scanned” is.

### 2. Walk each entry point

```text
Client → (AuthZ) → Size/type gates → Magic/MIME → Store quarantine
      → Scan/re-encode → Promote clean → Authorized download/serve
```

1. Capture request samples (redacted) and response headers on download.
2. Note async vs sync scan UX.

### 3. Test core bypasses (authorized lab)

```bash
# Oversized
# Wrong type with spoofed Content-Type
# Pathful filename ../../evil
# Double extension shell.php.jpg
# Empty or truncated magic
```

1. Record accept/reject matrix.
2. Confirm storage key not client-controlled path.

### 4. Close gaps

1. Apply missing controls from checklist sections B–F.
2. Prefer allowlists and re-encoding over endless blacklists.
3. Document intentional exceptions (e.g. internal trusted bulk import).

### 5. Verify with evidence

| Test | Expect |
| --- | --- |
| Unauth upload | 401/403 |
| Oversize | 413/400 |
| Disallowed type | 400 |
| Valid small PNG | 201 + private object |
| GET other tenant file | 403 |
| Download headers | nosniff + safe type |

### 6. Observe and harden

1. Metrics: upload failures by reason; scan queue lag.
2. Alert on spike of rejected magic mismatches (probing).
3. Re-run checklist on each new upload feature in PR template.

### 7. Hand off

1. Completed checklist with owners and dates.
2. Deep-dives linked to specialized skills.
3. Apply `code-quality-standards` for shipped code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Types | Allowlist images/pdf | Block `.exe` only |
| Filename | Metadata only | Saved as webroot name |
| Scan | Quarantine first | Serve immediately always |
| Headers | nosniff + attachment | Inline HTML from uploads |
| Auth | Per-tenant quota | Open anonymous unlimited |
| Proof | Matrix of tests | “We use Cloudinary so safe” without review |

## Output Checklist

- [ ] All upload entry points listed
- [ ] Sections A–F evaluated with evidence
- [ ] Critical gaps ticketed with severity
- [ ] Storage and serving model documented
- [ ] Specialized skills invoked where needed
- [ ] Regression tests for reject paths
- [ ] Metrics/alerts considered
- [ ] `code-quality-standards` applied

## Rules

- Authorized testing only; no real malware on shared infra without isolation.
- Checklists without evidence are incomplete—attach commands/results (redacted).
- This skill is the orchestration umbrella; do not ignore specialized polyglot/storage/AV runbooks.
- Fail closed on unknown types for high-risk apps.
