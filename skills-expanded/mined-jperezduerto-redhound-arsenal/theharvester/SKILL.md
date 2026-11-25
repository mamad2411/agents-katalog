---
name: theharvester
description: >
  Operate theHarvester — a passive OSINT reconnaissance tool for gathering email addresses, subdomains,
  hosts, employee names, and open ports from public sources. Use during the reconnaissance phase of
  penetration tests or red team engagements to enumerate external attack surface from a domain name
  using dozens of data sources including Google, Bing, LinkedIn, GitHub, Shodan, CertSpotter, crt.sh,
  and VirusTotal. Covers installation, data sources, all major flags (-d, -b, -l, -n, -v, -S, -f),
  API key configuration, output formats, and OSINT recon workflow integration.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/laramies/theHarvester
  stars: '12.2k'
  language: Python
---

# theharvester Agent Skill

## When to Use This Skill

Use this skill when:
- Starting external reconnaissance on a target organization
- Enumerating email addresses to build a phishing target list or perform password spraying
- Discovering subdomains and virtual hosts to expand attack surface
- Gathering employee names for social engineering or username generation
- Identifying open ports and IPs associated with a target domain via Shodan integration
- The user asks about OSINT, email harvesting, subdomain enumeration, or passive recon

## What theHarvester Does

theHarvester is a passive reconnaissance tool that queries dozens of public data sources to enumerate
email addresses, subdomains, IP addresses, employee names, and open ports associated with a target
domain. Unlike active scanners, it does not touch the target directly — it queries third-party sources
(search engines, certificate transparency logs, breach databases, Shodan, VirusTotal) to build an
external picture of the target's digital footprint.

## Installation

### Method 1 — Kali Linux (pre-installed)

```bash
# Kali ships theHarvester — update for latest sources
sudo apt update && sudo apt install theharvester -y
theHarvester -h
```

### Method 2 — pip (Python 3.9+)

```bash
# Install from PyPI
pip3 install theHarvester

# Or install specific version
pip3 install theHarvester==4.5.0
```

### Method 3 — From Source (recommended for latest sources)

```bash
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip3 install -r requirements/base.txt
pip3 install -r requirements/dev.txt

# Run directly
python3 theHarvester.py -h

# Or install
pip3 install -e .
```

### Verify Installation

```bash
theHarvester -h
# or
python3 theHarvester.py -h
```

## Core Concepts

### How It Works

theHarvester sends queries to public APIs and search engines, parsing results for:
- **Email addresses** — scraped from search results, GitHub commits, LinkedIn profiles
- **Subdomains** — discovered via DNS certificate transparency logs (crt.sh, CertSpotter), search
  engine indexed subdomains, DNS brute force (active)
- **IP addresses** — A records for discovered subdomains, Shodan host data
- **Employee names** — LinkedIn profiles, search engine results
- **Open ports** — Shodan API data associated with discovered IPs
- **Virtual hosts** — Bing reverse IP lookups, DNS-based discovery

### Data Sources Overview

Sources are specified with `-b`. Each source queries a different external service:

| Source | Type | Finds | API Key Required |
|--------|------|-------|-----------------|
| `google` | Search engine | emails, hosts | No (rate limited) |
| `bing` | Search engine | emails, hosts, virtual hosts | No |
| `baidu` | Search engine | emails, hosts | No |
| `yahoo` | Search engine | emails, hosts | No |
| `duckduckgo` | Search engine | emails, hosts | No |
| `linkedin` | Social | employee names | No (limited) |
| `twitter` | Social | emails | No |
| `github-code` | Code | emails, API keys in code | Yes (GITHUB_TOKEN) |
| `certspotter` | Cert transparency | subdomains | Yes (free tier) |
| `crtsh` | Cert transparency | subdomains | No |
| `dnsdumpster` | DNS | subdomains | No |
| `rapiddns` | DNS | subdomains | No |
| `shodan` | IoT/scan | IPs, ports, banners | Yes |
| `virustotal` | Threat intel | subdomains | Yes (free tier) |
| `hunter` | Email intel | emails | Yes |
| `securityTrails` | DNS history | subdomains, DNS history | Yes |
| `otx` | Threat intel | subdomains, IPs | Yes (free) |
| `fullhunt` | Attack surface | subdomains | Yes |
| `bevigil` | Mobile OSINT | subdomains from APKs | Yes |
| `binaryedge` | Scan data | subdomains, ports | Yes |
| `anubis` | DNS | subdomains | No |
| `hackertarget` | DNS | subdomains | No |
| `sitedossier` | Web | subdomains | No |

