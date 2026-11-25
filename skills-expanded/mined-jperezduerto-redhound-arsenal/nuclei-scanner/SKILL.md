---
name: nuclei-scanner
description: >
  Build, extend, and operate Nuclei — a fast, template-based vulnerability scanner by
  ProjectDiscovery. Use when running automated vulnerability scans, writing custom detection
  templates, or building recon pipelines with subfinder and httpx. Covers installation,
  template structure (id, info, requests, matchers, extractors), scan execution flags,
  template selection by tag and severity, rate limiting, output formats, headless scanning,
  interactsh OOB integration, workflow chaining, and the subfinder → httpx → nuclei pipeline.
license: MIT
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/projectdiscovery/nuclei
  language: Go
---

# nuclei-scanner Agent Skill

## When to Use This Skill

Use this skill when:
- Running automated vulnerability scans against web applications or infrastructure
- The user asks about Nuclei, nuclei templates, or ProjectDiscovery tooling
- Writing custom YAML templates to detect specific vulnerabilities or misconfigurations
- Building reconnaissance pipelines (subfinder → httpx → nuclei)
- Performing OOB (out-of-band) vulnerability detection with interactsh
- Tuning scan performance (rate limiting, concurrency, retries)

## What Nuclei Does

Nuclei is a fast, configurable vulnerability scanner driven by YAML templates. Each template
describes a specific check — HTTP request, DNS query, TCP probe, or headless browser action —
along with matchers that determine a positive finding. The public template library covers
thousands of CVEs, misconfigurations, exposures, and technology fingerprints. Teams use Nuclei
to operationalize security checks as version-controlled, shareable YAML files.

## Installation

```bash
# Go install (recommended — always latest)
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Prebuilt binary (Linux amd64)
wget https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_linux_amd64.zip
unzip nuclei_linux_amd64.zip && sudo mv nuclei /usr/local/bin/

# Kali / Debian (may lag behind latest)
sudo apt install nuclei

# macOS
brew install nuclei

# Docker
docker pull projectdiscovery/nuclei:latest
docker run --rm -v $(pwd):/data projectdiscovery/nuclei \
  -u https://target.example.com -t /root/nuclei-templates/

# Update templates after install
nuclei -ut        # update to latest community templates
nuclei -version
```

## Template Structure

Every Nuclei template is a YAML file with these top-level keys:

```yaml
id: template-unique-id        # lowercase, hyphens, unique across all templates

info:
  name: Human Readable Name
  author: operator
  severity: critical            # info, low, medium, high, critical
  description: What this detects and why it matters.
  reference:
    - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41773
  tags: apache,rce,cve,cve2021  # comma-separated tags for filtering
  metadata:
    cvss-score: 9.8
    cve-id: CVE-2021-41773
    cwe-id: CWE-22

# Protocol-specific block: http, dns, tcp, headless, ssl, websocket, whois
http:
  - method: GET
    path:
      - "{{BaseURL}}/cgi-bin/.%2e/.%2e/bin/sh"
    headers:
      Content-Type: application/x-www-form-urlencoded
    body: "echo Content-Type: text/plain; echo; id"
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      - type: word
        words:
          - "uid="
          - "gid="
        condition: and
```

## Template Variables

```yaml
{{BaseURL}}    # https://example.com/path
{{Hostname}}   # example.com
{{Host}}       # example.com (no port)
{{Port}}       # 443
{{Scheme}}     # https
{{randstr}}    # Random string per request
{{randint}}    # Random integer
{{unix_time}}  # Current Unix epoch
# DSL helpers: contains(), len(), regex(), to_lower(), md5(), base64(), url_encode()
```

## Matchers

```yaml
matchers:
  # Status code
  - type: status
    status:
      - 200
      - 302

  # Word match (in body by default)
  - type: word
    words:
      - "root:x:0:0"
    case-insensitive: true
    part: body          # body, header, all, interactsh_protocol

  # Regex match
  - type: regex
    regex:
      - "([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})"
    group: 1            # capture group to extract

  # Binary match (for non-text responses)
  - type: binary
    binary:
      - "504B0304"      # PK ZIP magic bytes (hex)

  # Size match
  - type: size
    size:
      - 1024

  # DSL expression match
  - type: dsl
    dsl:
      - "contains(body, 'uid=0') && status_code == 200"
      - "len(body) > 100"
    condition: or

# Combine matchers
matchers-condition: and    # all must match (default)
matchers-condition: or     # any must match
```

## Extractors

