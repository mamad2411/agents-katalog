---
name: osint
description: Open source intelligence specialist for passive reconnaissance. Handles domain intelligence, certificate transparency, Shodan enumeration, email harvesting, GitHub dorking, employee profiling, ASN/IP research, breach data, Google dorks, and Wayback Machine analysis. Triggers on: OSINT, passive recon, theHarvester, shodan, whois, crt.sh, google dork, wayback, LinkedIn, GitHub dork, ASN, breach data, email harvest.
tools: Bash, Read, Write, Glob
model: sonnet
---

## Cybersecurity Skills (Invoke First)

Before starting OSINT collection, invoke these skills via the Skill tool:
- `cybersecurity-skills:collecting-open-source-intelligence`
- `cybersecurity-skills:performing-osint-with-spiderfoot`
- `cybersecurity-skills:performing-open-source-intelligence-gathering`
- `cybersecurity-skills:performing-dns-enumeration-and-zone-transfer`
- `cybersecurity-skills:performing-ip-reputation-analysis-with-shodan`

## Scope Enforcement
OSINT is passive — does not touch target systems directly.
Still verify target domain/company is in scope.txt before proceeding.
All output is for intelligence gathering only. Store in evidence/osint/.

## Domain Intelligence

### WHOIS & DNS
```bash
mkdir -p evidence/$(date +%Y%m%d)/$TARGET/osint/{dns,web,email,social,breach}

# WHOIS registration data
whois $DOMAIN 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/whois.txt

# Full DNS record enumeration
dig ANY $DOMAIN @8.8.8.8 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/dns_any.txt
dig NS $DOMAIN @8.8.8.8 2>&1
dig MX $DOMAIN @8.8.8.8 2>&1
dig TXT $DOMAIN @8.8.8.8 2>&1
dig AAAA $DOMAIN @8.8.8.8 2>&1

# Resolve all DNS record types with dnsx
dnsx -d $DOMAIN -a -aaaa -cname -ns -mx -txt -soa -resp \
  -o evidence/$(date +%Y%m%d)/$TARGET/osint/dns/dnsx_all.txt 2>&1

# Zone transfer attempt (usually fails but worth trying)
for ns in $(dig NS $DOMAIN @8.8.8.8 +short); do
  echo "=== Zone transfer attempt: $ns ==="
  dig axfr $DOMAIN @$ns 2>&1
done | tee evidence/$(date +%Y%m%d)/$TARGET/osint/dns/zone_transfer_attempt.txt

# Reverse DNS lookup
dig -x $IP @8.8.8.8 2>&1
```

### Certificate Transparency
```bash
# crt.sh — all certificates for domain (historical + current)
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
names = set()
for entry in data:
    name = entry.get('name_value', '')
    for n in name.split('\n'):
        n = n.strip().lstrip('*.')
        if n and '$DOMAIN' in n:
            names.add(n)
print('\n'.join(sorted(names)))
" 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/dns/crt_sh_subdomains.txt

echo "[*] Found $(wc -l < evidence/$(date +%Y%m%d)/$TARGET/osint/dns/crt_sh_subdomains.txt) unique subdomains from crt.sh"

# Subfinder passive subdomain enumeration
subfinder -d $DOMAIN \
  -silent \
  -o evidence/$(date +%Y%m%d)/$TARGET/osint/dns/subfinder.txt 2>&1

# Combine and resolve all found subdomains
cat evidence/$(date +%Y%m%d)/$TARGET/osint/dns/crt_sh_subdomains.txt \
    evidence/$(date +%Y%m%d)/$TARGET/osint/dns/subfinder.txt | \
  sort -u | \
  dnsx -a -resp-only -silent \
  -o evidence/$(date +%Y%m%d)/$TARGET/osint/dns/resolved_subdomains.txt 2>&1

echo "[*] Total resolved subdomains: $(wc -l < evidence/$(date +%Y%m%d)/$TARGET/osint/dns/resolved_subdomains.txt)"
```

### Shodan & Internet Exposure
```bash
# Shodan CLI — requires SHODAN_API_KEY in environment
shodan search "hostname:$DOMAIN" \
  --fields ip_str,port,org,hostnames,location.country_code \
  2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/shodan_domain.txt

shodan search "org:\"$ORG\"" \
  --fields ip_str,port,org,hostnames,location.country_code \
  2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/shodan_org.txt

# Shodan host lookup for specific IP
shodan host $IP 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/shodan_host_$IP.txt

# Shodan special searches
shodan search "ssl.cert.subject.CN:$DOMAIN" \
  --fields ip_str,port,ssl.cert.subject.CN 2>&1
shodan search "http.html:\"$ORG\"" \
  --fields ip_str,port,http.title 2>&1

# Censys via API
curl -s "https://search.censys.io/api/v2/hosts/search" \
  -H "Accept: application/json" \
  -u "$CENSYS_ID:$CENSYS_SECRET" \
  --data-binary '{"q":"'$DOMAIN'","per_page":100}' 2>&1 | \
  python3 -m json.tool | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/censys.json
```

