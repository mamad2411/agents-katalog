---
name: gateways
description: IPFS HTTP gateways — path vs subdomain, trusted vs trustless (verified CAR/block responses), origin isolation, CORS, and public gateway rate limits. Use when deciding how to expose IPFS content via HTTPS or debugging browser-side gateway behavior.
---

# IPFS HTTP gateways

## What You Probably Got Wrong

**You serve `/ipfs/<cid>/` on a shared origin and call it done.** Path
gateways (`https://gateway.example.com/ipfs/bafy…`) serve every CID
from the same HTTP origin. That means any CID's JavaScript shares
`localStorage`, cookies, and same-origin XHR with every other CID.
Malicious content on the same gateway can steal data from benign
content. Subdomain gateways (`<cid>.ipfs.example.com`) fix this by
giving each CID its own origin.

**You think "trustless gateway" is a marketing label.** It's not.
Trustless gateways serve verifiable responses — the client re-hashes
the returned blocks and confirms they match the requested CID. If
your gateway just proxies bytes from your Kubo node over HTTPS, it's
a **trusted** gateway: the client trusts you didn't swap content. A
trustless gateway supports `Accept: application/vnd.ipld.raw` or CAR
responses that the client can verify.

**You expose a public gateway without rate limiting.** Anyone on the
internet can request arbitrary CIDs through your node. Without rate
limiting, you're a free IPFS CDN for every phisher, malware
distributor, and accidental infinite loop. Cloudflare in front, or
Traefik/nginx rate limits, or both.

**You forget the CORS story.** Gateways serve content loaded by
third-party sites (a dApp on `app.example.com` loading images from
`ipfs.example.com`). Without `Access-Control-Allow-Origin: *`, browsers
block the load. But setting it wide-open on a _path_ gateway creates
the origin-isolation problem above. This is why subdomain gateways
exist.

## Path vs subdomain — what's actually different

### Path gateway

```text
https://gateway.example.com/ipfs/bafybeiabcd.../path/to/file.html
```

- **One HTTP origin for all content.** Shared `localStorage`, shared
  service worker scope, shared cookies.
- **Relative links break.** `<a href="/about">` resolves to
  `https://gateway.example.com/about`, not
  `https://gateway.example.com/ipfs/bafy…/about`.
- **Simplest to serve** — one hostname, one cert, any HTTP server.

Acceptable for: small private deployments, one-off public links, CLI
tools, backend-to-backend fetches.

Unacceptable for: serving dApp frontends, anything with active content.

### Subdomain gateway

```text
https://bafybeiabcd....ipfs.example.com/path/to/file.html
```

- **Each CID is its own origin.** Isolation by construction.
- **Relative links work.** `<a href="/about">` resolves inside the CID.
- **Needs a wildcard cert** for `*.ipfs.example.com` (and
  `*.ipns.example.com` if you serve IPNS).
- **Needs a wildcard DNS record** (`*.ipfs` → gateway IP).

This is the only correct answer for serving real web content from IPFS.

Kubo supports both; configure subdomain mode in `Gateway.PublicGateways`
with `UseSubdomains: true` — path requests auto-redirect to subdomain.

## Trusted vs trustless — what each actually does

### Trusted gateway (the default Kubo gateway)

Client sends: `GET /ipfs/bafy…/`
Server returns: the bytes the client asked for.

The client _cannot verify_ those bytes are the real content of `bafy…`
without re-fetching them via a different trust path. You trust the
gateway operator.

### Trustless gateway

Client sends: `GET /ipfs/bafy…?format=car` or `Accept:
application/vnd.ipld.car`
Server returns: a CAR (Content Addressable aRchive) file of the block
and its children.

The client re-hashes each block and verifies the CIDs match. If the
server lies, the client catches it.

Other trustless formats:

- `application/vnd.ipld.raw` — a single block, verifiable against the
  CID.
- `application/vnd.ipld.dag-json` / `dag-cbor` — structured block
  decoding with verification.

Helia (the JS IPFS client) and modern IPFS library clients speak these
formats; browsers with native IPFS support (Brave's IPFS mode) do too.

Specification: [HTTP Gateway specs](https://specs.ipfs.tech/http-gateways/).

## CORS — the rule you actually need

For subdomain gateways, the content loads on a _new_ origin per CID, so
cross-origin isn't an issue for in-CID resources. But if a dApp on
`app.example.com` wants to `fetch()` an IPFS asset through the gateway:

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, HEAD, OPTIONS
```

Kubo's gateway sets these automatically if configured:

```yaml
API:
  HTTPHeaders:
    Access-Control-Allow-Origin: ["*"]
    Access-Control-Allow-Methods: ["GET", "POST", "PUT", "OPTIONS"]
```

(The `API` section controls the gateway + API. For a public gateway
you almost always want `Gateway.HTTPHeaders` instead, but the default
behavior is sane.)

## Rate limiting — don't skip this

A public gateway is a foot-gun without limits. Cloudflare handles
rate-per-IP for proxied hostnames. At the origin:

- Traefik: `RateLimit` middleware.
- nginx: `limit_req_zone` + `limit_req`.
- Caddy: the `rate_limit` handler (community module) or a Cloudflare
  sidecar.

Rates to start with for a home-scale gateway: 10 req/s per IP, 100
concurrent connections.

Everything here is the **read gateway** (`:8080`), which is plain
request→response — any of the three proxies works. The Kubo _write_ API
(`:5001`) is the opposite: `/api/v0/add` is bidirectionally streaming and
needs a full-duplex proxy, so nginx deadlocks it. Keep `:5001` off the
public proxy entirely; see [`ipfs/SKILL.md`](../ipfs/SKILL.md) and
[`nginx/SKILL.md`](../nginx/SKILL.md).

## The public-gateway reality check

Using Protocol Labs' `ipfs.io` or Cloudflare's `cf-ipfs.com` as your
app's gateway means:

- You share rate limits with the entire internet.
- A large fetch may be rejected (Cloudflare's 100 MB cap).
- The gateway may de-peer from your node and serve cache misses as
  404s for content you pin.
- Availability depends on the operator's uptime.

Running your own gateway for your own content isn't optional if you
care about reliability. Running it for content _anyone_ can request is
a choice with real ops implications.

## Worked example: SPIRENS gateway

SPIRENS runs Kubo as a subdomain gateway:

- `ipfs.example.com` — root, path requests get 301'd to subdomain form.
- `*.ipfs.example.com` — per-CID origins.
- `*.ipns.example.com` — per-IPNS-key origins.
- Wildcard TLS via LE DNS-01 (see [`tls-acme/SKILL.md`](../tls-acme/SKILL.md)).
- Behind Traefik for TLS termination; direct-connect (DNS-only) on the
  wildcards because CF wildcard proxy is ACM-paid
  (see [`cloudflare/SKILL.md`](../cloudflare/SKILL.md)).

Details: [`docs/08-ipfs.md`](../docs/08-ipfs.md).

## Upstream references

- [HTTP Gateway specs](https://specs.ipfs.tech/http-gateways/)
- [Subdomain gateway spec](https://specs.ipfs.tech/http-gateways/subdomain-gateway/)
- [Trustless gateway spec](https://specs.ipfs.tech/http-gateways/trustless-gateway/)
- [Path gateway spec](https://specs.ipfs.tech/http-gateways/path-gateway/)
- [IPIP-328 — redirect support](https://specs.ipfs.tech/ipips/ipip-0328/)
- [Kubo gateway config](https://github.com/ipfs/kubo/blob/master/docs/config.md#gateway)