```yaml
extractors:
  - type: regex
    name: api_key
    regex:
      - "api[_-]?key[\"']?\\s*[:=]\\s*[\"']?([A-Za-z0-9_\\-]{32,})"
    group: 1
    part: body
  - type: kval
    kval:
      - Set-Cookie
  - type: json
    name: token
    json:
      - ".data.token"
  - type: dsl
    dsl:
      - "concat(host, ':', port)"
```

## Running Scans

### Basic Usage

```bash
# Single target
nuclei -u https://target.example.com

# Target list
nuclei -l targets.txt

# Target list with specific templates
nuclei -l targets.txt -t cves/

# Single template
nuclei -u https://target.example.com -t cves/2021/CVE-2021-41773.yaml

# Template directory
nuclei -u https://target.example.com -t exposures/configs/

# Read targets from stdin
cat targets.txt | nuclei -t cves/
echo "https://target.example.com" | nuclei -t cves/2022/
```

### Template Selection

```bash
# By tags (AND logic by default)
nuclei -u https://target.example.com -tags cve
nuclei -u https://target.example.com -tags apache,rce
nuclei -u https://target.example.com -tags "cve,2021"

# By severity
nuclei -l targets.txt -severity critical,high
nuclei -l targets.txt -severity medium

# Exclude tags
nuclei -l targets.txt -exclude-tags dos,fuzz,intrusive

# Exclude templates by path
nuclei -l targets.txt -exclude-templates fuzzing/

# By author
nuclei -l targets.txt -author pdteam

# Combine: critical CVEs, no DoS
nuclei -l targets.txt -severity critical -tags cve -exclude-tags dos

# Automatic scan (Nuclei picks templates based on detected tech)
nuclei -u https://target.example.com -as
```

### Template Update

```bash
nuclei -ut                 # update to latest public templates
nuclei -ut -duc            # update and disable update check banner
```

### Rate Limiting and Concurrency

```bash
nuclei -l targets.txt -rl 100        # rate limit: 100 requests/sec (global)
nuclei -l targets.txt -c 25          # concurrent template executions (default 25)
nuclei -l targets.txt -bs 50         # bulk target size per template
nuclei -l targets.txt -rlm 10        # rate limit per minute
nuclei -l targets.txt -timeout 10    # per-request timeout in seconds
nuclei -l targets.txt -retries 2     # retry failed requests

# Conservative scan for sensitive targets
nuclei -l targets.txt -rl 10 -c 5 -timeout 15 -retries 1
```

### Output Formats

```bash
nuclei -l targets.txt -o results.txt          # plain text
nuclei -l targets.txt -json -o results.jsonl  # JSON lines (one JSON per finding)
nuclei -l targets.txt -json-export results.json  # single JSON array
nuclei -l targets.txt -me results/            # markdown export (per-host reports)
nuclei -l targets.txt -sarif-export results.sarif  # SARIF for CI/CD integration
nuclei -l targets.txt -silent                 # suppress banner, print findings only
nuclei -l targets.txt -nc                     # no color output
nuclei -l targets.txt -v                      # verbose (show sent/received)
nuclei -l targets.txt -debug                  # print full request/response
nuclei -l targets.txt -stats                  # periodic progress stats
```

## Headless Scanning (Browser-Based)

For JavaScript-heavy applications and DOM-based vulnerabilities.

```bash
# Install chromium dependency
nuclei -install-path-helper             # shows headless setup instructions

# Run headless templates
nuclei -u https://target.example.com -headless -t headless/

# Specific headless templates
nuclei -u https://target.example.com -t headless/generic/open-redirect.yaml

# Headless with browser flags
nuclei -u https://target.example.com -headless \
  -page-timeout 30 \
  -browser-args "no-sandbox,disable-gpu"
```

## Interactsh — OOB Testing

Nuclei integrates with interactsh for out-of-band vulnerability detection (SSRF, blind XXE, OOB SQLi, etc.)

```bash
# Public interactsh server (default, requires outbound DNS/HTTP)
nuclei -l targets.txt -t fuzzing/ssrf.yaml    # uses oast.pro by default

# Self-hosted interactsh server
interactsh-client -server interactsh.example.com -token mytoken &
nuclei -l targets.txt -iserver interactsh.example.com -itoken mytoken

# Disable interactsh (for air-gapped or strict environments)
nuclei -l targets.txt -no-interactsh
```

### Template Using interactsh

```yaml
id: blind-ssrf-example

info:
  name: Blind SSRF via interactsh
  severity: high
  tags: ssrf,oob

http:
  - method: GET
    path:
      - "{{BaseURL}}/fetch?url=http://{{interactsh-url}}"
    matchers:
      - type: word
        part: interactsh_protocol
        words:
          - "http"
```

