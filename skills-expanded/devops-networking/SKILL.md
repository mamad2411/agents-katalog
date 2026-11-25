---
name: devops-networking
description: "Networking for web services: DNS records and TTLs, TLS certificates and renewal, HSTS, reverse proxies (Caddy, Nginx, Traefik) with timeouts, body limits, WebSocket upgrades and compression, CDNs and cache keys, tunnels, load balancers, CORS versus same-origin proxies, and debugging with dig, curl and openssl. Read before changing DNS, certificates, a proxy or a CDN."
---

# Networking for web services

The generated version points the apex at a CNAME, leaves a one-day TTL on a
record about to move, renews a certificate by hand until the day it lapses,
submits HSTS preload on day one, and puts nginx in front with its defaults, so
uploads over 1 MB fail and idle WebSockets drop after 60 seconds. It trusts
`X-Forwarded-For` from anyone, caches signed-in HTML at the CDN, and debugs by
refreshing a browser. This is how the pieces between a user and the app are
set up, with the numbers, and how to see what actually happens. One part of
devops; the whole is in the `devops` skill.

## 1. DNS

| Record | Use | Notes |
|---|---|---|
| A, AAAA | Name to an IPv4 or IPv6 address | AAAA only if the host really answers on IPv6 |
| CNAME | Name to another name (a platform's host) | Never at the apex, never beside other records of the same name |
| ALIAS, ANAME, flattening | The apex to a platform's host | A provider feature: Cloudflare flattening, Route 53 alias |
| MX, TXT | Mail; SPF, DKIM, DMARC, verification tokens | |
| CAA | Which CAs may issue | `0 issue "letsencrypt.org"`, plus every CA your platforms and CDN use |

- TTL 300s for records that may change, 3600s or more for stable ones.
  Before a migration, lower it to 60 to 300s at least one old TTL ahead (a
  one-day TTL needs a day's notice), and raise it after. Negative answers are
  cached for the SOA minimum, so create a record before anyone asks for it.
- "Propagation" is caching: the authoritative servers change at once,
  resolvers keep the old answer until its TTL runs out. Ask the authoritative
  server to know what is published.
- Mail authentication, required by Gmail, Yahoo and Outlook for bulk senders:
  SPF (`v=spf1 include:<provider> ~all`, at most 10 DNS lookups), DKIM (the
  provider's `<selector>._domainkey` record), DMARC from
  `v=DMARC1; p=none; rua=mailto:dmarc@example.com` to `quarantine` to
  `reject` once reports are clean. A domain that sends no mail gets
  `v=spf1 -all` and `p=reject`.
- DNSSEC needs the signing at the DNS host and the DS record at the
  registrar to agree; a mismatch makes the domain vanish for validating
  resolvers (1.1.1.1, 8.8.8.8). Remove the DS record and wait before moving
  DNS providers.
- The domain: auto-renew, registrar lock, MFA on the account.

## 2. TLS

- ACME everywhere (Let's Encrypt, ZeroSSL, Google Trust Services) through
  the proxy (Caddy, Traefik), cert-manager, the platform, or certbot and lego.
  HTTP-01 needs port 80 reachable; DNS-01 needs a DNS API token and is the
  only way to wildcards and hosts that are not on the internet.
- Lifetimes keep shrinking: public certificates are capped at 200 days since
  15 March 2026, 100 days from March 2027 and 47 days from March 2029. Let's
  Encrypt issues 90 days today, 64 from February 2027 and 45 by 2028. Renewal
  must be automatic, at about two thirds of the lifetime.
- Let's Encrypt stopped emailing expiry warnings in June 2025 and shut down
  OCSP in August 2025 (drop `ssl_stapling` for its certificates): watch
  expiry yourself (`devops-observability`).
- Serve the full chain (`fullchain.pem`, not `cert.pem`), or some clients
  fail while browsers work. TLS 1.2 and 1.3 only, ciphers from Mozilla's
  "intermediate" profile.
- HSTS in steps: `max-age=300`, then a week, then
  `max-age=31536000; includeSubDomains`. Add `preload` and submit to
  hstspreload.org only when every subdomain, now and later, serves HTTPS;
  leaving the list takes months.

## 3. Reverse proxies

```caddyfile
app.example.com {
	encode zstd gzip
	request_body {
		max_size 10MB
	}
	header Strict-Transport-Security "max-age=31536000; includeSubDomains"
	reverse_proxy 127.0.0.1:3000 {
		header_up X-Request-Id {http.request.uuid}
		transport http {
			dial_timeout 5s
			response_header_timeout 60s
		}
	}
}
```

Caddy gets certificates, redirects HTTP, speaks HTTP/3, and passes
WebSockets and forwarded headers on its own.

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      '';
}
upstream app {
    server 127.0.0.1:3000;
    keepalive 32;
}
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name app.example.com;
    ssl_certificate     /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    client_max_body_size 10m;
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;

    location / {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-Id $request_id;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
    }
}
```

- The `map` sends `Connection: upgrade` only on WebSocket requests and no
  `Connection` header otherwise, so upstream keep-alive works; both need
  `proxy_http_version 1.1`. A separate `listen 80` server redirects to HTTPS.
- nginx defaults that bite: `client_max_body_size 1m` (a 413 on uploads),
  `proxy_read_timeout 60s` (idle sockets and slow reports cut: raise it per
  location, or ping every 30s), `proxy_buffering on` (breaks server-sent
  events: `proxy_buffering off` there, or `X-Accel-Buffering: no` from the
  app). Behind Cloudflare, `set_real_ip_from` its ranges with
  `real_ip_header CF-Connecting-IP`.
- Traefik reads labels on the containers (Coolify writes the same kind):

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.app.rule=Host(`app.example.com`)
  - traefik.http.routers.app.entrypoints=websecure
  - traefik.http.routers.app.tls.certresolver=letsencrypt
  - traefik.http.services.app.loadbalancer.server.port=3000
```

  Traefik v3's entry point `respondingTimeouts.readTimeout` defaults to 60s
  and covers the whole request body, so large or slow uploads fail until it
  is raised (it is not enforced over HTTP/3). The `buffering` middleware's
  `maxRequestBodyBytes` caps bodies, but buffers them.
- The app trusts forwarded headers only from its own proxy: Express
  `app.set("trust proxy", 1)`, Uvicorn `--forwarded-allow-ips`, the rightmost
  untrusted hop in `X-Forwarded-For` elsewhere. Trusting everyone lets a
  client forge its IP past rate limits.

| Hop | Timeout | Rule |
|---|---|---|
| Client to CDN | Cloudflare waits 100s for the origin (then 524) | Long work goes to jobs, not requests |
| Load balancer idle | AWS ALB 60s by default | The app's keep-alive must be longer |
| Proxy to app | Connect 5s, read 60s; longer only for sockets and streams | |
| App keep-alive | Node's `keepAliveTimeout` is 5s | Under a 60s idle LB, set 65s and `headersTimeout` 66s, or get random 502s |

## 4. CDNs and caching

| Content | `Cache-Control` |
|---|---|
| Hashed assets (`app.3f9a1c.js`) | `public, max-age=31536000, immutable` |
| Personal pages and API responses | `private, no-store` (or `no-cache` to revalidate) |
| Shared HTML that may be a minute stale | `public, max-age=0, s-maxage=60, stale-while-revalidate=300` |
| Unhashed images | `public, max-age=86400` with an `ETag` |

- The cache key is path plus query by default: strip tracking parameters
  (`utm_*`, `fbclid`), never key public pages on cookies, and send only
  `Vary: Accept-Encoding` (`Vary: User-Agent` or `Cookie` empties the cache).
- Nothing personal is cacheable, and cacheable responses set no cookies.
  `CDN-Cache-Control` sets the CDN's lifetime apart from the browser's.
- Hashed assets never need purging; HTML gets a short `s-maxage` or a purge
  on deploy. Tiered cache or origin shield sends a miss to one location, not
  all of them.
- Cloudflare: a proxied record hides the origin only if nothing else reveals
  it (old records, mail on the same host). SSL mode Full (strict), with a
  public or Cloudflare Origin CA certificate on the origin; Flexible speaks
  HTTP to the origin and loops when the origin redirects to HTTPS. It caches
  by file extension, not HTML, unless a Cache Rule says so; request bodies are
  capped at 100 MB on Free and Pro.
- Lock the origin to the CDN: its IP ranges on 443, authenticated origin
  pulls, or no open port at all (a tunnel).

## 5. Tunnels and load balancers

```yaml
# /etc/cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/<tunnel-id>.json
ingress:
  - hostname: app.example.com
    service: http://localhost:3000
  - service: http_status:404
```

- Cloudflare Tunnel connects outward, so the host opens no inbound port; the
  last ingress rule must be a catch-all. A dashboard-managed tunnel runs with
  a token (a secret). `originRequest: { noTLSVerify: true }` only for an
  origin on localhost. Cloudflare Access guards anything private.
- Tailscale: a WireGuard mesh with SSO for private access; `tailscale serve`
  shares a port inside the tailnet, `tailscale funnel` publishes it (ports
  443, 8443 and 10000 only).
- Load balancers: health checks on readiness every 5 to 10s, unhealthy after 2
  to 3 failures; a deregistration delay matching the app's drain (30 to 60s,
  not AWS's 300s default); sticky sessions only for legacy in-memory state
  (WebSocket fan-out across instances needs a pub/sub backplane such as Redis
  or NATS); one load balancer routing by host and path for many services.

## 6. Same origin, CORS, IPv6, HTTP/3

- Serving the API under the site's own origin avoids CORS entirely: no
  preflights, cookies with `SameSite=Lax`. In nginx,
  `location /api/ { proxy_pass http://api:8080/; }` (the trailing slash
  strips `/api`).
- A cross-origin API lists allowed origins, allows credentials only for
  them, and caches preflights with `Access-Control-Max-Age` (Chromium caps it
  at 2 hours) (`backend-api`, `backend-security`).
- IPv6: AAAA records only when the host listens on IPv6 and the firewall
  allows it; test with `curl -6`. HTTP/2 is on by default in Caddy, Traefik
  and CDNs (nginx: `http2 on;`). HTTP/3 needs UDP 443 open; nginx adds
  `listen 443 quic reuseport;` and an `Alt-Svc: h3=":443"; ma=86400` header.

## 7. Debugging

```sh
dig +short app.example.com A
dig @1.1.1.1 app.example.com                  # a public resolver, with the TTL left
dig @ns1.provider.net app.example.com         # what the authoritative server publishes
dig +trace app.example.com
curl -sSI https://app.example.com             # status, headers, redirects
curl -sS -o /dev/null -w 'dns %{time_namelookup} tls %{time_appconnect} ttfb %{time_starttransfer} total %{time_total}\n' https://app.example.com
curl -v --resolve app.example.com:443:203.0.113.10 https://app.example.com/   # one origin, skipping DNS
openssl s_client -connect app.example.com:443 -servername app.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

- Headers worth reading: `cf-cache-status`, `x-cache` and `age` (cached or
  not), `location` chains, `strict-transport-security`, `alt-svc`.
- On the host: `ss -tlnp` (what listens where), then
  `curl -v http://127.0.0.1:3000/healthz` to separate the app from the proxy.
- 502: nothing valid from upstream (down, wrong port, a keep-alive race);
  504: upstream too slow; 413: body limit; 525 and 526 at Cloudflare: the
  origin's TLS handshake or certificate; 524: the origin took over 100s.

## Check it

- `nginx -t`, `caddy validate --config Caddyfile`,
  `cloudflared tunnel ingress validate`, and
  `cloudflared tunnel ingress rule https://app.example.com` to see which rule
  matches.
- After a DNS change, the authoritative server and public resolvers agree,
  and the old TTL has passed before calling it done.
- `http://` answers 301 to `https://`; `https://` answers 200 with HSTS; the
  chain is complete and more than a third of the certificate's life is left.
- An upload just under the limit works and one just over gets 413; an idle
  WebSocket survives 5 minutes; server-sent events arrive unbuffered.
- A hashed asset shows a cache hit on the second request; a signed-in page
  never does.

## Avoid

A CNAME at the apex; long TTLs during a migration; hand-renewed
certificates; no expiry monitoring now that Let's Encrypt sends no emails;
HSTS preload before every subdomain is ready; nginx defaults for uploads,
sockets and streams; trusting `X-Forwarded-For` from anyone; app keep-alive
shorter than the load balancer's; caching personal pages or keying the cache
on cookies; Cloudflare Flexible mode; an origin reachable around the CDN;
AAAA records for a host that does not answer on IPv6; debugging DNS by
refreshing a browser.