## CLI Reference

### Core Flags

```bash
-d DOMAIN       # Target domain (required)
-b SOURCE       # Data source(s) to query (required)
-l N            # Limit results per source (default 500)
-S              # Take screenshots of discovered hosts
-n              # DNS lookup on discovered hosts
-v              # Enable virtual host discovery (Bing reverse IP)
-e SOURCE       # Exclude a source from -b all
-f FILENAME     # Output file (auto-detects XML or JSON by extension)
--screenshot DIR # Save screenshots to directory
-t              # Enable DNS TLD expansion
--dns-brute     # Perform DNS brute force using built-in wordlist
--dns-server IP # Use specific DNS server for resolution
```

### Basic Usage Examples

```bash
# Search Google for emails and hosts (quick start)
theHarvester -d example.com -b google

# Search multiple sources
theHarvester -d example.com -b google,bing,crtsh

# Use all sources (slow, requires API keys for full coverage)
theHarvester -b all -d example.com

# All sources except specific ones
theHarvester -b all -e linkedin,twitter -d example.com

# Limit results per source to 100
theHarvester -d example.com -b google -l 100

# Limit results — useful for rate-limited or slow sources
theHarvester -d example.com -b bing -l 200
```

### Certificate Transparency Sources (Best for Subdomains)

```bash
# crt.sh — certificate transparency log search (no API key, comprehensive)
theHarvester -d example.com -b crtsh

# CertSpotter — another CT log aggregator
theHarvester -d example.com -b certspotter

# Combine CT sources for maximum subdomain coverage
theHarvester -d example.com -b crtsh,certspotter,dnsdumpster,rapiddns
```

### Shodan Integration (Requires API Key)

```bash
# Shodan — enriches IPs with open ports, banners, CVEs
theHarvester -d example.com -b shodan

# Shodan results include:
# - IP addresses associated with domain
# - Open ports on those IPs
# - Service banners
# - Hostname data

# API key must be set in api-keys.yaml (see API Key Configuration below)
```

### Email Harvesting Focus

```bash
# Best sources for email addresses
theHarvester -d example.com -b google,bing,baidu,hunter,github-code

# Hunter.io — specialized in professional email discovery
theHarvester -d example.com -b hunter

# LinkedIn (finds employee names that can be turned into emails)
theHarvester -d example.com -b linkedin

# GitHub — searches code repos for committer emails
theHarvester -d example.com -b github-code
```

### DNS Resolution and Virtual Hosts

```bash
# Resolve all discovered subdomains to IPs (-n flag)
theHarvester -d example.com -b crtsh,dnsdumpster -n

# Virtual host discovery — Bing reverse IP lookup
# Finds other domains hosted on same IPs
theHarvester -d example.com -b bing -v

# DNS TLD expansion — tries common TLD variations
theHarvester -d example.com -b crtsh -t

# DNS brute force (active, semi-passive)
theHarvester -d example.com -b dnsdumpster --dns-brute

# Use specific DNS server
theHarvester -d example.com -b crtsh -n --dns-server 8.8.8.8
```

### Screenshots

```bash
# Take screenshots of discovered web hosts (-S flag)
# Requires aquatone or gowitness in PATH
theHarvester -d example.com -b crtsh,bing -S

# Specify screenshot output directory
theHarvester -d example.com -b crtsh --screenshot ./screenshots/
```

