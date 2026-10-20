---
name: tech-tomcat
description: Apache Tomcat servlet container security review — identifies exposed manager and host-manager applications, default credentials, unauthenticated application listing, example applications, AJP connector exposure (Ghostcat CVE-2020-1938), directory listing, version disclosure, JMX remote access, weak SSL/TLS configuration, session persistence and clustering exposure, and valve/misconfigured realm authentication. All probes are read-only HTTP requests and version fingerprinting. No application deployment, no WAR upload, no manager invocation, no AJP exploitation, no credential brute-forcing.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, tomcat-security-audit, connector-security-report]
---

# Apache Tomcat security review

Use this skill to assess the security posture of Apache Tomcat servlet containers. The review covers administrative application exposure (Manager, Host-Manager), authentication configuration, publicly accessible web applications, AJP connector security (including the Ghostcat vulnerability), version disclosure, default and example application risks, JMX remote monitoring, TLS configuration, and session/clustering security. All probes are read-only HTTP requests. This skill never deploys WAR files, uploads applications, interacts with Manager or Host-Manager functionality, exploits the AJP protocol, or attempts default credential login.

## Required inputs

- Tomcat base URL (e.g., `https://TARGET:8080`, `http://TARGET:8443`).
- If AJP is in scope: AJP connector port (default: 8009).
- Scope file confirming which hosts, ports, and web applications are in scope.
- Authorization cache valid for the target host.
- Optional: user-provided Tomcat configuration files (`server.xml`, `tomcat-users.xml`, `web.xml`, `context.xml`, `catalina.properties`) for offline review.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for the Tomcat host before requests.
3. `pentest_agent_check_authorization` before any HTTP requests.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — Server discovery and version fingerprinting

1. **Tomcat identification and version**:
   - `curl -sI https://TARGET:8080/ | grep -iE "Server:|X-Powered-By:"`.
   - Default Tomcat `Server` header: `Apache-Coyote/1.1`. Default error pages include: `Apache Tomcat/9.0.80`.
   - `/` (ROOT application) typically shows "Apache Tomcat/9.0.80" branding and the Tomcat logo.
   - `curl -s https://TARGET:8080/docs/ | head -10` — if the `docs` app is deployed, it reveals the exact version.
   - `/examples/` — example applications are bundled by default in many Tomcat distributions. If present, exact version is revealed and the examples themselves contain known vulnerabilities (e.g., session example `/examples/servlets/servlet/SessionExample` manipulates arbitrary session attributes).
2. **Version from error pages**:
   - `curl -s https://TARGET:8080/nonexistent-page-12345`. Tomcat's default 404 page includes "Apache Tomcat/version" in the footer.
   - `curl -s https://TARGET:8080/%00` — null byte injection may reveal version details on older versions.
3. **Server info endpoint** (if `ServerInfo` valve is not configured):
   - `curl -s https://TARGET:8080/manager/status?XML=true` — the Manager status endpoint may reveal version even when authentication is required (the 401 page often includes version).

### Phase 2 — Manager and Host-Manager application exposure

The Tomcat Manager application allows deploying, starting, stopping, and undeploying web applications remotely.

1. **Manager application accessibility**:
   - `curl -sI https://TARGET:8080/manager/html`. If HTTP 200 or 401 → Manager is accessible. If HTTP 401, authentication is required. If 403 → Manager is restricted by IP (RemoteAddrValve).
   - `curl -sI https://TARGET:8080/manager/text` (text-based interface, used by Ant/Maven).
   - `curl -sI https://TARGET:8080/manager/status?XML=true` (status endpoint, often less protected).
   - **Finding**: Manager accessible over the network → HIGH. Even if authenticated, the attack surface for credential guessing exists.
   - **Finding**: Manager accessible without authentication → CRITICAL. An attacker can deploy arbitrary WAR files → remote code execution on the Tomcat server.
2. **Host-Manager application** (manages virtual hosts):
   - `curl -sI https://TARGET:8080/host-manager/html`.
   - Similar risk profile to Manager — allows creating, removing, and listing virtual hosts. CRITICAL if unauthenticated.
