---
name: framework-dotnet
description: .NET/ASP.NET security review — validate debug and error disclosure, authentication middleware, ViewState and session configuration, Kestrel/IIS settings, and dependency hygiene with docs-first, read-only checks and no exploitation or deserialization attacks.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# .NET/ASP.NET security — configuration and surface review

Use this skill to review ASP.NET and .NET application security posture on authorized in-scope targets. Validate debug and error-page disclosure, authentication-middleware configuration, ViewState and session-state settings, Kestrel/IIS server hardening, and framework-version patch status. All tests are read-only and low-rate. Never attempt ViewState deserialization attacks, exploit Razor template injection, relay NTLM authentication, or test credential endpoints.

## Required inputs

- Written scope covering the .NET application hosts, API endpoints, static paths, IIS/Kestrel configuration endpoints, and allowed review methods. Explicit confirmation that deserialization attacks, NTLM relay, template injection, and credential testing are prohibited unless separately approved.
- .NET/ASP.NET version from: `X-AspNet-Version` header, `X-Powered-By` header, error-page format, response-header patterns, or local source code if provided.
- Official Microsoft documentation for the detected .NET version — prefer learn.microsoft.com.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — version detection and framework fingerprinting

1. Detect ASP.NET from response headers: `X-AspNet-Version: 4.0.30319` (classic ASP.NET), `X-Powered-By: ASP.NET` (IIS-hosted), and `Server: Microsoft-IIS/X.Y` or `Server: Kestrel`. The `X-AspNet-Version` header reveals the .NET Framework version and should be suppressed in production.
2. Identify the .NET platform: ASP.NET Framework (System.Web, IIS-dependent), ASP.NET Core (cross-platform, Kestrel/IIS), or Blazor (WebAssembly or Server). Each has distinct security characteristics: Framework relies on `machineKey` and `web.config`, Core uses `appsettings.json` and middleware, and Blazor Server uses SignalR with stateful circuits.
3. Check for additional framework signals: `__RequestVerificationToken` hidden fields (ASP.NET anti-CSRF), `__VIEWSTATE` hidden fields (WebForms), `.axd` extension handlers (Trace.axd, WebResource.axd), and `/swagger/` (Swashbuckle/Swagger in ASP.NET Core).
4. If the application returns detailed errors, extract the .NET version, stack trace format, and framework type from the error page. ASP.NET yellow error pages (YSOD) reveal extensive internal information.
5. Document version evidence. Flag: ASP.NET Framework versions before 4.8 (end of support), .NET Core versions before 3.1 (end of support), and any framework with known unpatched CVEs.

### Phase 2 — debug, trace, and error disclosure

1. Check whether `Trace.axd` is exposed: this ASP.NET Framework handler outputs detailed request-trace information including server variables, session state, cookies, and form data. If accessible without authentication, it is a critical information-disclosure finding.
2. Check for custom error mode: trigger errors via malformed input, missing parameters, or triggering a 404 on a framework path. If the application returns a detailed ASP.NET yellow error page with a full stack trace, source code snippets, and server variables, `customErrors` is not enabled or is set to `Off` — a high finding.
3. Check for debug-mode indicators: in ASP.NET Framework, `<compilation debug="true">` in `web.config` enables debug-mode behavior including longer timeouts, disabled caching, and detailed error output. In ASP.NET Core, `ASPNETCORE_ENVIRONMENT=Development` enables the Developer Exception Page with full stack traces and request details.
4. Check for `web.config` exposure: attempt to fetch `/web.config` directly. If the file is served, it contains database connection strings, `machineKey` values, authentication settings, and internal configuration — critical finding. IIS should block `.config` file serving by default, but misconfiguration happens.
5. Check for Swagger/OpenAPI exposure: ASP.NET Core applications commonly use Swashbuckle. Probe `/swagger/`, `/swagger/v1/swagger.json`. If Swagger is publicly accessible and documents internal endpoints, flag as information disclosure.

### Phase 3 — authentication and authorization middleware