### Output Formats

```bash
# Save results to XML file
theHarvester -d example.com -b google,crtsh -f results.xml

# Save results to JSON file
theHarvester -d example.com -b google,crtsh -f results.json

# HTML output (older versions)
theHarvester -d example.com -b google -f results.html

# Output filename extension determines format:
# .xml → XML format
# .json → JSON format
```

## API Key Configuration

theHarvester reads API keys from `api-keys.yaml` in its configuration directory.

```bash
# Find config file location
find / -name "api-keys.yaml" 2>/dev/null
# Usually: ~/.theHarvester/api-keys.yaml or /etc/theHarvester/api-keys.yaml
# Or in the cloned repo: theHarvester/

# Edit api-keys.yaml
nano ~/.theHarvester/api-keys.yaml
```

```yaml
# api-keys.yaml
apikeys:
  bevigil:
    key: YOUR_BEVIGIL_KEY
  binaryedge:
    key: YOUR_BINARYEDGE_KEY
  certspotter:
    key: YOUR_CERTSPOTTER_KEY
  fullhunt:
    key: YOUR_FULLHUNT_KEY
  github:
    key: YOUR_GITHUB_TOKEN        # Personal access token (no special scopes needed)
  hunter:
    key: YOUR_HUNTER_IO_KEY
  intelx:
    key: YOUR_INTELX_KEY
  otx:
    key: YOUR_OTX_KEY
  securityTrails:
    key: YOUR_SECURITYTRAILS_KEY
  shodan:
    key: YOUR_SHODAN_API_KEY
  virustotal:
    key: YOUR_VIRUSTOTAL_KEY
  zoomeye:
    key: YOUR_ZOOMEYE_KEY
```

### Free API Keys (Recommended to Get)

```bash
# All of these have free tiers sufficient for assessments:
# Shodan:         https://account.shodan.io/ (free tier: basic data)
# VirusTotal:     https://www.virustotal.com/gui/join-us (free)
# OTX AlienVault: https://otx.alienvault.com/ (free)
# SecurityTrails: https://securitytrails.com/ (free tier)
# Hunter.io:      https://hunter.io/ (free tier: 25 searches/month)
# GitHub:         Generate token at https://github.com/settings/tokens
# CertSpotter:    https://sslmate.com/certspotter/api/
```

## Common OSINT Recon Workflow

### Phase 1 — Passive Subdomain Discovery

```bash
# No API keys required — start here
theHarvester -d target.com -b crtsh,certspotter,dnsdumpster,rapiddns,anubis,hackertarget \
  -f phase1_passive.json -n

# Extract subdomains from output
cat phase1_passive.json | jq -r '.hosts[]' | sort -u > subdomains.txt
```

### Phase 2 — Email Address Harvesting

```bash
# Search engines + specialized sources
theHarvester -d target.com -b google,bing,baidu,github-code,hunter \
  -l 500 -f phase2_emails.json

# Extract emails
cat phase2_emails.json | jq -r '.emails[]' | sort -u > emails.txt
wc -l emails.txt
```

### Phase 3 — Enrichment with Shodan

```bash
# Get IP/port data for discovered IPs (requires Shodan API key)
theHarvester -d target.com -b shodan -n -f phase3_shodan.json

# Also run all free sources together
theHarvester -d target.com -b all -e linkedin -l 300 -f phase3_all.json
```

### Phase 4 — Consolidation

```bash
# Merge all discovered subdomains
for f in phase*.json; do
  jq -r '.hosts[] // empty' "$f" 2>/dev/null
done | sort -u > all_subdomains.txt

# Merge all emails
for f in phase*.json; do
  jq -r '.emails[] // empty' "$f" 2>/dev/null
done | sort -u > all_emails.txt

echo "Subdomains discovered: $(wc -l < all_subdomains.txt)"
echo "Emails discovered: $(wc -l < all_emails.txt)"

# Probe subdomains for live web services
cat all_subdomains.txt | httpx -ports 80,443,8080,8443 -o live_web.txt

# Screenshot live services
eyewitness --web -f live_web.txt -d ./screenshots/
```

