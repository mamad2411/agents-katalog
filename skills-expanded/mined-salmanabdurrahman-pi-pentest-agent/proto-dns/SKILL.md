---
name: proto-dns
description: DNS record and resolver review for scoped infrastructure — passive-first zone enumeration, record analysis, DNSSEC/DMARC/SPF validation, and zone-transfer attempt with explicit scope approval. No cache poisoning, amplification, or rebinding attacks.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# DNS assessment — safe record and configuration review

Use this skill to review DNS records, resolver exposure, email security controls (SPF/DKIM/DMARC), DNSSEC validation, and zone hygiene for authorized domains. Prefer passive record collection and user-provided zone exports. Active queries must be rate-limited and limited to in-scope names. Never attempt cache poisoning, amplification attacks, or DNS rebinding — these are destructive/aggressive methods blocked by default.

## Required inputs

- Written scope naming authorized domains, nameservers, allowed query types (A, AAAA, MX, TXT, NS, SOA, CNAME, SRV, CAA, DNSKEY, DS, RRSIG, PTR), rate limits, and testing window.
- Explicit permission for zone transfer attempts (AXFR) — this is a separate scope approval, not implied by general DNS enumeration.
- Valid authorization cache for each domain and nameserver.
- List of out-of-scope domains, nameservers, and IP ranges. Subdomain brute-force wordlists must be scoped to authorized domains only.
- Separate disabled-default approval before any DNS tunneling, cache poisoning, amplification testing, or rebinding work — these are policy-only unless explicitly unlocked.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each domain and nameserver.
3. `pentest_agent_check_authorization` before any active query.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (dig, dnsx, massdns) are used.
5. `pentest_agent_execute_tool` for all execution — rate-limit, throttle, and output-policy enforcement.
6. `pentest_agent_append_evidence` for all query results.

## Workflow

### Phase 1 — passive record inventory

Start with passive data sources — no direct target contact:

1. Query public DNS databases (SecurityTrails, crt.sh certificate transparency logs, DNSDumpster, Shodan DNS data) for known records of the authorized domain.
2. Collect: A, AAAA, MX, TXT, NS, SOA, CNAME, SRV records from passive sources.
3. Check certificate transparency logs for subdomain discovery (crt.sh: `%.example.com`).
4. Build a preliminary record inventory. Flag records that appear stale (pointing to decommissioned IPs, expired services) or misconfigured (CNAME to non-existent domains, MX pointing to obsolete mail servers).
5. If the operator provides a zone export file, parse it directly — no active queries needed for this data.

### Phase 2 — safe active record enumeration

For each authorized domain, query in-scope nameservers directly:

1. Use `dig` or `dnsx` through `pentest_agent_execute_tool`:
   - `A` record: `dig +short example.com A`
   - `AAAA` record: `dig +short example.com AAAA`
   - `MX` record: `dig +short example.com MX`
   - `TXT` record: `dig +short example.com TXT` (may contain SPF/DKIM verification strings)
   - `NS` record: `dig +short example.com NS`
   - `SOA` record: `dig +short example.com SOA`
   - `CNAME` for common subdomains: `www`, `mail`, `api`, `admin`, `dev`, `staging`
   - `SRV` records for service discovery: `_ldap._tcp`, `_kerberos._udp`, `_sip._tcp`, `_xmpp._tcp`
   - `CAA` record: `dig +short example.com CAA` (certificate authority authorization)
   - `PTR` record for in-scope IP ranges: `dig +short -x <IP>`
2. Rate-limit queries: maximum 5 queries per second per nameserver. Use `+timeout=3` and `+tries=1`.
3. Record: query timestamp, nameserver queried, query type, response (redacted if it contains internal hostnames not in scope), response time, and any errors (NXDOMAIN, SERVFAIL, REFUSED, timeout).
4. If a nameserver returns SERVFAIL or REFUSED for standard queries, note the restriction — do not probe further without explicit scope approval.
5. Do not query out-of-scope nameservers. If the domain's NS records point to out-of-scope servers, record the nameserver list but do not contact them.

