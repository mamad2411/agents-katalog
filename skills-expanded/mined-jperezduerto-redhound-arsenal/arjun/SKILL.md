---
name: arjun
description: >
  Operate Arjun — an HTTP parameter discovery tool that finds hidden GET, POST, JSON, and XML
  parameters in web endpoints through intelligent wordlist-based bruteforcing. Use when mapping
  an application's attack surface, discovering undocumented API parameters, or preparing targets
  for fuzzing with ffuf, SQLMap, or XSStrike. Covers installation, GET/POST/JSON/XML modes,
  Burp import, custom wordlists, threading, output formats, and integration into a full web
  application testing workflow.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/s0md3v/Arjun
  language: Python
---

# arjun Agent Skill

## When to Use This Skill

Use this skill when:
- An API endpoint or web page exists but its accepted parameters are unknown
- Mapping an application's complete attack surface before fuzzing or injection testing
- Finding hidden/undocumented parameters in admin panels, APIs, or legacy endpoints
- Discovering debug parameters (`debug=true`, `test=1`, `admin=1`) on production endpoints
- Preparing a parameter list for ffuf, SQLMap, or XSStrike
- Importing Burp Suite HTTP history to batch-discover parameters across multiple endpoints

## What Arjun Does

Arjun (s0md3v/Arjun, ~4.8k GitHub stars) discovers HTTP parameters that a web endpoint accepts
but that are not visible in the application's normal request flow. It sends large batches of
parameters simultaneously, compares responses for anomalies (size change, status change, content
change), and identifies which parameters cause a different response — indicating the server
processed that parameter. Arjun supports GET, POST (form-encoded), JSON body, and XML body
parameter discovery. It is an essential first step before fuzzing or injection testing on any
unknown endpoint.

## Installation

### pip (recommended)
```bash
pip3 install arjun
arjun --help
```

### pipx (isolated)
```bash
pipx install arjun
```

### From Source
```bash
git clone https://github.com/s0md3v/Arjun.git
cd Arjun
pip3 install -r requirements.txt
python3 arjun.py --help
```

### Verify
```bash
arjun -u https://httpbin.org/get
# Should discover: 'q', 'lang', or similar httpbin parameters
```

## Core Concepts

### Detection Method
Arjun sends requests with batches of parameters (default: 500 per chunk) and compares:
- **Response length change**: Parameter processed → response size differs from baseline
- **Status code change**: 200 → 302 or 200 → 403 → parameter exists but access controlled
- **Response time change**: Sleep-based parameters (`delay`, `timeout`)
- **Content change**: Keyword appears in response body

The chunk-based approach (testing 500 params per request) makes Arjun extremely fast compared
to testing each parameter individually.

### False Positive Filtering
Arjun automatically filters false positives by:
1. Sending the baseline request without parameters
2. Comparing every positive hit against the baseline
3. Re-verifying positive parameters with a second request
4. Reporting only stable positives

### Stable Mode
When the application's response is non-deterministic (random CSRF tokens, timestamps in body),
stable mode (`-s`) filters noise by sending multiple baseline requests and computing a stable
response signature.

## CLI Reference

### GET Parameter Discovery
```bash
# Basic GET scan
arjun -u http://target.com/search

# With custom output
arjun -u http://target.com/search -oT results.txt

# Multiple URLs from file
arjun --urls targets.txt

# Specific parameter to test alongside discovery
arjun -u http://target.com/api/users -m GET
```

### POST Parameter Discovery
```bash
# Form-encoded POST (application/x-www-form-urlencoded)
arjun -u http://target.com/login -m POST

# Explicitly specify method
arjun -u http://target.com/submit -m POST

# POST with pre-known parameters included
arjun -u http://target.com/update -m POST \
  --include "csrf_token=abc123&_method=PUT"
```

### JSON Parameter Discovery
```bash
# Test JSON body parameters (application/json)
arjun -u http://target.com/api/users -m JSON

# JSON mode automatically sets Content-Type header
# Sends: {"param1":"arjun","param2":"arjun",...} in batches

# JSON with existing required parameters
arjun -u http://target.com/api/search -m JSON \
  --include '{"api_key":"known_key"}'
```

### XML Parameter Discovery
```bash
# Test XML body parameters (application/xml / text/xml)
arjun -u http://target.com/xml-api -m XML

# XML mode wraps parameters in XML tags and POSTs to endpoint
```

### Importing from Burp Suite
```bash
# Export from Burp: Proxy → HTTP History → Select all → Save items → XML

# Import and scan all endpoints from Burp export
arjun -i burp_export.xml

# Import and test with specific method
arjun -i burp_export.xml -m GET

# Import + output to JSON
arjun -i burp_export.xml -oJ results.json

# This is the most efficient way to run Arjun across an entire application —
# browse all features in Burp first, then batch-discover parameters on all visited URLs
```

