---
name: recon-asn-whois
description: ASN, WHOIS, BGP, and network-ownership reconnaissance from public registries — IP-range discovery via ASN/BGP prefix lookups, WHOIS organization and contact pivoting, reverse WHOIS for related domains, CIDR block enumeration, IP history to find origin servers behind CDN, and passive DNS correlation. Fully passive; no direct target scanning.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [network-map, asset-notes, redacted-evidence, hypothesis-queue]
---

# ASN, WHOIS, and network ownership reconnaissance

Use this skill to map the target organization's IP address space, network infrastructure, and domain-registration footprint through public registries and BGP data sources. This is fully passive — all data comes from public WHOIS servers, BGP route collectors, regional internet registries (RIRs), and certificate transparency logs. The output is a network asset map that feeds into active port scanning and service discovery skills.

## Required inputs

- Target organization name, primary domain, or known IP address.
- Scope file with authorized IP ranges, CIDR blocks, and domain patterns.
- Rate limits for WHOIS and BGP API queries (most services allow 1-2 queries/second; RIR WHOIS servers may be slower).
- Evidence goal: IP-range inventory, ASN-to-organization mapping, WHOIS-pivoted related domains, and reverse-DNS hostname intelligence.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load authorized IP/CIDR ranges and domain patterns.
3. `pentest_agent_validate_target` for every discovered IP range before handing off to active scanning skills.
4. `pentest_agent_check_authorization` not required for passive WHOIS/BGP queries (no target contact), but required before active port scanning or service probing of discovered IP ranges.
5. `pentest_agent_append_evidence` with source attribution and confidence.

## Workflow

### Phase 1 — ASN discovery and IP-range enumeration

Map the target organization to its Autonomous System Number(s) and extract all advertised IP prefixes (CIDR blocks).

1. Resolve target domain to IP for initial lookup:
   - `TARGET_IP=$(dig +short TARGET.COM A | head -1)`
   - If the target uses a CDN (Cloudflare, Akamai, Fastly), the resolved IP is the CDN edge, not the origin. Use IP history (Phase 4) to find origin IPs.
2. ASN lookup via BGPView API:
   - `curl -s "https://api.bgpview.io/ip/$TARGET_IP" | jq '.data.prefixes[] | {prefix: .prefix, asn: .asn.asn, asn_name: .asn.name, asn_description: .asn.description}'`
   - This returns the ASN and all advertised prefixes for that IP.
3. ASN lookup via organization name:
   - `curl -s "https://api.bgpview.io/search?query_term=TARGET+ORG" | jq '.data.asns[] | {asn: .asn, name: .name, description: .description}'`
   - This finds all ASNs registered to the organization name, including subsidiaries and acquisitions.
4. Prefix enumeration for each discovered ASN:
   - `curl -s "https://api.bgpview.io/asn/AS12345/prefixes" | jq '.data.ipv4_prefixes[].prefix' -r | sort -u > asn_prefixes.txt`
   - Also query IPv6 prefixes: `jq '.data.ipv6_prefixes[].prefix' -r`
5. Regional Internet Registry (RIR) data as corroboration:
   - ARIN (North America): `whois -h whois.arin.net "a AS12345" | grep -E "CIDR|NetRange"`
   - RIPE (Europe/Middle East): `whois -h whois.ripe.net "AS12345" | grep -E "route:"`
   - APNIC (Asia-Pacific): `whois -h whois.apnic.net "AS12345" | grep -E "route:"`
6. Merge all prefix sources and deduplicate. Record: ASN, ASN name, prefix count, total IP count.

### Phase 2 — WHOIS domain intelligence

Query WHOIS for the target domain to extract registration metadata, nameservers, and administrative/technical contacts for pivoting.

1. Domain WHOIS:
   - `whois TARGET.COM | grep -iE "registrar|creation date|expir|name server|registrant|admin|tech|email|organization|address|phone"`
   - Record: registrar, creation date, expiration date, nameservers, registrant organization, administrative contact email, technical contact email.
2. Nameserver analysis:
   - Extract all nameservers from WHOIS. Are they self-hosted (`ns1.TARGET.COM`) or third-party (`ns1.cloudflare.com`, `ns1.awsdns.com`)? Third-party DNS may indicate CDN or cloud hosting.
   - Check if the nameserver domain is registered by the same organization — if not, it may be a third-party DNS provider.