3. **Default credential posture** (inspect configuration, do NOT attempt login):
   - Check `tomcat-users.xml` (if provided): default `tomcat` user with password `tomcat` or `s3cret`.
   - Common default roles: `manager-gui`, `manager-script`, `manager-jmx`, `manager-status`, `admin-gui`, `admin-script`.
   - **Finding**: `tomcat-users.xml` contains a user with `manager-gui` role and a weak/well-known password → CRITICAL. Document without attempting to log in.
   - **PROHIBITED**: do not attempt to authenticate with any username/password combination, including known defaults. The risk is documented based on configuration analysis.

### Phase 3 — Web application enumeration

Tomcat often deploys default and example applications that reveal information or contain vulnerabilities.

1. **Default application inventory**:
   - Common paths: `/`, `/manager/`, `/host-manager/`, `/docs/`, `/examples/`, `/ROOT/`.
   - Check: `curl -sI https://TARGET:8080/examples/` → HTTP 200 = examples deployed. MEDIUM.
   - The examples app contains: `/examples/servlets/servlet/SessionExample` (create/read arbitrary session attributes), `/examples/jsp/snp/snoop.jsp` (request/header dumper), `/examples/servlets/servlet/RequestInfoExample` (full request details).
   - **Finding**: examples application in production → HIGH. Information disclosure and potential for abuse.
2. **Directory listing** (listings enabled in `web.xml`):
   - `curl -s https://TARGET:8080/ROOT/ | grep -i "Index of"`.
   - If directory listing is enabled: all files in the web application root are browsable. HIGH.
   - Tomcat disables directory listing by default since version 7.0.x, but custom `web.xml` or context configuration can re-enable it.
3. **Custom application discovery**:
   - Enumerate application base paths: `/app/`, `/api/`, `/web/`, `/service/`, `/admin/`, `/console/`, `/actuator/`, `/swagger-ui/`, `/graphql/`.
   - Each Tomcat web application is a separate context with its own classloader and configuration.
   - Check for Spring Boot actuator endpoints if the app is a Spring Boot WAR deployed on Tomcat.

### Phase 4 — AJP connector security (port 8009)

The Apache JServ Protocol (AJP) connector allows proxying from Apache httpd to Tomcat. It is a binary protocol, not HTTP.

1. **AJP port discovery**:
   - Port 8009 is the default AJP port. Check: `nc -zv TARGET_IP 8009` (read-only port check, no protocol interaction).
   - If port is open → AJP connector is enabled. MEDIUM to CRITICAL depending on security settings.
2. **Ghostcat (CVE-2020-1938) vulnerability assessment**:
   - CVE-2020-1938 allows reading arbitrary files from the Tomcat web application directory via a crafted AJP request, without authentication.
   - Affected: Apache Tomcat 6.x (all versions), 7.x < 7.0.100, 8.x < 8.5.51, 9.x < 9.0.31.
   - If the detected Tomcat version falls in these ranges AND the AJP port is open → CRITICAL. The vulnerability allows reading `/WEB-INF/web.xml`, `/WEB-INF/classes/` (class files → decompiled source), and configuration files containing credentials.
   - **PROHIBITED**: do not attempt to exploit Ghostcat. Document the vulnerable version and recommend immediate upgrade.
   - **Mitigation**: set `secretRequired="true"` and `secret="..."` on the AJP connector in `server.xml` (the fix that backported versions use), or set `address="127.0.0.1"` to restrict AJP to localhost only.
3. **AJP secret configuration** (from user-provided `server.xml`):
   - `<Connector protocol="AJP/1.3" port="8009" secretRequired="true" secret="..." address="127.0.0.1" />`.
   - If `secretRequired="false"` → AJP accepts connections without a shared secret. CRITICAL.
   - If `address="0.0.0.0"` or not set → AJP listens on all interfaces. HIGH.

### Phase 5 — JMX and management security

JMX (Java Management Extensions) allows remote monitoring and management.

