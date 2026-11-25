---
name: nikto
description: >
  Build, operate, and interpret Nikto — a web server scanner that identifies misconfigurations,
  outdated software, dangerous files, and known CVEs across HTTP/HTTPS targets. Use when
  performing web server reconnaissance, checking for default credentials, enumerating CGI
  vulnerabilities, or validating SSL/TLS posture. Covers installation, tuning, output formats,
  authentication, evasion, plugin system, and OSVDB/CVE interpretation.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/sullo/nikto
  language: Perl
---

# nikto Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to scan a web server for known vulnerabilities, misconfigurations, or dangerous files
- Performing initial web reconnaissance on HTTP/HTTPS targets during a pentest or CTF
- Checking server banners, headers, and default content
- Validating SSL/TLS configuration weaknesses
- Running compliance-style checks against web infrastructure
- Chaining with other tools: nmap (port discovery) → nikto (web scan) → burp/zap (manual)

## What Nikto Does

Nikto is a Perl-based open-source web server scanner (sullo/nikto, ~9.2k GitHub stars) that performs
comprehensive tests against HTTP/HTTPS servers. It checks for over 6,700 potentially dangerous files
and programs, outdated server software, version-specific vulnerabilities, and server configuration
problems. Nikto is explicitly not a stealth tool — it is loud, fast, and designed for authorized
scanning where detection is not a concern.

## Installation

### apt (Kali/Debian/Ubuntu)
```bash
sudo apt update && sudo apt install -y nikto
nikto -Version
```

### From Source (latest)
```bash
git clone https://github.com/sullo/nikto.git
cd nikto/program
perl nikto.pl -Version
# Add to PATH
echo 'alias nikto="perl /opt/nikto/program/nikto.pl"' >> ~/.bashrc
```

### Docker
```bash
docker pull sullo/nikto
# Basic scan via Docker
docker run --rm sullo/nikto -h http://target.com
# With output file
docker run --rm -v $(pwd):/tmp sullo/nikto -h http://target.com -o /tmp/report.html -Format html
```

### Update Databases
```bash
nikto -update          # Update plugin and vulnerability databases
nikto -list-plugins    # List all available plugins after update
```

## Core Concepts

### Scan Database
Nikto tests are defined in `db_tests`, `db_headers`, `db_variables`, and plugin-specific databases.
Each test has a OSVDB ID (now legacy), description, and match condition. Output may reference
OSVDB IDs — cross-reference with CVE databases or vulners.com for current advisory details.

### Tuning Categories (`-T`)
Tuning controls which test categories run. Multiple values can be combined (e.g., `-T 123`):

| Code | Category |
|------|----------|
| 0    | File Upload |
| 1    | Interesting File / Seen in logs |
| 2    | Misconfiguration / Default File |
| 3    | Information Disclosure |
| 4    | Injection (XSS/Script/HTML) |
| 5    | Remote File Retrieval – Inside Web Root |
| 6    | Denial of Service |
| 7    | Remote File Retrieval – Server Wide |
| 8    | Command Execution / Remote Shell |
| 9    | SQL Injection |
| a    | Authentication Bypass |
| b    | Software Identification |
| c    | Remote Source Inclusion |
| x    | Reverse Tuning (exclude the selected categories) |

### Test IDs (`-t`)
Individual test IDs from the database; use `-t 000001` to run a single specific check.

## CLI Reference

### Basic Scanning
```bash
# Basic scan
nikto -h http://target.com

# Specify port explicitly
nikto -h target.com -p 8080

# Multiple ports
nikto -h target.com -p 80,443,8080,8443

# HTTPS target
nikto -h https://target.com
nikto -h target.com -ssl -p 443

# IPv6
nikto -h "[::1]" -p 80
```

### Tuning and Test Selection
```bash
# Only injection and SQL injection tests
nikto -h http://target.com -T 49

# Only interesting files and misconfigurations
nikto -h http://target.com -T 12

# All tests except DoS (useful for prod)
nikto -h http://target.com -T x6

# Run a specific test ID
nikto -h http://target.com -t 000398

# Mutate: guess additional filenames/directories
nikto -h http://target.com -mutate 1    # Test all files with all root dirs
nikto -h http://target.com -mutate 2    # Guess password file names
nikto -h http://target.com -mutate 3    # Enumerate user names via Apache /~user
nikto -h http://target.com -mutate 4    # Enumerate user names via cgiwrap
nikto -h http://target.com -mutate 5    # Attempt to brute force sub-domain names
nikto -h http://target.com -mutate 6    # Attempt to guess directory names from a dictionary
```

