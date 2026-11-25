---
name: httpx
description: >
  Operate and pipeline httpx — a fast, multi-purpose HTTP toolkit by ProjectDiscovery for
  probing live web services at scale. Use when working with projectdiscovery/httpx, when the
  user needs to identify live hosts from a list, extract status codes, page titles, tech stacks,
  web server banners, content lengths, or response times. Covers installation, all major flags,
  output formats, matching/filtering, favicon hashing, custom headers, rate limiting, and
  integration in the subfinder → httpx → nuclei reconnaissance pipeline.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/projectdiscovery/httpx
  language: Go
---

# httpx Agent Skill

## When to Use This Skill

Use this skill when:
- Probing a large list of hosts/subdomains to identify live HTTP/HTTPS services
- Extracting titles, status codes, tech stacks, or web server banners at scale
- Filtering large host lists by status code, content-length, or technology
- Feeding live host lists into nuclei or other scanning tools
- The user asks about httpx, HTTP probing, or web fingerprinting
- Detecting services by favicon hash (Shodan-style fingerprinting)
- Building reconnaissance pipelines with subfinder, nmap, amass, or nuclei

## What httpx Does

httpx is a high-performance HTTP probing tool that sends HTTP requests to a list of targets and
reports back rich metadata: status codes, content length, page title, web server, TLS certificate
details, technology stack (via Wappalyzer-equivalent fingerprints), response time, and more. It
is designed for scale — handling hundreds of thousands of hosts with configurable concurrency —
and integrates natively with the rest of the ProjectDiscovery ecosystem.

## Installation

### Go install (recommended)
```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### Pre-built binary
```bash
VERSION=1.6.10
curl -sSL https://github.com/projectdiscovery/httpx/releases/download/v${VERSION}/httpx_${VERSION}_linux_amd64.zip \
  -o httpx.zip && unzip httpx.zip httpx && chmod +x httpx && sudo mv httpx /usr/local/bin/
```

### Docker
```bash
docker pull projectdiscovery/httpx:latest
echo "example.com" | docker run --rm -i projectdiscovery/httpx:latest -title -tech-detect -status-code
```

### Kali / apt
```bash
# Not in default Kali repos — use Go install above
sudo apt install -y golang && go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

## Core Concepts

### Input methods
- stdin pipe (most common in pipelines)
- `-l` flag for a file of hosts
- `-u` / `-target` for a single URL

### Output modes
- Colorized stdout (default interactive)
- `-o` for plain file output
- `-json` / `-jsonl` for structured JSON
- `-csv` for spreadsheet-friendly output
- `-silent` + `-o` for clean file output with no noise

### Probing behaviour
- Tries both HTTP and HTTPS unless told otherwise
- Follows redirects by default (configurable depth)
- Uses a custom user-agent (configurable)
- Rate limits per-host and globally configurable
- Response body read limited to `-response-size-to-read` bytes

## CLI Reference

### Basic probing
```bash
# Single host
httpx -u https://example.com

# List of hosts from file
httpx -l hosts.txt

# From stdin
cat subdomains.txt | httpx

# Probe a CIDR range (use with caution — very noisy)
httpx -l cidr.txt -p 80,443,8080,8443
```

### Common output flags (combine freely)
```bash
httpx -l hosts.txt \
  -status-code   \    # -sc  : HTTP status code
  -title         \    # -t   : Page <title>
  -content-length\    # -cl  : Response body size
  -web-server    \    # -ws  : Server header
  -tech-detect   \    # -td  : Wappalyzer tech stack
  -response-time \    # -rt  : Time to first byte
  -ip            \    # -ip  : Resolved IP address
  -cname         \    # -cn  : CNAME chain
  -location      \    # -lc  : Redirect location
  -favicon       \    # -fh  : Favicon MD5 hash
  -tls-grab      \    # -tls : TLS cert details
  -hash sha256   \    # Body hash (md5, sha1, sha256, mmh3)
  -screenshot         # Screenshot page (requires headless Chrome)
```

### Tech detection
```bash
# Identify CMS, frameworks, libraries, WAFs
httpx -l hosts.txt -tech-detect -silent

# Combined with title and status code
httpx -l hosts.txt -td -title -sc -silent -o results.txt
```