### Phase 3 — email security control review

DNS-based email security controls protect against spoofing and phishing:

1. **SPF**: Parse the domain's TXT records for `v=spf1`. Validate:
   - SPF record syntax (valid mechanisms: `mx`, `a`, `include`, `ip4`, `ip6`, `all`).
   - Termination qualifier: `-all` (hard fail, strict) is strongest. `~all` (soft fail) is weaker. `?all` (neutral) or `+all` (allow all) is a critical finding.
   - Lookup count: SPF limited to 10 DNS lookups. Exceeding causes `PermError` — SPF record is invalid.
   - Includes: check that included domain SPF records exist and are not overly permissive.
2. **DKIM**: Check for `selector._domainkey.example.com` TXT records. Common selectors: `default`, `google`, `selector1`, `selector2`, `dkim`, `mail`. Validate:
   - Key type (`k=rsa`), key length (at least 1024-bit, 2048-bit preferred).
   - Testing mode (`t=y` or `t=s`) — if set, DKIM failures are not enforced.
3. **DMARC**: Query `_dmarc.example.com` TXT record. Validate:
   - Policy: `p=reject` (strictest), `p=quarantine`, `p=none` (monitoring only — weak).
   - Subdomain policy: `sp=reject` (applies to subdomains).
   - Reporting: `rua` (aggregate reports), `ruf` (forensic reports — contains email content, should be carefully scoped).
   - Alignment: `adkim=s` (strict) or `adkim=r` (relaxed). `aspf=s` or `aspf=r`.
   - Percentage: `pct=100` applies policy to all messages. `pct<100` means partial enforcement.
4. **MTA-STS**: Query `_mta-sts.example.com` TXT record. Check for `v=STSv1` and `id=` value.
5. **BIMI**: Query `default._bimi.example.com` TXT record for brand indicator support.
6. **DNSSEC**: Query for `DNSKEY` and `DS` records. Validate with `dig +dnssec +multi`. Check for `ad` (authenticated data) flag in response. Missing DNSSEC is a medium finding for domains handling sensitive data.
7. **DANE/TLSA**: For mail servers, query `_25._tcp.<mailserver>` TLSA records. Validates TLS certificates for SMTP.

### Phase 4 — zone transfer attempt (only with explicit scope approval)

Zone transfer (AXFR) can reveal all DNS records for a domain. This is a high-impact test that must be explicitly approved:

1. Confirm scope explicitly lists "zone-transfer" or "AXFR" as an allowed method.
2. For each authorized nameserver: `dig AXFR example.com @<ns>`
3. If zone transfer succeeds:
   - Record all returned records. This is a critical finding — zone transfer should be restricted to authorized secondary nameservers.
   - Do not dump or share the full zone content externally.
   - Redact any internal hostnames, IPs, or service endpoints that are not in the authorized scope.
4. If zone transfer is refused (`Transfer failed`), record the refusal as a positive security control.

### Phase 5 — subdomain enumeration (rate-limited)

Only if scope explicitly allows subdomain discovery:

1. Use a scoped wordlist (not a full Internet-scale list). Start with a small verified list (top 100-1000 subdomains from public datasets).
2. For each candidate: `dig +short <candidate>.example.com A` through `pentest_agent_execute_tool`.
3. Rate-limit: maximum 10 queries per second. Use DNS query aggregation (`massdns` with `-t A` and rate flags) only if the tool can honor scope rate limits.
4. Every discovered subdomain must be validated against scope: is it in-scope? Does it match an out-of-scope exclusion?
5. Record: candidate, resolved IP (redacted if not in scope), resolution timestamp.
6. If any discovered subdomain resolves to an out-of-scope IP or domain, stop probing that subdomain — record the observation but do not contact it further.
7. Do not brute-force with wordlists larger than 10,000 entries unless scope explicitly authorizes deep discovery.

## Decision points

