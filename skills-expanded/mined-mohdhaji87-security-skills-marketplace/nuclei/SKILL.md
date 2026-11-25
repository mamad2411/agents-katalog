---
name: nuclei
description: Fast, template-based vulnerability scanner for authorized security testing. Use when user asks to scan for vulnerabilities, detect CVEs, find misconfigurations, security audits, bug bounty hunting, or penetration testing. Supports HTTP, TCP, DNS, SSL protocols with 8000+ community templates.
---

# Nuclei Vulnerability Scanner

Fast, customizable vulnerability scanner using YAML-based templates. Developed by ProjectDiscovery.

**Authorization required**: Only scan targets you have explicit permission to test.

## Installation

```bash
# Go install (recommended)
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Homebrew (macOS)
brew install nuclei

# Docker
docker pull projectdiscovery/nuclei:latest

# Update templates
nuclei -update-templates
```

## Quick Start

```bash
# Scan single target with all templates
nuclei -u https://example.com

# Scan multiple targets from file
nuclei -l targets.txt

# Scan with specific templates
nuclei -u https://example.com -t cves/

# Scan with severity filter
nuclei -u https://example.com -s critical,high

# Output results to file
nuclei -u https://example.com -o results.txt
```

## Scripts

| Script | Purpose |
|--------|---------|
| `nuclei_scan.py` | Full-featured scan wrapper with reporting |
| `template_finder.py` | Search and filter templates by keywords |
| `bulk_scanner.py` | Parallel scanning of multiple targets |

## Common Use Cases

### CVE Detection
```bash
# Scan for all CVEs
nuclei -u https://target.com -t cves/

# Scan for specific CVE
nuclei -u https://target.com -t cves/2024/ -tags cve

# Critical CVEs only
nuclei -u https://target.com -t cves/ -s critical
```

### Web Application Security
```bash
# OWASP vulnerabilities
nuclei -u https://target.com -t vulnerabilities/

# Exposed panels and dashboards
nuclei -u https://target.com -t exposed-panels/

# Default credentials
nuclei -u https://target.com -t default-logins/

# Misconfigurations
nuclei -u https://target.com -t misconfiguration/
```

### Technology Detection
```bash
# Detect technologies
nuclei -u https://target.com -t technologies/

# Detect CMS
nuclei -u https://target.com -tags wordpress,joomla,drupal
```

### SSL/TLS Testing
```bash
# SSL certificate issues
nuclei -u https://target.com -t ssl/

# Expired certificates
nuclei -u https://target.com -t ssl/expired-ssl.yaml
```

### Subdomain Scanning
```bash
# Scan subdomains from file
subfinder -d example.com | nuclei -t technologies/

# With httpx preprocessing
subfinder -d example.com | httpx | nuclei
```

## Key Options

```
TARGET:
   -u, -target string[]     Target URLs/hosts to scan
   -l, -list string         File with list of targets
   -eh, -exclude-hosts      Hosts to exclude

TEMPLATES:
   -t, -templates string[]  Templates to run (directory/file)
   -nt, -new-templates      Run only new templates from last update
   -w, -workflows string[]  Workflows to run
   -tags string[]           Tags to include (comma-separated)
   -etags string[]          Tags to exclude
   -itags string[]          Run only templates with specific tags
   -id string[]             Template IDs to run
   -eid string[]            Template IDs to exclude

FILTERING:
   -s, -severity string[]   Filter by severity (info,low,medium,high,critical)
   -es, -exclude-severity   Exclude by severity
   -pt, -type string[]      Protocol types to run (http,dns,tcp,ssl,file)

OUTPUT:
   -o, -output string       Output file path
   -j, -jsonl               JSONL output format
   -markdown-export string  Export results as markdown
   -sarif-export string     Export results as SARIF

RATE-LIMIT:
   -rl, -rate-limit int     Requests per second (default: 150)
   -rlm, -rate-limit-minute Requests per minute
   -c, -concurrency int     Concurrent templates (default: 25)
   -bs, -bulk-size int      Hosts per template (default: 25)

OPTIMIZATION:
   -timeout int             Timeout in seconds (default: 10)
   -retries int             Retries for failed requests (default: 1)
   -mhe, -max-host-error    Max errors per host (default: 30)
   -nmhe                    Disable host skipping on errors

HEADLESS:
   -headless                Enable headless browser
   -page-timeout int        Page timeout in seconds (default: 20)
   -show-browser            Show browser during headless mode

INTERACTSH (OOB Testing):
   -iserver string          Interactsh server URL
   -itoken string           Interactsh auth token
   -interactions-cooldown   Cooldown period for interactions
```

