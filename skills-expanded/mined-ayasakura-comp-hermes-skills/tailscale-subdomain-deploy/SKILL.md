---
name: tailscale-subdomain-deploy
description: Deploy a local port service behind a Tailscale subdomain (e.g. https://<host>.<tailnet>/service-name). Handles service startup, Tailscale serve path routing, and TLS cert generation.
tags:
  - docker
  - streamlit
  - fastapi
  - deployment
  - tailscale
---

# Tailscale Subdomain Path Deploy

Deploy a local service running on a specific port and expose it via a Tailscale subdomain path (e.g. `https://aya.crayfish-monitor.ts.net/stock`).

## When to use

- A service (Docker, uv run, etc.) is running on `localhost:<port>` and needs to be exposed on the tailnet
- User wants `https://<hostname>.<tailnet-domain>/<subpath>` format access
- Combined with other deploy skills (docker-uv-deploy, etc.)

## Prerequisites

1. Tailscale is installed and active (`tailscale status` should show connected)
2. Service is already running on a known localhost port
3. Tailscale hostname is configured (`hostname` command)
4. Tailnet domain is known (check with `tailscale status --json`)

## Workflow

### Step 1: Get Tailscale Hostname & Tailnet Domain

```bash
tailscale status --json 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
s = d.get('Self', {})
print('HostName:', s.get('HostName'))
for name in s.get('DNSNames', []):
    print('DNSName:', name)
"
```

Example output:
```
HostName: aya
DNSName: aya.crayfish-monitor.ts.net
```

### Step 2: Ensure Service is Running

Start the service on `localhost:<port>` before configuring Tailscale serve.

**For Docker containers:**
```bash
docker ps --filter name=<container-name> --format "{{.Names}} {{.Status}}"
# If not running:
cd /path/to/service
docker compose up -d
```

**For uv-based services (Streamlit, FastAPI, etc.):**
```bash
cd /path/to/service
uv sync  # install deps
uv run streamlit run app.py --server.address 0.0.0.0 --server.port=<port>
# or
uv run python main.py --port <port>
### Step 3: Configure Tailscale Serve Path

**For Tailscale v1.98+ (current version):**

```bash
# Add new route
sudo tailscale serve --bg --set-path /<subpath> http://localhost:<port>/

# Remove existing route
sudo tailscale serve --https=443 --set-path=/oldpath off
```

**Example - Add /search for SearXNG on port 8081:**
```bash
sudo tailscale serve --bg --set-path /search http://localhost:8081/
```

**Example - Remove old / route:**
```bash
sudo tailscale serve --https=443 --set-path=/ off
```

**⚠️ Note:** `tailscale serve --json` is NOT supported in v1.98+. Use `--set-path` for adding routes and `off` for removing routes.

**Fallback for older Tailscale versions:**
If `set-config` is available, you can also:
1. `tailscale serve get-config --all > /tmp/ts-serve.json` to export
2. Modify the JSON file
3. `tailscale serve set-config /tmp/ts-serve.json --all` to apply

**Verify:**
```bash
sudo tailscale serve status
sudo tailscale serve status --json  # detailed
```

### Step 4: Verify

```bash
# Check serve config
sudo tailscale serve status

# Test via curl
curl -s https://<hostname>.<tailnet>/<subpath> | head -20
```

## Framework-Specific Notes

### Streamlit (must use baseUrlPath)

When Streamlit runs behind a subpath (Tailscale `/stock`, nginx `/app`, etc.), static resources fail to load.

**Fix:** Add `--server.baseUrlPath` to the Streamlit command:
```bash
uv run streamlit run dashboard.py --server.address 0.0.0.0 --server.baseUrlPath=/stock
```

Then Tailscale proxy:
```bash
sudo tailscale serve --bg --set-path /stock http://localhost:8501/stock
```

**Without `--server.baseUrlPath`, the page will be blank.**

### SearXNG (root path only)

SearXNG serves at root path `/` only. Never proxy to `/searxng`.

```bash
sudo tailscale serve --bg --set-path /search http://localhost:8081/
```

## Troubleshooting

### Blank page (especially Streamlit)
- **Cause:** App doesn't know it's behind a subpath
- **Fix:** Add framework-specific base path config (e.g., Streamlit `--server.baseUrlPath=/subpath`)

### Port conflict (Bind for 0.0.0.0:<port> failed)
- **Cause:** Another service or old container holds the port
- **Fix:** `docker stop <container> && docker rm <container>` or `lsof -i :<port>` to find the offender

### Serve config not persisting after reboot
- **Cause:** Tailscale serve config is stored in `/var/lib/tailscale/serve-config.json`
- **Fix:** Ensure Tailscale service is enabled: `sudo systemctl enable tailscale`

### Testing curl from localhost
- **Cause:** `curl https://host/ts.net` may resolve to localhost but TLS SNI fails
- **Fix:** Use `curl --resolve "<fqdn>:443:100.x.x.x" https://<fqdn>/subpath`

### DNS name changed after hostname update
- **Cause:** Tailnet domain may change (e.g. `tail465b60.ts.net` → `crayfish-monitor.ts.net`)
- **Fix:** Always re-check `DNSNames` after `sudo tailscale set --hostname=<name>`, then re-configure serve

## Quick Reference

| Action | Command |
|---|---|
| Check Tailscale status | `tailscale status` |
| Get DNS names | `tailscale status --json 2>&1 \| python3 -c "..."` |
| Configure serve | `sudo tailscale serve --json '{...}'` |
| Check serve config | `sudo tailscale serve status` |
| Check serve config as JSON | `sudo tailscale serve status --json` |
| Remove all routes | `sudo tailscale serve reset` |
| Generate TLS cert | `sudo tailscale cert <fqdn>` |
| Test locally | `curl -s https://<fqdn>/subpath` |

## Pitfalls

- **Streamlit needs `--server.baseUrlPath`** or the page will be blank behind a subpath
- **SearXNG serves at `/`** — proxy to `http://localhost:8081/`, NOT `http://localhost:8081/searxng`
- **Tailscale v1.98+ does NOT support `--json`** — use `--set-path` + `off` instead
- **Changing hostname can change the entire Tailnet domain** — always re-check DNSNames before serving
- **`/etc/hosts` entries** are temporary for testing — rely on Tailscale MagicDNS for actual access
- **`set-config --all <file>` has a CLI bug** in v1.98.1 — "must specify filename" error even with file. Use `--set-path` instead.
- **`get-config --all` returns incomplete data** — only returns `{"version": "0.0.1"}`, not the full serve config
