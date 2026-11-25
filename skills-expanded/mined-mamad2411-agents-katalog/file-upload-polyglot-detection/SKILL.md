---
name: file-upload-polyglot-detection
description: >
  Detect and defend against polyglot uploads (JPEG+JS, GIF+HTML, PDF+ZIP, phar, etc.)
  that bypass naive MIME or extension checks. Use when hardening upload pipelines,
  building content inspection, reviewing thumbnail/parser risks, or testing owned apps
  for double-format files that execute or smuggle payloads across trust boundaries.
---

# File Upload Polyglot Detection

## Scope And Authorization

- **In scope:** upload features you own or are authorized to test; synthetic polyglots in labs.
- **Out of scope:** distributing malware, uploading polyglots to third-party services without permission.
- Store research polyglots in isolated lab storage; do not email them to unprepared inboxes.
- Redact customer uploads from reports.
- Pair pipeline code with `code-quality-standards`.

## When To Use

- Upload acceptance based only on **extension or Content-Type**.
- CDN/static hosting that serves user content with dangerous MIME sniffing.
- Image/PDF parsers that might interpret embedded secondary formats.
- Building defense: magic-byte validation, re-encoding, content disposition, sandboxing.
- Investigating “valid image still XSS” or “PDF still ZIP” reports.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full upload checklist (size, auth, storage) | `file-upload-security-checklist` |
| Secure storage layout / bucket policies | `file-upload-secure-storage` |
| AV/malware scanning hooks | `file-upload-virus-scan-hook` |
| Zip slip on extract | `zip-slip-path-safety` |
| Classic XSS without uploads | `xss-cross-site-scripting` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Polyglot class | Risk |
| --- | --- |
| Image + HTML/JS | Stored XSS if served as HTML or sniffed |
| Image + script (PHP/JSP) | RCE if parsed by app server in webroot |
| PDF + JS / PDF + ZIP | Reader or pipeline confusion |
| ZIP + other | Bypass filters; later extract path issues |
| Polyglot media containers | Transcoder bugs / memory corruption (separate fuzz skills) |

## Detection signals

| Check | Good signal | Weak signal |
| --- | --- | --- |
| Magic bytes | Match declared type at offset 0 (and containers) | Trust `Content-Type` header only |
| Re-encode | ImageMagick/libvips decode→encode strip extras | Store original bytes as-is on web origin |
| MIME lib | libmagic / filetype sniff both claim types | Extension map only |
| Serve headers | `Content-Type` fixed; `X-Content-Type-Options: nosniff` | Inline HTML allowed from upload domain |
| Structure parse | Full format parser fails closed | Regex on first bytes only |

## Workflow

### 1. Confirm scope and success criteria

1. Map upload → storage → serving path (same origin vs cookie-less CDN).
2. Success: polyglot lab files rejected or neutralized (re-encoded); serving cannot execute secondary format.
3. Authorization for any active upload tests recorded.

### 2. Inventory pipeline

1. Validation steps order: auth → size → extension → MIME → AV → store.
2. Where files are served from and with which `Content-Type` / `Content-Disposition`.
3. Which processors parse files (thumbnails, antivirus, office converters).

### 3. Baseline polyglot tests (lab samples only)

```bash
# Example idea — craft/test only in lab; do not use against unauthorized hosts
# 1) Upload JPEG that also contains HTML comment/script payload variants per research notes
# 2) Observe stored Content-Type and browser interpretation on download URL
# 3) Upload file with double extension report.pdf.html if filter is naive
```

1. Record accept/reject and final response headers on GET of uploaded object.
2. Test browser MIME sniffing with and without `nosniff`.

### 4. Apply defenses

```python
import imghdr  # illustrative; prefer robust libs (filetype, pillow re-encode)
from pathlib import Path

ALLOWED = {"image/jpeg": b"\xff\xd8\xff", "image/png": b"\x89PNG\r\n\x1a\n"}

def assert_magic(data: bytes, declared: str) -> None:
    magic = ALLOWED.get(declared)
    if not magic or not data.startswith(magic):
        raise ValueError("magic_mismatch")

def neutralize_image(data: bytes) -> bytes:
    # Decode with Pillow and re-save as JPEG/PNG to drop appended payloads
    from io import BytesIO
    from PIL import Image
    im = Image.open(BytesIO(data))
    im = im.convert("RGB")
    out = BytesIO()
    im.save(out, format="JPEG", quality=90)
    return out.getvalue()
```

1. **Re-encode** images/audio when possible; do not serve raw user bytes from trusted origins.
2. Force `Content-Disposition: attachment` for untrusted types; separate **file domain** without cookies/session.
3. Set `X-Content-Type-Options: nosniff` and exact Content-Type from server map—not client.
4. Reject ambiguous libmagic results (e.g. multiple matches) when policy is strict.
5. Never store uploads under executable webroot; no script handlers on upload buckets.

### 5. Verify with evidence

```bash
curl -sS -D - -o /dev/null "https://files.example/u/lab-polyglot.jpg" | grep -iE 'content-type|content-disposition|x-content-type'
# Expect image/jpeg + nosniff (+ attachment if policy)
```

1. After re-encode, appended script bytes gone (hash/size change expected).
2. Attempted `evil.php.jpg` not executable as PHP.

### 6. Observe and harden

1. Metrics: magic_mismatch rejects, re-encode failures.
2. Quarantine bucket for failed inspection.
3. Keep polyglot research corpus versioned for regression tests (isolated).

### 7. Hand off

1. Document accepted types and neutralization method per type.
2. Link storage skill for bucket policy; AV skill for malware.
3. Apply `code-quality-standards` for inspection workers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Validation | Magic + re-encode + type allowlist | Extension only |
| Serving | Cookie-less domain + nosniff | Same site session origin inline |
| Ambiguity | Reject dual identity files | “It’s a JPEG so OK” |
| Processors | Sandbox converters | Privileged desktop Word on uploads |
| Evidence | Header + neutralized hash | Screenshot of upload success only |

## Output Checklist

- [ ] Upload→store→serve path documented
- [ ] Lab polyglot cases tested under authorization
- [ ] Magic/MIME/re-encode controls applied
- [ ] Response headers verified (type, nosniff, disposition)
- [ ] No executable webroot storage
- [ ] Regression corpus for polyglots (lab)
- [ ] Cross-links to checklist/storage/AV skills
- [ ] `code-quality-standards` applied

## Rules

- Authorized lab polyglots only; do not weaponize against third parties.
- Detection without safe serving still fails—fix both.
- Prefer neutralization (re-encode) over signature blacklists alone.
- Route general upload policy to `file-upload-security-checklist`; keep this skill on polyglot detection/defense.
