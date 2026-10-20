---
name: payload-reference-ssrf
description: Server-Side Request Forgery reference framework — defensive taxonomy organized by request context (HTTP client, file fetcher, URL import, webhook), protocol allowlist bypass awareness, cloud metadata defense classification, safe canary strategy via controlled redirect to confirm reachability, and blind/OOB validation without data exfiltration.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [reference-notes, validation-plan, safe-canary-log, redaction-decision]
---

# Payload Reference SSRF

Use this skill as a defensive reference framework for Server-Side Request Forgery assessment. Organize payload knowledge by request context (HTTP client library, file-fetch function, URL import, webhook handler), protocol awareness, and the SSRF bypass landscape. Every payload discussion maps to a safe canary strategy — confirming the server can make outbound requests to a controlled destination without touching internal services, cloud metadata endpoints, or sensitive local resources. This skill is a reference and triage aid. It never provides active exploitation runbooks. All active validation routes through `pentest_agent_execute_tool` with authorization, scope, and approval gates.

## Required inputs

- Request context: the function that processes the user-supplied URL (HTTP client, image fetcher, PDF generator, webhook, file upload via URL, server-side redirect follower, SSI include, or XML parser with external entity support).
- URL placement: where user input appears (query parameter, POST body, JSON field, XML element, header value, or uploaded file metadata).
- Any observed URL validation: protocol restrictions (http/https only), domain allowlist/blocklist, IP range filtering, redirect-following behavior.
- Target and scope file when any live system is mentioned.
- Authorization cache before target contact.
- Desired output: validation plan, safe canary design, triage decision, or redaction guidance.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` when target context exists.
3. `pentest_agent_validate_target` before any live URL, host, API, or account is contacted.
4. `pentest_agent_check_authorization` before active validation, including outbound listener setup.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for all active checks.
6. `pentest_agent_append_evidence` for redacted notes.

## Defensive payload taxonomy

### Category 1 — reachability confirmation (safe canaries)

Goal: confirm the server makes outbound HTTP requests to a controlled, external destination without touching internal services.

**External callback service**: use Burp Collaborator, interactsh, or a self-hosted web listener with a unique subdomain per test. The server's request to `<unique>.collaborator.oastify.com` confirms outbound HTTP reachability. Record: DNS lookup time, HTTP request method, User-Agent header, and any custom headers.

**Controlled redirect canary**: set up an endpoint on your controlled server that returns an HTTP 302 redirect to a second unique Collaborator URL. If both URLs receive requests, the server follows redirects. Record whether the server follows 301, 302, 307 redirects.

**Safe IP canary**: point the target at a public IP you control. Confirm the request arrives. Do NOT point at `127.0.0.1`, `localhost`, `169.254.169.254`, `10.x.x.x`, `172.16.x.x`, or `192.168.x.x` in the initial canary — these are internal and their reachability alone may be a finding. External reachability first, internal only after scope explicitly permits internal probing.

### Category 2 — internal network classification (gated)

Goal: understand internal network access patterns, but only after scope explicitly permits internal probing. Never probe internal networks without written scope authorization.

**Internal destination categories** (reference for defense):
- AWS metadata: `http://169.254.169.254/latest/meta-data/` — instance metadata including IAM credentials.
- GCP metadata: `http://metadata.google.internal/computeMetadata/v1/` — requires `Metadata-Flavor: Google` header.
- Azure metadata: `http://169.254.169.254/metadata/instance?api-version=2021-02-01` — requires `Metadata: true` header.
- DigitalOcean metadata: `http://169.254.169.254/metadata/v1/`.
- Oracle Cloud metadata: `http://169.254.169.254/opc/v1/`.
- Alibaba Cloud metadata: `http://100.100.100.200/latest/meta-data/`.
- Kubernetes API: `https://kubernetes.default.svc`, `http://localhost:10250`, `http://localhost:10255`.
- Docker socket: `http://localhost:2375`, `http://localhost:2376` (TLS), `unix:///var/run/docker.sock`.
- Local loopback: `http://127.0.0.1/`, `http://localhost/` — access to loopback confirms the server can reach itself, potentially accessing admin interfaces not exposed externally.
- Link-local (APIPA): `http://169.254.0.0/16` excluding `169.254.169.254` (cloud metadata).
- Private subnets: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.

