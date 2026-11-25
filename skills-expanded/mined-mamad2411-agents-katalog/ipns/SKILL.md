---
name: ipns
description: IPNS — mutable pointers on IPFS, keys, publishing, republish interval, and why dnslink is usually what you actually want. Use when a user needs a stable URL pointing at rotating IPFS content, or when debugging slow/missing IPNS resolution.
---

# IPNS & dnslink

## What You Probably Got Wrong

**You think IPNS is DNS for IPFS.** It's a mutable pointer signed by a
libp2p key, published to the DHT (or pubsub). Resolving an IPNS name
means querying the DHT for the latest record signed by that key.
Publishing means re-signing and re-announcing. Nothing about this is
fast.

**You think IPNS is fast.** First-lookup IPNS resolves via DHT walk —
typically **2-30 seconds**, sometimes longer, sometimes failing. Kubo
caches resolved records, so warm lookups are instant, but every cold
client pays the DHT cost. Pubsub IPNS (opt-in) is faster but requires
both publisher and resolver to be on the pubsub network.

**You forget IPNS records have TTLs.** Records last ~24 hours on the
DHT by default. If the publisher goes offline and doesn't republish,
the record eventually evaporates. Kubo republishes on an interval —
set it shorter than the record lifetime.

**You use IPNS when dnslink would be better.** For anything where you
control a DNS domain, **dnslink is almost always the right answer** —
faster resolution, standard DNS tooling, no libp2p key management. IPNS
shines when you _don't_ control DNS (purely-onchain apps, personal
identities without a domain).

## The two options

### IPNS

```text
/ipns/k51qzi5uqu5...   # public key, base36
/ipns/12D3KooW...       # legacy PeerID form
```

- **Source of truth:** a signed record in the IPFS DHT / pubsub.
- **Update latency:** seconds to minutes.
- **Read latency:** seconds (cold), instant (warm cache).
- **Operational burden:** keep the publisher node online and
  republishing.
- **Pros:** fully onchain/p2p, no DNS dependency, works for identities
  without domains.

### dnslink

```text
# DNS TXT record at _dnslink.example.com:
"dnslink=/ipfs/bafybei..."
```

- **Source of truth:** a TXT record in DNS.
- **Update latency:** TTL of the TXT record (seconds to minutes).
- **Read latency:** normal DNS lookup — milliseconds.
- **Operational burden:** update TXT records when you want to point at
  new content.
- **Pros:** fast, cacheable, uses existing DNS tooling. Kubo resolves
  dnslink natively for `/ipns/example.com` paths.

## When to use which

- **You own a domain and want a stable URL.** dnslink. Your CI/CD
  updates the TXT record after a new build; clients get the new content
  on the next DNS cache refresh.
- **You have an onchain identity without a domain.** IPNS.
- **You have both.** dnslink for the canonical URL, IPNS as a backup
  identity, same content. Pinning services like web3.storage publish
  both.

## Using dnslink

Kubo's resolver is already dnslink-aware. A request to `/ipns/example.com`
triggers a TXT lookup at `_dnslink.example.com`:

```bash
dig +short TXT _dnslink.example.com
# "dnslink=/ipfs/bafybeiabcd..."
```

Update flow:

1. Publish new content to IPFS, get a new CID.
2. Update the TXT record to point at the new CID.
3. Wait one TTL cycle.
4. `/ipns/example.com` now resolves to the new CID.

For automation: most DNS provider APIs let you PATCH a TXT record. The
same Cloudflare token scoped `Zone.DNS:Edit` used for ACME can update
dnslink records on the same zone.

## Using IPNS

```bash
# Generate a key.
ipfs key gen --type=ed25519 --size=256 my-site

# Publish (pointing at the current CID of some content you pinned).
ipfs name publish --key=my-site /ipfs/bafybei...

# Resolve.
ipfs name resolve /ipns/k51qzi5...
```

### Republishing

Kubo republishes your own IPNS records on a schedule:

```yaml
# Kubo config
Ipns:
  RepublishPeriod: "4h" # default "4h", "0" = disabled
  RecordLifetime: "24h" # how long the record is valid
```

Set `RepublishPeriod` < `RecordLifetime` so records are always fresh
before expiry. Stop the node, stop republishing — record goes stale and
eventually disappears from DHT caches.

### Pubsub-assisted IPNS (optional)

```yaml
Ipns:
  UsePubsub: true
```

Subscribes to an IPFS pubsub topic per key. When the publisher updates,
subscribers hear about it within seconds — no DHT lookup needed. Both
sides must have pubsub enabled. Fallback to DHT if the other side
doesn't.

## IPNS over HTTP (subdomain gateway)

The IPFS gateway serves IPNS at:

```text
/ipns/<key-or-domain>/path/
k51qzi5...ipns.example.com/path/       # subdomain form
example.com.ipns.example.com/path/     # dnslink via subdomain
```

Works for dnslink too — `/ipns/example.com` on a gateway does a
TXT-record lookup and returns the resolved content. Handy for one-shot
tests.

## The resolution path you care about

For `/ipns/example.com`:

1. Kubo looks up `_dnslink.example.com` TXT.
2. Finds `dnslink=/ipfs/bafy…` → resolves to that CID.
3. Serves the CID's content.

For `/ipns/k51qzi5…`:

1. Kubo asks the DHT for a record signed by the corresponding public
   key.
2. Finds the record (with luck), verifies signature, decodes the
   pointed-at path.
3. Resolves the pointed-at path (may itself be an IPFS CID or another
   IPNS name).
4. Serves content.

Step 1 in the IPNS case is the slow one.

## Troubleshooting IPNS

- **"My IPNS name doesn't resolve from a fresh client."** Check: is
  your publisher node online? When did it last republish? `ipfs name
resolve --nocache /ipns/<key>` from your own node — if _that_ fails,
  the DHT doesn't have your record.
- **"Resolution takes 30+ seconds."** That's IPNS. Turn on pubsub if
  both sides can; move to dnslink if possible.
- **"I publish, other node doesn't see the update."** DHT provide can
  take minutes. Or the other node has a cached record that hasn't
  expired. `--nocache` forces a fresh resolve.
- **"Record lifetime too short."** Bump `Ipns.RecordLifetime`. Default
  is 24h; 48h-168h is fine for infrequently-updated content.

## Worked example: SPIRENS dweb-proxy

SPIRENS's dweb-proxy layers ENS on top of dnslink: an ENS name's
contenthash (or its dnslink fallback) resolves to a CID, which the
gateway serves. IPNS is only involved if the ENS record itself points at
an IPNS path — rare.

See [`docs/09-dweb-proxy.md`](../docs/09-dweb-proxy.md) for the
resolution chain (ENS → dnslink → IPFS) and
[`ens-resolution/SKILL.md`](../ens-resolution/SKILL.md) for the ENS
specifics.

## Upstream references

- [IPNS spec](https://specs.ipfs.tech/ipns/)
- [IPNS over pubsub](https://specs.ipfs.tech/ipns/ipns-pubsub-router/)
- [DNSLink spec](https://specs.ipfs.tech/ipns/dnslink/)
- [Kubo IPNS config](https://github.com/ipfs/kubo/blob/master/docs/config.md#ipns)
