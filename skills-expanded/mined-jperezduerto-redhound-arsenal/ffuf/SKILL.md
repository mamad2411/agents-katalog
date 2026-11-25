---
name: ffuf
description: >
  Operate ffuf (Fuzz Faster U Fool) — an extremely fast web fuzzer written in Go. Use when
  the user needs to brute-force web directories, discover virtual hosts, fuzz GET/POST
  parameters, headers, or subdomains, or when the user asks about ffuf, directory brute
  forcing, web fuzzing, or content discovery. Covers installation, all filtering and matching
  flags, multiple wordlist positions (FUZZ, custom keywords), VHOST discovery, parameter
  fuzzing, recursion, output formats, rate limiting, authentication (cookies, headers),
  custom wordlists, and integration with SecLists.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/ffuf/ffuf
---

# ffuf Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to enumerate web directories, files, or endpoints
- The user asks about ffuf or web content discovery / directory brute forcing
- Fuzzing GET/POST parameters, headers, or cookies on a web application
- Discovering virtual hosts (vhosts) or subdomains via Host header fuzzing
- Running multi-wordlist fuzzing attacks with custom keyword positions
- Filtering large amounts of fuzzing results to isolate interesting responses

## What ffuf Does

ffuf is a high-performance web fuzzer written in Go that replaces the `FUZZ` keyword (or any custom keyword) in URLs, headers, POST bodies, or any other part of an HTTP request with words from a wordlist. It supports concurrent requests, multiple simultaneous wordlists, and fine-grained result filtering by status code, response size, word count, line count, or regex. ffuf is the de-facto standard fuzzer for directory brute forcing, VHOST discovery, and parameter fuzzing in bug bounty and penetration testing workflows.

## Installation

### Go Install (recommended)

```bash
# Requires Go 1.16+
go install github.com/ffuf/ffuf/v2@latest

# Verify
ffuf -V
```

### Package Managers

```bash
# macOS
brew install ffuf

# Kali Linux / Debian
apt install ffuf

# Arch
pacman -S ffuf
```

### Binary Releases

```bash
wget https://github.com/ffuf/ffuf/releases/latest/download/ffuf_*_linux_amd64.tar.gz
tar -xzf ffuf_*_linux_amd64.tar.gz
chmod +x ffuf && mv ffuf /usr/local/bin/
```

### Build from Source

```bash
git clone https://github.com/ffuf/ffuf
cd ffuf
go get && go build
./ffuf -V
```

## Core Concepts

### FUZZ Keyword and Custom Keywords

The `FUZZ` keyword is the default placeholder. Place it anywhere in the request — URL path, query parameter name or value, header value, POST body — and ffuf substitutes each wordlist entry in its place.

Custom keywords are defined using the `-w wordlist:KEYWORD` syntax, allowing multiple simultaneous wordlists with distinct positions.

```bash
# Default FUZZ in URL path
ffuf -w wordlist.txt -u https://example.com/FUZZ

# Custom keyword W1 in URL
ffuf -w wordlist.txt:W1 -u https://example.com/W1

# Multiple keywords in one request
ffuf -w params.txt:PARAM -w values.txt:VALUE -u "https://example.com/?PARAM=VALUE"
```

### Wordlist Modes (`-mode`)

When multiple wordlists are used, `-mode` controls how their entries are combined:

| Mode | Behavior |
|---|---|
| `clusterbomb` (default) | Every combination of all wordlists (cartesian product) |
| `pitchfork` | Parallel iteration — entry 1 of W1 with entry 1 of W2, etc. |
| `sniper` | Insert each wordlist into each position in turn |

## CLI Reference

### Core Flags

