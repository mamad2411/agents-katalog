---
name: specification-security-standards
description: "Guidelines from The Website Specification on web security, focusing on HTTP Security Headers and security.txt."
---

# Web Security Specification

According to [The Website Specification](https://specification.website/spec/security/), a good website protects its users proactively at the network layer.

## Core Requirements

### 1. HTTP Security Headers
All HTML responses must include modern security headers:
*   **Strict-Transport-Security (HSTS):** Enforce HTTPS connections.
*   **X-Content-Type-Options: `nosniff`**: Prevent MIME-sniffing attacks.
*   **X-Frame-Options: `DENY` or `SAMEORIGIN`**: Prevent clickjacking (though CSP `frame-ancestors` is preferred in modern browsers).
*   **Referrer-Policy: `strict-origin-when-cross-origin`**: Protect user privacy when linking externally.

### 2. Content Security Policy (CSP)
*   Implement a strict `Content-Security-Policy` header to mitigate Cross-Site Scripting (XSS).
*   Avoid using `'unsafe-inline'` for scripts; rely on nonces or hashes.
*   Use `frame-ancestors` to dictate exactly who can iframe your application.

### 3. `security.txt`
*   Publish a `/.well-known/security.txt` file as per RFC 9116.
*   It must contain an `Contact:` directive (an email or URL) indicating where security researchers and white-hat hackers can responsibly disclose vulnerabilities.
*   It must contain an `Expires:` directive to ensure the contact information remains valid and up-to-date.