### Phase 5 — Username Generation for Spraying

```bash
# Convert harvested names/emails to username list for Kerbrute
cat all_emails.txt | awk -F@ '{print $1}' > email_local_parts.txt

# Generate AD-format usernames from harvested employee names
# (First initial + Last name format)
cat names.txt | awk '{print tolower(substr($1,1,1)) tolower($2)}' >> usernames.txt

# Feed to Kerbrute for user enumeration
kerbrute userenum -d target.local --dc DC_IP \
  usernames.txt -o valid_ad_users.txt
```

## Advanced Techniques

### Chaining with amass for Deeper Coverage

```bash
# Run theHarvester for emails/CT; amass for deeper subdomain enumeration
theHarvester -d target.com -b crtsh,dnsdumpster,google -f harvester_results.json &
amass enum -passive -d target.com -o amass_subdomains.txt &
wait
# Merge results
cat amass_subdomains.txt >> all_subdomains.txt
cat harvester_results.json | jq -r '.hosts[]' >> all_subdomains.txt
sort -u all_subdomains.txt -o all_subdomains.txt
```

### Bulk Domain OSINT

```bash
# Run theHarvester against multiple acquired domains / subsidiaries
while read domain; do
  echo "[*] Harvesting: $domain"
  theHarvester -d "$domain" -b crtsh,google,dnsdumpster \
    -f "results_${domain//./\_}.json" -n 2>/dev/null
  sleep 5  # Throttle to avoid rate limiting
done < domains.txt
```

### Export and Deduplication

```bash
# Consolidate all JSON results into a master subdomain list
find . -name "results_*.json" -exec jq -r '.hosts[] // empty' {} \; | \
  sort -u > master_subdomains.txt

# Remove wildcard/catch-all results
# Test for wildcard DNS: nslookup randomxyz123.target.com
# If it resolves, many results may be catch-all

# Resolve only and remove non-resolving
cat master_subdomains.txt | dnsx -silent -o resolved_subdomains.txt
```

## Integration with Other Tools

### With EyeWitness

```bash
# Convert subdomains to URL format for EyeWitness
cat all_subdomains.txt | sed 's/^/https:\/\//' > urls_for_ew.txt
cat all_subdomains.txt | sed 's/^/http:\/\//' >> urls_for_ew.txt
eyewitness --web -f urls_for_ew.txt -d ./ew_output
```

### With Kerbrute

```bash
# Email local parts → Kerbrute username list
cat all_emails.txt | grep "@target.com" | cut -d@ -f1 > kerbrute_users.txt
kerbrute userenum -d target.local --dc DC_IP kerbrute_users.txt -o valid_users.txt
```

### With Nuclei

```bash
# Feed discovered live hosts to Nuclei for vulnerability scanning
cat live_web.txt | nuclei -t nuclei-templates/ -severity medium,high,critical
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| No results from Google | Rate limiting | Reduce `-l`, add delay, try different source |
| API source returns 0 results | Missing/invalid API key | Check `api-keys.yaml`, regenerate key |
| `ModuleNotFoundError` | Missing pip dependency | `pip3 install -r requirements/base.txt` |
| Shodan returns no data | Free tier limitations | Upgrade Shodan plan or use `crtsh`/Censys |
| Slow execution with `-b all` | Many sources, some slow/broken | Use `-e` to exclude slow sources |
| DNS resolution errors | DNS server issues | `--dns-server 8.8.8.8` |
| Screenshot fails | aquatone/gowitness not in PATH | `apt install gowitness` or use EyeWitness separately |
| LinkedIn returns names only | LinkedIn API restrictions | Use `-b linkedin` for name data; convert manually |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
