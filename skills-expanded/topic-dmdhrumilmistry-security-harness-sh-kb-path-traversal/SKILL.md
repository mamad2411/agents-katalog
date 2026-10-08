---
name: sh-kb-path-traversal
description: "Knowledge base for finding path/directory traversal and local/remote file inclusion - user-controlled paths reaching filesystem or include operations, enabling arbitrary file read/write or code inclusion. Use when hunting traversal/LFI/RFI. CWE-22/23/98, OWASP A01:2021-Broken Access Control."
---

# Path Traversal & File Inclusion - Hunter Knowledge Base

User-controlled path components reach a filesystem operation without being confined to an intended base
directory, letting an attacker read/write files outside it (`../../etc/passwd`) or include/execute files.

## Sources
Filenames/paths in request params/body/headers, upload filenames, `Content-Disposition`, archive entry
names (zip-slip), template/view names, download/attachment ids that map to paths.

## Sinks (grep targets)
- **Read/write**: `open(`, `readFile`/`readFileSync`, `fs.createReadStream`, `sendFile`/`send_file`,
  `res.download`, `File(`/`FileInputStream`, `Files.newInputStream`, `os.path.join(base, user)`,
  `path.join`/`path.resolve` with user input, `io.readfile`, PHP `file_get_contents`/`fopen`/`readfile`.
- **Include/execute (LFI/RFI)**: PHP `include`/`require`/`include_once` with user input, `virtual()`;
  template engines resolving user-supplied view names; dynamic `import`/`require(userPath)`.
- **Archive extraction (zip-slip)**: extracting entry names without normalizing (`ZipFile.extractall`,
  `tar.extractall`, `unzip`).

## Detection recipe
1. `graft grep "open\(|readFile|sendFile|send_file|path.join|os.path.join|include\(|require\(|extractall" --json`.
2. Trace the path argument to an untrusted source.
3. Check for confinement: canonicalize (`realpath`) then verify the result starts with the intended base;
   reject `..`, absolute paths, null bytes, and encoded variants. Absence of this after user input -> flag.

## Payloads / PoC
- `../../../../etc/passwd`, `..\..\..\..\windows\win.ini` (Windows), `....//....//` (filter bypass),
  URL-encoded `%2e%2e%2f`, double-encoded `%252e%252e%252f`, null byte `%00`, absolute `/etc/passwd`.
- LFI to RCE: include a log/upload/`/proc/self/environ` file containing attacker code; PHP wrappers
  `php://filter/convert.base64-encode/resource=index.php` (source disclosure), `data://`, `expect://`.
- Zip-slip: an archive entry named `../../app/config.py` overwriting a real file.
- PoC: request a file outside the base and confirm its contents return.

## False-positive filters
- Path is canonicalized and confined: `realpath`/`Path.resolve` then a base-prefix check (`startswith(base)`),
  or the framework's safe static-file handler with traversal protection (e.g. `send_from_directory`).
- Only a **basename** is used (`os.path.basename(user)`) against a fixed directory, with no `..` reachable.
- The identifier is an opaque id mapped through a DB/allowlist to a server-chosen path (user never supplies path).

## CWE / OWASP / severity
CWE-22 (traversal), CWE-23, CWE-98 (RFI), CWE-73 (external control of filename). OWASP A01:2021.
Arbitrary file read of secrets/config -> **high/critical**; write or LFI->RCE -> **critical**.

## Chaining hints
File read -> `secrets` (config/keys/`.env`) -> DB/cloud access; LFI + log poisoning -> RCE; zip-slip write ->
overwrite code/config -> RCE; feeds `access-control` (read other tenants' files).

## Mitigation
Don't build filesystem paths from user input. Map opaque ids to server-controlled paths; if a name is
needed, take only the basename, canonicalize, and enforce a base-directory prefix check; reject `..`,
absolute paths, and encoded traversal; validate archive entry names before extraction; never `include`
user-controlled paths.