## Writing Custom Templates

### HTTP Template (GET with regex)

```yaml
id: exposed-git-config

info:
  name: Exposed .git/config
  severity: medium
  tags: git,exposure,config

http:
  - method: GET
    path:
      - "{{BaseURL}}/.git/config"
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      - type: word
        words:
          - "[core]"
        part: body
    extractors:
      - type: regex
        regex:
          - "url = (.*)"
        part: body
```

### HTTP Template (POST with dynamic extraction)

```yaml
id: graphql-introspection

info:
  name: GraphQL Introspection Enabled
  severity: low
  tags: graphql,exposure

http:
  - method: POST
    path:
      - "{{BaseURL}}/graphql"
      - "{{BaseURL}}/api/graphql"
    headers:
      Content-Type: application/json
    body: '{"query":"{__schema{types{name}}}"}'
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      - type: word
        words:
          - "__schema"
        part: body
```

## Workflows

Workflows chain templates — run subsequent templates only if previous ones match.

```yaml
id: wordpress-workflow
info:
  name: WordPress Detection and Vuln Scan
  severity: info
  tags: wordpress,workflow
workflows:
  - template: technologies/wordpress-detect.yaml
    subtemplates:
      - template: cves/2020/CVE-2020-11738.yaml
      - template: vulnerabilities/wordpress/
```

```bash
nuclei -l targets.txt -w workflows/wordpress-workflow.yaml
```

## The Full Recon Pipeline

### subfinder → httpx → nuclei

```bash
# 1. Enumerate subdomains
subfinder -d example.com -silent -o subdomains.txt

# 2. Probe live web services
cat subdomains.txt | httpx -silent -o live_hosts.txt
# With port expansion:
cat subdomains.txt | httpx -silent -ports 80,443,8080,8443,8888 -o live_hosts.txt

# 3. Nuclei scan on live hosts
nuclei -l live_hosts.txt -t cves/ -t exposures/ \
  -severity critical,high \
  -rl 100 -c 25 \
  -json -o findings.jsonl

# One-liner (streaming)
subfinder -d example.com -silent | \
  httpx -silent | \
  nuclei -t cves/ -severity critical,high -json -o critical_findings.jsonl
```

## Advanced Techniques

### Template Filtering with Config File

```yaml
# ~/.config/nuclei/config.yaml
severity:
  - critical
  - high
exclude-tags:
  - dos
  - intrusive
  - fuzz
rate-limit: 150
concurrency: 30
```

```bash
nuclei -l targets.txt -config ~/.config/nuclei/config.yaml

# Resume interrupted scan
nuclei -l targets.txt -t cves/ -resume /path/to/resume.cfg

# Custom auth headers
nuclei -u https://target.example.com -H "Authorization: Bearer eyJ..." -t exposures/

# Proxy through Burp Suite
nuclei -l targets.txt -proxy http://127.0.0.1:8080 -ni
```

## Integration with Other Tools

```bash
# Results into Elasticsearch
nuclei -l targets.txt -json | \
  jq -c '. + {"@timestamp": now | todate}' | \
  curl -X POST "http://elk:9200/nuclei/_doc" -H 'Content-Type: application/json' -d @-

# Slack notification for critical findings
nuclei -l targets.txt -severity critical -json | \
  jq -r '"CVE Found: \(.info.name) on \(.host) [\(.severity)]"' | \
  xargs -I{} curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"{}"}' https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# GitHub Actions CI — SARIF upload
nuclei -l targets.txt -severity high,critical -sarif-export nuclei.sarif
```

## Troubleshooting

| Issue | Fix |
|---|---|
| No results despite known vulns | Run with `-v -debug` to inspect requests/responses |
| Rate limit errors (429) | Lower `-rl` (e.g. `-rl 20`) and `-c 5` |
| Templates not found | Run `nuclei -ut` to update template library |
| SSL errors on self-signed certs | Add `-ni` (disable TLS verification) |
| Interactsh OOB not triggering | Check outbound DNS/HTTP; use `-iserver` self-hosted |
| Too many false positives | Add `-exclude-tags intrusive,fuzz` and `-severity high,critical` |
| Headless not working | Install chromium: `apt install chromium` or `chromium-browser` |
| Memory usage too high | Reduce `-c` and `-bs`; split target list |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Why Your Penetration Test Report Is Useless (And What to Ask For Instead)](https://redhound.us/pentest-report)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
