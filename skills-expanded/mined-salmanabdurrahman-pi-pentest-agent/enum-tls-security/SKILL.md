---
name: enum-tls-security
description: TLS and transport security enumeration across all in-scope endpoints. Covers protocol version support, cipher suite analysis, certificate chain validation, HSTS enforcement, and TLS configuration gaps. Passive-first collection with active probing gated by authorization and scope validation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, tls-config-audit, cipher-suite-report, certificate-inventory]
---

# Enum TLS security

Use this skill to enumerate TLS and transport-layer security configurations across all in-scope targets. TLS misconfigurations expose data in transit to interception and downgrade attacks. This skill audits protocol support, cipher strength, certificate validity, and HSTS enforcement without performing active man-in-the-middle or downgrade attacks.

## Required inputs

- Validated target list with hostnames and ports for all in-scope TLS endpoints.
- Scope file defining allowed testing methods, ports, and rate limits.
- Authorization cache valid for all in-scope hosts.
- Optional: expected certificate details or TLS policy documentation provided by the target owner.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every target before contact.
3. Use `pentest_agent_check_authorization` before any active TLS probing.
4. Use `pentest_agent_build_command` for dry-run preview of TLS scanning tools.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for TLS configuration audit results, cipher reports, and certificate inventories.

## Workflow

### Phase 1 — Endpoint and port identification

Identify all TLS endpoints before probing individual configurations.

- Enumerate all in-scope hostnames. TLS certificates are bound to hostnames, not IPs; test every hostname, including subdomains discovered during recon.
- Identify TLS-enabled ports. Standard: 443 (HTTPS), 8443, 9443. Non-standard: 465 (SMTPS), 993 (IMAPS), 995 (POP3S), 636 (LDAPS), 3389 (RDP with TLS), 5432 (PostgreSQL with TLS), 3306 (MySQL with TLS). Only probe ports explicitly in scope.
- For web endpoints, confirm TLS by connecting via HTTPS. A redirect from HTTP to HTTPS is expected; a missing redirect is a separate finding.
- For non-web services, test whether TLS is offered by initiating a TLS handshake. Some services offer STARTTLS (protocol-level upgrade) rather than implicit TLS; test both.
- Document the full TLS endpoint inventory: hostname, IP, port, service type, and whether TLS is confirmed.

### Phase 2 — Protocol version enumeration

Determine which TLS and SSL protocol versions each endpoint supports.

- Use catalog TLS scanning tools to probe supported protocol versions: SSL 2.0, SSL 3.0, TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3.
- Flag any endpoint supporting SSL 2.0 or SSL 3.0. These protocols are broken by design (POODLE, DROWN) and should never be enabled.
- Flag any endpoint supporting TLS 1.0 or TLS 1.1. These protocols are deprecated by PCI DSS and major browsers. They lack modern cipher suites and are vulnerable to downgrade attacks.
- Flag any endpoint that does not support TLS 1.3. While TLS 1.2 remains secure, the absence of TLS 1.3 means the endpoint misses forward-secrecy-by-default, 0-RTT resumption, and improved cipher suites.
- Check whether the endpoint negotiates the highest offered protocol version or accepts downgrade. Test by offering only TLS 1.0 in the client hello. If the server accepts, it is downgrade-vulnerable.
- Document supported protocol versions per endpoint.

### Phase 3 — Cipher suite analysis

Audit the cipher suites offered by each endpoint.

- Enumerate all cipher suites offered by the server in the TLS handshake. Group by key exchange method (RSA, DHE, ECDHE), authentication (RSA, ECDSA), encryption algorithm (AES-GCM, AES-CBC, ChaCha20, 3DES, RC4), and hash (SHA-256, SHA-384).
- Flag dangerous cipher suites:
  - `RC4`: broken, stream-cipher weaknesses.
  - `3DES`: Sweet32 birthday attack, effective key strength ~112 bits.
  - `CBC` mode without `encrypt_then_mac`: vulnerable to padding-oracle attacks (Lucky13, POODLE).
  - `EXPORT` ciphers: deliberately weakened to 40-56 bits (FREAK, Logjam).
  - Anonymous key exchange (`aNULL`, `ADH`): no server authentication, enabling man-in-the-middle.
  - `NULL` encryption (`eNULL`): no encryption, plaintext transmission over TLS.
  - `MD5` hash: collision-vulnerable.
  - Static RSA key exchange (not `DHE` or `ECDHE`): no forward secrecy.
- Check whether the server prefers strong cipher suites. The server's cipher preference order determines which suite is negotiated; a weak cipher ranked above strong ciphers is exploitable.
- Check for cipher suite consistency across endpoints. A load-balanced endpoint with different cipher configurations on different backends causes unpredictable security behavior.
- Document the cipher suite inventory with risk flags per cipher.

### Phase 4 — Certificate chain validation

Validate every certificate in the chain presented by each endpoint.

- Retrieve the full certificate chain: leaf certificate, intermediate certificate(s), and root certificate.
- Check the leaf certificate:
  - Subject Common Name (CN) and Subject Alternative Names (SANs). Flag if the target hostname does not appear in the SAN list.
  - Validity period: Not Before and Not After dates. Flag if the certificate is expired or will expire within 30 days.
  - Key type and size: RSA 2048+, ECDSA P-256+. Flag RSA keys smaller than 2048 bits or ECDSA keys on non-standard curves.
  - Signature algorithm: SHA-256 with RSA or ECDSA. Flag SHA-1 signatures (deprecated, collision-vulnerable).
  - Extended Key Usage: must include `serverAuth` for server certificates.
