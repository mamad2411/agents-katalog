---
name: configure-reverse-proxy-lb
description: Configures a reverse proxy / load balancer (nginx, Envoy, Caddy, HAProxy) in front of services — upstream pools, active/passive health checks, per-hop connect/read/send timeouts, TLS termination vs passthrough, idempotent-only retries with circuit breaking, sticky sessions, and zero-drop graceful reloads.
when_to_use: Putting a proxy/LB in front of services, fixing 502/504s, balancing across instances, or routing by host/path. Distinct from configure-dns-tls (DNS records + cert issuance), setup-cdn-edge-waf (the CDN/WAF edge), rate-limiting (app-level request caps), and k8s-manifest-review (in-cluster Service/Ingress objects).
---

## When to Use

Reach for this skill when the request is about **the proxy/LB layer between clients and your services**:

- "Put nginx/Envoy/Caddy/HAProxy in front of these app instances"
- "We're getting random 502/504s — fix the timeouts"
- "Balance traffic across N backends and drop a dead one automatically"
- "Route by `Host:` / path prefix to different upstreams"
- "Terminate TLS at the proxy" / "pass TLS straight through to the backend"
- "Config reload kills in-flight requests — make it zero-drop"

NOT this skill:
- Creating DNS records or issuing/renewing the cert itself → configure-dns-tls
- The CDN/edge tier, bot rules, or WAF rulesets → setup-cdn-edge-waf
- Per-user/per-key request caps and 429s at the app → rate-limiting
- Kubernetes `Service`/`Ingress`/`Gateway` objects in-cluster → k8s-manifest-review

## Steps

1. **Pick the proxy by requirement — default to nginx.**

   | Proxy | Pick when | Watch out |
   |---|---|---|
   | **nginx** | General L7 in front of HTTP/HTTPS apps — the default | Active health checks need nginx **Plus**; OSS only does passive `max_fails` |
   | **Envoy** | Dynamic config via xDS, gRPC/HTTP2, fine-grained circuit breaking, outlier detection | Steep config; run with a control plane (Istio/Contour/Gloo) for anything large |
   | **Caddy** | You want automatic TLS (ACME) with near-zero config | Less knob-level control over upstreams/retries |
   | **HAProxy** | Heavy L4 (TCP) LB, max throughput, advanced balancing/observability | L7 ergonomics weaker than nginx for content routing |

   For a typical web service: **nginx terminating TLS, round-robin or least-conn upstream, passive health checks**. Reach for Envoy only when you genuinely need dynamic upstreams or per-endpoint outlier ejection.

2. **Define the upstream pool + algorithm — least-conn is the safer default for mixed latency.**

   ```nginx
   upstream app {
       least_conn;                         # round-robin is fine for uniform requests; least_conn for variable latency
       server 10.0.1.11:8080 max_fails=3 fail_timeout=10s;
       server 10.0.1.12:8080 max_fails=3 fail_timeout=10s;
       server 10.0.1.13:8080 max_fails=3 fail_timeout=10s backup;  # only when primaries are down
       keepalive 64;                       # REUSE upstream conns — without this every request does a fresh TCP+TLS handshake
   }
   ```

   - **round-robin** (default): uniform, cheap requests.
   - **least-conn**: requests with variable duration — avoids piling onto a slow node.
   - **consistent-hash** (`hash $arg_key consistent;` / Envoy ring-hash): only when a key must stick to a backend (cache affinity, sharding). Plain `ip_hash` rebalances badly when a node leaves; use `consistent` so a single ejection doesn't reshuffle every key.

