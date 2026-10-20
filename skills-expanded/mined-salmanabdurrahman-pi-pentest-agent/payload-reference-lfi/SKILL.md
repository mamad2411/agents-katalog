---
name: payload-reference-lfi
description: Local File Inclusion reference framework — defensive payload taxonomy organized by parser context, traversal depth, encoding bypass, wrapper chains, and log/session poisoning vectors. Safe canaries and inert marker strategy for minimal-proof validation handoff through executor gates.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [reference-notes, validation-plan, safe-canary-log, redaction-decision]
---

# Payload Reference LFI

Use this skill as a defensive reference framework for Local File Inclusion assessment. Organize payload knowledge by parser context, traversal depth, encoding bypass strategy, and wrapper chains. Every payload discussion maps to a safe canary or inert marker approach for minimal-proof validation — validation that proves the inclusion path exists without reading sensitive files, extracting data, or escalating to code execution. This skill is a reference and triage aid. It never provides active exploitation runbooks. All active validation routes through `pentest_agent_execute_tool` with authorization, scope, and approval gates.

## Required inputs

- Parser context: the include mechanism (PHP `include`/`require`, JSP `include`, SSI `<!--#include-->`, template engine `{% include %}`, Node.js `fs.readFile` with user-controlled path, Python `open()` with user path, or server-side fetch/proxy that follows file:// URIs).
- Affected parameter, request shape, encoding context, and any existing WAF/filter observations.
- Target and scope file when any live system, route, hostname, or account is mentioned.
- Authorization cache and allowed method before target contact.
- Desired output: validation plan, safe canary design, report note, triage decision, or redaction guidance.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` to confirm local policy and disabled-category posture.
2. `pentest_agent_parse_scope` when target context exists.
3. `pentest_agent_validate_target` before any live URL, host, API, or account is contacted.
4. `pentest_agent_check_authorization` before active validation.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for all active checks; never switch to raw shell for convenience.
6. `pentest_agent_append_evidence` for redacted notes when reference output informs engagement state.

## Defensive payload taxonomy

### Category 1 — traversal depth discovery (safe canaries)

Goal: confirm inclusion of a known-safe local resource to establish traversal depth and root position before considering target files.

**Safe canary files** (readable without sensitive content):
- `/etc/hostname` — single-line hostname, no credentials, safe to disclose in most scopes.
- `/proc/self/cmdline` — the current process command line; reveals binary path, useful for confirming traversal reached process view.
- `/proc/self/status` — process status including PID, UID, and memory limits; no credentials.
- `/etc/issue` — OS banner, no sensitive data.
- `C:\Windows\win.ini` — Windows version marker, benign.

**Depth ladder approach**: start with `../etc/hostname`, increase depth (`../../`, `../../../`, etc.) until the canary returns, then record the depth. This reveals the working directory position without touching sensitive files.

**Inert markers**: use parameter-specific canaries where the inclusion result is observable but harmless — DNS canary (`nslookup <unique>.your-burp-collaborator`), HTTP canary (include a local file that triggers a distinguishable output without data leakage), or a timing canary (include `/dev/zero` which may hang, indicating read access without data return).

### Category 2 — path truncation and encoding bypass

Goal: understand how the parser resolves paths and what encoding transformations bypass filters.

**Null-byte truncation** (historical, PHP < 5.3.4): `../../../etc/passwd%00.html` — the null byte terminates the PHP string at the C level before the appended extension. Modern PHP (5.3.4+) ignores null bytes; this vector is only relevant for very old targets.

**Path truncation via length** (historical, PHP < 5.2.8): `../../../etc/passwd/././././.` repeated to ~4096 characters — PHP's `realpath()` would truncate the path to MAXPATHLEN, dropping the appended extension. Modern PHP rejects excessively long paths.

**Double encoding**: `..%252f..%252f` — when the server URL-decodes input once and the include function decodes again, `%252f` becomes `%2f` then `/`. Test single-step encoding first, then double-encoding if WAF blocks literal `../`.

**Unicode/UTF-8 overlong sequences**: `..%c0%ae..%c0%ae` — overlong encoding of `/` (0x2F as %c0%ae) may bypass naive filters that check for literal `../` but miss overlong UTF-8 representations. Modern frameworks and WAFs typically normalize UTF-8 before filtering, but older or custom implementations may be vulnerable.

**Nested path separators**: `....//....//` — some filter implementations normalize `....//` to `../` after stripping `../`, creating a bypass. Test when `../` is explicitly blocked but no recursive normalization is applied.

**Path injection via wrapper**: `php://filter/convert.base64-encode/resource=index` — uses the `php://` stream wrapper to read a local PHP file, Base64-encoding the output to avoid PHP execution. This is the preferred safe canary for PHP targets: read `index.php` as Base64 to confirm LFI without risking code execution.

### Category 3 — PHP wrapper chains

Goal: understand the PHP stream wrapper ecosystem for defense, triage, and safe validation. These wrappers are PHP-specific; non-PHP targets need different approaches.

**Safe wrappers (can be used for validation)**:
- `php://filter/convert.base64-encode/resource=<file>` — read any local file as Base64 without PHP execution. Preferred canary: `php://filter/convert.base64-encode/resource=index.php` to confirm LFI without outputting PHP code context (Base64 output is benign).
- `php://filter/read=<file>/resource=<file>` — read raw file content.
- `php://filter/string.rot13/resource=<file>` — ROT13-encode file content; useful when the response is searched for specific string patterns that Base64 would hide.

**Wrappers with data risk (avoid in validation)**:
- `php://input` — reads raw POST body as file content; can be used for code execution if the include function processes PHP. Do not use in active validation without explicit scope authorization for code execution.
- `data://text/plain;base64,<base64>` — inline data wrapper; if the include function evaluates the data, this enables code execution. Reference only for triage and defense.
- `expect://<command>` — if the `expect` extension is loaded, executes a system command. Reference only; using this is destructive.
- `phar://` — PHP Archive wrapper; can trigger deserialization if the phar file is attacker-controlled. Reference only.
- `zip://` / `compress.zlib://` / `compress.bzip2://` — compressed archive wrappers; reference for defense understanding.

**Wrapper chaining**: `php://filter/convert.base64-encode|convert.iconv.utf-8.utf-16/resource=index.php` — chain multiple filters. The chaining capability itself is informative; actual exploitation through chaining depends on the specific filter stack.

### Category 4 — log, session, and file-upload poisoning

Goal: understand how LFI can escalate through controllable file content. This section is for defense and triage; do not execute poisoning steps without explicit scope authorization and separate code-execution approval.

**Log poisoning concept**: when the web server logs are readable via LFI, and the attacker can inject content into the logs (via User-Agent, Referer, or request parameters), the injected content is included by the PHP engine. Countermeasures: ensure logs are not readable by the web server user, use `open_basedir` to restrict include paths, and disable PHP execution in log directories.

**Session file poisoning**: when session files are readable via LFI and the session content is controllable (via user profile fields, uploaded filenames, or session variables), the attacker can inject PHP code into the session file. Countermeasures: use `session.save_path` outside the web root, use strict session ID validation, and hash session data.

**File upload + LFI**: when an uploaded file (profile picture, attachment) is stored within a path reachable by the include function, and the file content is not sanitized, the uploaded file becomes a code execution vector. Countermeasures: store uploaded files outside the web root, serve through a proxy script that does not `include` the file content, and validate file contents even for non-executable extensions.

**Second-order LFI**: when an LFI reads a database-stored file path that was previously set by an attacker through a separate vulnerability (SQL injection, stored XSS). The include follows the path from the database. Countermeasures: validate include paths against a whitelist; never store user-controlled paths in the database.

### Category 5 — cross-platform LFI patterns

**Windows-specific**:
- `C:\Windows\System32\drivers\etc\hosts` — Windows hosts file; safe canary equivalent to `/etc/hostname`.
- `C:\boot.ini` — boot configuration; benign information disclosure.
- Alternate data streams (ADS): `file.php::$DATA` — reveals the default stream; informative, not exploitable in most contexts.
- UNC path injection (SMB): `\\attacker-ip\share\file` — if the server permits outbound SMB, the include may fetch a remote file. This is an active SSRF/LFI hybrid; do not execute without explicit outbound-network authorization.

**Java/JSP-specific**:
- JSP include directives: `<jsp:include page="<%= userInput %>">`, `<%@ include file="<%= userInput %>" %>`, `<c:import url="<%= userInput %>">`.
- Spring `RequestDispatcher` and `ModelAndView` with user-controlled view names.
- Safe canary: include a known JSP fragment that outputs a distinguishable text pattern without sensitive content.

**Node.js-specific**:
- `fs.readFile(userInput)` / `fs.readFileSync(userInput)` with path traversal.
- `require(userInput)` — path traversal in `require` can load arbitrary JavaScript modules.
- `ejs.renderFile(userInput)` / `pug.renderFile(userInput)` — template engine file inclusion.
- Safe canary: read `package.json` to confirm traversal depth without exposing source code.

## Decision points

- **Canary returned benign file → confirm LFI**: record the traversal depth, parser context, and canary file name. Do not proceed to sensitive file read without separate authorization that permits data extraction.
- **Canary failed → LFI not confirmed at tested depth**: increase depth or try alternate canary. Do not read `/etc/passwd` as a fallback canary — it contains usernames.
- **Base64-encoded source returned via php://filter → confirm LFI with code access**: record that source code is readable. Do not decode, store, or analyze the Base64 payload beyond confirming successful inclusion. The decoded source may contain secrets.
- **Log/session poisoning path suspected → stop active testing**: poisoning for code execution requires separate destructive-workflow authorization and is outside the scope of LFI validation. Document the path and recommend server-side mitigation.
- **Wrapper chain appears useful but untested → reference only**: do not execute. Document the theoretical chain for defense/patching purposes.
- **Request includes `/proc/self/environ` or other environment files → refuse**: environment variables often contain secrets (database passwords, API keys, session secrets). Never read or include these.

## Prohibited behavior

- Reading `/etc/passwd`, `/etc/shadow`, `/etc/master.passwd`, or any file containing user credentials or password hashes.
- Reading environment files (`/proc/self/environ`, `.env`, `config.php`, `wp-config.php`) that may contain secrets.
- Reading source code of authentication, session, or cryptographic modules.
- Writing to log files, session files, or uploaded files intending to inject code for later inclusion.
- Using `expect://`, `data://`, or `input://` wrappers in active validation without explicit code-execution authorization.
- Chaining LFI with SSRF to read cloud metadata endpoints (`169.254.169.254`) — this is out of scope for LFI validation and requires separate SSRF authorization.
- Downloading, decoding, or storing Base64-encoded source code from `php://filter` output.
- Providing step-by-step exploitation recipes beyond safe product behavior and defensive reference.

## Stop conditions

- Safe canary fails after reasonable traversal depth and encoding attempts → stop, document LFI not confirmed, do not escalate to sensitive files.
- Response includes credential material (passwords, hashes, API keys) → stop, do not process further, redact immediately.
- Environment file path appears in the inclusion vector → stop, refuse to read environment files.
- Code execution or log poisoning path is requested → stop, redirect to appropriate destructive-workflow skill with separate authorization.
- Target includes out-of-scope host or file path → stop, request scope update.

## Evidence

Record: affected parameter and parser context, traversal depth discovered, safe canary file used, canary response indicator (key string from the canary output), WAF/filter observations (encoding that bypassed or was blocked), and redaction decisions (any file content beyond the canary must be discarded).

Never store: file contents from sensitive paths, Base64-decoded source code, environment variable values, credential data, `etc/passwd` entries, or log file contents containing user data.

## Report handoff

1. When a traversal surface is confirmed, hand off to `vuln-lfi-rfi` for active validation with `pentest_agent_execute_tool`.
2. Reference this payload taxonomy in the finding as the detection rationale — link the safe canary used, the traversal depth confirmed, and the parser context.
3. If path normalization or encoding variants were identified, include them in the handoff notes to guide the active validator.
4. Recommend: input allowlisting for file paths, use of `realpath()` to resolve and validate canonical paths, chroot/jail confinement for file-serving processes, and disabling directory listing and follow-symlink on file-serving endpoints.