1. **JMX port discovery**:
   - Default JMX RMI registry port: 1099. JMXMP port: 9999 (if configured).
   - Check for JMX service URL in `catalina.properties` or startup scripts: `-Dcom.sun.management.jmxremote.port=...`.
   - If JMX is enabled without authentication (`-Dcom.sun.management.jmxremote.authenticate=false`) → CRITICAL. Remote JMX allows invoking arbitrary MBean operations, potentially including `ThreadPoolExecutor` shutdown.
2. **JMX password file** (from user-provided config):
   - `jmxremote.password` and `jmxremote.access` files in `$CATALINA_BASE/conf/`.
   - Default passwords: `monitorRole` / `QED`, `controlRole` / `R&D`. CRITICAL if unchanged.

### Phase 6 — TLS and connector configuration

1. **TLS on HTTP connector**:
   - If Tomcat is on `https://` with port 8443: check with `testssl https://TARGET:8443`.
   - TLS 1.0/1.1 → HIGH. SSLv3 → CRITICAL.
   - Check for weak ciphers, missing forward secrecy, expired certificates.
2. **HTTP connector security**:
   - `server.xml` `<Connector>` settings: `allowTrace` (if `true` → TRACE method enabled, XST risk. MEDIUM), `maxPostSize` (limits upload size), `maxParameterCount` (prevents hash collision DoS).
   - `xpoweredBy` attribute → whether `X-Powered-By: Servlet/4.0 JSP/2.3` header is sent. LOW informational.
3. **Secure and HttpOnly cookie flags**:
   - Check the `Context` element in `context.xml`: `<Context useHttpOnly="true">`.
   - The `sessionCookiePath`, `sessionCookieDomain`, `sessionCookiePathUsesTrailingSlash` → session cookie security.

### Phase 7 — Realm and authentication configuration

1. **Realm type** (from `server.xml` or `context.xml`):
   - `UserDatabaseRealm` (default, uses `tomcat-users.xml`) — acceptable for small deployments. MEDIUM if `tomcat-users.xml` is writable by the Tomcat process.
   - `JDBCRealm` (database-backed users) — check if passwords are stored as plaintext or hashed. HIGH if plaintext.
   - `JNDIRealm` (LDAP/AD-backed) — secure option. Informational.
   - `MemoryRealm` (deprecated since Tomcat 7) — stored users in `tomcat-users.xml`. Now superseded by `UserDatabaseRealm`.
   - `JAASRealm` (Java Authentication and Authorization Service) — flexible but complex to configure correctly.
   - `LockOutRealm` — wraps another realm to prevent brute-force. Positive control if present.
   - **Finding**: no `LockOutRealm` wrapping the primary realm → MEDIUM (brute-force possible).
2. **Valve configuration**:
   - `RemoteAddrValve` — restricts access by IP address. Check Manager/Host-Manager context for `allow="127\.0\.0\.1|::1|10\.0\.0\..*"`. Secure if restricted to internal networks.
   - `RemoteCIDRValve` — CIDR-based equivalent.
   - `CrawlerSessionManagerValve` — prevents session hijacking via bot. Positive if present.

## Decision points

- **Manager app responds with 401 (not 403)**: authentication is required but no IP restriction. Brute-force risk exists. Flag as MEDIUM-HIGH if combined with weak credentials in `tomcat-users.xml`.
- **AJP port is open but `secretRequired="true"` and bound to `127.0.0.1`**: AJP is secured. The port is only accessible locally. Flag as LOW informational.
- **Tomcat version is 9.0.31+**: Ghostcat is patched. AJP risk is only from misconfiguration (missing secret, public bind address), not the CVE.
- **`examples` app is deployed but behind authentication**: still a finding. The examples app is intended for development and should not be deployed in any production environment.

## Prohibited behavior

- Attempting to authenticate to the Manager or Host-Manager applications.
- Exploiting Ghostcat or any other AJP vulnerability.
- Deploying, starting, stopping, or undeploying web applications.
- Uploading WAR files.
- Reading arbitrary files via the AJP connector.
- Brute-forcing JMX passwords or Tomcat user credentials.
- Exploiting example application vulnerabilities (session manipulation, information disclosure beyond confirming accessibility).
- Attempting to connect to JMX remote management.

