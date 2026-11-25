---
name: feroxbuster
description: >
  Operate Feroxbuster — a fast, recursive content discovery tool written in Rust for
  brute-forcing files, directories, and endpoints against web servers. Use when performing
  web content enumeration, finding hidden paths, discovering API endpoints, or recursively
  walking directory structures. Covers installation, wordlists, extensions, filtering,
  recursion, rate limiting, output formats, auto-tune, scan resumption, and comparison
  with ffuf, gobuster, and dirsearch.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/epi052/feroxbuster
  language: Rust
---

# feroxbuster Agent Skill

## When to Use This Skill

Use this skill when:
- Brute-forcing directories and files on web servers during pentest/CTF
- Performing recursive content discovery (feroxbuster auto-recurses into found directories)
- Discovering API endpoints, backup files, configuration files, admin panels
- Needing high-speed content discovery with auto-tune to avoid rate-limiting
- Resuming interrupted scans against the same target
- Comparing tool choices: feroxbuster vs ffuf vs gobuster vs dirsearch

## What Feroxbuster Does

Feroxbuster (epi052/feroxbuster, ~6.7k GitHub stars) is a Rust-based content discovery tool
designed for speed and recursion. Unlike gobuster, feroxbuster automatically recurses into
discovered directories by default, making it ideal for deeply nested web applications. Its
async I/O architecture allows hundreds of concurrent requests while its auto-tune feature
dynamically adjusts throughput based on server response latency and error rates.

## Installation

### Cargo (Rust toolchain)
```bash
cargo install feroxbuster
# Binary lands in ~/.cargo/bin/feroxbuster
```

### apt (Kali/Debian)
```bash
sudo apt update && sudo apt install -y feroxbuster
```

### Homebrew (macOS)
```bash
brew install feroxbuster
```

### Docker
```bash
docker pull epi052/feroxbuster
docker run --init -it epi052/feroxbuster -u http://target.com \
  -w /wordlists/raft-large-directories.txt
# Mount local wordlists:
docker run --init -it -v ~/wordlists:/wordlists epi052/feroxbuster \
  -u http://target.com -w /wordlists/raft-large-directories.txt
```

### Pre-built Binary
```bash
curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh \
  | bash -s $HOME/.local/bin
```

## Core Concepts

### Recursive by Default
Feroxbuster automatically recurses into every directory it finds that returns a 2xx or 3xx
response. This means a scan of `/` will automatically spawn sub-scans of `/admin/`, `/api/`,
`/api/v1/`, etc., without manual intervention. Control depth with `-d`.

### Auto-Tune
The `--auto-tune` flag monitors the ratio of errors to successes and dynamically reduces the
request rate when the server starts struggling. This prevents killing slow targets while still
maximising speed on fast targets.

### Response Filtering Strategy
Rather than relying purely on status codes, feroxbuster filters based on:
- **Status codes**: `-C` (filter OUT), `-s` (filter IN — show only)
- **Response size**: `--filter-size` (filter exact byte count), `--filter-similar-size`
- **Word count**: `--filter-words`
- **Line count**: `--filter-lines`
- **Regex on response body**: `--filter-regex`

## CLI Reference

### Basic Usage
```bash
# Basic directory discovery
feroxbuster -u http://target.com

# Specify wordlist (critical — default is small)
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt

# HTTPS target (certificate errors ignored by default)
feroxbuster -u https://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt
```

### Extensions
```bash
# Common web extensions
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt \
  -x php,html,txt,bak,zip,sql,js,json

# API discovery
feroxbuster -u http://target.com/api \
  -w /usr/share/seclists/Discovery/Web-Content/api/objects.txt \
  -x json

# Backup files
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-words.txt \
  -x bak,backup,old,orig,save,swp,tmp,.DS_Store
```

### Status Code Filtering
```bash
# Filter OUT (hide) 404 and 403 responses
feroxbuster -u http://target.com -C 404,403

# Only SHOW 200 and 301 responses
feroxbuster -u http://target.com -s 200,301

# Common combo: hide 404, 400, 500 errors
feroxbuster -u http://target.com -C 404,400,500

# Soft 404 detection: filter by size
# First run to see what 404 looks like
feroxbuster -u http://target.com -C 404 --auto-tune
# If 404 returns 200 with fixed body: filter by that size
feroxbuster -u http://target.com -s 200 --filter-size 1234
```

