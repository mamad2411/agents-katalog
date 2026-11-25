---
name: solcast-proxy
description: "Caching reverse proxy for the Solcast solar forecast API. Caches responses so multiple clients share one set of API calls from the daily quota. Relevant when working with solar data, Solcast API integration, or setting up solar forecast infrastructure."
allowed-tools:
  - Bash(solcast-proxy:*)
  - Read
user-invocable: false
metadata:
  author: bradleydwyer
  version: "0.1.0"
  status: stable
---

# solcast-proxy — Caching Reverse Proxy for Solcast

A local proxy that sits between your clients and the Solcast API. It caches responses with a configurable TTL so that multiple consumers (Home Assistant, dashboards, scripts) can read solar forecast data without each one burning API calls from your daily quota.

## When This Skill Is Relevant

- Setting up or troubleshooting Solcast API integration
- Configuring solar forecast data pipelines
- Reducing Solcast API call usage across multiple consumers
- Debugging solar production/forecast data issues

## CLI Reference

```bash
# Start on default port 8888
solcast-proxy

# Custom port
solcast-proxy -p 9000

# Custom cache TTL in seconds (default varies)
solcast-proxy --ttl 3600

# Minimum seconds between upstream API calls
solcast-proxy --rate-limit 9000

# Custom cache directory
solcast-proxy -c /path/to/cache
```

## How It Works

Clients point at `http://localhost:8888` instead of `https://api.solcast.com.au`. The proxy forwards the first request upstream, caches the response, and serves subsequent requests from cache until the TTL expires. The `--rate-limit` flag enforces a minimum interval between upstream calls regardless of TTL, protecting your quota from bursts.