- Check the intermediate certificates:
  - Flag missing intermediate certificates (incomplete chain). Clients may fail to build the trust path.
  - Flag intermediates signed with SHA-1.
  - Flag intermediates with keys too small to provide adequate security.
- Check certificate revocation status:
  - OCSP responder URL in the Authority Information Access (AIA) extension. Test whether the OCSP responder is reachable.
  - CRL Distribution Points. Test whether CRLs are accessible.
  - Flag certificates with no revocation information.
- Check for Certificate Transparency (CT): flag certificates without embedded Signed Certificate Timestamps (SCTs) on platforms that require CT (publicly trusted certificates issued after April 2018).
- Document certificate details per endpoint: issuer, subject, SANs, validity, key size, signature algorithm.

### Phase 5 — HSTS and HTTPS enforcement

Audit the application-layer enforcement of TLS.

- For each HTTPS endpoint, verify the `Strict-Transport-Security` header presence and value (see enum-headers-cookies for detailed HSTS audit).
- Test whether HTTP endpoints redirect to HTTPS. Send an HTTP request to port 80 for each hostname. Flag if the server responds with 200 OK over HTTP (no redirect).
- Test whether the HTTP-to-HTTPS redirect uses a 301 (permanent) or 302 (temporary) status. 301 is correct for permanent HTTPS enforcement. 302 with a short HSTS max-age may not be cached.
- Test whether subdomains are covered by HSTS. If the apex domain sets `includeSubDomains`, verify that subdomains also serve HTTPS.
- Test for mixed-content risks on pages that load resources over HTTP. While this is a content issue rather than TLS configuration, flag it as a related finding.
- Document HSTS and redirect posture per endpoint.

### Phase 6 — TLS extension and feature enumeration

Modern TLS includes extensions that improve security. Audit their presence.

- Check for Server Name Indication (SNI) support. The server must accept different certificates based on the SNI hostname. Flag if the server returns the same certificate for all hostnames (possible shared hosting or misconfigured virtual hosts).
- Check for OCSP Stapling (TLS Certificate Status Request extension). The server should staple a fresh OCSP response to the TLS handshake, improving revocation-check performance and privacy.
- Check for Session Ticket and Session ID support. Session resumption improves performance but the session ticket key must be rotated. Flag if session tickets are enabled without evidence of rotation.
- Check for Application-Layer Protocol Negotiation (ALPN): `h2` (HTTP/2) and `http/1.1`. Flag if HTTP/2 is not offered when the application benefits from it.
- Check for TLS compression (CRIME attack vector). Flag if compression is enabled.
- Check for TLS renegotiation: secure renegotiation (RFC 5746) must be supported; insecure renegotiation enables prefix-injection attacks.
- Check for TLS Fallback SCSV support to prevent protocol downgrade attacks triggered by network failures.
- Document TLS extension support per endpoint.

## Decision points

- Port scanning: only probe TLS ports explicitly listed in scope. If the scope allows service discovery, probe common TLS ports but stop at the scope boundary.
- Certificate validation: if the certificate is issued by a private CA for internal use, flag the private CA trust model but do not apply public-CT expectations. Internal CAs without CT are acceptable within the organization's PKI.
- Cipher audit depth: if the server offers 30+ cipher suites, audit the top-priority 10 and flag any weak ciphers anywhere in the list. A weak cipher at the bottom of the list is still exploitable if the client offers only that cipher.
- Session resumption: if session tickets are detected, note the risk but do not attempt ticket-key extraction or reuse (that requires access to server memory, which is out of scope for enumeration).

## Prohibited behavior

No man-in-the-middle interception of TLS connections. No downgrade attacks that actively modify the TLS handshake. No extraction or offline cracking of private keys, session tickets, or pre-master secrets. No probing of TLS ports outside the authorized scope. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop on an endpoint when protocol versions, cipher suites, certificate details, HSTS posture, and TLS extensions are fully documented. Stop if the endpoint closes connections or rate-limits TLS handshakes. Stop if the authorization cache expires.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- TLS endpoint inventory with confirmed ports and service types.
- Protocol version support matrix per endpoint with risk flags.
- Cipher suite inventory with algorithm breakdown and weak-cipher flags.
- Certificate chain details: issuer, subject, SANs, validity period, key size, signature algorithm, revocation status.
- HSTS and HTTPS-redirect posture per hostname.

Never store private keys, session ticket values, pre-master secrets, or raw certificate files containing internal PKI information. Redact certificate serial numbers, OCSP URLs containing internal hostnames, and CRL distribution points if they expose internal infrastructure.

## Report handoff

Record findings via `pentest_agent_record_finding` for: SSL 2.0/3.0 enabled (critical), TLS 1.0/1.1 enabled (high), weak cipher suites (high for RC4/EXPORT/NULL; medium for 3DES/CBC without encrypt-then-MAC), missing forward secrecy (medium), expired certificate (critical), certificate hostname mismatch (high), weak key size <2048 bits (high), SHA-1 signature (medium), missing HSTS (high), HTTP without HTTPS redirect (high), and TLS compression enabled (medium). Generate the TLS audit as structured evidence. Render the final report with `pentest_agent_render_report`.
