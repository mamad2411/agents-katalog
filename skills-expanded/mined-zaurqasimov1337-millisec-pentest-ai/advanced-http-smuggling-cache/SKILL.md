---
name: advanced-http-smuggling-cache
description: Advanced HTTP-layer attacks — request smuggling/desync (CL.TE/TE.CL/TE.TE/H2.CL/H2.TE), web cache poisoning & deception, HTTP Host header attacks, HTTP parameter pollution (HPP), and frontend/backend parser discrepancies. Use on any target behind a proxy/CDN/cache (e.g. Cloudflare) or with host-dependent behavior. WSTG-*, CWE-444/349/113/16.
---

# Request Smuggling / Cache / Host-Header / HPP / Parser Discrepancies

These exploit **discrepancies between two systems** parsing the same request (frontend proxy vs
backend, cache key vs real request). High-skill, high-impact. Be careful — some are intrusive;
stay non-destructive and stop if the target/proxy misbehaves.

## HTTP Request Smuggling / Desync (CWE-444)
Applicable when a frontend (CDN/LB/proxy) forwards to a backend. Test for parser disagreement on
message length:
- **CL.TE / TE.CL / TE.TE:** conflicting `Content-Length` vs `Transfer-Encoding` (obfuscate TE:
  `Transfer-Encoding: chunked` + space/tab/vertical variants). 
- **HTTP/2 desync (H2.CL / H2.TE):** H2→H1 downgrade smuggling, CRLF in H2 header values, `:path`
  tricks.
- **Method:** send a crafted request; a **time delay** (backend waits for more bytes) or a
  **poisoned next response** confirms desync. Prove with a benign prefix that captures the next
  request or returns an unexpected response — never poison other real users maliciously.
- Impact/chain: request tunnelling, response-queue poisoning, cache poisoning, auth bypass,
  credential capture.
- Tooling: manual with `curl --http1.1`/raw sockets; note the toolbox has no `smuggler.py` — do
  it by hand or flag for a specialist tool.

## Web Cache Poisoning (CWE-349) & Deception
- **Poisoning:** find **unkeyed inputs** (headers `X-Forwarded-Host`, `X-Forwarded-Scheme`,
  `X-Host`, `X-Forwarded-For`, or unkeyed query params) that influence the response but aren't in
  the cache key. Inject a payload (e.g. reflected XSS or a redirect) → if cached, it's served to
  others. Check `cf-cache-status`, `Age`, `X-Cache`.
- **Deception:** request a sensitive authed page with a static-looking suffix/path
  (`/account.css`, `/account/foo.js`, `/account;.css`, path-confusion) → if the cache stores the
  authenticated response, it leaks to anonymous users. Test extension/path/delimiter/normalization
  discrepancies.

## HTTP Host Header attacks (CWE-16/113)
- Inject `Host: attacker`, duplicate `Host`, absolute-URL request line, `X-Forwarded-Host`.
- **Password-reset poisoning:** if the reset email link is built from the Host/X-Forwarded-Host →
  the victim's reset token goes to attacker (chain with `auth-session-jwt`).
- **Routing-based SSRF** via Host/`X-Forwarded-Host` to reach internal vhosts.
- Web cache poisoning via Host.

## HTTP Parameter Pollution (HPP)
Send duplicate params (`?id=1&id=2`, duplicate POST fields, duplicate JSON keys, array/scalar
confusion). Look for **frontend↔backend interpretation differences** → WAF bypass, auth/logic
bypass, filter evasion. Test which value each layer honours (first/last/concatenated/array).

## Parser / normalization discrepancies (advanced)
- URL parser inconsistencies (`@`, `#`, `\`, `..;/`, `%2f`, double-encoding), Unicode/case/path
  normalization differences between proxy and app, Content-Type confusion, JSON parser quirks
  (duplicate keys, trailing data). These enable access-control bypass, SSRF filter bypass, WAF
  bypass, and cache key confusion. Test each boundary you can observe.

## Confirmation & recording
Prove with the exact raw request(s) + the divergent responses/timing. These are often
PLAUSIBLE until clearly reproduced — hold to `validation-gates`. Record CWE, impact, and the
chain (e.g. Host-injection → reset poisoning → ATO).