3. Email contact pivoting:
   - If the registrant or admin email uses a corporate domain (`@TARGET.COM`), that's expected.
   - If the email is a free provider (`@gmail.com`, `@yahoo.com`), the registration may be intentionally obscured or the domain is owned by an individual.
4. WHOIS history (if available):
   - Services like WhoisXMLAPI or DomainTools provide historical WHOIS data. Use only if authorized and within scope.

### Phase 3 — reverse WHOIS and related-domain discovery

Pivot from the organization name, registrant email, or postal address to discover other domains registered by the same entity. This reveals shadow IT, acquisitions, brand-protection domains, and forgotten subsidiaries.

1. Reverse WHOIS by organization name:
   - Use a commercial reverse-WHOIS service (DomainTools, WhoisXMLAPI) or the free ViewDNS.info: `curl -s "https://viewdns.info/reversewhois/?q=TARGET+ORGANIZATION" | grep -oE '[a-zA-Z0-9.-]+\.[a-z]{2,}' | sort -u | grep -v "viewdns\|google\|facebook" > related_domains.txt`
   - With API key: `curl -s "https://reverse-whois-api.example.com/?org=TARGET+ORGANIZATION&apikey=KEY" | jq -r '.domains[]'`
2. Reverse WHOIS by email:
   - `curl -s "https://viewdns.info/reversewhois/?q=admin@TARGET.COM" | grep -oE '[a-zA-Z0-9.-]+\.[a-z]{2,}' | sort -u > related_domains_email.txt`
3. Certificate Transparency log pivoting for discovered domains:
   - For each related domain, query crt.sh to find subdomains: `curl -s "https://crt.sh/?q=%25.RELATED.COM&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u`
   - This rapidly expands the domain footprint without active scanning.
4. Scope-validate all discovered related domains. Flag any domain that appears to be owned by the target but is not in the original scope — these may be forgotten assets not covered by the engagement.

### Phase 4 — IP history and origin-server discovery

Find historical IP addresses for the target domain to bypass CDN/WAF and discover the true origin server, legacy infrastructure, or retired environments still accessible.

1. IP history via public APIs:
   - `curl -s "https://api.hackertarget.com/hostsearch/?q=TARGET.COM"` — returns historical IP-to-hostname mappings.
   - `curl -s "https://api.viewdns.info/iphistory/?domain=TARGET.COM&apikey=KEY" | jq '.response.dns_records[] | {ip: .ip, last_seen: .last_seen}'` (API key required).
   - SecurityTrails (API): `curl -s "https://api.securitytrails.com/v1/history/TARGET.COM/dns/a" -H "apikey: KEY" | jq '.records[] | {ip: .values[].ip, first_seen: .first_seen, last_seen: .last_seen}'`
2. DNSDB (passive DNS): if access is available, query for historical A/AAAA records for the domain. This is the most comprehensive passive DNS source.
3. Censys/Shodan for passive host discovery:
   - Shodan: `shodan search "hostname:TARGET.COM" --fields ip_str,port,hostnames,org` (requires API key, sends no packets to target).
   - Censys: `censys search "parsed.names: TARGET.COM" --fields ip,services.port,services.service_name,location.country` (requires API key).
4. Identify origin IPs:
   - Historical IPs that predate CDN adoption (first_seen before the CDN was deployed).
   - IPs that only appeared briefly (during CDN misconfiguration or maintenance).
   - IPs hosting non-HTTP services (SSH, FTP, SMTP, RDP) — these are rarely behind CDN and may be direct origin access.
5. Reverse DNS on discovered IPs:
   - For each historical IP: `dig +short -x <IP>`
   - Reverse DNS may reveal the server hostname, provider (AWS/GCP/Azure hostname patterns), or internal naming conventions.

### Phase 5 — network map and handoff

1. Build a network asset map from all sources:
   - **ASN inventory**: ASN numbers, names, total IP count per ASN.
   - **Prefix/CIDR list**: all IP ranges associated with the target organization.
   - **Domain inventory**: primary domain, related domains from reverse WHOIS, subdomains from CT logs.
   - **Origin IP candidates**: IPs that bypass CDN/WAF.
   - **Service IPs**: IPs hosting non-HTTP services (from Shodan/Censys passive data).
