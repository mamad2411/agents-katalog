---
name: bytevirt-reality-node
description: "Use when provisioning or auditing a ByteVirt VPS as a no-panel Xray VLESS Reality Vision node: SSH into a fresh Debian 12 server, install Xray directly as a systemd service, generate per-node credentials, avoid exposing x-ui, verify port 443, and produce client import JSON or vless:// links for teammates."
---

# ByteVirt Reality Node

Use this skill when the user buys a ByteVirt VPS and wants a fresh Japan or other-region node like:

```text
client -> <bytevirt-ip>:443 -> Xray VLESS + Reality + Vision -> freedom outbound
```

Prefer a no-panel deployment unless the user explicitly asks for x-ui. Do not install or expose a public management panel by default. Do not store provider passwords, UUIDs, private keys, public keys, short IDs, or complete node links in the skill.

## Required Inputs

- ByteVirt public IPv4 address.
- SSH port.
- SSH user and auth method.
- Desired label, for example `vless-reality-jp-443`.
- Debian 12 is the preferred OS. If the provider asks for an OS, choose Debian 12.

If the user has just created the VPS and SSH times out during banner exchange, retry with `PubkeyAuthentication=no` and password-only auth before assuming the server is broken. ByteVirt may expose the TCP port before `sshd` is fully ready.

## Safety Defaults

- Install official Xray-core directly; do not install `x-ui` unless requested.
- Run Xray as a dedicated `xray` system user, not root.
- Give the systemd unit only the capabilities needed to bind low ports: `CAP_NET_BIND_SERVICE` and `CAP_NET_RAW`.
- Keep `/etc/xray/config.json` readable by the `xray` user only.
- Keep generated client material under `/root/<label>.txt` with mode `600`.
- Do not print private keys in the final answer. It is acceptable to print the complete `vless://` link only when the user explicitly needs it for import.
- If adding users for teammates, prefer one UUID per teammate so a single person can be disabled or rotated later.

## Preflight

Run from the local machine:

```bash
SSHPASS='<password>' sshpass -e ssh -4 \
  -o PubkeyAuthentication=no \
  -o PreferredAuthentications=password \
  -o NumberOfPasswordPrompts=1 \
  -o ConnectTimeout=15 \
  -o StrictHostKeyChecking=accept-new \
  -p <ssh-port> root@<ip> 'hostname; cat /etc/os-release; ss -tulpen | sed -n "1,100p"; df -hT /; free -h'
```

Expected for a clean VPS:

- Debian 12.
- SSH listening on the provider port.
- No service already listening on `443`.
- Enough memory for Xray; 1 GB works, 2 GB is better.

If `ssh` reports `Connection timed out during banner exchange` but `nc -vz <ip> <ssh-port>` succeeds, wait and retry. If `kex_exchange_identification: Connection closed by remote host` appears, retry with password-only auth as above.

## Install Xray

Run on the remote host:

```bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y ca-certificates wget unzip openssl

arch=$(uname -m)
case "$arch" in
  x86_64|amd64) asset="Xray-linux-64.zip" ;;
  aarch64|arm64) asset="Xray-linux-arm64-v8a.zip" ;;
  *) echo "unsupported arch: $arch" >&2; exit 1 ;;
esac

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
wget -q -O "$tmpdir/xray.zip" "https://github.com/XTLS/Xray-core/releases/latest/download/$asset"
unzip -q "$tmpdir/xray.zip" -d "$tmpdir/xray"

install -d -m 755 /usr/local/bin /usr/local/share/xray /etc/xray /var/log/xray
install -m 755 "$tmpdir/xray/xray" /usr/local/bin/xray
[ -f "$tmpdir/xray/geoip.dat" ] && install -m 644 "$tmpdir/xray/geoip.dat" /usr/local/share/xray/geoip.dat
[ -f "$tmpdir/xray/geosite.dat" ] && install -m 644 "$tmpdir/xray/geosite.dat" /usr/local/share/xray/geosite.dat

if ! id -u xray >/dev/null 2>&1; then
  useradd --system --no-create-home --shell /usr/sbin/nologin xray
fi
install -d -o xray -g xray -m 755 /var/log/xray
touch /var/log/xray/access.log /var/log/xray/error.log
chown xray:xray /var/log/xray/access.log /var/log/xray/error.log
chmod 640 /var/log/xray/access.log /var/log/xray/error.log
```

## Generate Credentials

Current Xray may print Reality keys as:

```text
PrivateKey: <private>
Password (PublicKey): <public>
```

Parse those exact labels, not older labels such as `Private key:` / `Public key:`:

