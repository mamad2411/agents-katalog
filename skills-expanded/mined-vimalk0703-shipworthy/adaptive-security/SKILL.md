---
name: adaptive-security
description: Use when building any application to automatically detect the software type and apply appropriate security measures. Covers web apps, APIs, mobile backends, CLI tools, data pipelines, IoT, desktop apps, and infrastructure.
invoke_when: Use when starting a new project, adding security-sensitive features, or when the security-first-development skill identifies the need for application-type-specific security measures.
---

# Adaptive Security Framework

## Core Rule

**Security is not one-size-fits-all.** A CLI tool has different attack surfaces than a web app. An IoT device faces different threats than a data pipeline. This skill detects the type of software being built and activates the correct security profile automatically.

Always apply the Cross-Cutting Security baseline (Section 12) regardless of application type, then layer on the type-specific profile.

## 1. Application Type Detection

Before writing or reviewing security-sensitive code, identify the application type by scanning the project for these signals:

| Signal | App Type | Security Profile |
|--------|----------|-----------------|
| `next.config.*`, React, Vue, Angular, `index.html` with SPA router | Web Application | Web Security Profile |
| Express, FastAPI, Gin, `routes/`, REST controllers | REST API | API Security Profile |
| GraphQL schema, resolvers, `typeDefs` | GraphQL API | GraphQL Security Profile |
| React Native, Flutter, iOS/Android dirs, mobile SDK refs | Mobile Backend | Mobile Security Profile |
| CLI args, commander, yargs, cobra, `process.argv` parsing | CLI Tool | CLI Security Profile |
| Kafka, RabbitMQ, Celery, Airflow, `dag/`, stream processors | Data Pipeline | Pipeline Security Profile |
| MQTT, GPIO, embedded, firmware, device SDKs | IoT/Edge | IoT Security Profile |
| Electron, Tauri, `main`/`renderer` process split | Desktop App | Desktop Security Profile |
| Terraform, Pulumi, CloudFormation, `.tf` files | Infrastructure | IaC Security Profile |
| Dockerfile, `docker-compose.yml`, container orchestration | Container | Container Security Profile |

**Multiple profiles can apply simultaneously.** A project with a React frontend, Express API, and Dockerfile should activate Web + API + Container profiles.

If the application type is ambiguous, ask the user. Do not guess and skip a profile.

## 2. Web Application Security Profile

Apply the full OWASP Top 10 checklist, plus these concrete measures:

- **Content-Security-Policy (CSP):** Set a strict CSP header. At minimum: `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'`. Tighten further for production. Never use `unsafe-eval`.
- **CORS:** Configure explicit origin allowlists. Never use `Access-Control-Allow-Origin: *` in production. Reflect only known origins.
- **XSS Prevention:** Rely on framework auto-escaping (React, Vue, Angular all do this). For user-generated HTML, sanitize with DOMPurify. Never use `dangerouslySetInnerHTML` or `v-html` with unvalidated content.
- **CSRF Protection:** Use anti-CSRF tokens for state-changing requests. Set `SameSite=Strict` or `SameSite=Lax` on session cookies. For SPAs using JWTs, store tokens in memory (not localStorage).
- **Clickjacking Prevention:** Set `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` (or restrict to specific parents).
- **HTTPS Enforcement:** Set `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`. Redirect all HTTP to HTTPS.
- **Cookie Security:** All session/auth cookies must be `HttpOnly`, `Secure`, and `SameSite=Strict`. Set the `Path` to the narrowest scope needed.
- **Subresource Integrity (SRI):** Every CDN-loaded script or stylesheet must have an `integrity` attribute with a SHA-384 or SHA-512 hash.
- **Rate Limiting:** Apply rate limits on login, registration, password reset, and all form submission endpoints. Return `429` with `Retry-After` header.

## 3. REST API Security Profile