2. Scope-validate the network map:
   - For each CIDR range, check if it overlaps with in-scope ranges from the engagement scope file. Flag overlaps as `IN_SCOPE`. Flag non-overlapping but organization-owned ranges as `OUT_OF_SCOPE` for documentation.
   - For each IP, check if it falls within an in-scope CIDR. Flag in-scope IPs for handoff to active scanning.
3. `pentest_agent_append_evidence` with the network map, source attribution per finding, confidence levels, and handoff recommendations.

## Decision points

- **CDN hides the true origin**: if all resolved IPs belong to CDN providers (Cloudflare, Akamai, Fastly, CloudFront), the target's origin IP is hidden. Use IP history (Phase 4) and passive DNS to find pre-CDN IPs. Also check non-HTTP services (mail servers from MX records, FTP, SSH) which may bypass CDN.
- **Organization has dozens of ASNs**: large organizations (ISPs, cloud providers, multinationals) may have many ASNs from acquisitions and regional registrations. Prioritize ASNs with the most prefixes (largest IP footprint) and those directly named after the target.
- **WHOIS is privacy-protected (GDPR redacted)**: EU-based domains often have redacted WHOIS. Use RIR data, BGP advertisements, and certificate transparency logs as alternative sources for organization-to-IP mapping.
- **Reverse WHOIS returns unrelated domains**: common organization names (e.g., "Amazon", "Apple") will match unrelated entities. Cross-reference with the target's known domain patterns, brand names, and industry to filter false positives.

## Prohibited behavior

- Sending any packet directly to the target's IP addresses during this skill — this is passive collection only.
- Port scanning, service probing, or HTTP requests to discovered IPs — hand off to active recon skills after scope validation.
- Using discovered origin IPs to bypass CDN/WAF and access the origin directly without explicit scope permission for origin access.
- Abusing WHOIS or BGP APIs at high rates — stay within rate limits.
- Storing registrant email addresses or phone numbers in evidence unless they are corporate contact addresses relevant to the engagement.

## Stop conditions

- WHOIS and BGP queries return no results for the target → the organization may be small, using only cloud infrastructure, or operating anonymously. Document the limitation. Use domain-based recon (subdomain enumeration, certificate transparency) as an alternative path.
- Target IPs are entirely cloud-provider addresses (AWS, GCP, Azure) with no dedicated ASN → the target does not operate its own network infrastructure. The network map is the cloud provider's prefix. Hand off to `recon-cloud-assets` for cloud-specific discovery.
- Rate-limited by BGPView or WHOIS servers → wait for the rate-limit window, reduce query rate, continue with remaining sources.

## Evidence

Store source attribution, ASN inventory, CIDR list with scope validation, reverse-WHOIS domain list, IP history with timestamps, origin-IP candidates, and handoff recommendations. Evidence template:

```text
Network ownership recon for: TARGET.COM
Target organization: Target Corp
Primary ASN: AS12345 (Target Corp Data Center)

ASN inventory:
  AS12345: 16 IPv4 prefixes, 65,536 IPs — primary production ASN
  AS67890: 4 IPv4 prefixes, 1,024 IPs — acquired subsidiary (Target EU)

CIDR inventory (in-scope):
  203.0.113.0/24 — primary web hosting (IN_SCOPE)
  198.51.100.0/22 — corporate office range (IN_SCOPE)
  192.0.2.0/25 — acquired subsidiary (OUT_OF_SCOPE = not in engagement scope)

Related domains from reverse WHOIS:
  target.eu (Target EU subsidiary)
  targetshop.com (e-commerce — retired, redirects to target.com)
  targetdev.com (registration only, no DNS — may be available for takeover)

Origin IP candidates (from IP history, bypass CDN):
  203.0.113.10 — direct SSH access (port 22), non-CDN
  198.51.100.25 — mail server (MX), non-CDN
  198.51.100.30 — pre-CDN origin, last seen 2022-06 (CDN deployed 2022-07)

Handoff:
  In-scope CIDRs → naabu/nmap port scan (recon-web-surface)
  Origin IPs → direct service probe, priority 1
  Related domains → subdomain enumeration (recon-subdomain)
```

Redact personal email addresses, phone numbers, and street addresses from evidence. Use only corporate/organizational contact data.

## Report handoff

No direct report — the network map is the handoff artifact. Downstream skills (`recon-web-surface`, `recon-subdomain`, `recon-cloud-assets`) consume the CIDR inventory, origin IP list, and related-domain list for active probing. Ensure all handoff data is scope-validated so active skills do not probe out-of-scope infrastructure.