```bash
uuid=$(/usr/local/bin/xray uuid)
keys=$(/usr/local/bin/xray x25519)
private_key=$(printf '%s\n' "$keys" | awk -F': ' '/^PrivateKey:/ {print $2}')
public_key=$(printf '%s\n' "$keys" | awk -F': ' '/^Password \(PublicKey\):/ {print $2}')
short_id=$(openssl rand -hex 8)

test -n "$uuid"
test -n "$private_key"
test -n "$public_key"
test -n "$short_id"
```

Use a real HTTPS site for Reality:

```text
server_name=www.cloudflare.com
dest=www.cloudflare.com:443
fingerprint=chrome
```

If this dest is changed, keep `serverName`/SNI and `dest` aligned.

## Server Config

Write `/etc/xray/config.json`:

```json
{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/xray/access.log",
    "error": "/var/log/xray/error.log"
  },
  "inbounds": [
    {
      "tag": "vless-reality-443",
      "listen": "0.0.0.0",
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "<uuid>",
            "email": "<label>",
            "flow": "xtls-rprx-vision"
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "show": false,
          "dest": "<dest>",
          "xver": 0,
          "serverNames": ["<server_name>"],
          "privateKey": "<private_key>",
          "shortIds": ["<short_id>"]
        }
      },
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls", "quic"]
      }
    }
  ],
  "outbounds": [
    { "protocol": "freedom", "tag": "direct" },
    { "protocol": "blackhole", "tag": "blocked" }
  ]
}
```

Set permissions:

```bash
chown xray:xray /etc/xray/config.json
chmod 600 /etc/xray/config.json
```

## systemd Unit

Write `/etc/systemd/system/xray.service`:

```ini
[Unit]
Description=Xray Service
Documentation=https://github.com/XTLS/Xray-core
After=network-online.target nss-lookup.target
Wants=network-online.target

[Service]
User=xray
Group=xray
CapabilityBoundingSet=CAP_NET_BIND_SERVICE CAP_NET_RAW
AmbientCapabilities=CAP_NET_BIND_SERVICE CAP_NET_RAW
NoNewPrivileges=true
ExecStart=/usr/local/bin/xray run -config /etc/xray/config.json
Restart=on-failure
RestartSec=5s
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
```

Start it:

```bash
/usr/local/bin/xray run -test -config /etc/xray/config.json
systemctl daemon-reload
systemctl enable --now xray.service
sleep 2
```

If the service exits with `open /etc/xray/config.json: permission denied`, fix config ownership for `xray`. If it exits with `open /var/log/xray/access.log: permission denied`, create the log files and `chown xray:xray` them before restarting.

## Client Link and JSON

Generate a client link:

```text
vless://<uuid>@<ip>:443?type=tcp&security=reality&pbk=<public_key>&fp=chrome&sni=<server_name>&sid=<short_id>&spx=%2F&flow=xtls-rprx-vision#<label>
```

For an Xray client JSON, replace only the `proxy` outbound values:

- `settings.vnext[0].address`: `<ip>`
- `settings.vnext[0].port`: `443`
- `settings.vnext[0].users[0].id`: `<uuid>`
- `settings.vnext[0].users[0].flow`: `xtls-rprx-vision`
- `streamSettings.security`: `reality`
- `streamSettings.realitySettings.serverName`: `<server_name>`
- `streamSettings.realitySettings.publicKey`: `<public_key>`
- `streamSettings.realitySettings.shortId`: `<short_id>`
- `streamSettings.realitySettings.fingerprint`: `chrome`
- `streamSettings.realitySettings.spiderX`: `/`

Do not change unrelated local DNS, TUN, or routing rules unless the user asks.

## Verification

Run before handoff:

```bash
systemctl is-enabled xray.service
systemctl is-active xray.service
ss -tulpen | grep ':443'
journalctl -u xray -n 40 --no-pager
nc -vz -w 8 <ip> 443
```

Expected:

- `xray.service` is `enabled` and `active`.
- `xray` listens on `*:443`.
- Public TCP connection to `<ip>:443` succeeds.
- No `x-ui.service` is present unless explicitly requested.

## Handoff

Report:

- VPS IP, SSH port, OS, and Xray version.
- Protocol summary: `VLESS + Reality + Vision`, `tcp`, `443`, SNI/dest.
- Service status and public `443` reachability.
- Path to `/etc/xray/config.json` and `/root/<label>.txt`.
- Client link or full client JSON only when the user asks for it.

Do not include SSH passwords, private keys, or old failed credentials in the handoff.