- **Authentication:** Use JWT with short expiry (15 minutes) plus refresh tokens with rotation, OR API keys with mandatory rotation schedules. Never use long-lived bearer tokens without refresh.
- **Authorization:** Implement RBAC or ABAC. Check permissions on every request at the handler level, not just middleware. Default deny -- explicitly grant access.
- **Input Validation:** Schema-validate every request body and query parameter. Use Zod (TypeScript), Pydantic (Python), or `validator` (Go). Reject unknown fields.
- **Output Filtering:** Never return entire database rows. Select only the fields the client needs. Implement response schemas to prevent accidental data leakage.
- **Rate Limiting:** Tier by user, IP, and endpoint. Auth endpoints get stricter limits (e.g., 5 attempts/minute for login). Public endpoints get per-IP limits. Authenticated endpoints get per-user limits.
- **Request Size Limits:** Set `body-parser` limits (e.g., `100kb`). Reject oversized payloads before processing.
- **API Versioning:** Version your API from day one (`/v1/`). This allows deploying security patches without breaking existing clients.
- **Webhook Signature Verification:** All outgoing webhooks must be signed (HMAC-SHA256). All incoming webhooks must verify signatures before processing.
- **CORS:** Explicit origin allowlist. Never wildcard.
- **OpenAPI Security Definitions:** Document security schemes in your OpenAPI/Swagger spec. Every endpoint must declare its security requirements.

## 4. GraphQL API Security Profile

GraphQL's flexibility creates unique attack vectors. Apply these controls:

- **Query Depth Limiting:** Set a maximum query depth (e.g., 10 levels). Reject queries that exceed it. Use `graphql-depth-limit` or equivalent.
- **Query Complexity Analysis:** Assign complexity scores to fields. Reject queries that exceed a total complexity budget. This prevents attackers from crafting expensive queries.
- **Introspection Disabled in Production:** Disable the `__schema` and `__type` introspection queries in production. Attackers use introspection to map your entire API surface.
- **Field-Level Authorization:** Check permissions at the resolver level, not just the query level. A user authorized to read `User.name` may not be authorized to read `User.email`.
- **Persisted Queries:** In production, accept only pre-registered query hashes. Reject arbitrary queries. This prevents query injection and abuse.
- **Batching Limits:** Limit the number of queries in a single batch request (e.g., max 10). Unbounded batching enables denial-of-service.
- **Timeout Per Query:** Set execution timeouts (e.g., 10 seconds). Kill long-running queries.

## 5. Mobile Backend Security Profile

Mobile clients operate in hostile environments. The backend must compensate:

- **Certificate Pinning Support:** Provide pinning configuration for mobile clients. Rotate pins gracefully with backup pins.
- **Token Storage Guidance:** Document that tokens must be stored in iOS Keychain or Android Keystore. Never SharedPreferences, UserDefaults, or localStorage.
- **Biometric Auth Integration:** Support biometric-gated token refresh. Issue short-lived tokens that require biometric re-authentication to renew.
- **Offline Data Encryption:** Any data cached on-device must be encrypted. Provide encryption keys tied to the user's authentication state.
- **API Key Obfuscation:** API keys must never appear in client bundles. Use backend proxies for third-party API calls. Mobile binaries are trivially decompiled.
- **Push Notification Security:** Encrypt notification payloads. Never include sensitive data in the notification preview text.
- **Device Attestation:** Verify device integrity via SafetyNet (Android) or DeviceCheck/App Attest (iOS). Reject requests from compromised devices.
- **Session Management:** Issue device-bound tokens. A token issued to Device A must not work on Device B. Include device fingerprint in token claims.

## 6. CLI Tool Security Profile

CLI tools run with the user's full permissions. Handle this responsibly:

- **Never Log Secrets:** Do not print API keys, tokens, passwords, or credentials to stdout or stderr. Mask sensitive values in all output.
- **Credential Storage:** Use the OS keychain (macOS Keychain, Windows Credential Manager, `libsecret` on Linux). Never store credentials in plaintext config files like `~/.myapp/config.json`.
- **Input Sanitization for Shell Commands:** If the tool executes shell commands, never interpolate user input into command strings. Use argument arrays: `execFile('cmd', [arg1, arg2])`, not `exec('cmd ' + userInput)`.
- **Argument Validation:** Reject unexpected flags and arguments. Use a strict argument parser that fails on unknown input rather than silently ignoring it.
- **File Permission Checks:** Files created by the tool must have restrictive permissions. Config files: `0600`. Never write world-readable files containing credentials.
- **Temporary File Cleanup:** Clean up all temporary files on exit, including on crash. Use OS-provided temp directories with unique names.
- **Update Verification:** If the tool has auto-update, verify release signatures before applying. Use code signing for distributed binaries.
- **No Telemetry Without Consent:** Never collect usage data without explicit opt-in. Provide a clear `--no-telemetry` flag and respect it.

## 7. Data Pipeline Security Profile

