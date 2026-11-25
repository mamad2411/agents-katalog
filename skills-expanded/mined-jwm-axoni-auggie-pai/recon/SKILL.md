---
name: recon
description: Technical reconnaissance of network infrastructure including domains, IPs, netblocks, and ASNs. Passive and authorized active techniques. USE WHEN recon, reconnaissance, find subdomains, DNS recon, WHOIS, IP lookup, scan, enumerate, ASN investigation, map infrastructure, passive recon.
---

# Infrastructure and Network Reconnaissance

Skill for technical reconnaissance of network infrastructure including domains, IP addresses,
netblocks, and ASNs. Combines passive intelligence gathering with authorized active techniques
to map attack surfaces and identify assets.

## When to Use This Skill

Activate when the user requests:
- "do recon on [target]", "run recon", "perform reconnaissance"
- "find subdomains", "enumerate subdomains", "DNS recon"
- "WHOIS [target]", "IP lookup", "investigate [IP/domain]"
- "scan [CIDR range]", "enumerate netblock", "ASN investigation"
- "passive recon", "active recon", "map infrastructure"
- Any request involving DNS, WHOIS, ASN, CIDR, or network mapping

## Authorization and Ethical Requirements

**CRITICAL -- Read before any action.**

**Default behavior is PASSIVE ONLY.** Always confirm before using active techniques.

### Authorization Rules

1. **Authorization first** -- never perform active scanning without explicit user confirmation
2. **Scope validation** -- ensure targets are in-scope for testing
3. **Rate limiting** -- respectful scanning, no aggressive or DoS-like behavior
4. **Documentation** -- log all recon activities with timestamps and authorization notes
5. **Responsible disclosure** -- if vulnerabilities are found, follow responsible disclosure
6. **No destructive testing** -- reconnaissance only, no exploitation

### Authorization Types

- Pentest engagement (written SOW/contract)
- Bug bounty program (in-scope targets only)
- Owned assets (your own infrastructure)
- Research lab/CTF environments

### Never Scan

- Systems without permission
- Out-of-scope targets
- Critical infrastructure (without specific authorization)
- Government systems (without specific authorization)

**When in doubt:** Ask for explicit confirmation and documented authorization.

## Workflow Auto-Selection

Automatically select the workflow based on input type:

| Input Pattern | Workflow |
|---|---|
| IP address (e.g., `1.2.3.4`) | IP Recon |
| Domain name (e.g., `example.com`) | Domain Recon |
| CIDR notation (e.g., `10.0.0.0/24`) | Netblock Recon |
| ASN (e.g., `AS15169`) | ASN Investigation |
| User says "passive only" | Passive-only mode (any target type) |

The user can override: "Use passive recon on 1.2.3.4" or "Run domain recon with active scanning."

## Available Tools

### System Commands (always available)

| Tool | Usage |
|---|---|
| `whois` | Domain and IP WHOIS lookups |
| `dig` | DNS queries (A, AAAA, MX, NS, TXT, CNAME, SOA, ANY) |
| `nslookup` | DNS resolution and reverse lookups |
| `curl` | HTTP requests, API calls, certificate inspection |
| `host` | Simple DNS lookups and reverse DNS |

### Auggie Built-in Tools

| Tool | Usage |
|---|---|
| WebFetch | Fetch and parse web content (crt.sh, BGP APIs, etc.) |
| WebSearch | Search for OSINT, documentation, public records |
| claude-browser MCP | Browser-based inspection of web properties |

### Example Commands

```bash
# WHOIS lookup
whois example.com
whois 1.2.3.4

# DNS enumeration
dig example.com ANY +noall +answer
dig example.com MX +short
dig example.com TXT +short
dig example.com NS +short
dig -x 1.2.3.4  # Reverse DNS

# Certificate transparency (via WebFetch)
# Fetch: https://crt.sh/?q=example.com&output=json

# ASN lookup
whois -h whois.radb.net AS15169
dig TXT 4.3.2.1.origin.asn.cymru.com  # IP-to-ASN via DNS

# Reverse DNS
host 1.2.3.4
nslookup 1.2.3.4

# SSL certificate inspection
curl -vI https://example.com 2>&1 | grep -A 10 "Server certificate"
```

## Passive Reconnaissance (No Authorization Required)

These techniques query only public data sources:

### 1. WHOIS Lookups
- Domain registration: registrar, dates, nameservers, contacts
- IP WHOIS: netblock owner, abuse contact, allocation

### 2. DNS Enumeration
- Record types: A, AAAA, MX, NS, TXT, CNAME, SOA, SRV, CAA
- Mail security: SPF (TXT), DMARC (_dmarc.domain TXT), DKIM
- Nameserver delegation chain

### 3. Certificate Transparency
- Use WebFetch to query `https://crt.sh/?q=%25.example.com&output=json`
- Extract subdomains from certificate Subject Alternative Names
- Review certificate history and issuers

### 4. Reverse DNS
- PTR record lookups for IP addresses
- Identify hostnames associated with IPs