### Custom Wordlists
```bash
# Use a custom parameter wordlist
arjun -u http://target.com/api -w /opt/wordlists/params.txt

# SecLists parameter wordlist
arjun -u http://target.com/api \
  -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt

# Minimal wordlist for quick scan
arjun -u http://target.com/api \
  -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt

# Stack multiple wordlists (concatenate first)
cat /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
    /opt/wordlists/custom_params.txt | sort -u > combined_params.txt
arjun -u http://target.com/api -w combined_params.txt
```

### Threading and Delay
```bash
# Increase threads (default: 5 — Arjun is intentionally conservative)
arjun -u http://target.com/api -t 20

# Maximum threads for fast targets
arjun -u http://target.com/api -t 50

# Delay between requests (seconds, float) — rate limit evasion
arjun -u http://target.com/api -d 1

# Combine: low threads + delay for fragile/WAF'd targets
arjun -u http://target.com/api -t 3 -d 2
```

### Custom Headers
```bash
# Add authentication header
arjun -u http://target.com/api/admin \
  --headers "Authorization: Bearer eyJhbGc..."

# Session cookie
arjun -u http://target.com/dashboard \
  --headers "Cookie: session=authenticated_token"

# Multiple headers (comma-separated or repeated)
arjun -u http://target.com/api \
  --headers "Authorization: Bearer TOKEN
X-API-Version: 2.0
Accept: application/json"
```

### Stable Mode
```bash
# Enable stable mode for applications with dynamic responses
# (CSRF tokens, timestamps, random elements in body)
arjun -u http://target.com/search -s

# Stable mode takes longer (runs more baseline requests) but reduces false positives
arjun -u http://target.com/dashboard -s -t 5 -d 1
```

### Output Formats
```bash
# Plain text output
arjun -u http://target.com/search -oT output.txt

# JSON output (structured, machine-readable)
arjun -u http://target.com/search -oJ output.json

# JSON output format:
# {"target.com": {"GET": ["q", "lang", "debug"], "POST": []}}

# Burp state output (for import back into Burp)
arjun -u http://target.com/search -oB output.xml

# Screen output only (default, no file)
arjun -u http://target.com/search
```

### Chunked Request Size
```bash
# Control how many parameters are tested per request (default: 500)
arjun -u http://target.com/search --chunk-size 250

# Smaller chunks for WAFs that reject large parameter sets
arjun -u http://target.com/search --chunk-size 50

# Larger chunks for fast targets with no WAF
arjun -u http://target.com/search --chunk-size 1000
```

### Proxy Support
```bash
# Route through Burp Suite
arjun -u http://target.com/search --proxy http://127.0.0.1:8080

# SOCKS5 proxy for internal targets
arjun -u http://192.168.1.10/api --proxy socks5://127.0.0.1:1080
```

### Timeout
```bash
# Request timeout in seconds (default: 15)
arjun -u http://target.com/search --timeout 30

# Fast scan with short timeout
arjun -u http://target.com/api --timeout 5 -t 20
```

## Common Workflows

### Standard API Reconnaissance
```bash
# Step 1: Discover GET params on main API endpoint
arjun -u http://target.com/api/users -m GET -oJ api_get_params.json

# Step 2: Discover POST params
arjun -u http://target.com/api/users -m POST -oJ api_post_params.json

# Step 3: Discover JSON params (modern APIs)
arjun -u http://target.com/api/users -m JSON -oJ api_json_params.json

# Step 4: Review and prioritise
cat api_json_params.json | python3 -m json.tool
```

### Burp-Integrated Full Application Scan
```bash
# 1. Browse the entire application through Burp (authenticated)
# 2. Export HTTP history: Proxy → HTTP History → Right-click → Save items

# 3. Run Arjun across all discovered endpoints
arjun -i burp_history.xml -oJ all_params.json -t 10 -s

# 4. Extract endpoints with discovered parameters
cat all_params.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for url, methods in data.items():
    for method, params in methods.items():
        if params:
            print(f'[{method}] {url}: {params}')
"
```

### Finding Debug/Hidden Parameters
```bash
# Use a targeted wordlist for common debug/admin params
cat > /tmp/debug_params.txt << 'EOF'
debug
test
dev
admin
verbose
log
trace
internal
hidden
preview
beta
staging
api_key
token
key
secret
EOF

arjun -u http://target.com/page -w /tmp/debug_params.txt -t 10

# Also try common params from SecLists
arjun -u http://target.com/page \
  -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
```

