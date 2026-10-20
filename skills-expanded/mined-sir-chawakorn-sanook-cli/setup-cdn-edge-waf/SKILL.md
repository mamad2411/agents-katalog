---
name: setup-cdn-edge-waf
description: Configures CDN/edge delivery and a WAF — cache keys and Cache-Control/Surrogate-Control, stale-while-revalidate, tag/path purge wired into deploy, origin shielding with request collapsing, edge TLS + HTTP/3, and a managed OWASP ruleset with edge rate-limiting and bot/DDoS mitigation rolled out detect-then-enforce — to raise cache hit-ratio and absorb attacks before the origin.
when_to_use: Serving static assets or APIs through a CDN, raising cache hit-ratio, or adding edge security (WAF, DDoS, bot mitigation). Distinct from caching-strategy (app/Redis caching), configure-reverse-proxy-lb (the origin proxy itself), rate-limiting (origin app limits), and configure-dns-tls (the cert/DNS records the CDN sits on top of).
---

## When to Use

Reach for this skill when the work is at the **edge in front of the origin** — caching, TLS termination, and attack absorption at the POP, not inside your app:

- "Put the static site / assets / images behind a CDN and stop hitting origin"
- "Our cache hit-ratio is low / everything is `MISS` / origin is melting under read traffic"
- "Cache this API response at the edge but purge it the instant we deploy / the record changes"
- "Add a WAF / block SQLi+XSS / OWASP ruleset / managed rules"
- "We're getting scraped / credential-stuffed / L7 DDoS'd — mitigate at the edge before it reaches us"
- "Enable HTTP/3, edge TLS, origin shielding, request collapsing"

NOT this skill:
- Cache-aside / write-through / Redis TTLs *inside the application* → caching-strategy
- Configuring the origin reverse proxy / load balancer (nginx/Envoy/HAProxy, upstream pools, health checks) → configure-reverse-proxy-lb
- Per-user/per-key request quotas enforced *in the origin app* (429 + Retry-After business logic) → rate-limiting
- Issuing the cert, DNS records, HSTS, CAA that the CDN hostname rides on → configure-dns-tls
- Fixing the actual SQLi/XSS/SSRF in code (the WAF is a shield, not a patch) → remediate-web-vulnerabilities
- Actively pen-testing the app to find injection bugs → fuzz-dynamic-security-test

## Steps

1. **Classify every route into a cache class first — caching policy follows the class, not the URL.** Decide this before touching any config.

   | Class | Example | Cache-Control | Edge TTL | Cache key includes |
   |---|---|---|---|---|
   | Immutable static | `/_next/static/*.js`, hashed assets | `public, max-age=31536000, immutable` | 1y | path only |
   | Versioned media | `/img/logo.png` | `public, max-age=86400, stale-while-revalidate=604800` | 1d | path only |
   | HTML (anon) | `/`, `/blog/x` | `public, max-age=0, s-maxage=300, stale-while-revalidate=86400` | 5m (edge), 0 (browser) | path + `Vary` allow-list |
   | Cacheable API (GET) | `/api/products` | `public, s-maxage=60, stale-while-revalidate=300` | 60s | path + canonical query + auth-tier |
   | Private / auth | `/account`, `POST` | `private, no-store` | bypass | never cache |

   Split `max-age` (browser) from `s-maxage`/`Surrogate-Control` (edge) so you can hold a long edge TTL while browsers revalidate. Origin sets `Surrogate-Control: max-age=...` (CDN strips it before responding); browser-facing `Cache-Control` carries the public value.

2. **Engineer the cache key — this is where hit-ratio is won or lost.** Default to: `scheme + host + path + sorted-allowlisted-query`.
   - **Strip tracking/garbage query params** (`utm_*`, `fbclid`, `gclid`, `ref`, session ids) from the key — otherwise every share link is a `MISS`. Allow-list the params that actually change the response; drop everything else.
   - **Sort query params** so `?a=1&b=2` and `?b=2&a=1` collapse to one entry.
   - **`Vary` only on what truly changes the body** — usually `Accept-Encoding` (or let the CDN normalize it) and at most a derived `X-Device-Type` (mobile/desktop) or auth-tier cookie you set. **Never `Vary: Cookie` or `Vary: User-Agent`** — that fragments the cache into near-uniqueness and kills hit-ratio.
   - For cacheable APIs, normalize the auth dimension to a *tier* (e.g. `anon` vs `member`), not the raw token — fold the token down to a coarse bucket in an edge function before keying.