Pipelines process data at scale. A breach here exposes everything:

- **Data Classification:** Tag every field as Public, Internal, Confidential, or Restricted (PII, PHI, PCI). This classification drives all downstream decisions.
- **Encryption:** Encrypt data at rest (encrypted volumes, encrypted S3 buckets) and in transit (TLS for all connections). No exceptions.
- **Access Control Per Stage:** Each pipeline stage should have its own credentials with access only to the data it needs. The ingestion stage should not have access to the reporting database.
- **Audit Logging:** Log every data access: who, what, when, from where. These logs must be immutable and retained per policy.
- **Data Retention Policies:** Implement automated deletion. Data that has exceeded its retention period must be purged, not just ignored.
- **PII Masking:** Mask PII in logs, error messages, and monitoring dashboards. Log `user_id=***` not `user_id=john.doe@example.com`.
- **Schema Validation at Ingestion:** Validate every record against an expected schema at the point of entry. Reject malformed data early.
- **Dead Letter Queue Security:** Failed messages in DLQs may contain sensitive data. Apply the same access controls and encryption to DLQs as to primary queues.
- **Secrets Management for Connections:** Database passwords, API keys, and connection strings must come from a secrets manager. Never hardcode them in pipeline definitions or DAG files.

## 8. IoT/Edge Security Profile

IoT devices are deployed in the field, physically accessible to attackers, and rarely updated:

- **Firmware Update Verification:** Sign all firmware updates. Devices must verify signatures before applying updates. Reject unsigned or tampered firmware.
- **Minimal Attack Surface:** Disable all unused ports, services, and protocols. If the device does not need SSH, disable it. If it does not need Bluetooth, disable it.
- **Mutual TLS:** Use mutual TLS (mTLS) for device-to-cloud communication. Both the device and the server authenticate each other.
- **Secure Boot Chain:** Implement a chain of trust from bootloader to application. Each stage verifies the next before executing it.
- **Physical Tamper Detection:** Where possible, detect physical tampering and respond by wiping credentials or entering a lockdown state.
- **Rate Limiting on Device APIs:** Device-side APIs must rate-limit requests to prevent local network attacks from overwhelming the device.
- **Data Minimization:** Transmit only the data needed for the current operation. Do not stream raw sensor data when aggregates suffice.
- **Credential Rotation:** Long-lived devices must rotate credentials on a schedule. Design the rotation protocol before deployment -- retrofitting is nearly impossible.

## 9. Desktop App Security Profile

Desktop apps have broad system access. Contain the blast radius:

- **IPC Channel Validation (Electron):** Validate every message on every IPC channel. Never trust data from the renderer process. Define an explicit allowlist of IPC methods.
- **No Node.js in Renderer (Electron):** Set `nodeIntegration: false` and `contextIsolation: true`. Use a preload script with a minimal, explicitly defined `contextBridge` API.
- **Code Signing:** Sign all release binaries. Unsigned apps trigger security warnings and may be blocked by OS gatekeeper systems.
- **Auto-Update Security:** Verify update signatures before applying. Use a secure update channel (HTTPS with certificate pinning). Never download and execute unsigned code.
- **Local Data Encryption:** Encrypt local databases (SQLCipher for SQLite). Encrypt sensitive files at rest. Derive encryption keys from user credentials, not hardcoded keys.
- **Sandboxing:** Enable OS-level sandboxing. On Electron, enable the sandbox for all renderer processes. Request only the OS permissions the app actually needs.
- **No Remote Code Execution:** Never download and execute code from remote servers. Never use `eval()` on remote data. Never load remote scripts into the renderer.

## 10. Infrastructure as Code Security Profile

IaC defines your entire infrastructure. A misconfiguration here is a breach:

- **No Secrets in IaC Files:** Never put passwords, API keys, or tokens in `.tf`, CloudFormation templates, or Pulumi code. Reference secrets from a secret manager.
- **Least Privilege IAM:** Every IAM role and policy must follow least privilege. No `Action: *` or `Resource: *`. Define exactly what each role can do.
- **Encryption Enabled by Default:** Enable encryption on every storage resource: S3 buckets (SSE-S3 or SSE-KMS), RDS instances (encryption at rest), EBS volumes, SQS queues.
- **Network Segmentation:** Place databases and internal services in private subnets. Only load balancers and API gateways go in public subnets. No direct internet access for backend services.
- **Logging Enabled:** Enable CloudTrail, VPC Flow Logs, S3 access logging, and RDS audit logging. Send logs to a central, immutable log store.
- **Drift Detection:** Run regular drift detection to catch manual changes that bypass IaC. Remediate drift immediately.
- **Policy as Code:** Use OPA (Open Policy Agent), Sentinel, or Checkov to enforce security policies. Block deployments that violate policies.

