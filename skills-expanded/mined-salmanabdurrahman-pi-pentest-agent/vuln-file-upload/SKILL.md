---
name: vuln-file-upload
description: File upload vulnerability validation — test extension, MIME, and magic-byte bypass with inert probe files; confirm RCE via safe canary execution only when scope explicitly authorizes it.
disable-model-invocation: true
risk: destructive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# File upload — upload-filter bypass validation

Use this skill to validate file upload vulnerabilities on an authorized, in-scope target. Test server-side upload restrictions — extension blocklists, MIME-type validation, magic-byte checks, and content inspection — using inert probe files. Confirm bypass by uploading a file that the server should reject but accepts. Only upload functional webshells or script files when scope explicitly authorizes RCE validation and destructive-risk approval is obtained.

## Required inputs

- Written scope naming the target, authorized upload endpoints, and explicit permission for upload filter bypass testing. Separate explicit permission required for webshell upload, code execution confirmation, or stored-XSS via upload.
- Valid authorization cache. Destructive risk class: webshell upload is RCE and requires maintainer approval before any functional script is uploaded.
- Test file corpus: a small inert text file, a minimal valid image (1×1 PNG with correct magic bytes), and an inert probe file with a harmless content payload.
- Known upload directory and file-serving behavior: does the server return uploaded files under a predictable path? Can uploaded files be accessed directly?
- Known file-processing pipeline (ImageMagick, Ghostscript, ffmpeg, ExifTool) if the server processes uploaded files — processing introduces separate vulnerabilities.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any upload.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution with destructive-risk approval — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — baseline upload behavior

Map the upload endpoint's normal behavior before attempting bypass:
1. Upload a legitimate file (e.g., a 1×1 PNG image) through the normal application flow.
2. Record: the upload URL, HTTP method, required headers (Content-Type, Authorization, CSRF token), form field name, and any additional POST parameters.
3. Observe the response: does it return the uploaded file's URL, an ID, or a download endpoint?
4. Access the uploaded file at its served URL. Does it render inline, force download, or return with a specific Content-Type?
5. Note any file-renaming behavior: is the original filename preserved, sanitized, or replaced with a UUID?

### Phase 2 — extension blocklist bypass

Test which file extensions the server accepts and which are blocked:

```text
Probe extensions (non-malicious content, just filename variation):
Baseline:  test.jpg, test.png, test.gif, test.pdf     — expected allowed
Blocked:   test.php, test.jsp, test.asp, test.aspx      — expected blocked
Bypass:    test.php5, test.phtml, test.phar, test.pht   — alternative PHP handlers
           test.php.jpg, test.jpg.php                     — double extension
           test.PHP, test.PhP, test.pHp                   — case variation
           test.php%00.jpg                                — null byte (legacy)
           test.php%0d%0a.jpg                             — CRLF injection
           test.php/.jpg                                  — path traversal
```

For each probe:
1. Upload a file with the target extension. File content is always the inert probe — never a functional script at this stage.
2. Record whether the upload succeeds (200/201), is rejected (400/403/415), or silently renamed.
3. If any non-standard extension is accepted → extension bypass confirmed.

### Phase 3 — MIME-type bypass

When extension checks are in place, the server may validate the `Content-Type` header instead:

```text
Probe MIME types (file content is still inert probe):
image/jpeg
image/png
image/gif
application/octet-stream
text/plain
```

1. Upload a file named `test.php` but with `Content-Type: image/jpeg`.
2. If the server accepts based on MIME type and ignores the extension → MIME-type bypass confirmed.
3. Test `Content-Type: application/octet-stream` — many servers accept this as a generic fallback.

### Phase 4 — magic-byte bypass

When both extension and MIME-type checks are enforced, the server may verify file magic bytes:

```text
Bypass techniques:
1. Prepend magic bytes to a script file:
   GIF89a + <?php system($_GET['cmd']); ?>  →  test.gif.php
   \xFF\xD8\xFF\xE0 + script content        →  test.jpg.php
   \x89PNG\r\n\x1a\n + script content        →  test.png.php

2. Polyglot files (valid image + valid script):
   Create a valid GIF/JPEG/PNG that also parses as PHP/ASP. The file renders as
   an image when accessed directly but executes as code when included or
   processed by a PHP/ASP handler.
```

Rules:
- Only upload files with inert script content (`<?php echo 'UPLOAD-PROBE-' . date('Ymd'); ?>`) until destructive-risk approval is obtained.
- If a bypass file is accepted, record the bypass technique and the served file URL.
- Do not access the uploaded script file (execute it) until Phase 5 approval.

### Phase 5 — execution confirmation

**Requires destructive-risk maintainer approval. Do not proceed without it.**

