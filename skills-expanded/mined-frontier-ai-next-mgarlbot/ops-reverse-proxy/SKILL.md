---
name: ops_reverse_proxy
description: Public deploy via Traefik/Nginx/frp on a VPS — inspect first; reverse proxy is **HTTP-only** by default (no TLS on the edge)
triggers: [traefik, nginx, reverse proxy, frp, frpc, subdomain, domain, tls, letsencrypt, certbot, proxy, ingress, ssl, public, реверс, поддомен, прокси, публичн]
tools: [shell]
platform: all
---

## Operator stack today: **HTTP-only on the reverse proxy**

Treat the edge (Traefik / Nginx / frp) as **plain HTTP** (port 80 or frp equivalent). **Do not** add TLS, `websecure`, `tls=true`, certresolver, or require Let’s Encrypt until **existing** projects on the same VPS clearly terminate HTTPS **or** the user explicitly asks for HTTPS.

Post-deploy check: `curl -sS -I http://<host>/` (and `Host:` if needed), not `https://` by default.

---

## Inspect first, then copy the pattern

Before writing a new `docker-compose.yml`, Traefik labels, or an Nginx `server {}`, understand **what already runs** on the target server and how **other projects** are wired. Otherwise you get a second incompatible stack (wrong Docker network, wrong entrypoint).

Remote VPS work uses **vps_host_ssh**:

```bash
ssh -F /data/.ssh/config vps 'COMMAND'
```

(If the bot runs without Docker but with HOST SHELL, the same SSH from the configured host is fine.)

### Step 1 — what serves traffic (HTTP first)

1. **Containers:** `docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'`
2. **Traefik:** names like `traefik`, `proxy`, image `traefik:*`. If present, sample labels from a **routed** service:
   - `docker inspect SERVICE_NAME --format '{{json .Config.Labels}}' | head -c 12000`
   - Check **entrypoints**: if everything is `web` / `:80`, new services stay HTTP-only. If you see `websecure` + `tls.certresolver`, copy TLS **like the neighbors**.
3. **Host Nginx:** `test -d /etc/nginx/sites-enabled && ls -1 /etc/nginx/sites-enabled || true` and optionally `grep -R listen /etc/nginx/sites-enabled/ 2>/dev/null | head -30` — if only `listen 80`, do not add `listen 443 ssl` without a user request and certs.
4. **frp:** `pgrep -a frpc || true`; common paths `~/frp/frpc.toml`, `/etc/frp/frpc.toml`, `/opt/frp/frpc.toml` — read-only. For HTTP prefer `type = http` and `customDomains`; do not switch to `https` without a clear need.

### Step 2 — where other compose projects live

Avoid aggressive `find /`:

```bash
ssh -F /data/.ssh/config vps 'for d in /opt /srv /var/www /root /home/*/apps; do test -d "$d" && ls -la "$d" 2>/dev/null; done'
ssh -F /data/.ssh/config vps 'ls -d /opt/*/docker-compose.yml /srv/*/docker-compose.yml 2>/dev/null | head -20'
```

Open **one** closest neighbor and note:

- External Docker **network** name (`traefik_public`, `web`, `proxy`, …);
- Traefik: label prefix, **entrypoints** (HTTP vs HTTPS), **certresolver** if any;
- Nginx: `server_name`, `listen`, `proxy_pass` / upstream.

### Step 3 — new service “like theirs”

- **Traefik HTTP (default):** same network as neighbors. Labels: `enable=true`, `rule=Host(\`sub.example.ru\`)`, `entrypoints=web` (or whatever neighbors use on :80). **No** `tls=true` if neighbors on that entrypoint have no TLS.
- **Traefik + TLS:** only if neighbors already use `websecure` and the same `tls.certresolver` — copy those names.
- **Nginx HTTP:** new `server { listen 80; server_name ...; location / { proxy_pass ... } }` like the neighbor. Certbot / `listen 443` only on explicit user request or if the whole host is already HTTPS.
- **frp:** same `type` and domain pattern as existing proxies; DNS (A) to **frps** if that is how neighbors work.

### Step 4 — DNS alignment

REG.RU subdomain — skill **ops_dns_regru**. A record points at the machine that actually receives **HTTP** (VPS or frps).

### Do not

- Remove neighbor sites or shared Traefik without explicit user approval.
- Paste secret file contents or full neighbor configs in chat — only facts (network names, entrypoints, paths).