- **Zone transfer success**: critical finding — immediately document, stop further AXFR attempts, alert operator.
- **SPF `+all` or missing SPF**: high finding — domain is vulnerable to email spoofing.
- **DMARC `p=none`**: medium finding — domain monitors but does not enforce anti-spoofing. Upgrade to high if domain is commonly phished.
- **DNSSEC missing on sensitive domain**: medium finding — DNS responses can be spoofed.
- **Wildcard DNS detected**: if `*.example.com` resolves to the same IP, subdomain discovery results must be validated to distinguish real subdomains from wildcard catch-all.
- **CNAME to cloud service without ownership verification**: medium finding — potential subdomain takeover (e.g., CNAME to unclaimed S3 bucket, Azure website, Heroku app, GitHub Pages).
- **Rate limit hit**: reduce query rate, respect nameserver backpressure, do not retry aggressively.

## Prohibited behavior

- DNS cache poisoning (sending forged DNS responses) — destructive, blocked by default.
- DNS amplification testing (checking for open resolvers that amplify traffic) — DoS-class method, blocked in bug-bounty/red-team modes.
- DNS rebinding (using DNS to bypass same-origin policy for SSRF) — exploitation, requires explicit approval.
- DNS tunneling (encoding data in DNS queries for C2/data exfiltration) — disabled-default.
- Brute-forcing with large wordlists without scope, rate limits, and executor approval.
- Querying out-of-scope nameservers or domains.
- Attempting zone transfer without explicit scope permission.
- Using `ANY` query type (amplification risk, often blocked).

## Stop conditions

- Nameserver returns REFUSED or blocks further queries → stop, respect the block.
- Zone transfer succeeds → stop AXFR, record finding, do not attempt on other nameservers in scope unless operator explicitly requests full audit.
- Discovered subdomain resolves to out-of-scope target → record, do not probe further.
- Evidence would include internal hostnames or IPs not in scope → redact and stop that query line.
- Rate limit exceeded → pause, wait, reduce rate.

## Evidence — DNS record matrix

For each authorized domain, record:

```text
Domain: example.com
Nameservers queried: [ns1.example.com, ns2.example.com]
Query window: <start> to <end> UTC

A records:
  example.com → 93.184.216.34 (TTL: 86400)
  www.example.com → 93.184.216.34 (TTL: 3600)

MX records:
  example.com → mail.example.com (priority: 10)
  example.com → mail2.example.com (priority: 20)

TXT records:
  SPF: v=spf1 mx -all (valid, hard fail)
  DMARC: v=DMARC1; p=reject; rua=mailto:dmarc@example.com (enforcing)

Security findings:
  [HIGH] Zone transfer succeeded on ns2.example.com — all records exposed
  [MEDIUM] DNSSEC not enabled on example.com
  [LOW] CAA record missing — no CA restriction

CNAME takeover risk:
  [none found | dev.example.com → CNAME dev.example.s3.amazonaws.com (unclaimed bucket)]
```

Aggregate into a domain security posture summary per authorized domain. Include: record inventory, email security posture (SPF/DKIM/DMARC grade), DNSSEC status, zone transfer vulnerability, subdomain takeover risks, and recommended remediation per finding class.

Never store: raw zone transfer output with internal records, unredacted subdomain lists for out-of-scope domains, or nameserver IPs if scope restricts disclosure.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed misconfiguration (missing SPF/DKIM/DMARC, missing DNSSEC, zone transfer exposure, CNAME takeover risk, wildcard DNS, stale/abandoned records).
2. Package DNS findings with the domain's overall email security grade and DNSSEC compliance status.
3. Recommend: enable DNSSEC, implement SPF/DKIM/DMARC with `reject` policy, restrict zone transfers to authorized secondary nameservers, audit CNAME records for takeover risk, implement CAA records, and monitor certificate transparency logs for unauthorized subdomains.
4. Explicitly note that no cache poisoning, amplification, rebinding, or tunneling tests were performed.
