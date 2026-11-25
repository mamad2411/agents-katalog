---
name: traefik-reverse-proxy
description: "Configure Traefik as a reverse proxy with Let's Encrypt TLS, Docker providers, and file-based routing — adding new services, managing ACME challenges, and cross-network container reachability."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [traefik, reverse-proxy, docker, letsencrypt, tls, acme, routing]
    triggers:
      - "add a new subdomain route to traefik"
      - "configure SSL/cert for a service behind Traefik"
      - "Traefik ACME challenge failing"
      - "HTTP-01 challenge blocked by redirect"
      - "switch to TLS-ALPN challenge"
      - "container not reachable from Traefik on different network"
      - "host.docker.internal pattern"
      - "deploy Postiz behind reverse proxy"
      - "app behind reverse proxy gives CORS errors on API calls because frontend uses localhost"
    related_skills:
      - docker-service-recovery
      - vps-application-deployment
      - static-site-deployment
---
# Traefik Reverse Proxy Configuration

## When to Use

When you need to:
- Add a new service behind an existing Traefik instance
- Configure TLS/SSL with Let's Encrypt for a new subdomain
- Debug ACME certificate issuance failures
- Connect a service container on a different Docker network to Traefik

## Traefik Architecture (the operator's Setup)

Traefik runs as a Docker container defined in:
`${MY_REPOS}\Documents\github\n8n\docker-compose.yml`

- **Ports**: 80 (HTTP → HTTPS redirect), 443 (HTTPS)
- **ACME**: Let's Encrypt with TLS-ALPN-01 challenge
- **File provider**: `/config` → `${MY_REPOS}\Documents\github\n8n\data\traefik\config\`
- **Docker provider**: Auto-discovers containers with Traefik labels

## Adding a New Service Route

### 1. Edit the File Provider Config

Add a **router** and a **service** to `data/traefik/config/docker-fallback.yml`:

```yaml
# Router — defines ingress rule
    <service-name>:
      rule: 'Host(`<subdomain>.your-domain.example`)'
      entryPoints:
        - 'websecure'
      service: '<service-name>'
      tls:
        certresolver: 'letsencrypt'

# Service — defines backend target
    <service-name>:
      loadBalancer:
        servers:
          - url: 'http://<target>:<port>'
        passHostHeader: true
```

### 2. Target URL Patterns

| Pattern | When to Use |
|---------|-------------|
| `http://<container-name>:<port>` | Service on the **same Docker network** as Traefik |
| `http://host.docker.internal:<host-port>` | Service on a **different Docker network** or on the **host** (e.g. localhost:4007) |

### 3. Force Config Reload (SIGHUP — Preferred)

The file watcher (`--providers.file.watch=true`) doesn't always trigger on Docker volume mounts, especially on Windows hosts. Instead of restarting the container:

```bash
docker kill -s HUP traefik
```

Then verify the new router and service appeared:

```bash
# List routers filtered to new service
docker exec traefik wget -q -O- http://localhost:8080/api/http/routers | python -c "import json,sys; data=json.load(sys.stdin); hits=[r for r in data if 'service-name' in r.get('name','').lower()]; print(f'Routers: {len(hits)}'); [print(f\"  {r['name']}: {r['status']} -> {r['rule']}\") for r in hits]"
```

```bash
# List services
docker exec traefik wget -q -O- http://localhost:8080/api/http/services | python -c "import json,sys; data=json.load(sys.stdin); hits=[s for s in data if 'service-name' in s.get('name','').lower()]; print(f'Services: {len(hits)}'); [print(f\"  {s['name']}: {s['status']}\") for s in hits]"
```

**Why SIGHUP over restart:** Zero downtime, preserves existing connections, doesn't trigger ACME re-issuance, fast (~1s). Always try SIGHUP first.

### 4. Alternative: Full Container Restart

If SIGHUP doesn't work (rare):

## ACME Challenge Types

### HTTP-01 (Default, but broken with redirect)

- Validates via `http://<domain>/.well-known/acme-challenge/<token>`
- **Requires port 80 to NOT redirect to HTTPS**
- The `--entrypoints.web.http.redirections.entryPoint.to=websecure` redirect intercepts the ACME challenge before Traefik can serve it, causing `403: unauthorized`
- **Do NOT use** when the HTTP entrypoint has a blanket redirect to HTTPS

### TLS-ALPN-01 (Preferred)

- Validates via port 443 using TLS handshake
- No port 80 dependency
- Works alongside HTTP→HTTPS redirect
- Switch in docker-compose.yml:
  ```yaml
  command:
    # Remove:
    # - --certificatesresolvers.letsencrypt.acme.httpchallenge=true
    # - --certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web
    # Add:
    - --certificatesresolvers.letsencrypt.acme.tlschallenge=true
  ```

### DNS-01

- Validates via DNS TXT records
- No port forwarding required — works on closed ports
- Requires DNS provider API credentials (e.g. Namecheap API)

## Pitfalls

- **HTTP-01 + Redirect conflict**: If the `web` entrypoint has `http.redirections.entryPoint.to=websecure`, the HTTP-01 challenge gets redirected instead of served. Switch to TLS-ALPN-01.
- **Different Docker networks**: Traefik and the target service must be on the same Docker network for container name resolution. If they're on different networks, use `host.docker.internal:<host-port>`.
- **certificatesresolvers.letsencrypt.acme.storage must persist**: Traefik stores issued certs in `acme.json`. If this file is lost, all certs must be re-issued.
- **File provider config must be valid YAML**: Traefik silently skips malformed config files. Use `docker logs traefik` to check for config errors.
- **`--providers.file.watch=true` doesn't always trigger on volume mounts**: The file watcher may miss changes when the config file is on a Docker volume mount (common on Windows hosts). If a new router doesn't appear after 10 seconds, force a reload with `docker kill -s HUP traefik`. Verify with the Traefik API at `localhost:8080/api/http/routers` or `api/http/services`.
- **Service name must match**: The router's `service:` field must match the service key name in the `services:` block exactly.
- **App-level CORS / broken API calls after routing**: Even when Traefik is routing correctly, the app's own frontend code may still reference `localhost:<port>` for API calls. Check the app's env vars (e.g. `NEXT_PUBLIC_BACKEND_URL`, `MAIN_URL`, `FRONTEND_URL`, `VITE_API_URL`) — they must point to the public domain, not localhost. Baked-in build-time values require a `docker compose down + create + start` (not just restart) since the container is recreated, or a full image rebuild if the framework baked the value into the JS bundle (Next.js pages router). With Next.js App Router + server components, `process.env.NEXT_PUBLIC_BACKEND_URL` is read at request time so a recreate is sufficient.
- **`http: 308 Permanent Redirect` on first setup**: Traefik returns 308 redirects for non-TLS requests. If a service health check uses HTTP, it gets redirected. Either use HTTPS in health checks or add an exception.

## Verification

After adding a route:

```bash
# Check Traefik logs for cert issuance
docker logs traefik --tail 30

# Verify HTTPS endpoint
curl -sk https://<domain>/ --max-time 10

# Check certificate details
echo | openssl s_client -connect <domain>:443 -servername <domain> 2>/dev/null | openssl x509 -noout -text | head -15

# Verify HTTP → HTTPS redirect
curl -skI http://<domain>/ 2>&1 | head -5
```
