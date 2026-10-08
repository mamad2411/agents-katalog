---
name: sh-kb-file-upload
description: "Knowledge base for finding unrestricted/insecure file upload - uploads that allow dangerous file types, execution in the upload dir, path control over the stored name, or missing content validation, leading to RCE, XSS, or overwrite. Use when hunting file-upload issues. CWE-434/436/616, OWASP A04/A05:2021."
---

# Unrestricted File Upload - Hunter Knowledge Base

Uploads become dangerous when the app trusts the client-provided type/name, stores files where they can be
executed or served, or skips content validation. Worst case: upload a web shell and get RCE.

## What to hunt
- **Executable upload + reachable path** (CWE-434): uploading `.php`/`.jsp`/`.aspx`/`.py` (or a bypass
  variant) into a directory the web server executes -> RCE.
- **Type/extension trust**: validating only the client `Content-Type` or extension (spoofable); no
  server-side content/magic-byte check.
- **Path control over stored name**: attacker sets the filename/path (traversal `../`, overwrite of an
  existing file, null byte, double extension `shell.php.jpg`, trailing dot/space, case tricks, NTFS
  Alternate Data Stream `shell.asp:.jpg`, or a name like `shell.p.phphp` that becomes `shell.php` after a
  single-pass, non-recursive strip of a blacklisted extension).
- **Upload-then-validate race window**: the app writes the file to a web-reachable path first and deletes
  it afterward if validation fails - an attacker who requests the file fast enough (or repeatedly re-uploads
  to widen the window) can get it executed before it's removed.
- **Content-driven XSS / SVG / HTML / polyglot**: uploading `.svg`/`.html` served inline on the app origin
  -> stored XSS; image polyglots; `.xml`-backed formats -> XXE.
- **Missing limits**: no size/rate limit -> DoS; zip-bomb; decompression bombs.
- **Metadata/EXIF or antivirus gaps**; server-side image processing (ImageMagick "ImageTragick") RCE.

## Sinks / patterns (grep targets)
Upload handlers and where they write: `request.files`, `MultipartFile`, `multer`, `formidable`,
`move_uploaded_file`, `save(`/`saveAs(`, `fs.writeFile(uploadPath)`, `os.path.join(upload_dir, filename)`,
`secure_filename` (Flask - check it's actually used), `Content-Type` checks, extension allowlist/denylist.
Also how the file is later **served** (static route over the upload dir) or **processed** (image libs).

## Detection recipe
1. `graft grep "request.files|MultipartFile|multer|move_uploaded_file|save(|writeFile|upload" --json`.
2. For each upload: How is the type validated (extension? content-type? magic bytes?). Is the stored name
   attacker-controlled? Where is it stored, and is that path executable or served inline on the app origin?
3. Trace the stored filename for traversal/overwrite; check size/count limits.

## Payloads / PoC
- Web shell: `shell.php` with `<?php system($_GET['c']); ?>` if PHP execution reachable; `.jsp`/`.aspx` equiv.
- Bypasses: double extension `shell.php.jpg`, null byte `shell.php%00.jpg`, case `shell.PhP`, trailing
  dot/space `shell.php.`, spoofed `Content-Type: image/png` with PHP body, magic-byte prefix + code,
  alternative interpreter extensions often missing from blacklists (`.phtml`, `.php5`, `.pht`, `.shtml`,
  `.asp;.aspx`), URL-encoded extension `exploit%2Ephp`, polyglot image+payload files (e.g. built with
  ExifTool) that pass magic-byte/dimension checks.
- Stored XSS: upload `poc.svg` containing `<script>...</script>` or `poc.html`, served inline.
- Traversal/overwrite: filename `../../app/config.py` (zip-slip for archives).
- PoC: upload the file, then request its served URL and observe execution/script/overwrite.

## False-positive filters
- Server-side **content** validation (magic bytes / re-encode image) **and** an extension **allowlist**
  (not denylist), with a server-generated random stored name (client name discarded).
- Uploads stored outside the webroot / on object storage with `Content-Disposition: attachment` and a
  non-executing content-type, served from a separate origin/domain.
- Size/count/rate limits enforced; archives validated before extraction.
- Validation happens **before** the file is written to any web-reachable path (no upload-then-delete-on-fail
  race window).
- Per-directory config overrides disabled (Apache `AllowOverride None`, IIS handler mappings locked) so a
  smuggled `.htaccess`/`web.config` in the upload dir can't grant execution; on Windows, 8.3 short-filename
  generation disabled (`fsutil behavior set disable8dot3 1`) so a blocked long name can't be reached via its
  short alias.

## CWE / OWASP / severity
CWE-434 (unrestricted upload), CWE-436 (interpretation conflict), CWE-616. OWASP A04/A05:2021.
Upload->RCE -> **critical**; stored XSS via upload -> high; overwrite/DoS -> per impact.

## Chaining hints
Upload web shell -> RCE -> `secrets`/lateral (chain terminus); SVG/HTML upload -> stored `xss` -> admin
takeover; filename control -> `path-traversal` overwrite; XML-backed upload -> `xxe`; feeds `injection`
(processing the file with a shell).

## Mitigation
Allowlist expected extensions **and** validate content (magic bytes / re-encode images) *before* the file
touches any web-reachable path; discard the client filename and generate a random server-side name; store
outside the webroot or on object storage served from a separate origin with `Content-Disposition: attachment`
and a safe content-type; disable per-directory config overrides and short-filename generation; enforce
size/count/rate limits; scan for malware; keep image-processing libraries patched.
