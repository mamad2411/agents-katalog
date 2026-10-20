---
name: spirens-skills
description: Table of contents for the SPIRENS decentralized-web infra skills. Fetch a specific skill (e.g. `ship/SKILL.md`, `tls-acme/SKILL.md`) when the user's question matches its topic.
---

# SPIRENS Skills

Short, intent-triggered guides for the infrastructure SPIRENS ships — IPFS,
IPNS, gateways, ENS resolution, TLS/ACME, DNS/Cloudflare, Traefik, and the
common alternatives (nginx, Caddy). Each skill corrects a specific blind
spot LLMs tend to have about this stack.

Modeled on [`ethskills`](https://github.com/austintgriffith/ethskills).
ethskills covers Ethereum itself; this plugin covers the infra that makes a
decentralized-web deployment actually serve traffic.

## Start here

- [`ship`](./ship/SKILL.md) — end-to-end path from bare domain to live
  `https://rpc.example.com`. Fetch FIRST; routes to the rest.

## Naming & discovery

- [`dns`](./dns/SKILL.md) — records, TTL, CAA, propagation reality.
- [`cloudflare`](./cloudflare/SKILL.md) — proxy vs DNS-only, API tokens,
  Universal SSL interaction.
- [`ipns`](./ipns/SKILL.md) — keys, publishing, TTL — and why dnslink is
  usually what you want instead.
- [`ens-resolution`](./ens-resolution/SKILL.md) — ENS name → contenthash
  → IPFS CID → gateway, via dweb-proxy.

## Transport & certs

- [`tls-acme`](./tls-acme/SKILL.md) — ACME protocol, DNS-01 vs HTTP-01 vs
  TLS-ALPN-01, wildcards, rate limits.
- [`lets-encrypt`](./lets-encrypt/SKILL.md) — LE specifics: chain of
  trust, renewals, ECDSA vs RSA, account keys.

## Content routing

- [`ipfs`](./ipfs/SKILL.md) — Kubo operation, pinning, peering, DHT vs
  delegated routing.
- [`gateways`](./gateways/SKILL.md) — subdomain vs path, trusted vs
  trustless, origin isolation.

## Reverse proxies

- [`traefik`](./traefik/SKILL.md) — entrypoints / routers / services /
  middlewares, ACME resolver, file vs label provider.
- [`nginx`](./nginx/SKILL.md) — http vs stream, TLS termination vs
  passthrough, certbot, upstream blocks.
- [`caddy`](./caddy/SKILL.md) — automatic HTTPS, Caddyfile, on-demand
  TLS risks, reverse_proxy patterns.

## JSON-RPC

- [`erpc`](./erpc/SKILL.md) — finality-aware caching, hedging, failover,
  per-chain config tiers.
- [`helios`](./helios/SKILL.md) — a16z's trustless light client.
  `eth_getProof` requirement, checkpoint trust, placement between
  dweb-proxy and eRPC.

## Topology

- [`topology`](./topology/SKILL.md) — single-host Compose vs Docker
  Swarm, overlay networks, stateful-service constraints.

## Worked example

Every skill links back into the SPIRENS repo for a real config you can
read or copy (`config/`, `compose/`, `docs/`). The skills themselves
stay short — for long-form, follow the links into
[`docs/`](./docs/index.md).
