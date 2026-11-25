---
name: network-security
description: TLS 1.3 enforcement, certificate verification, egress traffic governance, DNS rebinding mitigation, and safe HTTP client pooling
---
# Network Transport Security & Hardening

## 1. Modern TLS 1.3 Enforcement
Mandate TLS 1.3 as the default transport protocol, permitting TLS 1.2 as minimum fallback. Enforce secure cipher suites with ephemeral Diffie-Hellman key exchange (ECDHE). Permanently disable deprecated ciphers, RC4, 3DES, and CBC mode suites.

## 2. Certificate Verification & Mutual TLS (mTLS)
Enforce strict X.509 certificate chain validation using system trust stores. Validate Subject Alternative Name (SAN) match. For microservice-to-microservice traffic, enforce mutual TLS (mTLS) with client certificate verification.

## 3. Egress Traffic Governance
Implement default-deny outbound network egress policies for production and sandbox environments. Maintain an explicit allowlist of authorized external domains, ports, and API destinations. Route external requests through an egress proxy.

## 4. DNS Rebinding & Host Header Validation
Validate incoming Host and X-Forwarded-Host headers against an explicit list of authorized domain names. Reject unexpected hostnames with HTTP 400 Bad Request to eliminate DNS rebinding attack vectors.

## 5. Safe HTTP Client Configuration
Never instantiate unbounded default HTTP clients. Explicitly configure connect timeouts (max 5s), TLS handshake timeouts (max 5s), response header timeouts (max 10s), and idle connection pool limits to prevent connection exhaustion.

## 6. Slowloris & Connection Exhaustion Defense
Configure web servers and reverse proxies with strict read header timeouts (max 5s) and idle keep-alive timeouts. Limit maximum concurrent connections per IP address to mitigate Slowloris and resource starvation attacks.

## 7. Private Subnet & VPC Isolation
Place databases, cache clusters, and internal management interfaces inside private subnets with no direct public route. Access internal resources exclusively through secure bastion hosts, VPN tunnels, or WireGuard interfaces.

## 8. WebSocket & Streaming Security
Validate the Origin header during the initial HTTP upgrade handshake for WebSockets. Enforce per-connection message rate limits and strict payload size limits (max 64KB per frame) to prevent memory exhaustion.

## 9. Network Telemetry & Anomaly Detection
Capture VPC flow logs, DNS query logs, and connection state metrics. Configure automated anomaly detection alerts for unexpected egress data volume surges or repeated connection attempts to non-whitelisted IP addresses.

## 10. Zero Trust Microsegmentation
Eliminate implicit trust within internal networks. Enforce authentication, authorization, and encrypted transport on every network hop, treating internal service calls with the same security rigor as external requests.