### Arjun → ffuf → SQLMap Workflow
```bash
# Step 1: Discover parameters with Arjun
arjun -u http://target.com/search -m GET -oJ params.json

# Step 2: Extract parameter names
PARAMS=$(cat params.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
params = []
for url, methods in data.items():
    params.extend(methods.get('GET', []))
print(','.join(params))
")

# Step 3: Fuzz discovered parameters with ffuf
for param in $(echo $PARAMS | tr ',' '\n'); do
  echo "[*] Fuzzing param: $param"
  ffuf -u "http://target.com/search?${param}=FUZZ" \
    -w /usr/share/seclists/Fuzzing/special-chars.txt \
    -mc 200,302,400,500 -o ffuf_${param}.json -of json
done

# Step 4: SQLMap on parameters that show error responses
sqlmap -u "http://target.com/search?${PARAMS// /=test&}=test" --batch --dbs
```

### Arjun → XSStrike Workflow
```bash
# Find parameters
arjun -u http://target.com/page -oJ params.json

# Extract and build XSStrike command
PARAMS=$(cat params.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for url, methods in data.items():
    for p in methods.get('GET', []):
        print(p)
" | head -1)

# Test for XSS on discovered parameters
python3 /opt/XSStrike/xsstrike.py \
  -u "http://target.com/page?${PARAMS}=test" \
  --params "$PARAMS"
```

## Advanced Techniques

### Building a Custom Parameter Wordlist from Target
```bash
# Extract words from the application (page source, JS files)
# Step 1: Download all JS files
curl -s http://target.com | grep -oE 'src="[^"]*\.js"' | \
  grep -oE '"[^"]*"' | tr -d '"' | \
  while read js; do curl -s "http://target.com/$js"; done > all_js.txt

# Step 2: Extract variable names and property names from JS
cat all_js.txt | grep -oE '[a-zA-Z_][a-zA-Z0-9_]{2,20}' | \
  sort -u > custom_wordlist.txt

# Step 3: Use custom wordlist with Arjun
arjun -u http://target.com/api -w custom_wordlist.txt
```

### Batch Scanning Multiple Endpoints
```bash
#!/bin/bash
# Scan multiple API endpoints discovered during spidering
ENDPOINTS=(
  "http://target.com/api/v1/users"
  "http://target.com/api/v1/posts"
  "http://target.com/api/v2/search"
  "http://target.com/admin/settings"
)

for endpoint in "${ENDPOINTS[@]}"; do
  echo "[*] Scanning: $endpoint"
  arjun -u "$endpoint" -m GET -m POST -oJ \
    "arjun_$(echo $endpoint | md5sum | cut -c1-8).json" &
done
wait

# Merge results
python3 -c "
import json, glob
merged = {}
for f in glob.glob('arjun_*.json'):
    with open(f) as fh:
        data = json.load(fh)
    merged.update(data)
print(json.dumps(merged, indent=2))
" > all_discovered_params.json
```

### Rate Limit Evasion
```bash
arjun -u http://target.com/api -t 1 -d 3 --chunk-size 25
```

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| ffuf | Pass discovered params as FUZZ targets |
| SQLMap | Supply `-p param` for each discovered injectable param |
| XSStrike | `--params` flag accepts Arjun-discovered param names |
| Burp Suite | `-i` input, `-oB` output for round-trip integration |
| nuclei | Discovered endpoints + params → nuclei fuzzing templates |
| dalfox | Pipe discovered GET params for XSS scanning |

## Troubleshooting

**No parameters discovered on known endpoint**
```bash
# Try different method
arjun -u http://target.com/api -m JSON   # Instead of GET

# Reduce chunk size (server might reject large param sets)
arjun -u http://target.com/api --chunk-size 50

# Add authentication (endpoint may require auth to reveal params)
arjun -u http://target.com/api \
  --headers "Authorization: Bearer TOKEN"

# Use stable mode if responses vary
arjun -u http://target.com/api -s
```

**Too many false positives**
```bash
# Enable stable mode
arjun -u http://target.com/search -s

# Reduce chunk size to reduce noise
arjun -u http://target.com/search --chunk-size 100

# Route through Burp to see what responses look like
arjun -u http://target.com/search --proxy http://127.0.0.1:8080
```

**Rate limited / IP blocked during scan**
```bash
arjun -u http://target.com/api -t 2 -d 5 --chunk-size 25

# Or route via proxy
arjun -u http://target.com/api --proxy socks5://127.0.0.1:1080
```

**Burp import not working**
```bash
# Ensure export is in Burp XML format (not HAR)
# In Burp: Proxy → HTTP History → Right-click selected items → Save items → .xml
# Make sure file is uncompressed XML
file burp_export.xml   # Should say: XML document text
```

**JSON mode not sending correct Content-Type**
```bash
arjun -u http://target.com/api -m JSON \
  --headers "Content-Type: application/json"
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