3. **Add `stale-while-revalidate` and `stale-if-error` everywhere cacheable.** SWR serves the stale object instantly and revalidates in the background — no user waits on origin. `stale-if-error` keeps the site up when origin 5xx's. Without these, every TTL expiry is a latency spike and a thundering-herd to origin.

4. **Wire purge into deploy — by tag/path, never blanket.** A full "purge everything" after each deploy nukes hit-ratio to ~0 and stampedes origin. Tag objects with surrogate keys at the origin and purge those keys:

   ```http
   # origin response tags the object
   Surrogate-Key: product-42 catalog homepage

   # deploy/webhook purges only the affected keys (Fastly example)
   curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
        https://api.fastly.com/service/$SVC/purge/product-42
   ```
   - Static assets are **content-hashed** (`app.4f2a.js`) → never purge them, just deploy new filenames; old ones expire naturally.
   - Purge HTML/API by surrogate key on the entity that changed (`product-42`), driven from the same event that writes the DB — not on a timer.
   - Reserve path-based soft purge for the rare untagged route. Blanket purge is a break-glass action, not a deploy step.

5. **Turn on origin shielding + request collapsing.** Pin a single shield POP between all edge POPs and origin so a global cache `MISS` hits origin once, not once-per-POP. Request collapsing (a.k.a. coalescing) dedupes concurrent `MISS`es for the same key into **one** origin fetch while the rest wait — this is your built-in cache-stampede guard at the edge. Confirm both are enabled; they are the difference between a viral event being absorbed vs. a self-inflicted DDoS on origin.

6. **Terminate TLS at the edge and enable HTTP/3.** Edge TLS (TLS 1.3) + `Alt-Svc: h3` / HTTP/3 (QUIC) cuts handshake RTTs and head-of-line blocking on lossy/mobile networks. Keep **origin** connections on TLS too (full/strict, validated cert) — edge-to-origin in cleartext is a classic foot-gun. Force HTTPS with a 308 redirect at the edge; let configure-dns-tls own the cert issuance/HSTS/CAA underneath.

7. **Enable the WAF in detect/log mode first, then enforce.** Order matters — flipping a managed ruleset straight to block will false-positive real traffic and page you at 2am.
   - Turn on the **managed OWASP Core Rule Set** (SQLi, XSS, RCE, LFI/RFI, protocol anomalies) in **count/log mode**. Watch for 24–72h.
   - Triage the log: tune or exception the rules that hit legitimate traffic (rich-text editors, `<`/`'` in JSON bodies, signed webhooks). Adjust the **anomaly/paranoia threshold** rather than disabling whole rule families.
   - **Then flip to block.** Add **custom rules** for your app's known-bad shapes (admin paths from non-office IPs, deprecated API versions, oversized bodies). Example custom rule + edge rate-limit (Cloudflare ruleset-expression syntax):

     ```
     # block /admin from outside the office, enforce mode
     (http.request.uri.path matches "^/admin" and not ip.src in $office_ips)  ->  block

     # edge rate-limit /login: >10 req/min/IP -> managed challenge (never reaches origin)
     when (http.request.uri.path eq "/login")
       rate_limit { characteristics = ["ip.src"]; period = 60; requests = 10; action = "managed_challenge" }
     ```
   - **Edge rate-limiting** for brute-force/scraping (e.g. `/login` > N/min/IP → challenge or 429) — this is the *edge* sibling of origin `rate-limiting`; do coarse volumetric/abuse limits here, fine per-key quotas in the app.
   - **Bot + DDoS mitigation:** enable managed bot rules + L3/4 and L7 DDoS protection; serve a **JS/managed challenge** (not a hard block) to suspected bots so false positives self-recover. Geo/IP allow/deny rules only where you have a real basis (block sanctioned regions, allow-list admin office IPs) — geo-blocking is blunt and breaks VPN users, so prefer challenges.