```
-u <URL>              Target URL with FUZZ placeholder(s)
-w <wordlist[:KEY]>   Wordlist path and optional keyword (default key: FUZZ)
                      Use multiple -w flags for multiple wordlists
-X <method>           HTTP method (default: GET; use POST, PUT, etc.)
-d <data>             POST request body data (use with -X POST)
-H <header>           Add/override HTTP header (repeatable)
-b <cookies>          Cookie string (e.g., "NAME=VALUE; NAME2=VALUE2")
-r                    Follow HTTP redirects
-recursion            Enable recursive fuzzing (URL must end in FUZZ)
-recursion-depth <n>  Max recursion depth (default: 0 = unlimited)
-recursion-strategy <s>  "default" (redirect-based) or "greedy" (all matches)
-e <extensions>       Comma-separated extensions to append (e.g., php,html,txt)
-mode <mode>          Multi-wordlist mode: clusterbomb, pitchfork, sniper
-t <n>                Concurrent threads (default: 40)
-p <delay>            Delay between requests: "0.1" or "0.1-2.0" (random range)
-rate <n>             Max requests per second (0 = unlimited)
-timeout <n>          HTTP timeout in seconds (default: 10)
-maxtime <n>          Max total runtime in seconds
-maxtime-job <n>      Max runtime per job in seconds (useful with recursion)
-x <proxy>            HTTP proxy URL (e.g., http://127.0.0.1:8080)
-replay-proxy <proxy> Replay matched requests through a proxy (e.g., Burp)
-k                    TLS certificate verification disabled
-c                    Colorized output
-v                    Verbose mode (show request/response details)
-s                    Silent mode (suppress progress output — results only)
-ic                   Ignore wordlist comments (lines starting with #)
-json                 JSON Lines output to stdout
-noninteractive       Disable interactive mode (for scripting)
-V                    Print version and exit
```

### Matcher Options (what to KEEP)

```
-mc <codes>   Match HTTP status codes (default: 200-299,301,302,307,401,403,405,500)
              Use "all" to match every response
-ml <n>       Match responses with exactly N lines
-mr <regex>   Match responses where body matches regex
-ms <n>       Match responses with exactly N bytes
-mw <n>       Match responses with exactly N words
-mt <expr>    Match by response time: ">100" or "<100" (ms to first byte)
-mmode <op>   Matcher logic: "or" (default) or "and" (all matchers must match)
```

### Filter Options (what to DROP)

```
-fc <codes>   Filter HTTP status codes (comma-separated, ranges supported)
-fl <n>       Filter responses with exactly N lines (or comma-separated list)
-fr <regex>   Filter responses where body matches regex
-fs <n>       Filter responses with exactly N bytes (comma-separated list/ranges)
-fw <n>       Filter responses with exactly N words (comma-separated list/ranges)
-ft <expr>    Filter by response time: ">100" or "<100"
-fmode <op>   Filter logic: "or" (default) or "and" (all filters must match)
```

### Output Options

```
-o <file>     Write output to file
-of <format>  Output format: json (default), ejson, html, md, csv, ecsv, all
-od <dir>     Directory to store per-match response files
-or           Don't create output file if no results found
-json         JSON Lines to stdout (in addition to or instead of -o)
```

### Authentication Options

```
-b "NAME=VALUE; NAME2=VALUE2"    Cookie string (copy-as-curl format)
-H "Authorization: Bearer TOKEN" Authorization header
-H "Cookie: session=abc123"      Cookie via header (alternative to -b)
-cc <cert.pem>                   Client certificate file
-ck <key.pem>                    Client key file
-u http://user:pass@example.com  HTTP Basic Auth via URL
```

## Directory and File Brute Forcing

```bash
# Basic directory discovery
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u https://example.com/FUZZ -c

# With file extension appending
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt \
  -u https://example.com/FUZZ \
  -e .php,.html,.txt,.bak,.old \
  -mc 200,301,302,403 -c

# Filter by response size (hide default 404 page)
# First, check 404 size: curl -s https://example.com/nonexistentfile | wc -c
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u https://example.com/FUZZ \
  -fs 1234   # size of the 404 page

# Recursive directory brute force (max 2 levels deep)
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u https://example.com/FUZZ \
  -recursion -recursion-depth 2 \
  -maxtime-job 60 \
  -mc 200,301,302 -c

# Greedy recursion (recurse on all matches, not just redirects)
ffuf -w /usr/share/wordlists/dirb/common.txt \
  -u https://example.com/FUZZ \
  -recursion -recursion-strategy greedy \
  -mc 200,301,302,403 -c
```

