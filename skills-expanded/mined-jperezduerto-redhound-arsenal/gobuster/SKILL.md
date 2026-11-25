---
name: gobuster
description: >
  Use and operate Gobuster — a fast directory/file, DNS subdomain, virtual host, fuzzing, S3, and
  GCS brute-forcing tool written in Go. Use when enumerating web directories and files, discovering
  subdomains via DNS brute force, finding virtual hosts, fuzzing URL parameters, or testing cloud
  storage buckets. Covers all modes (dir, dns, vhost, fuzz, s3, gcs, tftp), global flags,
  performance tuning, authentication, proxy support, wildcard detection, wordlist selection with
  SecLists, output formats, and comparison with ffuf, feroxbuster, and dirsearch.
  GitHub: https://github.com/OJ/gobuster (13.6k stars).
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/OJ/gobuster
  language: Go
---

# gobuster Agent Skill

## When to Use This Skill

Use this skill when:
- Enumerating web directories, files, or API endpoints on a target (dir mode)
- Brute-forcing subdomains via DNS (dns mode)
- Discovering virtual hosts on a web server (vhost mode)
- Fuzzing URL parameters, headers, or POST body values (fuzz mode)
- Testing for exposed S3 buckets or Google Cloud Storage buckets (s3 / gcs mode)
- Comparing Gobuster to ffuf, feroxbuster, or dirsearch for the right tool selection
- Writing automation scripts that wrap Gobuster output

## What Gobuster Does

Gobuster is a Go-based brute-forcing tool that sends concurrent HTTP/DNS requests from a wordlist, reporting hits based on configurable response criteria (status codes, response length). Unlike recursive tools, it is intentionally non-recursive by default, making it extremely fast and predictable. It supports seven distinct modes, each with purpose-built flags, and can be run via Docker or installed as a single static binary.

## Installation

### Go Install (recommended — always latest)
```bash
go install github.com/OJ/gobuster/v3@latest
# Binary lands in $GOPATH/bin/gobuster (~$HOME/go/bin/gobuster)
export PATH=$PATH:$(go env GOPATH)/bin
gobuster version
```

### Apt (Kali / Debian/Ubuntu)
```bash
sudo apt update && sudo apt install gobuster
```

### Pre-built Releases
```bash
# Download from https://github.com/OJ/gobuster/releases
wget https://github.com/OJ/gobuster/releases/latest/download/gobuster_Linux_x86_64.tar.gz
tar -xzf gobuster_Linux_x86_64.tar.gz
sudo mv gobuster /usr/local/bin/
```

### Docker
```bash
docker pull ghcr.io/oj/gobuster:latest
docker run --rm -it ghcr.io/oj/gobuster:latest dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt
```

## Global Flags (apply to all modes)

```
-t, --threads int        Number of concurrent threads (default 10)
-o, --output string      Output file path (results written line-by-line)
-q, --quiet              Quiet mode — no banner, less output
-v, --verbose            Verbose output (show all attempts)
    --no-progress        Disable progress display
    --delay duration     Delay between requests (e.g. 100ms, 1s)
    --timeout duration   HTTP timeout (default 10s)
-z, --no-error           Suppress errors (useful when many 404/connection resets)
    --debug              Debug output (prints raw requests)
```

## dir Mode — Directory and File Enumeration

The most common mode. Sends GET requests for each wordlist entry, reports hits by status code.

### Basic Usage
```bash
gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt
```

### Essential dir Flags
```
-u, --url string               Target URL (required)
-w, --wordlist string          Wordlist path (required, or - for stdin)
-x, --extensions string        File extensions to append (comma-separated)
-s, --status-codes string      Allowed status codes (default 200-299,301,302,307,401,403,405,500)
    --status-codes-blacklist   Status codes to exclude (overrides -s if set)
-b, --status-codes-blacklist   Shorthand for blacklist
-l, --add-slash                Append / to each request
    --discover-backup          Append backup extensions (.bak, .old, ~, .swp, etc.)
-r, --follow-redirect          Follow HTTP redirects
-e, --expanded                 Print full URL in output
-c, --cookies string           Cookie string (e.g. "session=abc123; token=xyz")
-H, --headers stringArray      Custom headers (repeatable: -H "X-Api-Key: abc" -H "Host: internal")
-a, --useragent string         Custom User-Agent string
-U, --username string          HTTP basic auth username
-P, --password string          HTTP basic auth password
-p, --proxy string             Proxy URL (http://127.0.0.1:8080)
    --random-agent             Use a random User-Agent from built-in list
    --exclude-length string    Exclude responses by length (ranges: 100,200-300,500)
    --force-wildcard           Force enumeration even if wildcard detected
-k, --no-tls-validation        Skip TLS certificate verification
    --client-cert-p12 string   mTLS: PKCS12 certificate file
    --client-cert-p12-password Password for P12 cert
    --wordlist-offset int      Skip first N lines of wordlist
```

