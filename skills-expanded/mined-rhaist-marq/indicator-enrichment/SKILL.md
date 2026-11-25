---
name: indicator-enrichment
description: "Guides enriching and triaging a single indicator (IP, domain, hash, URL or CVE) with free no-login sources and deciding malicious vs benign vs unknown. Use when the user asks whether an IP, domain, file hash or URL is malicious, wants reputation or context for an IOC, or needs a quick verdict on an alert's indicator. (Expanding into related infrastructure: ioc-pivoting.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Indicator enrichment & triage

Given an indicator, gather context from free sources and reach a verdict:
**malicious / suspicious / benign / unknown** with the evidence behind it. For
deeper pivots use `ioc-pivoting`; for sources use
`load_skill security-apis`.

## Enrich by type (free, no-login)

- **IP** → `shodan_host` (keyless InternetDB: ports/CPEs/CVEs; full banners with
  a key), IPinfo (ASN/org/geo: cloud vs residential vs hosting). Reverse-DNS via
  HackerTarget. ORKL search for prior reporting (marq's `orkl` tool, `query`).
- `ioc_lookup` runs the hash, IP and domain lookups below (CIRCL hashlookup,
  GreyNoise, OTX, urlscan) in one call; curl them directly without marq.
- **Domain** → `ct_search` (cert age/SANs), `rdap` or `whois_lookup` (registration date; newly
  registered is suspicious), `dns_lookup` (resolves? parked? sinkholed?),
  urlscan search (screenshots, prior verdicts).
- **URL** → urlscan search for historical scans/redirects; check live status
  from your own tooling only if the client has authorized contact. Do **not** submit a client URL to a public
  scanner without authorization (opsec: see security-apis).
- **Hash** → CIRCL hashlookup: NSRL/known-good hit ⇒ very likely benign, clear it.
  ORKL + urlscan `hash:` for malicious sightings. Never detonate here.
- **CVE** (when an indicator is a vuln) → CIRCL CVE for detail/CVSS, FIRST EPSS
  for exploit-likelihood; prioritise high-EPSS over raw CVSS.

## Verdict decision rule

1. **Known-good wins early**: NSRL hashlookup hit, or major-provider/CDN IP
   (Cloudflare/Google/AWS edge) ⇒ likely benign; don't chase further. Beware
   abuse-on-shared-infra (a bad path on a CDN IP).
2. **Reported malicious**: appears in an ORKL report or urlscan malicious verdict
   ⇒ suspicious→malicious; corroborate with a second source before asserting.
3. **Freshness/anomaly signals**: domain registered days ago, cert minutes old,
   IP on a bulletproof/quiet ASN, DGA-looking name ⇒ raise suspicion.
4. **No signal ≠ benign**: absence of reporting = **unknown**, not clean.
   Especially for fresh, targeted, or low-prevalence indicators.
5. Weigh single third-party verdicts skeptically; require ≥2 independent sources
   before calling something malicious.

## Durability note (pyramid of pain)

Hash < IP < domain < TTP. A clean verdict on a hash/IP is fragile (rotates
cheaply); a behaviour/TTP verdict is durable. Triage the cheap indicators fast,
invest analysis in the durable ones.

## Output

- Per indicator, record: value, type, sources queried, key facts, verdict +
  confidence + one-line reasoning. `write_file` as a triage table.
- `report_finding` only confirmed-malicious indicators relevant to the engagement,
  citing the source URLs as references; never log a raw third-party verdict as
  established fact.
