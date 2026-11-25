---
name: tech-apache-nginx
description: Apache HTTP Server and Nginx configuration security review — identifies server-info/server-status exposure, path traversal via alias misconfigurations, .htaccess bypass, directory listing, HTTP method abuse (TRACE/PUT/DELETE), TLS and cipher misconfigurations, server-header version leakage, unsafe proxy configurations, and backup/config file exposure. All probes are read-only and low-rate. No exploit payload delivery, no configuration modification, no service restart.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, server-config-audit, misconfiguration-matrix]
---

# Apache HTTP Server and Nginx configuration security review

Use this skill to assess the security posture of Apache HTTP Server (httpd) and Nginx web server configurations. The review covers server fingerprinting, information disclosure endpoints (server-status, server-info), alias/directory traversal weaknesses, access control bypasses, HTTP method restrictions, TLS configuration, proxy/upstream misconfigurations, and exposed backup or configuration files. All probes are read-only HTTP requests at a low rate. This skill never delivers exploit payloads, accesses admin functionality, modifies server configuration, or restarts services. Active probing is gated behind `pentest_agent_execute_tool` with scope and authorization validation.

## Required inputs

- Target host or list of hosts running Apache or Nginx (confirmed via recon/enum phases).
- Scope file confirming which hosts, paths, and HTTP methods are in scope.
- Rate limits: max requests per second, max concurrent connections per host.
- Authorization cache valid for every target host.
- Optional: user-provided server configuration snippets for offline review (httpd.conf, nginx.conf, .htaccess files, vhost configs). If provided, prefer offline review over live probing.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every host before requests.
3. `pentest_agent_check_authorization` before any HTTP request.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval for any risky requests.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — server identification and version fingerprinting

Determine which web server is running, and if possible, its version.

1. **HTTP response header inspection** (passive, low-noise):
   - `curl -sI https://TARGET/ | grep -iE "Server:|X-Powered-By:|X-Generator:|X-AspNet-Version:"`.
   - Server header values: `Apache`, `Apache/2.4.57 (Ubuntu)`, `nginx`, `nginx/1.24.0`, `cloudflare` (CDN-fronted), `Netlify`, `Vercel`, `Caddy`, `LiteSpeed`, `IIS`, `openresty`, `Tengine`.
   - Document: if the server header is present with an exact version, this is a LOW finding (information disclosure). If it's been removed or set to a generic value, it's a positive control.
2. **Error-page fingerprinting** (request a non-existent path):
   - `curl -sI https://TARGET/nonexistent-page-12345`.
   - Apache default 404 page includes "Apache/version (OS) Server at hostname Port 80".
   - Nginx default 404 includes "nginx/version".
   - Custom error pages suppress this information.
3. **Nginx-specific header detection**: `X-Accel-*` headers, `X-Request-ID`, `X-Real-IP` (from nginx reverse proxy setups).
4. **Apache-specific header detection**: `X-Cache` (mod_cache), `X-Varnish` (Varnish cache in front of Apache).
5. **Technology differentiation**:
   - Apache + mod_php: `.php` files handled, `X-Powered-By: PHP/x.y.z`.
   - Apache + mod_wsgi (Python): `WSGI/` in headers.
   - Nginx + php-fpm: Nginx proxies `.php` to php-fpm. Nginx Server header + PHP response behavior.
   - Nginx as reverse proxy: `X-Forwarded-*` headers set, `X-Real-IP` present.
   - CDN-fronted: `CF-Ray`, `X-Cache: Hit from CloudFront`, `X-Served-By`, `X-Timer`.

### Phase 2 — information disclosure endpoints

Check for common debug and status pages that leak server internals.

1. **Apache server-status** (`/server-status`):
   - `curl -s https://TARGET/server-status`.
   - If accessible: displays all active connections, request URLs, client IPs, CPU usage, uptime. This is a HIGH finding — real-time traffic monitoring exposed.
   - Often protected by IP restriction but misconfigured to allow all.
