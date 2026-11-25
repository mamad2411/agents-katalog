---
name: assetsentry-stock-deploy
description: Deploy HayAegis (formerly AssetSentry) stock dashboard and services with proper path configuration for Tailscale subdomain/proxy access.
tags:
  - docker
  - streamlit
  - assetsentry
  - hayaegis
  - deployment
---

# HayAegis Stock Deployment

Deploy HayAegis stock portfolio dashboard and services with proper path configuration for Tailscale proxy access.

> [!TIP]
> For standard one-command restart and verification, use the `restart-stock` skill:
> `bash ~/.hermes/skills/restart-stock/scripts/restart.sh`

## Repository Location

```bash
/home/chihmin/HayAegis/HayAegis
```
*(Backward-compatible symlink maintained at `/home/chihmin/Assetsentry`)*

## Deployment via Docker Compose

```bash
cd /home/chihmin/HayAegis/HayAegis

# Build and start full stack with Tailscale HTTPS Funnel sidecar
docker compose -f docker-compose.yml -f docker-compose.override.yml --profile tailscale up -d --build
```

## Verification

```bash
# Check containers are running and healthy
docker compose -f docker-compose.yml -f docker-compose.override.yml --profile tailscale ps

# Test locally
curl -s http://localhost:8000/health/ready
curl -s http://localhost:80/ | head -20

# Test via Tailscale
curl -sk https://stock.crayfish-monitor.ts.net/ | head -20
```