1. Identify the authentication mechanism: ASP.NET Framework uses Forms Authentication, Windows Authentication, or OWIN middleware. ASP.NET Core uses `AuthenticationMiddleware` with JWT Bearer, Cookie, OAuth/OpenID Connect, or Windows authentication handlers.
2. Check for Windows Authentication (NTLM/Kerberos) exposure: if the application returns `WWW-Authenticate: Negotiate` or `WWW-Authenticate: NTLM` headers, the application uses integrated Windows authentication. Do not capture or relay NTLM challenge-response tokens — record the authentication type only.
3. Test authorization bypass on protected endpoints: send requests without authentication cookies/tokens. Confirm 401/403 response. If a protected endpoint returns 200 without authentication, flag as critical.
4. Check for missing anti-CSRF tokens: in ASP.NET Framework, state-changing POST requests should include `__RequestVerificationToken`. In ASP.NET Core, anti-CSRF is automatic with `[AutoValidateAntiforgeryToken]` — test by omitting the token on a POST and checking for 400/403.
5. Check role-based access: if the application exposes admin or management paths, confirm they are not accessible without authentication. Do not attempt to guess or forge roles.

### Phase 4 — ViewState, session state, and serialization review

1. For ASP.NET WebForms applications only: inspect the `__VIEWSTATE` hidden field. If present, the application uses ViewState for client-side state management. Decode the ViewState value (base64) and check whether it is encrypted. If the ViewState is not encrypted and contains sensitive data, flag as information disclosure.
2. Check for ViewState MAC protection: ASP.NET should sign ViewState with the `machineKey` to prevent tampering. If the application uses an unencrypted, unsigned ViewState, it may be vulnerable to deserialization attacks — but do not attempt ViewState deserialization or `ysoserial.net` payload generation.
3. Check for `machineKey` exposure: search for `machineKey` values in: `web.config` (if exposed), error pages, source-code leaks, and public repositories. A leaked `machineKey` allows ViewState forgery and session-token generation — critical finding.
4. Check session-state configuration: inspect session cookies for `ASP.NET_SessionId` or custom session identifiers. Check cookie flags: `HttpOnly`, `Secure`, `SameSite`, and `Path`.
5. Do not attempt to forge ViewState, craft deserialization payloads, or use `ysoserial.net`-type tools. Record configuration weaknesses only.

### Phase 5 — server hardening and header review

1. Inspect server-identity headers: `Server: Microsoft-IIS/X.Y`, `Server: Kestrel`, `X-Powered-By: ASP.NET`, and `X-AspNet-Version`. All should be suppressed in production — flag as hardening gaps.
2. Check for IIS-specific exposures: WebDAV enabled (`PROPFIND`/`OPTIONS` returning detailed methods), directory browsing enabled (directory listing on static paths), and IIS short-file-name disclosure (8.3 filename patterns) via tilde (`~`) requests.
3. Inspect security headers: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options`/`CSP: frame-ancestors`, `Strict-Transport-Security`, and `Referrer-Policy`. ASP.NET Core can add these via middleware or `web.config`/`appsettings.json`.
4. Check for CORS configuration: in ASP.NET Core, CORS is configured via `AddCors()` and `UseCors()`. Send cross-origin requests and check `Access-Control-Allow-Origin`. Reflective origin with credentials is a high finding.
5. Check for HTTPS enforcement: ASP.NET Core supports HTTPS redirection and HSTS via `UseHttpsRedirection()` and `UseHsts()`. Send plain-HTTP requests and verify redirection. Missing HTTPS on a production application is a high finding.

## Decision points

- **Escalate on `Trace.axd` exposed without authentication**: request traces including cookies, session state, and server variables → critical.
- **Escalate on `web.config` exposed**: database connection strings, `machineKey`, and internal configuration visible → critical.
- **Escalate on `customErrors Off` or Developer Exception Page**: full stack traces with source code and server variables → high in production.
- **Escalate on `machineKey` exposed**: allows ViewState forgery, session forgery, and authentication-token generation → critical.
- **Escalate on unencrypted ViewState with sensitive data**: client-side state containing PII, roles, or internal identifiers without encryption → high.
- **Downgrade on server-header disclosure**: informational — suppress in production but low risk on its own.

## Prohibited behavior

- Attempting ViewState deserialization attacks or generating `ysoserial.net` payloads.
- Capturing or relaying NTLM challenge-response tokens (recording presence only).
- Exploiting Razor or ASPX template injection for code execution.
- Testing authentication endpoints with credentials, password sprays, or token-forging.
- Running IIS short-name scanners, WebDAV exploitation tools, or directory brute-force.
- Accessing or extracting `web.config`, `appsettings.json`, or `.git` directories if found exposed — record exposure and stop.

## Stop conditions

- `web.config` or `machineKey` exposed → stop, critical finding, do not extract further.
- `Trace.axd` accessible → stop, record exposure, do not view request traces containing other users' data.
- Developer Exception Page with source code and secrets → stop, record finding, redact any credentials found.
- ViewState deserialization vulnerability suggested but exploitation would be destructive → stop, record finding.
- Target not in scope or testing would impact production → stop.

## Evidence — .NET security matrix

For each target, record:

```text
Target: <URL> | Platform: <ASP.NET Framework X.Y | ASP.NET Core X.Y | Blazor>
Version evidence: <X-AspNet-Version | X-Powered-By | error page | swagger | behavioral>