### Status code filtering
```bash
# Only show 200 OK
httpx -l hosts.txt -mc 200

# Only show 2xx and 3xx
httpx -l hosts.txt -mc 200,301,302,307,403

# Filter OUT 404s
httpx -l hosts.txt -fc 404

# Multiple exclusions
httpx -l hosts.txt -fc 404,400,500
```

### Content-length filtering
```bash
# Only responses larger than 0 bytes (filter empty responses)
httpx -l hosts.txt -ml 1

# Filter out responses matching exact content length (e.g., default 404 page)
httpx -l hosts.txt -fl 1234

# Minimum content length
httpx -l hosts.txt -ml 100
```

### String / regex matching in response
```bash
# Match responses containing a string
httpx -l hosts.txt -ms "admin panel"

# Match via regex
httpx -l hosts.txt -mr "api_key|secret|token"

# Filter out responses containing a string
httpx -l hosts.txt -fs "maintenance mode"

# Filter via regex
httpx -l hosts.txt -fr "403 Forbidden|Access Denied"
```

### Port scanning (HTTP-aware)
```bash
# Probe multiple ports per host
httpx -l hosts.txt -p 80,443,8080,8443,8888,9090,3000,4443

# Probe specific ports only
httpx -l hosts.txt -p 8080 -p 8443

# Probe all 65535 ports (slow — use targeted lists instead)
httpx -l hosts.txt -p 1-65535
```

### Following redirects
```bash
# Follow up to 10 redirects (default is 10)
httpx -l hosts.txt -follow-redirects

# Disable redirect following
httpx -l hosts.txt -no-follow-redirects

# Only follow redirects within same host
httpx -l hosts.txt -follow-host-redirects
```

### Custom headers and methods
```bash
# Add custom header
httpx -l hosts.txt -H "X-Forwarded-For: 127.0.0.1" -H "Authorization: Bearer TOKEN"

# Use POST method
httpx -l hosts.txt -x POST

# Send POST body
httpx -l hosts.txt -x POST -body '{"user":"admin","pass":"admin"}'

# Custom user agent
httpx -l hosts.txt -ua "Mozilla/5.0 (compatible; Googlebot/2.1)"
```

### Rate limiting and concurrency
```bash
# Set number of concurrent threads (default 50)
httpx -l hosts.txt -c 100

# Rate limit: requests per second
httpx -l hosts.txt -rate-limit 100

# Rate limit per host
httpx -l hosts.txt -rate-limit-minute 60

# Timeout per request (seconds)
httpx -l hosts.txt -timeout 10

# Retries
httpx -l hosts.txt -retries 2
```

### Output formats
```bash
# JSON (one object per line — JSONL)
httpx -l hosts.txt -json -o results.jsonl

# JSON with full response body
httpx -l hosts.txt -json -include-response -o full.jsonl

# CSV output
httpx -l hosts.txt -csv -o results.csv

# Silent (no progress, just results)
httpx -l hosts.txt -silent -o clean.txt

# Store response bodies to directory
httpx -l hosts.txt -store-response -store-response-dir ./responses/

# Store chain (all redirect responses)
httpx -l hosts.txt -store-chain
```

### Favicon hash detection (Shodan-style)
```bash
# Get MMH3 favicon hash for a host
httpx -u https://example.com -favicon

# Batch favicon hashing
httpx -l hosts.txt -favicon -silent -json | jq -r '"\(.favicon) \(.url)"'

# Cross-reference hash against known fingerprints
# Known hashes: https://github.com/sansatart/scrapts/blob/master/shodan-favicon-hashes.csv
# Shodan query: http.favicon.hash:-247388890
```

### TLS/Certificate inspection
```bash
# Grab TLS details
httpx -l hosts.txt -tls-grab -json | jq '.tls'

# Filter expired certs
httpx -l hosts.txt -tls-grab -json | \
  jq -r 'select(.tls.expired == true) | .url'

# Find certs expiring in 30 days
httpx -l hosts.txt -tls-grab -json | \
  jq -r 'select(.tls.not_after != null) | [.url, .tls.not_after] | @tsv'
```

## Common Workflows