### dir Examples
```bash
# Basic directory enum with common extensions
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt \
  -x php,html,js,txt -t 50

# PHP app — focus on PHP, backup files
gobuster dir -u https://target.com \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,php.bak,php.old,php~ -t 40 -o dir-results.txt

# Admin panel hunting — accept 200,301,302,403
gobuster dir -u https://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -s 200,301,302,403 -t 30

# API endpoint discovery
gobuster dir -u https://api.target.com/v1 \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -x json -H "Content-Type: application/json" -t 30

# Behind auth — inject cookie
gobuster dir -u https://target.com/admin \
  -w /usr/share/wordlists/dirb/common.txt \
  -c "PHPSESSID=abc123def456" -t 20

# Through Burp proxy — inspect traffic
gobuster dir -u https://target.com -w common.txt -p http://127.0.0.1:8080 -k

# Filter false positives by length
gobuster dir -u https://target.com -w common.txt --exclude-length 1234,5678

# Backup file discovery
gobuster dir -u https://target.com -w common.txt --discover-backup
```

## dns Mode — Subdomain Brute Forcing

Resolves DNS entries for each wordlist word prepended to the domain.

### Essential dns Flags
```
-d, --domain string      Target domain (required)
-w, --wordlist string    Wordlist (required)
-r, --resolver string    Custom DNS resolver (default: system — e.g. 8.8.8.8:53)
    --show-cname         Show CNAME records (cannot use with -i)
-i, --show-ips           Show IP addresses of resolved subdomains
    --no-fqdn            Do not automatically add trailing dot to DNS queries
    --wildcard-forced    Force enumeration even if wildcard DNS detected
```

### dns Examples
```bash
# Basic subdomain enum
gobuster dns -d target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Show IP addresses
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -i -t 50

# Use custom DNS resolver (bypass split-horizon DNS)
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -r 8.8.8.8:53 -t 50

# Large wordlist for thorough enum
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
  -t 100 -o dns-results.txt

# Show CNAME (useful for subdomain takeover detection)
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  --show-cname -t 30
```

**Wildcard Detection**: If the domain resolves any random subdomain (wildcard DNS), gobuster warns and stops by default. Use `--wildcard-forced` to override. Check manually: `dig randomxyz12345.target.com`.

## vhost Mode — Virtual Host Discovery

Fuzzes the `Host` header to find virtual hosts that share an IP. Useful when multiple sites are hosted on one server.

### Essential vhost Flags
```
-u, --url string         Target URL/IP (required)
-w, --wordlist string    Wordlist (required)
    --append-domain      Append base domain to each word (e.g. word → word.target.com)
    --domain string      Base domain to append when --append-domain is used
    --exclude-length     Exclude responses matching this length
-r, --follow-redirect    Follow redirects
```

### vhost Examples
```bash
# Basic vhost discovery (append-domain is critical)
gobuster vhost -u http://10.10.10.100 \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  --append-domain -H "Host: FUZZ.target.com"

# With domain specified
gobuster vhost -u https://10.10.10.100 \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  --append-domain --domain target.com -k -t 30

# Filter by response length to remove false positives
gobuster vhost -u http://10.10.10.100 \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  --append-domain --exclude-length 612 -t 40
```

## fuzz Mode — Parameter and Value Fuzzing

Replaces the keyword `FUZZ` anywhere in the request (URL, headers, POST body).

### Essential fuzz Flags
```
-u, --url string         URL with FUZZ placeholder (required)
-w, --wordlist string    Wordlist (required)
-b, --body string        POST body with FUZZ placeholder
-H, --headers            Header with FUZZ placeholder
    --exclude-length     Exclude by response length
```

### fuzz Examples
```bash
# URL parameter fuzzing
gobuster fuzz -u "https://target.com/page?id=FUZZ" \
  -w /usr/share/seclists/Fuzzing/Integers/Integers.txt \
  --exclude-length 0 -t 30

# POST body fuzzing (password spraying / credential stuffing)
gobuster fuzz -u https://target.com/login \
  -w /usr/share/wordlists/rockyou.txt \
  -b "username=admin&password=FUZZ" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --exclude-length 1234 -t 10

# Header fuzzing (finding valid X-Forwarded-For values, etc.)
gobuster fuzz -u https://target.com/admin \
  -w /usr/share/seclists/Fuzzing/IPs.txt \
  -H "X-Forwarded-For: FUZZ" --exclude-length 403body -t 20

# Path traversal fuzzing
gobuster fuzz -u "https://target.com/file?path=FUZZ" \
  -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -t 20
```

## s3 Mode — S3 Bucket Enumeration

Tests for the existence of public S3 buckets by name.
```bash
# Basic S3 enum
gobuster s3 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# With debug output (see AWS responses)
gobuster s3 -w bucket-names.txt --debug -t 20

# Company-specific naming patterns
gobuster s3 -w company-buckets.txt -v -o s3-results.txt

# Typical wordlist pattern: generate from company name permutations
# target, target-backup, target-prod, target-dev, target-assets, etc.
```

## gcs Mode — Google Cloud Storage Bucket Enumeration

```bash
gobuster gcs -w bucket-names.txt -t 20
gobuster gcs -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --debug
```

## tftp Mode — TFTP File Enumeration

