---
name: katana-crawler
description: >
  Operate Katana — the next-generation web crawling and spidering framework by ProjectDiscovery.
  Use when the user needs to enumerate web application endpoints, discover JavaScript files and
  API paths, extract forms, emails, or parameters, or when the user asks about Katana, web
  crawling, or spidering for bug bounty or pentesting. Covers installation (Go install, Docker),
  standard and headless Chrome crawling modes, depth and scope control, field extraction,
  output filtering, JavaScript parsing, automatic form filling, rate limiting, custom headers,
  and integration with the ProjectDiscovery tool chain (subfinder, httpx, nuclei).
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/projectdiscovery/katana
---

# katana-crawler Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to crawl a web application to discover all reachable endpoints
- The user asks about Katana or ProjectDiscovery's crawling tooling
- Building an asset inventory from discovered domains (subfinder → httpx → katana pipeline)
- Enumerating JavaScript files for hidden API endpoints and hardcoded secrets
- Running headless browser crawling to capture dynamically rendered pages
- Bug bounty recon workflows requiring deep parameter and form discovery

## What Katana Does

Katana is a high-performance web crawler built in Go by ProjectDiscovery that operates in two modes: a fast standard mode using Go's native HTTP client, and a headless mode that drives Chrome to render JavaScript and capture dynamically generated endpoints. It integrates natively with the rest of the ProjectDiscovery ecosystem — accepting output from httpx and subfinder and feeding into nuclei. Katana extracts URLs, JS file endpoints, form fields, email addresses, XHR requests, and more, with fine-grained scope control and output filtering.

## Installation

### Go Install (recommended)

```bash
# Requires Go 1.21+
go install github.com/projectdiscovery/katana/cmd/katana@latest

# Headless mode requires Chrome — install on Ubuntu:
sudo apt update && sudo apt install google-chrome-stable -y

# Ubuntu full install (Go + Chrome)
sudo apt update && sudo snap refresh
sudo apt install zip curl wget git -y
sudo snap install golang --classic
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt update && sudo apt install google-chrome-stable -y
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

### Docker

```bash
# Pull image
docker pull projectdiscovery/katana:latest

# Standard crawl
docker run projectdiscovery/katana:latest -u https://example.com

# Headless crawl (uses bundled Chrome)
docker run projectdiscovery/katana:latest -u https://example.com -headless