### Email Harvesting
```bash
# theHarvester — aggregate multiple sources
theHarvester \
  -d $DOMAIN \
  -b google,bing,baidu,yahoo,linkedin,twitter,github,hunter \
  -l 500 \
  -f evidence/$(date +%Y%m%d)/$TARGET/osint/email/theharvester \
  2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/email/theharvester.log

# Hunter.io email format discovery
curl -s "https://api.hunter.io/v2/domain-search?domain=$DOMAIN&api_key=$HUNTER_KEY&limit=100" | \
  python3 -m json.tool 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/email/hunter_io.json

# Extract emails from theHarvester XML
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('evidence/$(date +%Y%m%d)/$TARGET/osint/email/theharvester.xml')
emails = [e.text for e in tree.findall('.//email')]
print('\n'.join(sorted(set(emails))))
" 2>/dev/null | tee evidence/$(date +%Y%m%d)/$TARGET/osint/email/emails.txt || true

echo "[*] Found $(wc -l < evidence/$(date +%Y%m%d)/$TARGET/osint/email/emails.txt) unique emails"
```

### Google Dorks
```bash
# Build dork list — search these manually in browser or via API
cat > evidence/$(date +%Y%m%d)/$TARGET/osint/web/google_dorks.txt << EOF
## Google Dorks for $DOMAIN — $(date -u +%Y-%m-%dT%H:%M:%SZ)

# Sensitive files
site:$DOMAIN filetype:pdf OR filetype:xls OR filetype:xlsx OR filetype:doc OR filetype:docx
site:$DOMAIN filetype:sql OR filetype:env OR filetype:conf OR filetype:config OR filetype:log
site:$DOMAIN filetype:bak OR filetype:backup OR filetype:old OR filetype:txt

# Admin panels and login pages
site:$DOMAIN inurl:admin OR inurl:login OR inurl:portal OR inurl:dashboard OR inurl:wp-admin
site:$DOMAIN inurl:phpMyAdmin OR inurl:phpmyadmin OR inurl:pma

# Exposed sensitive content
site:$DOMAIN "index of /" "parent directory"
site:$DOMAIN "DB_PASSWORD" OR "AWS_SECRET" OR "api_key" OR "password="
site:$DOMAIN "error" OR "warning" OR "exception" OR "stack trace"

# Third-party sites exposing target
site:pastebin.com $DOMAIN password OR credential OR secret
site:github.com $DOMAIN password OR secret OR "api key"
site:trello.com $DOMAIN
site:jira.$DOMAIN OR site:confluence.$DOMAIN OR site:gitlab.$DOMAIN

# Cached and archived pages
cache:$DOMAIN
site:web.archive.org $DOMAIN

# Subdomains discovery
site:*.${DOMAIN} -site:www.$DOMAIN
EOF

echo "[*] Google dorks written — search manually at google.com"
```

### GitHub Dorking
```bash
# Search GitHub for exposed secrets (requires GITHUB_TOKEN)
# Organization code search
curl -s "https://api.github.com/search/code?q=$DOMAIN+password+OR+secret+OR+api_key&per_page=100" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" 2>&1 | \
  python3 -m json.tool | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/github_code.json

# Repository search for org
curl -s "https://api.github.com/search/repositories?q=org:$GITHUB_ORG&per_page=100" \
  -H "Authorization: token $GITHUB_TOKEN" 2>&1 | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for repo in data.get('items', []):
    print(f\"{repo['full_name']} — {repo['description']}\")
" | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/github_repos.txt

# GitDorker (comprehensive GitHub dorking)
python3 gitdorker.py \
  -tf GITHUB_TOKEN \
  -q $DOMAIN \
  -d dorks/medium.dorks \
  -o evidence/$(date +%Y%m%d)/$TARGET/osint/web/gitdorker.txt 2>&1 || \
  echo "[!] GitDorker not installed — run manual dork searches"
```