**Validation gating**: internal probing requires:
1. Scope explicitly listing internal networks as in-scope.
2. Authorization proof covering internal infrastructure.
3. Explicit approval for internal probing — never infer authorization for internal testing from external scope.

### Category 3 — protocol and scheme bypass awareness (reference only)

Goal: understand URL parser inconsistencies that allow protocol bypass for defense assessment.

**URL scheme bypass**:
- `file:///etc/passwd` — direct file read; blocked by most modern HTTP clients.
- `gopher://` — legacy protocol; can be used to craft raw TCP streams to internal services (SMTP, Redis, Memcached).
- `dict://` — Dictionary protocol; can probe internal service banners (`dict://localhost:6379/info` probes Redis).
- `ftp://` — FTP protocol; may be allowed by misconfigured URL fetchers.
- `sf://` / `sftp://` — Secure File Transfer.
- `ldap://` — LDAP injection via URL fetcher.
- `jar://` — Java JAR protocol handler; can trigger remote class loading.

**URL parser bypass (reference)**:
- Using credentials in URL to confuse host parser: `http://expected-host@attacker.com/` — some parsers treat `expected-host` as the username, `attacker.com` as the host.
- Using IP address encoding to bypass string-based blocklists: `http://2130706433/` (decimal encoding of `127.0.0.1`), `http://0x7f.0x00.0x00.0x01/`, `http://0177.0.0.01/` (octal), `http://127.0.0.1.nip.io/` (DNS rebinding service).
- Using DNS rebinding: domain that resolves to different IPs over time (`1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.xip.io`).
- Using URL shorteners or redirect services that redirect to internal IPs.
- IPv6: `http://[::1]/` or `http://[0:0:0:0:0:0:0:1]/` for loopback.
- Enclosed alphanumerics: Unicode characters that render as IP digits may bypass filters that check ASCII only.

Reference only for defense assessment and WAF/validation design. Do not execute protocol bypass, URL parser bypass, or DNS rebinding in active testing without explicit authorization for bypass techniques.

### Category 4 — blind SSRF and out-of-band patterns

Goal: confirm SSRF when the response is not returned to the attacker (blind SSRF).

**Blind confirmation techniques**:
- DNS callback only: the server resolves the Collaborator hostname (DNS lookup) but does not complete the HTTP request. Confirms the URL is parsed and host resolution occurs, but not that an HTTP connection is made.
- HTTP callback with no response body: the server completes the request but does not include the response in the application output. Confirmed by Collaborator receiving an HTTP request.
- TCP handshake only (half-open): the server initiates a TCP SYN to the listener but does not send an HTTP request. Indicates a non-HTTP protocol or connection timeout.

**Blind SSRF to internal service probing**: when the response is not visible but the timing differs. If a request to `http://localhost:80/` (valid internal web service) returns faster than a request to `http://localhost:19999/` (no service), a timing differential confirms reachability of the port. This is noisy and requires careful baseline measurement. Use only with explicit internal probing authorization.

### Category 5 — cloud and container-specific awareness (reference)

Goal: understand cloud metadata and container SSRF vectors for defense assessment.

**Cloud metadata endpoints** (reference for defense; do not probe without explicit cloud infrastructure authorization):
- AWS IMDSv1: `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>` — returns temporary IAM credentials. IMDSv2 requires a PUT request first to obtain a token, which most SSRF vectors cannot issue (HTTP clients default to GET). IMDSv2 provides defense-in-depth but is not a complete SSRF mitigation.
- GCP: `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token` — requires `Metadata-Flavor: Google` header. Most SSRF vectors cannot add custom headers without control over the HTTP client configuration.
- Azure: Similar to AWS, but requires `Metadata: true` header.
- Kubernetes: `https://kubernetes.default.svc` — the Kubernetes API server; requires a service account token from `/var/run/secrets/kubernetes.io/serviceaccount/token`. An SSRF that can read local files AND make HTTP requests can combine both to authenticate to the Kubernetes API.