# With system Chrome (mount Chrome binary)
docker run projectdiscovery/katana:latest -u https://example.com -system-chrome -headless
```

### Binary Releases

```bash
# Download from releases page
wget https://github.com/projectdiscovery/katana/releases/latest/download/katana_*_linux_amd64.zip
unzip katana_*_linux_amd64.zip
chmod +x katana
mv katana /usr/local/bin/
```

## Core Concepts

### Crawling Modes

| Mode | Flag | Description | Use Case |
|---|---|---|---|
| **Standard** | (default) | Go HTTP client, no JS execution, fast | APIs, static sites, maximum speed |
| **Headless** | `-hl` / `-headless` | Chrome-driven, full JS rendering | SPAs, React/Vue/Angular apps, lazy-loaded content |

Standard mode is 3–5x faster but misses JavaScript-rendered endpoints. Headless mode catches endpoints that only exist after JS execution but requires Chrome and is slower.

### Scope Definitions

Katana's default scope (`rdn` — registered domain name) keeps crawling within `*.example.com`. Understanding scope modes prevents runaway crawls on third-party domains.

| Scope Value | Matches |
|---|---|
| `rdn` (default) | `*.example.com` — all subdomains |
| `fqdn` | Only the exact host specified (e.g., `www.example.com`) |
| `dn` | Domain name string match only (e.g., `example`) |
| Custom regex | Any pattern via `-cs` flag |

## CLI Reference

### Input / Output

```
-u, -url string[]           Target URL(s) — single or comma-separated
-list string                File with list of URLs (one per line)
-resume string              Resume from a saved state file
-o, -output string          Output file path
-j, -json                   JSON Lines output format (JSONL)
-no-color                   Disable color output
-silent                     Suppress informational output (results only)
-v, -verbose                Verbose mode
```

### Crawling Configuration

```
-d, -depth int              Maximum crawl depth (default: 3)
-jc, -js-crawl              Parse and crawl endpoints found in JS files
-jsl, -jsluice              Deep JS parsing with jsluice (memory intensive)
-ct, -crawl-duration value  Max duration for crawling (e.g., 30s, 5m)
-kf, -known-files string    Crawl known files: all, robotstxt, sitemapxml
-mrs, -max-response-size    Max response size to process (bytes, default: 2MB)
-timeout int                HTTP request timeout in seconds (default: 10)
-retry int                  Retries on failure (default: 1)
-proxy string               HTTP proxy URL (e.g., http://127.0.0.1:8080)
-H, -headers string[]       Custom HTTP headers (e.g., "Authorization: Bearer TOKEN")
```

### Rate Limiting and Concurrency

```
-c, -concurrency int        Concurrent goroutines per host (default: 10)
-p, -parallelism int        Concurrent targets to crawl in parallel (default: 10)
-rd, -delay int             Milliseconds between requests (rate limiting)
-rl, -rate-limit int        Max requests per second globally (default: 150)
-rlm, -rate-limit-minute    Max requests per minute globally
```

### Scope Control

```
-fs, -field-scope string    Scope by field: dn, rdn (default), fqdn
-cs, -crawl-scope string[]  Additional in-scope URL regex patterns
-cos, -crawl-out-scope string[]  Out-of-scope URL regex (excluded)
-ns, -no-scope              Disable default host-based scope (follow all links)
-do, -display-out-scope     Show out-of-scope endpoints in output
```

### Field Extraction

```
-f, -field string           Field(s) to display: url, path, fqdn, rdn, rurl, qurl,
                            qpath, file, ufile, key, value, kv, dir, udir
-sf, -store-field string    Store field per-host in separate files (same fields)
-ot, -output-template string  Custom output format string
-fx, -form-extraction       Extract form/input/textarea/select elements (JSONL)
-xhr, -xhr-extraction       Extract XHR URLs and methods (JSONL)
-td, -tech-detect           Detect technologies (JSONL output)
```

### Output Filtering

```
-mr, -match-regex string[]       Include only URLs matching regex
-fr, -filter-regex string[]      Exclude URLs matching regex
-em, -extension-match string[]   Match only specific extensions (php,js,html)
-ef, -extension-filter string[]  Exclude specific extensions (png,css,svg,ico)
-mdc, -match-condition string    DSL-based match condition
-fdc, -filter-condition string   DSL-based filter condition
-fpt, -filter-page-type string[] Filter by page type: error, captcha, parked
-duf, -disable-unique-filter     Allow duplicate URLs in output
```

## Headless Mode

Enable with `-hl` or `-headless`. Requires Chrome installed on the host.

```bash
# Basic headless crawl
katana -u https://app.example.com -hl

# Use system Chrome instead of Katana's bundled version
katana -u https://app.example.com -hl -sc

# Show browser window (debug)
katana -u https://app.example.com -hl -sb

# No sandbox (required in Docker/root environments)
katana -u https://app.example.com -hl -nos

# Wait longer for JS rendering (ms after DOMContentLoaded)
katana -u https://app.example.com -hl -dwt 8000

# Page load strategy
katana -u https://app.example.com -hl -pls networkidle

# Connect to existing Chrome instance (CDP)
katana -u https://app.example.com -cwu ws://127.0.0.1:9222

# Pass Chrome flags (e.g., ignore certificate errors)
katana -u https://app.example.com -hl -ho "--ignore-certificate-errors"

# Captcha solving (requires capsolver API key)
katana -u https://app.example.com -hl -csp capsolver -csk YOUR_API_KEY
```

### Headless Page Load Strategies

| Strategy | When to Use |
|---|---|
| `heuristic` (default) | Smart waiting — best for most sites |
| `load` | Wait for full `load` event |
| `domcontentloaded` | DOMContentLoaded + `--dom-wait-time` |
| `networkidle` | Wait until no network requests for 500ms |
| `none` | No waiting — fastest, may miss lazy content |

## JavaScript Crawling and Parsing

```bash
# Parse endpoints out of JS files encountered during crawl
katana -u https://app.example.com -jc

# Deep JS analysis with jsluice (finds more secrets/endpoints, RAM intensive)
katana -u https://app.example.com -jsl

# Both combined (maximum JS coverage)
katana -u https://app.example.com -jc -jsl -hl

# Target only JS files and extract endpoints
katana -u https://app.example.com -em js -jc -f url
```

## Form Filling and Submission

Katana can automatically fill and submit forms encountered during crawling, enabling discovery of endpoints only reachable via POST or parameterized GET.

```bash
# Enable automatic form fill (experimental)
katana -u https://app.example.com -aff

# Use custom form config
katana -u https://app.example.com -aff -fc /path/to/form-config.yaml

# Extract form fields without submitting
katana -u https://app.example.com -fx -j
```

Default form config location: `~/.config/katana/form-config.yaml`

```yaml
# form-config.yaml example
- selector: "input[type=email]"
  value: "test@example.com"
- selector: "input[name=username]"
  value: "testuser"
- selector: "input[name=password]"
  value: "Password123!"
- selector: "input[type=text]"
  value: "{{rand_str(8)}}"   # DSL function
```

## Field Extraction Deep Dive

```bash
# Extract only URLs
katana -u https://example.com -f url

# Extract unique file extensions found
katana -u https://example.com -f file

# Extract all query parameter key=value pairs
katana -u https://example.com -f kv

# Extract all query parameter keys (for fuzzing)
katana -u https://example.com -f key

# Extract unique directories
katana -u https://example.com -f dir

# Custom template: show method + URL
katana -u https://example.com -ot "{{method}} {{url}}"

# Store per-host output
katana -list hosts.txt -sf url -o crawl_output/
```

### Extracting JS Files and Analyzing with LinkFinder/SecretFinder

```bash
# Extract all JS file URLs
katana -u https://app.example.com -em js -f url -silent | tee js_files.txt

# Download and analyze with linkfinder
cat js_files.txt | xargs -I{} python3 linkfinder.py -i {} -o cli | tee endpoints.txt

# Analyze with trufflehog / secretfinder
cat js_files.txt | xargs -I{} curl -sk {} | grep -E "(api_key|token|secret|password)" -i
```

## Custom Headers and Authentication

```bash
# Bearer token auth
katana -u https://api.example.com -H "Authorization: Bearer eyJhbGci..."

# Multiple headers
katana -u https://app.example.com \
  -H "Cookie: session=abc123def456" \
  -H "X-Forwarded-For: 127.0.0.1"

# User-agent spoofing
katana -u https://app.example.com -H "User-Agent: Mozilla/5.0 (compatible; Googlebot)"

# Through Burp proxy (intercept crawl traffic)
katana -u https://app.example.com -proxy http://127.0.0.1:8080
```

## Common Workflows

### Bug Bounty Recon — Full Pipeline

```bash
# Step 1: Subdomain discovery
subfinder -d target.com -silent | tee subdomains.txt

# Step 2: Probe for live web hosts
cat subdomains.txt | httpx -silent | tee live_hosts.txt

# Step 3: Deep crawl all live hosts
cat live_hosts.txt | katana -jc -d 5 -rl 100 -o all_endpoints.txt

# Step 4: Feed interesting endpoints to nuclei
cat all_endpoints.txt | nuclei -t ~/nuclei-templates/ -severity medium,high,critical

# Step 5: Extract parameters for fuzzing
cat all_endpoints.txt | grep "?" | grep -oP "\?.*" | tr "&" "\n" | cut -d= -f1 | sort -u > parameters.txt
```

### Authenticated Application Crawl

```bash
# Log in via browser, copy session cookie, then crawl with auth
katana -u https://app.example.com \
  -H "Cookie: PHPSESSID=abc123; auth_token=xyz789" \
  -hl -d 5 -jc -aff \
  -o authenticated_endpoints.txt
```

### JavaScript-Heavy SPA Crawl

```bash
# React/Vue/Angular app — headless only
katana -u https://spa.example.com \
  -hl \
  -pls networkidle \
  -dwt 5000 \
  -jc -jsl \
  -d 4 \
  -fx \          # extract form elements
  -xhr \         # extract XHR/fetch calls
  -j \           # JSONL output
  -o spa_crawl.jsonl
```

### Scope-Controlled Crawl

```bash
# Only follow links on the exact FQDN
katana -u https://api.example.com -fs fqdn

# Custom in-scope regex (allow subdomains of example.com only)
katana -u https://example.com -cs ".*\.example\.com.*"

# Exclude specific out-of-scope paths
katana -u https://example.com \
  -cos ".*logout.*" \
  -cos ".*delete.*" \
  -cos ".*admin/destroy.*"

# No scope restriction (follow all external links too)
katana -u https://example.com -ns
```

### Known Files and Sitemap Crawling

```bash
# Crawl robots.txt and sitemap.xml (depth must be >= 3)
katana -u https://example.com -kf all -d 5

# Only robots.txt
katana -u https://example.com -kf robotstxt

# Only sitemap
katana -u https://example.com -kf sitemapxml
```

## Integration with ProjectDiscovery Tools

### Full Bug Bounty Pipeline

```bash
# Discovery → Probing → Crawling → Vulnerability scanning
subfinder -d target.com -all -silent | \
  httpx -silent -mc 200,301,302,403 | \
  katana -jc -d 4 -rl 150 -silent | \
  nuclei -t ~/nuclei-templates/http/ -severity medium,high,critical -o findings.txt
```

### Filter for Specific Vulnerability Classes

```bash
# Find all URLs with query parameters (for SQLi/XSS testing)
katana -u https://example.com -d 5 -jc | grep "?" | tee parameterized.txt

# Pipe into dalfox for XSS scanning
cat parameterized.txt | dalfox pipe -o xss_results.txt

# Pipe into sqlmap
cat parameterized.txt | head -1 | xargs -I{} sqlmap -u {} --batch --level 2
```

### Custom Field Extraction for Wordlist Building

```bash
# Build directory wordlist from crawl
katana -u https://example.com -d 5 -f dir | sort -u > dirs.txt

# Build parameter wordlist
katana -u https://example.com -d 5 -f key | sort -u > params.txt

# Use in ffuf
ffuf -u https://example.com/FUZZ -w dirs.txt -mc 200,301,302,403
ffuf -u "https://example.com/api?FUZZ=test" -w params.txt -mc 200
```

## Advanced Techniques

### Resuming Long Crawls

```bash
# Save state and resume
katana -u https://large-site.com -d 10 -ct 30m -resume state.yaml

# Resume from previous state
katana -resume state.yaml
```

### Technology Detection

```bash
# Detect technologies while crawling
katana -u https://example.com -td -j | jq '.technologies[]'

# Filter for sites using specific tech
katana -list hosts.txt -td -j | jq 'select(.technologies[] | contains("WordPress")) | .endpoint'
```

### Rate Limit Bypass Techniques

```bash
# Slow crawl to avoid WAF/rate limits
katana -u https://example.com -rl 10 -rd 500 -c 2

# Rotate through proxies
katana -u https://example.com -proxy http://proxy1:8080
# (proxify from ProjectDiscovery handles proxy rotation)
cat urls.txt | proxify | katana
```

## Troubleshooting

| Issue | Fix |
|---|---|
| Headless fails to start | Install Chrome: `apt install google-chrome-stable`; use `-nos` in Docker |
| Very few results on SPA | Switch to `-hl` headless mode with `-pls networkidle` |
| Crawl goes out of scope | Check `-fs` setting; add `-cos` patterns for exclusion |
| Chrome crashes under load | Reduce concurrency: `-c 3 -p 3`; increase Docker memory limit |
| Results missing JS endpoints | Add `-jc` flag; for deep coverage add `-jsl` |
| Rate limit hit (403/429) | Reduce `-rl` and add `-rd` delay between requests |
| Auth session expires | Reduce crawl scope/depth; use shorter `-ct` duration with fresh cookie |
| JSONL output malformed | Ensure `-j` flag is set; pipe to `jq '.'` to validate |
| `CGO_ENABLED=1` build error | Install `gcc`: `apt install build-essential`; then re-run go install |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
