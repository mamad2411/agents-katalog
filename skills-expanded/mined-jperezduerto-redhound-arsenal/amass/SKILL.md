---
name: amass
description: >
  Build, extend, and operate Amass — the OWASP attack surface mapping tool for subdomain enumeration,
  ASN/org discovery, and DNS intelligence. Use when performing external reconnaissance, passive or active
  subdomain enumeration, certificate transparency analysis, ASN mapping, or tracking changes in an attack surface.
  Use when the user asks about subdomain discovery, passive DNS, API key integration, graph visualization,
  Amass config files, or comparing Amass with subfinder. Covers installation, all subcommands, config,
  data sources, brute force, resolvers, and visualization.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/owasp-amass/amass
  stars: '12.8k'
---

# amass Agent Skill

## When to Use This Skill

Use this skill when:
- Enumerating subdomains for an external attack surface assessment
- Mapping ASNs and IP ranges owned by a target organization
- Performing passive DNS reconnaissance without touching the target
- Running active DNS enumeration (brute force, permutations)
- Discovering SaaS/cloud assets beyond the primary domain
- Tracking changes in an organization's external footprint over time
- Integrating with data sources (Shodan, VirusTotal, SecurityTrails) via API keys
- Visualizing the discovered graph of domains, IPs, and ASNs

## What Amass Does

Amass is the OWASP project for in-depth DNS enumeration and network mapping. It combines passive techniques (passive DNS, certificate transparency, web archives, BGP routing tables, public APIs) with active techniques (brute force, DNS zone walking, certificate SAN expansion, alterations) and stores all results in a local graph database. The graph model enables cross-session change tracking and relationship visualization across domains, IPs, CIDRs, ASNs, and organizations. Compared to subfinder, Amass is slower but deeper — subfinder is optimal for speed, Amass for completeness.

## Installation

```bash
# Go install (Go 1.21+)
go install -v github.com/owasp-amass/amass/v4/...@master
# Binary lands at: $GOPATH/bin/amass

# Snap (Linux)
sudo snap install amass

# Docker
docker pull caffix/amass
docker run --rm -v ~/.config/amass:/root/.config/amass \
  caffix/amass enum -passive -d example.com

# Homebrew (macOS)
brew install amass

# Pre-built binary
# Download from: https://github.com/owasp-amass/amass/releases
wget https://github.com/owasp-amass/amass/releases/latest/download/amass_Linux_amd64.zip
unzip amass_Linux_amd64.zip
sudo mv amass_Linux_amd64/amass /usr/local/bin/

# Verify
amass -version
```

## Subcommands Overview

| Subcommand | Purpose |
|------------|---------|
| `enum`     | Subdomain enumeration (passive + active) |
| `intel`    | Org/ASN/CIDR discovery from targets |
| `track`    | Change detection across sessions |
| `db`       | Query and manage local graph database |
| `viz`      | Generate graph visualizations |

## enum — Subdomain Enumeration

### Passive Mode (no DNS queries to target)

```bash
# Basic passive enumeration
amass enum -passive -d example.com

# Multiple domains
amass enum -passive -d example.com -d sub.example.com

# Passive + output to file
amass enum -passive -d example.com -o passive-results.txt

# With all configured API sources
amass enum -passive -d example.com -config ~/.config/amass/config.yaml -o results.txt

# JSON output
amass enum -passive -d example.com -json passive.json

# Suppress banner, timestamps
amass enum -passive -d example.com -silent -o results.txt
```

### Active Mode (queries DNS, performs brute force)

```bash
# Active enumeration (default when -passive not set)
amass enum -active -d example.com

# With brute force using built-in wordlist
amass enum -brute -d example.com

# Custom brute force wordlist
amass enum -brute -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Brute force + permutations/alterations
amass enum -brute -alts -d example.com -w /path/to/wordlist.txt

# Recursive brute force (brute force discovered subdomains)
amass enum -brute -d example.com -w wordlist.txt -max-dns-queries 50000

# Limit to specific data sources
amass enum -passive -d example.com -src CertSpotter,VirusTotal,Shodan
```

### Resolver Configuration

```bash
# Use custom resolver list (critical for speed and accuracy)
amass enum -d example.com -r 1.1.1.1,8.8.8.8,9.9.9.9

# Resolver file (one per line)
cat > resolvers.txt << 'EOF'
1.1.1.1
8.8.8.8
8.8.4.4
9.9.9.9
64.6.64.6
208.67.222.222
EOF
amass enum -d example.com -rf resolvers.txt

# Trusted resolvers (used to verify results from untrusted resolvers)
amass enum -d example.com -tr 1.1.1.1,8.8.8.8

# Validate all results against trusted resolvers
amass enum -active -d example.com -rf resolvers.txt -tr 1.1.1.1
```

