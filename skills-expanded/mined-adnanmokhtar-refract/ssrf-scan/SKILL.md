---
name: ssrf-scan
description: Static taint-trace for URL-shaped sinks — user-controlled URL reaching an outbound fetch with no allow-list, unblocked internal/metadata ranges, hostname validated but not the resolved IP (DNS rebinding), followed redirects, dangerous URL schemes, reachable IMDSv1, and user-controlled redirect targets (open redirector). Run on any endpoint that fetches a user-supplied URL, unfurls a link, imports from a URL, registers a webhook, or bounces the browser to a URL from a query parameter. Not a dependency or secret scan — `/security-audit` dispatches here when its A01 surface fires.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: ssrf-scan

## Premise

Server-Side Request Forgery is a top-tier vulnerability (folded into OWASP **A01:2025**) and the one the auditor's checklist can only surface as a single bullet. It happens whenever the server makes an outbound request to a **URL or host derived from user input** without an allow-list — the attacker turns your server into a proxy to reach cloud metadata (`169.254.169.254`), internal services, and localhost admin ports. This skill is the dedicated static detector for URL-shaped sinks: the egress ones, plus the one redirect sink that shares their taint source (§ 7).

**Every finding cites the sink at `<file:line>` + the user-controlled source + the fix.** "Might be SSRF-able" without the cited fetch call and the tainted input is not a finding. Static taint-trace: a user-controlled value reaching an outbound-request API.

When `llm-trust-scan` ran first, its `completion-sources.txt` (§3s, `<file:line>` of every completion, tool-call argument and model message read) is a source list: trace each one forward to this skill's sinks, and grade the sink here (OH-5, URL and redirect sinks — a model-chosen URL in a fetch tool is the agent shape); `llm-trust-scan` lists the count only.

## Adapt to the codebase

Detect the HTTP-client + URL-validation primitive in use and phrase fixes in it:

| Stack | Outbound sink to grep | Allow-list / validation primitive |
|---|---|---|
| **Node** | `fetch`, `axios`, `got`, `http.request`, `undici` | a URL allow-list + `dns.lookup` on the resolved IP; `undici` `connect` hook |
| **Python** | `requests`, `httpx`, `urllib`, `aiohttp` | validate + resolve; `requests` no-redirect + custom adapter |
| **Go** | `http.Get/Do`, `net/http` | `http.Transport.DialContext` that rejects private IPs |
| **Java** | `HttpClient`, `RestTemplate`, `URL.openConnection` | URL validator + `no-redirect` |
| **Ruby/PHP** | `Net::HTTP`, `open-uri`, `Guzzle`, `file_get_contents` | allow-list; disable `allow_url_fopen` for user input |

The common SSRF sinks to prioritize: webhook/callback registration, **fetch-image/avatar-by-URL**, link-preview / OpenGraph unfurl, PDF / HTML-to-image render, import-from-URL, and any proxy endpoint.

## Pre-flight greps

