---
name: subfinder
description: >
  Use and operate Subfinder — a fast passive subdomain enumeration tool by ProjectDiscovery that
  queries dozens of passive DNS data sources simultaneously. Use when performing subdomain
  discovery during recon, configuring API keys for maximum source coverage, integrating passive
  enumeration into recon pipelines with httpx and nuclei, or chaining with active tools for
  full-spectrum recon-to-exploit workflows. Covers installation, all flags, provider-config.yaml
  setup with all supported API key providers, output formats, recursive enumeration, rate limiting,
  silent mode, stdin/stdout piping, and complete pipeline integration.
  GitHub: https://github.com/projectdiscovery/subfinder (13.4k stars).
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/projectdiscovery/subfinder
  language: Go
---

# subfinder Agent Skill

## When to Use This Skill

Use this skill when:
- Performing passive subdomain enumeration during external recon (no direct target interaction)
- Configuring Subfinder API keys for maximum source coverage across providers
- Building automated recon pipelines: subfinder → httpx → nuclei
- Enumerating subdomains at scale across multiple domains from a list
- Integrating Subfinder with ProjectDiscovery's broader tool ecosystem (uncover, katana, nuclei)
- Comparing passive enumeration results with active brute-forcing (Gobuster dns mode, amass)

## What Subfinder Does

Subfinder queries passive DNS intelligence sources — certificate transparency logs, search engines, threat intel platforms, DNS archives — without sending a single packet to the target. It aggregates results from 40+ data sources simultaneously, deduplicates, and streams to stdout or a file. Because it is entirely passive, it leaves no trace on the target infrastructure and is safe to run without authorization concerns on the enumeration phase itself. It requires Go 1.24+ and is part of the ProjectDiscovery open-source toolkit.

## Installation

### Go Install (recommended — always latest)
```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
# Binary lands in $GOPATH/bin/subfinder
export PATH=$PATH:$(go env GOPATH)/bin
subfinder -version
```

### Pre-built Releases
```bash
# Download from https://github.com/projectdiscovery/subfinder/releases
wget https://github.com/projectdiscovery/subfinder/releases/latest/download/subfinder_linux_amd64.zip
unzip subfinder_linux_amd64.zip
sudo mv subfinder /usr/local/bin/
subfinder -version
```

### Docker
```bash
docker pull projectdiscovery/subfinder:latest
docker run --rm projectdiscovery/subfinder:latest -d example.com -silent

# With provider config mounted
docker run --rm \
  -v $HOME/.config/subfinder:/root/.config/subfinder \
  projectdiscovery/subfinder:latest \
  -d example.com -silent
```

### Apt / Homebrew
```bash
# Kali / via pdtm (ProjectDiscovery Tool Manager)
go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest
pdtm -install subfinder

# macOS Homebrew
brew install subfinder
```

## Provider Configuration

Subfinder's value multiplies dramatically with API keys. Without keys, only ~15 sources work. With a full config, 40+ sources are active.

### Config File Location
```
Linux/macOS: ~/.config/subfinder/provider-config.yaml
Windows:     %USERPROFILE%\AppData\Roaming\subfinder\provider-config.yaml
```

### Initialize Config
```bash
# Run once to create default config files
subfinder -d example.com
# Creates ~/.config/subfinder/config.yaml and provider-config.yaml
```

