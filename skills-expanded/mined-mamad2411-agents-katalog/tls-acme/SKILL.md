---
name: tls-acme
description: ACME protocol — DNS-01 vs HTTP-01 vs TLS-ALPN-01, wildcards, rate limits, the staging endpoint. Use when debugging certificate issuance, picking a challenge type, or automating TLS for a new hostname.
---

# TLS & ACME

## What You Probably Got Wrong

**You think HTTP-01 is the default, so you pick it.** HTTP-01 is the
loudest tutorial but the narrowest in practice. It requires port 80 open
to the public internet on the hostname being validated — impossible for
LAN-only services, VPN-gated admin panels, or anything behind a tunnel.
Pick the challenge that matches your reachability, not the first one you
saw.

**You think you can get a wildcard with HTTP-01.** You cannot. Wildcards
(`*.ipfs.example.com`) require **DNS-01** — no exceptions, no toggle, no
plan upgrade. This is baked into the ACME spec (RFC 8555 §8.4).

**You forget Let's Encrypt's rate limits until they bite.** Production
LE's limits include **50 certs per registered domain per week** and **5
duplicate certs per week**. If you're iterating on cert issuance and hit
either, you're locked out for up to a week. Always hammer the staging
endpoint first.

**You conflate "it renewed" with "it renewed correctly."** Certbot /
Traefik / Caddy all log renewal success. They don't all verify that the
renewed cert is what the client is actually being served — a stale file
mount, a reverse-proxy that pinned the old cert, or an orange-clouded CDN
serving its own cert will silently mask the renewal. Verify with
`openssl s_client`, not with the renewer's logs alone.

## The three ACME challenge types

| Challenge   | How it proves control                                                                             | Needs                                                 | Wildcards | Typical use                                                |
| :---------- | :------------------------------------------------------------------------------------------------ | :---------------------------------------------------- | :-------: | :--------------------------------------------------------- |
| HTTP-01     | GET over :80 at `/.well-known/acme-challenge/<token>`                                             | Port 80 reachable from ACME server on validated host  |    No     | Single hostname, public origin, port 80 open               |
| DNS-01      | TXT record at `_acme-challenge.<host>` matching a hash                                            | API access to your DNS provider                       |  **Yes**  | Wildcards, LAN-only services, CF-proxied origins           |
| TLS-ALPN-01 | TLS handshake on :443 negotiating `acme-tls/1` ALPN, presenting a self-signed cert with the token | Port 443 reachable from ACME server on validated host |    No     | Port 80 blocked but 443 open; proxies that can't share :80 |

DNS-01 is the most flexible; HTTP-01 is the most widely-documented;
TLS-ALPN-01 is the least-supported.

## When to pick which

- **"I need `*.foo.example.com`."** DNS-01. This is the only answer.
- **"My box is behind NAT / firewall / VPN."** DNS-01. No inbound
  required.
- **"I'm running behind Cloudflare proxy (orange cloud)."** DNS-01.
  TLS-ALPN-01 breaks because CF terminates TLS at the edge; HTTP-01 works
  only for the bare hostname and only if CF forwards :80.
- **"I have one public-facing web service with :80 open."** HTTP-01 is
  fine; it's the simplest to set up if you don't need wildcards.
- **"Port 80 is blocked by policy but 443 works."** TLS-ALPN-01. Caddy
  supports it natively; Traefik supports it as `tlsChallenge`.

## Rate limits — the exact numbers