### SSL/TLS Testing
```bash
# Force SSL
nikto -h target.com -ssl

# Check SSL certificate details
nikto -h target.com -ssl -Plugins "ssl"

# Test specific TLS version support (via tuning)
nikto -h target.com -ssl -T b   # Software identification (shows TLS version)
```

### Output Formats
```bash
# Text output (default)
nikto -h http://target.com -o report.txt

# HTML report
nikto -h http://target.com -o report.html -Format html

# CSV (for spreadsheet analysis)
nikto -h http://target.com -o report.csv -Format csv

# XML (for pipeline integration)
nikto -h http://target.com -o report.xml -Format xml

# NBE (Nessus format)
nikto -h http://target.com -o report.nbe -Format nbe

# JSON (for scripting)
nikto -h http://target.com -o report.json -Format json

# Multiple formats simultaneously: run once, pipe to both
nikto -h http://target.com -o report.xml -Format xml
```

### Authentication
```bash
# HTTP Basic auth
nikto -h http://target.com -id admin:password

# Digest auth (auto-detected)
nikto -h http://target.com -id admin:password

# Cookie-based auth (inject session cookie)
nikto -h http://target.com -cookies "PHPSESSID=abc123; auth=1"

# Form-based: authenticate externally, pass cookie
# 1. Get cookie from curl/burp
# 2. Pass via -cookies flag
```

### Proxy Support
```bash
# Route through Burp Suite (for manual review)
nikto -h http://target.com -useproxy http://127.0.0.1:8080

# SOCKS proxy via proxychains
proxychains nikto -h http://target.com

# Authenticated proxy
nikto -h http://target.com -useproxy http://user:pass@proxy:8080
```

### Evasion Techniques
Evasion mode alters requests to bypass IDS/WAF signatures. Combine values (e.g., `-evasion 12`):

| Code | Technique |
|------|-----------|
| 1    | Random URI encoding (non-UTF8) |
| 2    | Directory self-reference (/./) |
| 3    | Premature URL ending |
| 4    | Prepend long random string |
| 5    | Fake parameter |
| 6    | TAB as request spacer |
| 7    | Change the case of the URL |
| 8    | Use Windows directory separator (\) |
| A    | Use carriage return (0x0d) as request spacer |
| B    | Use binary value 0x0b as request spacer |

```bash
# Case mutation + directory self-reference
nikto -h http://target.com -evasion 27

# Random encoding + fake param
nikto -h http://target.com -evasion 15
```

### Plugin System
```bash
# List all plugins
nikto -list-plugins

# Run specific plugin only
nikto -h http://target.com -Plugins "headers"
nikto -h http://target.com -Plugins "robots"
nikto -h http://target.com -Plugins "ssl"
nikto -h http://target.com -Plugins "shellshock"
nikto -h http://target.com -Plugins "apache_expect_xss"

# Run multiple plugins
nikto -h http://target.com -Plugins "headers;robots;ssl"

# Disable a plugin
nikto -h http://target.com -Plugins "-headers"
```

### Host Header Injection / Virtual Hosts
```bash
# Scan IP but send specific Host header (virtual host enumeration)
nikto -h 10.10.10.10 -vhost app.target.com

# Test all virtual hosts from a list
for vhost in $(cat vhosts.txt); do
  nikto -h 10.10.10.10 -vhost $vhost -o ${vhost}_scan.txt
done
```

### Performance and Timing
```bash
# Set timeout per request (seconds)
nikto -h http://target.com -timeout 10

# Pause between requests (seconds, float)
nikto -h http://target.com -Pause 0.5

# Display progress
nikto -h http://target.com -Display P

# Verbose output (show all 200/301/302 responses)
nikto -h http://target.com -Display V

# Debug mode (show all HTTP transactions)
nikto -h http://target.com -Display D
```

## Common Workflows

### Initial Web Recon (CTF / OSCP)
```bash
# Step 1: Quick banner grab + interesting files
nikto -h http://target.com -T 123b -o initial.txt

# Step 2: Full scan with HTML report
nikto -h http://target.com -o full_report.html -Format html

# Step 3: CGI enumeration specifically
nikto -h http://target.com -Plugins "cgi" -T 8

# Step 4: Review for CVEs — grep output
grep -i "CVE\|OSVDB\|inject\|upload\|shell" full_report.html
```

### HTTPS / SSL Assessment
```bash
nikto -h target.com -ssl -p 443 \
  -Plugins "ssl;headers" \
  -T b \
  -o ssl_report.html -Format html
```