### Recommended SecLists Wordlists

| Use Case | Wordlist Path |
|---|---|
| General directory discovery | `Discovery/Web-Content/common.txt` |
| Comprehensive files | `Discovery/Web-Content/raft-large-files.txt` |
| Comprehensive directories | `Discovery/Web-Content/raft-large-directories.txt` |
| Medium balanced | `Discovery/Web-Content/directory-list-2.3-medium.txt` |
| API endpoints | `Discovery/Web-Content/api/objects.txt` |
| Backup files | `Discovery/Web-Content/raft-large-extensions.txt` |
| Parameter names | `Discovery/Web-Content/burp-parameter-names.txt` |
| Subdomains | `Discovery/DNS/subdomains-top1million-5000.txt` |

## VHOST Discovery

VHOST discovery works by fuzzing the `Host:` header. Responses that differ from the default (wrong vhost) response indicate a valid virtual host.

```bash
# Step 1: Establish default response size (baseline)
curl -s -o /dev/null -w "%{size_download}" -H "Host: nonexistent.example.com" https://example.com

# Step 2: Fuzz Host header, filter baseline size
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -u https://example.com \
  -H "Host: FUZZ.example.com" \
  -fs 4242   # replace with actual baseline size
  -c

# Alternative: match only responses that differ from known bad size
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -u http://10.10.10.10 \
  -H "Host: FUZZ.target.htb" \
  -fw 839    # filter by word count of 404 response

# With HTTPS and ignore TLS errors
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -u https://example.com \
  -H "Host: FUZZ.example.com" \
  -fs 4242 -k -c
```

## Parameter Fuzzing

### GET Parameter Name Discovery

```bash
# Find valid parameter names when the parameter name is unknown
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u "https://example.com/search?FUZZ=test" \
  -fs 1234   # size of response with no/invalid param
  -c

# With regex match (look for data in response body)
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u "https://example.com/api?FUZZ=1" \
  -mr "data|result|error" -c
```

### GET Parameter Value Fuzzing

```bash
# Fuzz value of a known parameter
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
  -u "https://example.com/page?file=FUZZ" \
  -fc 400,500 -c

# IDOR — numeric ID brute force
ffuf -w <(seq 1 10000) \
  -u "https://example.com/api/user/FUZZ" \
  -mc 200 -c

# Auth bypass values
ffuf -w /usr/share/seclists/Fuzzing/special-chars.txt \
  -u "https://example.com/login?admin=FUZZ" \
  -mc 200,302 -c
```

### POST Parameter Fuzzing

```bash
# Fuzz POST parameter name (form body)
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u https://example.com/login \
  -X POST \
  -d "FUZZ=value&known_param=value" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -fc 302,200 -c

# Fuzz POST parameter value (e.g., password brute force)
ffuf -w /usr/share/seclists/Passwords/Leaked-Databases/rockyou-10.txt \
  -u https://example.com/login \
  -X POST \
  -d "username=admin&password=FUZZ" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -fc 302 -mr "Invalid" -c

# JSON POST body fuzzing
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u https://api.example.com/v1/users \
  -X POST \
  -d '{"FUZZ":"value"}' \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -mc 200 -c
```

## Header Fuzzing

```bash
# Fuzz header names
ffuf -w /usr/share/seclists/Fuzzing/http-request-headers/http-request-headers-common.txt \
  -u https://example.com/ \
  -H "FUZZ: test" \
  -fs 1234 -c

# Fuzz header values (e.g., X-Forwarded-For bypass)
ffuf -w /usr/share/seclists/Fuzzing/IP-list.txt \
  -u https://example.com/admin \
  -H "X-Forwarded-For: FUZZ" \
  -mc 200 -c

# User-Agent fuzzing
ffuf -w /usr/share/seclists/Fuzzing/User-Agents/user-agents.txt \
  -u https://example.com/ \
  -H "User-Agent: FUZZ" \
  -mc 200 -fs 1234 -c
```