The [Let's Encrypt rate-limits page](https://letsencrypt.org/docs/rate-limits/)
is the source of truth. The ones you hit most often:

- **50 certificates per registered domain per week.** "Registered domain"
  means the eTLD+1 (`example.com`), not each subdomain. All your
  `*.example.com` certs share this bucket.
- **5 duplicate certificates per week.** A "duplicate" is the same set
  of hostnames (in any order). Re-issuing an unchanged cert burns this.
- **300 new orders per account per 3 hours.**
- **5 failed validations per account, per hostname, per hour.** This is
  the one that bites during misconfiguration — each failed DNS-01 or
  HTTP-01 counts.

### Don't test against production

Always iterate against
[LE staging](https://letsencrypt.org/docs/staging-environment/). Staging
has ~10× higher limits and issues certs from "Fake LE Intermediate" —
not publicly trusted, which is the point. When you're confident, switch
to prod.

In Traefik:

```yaml
certificatesResolvers:
  le-staging:
    acme:
      caServer: https://acme-staging-v02.api.letsencrypt.org/directory
      # ...
  le:
    acme:
      caServer: https://acme-v02.api.letsencrypt.org/directory
      # ...
```

Keep both resolvers defined; swap `certresolver=le-staging` ↔
`certresolver=le` on your router to flip.

## Verifying what's actually served

Renewer logs can lie. The wire cannot.

```bash
# Show the cert chain the server returns right now.
openssl s_client -connect rpc.example.com:443 -servername rpc.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates

# Check wildcard coverage specifically.
openssl s_client -connect foo.eth.example.com:443 -servername foo.eth.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -ext subjectAltName
```

For a production LE cert you want to see:

- `issuer= /C=US/O=Let's Encrypt/CN=R10` (or R11/E5/E6 — the active
  intermediates rotate).
- `subject=CN=<your-host>` and SANs covering what you requested.
- `notAfter` ≥ 30 days out. LE issues 90-day certs; if you're inside
  the 30-day renewal window and it hasn't rolled, something's stuck.

For a staging cert you'll see `CN=(STAGING) ...` and browsers will
reject the chain. That's correct.

## The "why isn't it issuing" checklist

When ACME is stuck, the cause is almost always one of five things:

1. **Rate limit.** Check the CA's response in the renewer logs for
   `too many certificates` or `too many failed authorizations`. Switch
   to staging until you've debugged.
2. **CAA record blocking issuance.** If the domain has a CAA record not
   listing `letsencrypt.org` (or your CA), LE will refuse.
   `dig +short CAA example.com` — empty is fine; a restrictive record
   needs updating.
3. **DNS propagation for DNS-01.** The challenge TXT has to be
   resolvable from LE's validation servers. If your DNS provider is
   slow, the challenge times out. Increase the provider's propagation
   check wait, or switch providers.
4. **Reachability for HTTP-01 / TLS-ALPN-01.** The ACME server has to
   reach your origin on :80 or :443 respectively, from the public
   internet, on the exact hostname being validated. A CDN in front, an
   IP allowlist, or a firewall rule all break this.
5. **Wrong challenge for the cert.** Wildcards need DNS-01. Internal
   hostnames need DNS-01 (HTTP-01/TLS-ALPN-01 can't reach them).

## Worked example: SPIRENS (Traefik + Cloudflare DNS-01)

SPIRENS uses DNS-01 with Cloudflare because it needs wildcards
(`*.eth.example.com`, `*.ipfs.example.com`, `*.ipns.example.com`) and
works regardless of whether records are CF-proxied. See:

- [`docs/03-certificates.md`](../docs/03-certificates.md) — walkthrough
  with cert-issuance log snippets.
- [`docs/02-dns-and-cloudflare.md`](../docs/02-dns-and-cloudflare.md) —
  required CF API token scopes (`Zone.DNS:Edit`, `Zone:Read`).
- `compose/single-host/compose.traefik.yml` — the `le` resolver
  declaration with `dnschallenge.provider=cloudflare`, as CLI flags.

The exact token scopes matter: Traefik only needs `Zone.DNS:Edit` and
`Zone:Read`. Anything broader is over-privileged.

## Upstream references

- [RFC 8555 — Automatic Certificate Management Environment](https://datatracker.ietf.org/doc/html/rfc8555)
- [Let's Encrypt rate limits](https://letsencrypt.org/docs/rate-limits/)
- [Let's Encrypt staging environment](https://letsencrypt.org/docs/staging-environment/)
- [Let's Encrypt chain of trust](https://letsencrypt.org/certificates/)
- [lego DNS provider list](https://go-acme.github.io/lego/dns/) — the
  170+ providers Traefik/lego can drive DNS-01 through.