### provider-config.yaml — Full Structure
```yaml
binaryedge:
  - your-binaryedge-api-key
bufferover:
  - your-bufferover-api-key
c99:
  - your-c99-api-key
censys:
  - your-censys-api-id:your-censys-api-secret   # format: ID:SECRET
certspotter:
  - your-certspotter-api-key
chaos:
  - your-chaos-api-key                           # ProjectDiscovery Chaos
chinaz:
  - your-chinaz-api-key
dnsdb:
  - your-dnsdb-api-key
fofa:
  - your-fofa-email:your-fofa-api-key            # format: EMAIL:KEY
fullhunt:
  - your-fullhunt-api-key
github:
  - your-github-personal-access-token            # free, just needs public scope
gitlab:
  - your-gitlab-personal-access-token
hunter:
  - your-hunter-api-key
intelx:
  - your-intelx-api-key
leakix:
  - your-leakix-api-key
netlas:
  - your-netlas-api-key
passivetotal:
  - your-passivetotal-api-key                    # RiskIQ — username:key format
quake:
  - your-quake-api-key
robtex:
  - your-robtex-api-key
securitytrails:
  - your-securitytrails-api-key                  # free tier available
shodan:
  - your-shodan-api-key                          # free tier available
shodan:
  - SHODAN_KEY
spyse:
  - your-spyse-api-key
urlscan:
  - your-urlscan-api-key                         # free tier available
virustotal:
  - your-virustotal-api-key                      # free tier available (500 req/day)
whoisxmlapi:
  - your-whoisxmlapi-key
zoomeye:
  - your-zoomeye-api-key                         # format: USERNAME:PASSWORD
zoomeyeapi:
  - your-zoomeye-api-key
```

### Priority API Keys to Get First (free tiers available)
| Provider | Source Value | Free Tier | Get Key |
|---|---|---|---|
| GitHub | Excellent (code search) | Yes | github.com/settings/tokens |
| VirusTotal | High (passive DNS) | 500/day | virustotal.com |
| SecurityTrails | High (DNS history) | 50/month | securitytrails.com |
| Shodan | High (internet scanner) | Yes (limited) | account.shodan.io |
| Censys | High (internet scanner) | Yes | search.censys.io/account |
| Chaos | Very high (PD dataset) | Invite | chaos.projectdiscovery.io |
| URLScan | Medium | Yes | urlscan.io/user/settings |

```bash
# Verify your config works — list active sources
subfinder -ls

# Verify against a known domain
subfinder -d hackerone.com -v
```

## Complete Flag Reference

### Input Flags
```
-d, -domain string[]    Single domain or comma-separated domains
-dL, -list string       File containing domains (one per line)
```

### Source Selection Flags
```
-s, -sources string[]         Specific sources to use (-s crtsh,github,virustotal)
-recursive                    Use only sources supporting recursive subdomain lookup
-all                          Use ALL available sources (slow, max coverage)
-es, -exclude-sources string[]  Sources to exclude (-es alienvault,threatcrowd)
-ls, -list-sources            List all available sources and exit
```

### Output Flags
```
-o, -output string      Write output to file (one subdomain per line)
-oJ, -json              Write JSON lines output (JSONL format)
-oD, -output-dir string Directory for output when using -dL (one file per domain)
-cs, -collect-sources   Include source names in output (requires -oJ)
-oI, -ip                Include resolved IP addresses (-active only)
```

### Filter Flags
```
-m, -match string[]     Match subdomains containing this string/pattern
-f, -filter string[]    Filter OUT subdomains containing this string/pattern
```

### Rate Limiting Flags
```
-rl, -rate-limit int    Max HTTP requests per second (global)
-rls value              Per-provider rate limits: "hackertarget=10/s,shodan=15/s"
-t int                  Goroutines for resolving (default 10, -active only)
```

### Configuration Flags
```
-config string          Config file path (default: ~/.config/subfinder/config.yaml)
-pc, -provider-config   Provider config file (default: ~/.config/subfinder/provider-config.yaml)
-r string[]             Custom resolvers (comma-separated IPs)
-rL, -rlist string      File containing resolver IPs
-nW, -active            Show only active (resolving) subdomains
-proxy string           HTTP proxy (http://127.0.0.1:8080)
-ei, -exclude-ip        Exclude IP addresses from domain output
```

### Debug / Control Flags
```
-silent             Output only subdomains (no banner/metadata) — best for piping
-v                  Verbose output (show source tags, debug info)
-nc, -no-color      Disable color output
-version            Show version
-up, -update        Update subfinder to latest version
-duc, -disable-update-check  Disable auto-update check
```

