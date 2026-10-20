---
name: misc-attack-surface
description: Remaining vulnerability families for full-coverage web/API pentests — email injection, webhooks, file-processing (CSV/formula, PDF/image, Zip Slip), DoS/resource-consumption, logging/error handling, cloud/infra exposure, supply chain, cryptography, clickjacking, dangerous HTTP methods & reverse-proxy misconfig, and CMS/framework-specific checks. Use to close out coverage against the master checklist.
---

# Misc / Full-Coverage Attack Surface

Run these so no checklist family is skipped. Only actively DoS-test if scope/RoE allows.

## Email functionality (CWE-93)
Email header injection (CR/LF in name/subject/recipient → extra `Bcc`/`To`/headers), sender/
recipient manipulation, **HTML/template injection** in emails, verification/reset weaknesses
(`auth-session-jwt`), email bombing/resource abuse (demonstrate the *gap*, don't spam). Anywhere
the app sends mail from user input.

## Webhooks (CWE-918/345)
Missing auth / weak signature verification / no replay protection (timestamp) / secret exposure /
**SSRF via callback URL** (point it at `http://<cid>.oast` or internal) / event spoofing / IDOR /
duplicate-event and race handling.

## File processing (CWE-1236/611/22)
- **CSV/Formula injection:** exported fields starting `=,+,-,@` → `=cmd|'/c calc'!A1` executes in
  the victim's spreadsheet. Test any export (CSV/XLSX).
- **PDF/Office/image generation:** server-side HTML→PDF or image parsing → SSRF/LFI/XXE via
  embedded URLs/`<img src=file://>` (chain with `server-side-ssrf-lfi`).
- **Archive extraction / Zip Slip:** upload an archive with `../` paths → write outside target dir.
- Metadata/document-conversion attack surface, external-resource fetching during render.

## DoS / resource consumption (CWE-400) — scope-gated
Missing rate limits on costly ops, GraphQL depth/complexity, **ReDoS** (catastrophic regex),
large-upload handling, unbounded pagination, expensive report/export, email/SMS abuse.
Demonstrate the *absence of limits* with a small safe sample; never actually take the service down.

## Logging / monitoring & error handling (CWE-532/209/117)
Sensitive data/passwords/tokens in logs; **log injection/forging** (CRLF into logs); missing
security-event/auth-failure logging; audit-log tampering; user-accessible internal logs.
Error handling: stack traces, SQL/framework errors, internal paths/IPs, source disclosure, debug
mode, **enumeration via differing errors**.

## Cloud / infra (CWE-16/200)
Cloud metadata exposure (via SSRF), public storage buckets, signed-URL weaknesses (expired/
non-expiring/guessable), leaked cloud creds, CDN misconfig, **origin-server exposure** (bypass
the CDN/WAF only if in scope), serverless/internal-service exposure, secret-management failures.

## Supply chain (CWE-1104/1035)
Outdated/known-vulnerable JS libs (`nuclei -tags tech,cve`; inspect bundle lib versions),
abandoned packages, dependency-confusion exposure, third-party script compromise blast radius,
external-API/webhook trust.

## Cryptography (CWE-327/330/338)
Weak hashing / weak password hashing, hardcoded keys, predictable/weak PRNG, static IV, key
reuse, insecure mode (ECB), custom crypto, client-side secrets, encryption without integrity.
Inspect tokens/reset-codes/IDs for predictability.

## Clickjacking / UI redressing (CWE-1021)
Missing `X-Frame-Options`/CSP `frame-ancestors` on sensitive actions → framing/UI-redress.
(Confirm the sensitive page is framable; PoC an iframe.)

## Web server / reverse-proxy misconfig (CWE-16)
Dangerous methods (`OPTIONS`,`PUT`,`DELETE`,`TRACE` — test with `curl -X`), directory listing,
default files/creds, server-status/actuator/debug exposure, **`X-Forwarded-*` trust**,
reverse-proxy path bypass, alternate-port exposure, internal routing exposure.

## CMS / framework-specific (CWE-1395)
Identify CMS/framework+version → known CVEs, plugin/theme vulns, default endpoints/creds, debug
functionality, framework deserialization/debug endpoints. `nuclei -tags <cms>,cve,default-login`.

## Automated helpers (toolbox)
Run broad automated coverage alongside manual: `nuclei` with tags
`exposure,misconfig,config,cve,default-login,takeover,tech,xss,ssrf,lfi,sqli` and inspect every
hit; `nikto` for server issues; `testssl.sh` for TLS; `corsy` for CORS; `nmap --script http-*`
for method/vhost checks. **Always manually validate** automated hits via `validation-gates`.