## Multiple Wordlist Positions

### Clusterbomb (all combinations)

```bash
# Fuzz both parameter name and value simultaneously
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:PARAM \
  -w /usr/share/seclists/Fuzzing/Extensions/common-file-extensions-wordlist.txt:EXT \
  -u "https://example.com/?PARAM=FUZZ_EXT" \
  -mode clusterbomb \
  -mc 200 -c
# Warning: N×M requests — keep wordlists small or use pitchfork
```

### Pitchfork (parallel iteration)

```bash
# Test username:password pairs from aligned wordlists (same line count)
ffuf -w usernames.txt:USER \
  -w passwords.txt:PASS \
  -u https://example.com/login \
  -X POST \
  -d "username=USER&password=PASS" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -mode pitchfork \
  -fc 302 -c

# Custom keyword names (any string, not just W1/W2)
ffuf -w ids.txt:ID -w tokens.txt:TOKEN \
  -u "https://api.example.com/user/ID?auth=TOKEN" \
  -mode pitchfork \
  -mc 200 -c
```

## Filtering Strategy

Getting clean results from ffuf requires calibrating filters against the baseline response. Typical workflow:

```bash
# 1. Probe baseline: size of a guaranteed 404
curl -s -o /dev/null -w "size=%{size_download} words=%{num_redirects}" \
  https://example.com/definitely_not_real_path_xyz123

# 2. Run ffuf with that size filtered
ffuf -w wordlist.txt -u https://example.com/FUZZ -fs 1234 -c

# 3. If still noisy, add word count filter
ffuf -w wordlist.txt -u https://example.com/FUZZ -fs 1234 -fw 52 -c

# 4. Or use regex to only match interesting content
ffuf -w wordlist.txt -u https://example.com/FUZZ -mr "password|admin|config" -c

# Filter ranges (e.g., filter 1000-2000 bytes)
ffuf -w wordlist.txt -u https://example.com/FUZZ -fs 1000-2000 -c

# Match multiple status codes explicitly
ffuf -w wordlist.txt -u https://example.com/FUZZ -mc 200,204,301,302,307,401,403 -c

# Combine AND filters (both must match to filter)
ffuf -w wordlist.txt -u https://example.com/FUZZ -fc 404 -fs 1234 -fmode and -c
```

## Rate Limiting and Stealth

```bash
# Hard rate limit (requests per second)
ffuf -w wordlist.txt -u https://example.com/FUZZ -rate 50

# Random delay between requests (stealth)
ffuf -w wordlist.txt -u https://example.com/FUZZ -p 0.5-2.0

# Reduce threads for less aggressive scanning
ffuf -w wordlist.txt -u https://example.com/FUZZ -t 5 -p 0.2

# Replay matched requests through Burp (analyze manually)
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -replay-proxy http://127.0.0.1:8080 \
  -mc 200 -c
```

## Output Formats and Saving Results

```bash
# Save as JSON
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -o results.json -of json -c

# Save as HTML report
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -o report.html -of html -c

# Save as CSV
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -o results.csv -of csv -c

# Save all formats simultaneously
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -o results -of all -c

# Save raw response bodies for matched results
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -od ./responses/ -mc 200 -c

# JSON to stdout for piping
ffuf -w wordlist.txt -u https://example.com/FUZZ -json -s | \
  jq '.results[] | {url: .url, status: .status, size: .length}'

# Skip writing output file if nothing found
ffuf -w wordlist.txt -u https://example.com/FUZZ -o results.json -or -c
```

## Interactive Mode

During an active scan, press `ENTER` to open the interactive console:

```
ffuf interactive> help
Available commands:
  help         - Show this help
  fc [value]   - Add/remove filter status codes
  fl [value]   - Add/remove filter line count
  fw [value]   - Add/remove filter word count
  fs [value]   - Add/remove filter size
  fr [value]   - Add/remove filter regex
  pause        - Pause scanning
  resume       - Resume scanning
  rate [value] - Adjust requests per second
  queueshow    - Show queue
  restart      - Restart scan
  quit         - Stop scan
```