3. **Set timeouts at EVERY hop — a proxy timeout shorter than the app is the #1 cause of 502/504.** A 502 = backend refused/reset the connection; a 504 = backend accepted but didn't answer before `proxy_read_timeout`. The proxy's read timeout must be **longer** than the slowest legitimate backend response, and the backend's own keepalive must be **longer** than the proxy's so the proxy never reuses a socket the backend just closed (classic race → sporadic 502).

   ```nginx
   location / {
       proxy_pass http://app;
       proxy_http_version 1.1;
       proxy_set_header Connection "";      # required so keepalive to upstream actually works

       proxy_connect_timeout 2s;            # TCP connect to backend — short; a backend that won't accept is dead
       proxy_send_timeout   30s;            # writing the request body to backend
       proxy_read_timeout   60s;            # waiting for the backend's response — MUST exceed slowest real response
   }
   # And: backend keepalive_timeout (e.g. 75s) > nginx upstream idle reuse window, to avoid the reuse-after-close 502.
   ```

   Envoy: set `connect_timeout` on the cluster and `route.timeout` per route; default route timeout is 15s and silently truncates long requests — set it deliberately.

4. **Add health checks — passive at minimum, active if your proxy supports it.** Passive ejection (`max_fails`/`fail_timeout`, Envoy outlier detection) reacts only to *real* request failures, so a freshly-booted-but-broken node still gets traffic until it fails N live requests. Active checks (nginx Plus `health_check`, HAProxy `option httpchk`, Envoy `health_checks`) probe a `/healthz` endpoint and eject before user traffic hits it.

   - Health endpoint must check **dependencies** (DB, cache reachable), not just "process is up" — otherwise you keep a node that 500s on every real request.
   - Set an explicit `unhealthy`→`healthy` hysteresis (e.g. eject after 3 fails, re-add after 2 passes) so a flapping node doesn't oscillate in and out of rotation.

5. **TLS: terminate at the proxy unless the backend legally must see the cert.** Terminate (decrypt at proxy, plaintext or re-encrypt to backend) for HTTP routing, header inspection, and central cert management — the common case. **Passthrough** (L4 `stream`/SNI routing, proxy never decrypts) only for end-to-end encryption mandates or non-HTTP TLS. When terminating, forward the original scheme/IP so the app builds correct URLs and logs the real client:

   ```nginx
   proxy_set_header Host              $host;
   proxy_set_header X-Real-IP         $remote_addr;
   proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;   # app uses this to know the request was HTTPS
   ```

   Pin `ssl_protocols TLSv1.2 TLSv1.3;` and a modern cipher suite; redirect `:80` → `:443`.

6. **Retry idempotent requests ONLY, with circuit breaking.** Auto-retrying a `POST`/`PATCH` that timed out can double-charge a card or double-write. Restrict retries to safe methods + connect/early failures, cap attempts, and stop retrying once the backend is clearly down.

   ```nginx
   proxy_next_upstream error timeout http_502 http_503;   # NOT non_idempotent — never blindly retry POST
   proxy_next_upstream_tries 2;
   proxy_next_upstream_timeout 10s;
   ```

   Envoy: `retry_policy` with `retry_on: connect-failure,refused-stream,unavailable`, `num_retries: 2`, plus `retry_back_off`. Add **circuit breaking** (Envoy `circuit_breakers` max connections/pending/retries, or outlier detection ejecting a 5xx-storming host) so retries don't amplify load against a struggling backend into a full meltdown.

