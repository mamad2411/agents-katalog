---
name: recon-dns
description: DNS reconnaissance for authorized domains — passive-first record enumeration (A, AAAA, MX, TXT, NS, SOA, CNAME, SRV, CAA, DNSKEY, DS, RRSIG, PTR), SPF/DKIM/DMARC email security review, DNSSEC validation, zone-transfer attempt with explicit scope permission, and subdomain brute-force with rate-limited wordlists. Active queries require authorization and scope validation; passive resolution via public resolvers is safe by default but still logged.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [dns-notes, command-log, redacted-evidence, finding-draft]
---

# DNS reconnaissance — record and configuration review

Use this skill to enumerate DNS records, assess email security controls (SPF, DKIM, DMARC), validate DNSSEC deployment, and review zone hygiene for authorized domains. Prefer passive record collection — zone exports from the client, passive DNS databases, and public resolver queries are low-impact. Active zone-transfer attempts and subdomain brute-force require separate explicit permission within the scope. Never perform cache poisoning, amplification attacks, or DNS rebinding — these are destructive/aggressive methods blocked by default.

## Required inputs

- Written scope naming authorized domains, nameservers, allowed query types (A, AAAA, MX, TXT, NS, SOA, CNAME, SRV, CAA, DNSKEY, DS, RRSIG, PTR), rate limits, and testing window.
- Explicit permission for zone transfer (AXFR) attempts — this is a high-noise, easily detected activity that must be separately authorized in the scope.
- Explicit permission for subdomain brute-force — aggressive query volume requires scope approval and rate-limit agreement.
- Valid authorization cache for every domain and nameserver queried.
- List of out-of-scope domains, nameservers, and IP ranges.
- Disabled-default approval before any DNS tunneling, cache poisoning, amplification, or rebinding work — these are policy-only unless explicitly unlocked.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load authorized domains, nameservers, query types, zone-transfer permission, and brute-force wordlist scope.
3. `pentest_agent_validate_target` for every domain and nameserver before querying.
4. `pentest_agent_check_authorization` before any active query. Passive resolution through public resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) counts as active — you are sending packets that reach the authoritative nameserver path.
5. `pentest_agent_build_command` for dry-run argv preview of dig, dnsx, massdns commands.
6. `pentest_agent_execute_tool` for all query execution — rate-limit enforcement, bounded output.
7. `pentest_agent_append_evidence` with record data, source, and confidence.

## Workflow

### Phase 1 — basic record enumeration

Collect all standard DNS record types for the target domain. Use public resolvers unless the client provides an internal resolver for internal DNS review.

1. Record-by-record collection with `dig`:
   - **A (IPv4)**: `dig +short TARGET.COM A`
   - **AAAA (IPv6)**: `dig +short TARGET.COM AAAA`
   - **MX (mail servers)**: `dig +short TARGET.COM MX` — mail servers with priority. Lower priority = preferred. Flag: multiple MX records with different providers (split mail routing).
   - **NS (nameservers)**: `dig +short TARGET.COM NS` — authoritative nameservers. Flag: all nameservers in the same IP range (single point of failure), nameservers from different providers (unusual), and nameservers whose domains differ from the target.
   - **SOA (start of authority)**: `dig +short TARGET.COM SOA` — primary nameserver, admin email (with `.` replacing `@`), serial number (YYYYMMDDNN format common, incrementing indicates zone updates), refresh/retry/expire/minimum TTLs.
   - **CNAME (canonical name)**: `dig +short www.TARGET.COM CNAME` — aliases. Flag: CNAME to cloud services (CloudFront, Azure CDN, GitHub Pages, Heroku, Netlify — potential subdomain takeover candidates).
   - **TXT**: `dig +short TARGET.COM TXT` — text records. Includes SPF records (`v=spf1`), domain verification tokens (Google, Microsoft 365, AWS), and other arbitrary text.
   - **SRV (service)**: `dig +short _sip._tcp.TARGET.COM SRV`, `dig +short _ldap._tcp.TARGET.COM SRV` — service-specific records. Flag: exposed internal services (LDAP, SIP, XMPP).
   - **CAA (certificate authority authorization)**: `dig +short TARGET.COM CAA` — restricts which CAs can issue certificates. Flag: missing CAA record (any CA can issue), overly permissive CAA (allows multiple CAs), or CAA pointing to a deprecated CA.
   - **PTR (reverse DNS)**: `dig +short -x <IP_ADDRESS>` — maps IP to hostname. Use for IPs discovered from A/AAAA records.