Run these first — they produce the candidate set the detectors below judge. Adjust the sink alternation to the stack's row in the table above; `rg` with PCRE2 is assumed. Every command takes the two exclusion arrays, so vendored code, tests, fixtures and data dumps do not drown the result, and names its path (`.`). Any `rg` error on stderr is a failed grep, not zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/*.min.js' -g '!**/*.{md,lock,map,svg}')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,__snapshots__,testdata}/**' -g '!**/*.{spec,test,e2e-spec,mock,stories}.*' -g '!**/{*_test,*_spec,test_*}.*' -g '!**/*.snap' -g '!**/*.json' -g '!ai/**')

# 1. Every outbound sink in the repo — the universe of candidates.
rg -n --pcre2 '\b(fetch|axios(\.\w+)?|got|undici|http\.request|https\.request|requests\.(get|post|put|request)|httpx\.|urlopen|http\.Get|http\.Do|open-uri|file_get_contents|curl_exec)\s*\(' "${X[@]}" "${T[@]}" .

# 2. Sinks whose URL is request-derived (§1). 2a: the request on the same line — a route handler fetching.
#    2b: the URL is a URL-shaped variable or a parameter's field (`fetch(rawUrl)`, `fetch(request.url)`) —
#    a helper or port adapter whose CALLERS carry the taint. 2c: those callers — a call that passes a
#    non-literal `url:` / `host:` / `baseUrl:` field into a shared client (matched multi-line with -U, printed
#    as one line per URL field of each file, the right-hand side to trace). 2d: a template-literal URL whose
#    HOST is interpolated (`url: \`https://${slug}.vendor.shop/…\``) — 2b sees no URL-named variable there.
rg -n --pcre2 '\b(fetch|axios(\.\w+)?|got|http\.request|requests\.(get|post)|httpx\.|urlopen|http\.Get)\s*\([^)]*\b(req|request|params|query|body|input|payload|dto)\b' "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 '\b(fetch|axios(\.\w+)?|got|undici\.request|http\.request|https\.request|requests\.(get|post|put|request)|httpx\.\w+|urlopen|http\.Get|file_get_contents)\s*\(\s*(new URL\(\s*)?[\w.]*\b\w*(url|uri|href|host|domain|endpoint|origin|link|webhook|callback|target|address)\w*\b' "${X[@]}" "${T[@]}" .
rg -l -U --pcre2 '\b\w+\.(?!push\b)\w+\(\s*\{(?:[^{}]|\{[^{}]*\}){0,400}?\b(url|baseUrl|baseURL|endpoint|host|hostname)\s*:\s*(?!["\x27]https?:)(?!["\x27]/)(?=[\w$`])' "${X[@]}" "${T[@]}" . | xargs -r rg -n --pcre2 '\b(url|baseUrl|baseURL|endpoint|host|hostname)\s*:\s*(?!["\x27]https?:)(?!["\x27]/)[\w$`]'
rg -n --pcre2 '\b(url|uri|baseUrl|baseURL|endpoint|href|target)\s*[:=]\s*\x60(https?:)?//\$\{|\b(fetch|axios(\.\w+)?|got|undici\.request|request)\s*\(\s*\x60(https?:)?//\$\{' "${X[@]}" "${T[@]}" .

# 3. Redirect policy — a hit here means "check how many hops"; NO hit on a client
#    that follows redirects by default is itself the finding (§4).
rg -n 'maxRedirects|maxRedirections|allow_redirects|follow_redirects|CheckRedirect|redirect:\s*.(manual|error).' "${X[@]}" "${T[@]}" .

# 4. Hostname-only validation — the DNS-rebinding shape (§3). A file in 4a and NOT in 4b
#    validates a host string it never resolves.
rg -n 'hostname|host\s*===|\.host\b|allowlist|allowedHosts|ALLOWED_HOSTS' "${X[@]}" "${T[@]}" .
rg -n 'dns\.lookup|dns\.resolve|getaddrinfo|socket\.getaddrinfo|net\.LookupIP' "${X[@]}" "${T[@]}" .

# 5. Every redirect sink (§7), whatever feeds its target: a framework redirect, a Location header, a
#    meta refresh built in a string, and the browser-side assignments. Trace each target back to its source.
#    The `Location` header literal is case-sensitive and a bare `location =` skips declarations and `.location`
#    fields: a domain column named `location` and `const location = useLocation()` are not sinks.
rg -n --pcre2 '(?i:\b(res|reply|response|ctx|c|w)\.redirect\s*\(|\bredirect(_to|_back)?\s*\(|\b(sendRedirect|HttpResponseRedirect|RedirectResponse|http\.Redirect)\b|\bnew\s+Redirect\w*\(|\.(setHeader|header|set|append)\(\s*["\x27`]location["\x27`]|http-equiv\s*=\s*\\?["\x27]?refresh)|["\x27`]Location["\x27`]\s*[:,]|\b(window|document|self|top|parent)\.location(\.href)?\s*=(?!=)|(?<![\w.$])(?<!const )(?<!let )(?<!var )location(\.href)?\s*=(?!=)|\blocation\.(assign|replace)\s*\(|\bwindow\.open\s*\(' "${X[@]}" "${T[@]}" .
```

**Measured on a real repo** (a NestJS-on-Fastify monorepo with a hexagonal API, ~11,400 files). Old 2a returned one line: the shared HTTP kernel. The 16 adapters that feed it a tenant URL pass that URL as a field on a port argument, so 2a never sees them. 2b names the kernel, and 2c lists 41 calls, 34 of them into that kernel. The old 5a tied a redirect sink to a request word on the same line. It missed the repo's one open redirector, a `<meta http-equiv="refresh">` built in a domain function, and on the seeded fixture it missed `res.redirect(returnTo || …)`. The sweep returns 55 sinks (15 server-side) and both are on the list. `X` and `T` cut 1a from 97 lines to 40 and 4a from 229 to 127. Re-measured 2026-10-15 on a real NestJS + React monorepo: 2c printed 182 multi-line lines for 54 files, now 104 URL-field lines; 2d (new) prints 11 host-interpolated URLs (9 through a shop-host helper, 2 from a vendor slug builder with no host check — the real sink, which 2b missed and 2c buried); grep 5 went from 51 lines to 25 with no sink lost (26 dropped: `location` columns and fields, `useLocation()`, response-header reads). On the fixtures grep 5 keeps `res.redirect(returnTo || …)` and drops two dict keys.

A finding is grep-hit **plus** a read of the surrounding function. The greps narrow; they do not decide.

## Scans for

### 1. User-controlled URL reaches an outbound fetch with no allow-list

```
BAD:   const r = await fetch(req.body.url)                 // attacker → http://169.254.169.254/…
GOOD:  const u = new URL(req.body.url);
       if (!ALLOWED_HOSTS.has(u.hostname) || u.protocol !== 'https:') reject(400)
       // then fetch by the RESOLVED, re-checked IP
```
Grep 2 above is this detector's candidate list. A hit is a finding when no allow-list check precedes the call in the same function or its middleware chain.

**On a layered or hexagonal app, trace the port argument.** `fetch(req.body.url)` is rare there. All egress goes through one shared client, and the tainted URL reaches it as a field on an argument: `request.url`, `input.shopDomain`, a stored `settings.apiUrl` a tenant wrote. A 2b hit whose URL is the function's own parameter is that client. Name it, then treat every caller in 2c as the sink, and follow the URL field back to its source: a request DTO, a tenant setting, a webhook body, a carrier or store record. An allow-list inside the shared client covers every caller only if no caller can skip it, for example through a raw `fetch` or a second client. Each remaining grep 1 sink is checked for that bypass.

### 2. No block of internal / metadata ranges

Flag a validated fetch that checks the hostname *string* but not the ranges: `169.254.169.254` (AWS/Azure/GCP metadata), `metadata.google.internal`, `127.0.0.0/8`, `::1`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `0.0.0.0`. Block these on the **resolved** IP. A name-layer deny-list (`localhost`, `*.internal`, `*.local`, `*.cluster.local`) also misses a **single-label hostname** — `redis`, `postgres`, `db` — which resolves to a private address inside a cluster or a compose network. With a resolved-IP pin on every dial, that is hardening. Without one, it is the finding.

### 3. Hostname validated but not the resolved IP (DNS rebinding)

```
BAD:   if (allowed(u.hostname)) fetch(u)                    // DNS rebinds evil.com → 169.254.169.254
GOOD:  const ip = await dns.lookup(u.hostname); assertPublic(ip); fetch(u, { lookup: () => ip })
```
Flag validation on the hostname alone with no resolve-then-pin — the attacker's DNS can rebind between the check and the fetch (TOCTOU). Greps 4 find this as a set difference: files that validate a host string but never resolve it.

### 4. Redirects followed to a denied host

Flag an HTTP client that follows redirects by default with no per-hop re-validation (a `200`→`302`→`http://169.254…`). Disable auto-redirect or re-check each hop. Grep 3 finds the explicit policy; its **absence** on a default-following client is the finding.

### 5. Dangerous URL schemes allowed

Flag a fetch that accepts `file://`, `gopher://`, `dict://`, `ftp://`, `data:` from user input — restrict to `https:` (and `http:` only if required).

### 6. Cloud-metadata reachable / IMDSv1

Flag no egress restriction to the metadata IP, and (infra-adjacent) IMDSv1 still enabled on the instance — recommend IMDSv2 (hop-limit 1, token-required) via the infrastructure pack.

**Reach left by an egress NetworkPolicy (gate 6, [`finding-verification.md`](../../../../snippets/finding-verification.md) § 4 NET1–NET2).** Read what the policy leaves, not that it exists. A NetworkPolicy does not govern a pod's own loopback: `127.0.0.1` / `localhost` and every port a sidecar or the app itself listens on stay reachable whatever the egress rules say. An `ipBlock` allowing `0.0.0.0/0` with an `except:` list of private ranges usually re-admits the VPC CIDR for the database and cache ports through a second rule. The residual reach decides the severity: loopback admin or metrics ports, the managed datastores' private hosts, and public 443 stay in scope; rate a host-controlled fetch on what is left.

### 7. User-controlled redirect target (open redirector)

The same tainted URL, a different sink: instead of the **server** fetching it, the server tells the **browser** to go there. `?next=` / `?returnUrl=` / `?continue=` / `?redirect_uri=` reflected into a `Location` header or a framework redirect helper, with no check that the target is same-origin or on an allow-list. The sink is not always a redirect call. It can be a `<meta http-equiv="refresh" content="0; url=…">` assembled in a string by a link-preview or share page, a `location.assign` / `location.replace` / `window.location =` in the SPA, or a URL built from a **host** parameter rather than a whole URL (`https://${query.host}${path}`). A host that passes a character-set check is still any external domain. Resolve it against the verified domains, or refuse it. Grep 5 lists every sink without asking what feeds it, because the taint usually arrives through a variable (`@Query('returnTo') returnTo`), and a same-line filter misses it.

```
BAD:   res.redirect(req.query.next)                  // → https://evil.example/harvest
GOOD:  const t = req.query.next ?? '/';
       if (!isRelativePath(t) && !ALLOWED_RETURN_ORIGINS.has(new URL(t).origin)) return res.redirect('/');
```

OAuth 2.1 makes this a client obligation: *"Clients MUST NOT expose URLs that forward the user's browser to arbitrary URIs obtained from a query parameter ('open redirector')… Open redirectors can enable exfiltration of authorization codes and access tokens"* (§ 2.3.1, <https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13>).

**Boundary with `@auth-reviewer`, which also covers this.** That agent audits the open redirector *on the auth surface* — login-return, post-logout, OAuth callback — where it chains into code/token exfiltration, and it owns redirect-URI registration on the authorization-server side. This detector's job is different in shape: grep 5 sweeps **every** redirect sink in the app, including the ones no auth review reaches (an unsubscribe link, a legacy `?dest=` shortener, a "back to where you were" on a marketing page). Sweep all of them here; hand any hit on an auth path to `@auth-reviewer` for the chain analysis rather than re-deriving it.

Fixes, in order of strength: accept only a **relative path** (reject anything with a scheme or `//`); else an allow-list of return origins; never a deny-list, and never a "starts with our domain" check (`https://our.app.evil.example` passes it).

## Upload egress note

The *inbound* upload surface and the read side (magic-byte type validation, size cap, path traversal, uuid keys, storage outside webroot, archive extraction, download IDOR) are executed by the `file-access-scan` skill — the detector behind the backend `file-upload` pattern + the `security-principles` file-upload MUST. Dispatch there. The **security-specific** upload risks to also flag: an SVG accepted as an image (SVG carries script → stored XSS), a polyglot file (valid image + valid HTML/JS), and an image processed by a native parser with a known CVE (ImageMagick/`libvips`) — treat user images as untrusted input to the parser.

## Output

```
ssrf-scan — <route set>

Findings: 3

1. src/services/preview.service.ts:31                  [report-with-fix]
   fetch(req.body.url) — user URL, no allow-list. Reachable: 169.254.169.254 (AWS metadata).
   Fix: URL allow-list + resolve-and-pin the IP + reject private/metadata ranges + https-only.

2. src/avatar/import.ts:12                             [report-flagged]
   axios.get(url, { maxRedirects: 5 }) validates hostname but follows redirects.
   Fix: maxRedirects: 0 (or re-validate each hop against the resolved IP).

3. src/auth/callback.controller.ts:44                  [report-with-fix]
   res.redirect(req.query.returnUrl) — open redirector on the OAuth callback path.
   Fix: relative-path-only, else an allow-list of return origins. Never a prefix check.
```

## False positives / gotchas

- **A hardcoded/internal URL is not SSRF** — flag only user-*controlled* URL/host inputs.
- **An allow-list of first-party hosts is the fix, not a finding** — don't re-flag a validated fetch.
- **Deny-lists are weak** — blocking `169.254.169.254` misses `[::ffff:169.254.169.254]`, decimal/octal IP encodings, and rebinding; prefer an allow-list + resolved-IP check.
- **A prefix check is not an origin check** — `startsWith('https://our.app')` accepts `https://our.app.evil.example`. Parse the URL and compare the origin.
- **Egress network policy is defense-in-depth**, not a substitute — the infra pack's network policy that blocks pod→metadata is the belt to this code-level suspenders.

## When to run

- On any endpoint that fetches a user-supplied URL, imports from a URL, renders/proxies remote content, registers a webhook/callback, or redirects the browser to a URL taken from input.
- Before launch on a public API; when `/security-audit`'s A01 surface fires and needs deep confirmation.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the cited sink `<file:line>` + the user-controlled source + the fix.
- Do not propose a deny-list as the primary control — require an allow-list + resolved-IP check.
- Do not flag a hardcoded/internal URL or an already-allow-listed fetch.
- Do not report a grep hit as a finding. Every row is a hit **plus** a read of the enclosing function that establishes the taint path.

## Related

- `/security-audit` — dispatches here when its Phase 2 A01/outbound-fetch signal fires.
- `@security-auditor` — its A01 SSRF row is the detector; this skill is the executor behind that one bullet.
- `@auth-reviewer` — owns authorization-server redirect-URI registration (exact match, no wildcards); § 7 here owns every other redirect the app performs.
- `backend/ai-patterns/file-upload.md` — the inbound upload contract, executed by `file-access-scan`; this skill covers egress only.
- `rules/security-principles.md` — the SSRF + file-upload MUSTs.
- `infrastructure` pack — egress network policy + IMDSv2 (defense-in-depth).