When a bypass file has been uploaded:
1. Access the file at its served URL with a benign query parameter: `uploaded.php?cmd=id` → if `uid=` or user information appears in the response, code execution is confirmed.
2. If the file is not directly accessible, test whether it is included elsewhere (LFI via path traversal, include in template, background processing).
3. Confirm execution with a single `id` or `whoami` command only. Do not explore the filesystem, list processes, or open network connections.
4. After confirmation, immediately delete the uploaded file through the application (if a delete function exists) or record the file location for the target's cleanup.

Alternative execution contexts:
- **SVG XSS**: upload `<svg><script>console.log('UPLOAD-XSS')</script></svg>` as `test.svg`. If the SVG is served inline and script executes → stored XSS via file upload.
- **.htaccess upload**: upload a `.htaccess` file with `AddType application/x-httpd-php .jpg` to make `.jpg` files execute as PHP. Apache-only.
- **Server-side includes**: upload `.shtml` or `.stm` files if SSI is enabled.

### Phase 6 — file-processing pipeline risk

If the server processes uploaded files (image resizing, PDF conversion, metadata extraction), test:
- **ImageTragick (CVE-2016-3714)**: SVG/MVG files with shell command injection in ImageMagick.
- **Ghostscript RCE**: malicious PostScript/EPS files.
- **ExifTool RCE (CVE-2021-22204)**: crafted DjVu metadata.
- **ffmpeg SSRF**: M3U8/HLS playlist with external URLs.

These are distinct vulnerability classes. Test only if scope explicitly authorizes file-processing attacks. When not in scope, note the processing pipeline and recommend separate assessment.

## Decision points

- **Stop at extension bypass without execution**: if a non-standard extension is accepted but the file is not served as code (returned as `Content-Type: text/plain`, not executed), the finding is "insufficient upload filtering" — medium severity. Do not escalate to webshell without approval.
- **Escalate on code execution**: if a bypass file executes and returns command output → RCE confirmed, critical severity.
- **Escalate on .htaccess upload**: ability to upload `.htaccess` means server configuration can be modified → critical.
- **Downgrade on content-disposition**: if all uploaded files are served with `Content-Disposition: attachment`, script execution may be blocked. Check if the `attachment` header can be bypassed via path tricks.

## Prohibited behavior

- Uploading webshells, reverse shells, or persistent backdoors without explicit destructive-risk approval.
- Uploading files that overwrite existing application files, configuration, or `.htaccess` unless scope authorizes.
- Uploading files with malicious content targeting other users (stored XSS payloads, CSRF triggers, redirect scripts).
- Deleting, moving, or modifying other users' uploaded files.
- Using file upload as a pivot point to access the server filesystem beyond the upload directory.
- Uploading files larger than the scope-defined limit or that could cause denial of service (zip bombs, billion-laughs XML).

## Stop conditions

- Extension bypass confirmed + file served as code + `id` executes → RCE confirmed, critical finding, stop.
- Extension bypass confirmed but file not executed → medium finding, stop testing that endpoint.
- All bypass attempts consistently blocked → negative result, document server protections.
- WAF blocks all non-image uploads → protected, document WAF posture.
- Rate limiting, account lockout, or detection-team contact.

## Evidence — upload bypass matrix

For each tested endpoint, record:

```text
Upload endpoint: <URL>
Baseline allowed extensions: <jpg | png | gif | pdf | ...>
Blocked extensions tested: <php | php5 | phtml | phar | ...>
Bypass technique: <extension variation | MIME mismatch | magic-byte prepend | none>
Accepted bypass extension: <extension that passed filter>
File served URL: <URL of uploaded probe file>
Content-Type when served: <image/jpeg | text/html | application/octet-stream | ...>
Execution confirmed: <yes | no | not tested (no destructive approval)>
Command executed: <id | whoami | not applicable>
Impact: <none | insufficient filtering | RCE confirmed via upload>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into an endpoint × bypass-technique matrix. Never store: functional webshell files, uploaded files containing backdoors or reverse shells, `.htaccess` files with permissive rules, or SVG/script files with active stored-XSS payloads.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, bypass technique, CVSS estimate (5.3–6.5 for insufficient filtering without execution, 9.0–10.0 for confirmed RCE via upload), and remediation guidance.
2. Reference the upload bypass matrix.
3. Recommend: extension allowlist (only explicitly permitted extensions), MIME-type validation in combination with extension check, magic-byte validation (not as sole check — can be bypassed), store uploaded files outside web root, serve uploaded files with `Content-Disposition: attachment` and non-executable Content-Type, never include user-controlled filenames in server-side include/exec calls, scan uploaded files with antivirus, and run file-upload security tests in CI with benign payloads.