2. **Apache server-info** (`/server-info`):
   - `curl -s https://TARGET/server-info`.
   - Displays loaded modules, configuration directives, virtual hosts, environment variables. HIGH finding — server architecture fully exposed.
3. **Nginx status module** (`/nginx_status`, `/status`, `/basic_status`):
   - `curl -s https://TARGET/nginx_status`.
   - Shows active connections, accepted/ handled requests, reading/writing/waiting counts.
4. **PHP-FPM status** (`/fpm-status`, `/php-fpm-status`, `/status?full`):
   - `curl -s https://TARGET/fpm-status?full`.
   - Shows per-process memory usage, request duration, request URI, state. HIGH finding.
5. **Directory listing**:
   - Check common upload/static directories for directory listing.
   - `curl -sI https://TARGET/uploads/ | grep -i "Index of"`.
   - Apache: `Options +Indexes` without `-Indexes`. Nginx: `autoindex on` in location block.
   - Finding: directory listing exposes file structure. MEDIUM unless sensitive files are exposed.

### Phase 3 — alias and path traversal

Identify misconfigurations that allow reading files outside the intended document root.

1. **Nginx alias misconfiguration (off-by-slash)**:
   - Vulnerability: `location /static { alias /var/www/uploads/; }` — missing trailing slash on `location`.
   - Exploit: `https://TARGET/static../etc/passwd` resolves to `/var/www/uploads/../etc/passwd`.
   - Test: `curl -s https://TARGET/static../etc/passwd | head -5`. If content returned: CRITICAL.
   - Test: `curl -s https://TARGET/static../etc/nginx/nginx.conf` — Nginx config may contain upstream addresses, SSL certificate paths, auth credentials.
   - **SAFETY**: describe the technique, do not provide paste-ready path-traversal payloads. Use the test only through `pentest_agent_execute_tool` with approval for destructive risk.
2. **Nginx `proxy_pass` without trailing slash**:
   - If `location /api { proxy_pass http://backend:8080; }`, a request to `/api../admin` may reach `http://backend:8080/../admin`.
   - Test: `curl -s https://TARGET/api../admin/`. Document impact without full exploitation.
3. **Apache Alias traversal**:
   - If `Alias /icons/ /usr/share/apache2/icons/`, test for traversal: `curl -s https://TARGET/icons/../../../etc/passwd`.
   - Apache 2.4.49 (CVE-2021-41773) and 2.4.50 (CVE-2021-42013): path traversal and RCE via `Require all denied` bypass.
   - If version fingerprint suggests 2.4.49 or 2.4.50: flag as CRITICAL — known RCE. Do not attempt to exploit. Recommend immediate upgrade.
4. **Nginx merge_slashes bypass**: if `merge_slashes` is off, `//` sequences reach the backend. Test for access-control bypass via path obfuscation.

### Phase 4 — access control and .htaccess bypass

Test whether access controls can be circumvented.

1. **.htaccess / .htpasswd exposure**:
   - `curl -sI https://TARGET/.htaccess` — HTTP 200 = exposed. May contain rewrite rules, IP restrictions, auth configuration.
   - `curl -sI https://TARGET/.htpasswd` — HTTP 200 = CRITICAL. Contains password hashes for HTTP Basic Auth users.
2. **Protected path bypass techniques** (test only with approval):
   - Case manipulation: `/Admin` vs `/admin` (Apache on case-insensitive filesystems).
   - Trailing characters: `/admin.`, `/admin/`, `/admin/.`, `/./admin/`.
   - URL encoding: `/adm%69n` (`i` encoded), `/%61dmin` (`a` encoded).
   - HTTP method override: `GET /admin` blocked → `POST /admin` or `OPTIONS /admin` allowed.
   - IP restriction bypass via `X-Forwarded-For`: `curl -H "X-Forwarded-For: 127.0.0.1" https://TARGET/admin/`.
   - These are active bypass probes. Each requires scope permission and executor approval.