### Response Size and Content Filtering
```bash
# Filter responses of exact size (soft 404 pages)
feroxbuster -u http://target.com --filter-size 1234

# Filter similar sizes (within N bytes)
feroxbuster -u http://target.com --filter-similar-size 1300

# Filter by word count
feroxbuster -u http://target.com --filter-words 42

# Filter by line count
feroxbuster -u http://target.com --filter-lines 10

# Filter by regex match in body
feroxbuster -u http://target.com --filter-regex "Not Found|Error 404"
```

### Recursion Control
```bash
# Disable recursion entirely (flat scan only)
feroxbuster -u http://target.com --no-recursion

# Limit recursion depth (default: 4)
feroxbuster -u http://target.com -d 2

# Only recurse into specific status codes
feroxbuster -u http://target.com --depth 3 -s 200,301,302,403
```

### Threading and Rate Limiting
```bash
# Set thread count (default: 50)
feroxbuster -u http://target.com -t 100

# Reduce threads for slow/fragile targets
feroxbuster -u http://target.com -t 10

# Rate limit: max requests per second
feroxbuster -u http://target.com --rate-limit 50

# Auto-tune: let feroxbuster adjust automatically
feroxbuster -u http://target.com --auto-tune

# Combined: tune + manual rate ceiling
feroxbuster -u http://target.com --auto-tune --rate-limit 100
```

### Output Options
```bash
# Write output to file (replays terminal output)
feroxbuster -u http://target.com -o results.txt

# JSON output (structured, for scripting)
feroxbuster -u http://target.com --json -o results.json

# Quiet mode (only show findings, no progress bar)
feroxbuster -u http://target.com -q

# Silent mode (only show URLs of successful finds)
feroxbuster -u http://target.com --silent

# No colour (for log files)
feroxbuster -u http://target.com --no-color -o clean.txt
```

### Resuming Scans
```bash
# Save scan state for resume
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
  --output scan_state.txt \
  --json

# Resume from a previous scan state file
feroxbuster --resume-from scan_state.json

# Auto-save state file (feroxbuster creates .ferox_resume.json by default on Ctrl+C)
# Simply Ctrl+C → feroxbuster writes state → resume with:
feroxbuster --resume-from .ferox_resume.json
```

### Proxy Support
```bash
# HTTP proxy (Burp Suite)
feroxbuster -u http://target.com -p http://127.0.0.1:8080

# SOCKS5 proxy
feroxbuster -u http://target.com -p socks5://127.0.0.1:1080

# Replay only interesting findings through proxy
feroxbuster -u http://target.com \
  --replay-proxy http://127.0.0.1:8080 \
  --replay-codes 200,201,204,301,302,307,401,403
```

### Headers and Authentication
```bash
# Custom headers
feroxbuster -u http://target.com \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "X-Custom-Header: value"

# Cookie-based auth
feroxbuster -u http://target.com \
  -H "Cookie: session=authenticated_token"

# HTTP Basic auth
feroxbuster -u http://target.com \
  --username admin --password password

# Custom user agent
feroxbuster -u http://target.com \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0)"
```

### Link Extraction and Word Collection
```bash
# Don't extract links from responses (faster, less recursive noise)
feroxbuster -u http://target.com --dont-extract-links

# Collect words from responses to auto-build a target-specific wordlist
feroxbuster -u http://target.com --collect-words \
  -o collected_words.txt

# Collect extensions observed in responses
feroxbuster -u http://target.com --collect-extensions
```

### Multiple Targets
```bash
# Scan multiple URLs from a file
feroxbuster --stdin -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
  < targets.txt

# Or pass via argument
cat targets.txt | feroxbuster --stdin \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

### Timeout and Connection Settings
```bash
# Per-request timeout (default: 7 seconds)
feroxbuster -u http://target.com --timeout 15

# Retry failed requests
feroxbuster -u http://target.com --retries 2

# Ignore SSL/TLS errors (self-signed certs)
feroxbuster -u https://target.com --insecure
```

## Common Workflows

### Standard Web App Discovery (OSCP/CTF)
```bash
# Phase 1: Fast directory scan
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
  -C 404 -d 2 -t 50 -o phase1_dirs.txt

# Phase 2: File extension scan on found directories
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt \
  -x php,html,txt,bak,zip,sql -C 404 -d 1 -o phase2_files.txt

# Phase 3: Recursive deep dive with large wordlist
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-large.txt \
  -C 404,400 --auto-tune -o phase3_deep.txt
```

### API Endpoint Discovery
```bash
feroxbuster -u http://target.com/api \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -x json -s 200,201,400,401,403 \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -C 404 -d 3
```

### Authenticated Application Scan
```bash
# Get session cookie from browser/Burp
feroxbuster -u http://target.com/dashboard \
  -H "Cookie: PHPSESSID=your_authenticated_session" \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
  -C 404,302 -d 3 --auto-tune