### 5. ASN and BGP Data
- IP-to-ASN mapping via Team Cymru DNS or WHOIS
- ASN-to-prefixes mapping via RADB or BGP tools
- Organization and peer information

### 6. Public Database Searches
- Use WebSearch for historical DNS, public breach data, paste sites
- Check Shodan/Censys results via WebSearch (no direct API required)

## Active Reconnaissance (Requires Explicit Authorization)

**STOP -- Confirm authorization before proceeding with any active technique.**

### Port Scanning Concepts
- Active techniques involve sending packets directly to target systems
- For authorized targets, use system tools like `curl` to probe specific ports
- Example: `curl -s --connect-timeout 3 http://target:8080` to check if a service responds
- Document all active probing with timestamps

### Service Detection
- Banner grabbing via `curl` or direct TCP connections
- HTTP header inspection: `curl -sI https://target.com`
- Technology fingerprinting from response headers and content
- SSL/TLS configuration analysis: `curl -vI https://target.com 2>&1`

## Workflow Details

### IP Recon Workflow

1. Reverse DNS lookup (`dig -x`, `host`)
2. WHOIS on IP (netblock, owner, abuse contact)
3. IP-to-ASN mapping (Team Cymru DNS)
4. Certificate transparency search for the IP
5. (If authorized) HTTP/HTTPS probe, banner grab
6. Compile IP reconnaissance report

### Domain Recon Workflow

1. WHOIS domain registration data
2. Full DNS enumeration (all record types)
3. Certificate transparency subdomain discovery via crt.sh
4. Mail security check (SPF, DMARC, DKIM)
5. Identify IP addresses behind domain (A/AAAA records)
6. (If authorized) HTTP probing of discovered subdomains
7. Compile domain reconnaissance report

### Netblock Recon Workflow

1. CIDR parsing and range validation
2. WHOIS netblock ownership lookup
3. ASN/organization mapping
4. Reverse DNS sweep on key addresses (first, last, common offsets)
5. (If authorized) Selective probing of live hosts
6. Compile netblock report

### ASN Investigation Workflow

1. ASN WHOIS lookup (organization, contact)
2. Enumerate all prefixes announced by ASN (RADB, BGP data)
3. Geographic distribution of prefixes
4. Peer and upstream identification
5. Compile ASN mapping report

## Integration Pipeline

This skill fits into a broader security workflow:

```
OSINT (identify entities) --> Recon (map infrastructure) --> Web Assessment (test applications)
```

- OSINT identifies companies, domains, people
- Recon maps their technical infrastructure (this skill)
- Web Assessment tests discovered web applications for vulnerabilities

When called from another workflow, accept the target list and return structured recon data.

## Output Format

Structure all reports as follows:

```markdown
# [Type] Reconnaissance: [Target]

## Summary
- Target: [target identifier]
- Type: [IP / Domain / CIDR / ASN]
- Mode: [Passive / Passive + Active (Authorized)]
- Date: [timestamp]

## DNS
- [All DNS records discovered]
- Reverse DNS: [if applicable]
- Mail security: SPF [status], DMARC [status], DKIM [status]

## Network Information
- CIDR: [netblock]
- ASN: [AS number and name]
- Organization: [owner]
- Abuse Contact: [email]
- Location: [geographic info if available]

## Subdomains (if domain recon)
- [List of discovered subdomains with IPs]

## Services (Passive)
- Certificates: [count and notable findings from crt.sh]
- Public records: [any Shodan/Censys/VirusTotal findings via WebSearch]

## Services (Active -- Authorized Only)
- Open ports: [list]
- Detected services: [service names and versions]
- Technologies: [identified tech stack]

## Recommendations
- Further investigation areas
- Related assets to examine
- Security observations
- Suggested next steps (e.g., "run web assessment on api.example.com")
```

## Company Context

When performing recon in the context of your company's work:
- Use claude-browser MCP to check internal documentation if available
- Cross-reference discovered assets with your company's asset inventory
- Consider the SaaS attack surface model relevant to your platform
- Check ticketing/wiki via claude-browser for related security tickets if relevant

## Examples

### Example 1: Passive Domain Recon
```
User: "Do passive recon on example.com"
--> Run WHOIS, DNS, crt.sh, mail security checks
--> Generate domain reconnaissance report
--> All passive, no authorization needed
```

### Example 2: IP Investigation (Owned Asset)
```
User: "Investigate IP 1.2.3.4 -- I own this server"
--> Confirm authorization (user states ownership)
--> Passive: reverse DNS, WHOIS, ASN lookup
--> Active: HTTP probe, banner grab, certificate check
--> Generate IP reconnaissance report
```

### Example 3: ASN Research
```
User: "Investigate AS15169"
--> WHOIS ASN lookup
--> Enumerate all announced prefixes
--> Map organization and geography
--> Generate ASN report (fully passive)
```

---

**Remember:** Start passive, confirm authorization before going active, document everything,
and be respectful of target systems.
