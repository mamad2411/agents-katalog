---
name: ioc-pivoting
description: "Guides pivoting one indicator (IP, domain, hash or URL) into context, history and related infrastructure using free sources such as Shodan, TLS certs, WHOIS/DNS, JARM and favicon hashes, ranked by clustering signal. Use when the user asks to find related domains or infrastructure, expand an IOC into a campaign, or map attacker infrastructure. (Single-indicator verdict: indicator-enrichment.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# IOC pivoting

Turn a single indicator into a cluster: who/what it is, when it was active, and
what else shares its infrastructure. Pivot outward, then verdict (see
`indicator-enrichment`). Sources: `load_skill security-apis`.

## First move, always

- ORKL full-text search the raw indicator:
  marq's `orkl` tool (`query`), or without marq
  `curl -s 'https://orkl.eu/api/v1/library/search?query=<ioc>'`. A hit means the
  indicator already appears in a published APT/threat report; read it for actor,
  campaign, and sibling IOCs. This is the highest-value single pivot.
- `ioc_lookup` (hash, IP or domain) covers CIRCL hashlookup, GreyNoise, OTX and
  urlscan search in one call; `rdap` and `ct_search` cover registration and
  certificates. Curl the sources below directly if your client has no marq.
- urlscan search (domain/IP/url) for historical scans, screenshots, page hashes,
  and linked domains: `q=domain:<d>` / `q=ip:<ip>` / `q=hash:<sha256>`.

## By indicator type

- **IP** → `shodan_host` (open ports, TLS certs, banners, hostnames), Shodan
  InternetDB (ports/CVEs, no key), IPinfo (ASN/org/geo). Pivot on: shared TLS
  cert serial/SHA1, JARM, favicon hash, ASN, reverse-DNS, hosting org. Stay passive:
  marq does no active probing of the IP.
- **Domain** → `subfinder` + `ct_search` (crt.sh, `%25.<domain>`) for siblings sharing the
  cert; `whois_lookup` + `dns_lookup` for registrant, NS, MX, current A/AAAA;
  `dns_lookup` to resolve. Pivot on: registrant email/org, NS set, same A record
  (shared host), cert SAN entries, registration date clustering.
- **URL** → urlscan for redirect chain + resources; extract the host and pivot as
  domain/IP.
- **Hash** → CIRCL hashlookup (known-good NSRL → likely benign), ORKL search,
  urlscan `hash:` for samples seen serving it. No detonation here.

## Infra-clustering pivots (ranked by signal)

- Shared TLS cert (SHA1/serial) or self-signed CN: strong, often same operator.
- Shared JARM / JA3S / favicon (murmur) hash: same server stack/panel.
- Same registrant email, or NS pair, or hosting on one quiet ASN: moderate.
- Co-resolution: many domains → one IP, or one domain → rotating IPs (fast-flux).
- Naming/registration-time clustering (DGA, batch-registered same day): weak
  alone, strong with another pivot.

## Durability (pyramid of pain)

Pivot toward the durable end: hash < IP < domain < TTP. A hash/IP rotates
cheaply; cert reuse, panel fingerprints, and TTPs cost the adversary more, so
note those as the trackable indicators. Hand actor/TTP work to
`actor-ttp-attribution`.

## Record

- `write_file` the pivot graph (indicator → relation → indicator + source).
- `report_finding` only confirmed malicious infra tied to the engagement, with
  the source URL/report as a reference. Don't log raw third-party verdicts as
  fact; cite them.