Debug and error disclosure:
  Trace.axd: <exposed | not found | not applicable (Core)>
  customErrors mode: <Off — YSOD visible | On — custom errors | RemoteOnly>
  Developer Exception Page: <yes — stack trace | no>
  web.config accessible: <yes — critical | no>
  Swagger docs exposed: <yes — /swagger/ | no>

Authentication and authorization:
  Auth mechanism: <Forms | Windows/NTLM | JWT Bearer | Cookie | OAuth2 | none>
  NTLM Negotiate header: <present | absent>
  Auth bypass (unauthenticated): <yes — endpoint | no — 401/403>
  Anti-CSRF enforced: <yes — 400 on missing token | no — request processed | not tested>
  Role-protected paths accessible: <yes — path | no>

ViewState and session (WebForms only):
  __VIEWSTATE present: <yes | no — not WebForms>
  ViewState encrypted: <yes | no — plaintext>
  ViewState MAC signed: <yes | no — unsigned>
  machineKey exposure: <exposed in config/error/repo | not found>
  Session cookie HttpOnly: <yes | no>
  Session cookie Secure: <yes | no>
  Session cookie SameSite: <Lax | Strict | None>

Server hardening:
  Server header: <IIS/X.Y | Kestrel | suppressed>
  X-Powered-By: <ASP.NET | suppressed>
  X-AspNet-Version: <version | suppressed>
  IIS directory browsing: <enabled — path | disabled>
  IIS short names: <tilde requests accepted | blocked>
  WebDAV enabled: <PROPFIND allowed | disabled>

Security headers:
  CSP: <present — strong | present — weak | missing>
  HSTS: <present — max-age | missing on HTTPS>
  X-Content-Type-Options: <nosniff | missing>
  Frame protection: <X-Frame-Options | CSP frame-ancestors | missing>

Overall risk: <critical | high | medium | low>
```

Never store: `machineKey` values, database connection strings from `web.config`, `__VIEWSTATE` values containing sensitive user data, NTLM challenge/response tokens, authentication cookies, Swagger schemas with internal endpoint details, or error-page stack traces with server paths or credentials.

## Report handoff

1. `pentest_agent_record_finding` for: exposed `Trace.axd` or `web.config`, detailed error pages in production, missing anti-CSRF, authentication bypass, `machineKey` exposure, unencrypted ViewState, missing HTTPS/HSTS, and suppressed security headers.
2. Reference the .NET security matrix.
3. Recommend: set `<customErrors mode="On" />` or `ASPNETCORE_ENVIRONMENT=Production`, suppress `X-AspNet-Version`, `X-Powered-By`, and `Server` headers via `web.config` `<httpProtocol>` or `AddServerHeader = false` in Kestrel, enforce HTTPS with HSTS via `UseHttpsRedirection()` and `UseHsts()`, enable anti-CSRF with `[AutoValidateAntiforgeryToken]` in Core or `<pages enableViewStateMac="true">` in Framework, encrypt ViewState and set `<machineKey validation="SHA256" decryption="AES" />` (do not hardcode key values in config where they can be leaked), disable `Trace.axd` via `<trace enabled="false" />`, use `add-cors` with explicit origins and no `AllowCredentials` with wildcard, migrate from ASP.NET Framework to supported ASP.NET Core LTS releases, and apply monthly .NET security patches.
