---
name: cloudflare-tunnel-ops
description: >
  Operate Cloudflare Tunnel (cloudflared): install, service mode, ingress rules,
  credentials/token security, HA replicas, DNS routing, and origin lockdown so apps
  are not exposed on the public Internet. Use for owned expose patterns with Zero
  Trust — pair with cloudflare-access-policies for identity; do not tunnel unowned
  networks without authorization.
---

# Cloudflare Tunnel Ops

## Scope And Authorization

- **In scope:** networks and hosts you own; authorized lab tunnels.
- **Out of scope:** tunneling into third-party networks; covert exfil channels.
- Protect `*.json` tunnel credentials and install tokens as secrets.
- Prefer least-privilege local service accounts for cloudflared.
- Pair with `cloudflare-access-policies` for identity at the edge.

## When To Use

- Exposing internal HTTP/TCP services without opening inbound firewall ports.
- Replacing VPN-only admin access with CF Tunnel + Access.
- Running highly available `cloudflared` replicas.
- Tokens: cloudflared, tunnel ingress, tunnel token, private network, WARP-to-tunnel.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Access policy design | `cloudflare-access-policies` |
| Workers/R2/D1 | respective cloudflare-* skills |
| Generic VPN design | network architecture skill |
| Cilium/K8s policy | `cilium-network-policy-basics` |

## Architecture

```text
Client → Cloudflare edge → Tunnel (cloudflared) → origin localhost/service
```

| Piece | Notes |
| --- | --- |
| Tunnel ID | Stable identity in CF account |
| Credentials / token | Authenticates cloudflared; treat as root to origin |
| Ingress rules | Hostname → service URL mapping |
| Origin | Should not be publicly reachable |

## Workflow

### 1. Confirm scope and success criteria

1. Hostnames, origin URLs, HA needs, Access required or not, owners.
2. Success: DNS routes to tunnel; origin closed to Internet; Access enforced if planned; failover works.
3. Rollback: previous ingress config; keep one healthy replica during changes.

### 2. Install and authenticate

```bash
# Linux service example (version pin in real ops)
cloudflared --version
# Token-based install (preferred in many orgs) — token from dashboard, store in vault
sudo cloudflared service install "$TUNNEL_TOKEN"
sudo systemctl status cloudflared
```

1. Prefer **token** install managed by CF for simpler rotation patterns where supported.
2. If using `cert.pem` + credentials JSON, restrict filesystem permissions `0600`, root-only.

### 3. Configure ingress

```yml
# config.yml (if file-based)
tunnel: TUNNEL_ID
credentials-file: /etc/cloudflared/ creds.json

ingress:
  - hostname: app.internal.example.com
    service: http://127.0.0.1:8080
  - hostname: ssh.internal.example.com
    service: ssh://127.0.0.1:22
  - service: http_status:404
```

1. Always end with catch-all `http_status:404`.
2. Use localhost origins; avoid pointing tunnel at wide internal ranges unless private network feature is intentionally designed.
3. For Kubernetes: deployment with multiple replicas, same tunnel token.

### 4. DNS and Access

1. Route hostname CNAME to tunnel target via CF dashboard/API (`cloudflared tunnel route dns`).
2. Attach **Access** application policies for human-facing HTTP.
3. Ensure origin firewall: no `0.0.0.0/0` on app ports.

### 5. HA and upgrades

1. Run ≥2 `cloudflared` replicas on separate hosts/AZs.
2. Pin versions; stage upgrades.
3. Health: systemd + CF tunnel health metrics; alert on disconnect.

### 6. Verify

```bash
curl -sI https://app.internal.example.com/
# Expect Access redirect or 200 if bypass intentional
# From Internet to origin IP:port → should time out / refuse
ss -lntp | rg 8080  # only localhost
journalctl -u cloudflared -n 100 --no-pager
```

1. Kill one replica → traffic still flows.
2. Invalid hostname → 404 catch-all, not random origin.

### 7. Incident / secrets

1. Leaked tunnel token/creds → rotate tunnel credentials immediately; reinstall service.
2. Compromised host → revoke tunnel, rebuild host, review origin access logs.
3. Do not commit credentials JSON to git.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Origin | Localhost + host firewall | Public IP still open “for debug” |
| Secrets | Vault + 0600 files | Creds in world-readable home |
| Ingress | Explicit hostnames + 404 | Broad IP routes by accident |
| Identity | Access on admin UIs | Tunnel alone = security |
| HA | Multi-replica | Single laptop cloudflared prod |

## Output Checklist

- [ ] Tunnel created; credentials/token vaulted
- [ ] Ingress rules reviewed with catch-all
- [ ] DNS routed; TLS at CF edge OK
- [ ] Access policies attached where required
- [ ] Origin not Internet-reachable
- [ ] HA replicas and upgrade plan
- [ ] Monitoring/alerts on tunnel down
- [ ] Rotation runbook tested
- [ ] Residual risk documented

## Rules

- Authorized networks only.
- Tunnel credentials are high value — protect and rotate.
- Prefer Access + origin lockdown over tunnel-only trust.
- Focus on **tunnel ops**; policy detail in `cloudflare-access-policies`.
