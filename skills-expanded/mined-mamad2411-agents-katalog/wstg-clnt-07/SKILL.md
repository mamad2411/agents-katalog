---
hide: true
name: wstg-clnt-07
description: "Testing for Cross-Origin Resource Sharing (CORS)"
category: infrastructure
owasp_id: WSTG-CLNT-07
cwe_ids: [CWE-942]
---

# wstg-clnt-07 — Cross-Origin Resource Sharing (CORS)

## Objective

Confirm whether CORS policies allow untrusted origins to read authenticated responses — wildcard ACAO, origin reflection without validation, `null` origin acceptance, or credentials combined with permissive origins. Exploit work lives in `skill://attack-cors` (read via the `read` tool).

## When to run

Run when any endpoint emits `Access-Control-Allow-Origin` headers, especially for sensitive/authenticated data (profile, orders, admin APIs). Skip when no endpoint returns CORS headers. Authenticated endpoints: curl `-b/-c <out>/session/<role>/cookies.txt`, `--token-a` from `<out>/session/<role>/headers.json`; 401 → retry once after 2s, then re-auth.

## Checklist

- [ ] Automated sweep: `attack_script cors_checker` on sensitive endpoints
- [ ] Test wildcard (`*`) Access-Control-Allow-Origin
- [ ] Test origin reflection (arbitrary, subdomain, suffix-match origins)
- [ ] Test `null` origin acceptance
- [ ] Check `Access-Control-Allow-Credentials` with permissive origins
- [ ] Test internal/localhost endpoints for permissive CORS
- [ ] Confirm cross-origin read with a browser PoC (link `skill://attack-cors`, read via the `read` tool)
- [ ] Record findings with 3-gate evidence

## Procedure

Bodies to `<out>/responses/`.

1. **Automated sweep.**

```bash
attack_script cors_checker https://TARGET/api/user --token-a "Bearer <token>" --json-output
```


2. **Wildcard.** Request without Origin then with a foreign Origin; check `Access-Control-Allow-Origin`:

```bash
curl -sSI https://TARGET/api/user
curl -sSI -H "Origin: https://evil.com" https://TARGET/api/user
```

`ACAO: *` → wildcard candidate.

3. **Reflection.** Send the origin set — `https://evil.com`, `https://sub.TARGET`, `https://TARGET.evil.com` (suffix match), `https://evil-TARGET` (prefix confusion):

```bash
curl -sSI -H "Origin: https://TARGET.evil.com" https://TARGET/api/user | grep -i "access-control"
```

Reflected attacker origin → misconfig candidate.

4. **null origin.**

```bash
curl -sSI -H "Origin: null" https://TARGET/api/user
```

`null` reflected → sandboxed/iframe origins can read data.

5. **Credentials.** With any reflected/`*` ACAO, check for `Access-Control-Allow-Credentials: true` — required for cookie/bearer-authenticated reads.

6. **Internal endpoints.** Probe internal/localhost-facing endpoints (`localhost`, `127.0.0.1`, internal hostnames from JS/config) for permissive CORS — send the same origin set; reflection or `*` on an internal service → lateral-read candidate:

```bash
curl -sSI -H "Origin: https://evil.com" "https://TARGET/localhost-status" | grep -i "access-control"
```


7. **Browser PoC.** If ACAO reflects an attacker origin AND credentials are allowed, build the cross-origin fetch PoC (see `skill://attack-cors` (read via the `read` tool) Procedure step 4), save to `<out>/responses/cors-poc.html`, `browser` open it, and observe whether the exfil request fires; screenshot → `<out>/responses/cors-poc.png`.

8. **Findings.** Per confirmed endpoint → F<seq> in `<out>/findings.md` (umbrella §6, CWE-942, WSTG-CLNT-07): arbitrary origin + credentials → P1; null/subdomain + credentials → P2; wildcard without credentials → P3.

## Evidence

- Per origin test: request + ACAO/ACAC response headers
- Browser PoC + observed exfil request + screenshot
- Findings: umbrella §6 F<seq> format

## Done when

- All sensitive endpoints swept and tested for wildcard, reflection, null, and credentials
- Every permissive combination confirmed with a real-browser cross-origin read
- No-CORS targets documented as a skip
