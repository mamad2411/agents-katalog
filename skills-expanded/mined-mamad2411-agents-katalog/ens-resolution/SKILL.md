---
name: ens-resolution
description: ENS name → contenthash → IPFS CID → gateway, including wildcard resolvers, dweb-proxy pattern, and the DoH trick Kubo uses for `.eth` resolution. Use when a user wants browser-navigable ENS pages or to debug `vitalik.eth`-style resolution.
---

# ENS resolution (name → content)

## What You Probably Got Wrong

**You think `vitalik.eth` resolves in the browser.** Mostly it doesn't.
Brave has native ENS. Firefox and Chrome don't. Safari doesn't. "Type
`.eth` into the URL bar and it works" is a browser-specific feature,
not a web standard. For broad reach you need a gateway hostname
(`vitalik.eth.example.com` → your infra → resolves and redirects).

**You think ENS has DNS-like zone records.** It has a smart-contract
resolver. Each ENS name has a resolver contract address; the resolver
contract has typed getters (`addr(bytes32)`, `contenthash(bytes32)`,
`text(bytes32, string)`). Resolving a name means: (1) look up the
registry to find the resolver, (2) call the resolver's getter for the
field you want. Not TXT records. Not DNS.

**You skip the RPC dependency.** Resolving ENS is JSON-RPC calls to an
Ethereum node. No RPC = no resolution. If your RPC is flaky, your ENS
gateway is flaky. This is why SPIRENS layers eRPC under dweb-proxy —
see [`erpc/SKILL.md`](../erpc/SKILL.md).

**You assume contenthash points to IPFS.** It usually does, but the
contenthash format (EIP-1577) is a multicodec-prefixed blob that can
encode IPFS, IPNS, Swarm, Onion, or others. Decoders parse the prefix
byte and pick a handler.

## The resolution chain

```text
vitalik.eth
   │  (1) ENS Registry contract → resolver address
   ▼
Resolver contract
   │  (2) contenthash(namehash("vitalik.eth")) → 0xe3…cid…
   ▼
Multicodec decode (EIP-1577)
   │  0xe3 prefix → IPFS, remaining bytes → CID
   ▼
bafybei...          (the CID)
   │
   ▼
IPFS gateway serves the CID as a website
```

Every step is a regular EVM call. `eth_call` to the Registry, `eth_call`
to the Resolver, then local decoding. ~200-500 ms total over a healthy
RPC.

## The dweb-proxy pattern

Most IPFS gateways speak IPFS and DNSLink, not ENS. To bridge the gap,
run an HTTP service that:

1. Accepts requests for `<name>.eth.example.com`.
2. Extracts the ENS name from the Host header.
3. Does the resolution chain above via JSON-RPC.
4. Returns a 30x redirect to `<cid>.ipfs.example.com` (or serves the
   content inline).