### Scanning Multiple Targets
```bash
# From nmap XML — extract HTTP hosts
nmap -p 80,443,8080,8443 -oX nmap_web.xml 10.10.10.0/24
# Parse and feed to nikto
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('nmap_web.xml')
for host in tree.findall('.//host'):
    addr = host.find('address').get('addr')
    for port in host.findall('.//port'):
        if port.find('state').get('state') == 'open':
            print(f'http://{addr}:{port.get(\"portid\")}')
" > targets.txt

# Scan all
while read url; do
  nikto -h $url -o scan_$(echo $url | tr '/:' '_').txt &
done < targets.txt
wait
```

### CGI / Shellshock Check
```bash
nikto -h http://target.com -Plugins "shellshock" -T 8
# Also test manually
curl -A "() { :; }; echo Content-Type: text/plain; echo; /bin/id" \
  http://target.com/cgi-bin/test.cgi
```

## Interpreting Output

### OSVDB References
OSVDB (Open Source Vulnerability Database) is now offline. Cross-reference IDs using:
- `https://vulners.com/search?query=osvdb:{ID}`
- `https://www.cvedetails.com` (search description keywords)
- NVD: `https://nvd.nist.gov/vuln/search`

### Key Finding Indicators
```
+ OSVDB-XXXXX: /file.ext — Indicates known vulnerable file or path
+ Server: Apache/2.2.3  — Outdated version, check CVE list
+ /admin/: Directory indexing enabled
+ X-Frame-Options header is not set — Clickjacking vector
+ No CGI Directories found — Not a CGI attack surface
+ /phpmyadmin/: phpMyAdmin detected
+ Cookie PHPSESSID set without httponly flag
```

### Severity Interpretation
Nikto does not natively assign CVSS scores. Apply this mental model:
- **Remote code execution paths** (shellshock, file upload, command exec): Critical
- **Auth bypass, default creds**: High
- **Information disclosure** (server version, stack traces): Medium
- **Missing headers** (X-Frame-Options, CSP): Low/Informational

## Advanced Techniques

### Custom Test Database Entry
Add custom tests to `nikto/databases/db_tests`:
```
"000999","GET","/custom-path.php","200","","","Custom sensitive file check","","","",""
```
Format: `ID, method, URI, match code, match string, fail string, description, OSVDB ID, ...`

### Integrating Nikto into a Pipeline
```bash
# Run nikto → parse JSON → feed findings to nuclei for validation
nikto -h http://target.com -o out.json -Format json
cat out.json | jq -r '.vulnerabilities[].uri' | sort -u > paths.txt
nuclei -l paths.txt -t /opt/nuclei-templates/
```

### Scanning Behind a Load Balancer (Host Header Cycling)
```bash
# Identify backend servers via different responses
for ip in 10.10.10.{1..10}; do
  nikto -h $ip -vhost www.target.com -T 3b \
    -o lb_${ip}.txt 2>/dev/null &
done
wait
diff lb_10.10.10.1.txt lb_10.10.10.2.txt
```

## Integration with Other Tools

| Stage | Tool | Purpose |
|-------|------|---------|
| Port discovery | nmap | Find open HTTP/HTTPS ports before nikto |
| Traffic inspection | Burp Suite | `-useproxy` to capture all nikto requests |
| Dir bruteforce | feroxbuster/ffuf | Deeper content discovery after nikto |
| Vuln validation | nuclei | Validate CVEs nikto flags |
| Credential testing | hydra | Brute force login pages nikto finds |

```bash
# Full web recon pipeline
nmap -p- --open -T4 target.com -oG - | grep '/open' | \
  awk '{print $2}' > live_hosts.txt
nikto -h http://target.com -o nikto.xml -Format xml
feroxbuster -u http://target.com -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt
```

## Troubleshooting

**"0 hosts tested" / no output**
- Check that the target is reachable: `curl -I http://target.com`
- Verify port is correct: `nmap -p 80 target.com`
- Try with `-ssl` if getting SSL errors

**SSL handshake failures**
```bash
nikto -h target.com -ssl -nossl   # Force non-SSL even on 443
# Or: downgrade TLS version
nikto -h target.com -ssl -config nikto.conf
# Edit nikto.conf: STATIC-COOKIE= / add SSL options
```

**Proxy not working**
```bash
# Verify Burp is listening
curl --proxy http://127.0.0.1:8080 http://target.com
# Then retry nikto with same proxy
```

**Outdated database warnings**
```bash
nikto -update   # Pull latest db_* files from GitHub
```

**Rate limiting / WAF blocking**
```bash
# Add delays and evasion
nikto -h http://target.com -Pause 2 -evasion 1234 -timeout 30
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
