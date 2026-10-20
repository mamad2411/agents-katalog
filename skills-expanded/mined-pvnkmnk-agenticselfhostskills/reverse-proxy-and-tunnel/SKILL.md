---
name: reverse-proxy-and-tunnel
description: Configures Nginx/Caddy reverse proxies and Cloudflare/WireGuard tunnels for safe homelab service exposure.
---

# reverse-proxy-and-tunnel

Manages safe external access to homelab services via reverse proxies (Nginx, Caddy) and tunnels (Cloudflare Tunnel, WireGuard, Tailscale). Enforces the `homelab-safe-ops` rule that no port is opened directly to the internet.

## Invocation

**OpenCode / Codex:** `Invoke reverse-proxy-and-tunnel`
**Freebuff:** `/skill reverse-proxy-and-tunnel`

## Access Patterns (choose one)

### Cloudflare Tunnel (recommended for public services)
- Install `cloudflared` on the host.
- Authenticate with Cloudflare account.
- Create a tunnel and route a subdomain to the local service.
- No inbound firewall ports required.

### Caddy Reverse Proxy (internal + Let's Encrypt TLS)
- Add a Caddyfile entry: `subdomain.domain.com { reverse_proxy localhost:PORT }`
- Caddy handles TLS automatically.

### Nginx Reverse Proxy
- Add a server block in `/etc/nginx/sites-available/`.
- Use Certbot for TLS.

### WireGuard / Tailscale (internal VPN access)
- Install WireGuard or Tailscale on both client and server.
- Route access over the VPN; never expose service port publicly.

## Safety

- Never open ports directly to WAN.
- Always use TLS for any public-facing endpoint.
- Validate DNS propagation before considering a tunnel live.
- Log configuration changes in `homelab-logbook`.

## Companion Skills

- `homelab-safe-ops` — safety gate
- `docker-app-deployer` — deploy the service first
- `homelab-logbook` — log network changes

## References

- Cloudflare Tunnel: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- Caddy docs: https://caddyserver.com/docs/
- Tailscale: https://tailscale.com/kb