## Stop conditions

- Manager or Host-Manager application returns HTTP 200 without redirect → no authentication. CRITICAL. Document and stop probing those paths.
- AJP port is open and Tomcat version is vulnerable to Ghostcat → CRITICAL. Do not exploit.
- `tomcat-users.xml` (if provided) contains a user with `manager-gui` and a weak password → CRITICAL. Document without testing authentication.
- JMX port is open and `jmxremote.authenticate=false` → CRITICAL.

## Evidence

For each finding, record: host:port, finding type, endpoint/configuration, access level, severity, and remediation. Evidence template:

```text
Apache Tomcat security review for: [TARGET_IP:PORT]
Tomcat version: [detected version] (from: [Server header / error page / branding])
Review date: [DATE]

Manager applications:
  Manager (/manager/html): [not deployed / IP-restricted (403) / auth-required (401) (HIGH) / open (200) (CRITICAL)]
  Host-Manager (/host-manager/html): [not deployed / IP-restricted / auth-required / open (CRITICAL)]
  Manager status (/manager/status): [accessible / blocked]

Default applications:
  ROOT: [branding only / custom]
  Docs: [deployed (MEDIUM) / not deployed]
  Examples: [deployed (HIGH) / not deployed]
  Directory listing: [enabled (HIGH) / disabled]

AJP connector (port 8009):
  Port status: [open / closed]
  Vulnerable to Ghostcat: [yes (CRITICAL) / no (patched) / version unknown]
  secretRequired: [true (OK) / false (CRITICAL)]
  Bind address: [127.0.0.1 (OK) / 0.0.0.0 (HIGH)]

TLS:
  Protocol: [TLS 1.3 / TLS 1.2 / TLS 1.0-1.1 (HIGH) / SSLv3 (CRITICAL)]
  Certificate: [valid / expired (MEDIUM) / self-signed (LOW)]

JMX:
  Enabled: [yes / no]
  Authenticate: [true (OK) / false (CRITICAL)]

Authentication:
  Realm type: [UserDatabase / JDBC / JNDI / JAAS / LockOutRealm]
  LockOutRealm: [present (OK) / absent (MEDIUM)]
  RemoteAddrValve on Manager: [present (OK) / absent (HIGH)]

Redaction notes:
  - No authentication attempts were made.
  - No WAR files were deployed.
  - No AJP requests were sent beyond port-open detection.
  - Ghostcat was NOT exploited.
  - Tomcat user credentials from configuration files are not included.
  - JMX passwords are redacted if found in configuration.
```

## Report handoff

1. `pentest_agent_record_finding` for each finding with: host, finding type, severity, specific remediation (server.xml change, valve addition, application removal, Tomcat upgrade), and verification test.
2. Priority matrix: CRITICAL (unauthenticated Manager, Ghostcat-vulnerable + AJP open, JMX without auth, manager-gui user with default password). HIGH (Manager accessible without IP restriction, Examples app in production, directory listing, AJP on public interface, Ghostcat-vulnerable with AJP closed). MEDIUM (Docs app deployed, Server header version disclosure, no LockOutRealm, TRACE method enabled, weak TLS). LOW (ROOT branding page, X-Powered-By header).
3. Provide a Tomcat hardening checklist: remove default applications (docs, examples, ROOT), restrict Manager/Host-Manager with RemoteAddrValve and strong passwords, upgrade to latest version to patch Ghostcat, set `secretRequired="true"` on AJP connector with strong secret and bind to localhost, remove `Server` header via `server` attribute in connector, disable TRACE method, enforce TLS 1.2+, implement LockOutRealm, ensure JMX authentication, and set `useHttpOnly="true"`.
4. Explicitly note: no authentication attempts were made against Manager or Host-Manager; Ghostcat was NOT exploited; no WAR files were deployed; no AJP requests beyond port-open detection were sent; all probing was read-only HTTP.