## Common Errors

- **Blanket purge on every deploy.** Drops global hit-ratio to zero and stampedes origin each release. Tag with surrogate keys and purge only what changed; let hashed assets expire on their own.
- **Tracking params in the cache key.** `?utm_source=...` makes every shared link a unique `MISS`. Strip the allow-list's complement before keying.
- **`Vary: Cookie` (or `User-Agent`).** Fragments the cache to near-uniqueness — effectively no caching. Normalize to a coarse derived dimension (auth-tier, device-class) and `Vary` on that.
- **One TTL for both browser and edge.** Using `max-age` alone means you can't hold a long edge TTL without baking it into browsers. Separate `s-maxage`/`Surrogate-Control` (edge) from `max-age` (browser).
- **No `stale-while-revalidate`.** Every expiry becomes a synchronous origin round-trip and a latency spike; add SWR + `stale-if-error`.
- **No origin shield / no request collapsing.** A cold key fetches origin once *per POP* and concurrent misses each hit origin — a viral object DDoSes you. Enable both.
- **Cleartext edge-to-origin.** TLS terminates at the edge but the origin pull is HTTP — a MITM goldmine. Use full/strict mode with a validated origin cert.
- **WAF flipped straight to block.** Guaranteed false positives on launch. Run count/log mode 24–72h, tune, then enforce.
- **Hard-blocking suspected bots.** A false positive locks out a real user with no recovery. Serve a managed/JS challenge instead so legit clients pass automatically.
- **Caching `Set-Cookie` / personalized HTML.** Leaks one user's session or data to the next requester. Force `private, no-store` on any response carrying `Set-Cookie` or auth-specific content, and strip `Set-Cookie` from cacheable responses.
- **Treating the WAF as the fix.** A blocked payload is still an unpatched bug; an attacker who bypasses one rule still wins. Fix the vuln in code (remediate-web-vulnerabilities) — the WAF only buys time.

## Verify

1. **Hit-ratio rises, origin load drops.** Pull the CDN analytics cache hit-ratio before/after; it should climb (static well above 95%, cacheable HTML/API materially up). Confirm origin request rate / bandwidth fell by a corresponding amount — the whole point.
2. **Edge actually served it.** `curl -sI https://host/path` shows the CDN cache header (`x-cache: HIT`, `cf-cache-status: HIT`, or `x-served-by` with `cache-*-HIT`) and the expected `Cache-Control`/`age`. A second request after a `MISS` must return `HIT`.
3. **Key normalization works.** Request `?utm_source=x` and the bare URL → both `HIT` the same object (same `age`/etag), proving tracking params are stripped and params are sorted.
4. **Purge actually invalidates.** Cache an object (`HIT`), change the entity, fire the surrogate-key/path purge, re-request → `MISS` then fresh content. A purge that doesn't flip `HIT`→`MISS` is broken.
5. **SWR serves stale instantly.** After TTL expiry, the first request returns immediately (stale, background revalidate) rather than blocking on origin; latency stays flat across the expiry boundary.
6. **TLS + HTTP/3 negotiated.** `curl --http3 -sI https://host` succeeds and `Alt-Svc: h3` is advertised; TLS 1.3 on edge *and* validated TLS on the origin pull (no cleartext hop).
7. **WAF blocks a test attack.** Send a benign canary payload (`?q=' OR 1=1--`, a reflected-XSS probe) → blocked (403/challenge) with a rule id in the WAF log. Confirm in the same window that real traffic shows ~0 false positives (block-mode log clean of legit requests).
8. **Edge rate-limit / bot rule fires.** Burst `/login` past the threshold from one IP → challenge/429 at the edge (request never reaches origin logs). A known-good client sails through.

Done = cache hit-ratio is up and measured origin load is down, `HIT`/purge/SWR behave exactly as configured, edge+origin TLS with HTTP/3 are verified, and the WAF blocks a canary attack with zero false positives on real traffic (managed rules in enforce mode, not count).