3. **HTTP method restrictions**:
   - `curl -s -X OPTIONS https://TARGET/ -I | grep "Allow:"`.
   - Dangerous methods if allowed: PUT (file upload), DELETE (file removal), TRACE (XST — Cross-Site Tracing), CONNECT (tunneling).
   - TRACE enabled: `curl -s -X TRACE https://TARGET/ -H "Custom: test-value"`. If the header is reflected, XST is possible. MEDIUM finding in most contexts (modern browsers disable TRACE).

### Phase 5 — TLS and cipher security

If the server uses HTTPS, assess its TLS configuration.

1. **TLS version support**:
   - `testssl --protocols https://TARGET` or `sslscan TARGET:443`.
   - TLS 1.0 and 1.1 → HIGH (end-of-life, insecure). TLS 1.2 → acceptable. TLS 1.3 → best.
   - SSLv2/SSLv3 → CRITICAL (should never be enabled).
2. **Cipher suite audit**:
   - Check for: NULL ciphers (no encryption), EXPORT ciphers (weak), RC4, 3DES, CBC ciphers without Encrypt-then-MAC.
   - Check for forward secrecy: ECDHE or DHE key exchange.
   - Finding: weak ciphers → MEDIUM. NULL/EXPORT ciphers → HIGH.
3. **Certificate validation**:
   - Expiry date, wildcard scope, Subject Alternative Names (SANs).
   - Self-signed certificate → MEDIUM for internal services, HIGH for public-facing.
   - Certificate transparency log check.

### Phase 6 — proxy and upstream misconfigurations

For Nginx/Apache acting as reverse proxies, check for unsafe proxy behavior.

1. **SSRF via proxy_pass with user-controllable host**:
   - If Nginx `proxy_pass` uses a variable from the request (e.g., `$http_host`, `$arg_backend`), an attacker can set the proxy destination.
   - Test pattern: `curl -H "Host: 169.254.169.254" https://TARGET/` (AWS metadata endpoint). If the response is AWS metadata → CRITICAL SSRF.
   - **SAFETY**: this is an active probe that may trigger an alert in the target's cloud environment. Requires explicit approval and documented risk acknowledgment.
2. **Host header injection**: if the backend trusts the `Host` or `X-Forwarded-Host` header for URL generation, craft requests that poison links, password reset emails, or redirect destinations.
3. **`proxy_set_header` hygiene**:
   - Is `X-Forwarded-For` sanitized? (Attacker can spoof source IP.)
   - Is `X-Real-IP` trusted by the backend? (Actions attributed to wrong IP.)

### Phase 7 — exposed backup and configuration files

Check common locations for accidentally exposed files.

1. **Backup file patterns**:
   - `config.php.bak`, `config.php~`, `config.php.old`, `config.php.orig`, `config.php.save`, `config.php.swp`, `.config.php.swp`.
   - `database.yml.bak`, `wp-config.php.bak`, `.env.backup`, `settings.py.old`.
   - Test: `curl -sI https://TARGET/config.php.bak` (and other variations).
2. **Version control exposure**:
   - `/.git/HEAD` (HTTP 200 → entire Git history accessible).
   - `/.svn/entries`, `/.svn/wc.db`.
   - `/.DS_Store` (macOS directory metadata, can reveal directory structure).
3. **Editor swap and temp files**: `.index.php.swp`, `.index.php.swo`, `index.php~`.

## Decision points

- **Server version is end-of-life** (e.g., Apache 2.2, Nginx < 1.16): flag as HIGH. EOL means no security patches. Recommend upgrade path with specific target version.
- **Server-status or server-info is accessible but requires a specific IP** (HTTP 403 for you, HTTP 200 for the allowed IP): document as "access control present." Attempt IP spoofing only if scope explicitly permits it.
- **Alias traversal test returns no content but different status code**: 403 = path exists but access denied (the traversal works; the file is protected). 404 = path doesn't exist. 200 with empty body = file exists but is empty.
- **TLS scan is blocked by CDN/WAF**: document CDN detection. The actual origin server's TLS configuration may differ and cannot be assessed.
- **`.git` directory is accessible**: CRITICAL. Stop current phase and document immediately. Do not proceed to dump the repository without explicit separate approval.

## Prohibited behavior