2. DNSSEC validation:
   - `dig +short TARGET.COM DNSKEY` — public keys for DNSSEC validation.
   - `dig +short TARGET.COM DS` — delegation signer record (links child zone to parent).
   - `dig +short TARGET.COM RRSIG` — signatures for DNSSEC-signed records.
   - `dig +dnssec TARGET.COM A` — includes RRSIG in response.
   - Flag: DNSSEC not deployed (no DNSKEY/DS/RRSIG records), DNSSEC deployed but with weak algorithms (RSA/SHA-1, algorithm 5 or 7), or DNSSEC misconfigured (signatures expired, invalid chain of trust).
3. Record aggregate data: all IPs for A/AAAA, all mail servers, all nameservers, TXT record inventory.

### Phase 2 — email security assessment (SPF, DKIM, DMARC)

Evaluate the domain's email security posture to detect spoofability and phishing risk.

1. SPF (Sender Policy Framework):
   - `dig +short TARGET.COM TXT | grep "v=spf1"`
   - Parse the SPF record:
     - `include:<domain>` — delegates to another domain's SPF. Flag: `include` chains longer than 3 levels (SPF lookup limit is 10 total; deep chains risk exceeding this).
     - `ip4:<cidr>` / `ip6:<cidr>` — authorized IP ranges. Flag: overly broad ranges like `/16` or `/8`.
     - `~all` (softfail) — spoofed email is accepted but marked. Weak posture.
     - `-all` (hardfail) — spoofed email is rejected. Strong posture.
     - `+all` — ALL email is authorized (anyone can spoof). CRITICAL finding — this is a misconfiguration.
     - `?all` (neutral) — no policy. Spoofing is not prevented.
   - Flag: no SPF record at all (domain is fully spoofable).
2. DKIM (DomainKeys Identified Mail):
   - Common selector names: `default`, `google`, `selector1`, `selector2`, `mail`, `dkim`, `<year><month>`.
   - `dig +short <selector>._domainkey.TARGET.COM TXT`
   - If no selectors are known, this is harder to enumerate. Use the `default` and `google` selectors as common probes.
   - Flag: DKIM key length < 1024 bits (weak — factorable), DKIM testing mode (`t=y`), or no DKIM at all.
3. DMARC (Domain-based Message Authentication, Reporting, and Conformance):
   - `dig +short _dmarc.TARGET.COM TXT`
   - Parse DMARC:
     - `p=none` — monitoring only, no enforcement. Weak initial posture.
     - `p=quarantine` — suspicious emails go to spam.
     - `p=reject` — spoofed emails are rejected. Strong posture.
     - `pct=<N>` — percentage of emails the policy applies to. Flag: `pct=0` effectively disables DMARC.
     - `rua=mailto:<address>` — aggregate reports sent here. Flag: external reporting address may leak internal email addresses.
     - `sp=none` — subdomain policy. If the main domain is protected but subdomains are not, spoofing from `subdomain.TARGET.COM` bypasses DMARC.
   - Flag: no DMARC record (SPF/DKIM results are not enforced — spoofing possible), `p=none` (no enforcement), DMARC for root domain but no subdomain policy.
4. Email security summary: spoofability assessment (can an attacker send email appearing to come from the target domain?), recommended SPF/DKIM/DMARC hardening steps.

### Phase 3 — zone transfer attempt (AXFR)

Attempt a DNS zone transfer ONLY if scope explicitly authorizes AXFR. Zone transfer is a high-noise, easily detected activity. It requests a complete copy of the domain's DNS zone from the authoritative nameserver.

1. Identify authoritative nameservers (from Phase 1 NS records).
2. For each nameserver:
   - `dig @NS1.TARGET.COM TARGET.COM AXFR`
   - `dig @NS2.TARGET.COM TARGET.COM AXFR`
3. If AXFR succeeds: the nameserver returns ALL DNS records for the zone — every subdomain, every internal IP, every service record. This is a CRITICAL information-disclosure finding. Stop further DNS enumeration for this domain — you have the complete zone. Record the finding and all discovered records (redacted as needed).
4. If AXFR fails ("Transfer failed", "REFUSED", or connection timeout): this is the expected and correct behavior. Most properly configured nameservers restrict zone transfers to authorized secondaries only. Record the attempt and result.
5. Attempt incremental zone transfer (IXFR) with the same command — some servers allow IXFR but block AXFR. `dig @NS1.TARGET.COM TARGET.COM IXFR=<serial>`
6. Do NOT retry failed AXFR attempts more than twice per nameserver. Repeated attempts look like an attack and may trigger monitoring alerts.

### Phase 4 — subdomain brute-force (scope-permitted only)

Attempt to discover additional subdomains through dictionary-based DNS resolution. This requires explicit scope permission — it is volume-intensive and easily detected.