Tests for readable files on a TFTP server (common in network devices, IoT).
```bash
gobuster tftp -s 10.10.10.100 -w /usr/share/seclists/Discovery/TFTP/tftp.txt
gobuster tftp -s 192.168.1.1 -w cisco-configs.txt -t 10
```

## Wordlist Selection (SecLists)

```bash
# Install SecLists
sudo apt install seclists
# or: git clone https://github.com/danielmiessler/SecLists /usr/share/seclists

# Recommended wordlists by use case:
# Quick web directory enum
/usr/share/seclists/Discovery/Web-Content/common.txt                    # ~4.7k entries
/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt   # ~30k entries

# Thorough web (slow)
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt            # ~220k entries

# Extensions
/usr/share/seclists/Discovery/Web-Content/web-extensions.txt

# API discovery
/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
/usr/share/seclists/Discovery/Web-Content/api/objects.txt

# DNS subdomain brute force
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt       # fast
/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt      # balanced
/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt     # thorough

# DNS with mutations
/usr/share/seclists/Discovery/DNS/dns-Jhaddix.txt                       # 1.9M entries
```

## Performance Tuning

```bash
# Threads: balance speed vs. rate limiting (start at 10, increase to 50-100 for stable targets)
-t 50         # 50 concurrent threads

# Delay: add artificial delay to avoid WAF/IDS triggering
--delay 100ms

# Timeout: increase for slow targets
--timeout 30s

# Combine: fast but polite
gobuster dir -u https://target.com -w common.txt -t 30 --delay 50ms --timeout 20s

# Maximum aggressive (for CTF/lab only)
gobuster dir -u https://target.com -w big.txt -t 200 --timeout 5s
```

## Common Workflows

### Web App Recon Chain
```bash
# 1. Quick common path discovery
gobuster dir -u https://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x php,asp,aspx,html,txt -t 40 -o quick-dirs.txt

# 2. Deep recursive-style: run against each found directory
while IFS= read -r dir; do
  url=$(echo "$dir" | awk '{print $1}')
  gobuster dir -u "$url" -w common.txt -x php,txt -t 20 -q >> deep-dirs.txt
done < <(grep "Status: 200\|Status: 301" quick-dirs.txt)

# 3. Backup file sweep on interesting paths
gobuster dir -u https://target.com -w found-paths.txt --discover-backup -t 20
```

### Subdomain to VHost Full Chain
```bash
# 1. DNS brute force
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -i -t 50 -o dns-subs.txt

# 2. VHost discovery on main IP
gobuster vhost -u https://10.10.10.100 \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  --append-domain --domain target.com -k --exclude-length 612 -t 30 -o vhosts.txt
```

## Gobuster vs. Similar Tools

| Feature | Gobuster | ffuf | feroxbuster | dirsearch |
|---|---|---|---|---|
| Language | Go | Go | Rust | Python |
| Recursion | No (manual) | Yes (-recursion) | Yes (built-in) | Yes |
| Fuzzing | fuzz mode | Core feature | Limited | Limited |
| DNS mode | Yes | No | No | No |
| VHost mode | Yes | Yes (-H Host:) | No | No |
| S3/GCS/TFTP | Yes | No | No | No |
| Speed | Fast | Fastest | Very Fast | Moderate |
| Output formats | txt | txt/json/csv/html | txt/json/md | plain/json/xml |
| Best for | Multi-mode versatility | Advanced fuzzing | Recursive web enum | Quick web sweeps |

## Integration with Other Tools

```bash
# Pipe gobuster DNS results into httpx for alive check
gobuster dns -d target.com -w subdomains.txt -i -q | \
  awk '{print $2}' | httpx -silent -o live-hosts.txt

# Feed gobuster dir results into nuclei for vuln scanning
gobuster dir -u https://target.com -w common.txt -q | \
  grep "Status: 200" | awk '{print $1}' | \
  nuclei -t /usr/share/nuclei-templates/ -o nuclei-findings.txt

# Use with nmap — scan discovered subdomains
gobuster dns -d target.com -w subdomains.txt -i -q | \
  awk '{print $3}' | sort -u | nmap -iL - -sV -p 80,443,8080,8443
```

## Troubleshooting

**Wildcard DNS detected — gobuster stops**
→ `--wildcard-forced` to override. Validate manually: `dig random12345.target.com`. If it resolves, filtering by `--exclude-length` matching the wildcard response is the clean fix.

**Too many false positives in dir mode**
→ Identify the false positive response length, add `--exclude-length <len>`. Check: `curl -o /dev/null -sw "%{size_download}" https://target.com/randomxyz123`

**Rate limited / 429 responses**
→ Reduce threads (`-t 5`), add delay (`--delay 500ms`), rotate User-Agent (`--random-agent`), use a proxy with rotation.

**TLS certificate errors**
→ Add `-k` flag to skip TLS verification for self-signed certs.

**`Error: error on running gobuster: unable to connect to ... no such host`**
→ DNS resolution failure. Check connectivity, try `-r 8.8.8.8:53`, verify target is reachable.

**vhost mode returns everything (all same length)**
→ Server returns same page regardless of Host header. Use `--exclude-length` matching the default response size. Try filtering by response body content instead (pipe through grep).
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
