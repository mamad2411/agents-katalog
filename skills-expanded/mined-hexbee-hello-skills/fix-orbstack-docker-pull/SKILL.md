---
name: fix-orbstack-docker-pull
description: Diagnose and fix Docker image pull failures on macOS with OrbStack, especially Docker Hub EOF/TLS/manifest errors caused by system proxies, Clash/CyberClash/Mihomo/Surge-style TUN mode, fake-ip DNS such as 198.18.0.x, or unstable registry access. Use when `docker pull` or `docker manifest inspect` fails with EOF, SSL_ERROR_SYSCALL, failed to fetch anonymous token, failed to resolve reference, failed to copy, or registry-1.docker.io/auth.docker.io connectivity confusion.
---

# Fix OrbStack Docker Pull

## Core Rule

Treat Docker Hub `EOF` on OrbStack as a network path problem until proven otherwise. Do not assume the image is missing, private, or platform-incompatible before testing a small public image and the daemon's proxy path.

Expected responses that are not failures:

- `curl -I https://auth.docker.io` returning `HTTP/2 404` is normal for the auth service root.
- `curl -I https://registry-1.docker.io` returning `HTTP/2 404` is normal for the registry root.
- `curl -I https://registry-1.docker.io/v2/` returning `401` with `www-authenticate: Bearer ...` is the expected unauthenticated registry response.

Suspicious signals:

- `docker pull hello-world:latest` fails with `Head "https://registry-1.docker.io/v2/.../manifests/latest": EOF`.
- `docker buildx imagetools inspect` or `docker manifest inspect` fails while explicit `curl -x http://127.0.0.1:<port>` succeeds.
- `registry-1.docker.io` resolves to `198.18.0.x`, which usually indicates Clash-style fake-ip/TUN routing.
- macOS has system HTTP/HTTPS proxy enabled, but OrbStack Docker daemon is still using an unstable automatic proxy path.

## Quick Diagnose

Run the bundled read-only diagnostic script first when local shell access is available:

```bash
/Users/jiamingfeng/.codex/skills/fix-orbstack-docker-pull/scripts/diagnose-orbstack-docker-pull.sh
```

If the skill has been installed elsewhere, resolve the script relative to this `SKILL.md`.

If running manually, collect these facts:

```bash
docker version
docker info
orb version
orb config get network_proxy
sed -n '1,120p' ~/.orbstack/config/docker.json
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
dscacheutil -q host -a name registry-1.docker.io
dig registry-1.docker.io
netstat -rn -f inet | grep -E '198\\.18|default|utun'
curl -I --max-time 15 https://registry-1.docker.io/v2/
curl -x http://127.0.0.1:7890 -I --max-time 15 https://registry-1.docker.io/v2/
docker pull hello-world:latest
```

Adapt the proxy port from `networksetup`; do not hard-code `7890` unless the system proxy reports it.

## Fix Workflow

1. Confirm the issue is general:

```bash
docker pull hello-world:latest
```

If `hello-world` also fails with Docker Hub `EOF`, focus on daemon networking rather than the requested image.

2. Find the active macOS proxy:

```bash
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
ps aux | grep -Ei 'clash|cyberclash|mihomo|sing-box|surge|stash|v2ray|xray|shadow|proxy' | grep -v grep
```

If `Server: 127.0.0.1` and `Port: 7890` appear, the proxy URL is `http://127.0.0.1:7890`. Use the actual service name if the Mac is not using `Wi-Fi`.

3. Make OrbStack use the proxy explicitly:

```bash
orb config set network_proxy http://127.0.0.1:<port>
orb restart docker
```

Verify:

```bash
orb config get network_proxy
docker pull hello-world:latest
```

4. If pulls still intermittently EOF or large layers hang, reduce Docker daemon download concurrency:

```json
{
  "max-concurrent-downloads": 1
}
```

Write that JSON to `~/.orbstack/config/docker.json`, preserving any existing daemon settings. Then restart:

```bash
orb restart docker
docker pull <image>
```

5. Continue interrupted pulls instead of cleaning state:

```bash
docker pull <image>
docker system df
orb logs docker | tail -80
```

Docker often retains partially downloaded blobs after an interrupted pull. Avoid `docker system prune` unless the user explicitly wants to discard partial progress.

## Interpretation Guide

- `registry-1.docker.io` resolving to `198.18.0.x` is a fake-ip/TUN clue, not the real Docker Hub endpoint.
- `curl -x http://127.0.0.1:<port> -I https://registry-1.docker.io/v2/` succeeding while direct curl or Docker fails means the explicit proxy path is healthier than auto/TUN routing.
- `docker manifest inspect` may fail from the macOS-side client path even when `docker pull` succeeds through the daemon path; prioritize `docker pull hello-world` and the actual target pull for validation.
- A long pause during a large layer can still be normal. Check `docker system df` growth or daemon logs before killing the pull.
- If the proxy port changes after reboot, update OrbStack with the new port and restart Docker.

## Persistence

These settings persist across Mac reboots:

```bash
orb config get network_proxy
sed -n '1,120p' ~/.orbstack/config/docker.json
```

Before future pulls, the user usually only needs OrbStack and the proxy app running. If the proxy app changes port, rerun:

```bash
orb config set network_proxy http://127.0.0.1:<new-port>
orb restart docker
```