### Output and Logging

```bash
# All output formats
amass enum -d example.com \
  -o subdomains.txt \        # one subdomain per line
  -json results.json \        # full JSON with source metadata
  -log amass.log             # verbose operational log

# Show data source for each finding
amass enum -passive -d example.com -show-graph

# IPv4 and IPv6 addresses
amass enum -d example.com -ipv4 -ipv6
```

## intel — Organization and ASN Discovery

```bash
# Discover ASNs by organization name
amass intel -org "Acme Corp"

# Reverse whois from known domain
amass intel -whois -d example.com

# Discover CIDRs from ASN
amass intel -asn 12345

# Expand from known IP address
amass intel -ip 93.184.216.34

# Full intel workflow: org → ASN → CIDRs → domains
amass intel -org "Target Corp" 2>&1 | grep -E "^[0-9]" | awk '{print $1}' > asns.txt
# Then expand each ASN:
while read asn; do
    amass intel -asn "$asn" -o "asn-${asn}-ranges.txt"
done < asns.txt
```

## track — Change Detection

```bash
# Compare current scan to previous (requires same database)
amass track -d example.com

# Show only new subdomains since last scan
amass track -d example.com -show new

# Show lost (no longer resolving) subdomains
amass track -d example.com -show lost

# Track with specific config (to use same API keys/resolvers)
amass track -d example.com -config ~/.config/amass/config.yaml
```

## db — Graph Database Operations

```bash
# List all tracked domains
amass db -list

# Show all subdomains for a domain
amass db -d example.com -show

# Show discovered names and associated IPs
amass db -d example.com -ip -show

# Export database for visualization
amass db -d example.com -enum 1  # specific enumeration run

# Show all names discovered from all runs
amass db -names -d example.com

# Show all associated IPs and ASNs
amass db -summary -d example.com
```

Database location: `~/.config/amass/amass.sqlite` (configurable in config.yaml)

## Configuration File

Location: `~/.config/amass/config.yaml`

```yaml
# ~/.config/amass/config.yaml

# Output directory for databases
output_directory: /home/user/.config/amass

# Minimum number of trusted resolvers that agree on result
minimum_ttl: 1440  # seconds, 24h

# Resolver settings
resolvers:
  - 1.1.1.1
  - 8.8.8.8

# Wordlist for brute force (default wordlist if not specified via -w)
bruteforce:
  enabled: true
  wordlist_file: /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
  recursive: true
  minimum_for_recursive: 1

# Alterations/permutations
alterations:
  enabled: true
  flip_words: true
  add_words: true
  edit_distance: 1

# Scope: domains to include/exclude
scope:
  domains:
    - example.com
  blacklist:
    - www.example.com  # known false positive

# API Data Sources
datasources:
  - name: Shodan
    apikey: YOUR_SHODAN_KEY
  - name: VirusTotal
    apikey: YOUR_VT_KEY
  - name: SecurityTrails
    apikey: YOUR_ST_KEY
  - name: Censys
    apikey: YOUR_CENSYS_ID
    secret: YOUR_CENSYS_SECRET
  - name: GitHub
    apikey: YOUR_GITHUB_TOKEN
  - name: PassiveTotal
    apikey: YOUR_PT_KEY
    secret: YOUR_PT_SECRET
  - name: Chaos
    apikey: YOUR_CHAOS_KEY
  - name: BinaryEdge
    apikey: YOUR_BE_KEY
  - name: URLScan
    apikey: YOUR_URLSCAN_KEY
```

## Data Sources (Passive DNS and More)

Amass integrates 50+ data sources out of the box. Key categories:

| Category | Sources |
|----------|---------|
| Certificate Transparency | crt.sh, CertSpotter, Facebook CT |
| Passive DNS | Mnemonic, Robtex, CIRCL |
| DNS Databases | VirusTotal, SecurityTrails, PassiveTotal |
| Search Engines | Google, Bing, Yahoo, Baidu, DuckDuckGo |
| Web Archives | Wayback Machine, CommonCrawl |
| Internet Scanning | Shodan, Censys, BinaryEdge |
| Code / Dev | GitHub, GitLab (search for subdomain leakage) |
| Threat Intel | AlienVault OTX, ThreatCrowd |
| BGP / Routing | BGPView, Hurricane Electric |
| DNS Wild Card / AXFR | Active zone transfer attempts |

