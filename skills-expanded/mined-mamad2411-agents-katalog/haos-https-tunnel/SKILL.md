---
name: haos-https-tunnel
description: Give a Home Assistant OS (HAOS) instance a real HTTPS URL — inside and outside the LAN — via a Cloudflare Tunnel (cloudflared add-on), with no port forwarding and no device-side install. Use when the user wants HTTPS / remote access / external access for Home Assistant, mentions cloudflared, Cloudflare Tunnel, HA App 外部連線, HA 走 https, or asks how to reach HA from outside without exposing their home IP. Also consult it before ever suggesting DuckDNS, port forwarding, or HA-native SSL for a HAOS box — this route beats those on safety and side effects.
---

# HAOS HTTPS via Cloudflare Tunnel

Give a HAOS box a public `https://ha.<domain>` that works from anywhere, without opening
router ports or installing anything on client devices. Battle-tested 2026-07-10 on a
Raspberry Pi 4 (HAOS 18.1, Core 2026.6.4) with the **brenner-tobias/cloudflared** add-on
v7.0.9. Every pitfall below was hit for real; ⚠️ marks them.
`ha` = SSH alias into the Advanced SSH & Web Terminal add-on (see `haos-addon-deploy` §8
for SSH setup; Protection mode must be off).

## 0. Why this route (and what was rejected)

Tunnel = the RPi opens an **outbound** long-lived connection to Cloudflare; DNS is a
CNAME to `cfargotunnel.com`, never your home IP. No inbound port, dynamic IP is a
non-event, TLS terminates at Cloudflare against a tunnel token.

Rejected alternatives (don't re-suggest without new facts):
- **HA-native SSL** (`http: ssl_certificate`): forces HTTPS globally — local
  `http://<ip>:8123` stops working and everything gets slower. Real-world regret.
- **DuckDNS + port-forward 443**: exposes the home IP and an inbound port to the internet.
- **Nabu Casa**: works, but monthly fee.
- **Tailscale**: needs an app on every client device.

## 1. Prerequisites

- A domain **in the user's Cloudflare account as a zone**. Bought via Cloudflare
  Registrar → zone exists automatically. Verify from anywhere:
  `dig +short NS <domain>` → should return `*.ns.cloudflare.com` names.
- SSH access to the HAOS box per `haos-addon-deploy` §0/§8 (⚠️ non-interactive `ha` CLI
  calls need `ssh ha 'bash -lc "…"'`, otherwise `unauthorized`).
- ⚠️ You (the agent) can do everything below **except one step**: the Cloudflare login
  authorisation (§5) is the user's — plan the hand-off.

## 2. Install the cloudflared add-on

```bash
ssh ha 'bash -lc "ha store add https://github.com/brenner-tobias/ha-addons && ha store reload"'
ssh ha 'bash -lc "ha store repositories | grep -B2 -A4 -i brenner"'   # repo slug: 9074a9fa
ssh ha 'bash -lc "ha apps install 9074a9fa_cloudflared"'
```

- ⚠️ The subcommand is **`ha store add <url>`**. There is no `add-repository`; a wrong
  subcommand doesn't error — it dumps the whole store listing and exits 0, so verify the
  repo actually appeared (`ha store repositories`) instead of trusting the exit code.
- The installed add-on slug is `<repo-slug>_cloudflared`, e.g. `9074a9fa_cloudflared`.

## 3. Configure the add-on

Only one option is required — the public hostname:

```bash
echo '{"options":{"external_hostname":"ha.<domain>","additional_hosts":[]}}' \
  | ssh ha 'bash -lc "curl -sS -X POST -H \"Authorization: Bearer \$SUPERVISOR_TOKEN\" \
            -H \"Content-Type: application/json\" -d @- \
            http://supervisor/addons/9074a9fa_cloudflared/options"'
```

(Or the add-on's Configuration tab in the HA UI.) Other options — `tunnel_token`
(for a dashboard-managed tunnel), `additional_hosts` (expose more services later),
`catch_all_service` — are not needed for the basic HA case.

## 4. Trust the proxy in configuration.yaml (before first start)

Tunnel traffic reaches HA as reverse-proxied requests; HA rejects them (or logs the
proxy's IP for everything, breaking `ip_ban_enabled`) unless the proxy subnet is trusted:

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.30.33.0/24   # Supervisor docker subnet, where add-ons live
  ip_ban_enabled: true          # public endpoint now — keep this on
  login_attempts_threshold: 3
```

- File location from the SSH add-on: **`/config/configuration.yaml`**
  (`/homeassistant/...` is an alias mount of the same volume).
- ⚠️ `/config` is root-owned — `cp`/`sed` need **sudo** from the SSH add-on.
- High-risk config edit: back up first (`sudo cp configuration.yaml
  configuration.yaml.bak-YYYYMMDD`), then edit, then **`ha core check`** before
  `ha core restart`. Don't skip the check — a broken yaml keeps HA from booting.
- Local plain-HTTP access (`http://<lan-ip>:8123`) keeps working — unlike native SSL,
  nothing is forced. HA App: set the new URL as **external**, keep the LAN URL internal.

## 5. Start and authorise (user hand-off)

```bash
ssh ha 'bash -lc "ha apps start 9074a9fa_cloudflared"'
ssh ha 'bash -lc "ha apps logs 9074a9fa_cloudflared"'
```

First start with no `tunnel_token`: the log prints
`Please open the following URL and log in with your Cloudflare account:` followed by a
`https://dash.cloudflare.com/argotunnel?...` link. **Hand this URL to the user** — they
log in, pick the zone, authorise. cloudflared then downloads the cert, creates the
tunnel, and **creates the DNS CNAME itself** — no manual DNS work.

## 6. Verify

```bash
ssh ha 'bash -lc "ha apps logs 9074a9fa_cloudflared"' | grep -iE "registered|route|error"
# want: "Added CNAME ha.<domain> …" + 4× "Registered tunnel connection"
curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" https://ha.<domain>/
# want: 200
```

- ⚠️ A precheck line `UDP Connectivity … QUIC connection failed / degraded transport,
  will proceed using 'http2'` is **fine** — some networks block outbound UDP 7844;
  http2 fallback works. Only a hard fail matters.
- Nearby edge locations in the "Registered tunnel connection" lines (e.g. `tpe01`)
  = good latency; nothing to configure.

## 7. Post-setup (tell the user)

- **Enable 2FA** on HA accounts — the login page is now on the public internet.
  `ip_ban_enabled` + `login_attempts_threshold` (§4) are the second line, not a substitute.
- **HA App**: external URL → `https://ha.<domain>`; internal URL → keep the LAN address.
- **Take a full HA backup now** (config just changed) and pull it off the box —
  `scp ha:/backup/<file>.tar` beats the web download. Don't git-track `/config`
  wholesale: `.storage/` holds auth tokens and `secrets.yaml` is a secret.