7. **Sticky sessions only when state truly demands it.** Cookie/affinity routing (`sticky cookie`, Envoy hash policy) pins a client to one backend — necessary for in-memory session state, fatal for even load balancing and graceful drain (a drained node's clients all break). **First fix the state**: move sessions to Redis/JWT so any backend serves any user, then drop stickiness. Only keep it for unavoidable backend-local state, and pair it with consistent hashing so losing one node reshuffles minimally.

8. **Make reloads zero-drop (graceful drain).** A naive restart cuts in-flight connections → user-visible 5xx during every deploy.
   - **nginx:** `nginx -t && nginx -s reload` — the master spins up new workers on the new config and lets old workers finish in-flight requests before exiting. Never `kill -9` / hard restart for a config change.
   - **HAProxy:** run with `-sf $(cat pid)` (seamless finish) or the master-worker socket reload.
   - **Envoy:** hot restart / xDS push drains the old listener.
   - For removing a **backend**: first mark it `down`/drain in the pool and reload so the proxy stops sending *new* requests, wait for in-flight to finish, then stop the backend. Tie the backend's shutdown to its readiness probe (fail `/healthz` → proxy ejects → then SIGTERM) so the LB drains it before it dies.

## Common Errors

- **`proxy_read_timeout` shorter than the slowest real response.** Long uploads/reports hit a **504** even though the backend is healthy. Set the read timeout above the legitimate p99, and only then chase a slow endpoint separately.
- **Backend keepalive shorter than the proxy's upstream idle window.** Backend closes an idle socket the proxy then reuses → sporadic **502** under no real load. Make backend `keepalive_timeout` longer than the proxy's, and set `proxy_http_version 1.1` + `Connection ""`.
- **No `keepalive` in the upstream block.** Every request does a fresh TCP (and TLS) handshake to the backend — latency and CPU explode under load. Add `keepalive N` and clear the `Connection` header.
- **Retrying non-idempotent requests.** `proxy_next_upstream` including `non_idempotent` (or an Envoy `retry_on` that catches POSTs) silently double-executes writes on a timeout → duplicate charges/orders. Retry safe methods + connect failures only.
- **Health check that only pings the port / returns 200 unconditionally.** A node with a dead DB stays in rotation and 500s every request. Probe real dependencies in `/healthz`.
- **`ip_hash` / non-consistent hashing for affinity.** Removing or adding one node reshuffles *every* client to a new backend, blowing caches and sessions. Use `consistent` hashing.
- **Trusting client-supplied `X-Forwarded-For`/`X-Forwarded-Proto`.** The app sees spoofed client IPs or thinks plaintext is HTTPS. Reset these headers at the trust boundary (`proxy_set_header ... $remote_addr`/`$scheme`); never pass the raw inbound value through.
- **Hard restart on config change.** `systemctl restart nginx` / `kill -9` drops in-flight connections every deploy. Use `reload` / `-sf` graceful paths.
- **Stopping a backend before draining it.** Killing an instance while the LB still routes to it = a burst of 5xx for its in-flight requests. Drain (fail readiness → eject) first, then SIGTERM.
- **Default Envoy 15s route timeout left implicit.** Long-running requests get cut at 15s with no obvious cause. Set `route.timeout` explicitly per route.
- **Single proxy = single point of failure.** One LB box and the whole service is down when it dies or reloads badly. Run ≥2 behind a VIP/anycast/keepalived or a managed LB.

## Verify

1. **Config is valid before reload:** `nginx -t` (or `haproxy -c -f`, `envoy --mode validate`, `caddy validate`) returns OK. Never reload an unvalidated config.
2. **Balancing works:** fire `N` requests (`hey`, `vegeta`, `for i in $(seq 100); do curl -s .../whoami; done`) and confirm responses spread across all backends per the chosen algorithm (e.g. roughly even for round-robin).
3. **Dead-backend reroute, zero 5xx:** kill one backend mid-load. Traffic must reroute to healthy nodes and the client must see **no 5xx** (passive: a brief blip until `max_fails`; active: none). The killed node returns to rotation after it's healthy again.
4. **Timeouts behave:** point at a backend that sleeps longer than `proxy_read_timeout` → you get **504** at the configured time, not earlier/later. A backend refusing connections → **502** (not a retry storm).
5. **Retries are idempotent-only:** a timed-out `GET` retries to a second backend (one served response); a timed-out `POST` does **not** double-execute (assert the write happened exactly once at the backend).
6. **Zero-drop reload:** run sustained load (`vegeta attack -rate=200 -duration=60s`), trigger a config `reload` mid-run, and confirm **0 connection errors / 0 non-2xx** attributable to the reload in the report.
7. **TLS + forwarded headers:** `curl -v https://host` negotiates TLS1.2/1.3; the backend logs the real client IP (`X-Real-IP`) and sees `X-Forwarded-Proto: https`; `:80` 301-redirects to `:443`.
8. **Drain before stop:** mark a backend down, confirm new requests stop hitting it while in-flight ones complete, *then* stop it — no 5xx in the transition.

Done = killing a backend reroutes with **zero 5xx**, timeouts produce the right code at the right time, idempotent-only retries never double-write, and a config reload under sustained load drops **zero** in-flight connections — all with a validated config and ≥2 proxies (no single point of failure).