1. Wordlist selection:
   - Use a targeted wordlist, not a massive generic list. Start with the top 5,000 subdomain names (SecLists: `subdomains-top1million-5000.txt`).
   - Use a curated list of common service names: `www`, `mail`, `ftp`, `admin`, `dev`, `staging`, `test`, `api`, `vpn`, `remote`, `portal`, `blog`, `shop`, `cdn`, `static`, `assets`, `media`, `files`, `docs`, `wiki`, `jira`, `git`, `jenkins`, `grafana`, `kibana`, `monitor`, `status`, `help`, `support`, `auth`, `sso`, `login`, `secure`, `m`, `mobile`, `app`, `dashboard`.
2. Resolution with dnsx:
   - `dnsx -d TARGET.COM -w <wordlist> -a -resp -silent -o bruteforce_subs.txt`
   - `-a`: include A records. `-resp`: include the resolver response IP. `-silent`: output only found subdomains.
   - Limit rate: `-t 50` (50 concurrent queries max) unless scope specifies a higher limit.
3. Handle wildcard DNS:
   - Check for wildcard DNS first: `dig +short RANDOMSTRING12345.TARGET.COM A`. If this returns an IP, the domain has wildcard DNS — all non-existent subdomains resolve to the same IP. In this case, brute-force results are unreliable (every subdomain will appear to exist). Stop brute-force and document the wildcard.
   - If wildcard is present, filter brute-force results by checking if the resolved IP is the wildcard IP. Only subdomains resolving to a different IP are real.
4. Resolution with massdns (higher throughput, requires more coordination):
   - `massdns -r /path/to/resolvers.txt -t A -o S -w massdns_results.txt <wordlist_file>`
   - Use a list of public recursive resolvers (available from public-dns.info or similar). Distribute queries across resolvers to avoid rate-limiting any single resolver.
5. Record: wordlist used, query count, found subdomain count, wildcard status, IPs discovered. Hand off discovered subdomains to live-service detection.

### Phase 5 — CNAME chain analysis and takeover detection

Analyze CNAME records for potential subdomain takeover vulnerabilities.

1. For each discovered subdomain (from Phase 1 and Phase 4), check the CNAME chain:
   - `dig +short <subdomain>.TARGET.COM CNAME`
   - If the CNAME points to a cloud service that allows unclaimed resources (GitHub Pages, Heroku, Azure Websites, AWS S3 static hosting, Netlify, Surge.sh, Shopify, etc.) and the service endpoint returns a 404 or "not found" error, the subdomain is vulnerable to takeover.
2. Common takeover-vulnerable services and detection signals:
   - **GitHub Pages**: CNAME to `<user>.github.io`. Check: `curl -s "https://<user>.github.io"` returns 404 "There isn't a GitHub Pages site here."
   - **Heroku**: CNAME to `<app>.herokuapp.com`. Check: `curl -s "https://<app>.herokuapp.com"` returns "No such app."
   - **AWS S3**: CNAME to `<bucket>.s3.amazonaws.com`. Bucket existence already checked in `recon-cloud-assets`. If bucket returns NoSuchBucket, the subdomain is take-overable.
   - **Azure**: CNAME to `<site>.azurewebsites.net` or `<site>.cloudapp.net`. Check: HTTP request returns 404 with Azure-specific error page.
   - **Netlify**: CNAME to `<site>.netlify.app`. Check for Netlify "site not found" page.
   - **Surge.sh**: CNAME to `<site>.surge.sh`. Check for Surge "project not found" page.
   - **Fastly/CloudFront**: CNAME to `*.fastly.net` or `*.cloudfront.net`. These are harder to verify without actually claiming the resource (do NOT attempt to claim).
3. For each confirmed takeover candidate:
   - Record: subdomain, CNAME target, service provider, detection method, and HTTP response evidence.
   - Flag as HIGH finding — subdomain takeover enables serving arbitrary content under the target's domain, including phishing pages, credential harvesting, and cookie theft.
   - Do NOT claim or register the unclaimed resource. This is a scope boundary — claiming a resource modifies third-party state and may constitute unauthorized access.

## Decision points

- **AXFR succeeds**: stop DNS enumeration. You have the complete zone — no need for brute-force or further record collection. CRITICAL finding.
- **Wildcard DNS detected**: stop brute-force. All results are unreliable. Cross-reference with certificate transparency logs for subdomain discovery instead.
- **SPF record with `+all`**: CRITICAL finding. Domain is fully spoofable. Document immediately.
- **CNAME to unclaimed cloud resource**: HIGH finding. Document with exact service and detection evidence. Do NOT claim the resource.
- **DNSSEC missing or misconfigured**: the domain's DNS responses are not cryptographically verified. Cache poisoning is possible (though difficult in practice). Flag as MEDIUM finding.
- **DMARC `p=none`**: the domain has SPF/DKIM set up but does not enforce results. Spoofing is still possible. Flag as MEDIUM finding — recommend moving to `p=reject`.