## Template Categories

| Category | Description |
|----------|-------------|
| `cves/` | Known CVE exploits |
| `vulnerabilities/` | Generic vulnerabilities |
| `exposed-panels/` | Admin panels, dashboards |
| `default-logins/` | Default credentials |
| `misconfiguration/` | Security misconfigurations |
| `technologies/` | Technology fingerprinting |
| `exposures/` | Sensitive data exposure |
| `takeovers/` | Subdomain takeover checks |
| `fuzzing/` | Fuzzing templates |
| `workflows/` | Multi-step scanning workflows |
| `ssl/` | SSL/TLS issues |
| `dns/` | DNS security checks |
| `network/` | Network service checks |
| `file/` | Local file analysis |

## Writing Custom Templates

### Basic HTTP Template
```yaml
id: custom-check

info:
  name: Custom Security Check
  author: your-name
  severity: medium
  description: Detects custom vulnerability
  tags: custom,security

http:
  - method: GET
    path:
      - "{{BaseURL}}/admin"
      - "{{BaseURL}}/administrator"

    matchers-condition: or
    matchers:
      - type: word
        words:
          - "Admin Panel"
          - "Login"
        condition: or

      - type: status
        status:
          - 200
```

### Template with Extractors
```yaml
id: version-extractor

info:
  name: Version Extractor
  author: your-name
  severity: info

http:
  - method: GET
    path:
      - "{{BaseURL}}"

    extractors:
      - type: regex
        name: version
        regex:
          - 'Version[:\s]+([0-9.]+)'
        group: 1
```

### DNS Template
```yaml
id: dns-zone-transfer

info:
  name: DNS Zone Transfer
  author: your-name
  severity: high

dns:
  - name: "{{FQDN}}"
    type: AXFR

    matchers:
      - type: word
        words:
          - "IN"
          - "SOA"
        condition: and
```

## Advanced Usage

### Authenticated Scanning
```bash
# With header
nuclei -u https://target.com -H "Authorization: Bearer token123"

# With cookie
nuclei -u https://target.com -H "Cookie: session=abc123"

# From config file
nuclei -u https://target.com -config nuclei-config.yaml
```

### Workflow Scanning
```bash
# Run WordPress workflow
nuclei -u https://target.com -w workflows/wordpress-workflow.yaml

# Run tech detection workflow
nuclei -u https://target.com -w workflows/tech-detect-workflow.yaml
```

### Reporting
```bash
# JSON output
nuclei -u https://target.com -j -o results.json

# Markdown report
nuclei -u https://target.com -markdown-export report/

# SARIF format (for CI/CD integration)
nuclei -u https://target.com -sarif-export results.sarif
```

### Integration with Other Tools
```bash
# With subfinder
subfinder -d target.com -silent | httpx -silent | nuclei

# With naabu (port scanning)
naabu -host target.com | nuclei

# With katana (crawling)
katana -u https://target.com | nuclei
```

## Best Practices

1. **Always update templates**: Run `nuclei -update-templates` regularly
2. **Start with severity filters**: Use `-s critical,high` for initial scans
3. **Respect rate limits**: Adjust `-rl` for production systems
4. **Use tags**: Combine tags for focused scanning (`-tags cve,rce`)
5. **Exclude noise**: Use `-etags` to exclude noisy checks
6. **Monitor resources**: Use `-stats` to monitor scan progress
7. **Save results**: Always output to file with `-o` or `-j`
8. **Verify findings**: Manual verification of reported issues is essential

## Reference Files

- **references/template-syntax.md** - Complete template syntax reference
- **references/matchers.md** - Matcher types and examples
- **references/extractors.md** - Extractor usage guide
- **templates/** - Custom template examples