## 11. Container Security Profile

Invoke the `container-security` skill for the full checklist. Key highlights:

- **Non-Root User:** All containers must run as a non-root user. Set `USER` in the Dockerfile.
- **Minimal Base Images:** Use `distroless`, `-slim`, or `-alpine` variants. Smaller images have fewer vulnerabilities.
- **No Secrets in Dockerfiles:** Never `COPY .env` or set `ENV SECRET=`. Use BuildKit secret mounts for build-time secrets. Inject runtime secrets via orchestration.
- **Read-Only Filesystem:** Mount the root filesystem as read-only where possible. Write only to explicitly defined volumes.
- **Resource Limits:** Set CPU and memory limits. A compromised container should not be able to starve the host.
- **Health Checks:** Define `HEALTHCHECK` instructions. Orchestrators use these to detect and restart compromised containers.
- **Image Scanning in CI:** Scan every image with Trivy, Snyk, or Docker Scout before pushing. Block images with CRITICAL vulnerabilities.
- **Signed Images:** Sign images with cosign or Docker Content Trust. Verify signatures before deploying.

## 12. Cross-Cutting Security (ALL Profiles)

These apply to every application type, no exceptions:

- **Secrets Management:** Environment variables validated at startup with clear error messages for missing values. `.env` files must be in `.gitignore`. Use `secrets-management` skill for full guidance.
- **Dependency Scanning:** Run `npm audit`, `pip audit`, or `govulncheck` before every commit. No critical vulnerabilities in production dependencies. Use `supply-chain-security` skill for full guidance.
- **Static Analysis (SAST):** Run static analysis in CI. Use Semgrep, CodeQL, or language-specific tools (ESLint security plugin, Bandit for Python).
- **Logging Hygiene:** Never log passwords, tokens, API keys, session IDs, or PII. Log request IDs and user IDs for traceability, but mask everything sensitive.
- **Error Handling:** Never expose stack traces, internal paths, or database errors to end users. Return generic error messages externally; log detailed errors internally.
- **Authentication:** Use established libraries. Never implement your own password hashing, token generation, or session management from scratch. Never roll your own crypto.

## 13. Rationalization Pressure Test

When someone suggests skipping a security measure, counter with this table:

| Excuse | Counter |
|--------|---------|
| "We'll add security later" | Security retrofits cost 10x more than building it in. The architecture may not support it later. Do it now. |
| "It's just an internal tool" | Internal tools get compromised via phishing, stolen credentials, and lateral movement. Internal does not mean safe. |
| "Nobody would attack us" | Automated scanners attack every public endpoint within hours of deployment. It is not personal; it is automated. |
| "We're too small to be a target" | Small companies are preferred targets because they have weaker defenses. Size does not equal safety. |
| "That's overkill for an MVP" | An MVP with a data breach is not viable. The M in MVP stands for Minimum, not Minimal Security. |
| "The framework handles it" | Frameworks provide tools, not guarantees. Misconfigured frameworks are the #1 source of web vulnerabilities. |
| "We use HTTPS, so we're secure" | HTTPS protects data in transit. It does nothing for injection, broken auth, IDOR, misconfigurations, or supply chain attacks. |
| "We don't store sensitive data" | You store passwords, emails, and session tokens. That is sensitive data. You probably also store IP addresses and user behavior -- also sensitive under GDPR. |
| "Our users trust us" | Trust is why they gave you their data. Breaching that trust has legal, financial, and reputational consequences. |
| "Security slows down development" | A breach slows down development for months. An hour spent on security now saves weeks of incident response later. |

## Activation Protocol

When this skill is invoked:

1. Scan the project to identify application type(s) using the detection table in Section 1.
2. Activate all matching security profiles.
3. Apply the Cross-Cutting Security baseline (Section 12) unconditionally.
4. When writing or reviewing code, check against the active profiles.
5. If a security measure from an active profile is missing, flag it and implement it.
6. If someone pushes back on a security measure, consult the Rationalization Pressure Test (Section 13).
