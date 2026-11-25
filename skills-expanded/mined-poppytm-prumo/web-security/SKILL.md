---
name: web-security
description: Strict Content Security Policy (CSP), context-aware XSS prevention, SameSite CSRF defense, secure cookies, and SSRF prevention
---
# Web Application Security & Hardening

## 1. Strict Content Security Policy (CSP)
Deploy a nonce-based Content Security Policy: default-src 'none'; script-src 'nonce-{RANDOM}' 'strict-dynamic'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'. Ban unsafe-eval and arbitrary third-party script sources.

## 2. Context-Aware Output Encoding (XSS Defense)
Encode all untrusted data before rendering into HTML, JavaScript, CSS, or URL contexts. Use battle-tested sanitizers (DOMPurify) when user-authored HTML is required. Prefer textContent and framework-native data bindings over innerHTML.

## 3. Anti-CSRF Tokens & SameSite Protection
Configure session cookies with SameSite=Lax (or Strict where feasible). For sensitive mutating requests, mandate custom anti-CSRF headers (X-CSRF-Token) verified server-side with HMAC validation.

## 4. Secure Cookie Attributes
Flag all session and authentication cookies with Secure, HttpOnly, and SameSite attributes. Use the __Host- prefix (__Host-session) to enforce that cookies are served only over HTTPS, bound to the host domain, and unshared with subdomains.

## 5. Clickjacking Defense
Prevent framing of web interfaces by setting Content-Security-Policy with frame-ancestors 'none' (or 'self' if embedded intentionally) and the legacy X-Frame-Options: DENY header.

## 6. Server-Side Request Forgery (SSRF) Defense
When fetching user-supplied URLs, validate the destination IP address against private and loopback ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.169.254). Reject IPv6 link-local addresses and disable automatic HTTP redirects.

## 7. Safe File Upload Architecture
Validate file uploads using magic bytes / MIME sniffing rather than trusting the user-provided file extension. Store uploaded assets in isolated cloud storage buckets with public execution disabled. Serve user uploads with Content-Disposition: attachment.

## 8. CORS Hardening
Explicitly whitelist permitted client origins. Never reflect the Origin header directly into Access-Control-Allow-Origin without validation. Never combine Access-Control-Allow-Origin: * with Access-Control-Allow-Credentials: true.

## 9. Open Redirect Prevention
Validate target redirect paths against relative URI patterns (/path) or an explicit trusted domain allowlist. Never redirect to external URLs supplied directly via query parameters (?next=https://malicious.com).

## 10. Subresource Integrity (SRI) & CAA Records
Include cryptographic hashes (integrity="sha384-...") on all external stylesheet and script tags imported from CDNs. Configure DNS CAA (Certificate Authority Authorization) records to restrict which CAs may issue certificates.