- Sending HTTP requests to any host not validated through `pentest_agent_validate_target`.
- Running exploit payloads, shell commands, or reverse shells through server misconfigurations.
- Modifying server configuration or restarting services.
- Performing path traversal beyond reading files commonly used for proof (e.g., reading `/etc/passwd` is sufficient; do not traverse to `/etc/shadow`, private keys, or database files without explicit approval).
- Using TRACE for XST beyond a header-reflection test.
- Exploiting CVE-2021-41773 or CVE-2021-42013 — document as "known RCE — immediate upgrade required." Do not attempt exploitation.
- Testing SSRF via proxy_pass against cloud metadata endpoints without explicit risk acknowledgment.

## Stop conditions

- Server returns 429 (rate limiting) or 403 (WAF block) → reduce rate or stop. Do not attempt to evade WAF.
- Probe triggers an error page with a stack trace or database connection error → stop current probe type, document the information leak as a finding, do not exploit the exposed data.
- `.git/HEAD` returns 200 → do not proceed to enumerate or dump the repository. Document as CRITICAL.
- `proxy_pass` SSRF test returns cloud metadata → stop. Document the SSRF finding with impact. Do not enumerate the metadata service further without explicit approval.
- Apache version 2.4.49 or 2.4.50 is confirmed → flag for immediate upgrade. Do not test the RCE.

## Evidence

For each finding, record: target host, finding type, specific endpoint/configuration, HTTP request/response (redacted), severity, and remediation. Evidence template:

```text
Apache/Nginx configuration review for: [TARGET_HOST]
Server: [Apache 2.4.57 / nginx 1.24.0 / CDN-fronted — origin [detected/unknown]]
Probe date: [DATE]

Findings summary:
  CRITICAL: [N] | HIGH: [N] | MEDIUM: [N] | LOW: [N] | Informational: [N]

Information disclosure:
  - server-status: [accessible (HIGH) / blocked / not present]
  - server-info: [accessible (HIGH) / blocked / not present]
  - Directory listing: [N] directories with listing enabled
  - Server header version: [exposed (LOW) / suppressed]

Access control:
  - Methods allowed: GET, POST, [PUT (MEDIUM)], [DELETE (HIGH)], [TRACE (MEDIUM)]
  - .htaccess exposed: [yes (MEDIUM) / no]
  - .htpasswd exposed: [yes (CRITICAL) / no]

Alias/path traversal:
  - Nginx off-by-slash: [vulnerable (CRITICAL) / not vulnerable / not applicable]
  - Apache mod_alias traversal: [vulnerable / not vulnerable / not applicable]
  - Apache CVE-2021-41773/42013: [vulnerable version detected (CRITICAL — immediate upgrade) / not applicable]

TLS configuration:
  - TLS 1.0/1.1: [enabled (HIGH) / disabled]
  - SSLv2/SSLv3: [enabled (CRITICAL) / disabled]
  - Weak ciphers: [N] detected
  - Forward secrecy: [supported / not supported]

Exposed files:
  - .git: [exposed (CRITICAL) / not exposed]
  - Backup/config files: [N] exposed

Redaction notes:
  - All probes were rate-limited read-only HTTP requests.
  - No exploit payloads were delivered.
  - Server version details in evidence are redacted to major version only.
  - No repository dumps or file exfiltration occurred.
  - No server configuration was modified.
```

## Report handoff

1. `pentest_agent_record_finding` for each misconfiguration with: host, endpoint, finding type, severity, redacted evidence excerpt, remediation configuration change (specific Nginx/Apache directive), and verification test.
2. Priority: CRITICAL (exposed .git, known RCE version, .htpasswd exposure, alias traversal to system files). HIGH (server-status, server-info, TRACE enabled, TLS 1.0, PUT/DELETE allowed). MEDIUM (directory listing, server version header, weak ciphers). LOW (backup file with non-sensitive data).
3. Provide an Nginx/Apache hardening checklist based on findings.
4. Explicitly note: all probing was read-only, rate-limited, and scope-validated. No exploit payloads were delivered, no server configuration was modified, and no services were affected.