# Note: filter 302 if it redirects unauthenticated requests to /login
```

### Soft 404 Handling
```bash
# Step 1: Probe a known non-existent path to get 404 size
curl -si "http://target.com/definitely_not_real_$(date +%s)" | \
  grep -i "content-length"
# Returns: Content-Length: 1523

# Step 2: Filter that exact size
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
  -s 200 --filter-size 1523
```

### Post-Discovery Filtering Pipeline
```bash
# Parse JSON output to extract only 200 OK paths
cat results.json | jq -r 'select(.status==200) | .url' | sort -u > live_paths.txt

# Find interesting files in results
grep -iE "admin|backup|config|\.sql|\.zip|\.bak|login|upload" results.txt

# Extract directories for further targeted scanning
grep -E " 301 " results.txt | awk '{print $NF}' > found_dirs.txt
```

## Tool Comparison

| Feature | feroxbuster | ffuf | gobuster | dirsearch |
|---------|-------------|------|----------|-----------|
| Language | Rust | Go | Go | Python |
| Auto-recursion | Yes (default) | No (manual) | No | Yes (opt-in) |
| Auto-tune | Yes | No | No | No |
| Resume scans | Yes | No | No | Yes |
| Response filtering | Rich (size/words/lines/regex) | Good | Basic | Good |
| POST fuzzing | No | Yes | No | No |
| Speed | Very fast | Very fast | Fast | Moderate |
| Config file | Yes | Yes | No | No |
| Best for | Recursive dir enum | All-purpose fuzzing | Simple dir/DNS | Python workflow |

**When to use ffuf instead**: POST fuzzing, FUZZ in headers/body, vhost discovery, parameter
fuzzing — ffuf's `FUZZ` keyword approach is more flexible for non-path targets.

**When to use gobuster instead**: DNS subdomain bruteforce (`dns` mode), S3 bucket enumeration
(`s3` mode), very simple flat scans where recursion is not needed.

## Advanced Techniques

### Configuration File
```toml
# ~/.config/feroxbuster/ferox-config.toml
wordlist = "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt"
status_codes = [200, 204, 301, 302, 307, 308, 401, 403, 405]
threads = 50
depth = 4
timeout = 7
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) feroxbuster"
auto_tune = true
```

### Chaining with Nuclei for Vulnerability Detection
```bash
# Find all endpoints
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt \
  --silent -s 200,403 --json -o ferox.json

# Extract URLs → feed nuclei
cat ferox.json | jq -r '.url' > endpoints.txt
nuclei -l endpoints.txt -t /opt/nuclei-templates/ -severity medium,high,critical
```

### Building Target-Specific Wordlist
```bash
# Collect words from the application itself
feroxbuster -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  --collect-words -o /dev/null
# Words are saved to collected_words_TIMESTAMP.txt
# Use that wordlist for a deeper scan
feroxbuster -u http://target.com \
  -w collected_words_*.txt \
  -C 404 --auto-tune
```

## Integration with Other Tools

```bash
# nmap → feroxbuster pipeline
nmap -p 80,443,8080,8443 --open -T4 10.10.10.0/24 -oG - | \
  grep "80/open\|443/open\|8080/open" | \
  awk '{print "http://"$2}' | \
  feroxbuster --stdin \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

# AutoRecon already runs feroxbuster/gobuster; review its results at:
# results/TARGET/scans/_http_PORT/*.txt
```

## Troubleshooting

**Too many false positives (all paths return 200)**
```bash
# Target uses custom 404 pages returning 200 — filter by size
curl -s "http://target.com/fake_$(date +%s%N)" | wc -c
# Returns: 2048
feroxbuster -u http://target.com --filter-size 2048
```

**Scan kills the server / connection refused**
```bash
# Drastically reduce threads and add rate limit
feroxbuster -u http://target.com -t 5 --rate-limit 10 --auto-tune
```

**HTTPS SSL errors**
```bash
feroxbuster -u https://target.com --insecure
```

**Recursion spawning too many sub-scans**
```bash
# Limit depth and only recurse into successful finds
feroxbuster -u http://target.com -d 2 --no-recursion
# Or: run flat, identify interesting dirs manually, then recurse selectively
feroxbuster -u http://target.com/admin/ -d 3
```

**Resume not working**
```bash
# Ensure JSON output was used and state file exists
ls -la .ferox_resume.json
feroxbuster --resume-from .ferox_resume.json
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