[`dweb-proxy-api`](https://github.com/ethlimo/dweb-proxy-api) does
exactly this. It also provides a DoH endpoint (see below) so an IPFS
node can resolve `.eth` names as if they were DNSLink.

### Walk-through

```bash
# The user hits:
#   https://vitalik.eth.example.com/

# Traefik matches *.eth.example.com and routes to dweb-proxy.
# dweb-proxy:
#   1. Strips "eth.example.com" from Host → "vitalik.eth"
#   2. eth_call to ENS Registry to find vitalik.eth's resolver
#   3. eth_call to resolver for contenthash(vitalik.eth)
#   4. Decodes EIP-1577 → bafybei...
#   5. Returns:
#        HTTP/1.1 302 Found
#        Location: https://bafybei....ipfs.example.com/
#        X-Content-Location: https://bafybei....ipfs.example.com/

# Browser follows redirect. Subdomain gateway serves the CID.
```

SPIRENS's implementation: [`docs/09-dweb-proxy.md`](../docs/09-dweb-proxy.md).

## The DoH trick (DNSLink-over-ENS)

Kubo resolves `/ipns/vitalik.eth` via **DNSLink** — it looks for a TXT
record at `_dnslink.vitalik.eth`. The `.eth` zone isn't real DNS, so
normally this fails. The trick:

1. Configure Kubo to use a custom DoH resolver for the `eth.` zone:

   ```yaml
   DNS:
     Resolvers:
       "eth.": "https://ens-resolver.example.com/dns-query"
   ```

2. Point `ens-resolver.example.com` at dweb-proxy's DoH port.
3. When Kubo asks for `_dnslink.vitalik.eth` TXT, dweb-proxy does the
   ENS resolution chain and wraps the result as a synthetic DNS TXT
   response: `dnslink=/ipfs/bafybei…`.
4. Kubo sees DNSLink and resolves normally.

This lets `ipfs resolve /ipns/vitalik.eth` and `ipfs cat /ipns/vitalik.eth/...`
work without Kubo needing to understand ENS.

## Wildcard resolvers (ENSIP-10 / CCIP-Read)

A "wildcard resolver" lets a single resolver contract answer for every
subdomain of `parent.eth` — e.g. `*.vitalik.eth`. Implementations
typically use **CCIP-Read** (EIP-3668) to offload the lookup to an
off-chain HTTP service the resolver contract calls out to.

Implications for gateways:

- Your RPC provider must support CCIP-Read (eRPC does; many public RPCs
  don't).
- Some resolvers return different contenthash per subname — your
  gateway must re-resolve per request, no caching across subnames.

## The browser native ENS situation

As of early 2026:

| Browser | Native ENS? |
| :------ | :---------- |
| Brave   | Yes         |
| Chrome  | No          |
| Firefox | No          |
| Safari  | No          |
| Opera   | Partial     |
| Status  | Yes (dApp)  |

For the 97% of users on non-Brave browsers, your
`*.eth.example.com` gateway is the reliable entry point.

## Resolution tuning — cache and RPC selection

ENS names that change often (CMS-backed ENS sites) need cache
invalidation. Names that never change (personal homepages) can be
cached aggressively.

dweb-proxy uses Redis for caching — default TTL a few minutes. Tune in
`.env`:

```ini
LIMO_CACHE_TTL=300
```

Selecting the right RPC matters too. Public RPCs often lack CCIP-Read
or have tight rate limits that break batch ENS resolution. A healthy
local node via eRPC is the best option; a paid vendor is the runner-up.

## Verification

```bash
# HTTP resolution via dweb-proxy.
curl -sIL https://vitalik.eth.example.com \
  | grep -E '^(HTTP|Location|X-Content-Location)'

# Expected:
#   HTTP/2 302
#   Location: https://bafybei....ipfs.example.com/
#   X-Content-Location: https://bafybei....ipfs.example.com/

# DoH resolution from a running Kubo container:
docker exec spirens-ipfs ipfs resolve /ipns/vitalik.eth
# /ipfs/bafybei....
```

## Worked example: SPIRENS

See [`docs/09-dweb-proxy.md`](../docs/09-dweb-proxy.md) for the full
flow diagrams and Redis dependency explanation. Key files:

- `config/dweb-proxy/hostname-map.json` — host-substitution map.
- `spirens encode-hostname-map` — encodes the map for the env var
  `LIMO_HOSTNAME_SUBSTITUTION_CONFIG` (auto-run by `spirens up`).
- `compose/single-host/compose.dweb-proxy.yml` — the service,
  including the dual-port setup (HTTP :8080, DoH :11000).

To add a second TLD (e.g. Solana's SNS), extend `hostname-map.json`,
add a `*.sol` DNS record, duplicate the Traefik router, restart.

## Upstream references

- [ENS developer docs](https://docs.ens.domains/)
- [EIP-1577 — contenthash field for ENS](https://eips.ethereum.org/EIPS/eip-1577)
- [ENSIP-10 — wildcard resolution](https://docs.ens.domains/ensip/10)
- [EIP-3668 — CCIP-Read](https://eips.ethereum.org/EIPS/eip-3668)
- [dweb-proxy-api](https://github.com/ethlimo/dweb-proxy-api)
- [eth.limo](https://eth.limo/) — hosted equivalent of what SPIRENS runs