## Prohibited behavior

- Zone transfer (AXFR/IXFR) without explicit scope permission.
- Subdomain brute-force without explicit scope permission.
- DNS cache poisoning, amplification, tunneling, or rebinding — these are destructive/aggressive methods blocked by default.
- DNS reflection or DDoS techniques using the target's nameservers.
- Claiming or registering unclaimed cloud resources identified during takeover detection.
- Querying internal nameservers or non-public DNS infrastructure without authorization.
- Using DNS data to map internal network topology beyond what the scope authorizes.

## Stop conditions

- AXFR is refused by all nameservers → stop AXFR attempts. Document refusal as expected behavior.
- Wildcard DNS confirmed → stop brute-force. Use passive discovery methods (CT logs, search engines) for subdomain discovery.
- Rate-limited by target nameservers (SERVFAIL, dropped queries) → stop, reduce query rate, document rate-limit threshold.
- DNS queries resolve to IPs clearly outside the engagement scope → stop querying that domain tree, flag the out-of-scope boundary.

## Evidence

For each domain analyzed, record: all DNS records organized by type, nameserver inventory, email security summary (SPF/DKIM/DMARC posture, spoofability), DNSSEC status, zone-transfer attempt results, brute-force results (wordlist used, query count, hit count), and CNAME/takeover findings. Evidence template:

```text
DNS recon for: TARGET.COM

A/AAAA: 203.0.113.10, 203.0.113.11 (round-robin), 2001:db8::10
MX: 10 mail1.TARGET.COM (203.0.113.20), 20 mail2.TARGET.COM (203.0.113.21)
NS: ns1.TARGET.COM, ns2.TARGET.COM (both in 203.0.113.0/24 — single point of failure)
TXT: "v=spf1 ip4:203.0.113.0/24 include:_spf.google.com ~all" (softfail — weak)

Email security:
  SPF: ~all (softfail) — spoofed email goes to spam, not rejected.
  DKIM: default._domainkey found — 2048-bit RSA key. Strong.
  DMARC: v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@TARGET.COM — strong enforcement.
  Spoofability: LOW — DMARC reject with DKIM signing. SPF alone would allow spoofing but DMARC enforces.

DNSSEC: Deployed — algorithm 13 (ECDSA P-256 SHA-256), signatures valid.

Zone transfer (AXFR):
  ns1.TARGET.COM: REFUSED (correct)
  ns2.TARGET.COM: REFUSED (correct)

Brute-force (permitted, 5,000-word list, dnsx, 50 concurrent):
  Queries: 5,000. Found: 34 new subdomains. Wildcard: none.
  Notable: admin.TARGET.COM (203.0.113.50 — internal IP, exposed), dev.TARGET.COM (203.0.113.51)

CNAME analysis:
  blog.TARGET.COM → CNAME → TARGET.github.io → 404 "not found"
  → [HIGH] GitHub Pages subdomain takeover candidate.

Findings:
  [HIGH] GitHub Pages takeover candidate: blog.TARGET.COM → TARGET.github.io (404)
  [MEDIUM] SPF softfail (~all) — weaker posture than recommended -all hardfail.
  [INFO] NS servers share IP range — single-facility failure risk.
  [INFO] admin.TARGET.COM exposes internal IP (203.0.113.50) — not publicly routable.
```

Redact internal naming conventions, IP addresses beyond what the scope permits sharing, and any PII in TXT records or WHOIS-correlated data.

## Report handoff

1. `pentest_agent_record_finding` for: zone transfer success, subdomain takeover candidates, SPF `+all` or missing DMARC (full spoofability), missing DNSSEC, exposed internal IPs, and wildcard DNS misconfiguration.
2. Package findings with: domain, record type, record value, assessment, and remediation recommendation.
3. Recommend: harden SPF to `-all`, deploy DMARC with `p=reject` (after monitoring with `p=none` to validate), implement DNSSEC with modern algorithms (ECDSA P-256 or Ed25519), restrict zone transfers to authorized secondaries only, decommission dangling CNAME records, and separate nameserver IP ranges across facilities.
4. Explicitly note: all DNS queries were rate-limited per engagement scope, no AXFR was attempted without scope permission, no cache poisoning or amplification was performed, and all discovered records are from authorized domains only.