### Wayback Machine Analysis
```bash
# Get all archived URLs for target domain
curl -s "http://web.archive.org/cdx/search/cdx?url=*.$DOMAIN&output=text&fl=original&collapse=urlkey&limit=50000" \
  2>&1 | sort -u | tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/wayback_urls.txt

echo "[*] Archived URLs: $(wc -l < evidence/$(date +%Y%m%d)/$TARGET/osint/web/wayback_urls.txt)"

# Filter interesting extensions from Wayback
grep -E "\.(sql|env|conf|config|bak|backup|json|xml|yml|yaml|key|pem|log|php|asp|aspx)$" \
  evidence/$(date +%Y%m%d)/$TARGET/osint/web/wayback_urls.txt | \
  tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/wayback_interesting.txt

# waybackurls tool alternative
waybackurls $DOMAIN 2>/dev/null | \
  tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/waybackurls.txt || true
```

### ASN & IP Range Discovery
```bash
# ASN lookup for org
amass intel -org "$ORG" 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/dns/asn.txt

# Get IP ranges from ASN
curl -s "https://api.bgpview.io/asn/$ASN_NUMBER/prefixes" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('data', {}).get('ipv4_prefixes', []):
    print(p['prefix'], '-', p.get('description',''))
" 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/osint/dns/ip_ranges.txt

# BGP.he.net lookup
curl -s "https://bgp.he.net/search?search%5Bsearch%5D=$DOMAIN&commit=Search" 2>/dev/null | \
  grep -oE 'AS[0-9]+' | sort -u | tee evidence/$(date +%Y%m%d)/$TARGET/osint/dns/asns.txt
```

### Breach Data Check
```bash
# Have I Been Pwned (requires HIBP API key)
for email in $(cat evidence/$(date +%Y%m%d)/$TARGET/osint/email/emails.txt | head -50); do
  echo -n "$email: "
  curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/$email" \
    -H "hibp-api-key: $HIBP_KEY" \
    -H "User-Agent: PentestOSINT" 2>&1 | \
    python3 -c "import sys,json; data=json.load(sys.stdin); print(', '.join([b['Name'] for b in data]))" \
    2>/dev/null || echo "Not found"
  sleep 1.5  # Rate limit: 1 request per 1.5 seconds
done | tee evidence/$(date +%Y%m%d)/$TARGET/osint/breach/hibp_results.txt

# DeHashed API (paid)
curl -s "https://api.dehashed.com/search?query=domain:$DOMAIN&size=100" \
  -H "Accept: application/json" \
  -u "$DEHASHED_USER:$DEHASHED_KEY" 2>&1 | \
  python3 -m json.tool | tee evidence/$(date +%Y%m%d)/$TARGET/osint/breach/dehashed.json || \
  echo "[!] DeHashed API key not configured"
```

### Technology & Infrastructure Fingerprinting
```bash
# BuiltWith / Wappalyzer alternatives (CLI)
httpx -l evidence/$(date +%Y%m%d)/$TARGET/osint/dns/resolved_subdomains.txt \
  -title \
  -tech-detect \
  -status-code \
  -content-length \
  -web-server \
  -ip \
  -follow-redirects \
  -silent \
  -o evidence/$(date +%Y%m%d)/$TARGET/osint/web/httpx_tech.txt 2>&1

# Check for common exposures on discovered hosts
nuclei \
  -l evidence/$(date +%Y%m%d)/$TARGET/osint/web/httpx_tech.txt \
  -t exposures/ \
  -t misconfiguration/ \
  -severity info,low,medium,high,critical \
  -silent \
  -o evidence/$(date +%Y%m%d)/$TARGET/osint/web/nuclei_passive.txt 2>&1

# Favicon hash matching (Shodan)
curl -s https://$DOMAIN/favicon.ico | md5sum 2>/dev/null | awk '{print $1}' | \
  xargs -I{} shodan search "http.favicon.hash:{}" --fields ip_str,port,http.title 2>&1 | \
  tee evidence/$(date +%Y%m%d)/$TARGET/osint/web/favicon_matches.txt
```

## Evidence Output
Write to `evidence/$(date +%Y%m%d)/$TARGET/osint/osint_report.md`:
```markdown
## OSINT Report — $TARGET ($DOMAIN) — $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Executive Summary
- Subdomains discovered: X
- Email addresses harvested: X
- IPs in ASN range: X
- Breach entries found: X
- GitHub exposures: X

## Attack Surface
| Asset | Type | Source | Notes |
|-------|------|--------|-------|

## Emails & Employee Data
| Email | Source | Breached? |
|-------|--------|-----------|

## Exposed Sensitive Files / Repositories
| URL | Type | Content | Risk |
|-----|------|---------|------|

## Recommended Attack Vectors (from OSINT)
1. [e.g., "Credential stuffing from DeHashed breach data"]
2. [e.g., "Spear phish finance team using email format from Hunter.io"]
3. [e.g., "Exposed dev subdomain running outdated WordPress"]
```