### Workflow 1: Subfinder → httpx → nuclei (full recon pipeline)
```bash
# Step 1: enumerate subdomains
subfinder -d example.com -silent -o subdomains.txt

# Step 2: probe live web services
httpx -l subdomains.txt -silent -o live-hosts.txt

# Step 3: scan with nuclei for vulnerabilities
nuclei -l live-hosts.txt -t /root/nuclei-templates/ -o vulns.txt
```

### Workflow 2: nmap → httpx enrichment
```bash
# Extract open HTTP ports from nmap XML
nmap -p 80,443,8080,8443 192.168.1.0/24 -oX scan.xml
# Parse IPs with open ports → feed to httpx
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('scan.xml')
for host in tree.findall('.//host'):
    ip = host.find('.//address[@addrtype=\"ipv4\"]').get('addr')
    for port in host.findall('.//port[@protocol=\"tcp\"]'):
        if port.find('state').get('state') == 'open':
            print(f'{ip}:{port.get(\"portid\")}')
" | httpx -sc -title -web-server -tech-detect -silent
```

### Workflow 3: Bug bounty scope probing
```bash
# Enumerate + probe + deduplicate + enrich
subfinder -d target.com -all -silent | \
  dnsx -silent -a | \
  httpx -sc -cl -title -td -location -silent -json -o bounty-recon.jsonl

# Find juicy endpoints
cat bounty-recon.jsonl | jq -r 'select(.status_code == 200) | "\(.status_code) \(.content_length) \(.title) \(.url)"' | sort -k2 -rn | head -50
```

### Workflow 4: Find admin panels
```bash
httpx -l hosts.txt -sc -title -silent | \
  grep -iE "(admin|dashboard|panel|login|console|management|portal)"
```

### Workflow 5: Technology-based targeting
```bash
# Find WordPress sites
httpx -l hosts.txt -tech-detect -silent -json | \
  jq -r 'select(.tech[]? | test("WordPress";"i")) | .url'

# Find Apache Struts (high-value)
httpx -l hosts.txt -tech-detect -silent -json | \
  jq -r 'select(.tech[]? | test("Apache Struts";"i")) | .url'
```

## Advanced Techniques

### Probe with SNI/virtual host override
```bash
# Force HTTP Host header (vhost fuzzing)
httpx -u http://192.168.1.100 -H "Host: internal.example.com" -title -sc
```

### Screenshot capturing (headless Chrome)
```bash
# Requires Chrome/Chromium in PATH
httpx -l hosts.txt -screenshot -screenshot-timeout 15 -screenshot-path ./screenshots/
```

### Custom fingerprint matching (YAML extension)
```bash
# httpx uses wappalyzer fingerprints internally; add custom tech detection via response matching
httpx -l hosts.txt -mr "X-Powered-By: CustomApp" -ms "customapp_version"
```

### Integration with Burp Suite
```bash
# Send all live hosts through Burp proxy
httpx -l hosts.txt -http-proxy http://127.0.0.1:8080 -sc -title
```

### jq recipes for JSONL output
```bash
# All 200 OK URLs
cat results.jsonl | jq -r 'select(.status_code == 200) | .url'

# Group by status code
cat results.jsonl | jq -r '.status_code' | sort | uniq -c | sort -rn

# URLs with interesting tech
cat results.jsonl | jq -r 'select(.tech | length > 0) | "\(.url) \(.tech | join(", "))"'

# Sort by content length descending
cat results.jsonl | jq -r '[.url, .content_length] | @tsv' | sort -k2 -rn | head -20
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `no such file or directory` binary | Not in PATH | Add $(go env GOPATH)/bin to PATH |
| Tech detection empty | Fingerprint DB not updated | Run `httpx -update` or reinstall |
| Slow throughput | Default concurrency too low | Increase `-c 200` or `-c 500` |
| TLS errors | Invalid certs on target | Add `-no-verify` flag |
| Too many false positives | Redirect to login page | Use `-fc 301,302` or `-ms "keyword"` |
| Screenshot fails | Chrome not found | Install `chromium-browser` and ensure it's in PATH |
| Rate limiting by target | Too aggressive | Use `-rate-limit 10 -c 10` |
| Large JSONL file hard to parse | Output too large | Filter with `-mc 200` before `-json` |

```bash
# Debug single host
httpx -u https://example.com -debug -v

# Update templates / fingerprints
httpx -update
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
