---
name: lyra-security-appsec
description: "Application security for code being written or reviewed: trust-boundary validation, parameterized sinks (SQLi/command/path/XSS/deserialization), server-side deny-by-default authorization, session and password handling, SSRF and upload defenses, CSRF, security headers, rate limiting, safe error handling, and LLM/prompt-injection surfaces — with a source-to-sink review methodology. Use when writing code that touches user input, auth, money, or an LLM; when doing a security review; or when triaging a reported vulnerability."
compatibility: "No tools required. Language-agnostic with web/API focus; examples in TypeScript. Composes with lyra-bug-hunter (--scan-only sweeps), lyra-security-secrets, lyra-security-supply-chain, lyra-security-containers. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-security-appsec

## What it does

Defensive application security as coding rules, not a compliance checklist. The organizing model: every vulnerability is a path from a **source** (anything an attacker influences: params, headers, cookies, files, webhooks, third-party API responses, database values another user wrote) to a **sink** (query, shell, filesystem, HTML, redirect, deserializer, authz decision) without an adequate barrier between. Writing secure code means placing barriers; reviewing means walking the paths. Grounded in the OWASP Top 10 and ASVS without depending on their edition numbering.

## The rules

### 1. Validate at trust boundaries — allowlist, canonicalize first

Every input crossing a trust boundary gets validated at the edge: schema-validate shape and type (zod/JSON Schema/DTOs), allowlist values over blocklisting badness, enforce length limits, and canonicalize (decode, normalize paths/unicode) **before** validating — validating then decoding is how `..%2f` walks past a path check. Webhooks are a boundary with a solved answer: verify the HMAC signature (timing-safe compare, replay window) before parsing the payload — an unverified webhook endpoint is an open API that believes anyone. Internal code then trusts its typed inputs; sprinkling re-validation everywhere is noise (see lyra-de-slop rule 5), missing it at the boundary is a breach.

### 2. Parameterize every sink — string-building is the vulnerability

SQL through bound parameters or a query builder, never interpolation. Shell through arg arrays (`execFile`), never `exec` with a built string. Paths through `path.join` + a post-resolution prefix check against the allowed root. HTML through the framework's escaping — `dangerouslySetInnerHTML`/`innerHTML` with anything user-influenced requires sanitization (DOMPurify) and a written justification. Templates: user data as *data*, never concatenated into the template source (SSTI). Deserialization of untrusted data: data-only formats (JSON + schema) over native object deserialization — pickle/unserialize/BinaryFormatter on attacker bytes is remote code execution by design; where a native format is unavoidable, allowlist the types. XML parsers are the same sink family: disable external entities and DTDs (XXE) before parsing anything attacker-influenced — still live in 2026 wherever SAML, SOAP, SVG, or document pipelines survive. If input must reach a sink structurally, the answer is always the parameterized API, not a cleverer escape function.

### 3. Authorization is server-side, deny-by-default, object-level

Every endpoint states who may call it; anything unstated is denied. Check **object-level** access — that this user may touch *this* resource id (IDOR/BOLA, the most common real-world API hole), not just that they're logged in. Never trust client-supplied identity: user id from the session, role from the server, tenant from the resource — anything in the request body or JWT payload that the client controls is a claim, not a fact, until verified. UI hiding is not access control.

### 4. Sessions and passwords have solved answers — use them

Passwords: argon2id (or bcrypt with adequate cost), never a fast hash, never homemade. Sessions: regenerate the id on login (fixation), invalidate server-side on logout, cookies `HttpOnly; Secure; SameSite=Lax` or stricter. JWTs: verify with an allowlisted algorithm (reject `alg: none` and unexpected downgrades), short expiry with rotation, and a revocation story — a JWT you can't revoke is a bearer token for its full lifetime. Rate-limit and add backoff on auth endpoints; log failures with an identifier for detection.

### 5. SSRF: outbound requests to user-influenced URLs are guarded

Fetching a URL an attacker can influence (webhooks, importers, previewers, PDF renderers) requires: allowlist of destinations where possible; otherwise resolve and reject private/link-local/metadata ranges (169.254.169.254 is the cloud-credential jackpot), pin the resolved IP for the actual request (DNS rebinding), disable redirects or re-validate each hop.

### 6. File uploads: validate content, quarantine location, randomize names

Type by content sniffing, never trusting extension or client MIME; hard size limits; server-generated random names (user filenames are path traversal + XSS vectors); stored outside the webroot or in object storage, served with `Content-Disposition` and a content-type that can't execute. Image processing gets hardened libraries and resource limits — decompression bombs are denial of service in a .png.

### 7. Errors are boring outside, rich inside

Clients get a generic message and a correlation id; logs get the stack, the id, and the context — never secrets, tokens, or full card/personal data (that's a compliance breach via logfile). Error paths must fail closed: an exception in an authz check denies. Timing matters where enumeration does: constant responses for "user not found" vs "wrong password".

### 8. The unglamorous headers and limits, on by default

`Content-Security-Policy` (start restrictive, loosen deliberately), `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, framing denied unless embedding is a feature. CORS: explicit origin allowlist — `*` with credentials is a contradiction the browser refuses anyway, and reflecting `Origin` unvalidated is `*` with extra steps. CSRF: `SameSite` narrows the window but doesn't close it — state-changing requests authenticated by cookies still get anti-CSRF tokens (or an explicit custom-header check on a same-site-only API). Rate limiting on everything unauthenticated and everything expensive; request body size limits at the edge. Mass assignment: bind requests to explicit DTOs/allowlists, never spread a request body into a model (`role: "admin"` arrives eventually).

### 9. Crypto: boring, modern, delegated

TLS everywhere including service-to-service. Randomness from the CSPRNG (`crypto.randomUUID`/`randomBytes`), never `Math.random` for anything security-relevant. AEAD (AES-GCM/ChaCha20-Poly1305) via a vetted library; no homemade constructions, no ECB, no static IVs. Key material handling belongs to lyra-security-secrets.

### 10. LLM features are a source and a sink at once

If the application feeds content into an LLM that can call tools, browse, or emit text shown to others, apply the same model: **prompt injection is untrusted input reaching a privileged sink.** Anything the model reads — user messages, retrieved documents, web pages, file contents, tool results — can carry instructions, so the model's *output* is untrusted input too: never `eval` it, never pass it to a shell or query unparameterized, never let it name arbitrary URLs/paths without the rule 5/2 barriers. Contain instead of sanitize (injection cannot be reliably filtered): least-privilege tool allowlists per feature, human confirmation on state-changing or irreversible actions, no secrets in prompts (lyra-security-secrets rule 8), and treat model-generated markdown/HTML rendered to other users as an XSS source under rule 2.

### 11. Review methodology: walk source → sink, rank by exploitability × impact

Security review = enumerate sources, enumerate sinks, walk each path asking "where is the barrier and can I get around it?" — not grepping for scary function names. LLM surfaces get walked like any other path (rule 10): what can reach the model, what can the model reach. Verify findings like lyra-bug-hunter demands: a concrete attacker input and what it achieves. Severity = exploitability × impact: an unauthenticated SQLi outranks a self-XSS behind three settings. Fix order follows severity, and every fix lands with a regression test that encodes the attack.

---

_Part of the [skill collection](../README.md)._