### Timeout Flags
```
-timeout int       Seconds before a source times out (default 30)
-max-time int      Total enumeration time limit in minutes (default 10)
```

## Basic Usage Examples

```bash
# Single domain — default sources
subfinder -d example.com

# Silent mode (clean output for piping)
subfinder -d example.com -silent

# Save to file
subfinder -d example.com -o subs.txt

# JSON output with source attribution
subfinder -d example.com -oJ -cs -o subs.json

# Multiple domains
subfinder -d example.com,example.org,example.net -silent

# From domain list file
subfinder -dL domains.txt -silent -o all-subs.txt

# Output per-domain files to directory
subfinder -dL domains.txt -oD ./results/

# Use all sources (maximum coverage, slow)
subfinder -d example.com -all -silent

# Only use specific fast sources
subfinder -d example.com -s crtsh,certspotter,hackertarget,bufferover -silent

# Exclude noisy sources
subfinder -d example.com -es alienvault,threatcrowd -silent

# Recursive enumeration (finds sub.sub.example.com patterns)
subfinder -d example.com -recursive -silent

# Active subdomains only (resolves each)
subfinder -d example.com -nW -silent
```

## Output Formats

### Plain text (default)
```bash
subfinder -d example.com -o subs.txt
# Output: one subdomain per line
# api.example.com
# mail.example.com
# dev.example.com
```

### JSON Lines (-oJ)
```bash
subfinder -d example.com -oJ -cs -o subs.jsonl
# Each line: {"host":"api.example.com","source":["virustotal","crtsh"]}
```

### Parse JSONL for source analysis
```bash
cat subs.jsonl | jq -r '.host' | sort -u           # just hostnames
cat subs.jsonl | jq -r '"[\(.source[])] \(.host)"' # with sources
cat subs.jsonl | jq -r 'select(.source[] == "virustotal") | .host'  # filter by source
```

### With IP resolution
```bash
subfinder -d example.com -nW -oI -silent
# Output includes IP: api.example.com,1.2.3.4
```

## Pipeline Integration

### Subfinder → httpx (alive host probe)
```bash
# Basic alive check
subfinder -d example.com -silent | httpx -silent

# With status codes and titles
subfinder -d example.com -silent | httpx -status-code -title -tech-detect -silent

# Save live URLs
subfinder -d example.com -silent | httpx -silent -o live-hosts.txt

# Filter to HTTPS only
subfinder -d example.com -silent | httpx -silent -filter-string "https"
```

### Subfinder → httpx → nuclei (full recon-to-exploit)
```bash
# Complete pipeline: enum → alive check → vuln scan
subfinder -d example.com -silent | \
  httpx -silent | \
  nuclei -t /usr/share/nuclei-templates/ -severity critical,high -silent

# With rate limiting and output
subfinder -d example.com -silent | \
  httpx -silent -threads 50 | \
  nuclei -t /usr/share/nuclei-templates/ \
    -severity critical,high,medium \
    -rate-limit 50 \
    -o nuclei-findings.txt

# Specific template categories
subfinder -d example.com -silent | \
  httpx -silent | \
  nuclei -tags cve,misconfig,exposed-panels -o findings.txt
```

### Multi-domain recon pipeline
```bash
# Run across multiple targets from a list
subfinder -dL targets.txt -silent -oD ./subfinder-results/

# Aggregate and deduplicate
cat ./subfinder-results/*.txt | sort -u > all-subs.txt

# Probe all discovered subdomains
cat all-subs.txt | httpx -silent -threads 100 | \
  nuclei -t /usr/share/nuclei-templates/ -o all-findings.txt
```

### Subfinder → Gobuster (passive → active brute force)
```bash
# First passive, then active brute force for missed subs
subfinder -d example.com -silent -o passive-subs.txt
gobuster dns -d example.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -t 50 -q | awk '{print $2}' > active-subs.txt

# Combine and deduplicate
cat passive-subs.txt active-subs.txt | sort -u > all-discovered.txt
```