**Container escape awareness via SSRF** (reference for defense):
- Docker socket (`/var/run/docker.sock`): an SSRF that can reach the Docker socket via `file://` or through an HTTP client running on the host can create containers with host filesystem mounts, enabling container escape.
- containerd socket (`/run/containerd/containerd.sock`).
- CRI-O socket (`/var/run/crio/crio.sock`).

**Serverless** (AWS Lambda, Google Cloud Functions, Azure Functions):
- Lambda runtime API: `http://127.0.0.1:9001/2018-06-01/runtime/invocation/next` — the Lambda runtime internal API; accessible only within the execution environment.

## Decision points

- **External canary succeeds → confirm outbound HTTP**: record the request details. Do not escalate to internal probing without separate scope authorization covering internal networks.
- **External canary with redirect succeeds → confirm redirect-following**: record the redirect chain. Note that redirect-following can be used to reach internal IPs if the redirect target is `127.0.0.1` — do not test this without internal authorization.
- **Only DNS callback received → confirm URL parsing and host resolution**: SSRF is present but limited; the HTTP client may restrict protocols or the target may be unreachable. Document limitation.
- **Cloud metadata endpoint returned data → critical finding, stop probing**: the presence of cloud metadata access is itself a critical finding. Do not enumerate further metadata paths. Recommend IMDSv2 enforcement immediately.
- **Internal service banner returned → confirm internal access**: STOP. Do not enumerate further internal services. Document the accessible service and recommend network segmentation.
- **File read via `file://` succeeded → confirm local file access**: STOP immediately. Do not read additional files. Document the inclusion vector.

## Prohibited behavior

- Probing cloud metadata endpoints without explicit cloud infrastructure authorization.
- Enumerating internal IP ranges, ports, or services beyond a single confirmatory canary.
- Accessing Docker socket, Kubernetes API, or container runtime endpoints.
- Reading local files via `file://`, `gopher://`, or any scheme beyond the initial HTTP canary.
- Using DNS rebinding to bypass IP-based access controls.
- Using URL parser bypass techniques to reach internal or blocked destinations.
- Injecting SSRF payloads into webhook handlers that trigger outbound requests to third-party services (can cause collateral impact).
- Setting up persistent listeners that capture traffic beyond the test session.
- Providing step-by-step exploitation recipes beyond safe product behavior and defensive reference.

## Stop conditions

- External canary fails after testing multiple Collaborator domains and URL placements → stop, document SSRF not confirmed at tested injection points.
- ANY response from an internal destination → stop, document the accessible internal resource, and do not enumerate further.
- Cloud metadata endpoint returns any data → stop, critical finding, recommend immediate IMDSv2 enforcement.
- DNS callback resolves to internal IP via DNS rebinding service → stop, this is out of scope for passive validation.
- Collaborator receives unexpected third-party requests during testing → stop, investigate possible interference or out-of-scope impact.

## Evidence

Record: affected parameter and URL placement, outbound confirmation (DNS only, HTTP, HTTP with redirect), Collaborator/interactsh interaction ID (for verification, not the raw interaction content), User-Agent or identifying headers from the server's request, redirect-following behavior, and any protocol restrictions observed.

Never store: cloud metadata response content, internal service banner output, file contents from `file://` reads, Collaborator interaction bodies containing sensitive server data, or internal IP addresses beyond the minimal confirmatory canary.

## Report handoff

1. When an SSRF surface is confirmed, hand off to `vuln-ssrf` for active validation with `pentest_agent_execute_tool`.
2. Reference this payload taxonomy in the finding as the detection rationale — link the canary type used (DNS vs HTTP), the protocol reach confirmed, and the outbound behavior observed.
3. If redirect-following or protocol restrictions were identified, include them in the handoff notes to guide the active validator.
4. Recommend: input allowlisting for URLs (protocol + hostname + path), network egress restrictions at the host/firewall level, disable redirect-following in HTTP clients used for user-supplied URLs, and block access to cloud metadata endpoints (169.254.169.254) and internal IP ranges.