This lets you tune filters mid-scan without restarting — particularly useful when the baseline changes dynamically.

## Common Workflows

### HTB / CTF Directory Brute Force

```bash
# Fast standard sweep
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -u http://10.10.10.10/FUZZ \
  -mc 200,301,302,403 \
  -e .php,.txt,.html \
  -c -v

# With authentication cookie
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u http://10.10.10.10/FUZZ \
  -b "PHPSESSID=abc123def456" \
  -mc 200,301,302,403 -c
```

### Subdomain Enumeration via DNS (with httpx probe)

```bash
# Fuzz DNS subdomains via virtual hosting
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
  -u http://FUZZ.example.com \
  -mc 200,301,302 \
  -t 50 -c | \
  grep "FUZZ" | awk '{print $1}' | \
  httpx -silent | tee live_subdomains.txt
```

### API Endpoint Discovery

```bash
# Common REST API paths
ffuf -w /usr/share/seclists/Discovery/Web-Content/api/objects.txt \
  -u https://api.example.com/v1/FUZZ \
  -H "Authorization: Bearer TOKEN" \
  -mc 200,201,401,403 \
  -c

# Versioned API brute force
ffuf -w <(echo -e "v1\nv2\nv3\nv4\nv5\nbeta\nalpha") \
  -u https://api.example.com/FUZZ/users \
  -H "Authorization: Bearer TOKEN" \
  -mc 200 -c
```

### Full Engagement Workflow

```bash
# Phase 1: Directory discovery
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
  -u https://target.com/FUZZ \
  -mc 200,301,302,403 -fs 4096 \
  -o phase1_dirs.json -of json \
  -c -t 40

# Phase 2: File fuzzing in discovered directories
for dir in $(cat phase1_dirs.json | jq -r '.results[].url'); do
  ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt \
    -u "${dir}/FUZZ" \
    -mc 200 -fs 4096 \
    -o "phase2_$(echo $dir | md5sum | cut -c1-8).json" -of json \
    -c -t 20 &
done
wait

# Phase 3: Parameter discovery on interesting endpoints
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u "https://target.com/search?FUZZ=test" \
  -mc 200 -fs 4096 -c
```

## Integration with SecLists and Other Tools

```bash
# SecLists install
sudo apt install seclists
# or
git clone https://github.com/danielmiessler/SecLists /usr/share/seclists

# Chain with feroxbuster for comparison
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u https://example.com/FUZZ -mc 200,301 -c -o ffuf_results.json

# Pipe ffuf JSON output into httpx for probing
cat ffuf_results.json | jq -r '.results[].url' | httpx -silent

# Send matches to Burp for manual review
ffuf -w wordlist.txt -u https://example.com/FUZZ \
  -mc 200 \
  -replay-proxy http://127.0.0.1:8080 \
  -c
```

## Troubleshooting

| Issue | Fix |
|---|---|
| Too many false positives | Determine 404 response size/words with `curl`, set `-fs` or `-fw` |
| All results filtered | `-mc all` to see everything, then re-tune filters |
| Scan finishes instantly with 0 results | Check target is reachable; verify `-u` URL and FUZZ placement |
| Recursion running forever | Set `-maxtime-job 60` and `-recursion-depth 2` |
| Rate limit errors (429) | Add `-rate 20` and `-p 0.5-1.5`; reduce `-t` to 10 |
| TLS errors | Add `-k` to skip certificate verification |
| POST body not sent | Verify `-X POST` and `-H "Content-Type: application/x-www-form-urlencoded"` |
| Encoding issues in FUZZ | Use `-enc FUZZ:urlencode` or pre-encode wordlist entries |
| Output file empty despite matches | Remove `-or` flag; check `-o` path is writable |
| Interactive mode not available | Use `-noninteractive` flag to suppress and script safely |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