### Subdomain takeover check pipeline
```bash
# Find subdomains → check for takeover potential
subfinder -d example.com -silent | \
  httpx -silent -cname -o hosts-with-cnames.txt

# Use nuclei takeover templates
subfinder -d example.com -silent | \
  nuclei -t /usr/share/nuclei-templates/http/takeovers/ -o takeovers.txt
```

### Integration with dnsx
```bash
# Resolve subdomains and get A records
subfinder -d example.com -silent | \
  dnsx -silent -a -resp -o dns-records.txt

# Filter to specific IP ranges (e.g., cloud provider CIDRs)
subfinder -d example.com -silent | \
  dnsx -silent -a -resp | \
  grep -E "1\.2\.3\.|10\.0\."
```

## Advanced Techniques

### Rate Limiting for Bug Bounty (polite enumeration)
```bash
# Global rate limit — 10 req/sec total
subfinder -d example.com -rl 10 -silent

# Per-source limits (prevent API exhaustion)
subfinder -d example.com -rls "securitytrails=5/s,shodan=2/s,virustotal=4/s" -silent

# Combined: global + per-source
subfinder -d example.com -rl 20 -rls "github=10/s" -silent
```

### Recursive Enumeration
```bash
# Recursive mode — queries sub-subdomains
subfinder -d example.com -recursive -silent

# Manual recursive: use found subs as new input
subfinder -d example.com -silent > level1.txt
cat level1.txt | while read sub; do
  subfinder -d "$sub" -silent
done | sort -u > level2.txt
cat level1.txt level2.txt | sort -u > all-recursive.txt
```

### Custom Resolvers
```bash
# Use specific DNS resolvers
subfinder -d example.com -r 8.8.8.8,1.1.1.1,9.9.9.9 -silent

# From resolver file (use with large wordlists — dnsx style)
cat > resolvers.txt << 'EOF'
8.8.8.8
1.1.1.1
9.9.9.9
208.67.222.222
EOF
subfinder -d example.com -rL resolvers.txt -silent
```

### Scope Matching and Filtering
```bash
# Match only subdomains containing "api" or "dev"
subfinder -d example.com -m api,dev -silent

# Filter out CDN/third-party subdomains
subfinder -d example.com -f cdn,akamai,cloudfront -silent

# Combine match and filter
subfinder -d example.com -m admin,internal -f test,staging -silent
```

### Version Checking and Updates
```bash
subfinder -version
subfinder -up         # Update to latest
subfinder -duc        # Disable update check (useful in CI)
```

## Troubleshooting

**Few or no results returned**
→ Most sources need API keys. Run `subfinder -ls` to see which sources are active. Add keys to `~/.config/subfinder/provider-config.yaml`. Verify key validity by testing a well-known domain: `subfinder -d google.com -v`.

**"Error: API rate limit exceeded"**
→ Use `-rl` to reduce requests per second. For specific providers, use `-rls "provider=N/s"`. Check if free tier quota is exhausted.

**Docker: provider config not found**
→ Mount your config: `-v $HOME/.config/subfinder:/root/.config/subfinder`

**Output is empty with -nW flag**
→ `-nW` (active mode) resolves each subdomain and discards non-resolving ones. If your DNS resolver is unreliable, use `-r 8.8.8.8,1.1.1.1`.

**Timeout on large domain sets**
→ Increase `-max-time` (default 10 minutes). For large `-dL` lists, consider running batches and using `-oD` for per-domain output files to avoid losing progress.

**Duplicate subdomains in output**
→ Subfinder deduplicates by default. If seeing duplicates after piping, add `| sort -u` in the shell pipeline.

**"panic: runtime error" on startup**
→ Go version too old. Subfinder requires Go 1.24+. Update: `go install golang.org/dl/go1.24.0@latest && go1.24.0 download`
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