```bash
# List all available data sources and their API status
amass enum -list-sources
```

## Visualization

```bash
# Generate D3.js graph (interactive HTML)
amass viz -d3 -d example.com -o graph.html

# Gephi format for advanced graph analysis
amass viz -gephi -d example.com -o graph.gexf

# GraphML format
amass viz -graphml -d example.com -o graph.graphml

# DOT format (Graphviz)
amass viz -dot -d example.com -o graph.dot
dot -Tsvg graph.dot > graph.svg
```

## Comparison with subfinder

| Feature | Amass | subfinder |
|---------|-------|-----------|
| Speed | Slow (thorough) | Fast |
| Passive DNS sources | 50+ | 40+ |
| Active brute force | Yes (built-in) | No (external) |
| Alterations | Yes | No |
| Graph database | Yes (sqlite) | No |
| Change tracking | Yes (`track`) | No |
| ASN/org mapping | Yes (`intel`) | No |
| Memory usage | High | Low |
| Config complexity | High | Low |
| Best for | Comprehensive OSINT | Quick passive enum |

**Recommended combined workflow:**
```bash
# Fast pass with subfinder
subfinder -d example.com -all -o sf-results.txt

# Deep pass with Amass
amass enum -passive -d example.com -config ~/.config/amass/config.yaml -o amass-results.txt

# Merge and deduplicate
cat sf-results.txt amass-results.txt | sort -u > all-subs.txt
```

## Common Workflows

### Full Passive Recon

```bash
#!/bin/bash
DOMAIN=$1
OUTDIR="recon-$DOMAIN-$(date +%Y%m%d)"
mkdir -p "$OUTDIR"

# Passive enumeration with all API sources
amass enum -passive -d "$DOMAIN" \
  -config ~/.config/amass/config.yaml \
  -o "$OUTDIR/subdomains.txt" \
  -json "$OUTDIR/amass-full.json" \
  -log "$OUTDIR/amass.log"

echo "[+] Found $(wc -l < "$OUTDIR/subdomains.txt") subdomains"
```

### Active + Brute Force Enumeration

```bash
amass enum -active -brute -alts \
  -d example.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
  -rf resolvers.txt \
  -tr 1.1.1.1,8.8.8.8 \
  -config ~/.config/amass/config.yaml \
  -o active-enum.txt \
  -json active-enum.json
```

### Attack Surface Expansion (Intel Phase)

```bash
# 1. Find target ASNs
amass intel -org "Target Corp" | tee target-asns.txt

# 2. Enumerate IP ranges per ASN
while read -r asn; do
    amass intel -asn "$asn" | tee -a target-cidrs.txt
done < target-asns.txt

# 3. Run enum across all discovered domains
amass enum -passive -df discovered-domains.txt \
  -config ~/.config/amass/config.yaml \
  -o all-subs.txt

# 4. Probe for live HTTP(S) services
cat all-subs.txt | httpx -silent -o live-hosts.txt
```

### Weekly Change Tracking

```bash
#!/bin/bash
# Run weekly, alert on new domains
amass enum -passive -d example.com \
  -config ~/.config/amass/config.yaml \
  -o /dev/null 2>&1

amass track -d example.com -show new > new-subs-$(date +%Y%m%d).txt
if [ -s new-subs-$(date +%Y%m%d).txt ]; then
    echo "New subdomains detected:" | cat - new-subs-$(date +%Y%m%d).txt | mail -s "Amass Alert: $domain" security@company.com
fi
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Very slow / hanging | Normal for passive mode — Amass queries 50+ sources; use `-timeout 30` |
| No results | Check API key validity; try `amass enum -list-sources` to see active sources |
| Wildcard DNS false positives | Amass auto-detects wildcards; if not, add domain to scope blacklist |
| High memory usage | Normal — graph DB is in-memory during run; reduce sources with `-src` flag |
| Database locked | Only run one Amass instance per database directory |
| Brute force slow | Use smaller wordlist; increase `-max-dns-queries` |
| `connection refused` (Docker) | Mount config: `-v ~/.config/amass:/root/.config/amass` |
| API auth errors | Verify key format in config.yaml; test key independently |
| Resolver SERVFAIL | Use public resolvers like `1.1.1.1`; avoid ISP resolvers for large scans |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
