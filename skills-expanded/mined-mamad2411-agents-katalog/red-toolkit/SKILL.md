---
name: red-toolkit
description: Consolidated toolkit for red. Covers red-team-tools, red-team-tactics
---
# Red Toolkit

## Core Capabilities
# Red Toolkit

# Red Team Tools and Methodology

## Purpose

Implement proven methodologies and tool workflows from top security researchers for effective reconnaissance, vulnerability discovery, and bug bounty hunting. Automate common tasks while maintaining thorough coverage of attack surfaces.

## Inputs/Prerequisites

- Target scope definition (domains, IP ranges, applications)
- Linux-based attack machine (Kali, Ubuntu)
- Bug bounty program rules and scope
- Tool dependencies installed (Go, Python, Ruby)
- API keys for various services (Shodan, Censys, etc.)

## Outputs/Deliverables

- Comprehensive subdomain enumeration
- Live host discovery and technology fingerprinting
- Identified vulnerabilities and attack vectors
- Automated recon pipeline outputs
- Documented findings for reporting

## Core Workflow

### 1. Project Tracking and Acquisitions

Set up reconnaissance tracking:

```bash
# Create project structure
mkdir -p target/{recon,vulns,reports}
cd target

# Find acquisitions using Crunchbase
# Search manually for subsidiary companies

# Get ASN for targets
amass intel -org "Target Company" -src

# Alternative ASN lookup
curl -s "https://bgp.he.net/search?search=targetcompany&commit=Search"
```

### 2. Subdomain Enumeration

Comprehensive subdomain discovery:

```bash
# Create wildcards file
echo "target.com" > wildcards

# Run Amass passively
amass enum -passive -d target.com -src -o amass_passive.txt

# Run Amass actively
amass enum -active -d target.com -src -o amass_active.txt

# Use Subfinder
subfinder -d target.com -silent -o subfinder.txt

# Asset discovery
cat wildcards | assetfinder --subs-only | anew domains.txt

# Alternative subdomain tools
findomain -t target.com -o

# Generate permutations with dnsgen
cat domains.txt | dnsgen - | httprobe > permuted.txt

# Combine all sources
cat amass_*.txt subfinder.txt | sort -u > all_subs.txt
```

### 3. Live Host Discovery

Identify responding hosts:

```bash
# Check which hosts are live with httprobe
cat domains.txt | httprobe -c 80 --prefer-https | anew hosts.txt

# Use httpx for more details
cat domains.txt | httpx -title -tech-detect -status-code -o live_hosts.txt

# Alternative with massdns
massdns -r resolvers.txt -t A -o S domains.txt > resolved.txt
```

### 4. Technology Fingerprinting

Identify technologies for targeted attacks:

```bash
# Whatweb scanning
whatweb -i hosts.txt -a 3 -v > tech_stack.txt

# Nuclei technology detection
nuclei -l hosts.txt -t technologies/ -o tech_nuclei.txt

# Wappalyzer (if available)
# Browser extension for manual review
```

### 5. Content Discovery

Find hidden endpoints and files:

```bash
# Directory bruteforce with ffuf
ffuf -ac -v -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

# Historical URLs from Wayback
waybackurls target.com | tee wayback.txt

# Find all URLs with gau
gau target.com | tee all_urls.txt

# Parameter discovery
cat all_urls.txt | grep "=" | sort -u > params.txt

# Generate custom wordlist from historical data
cat all_urls.txt | unfurl paths | sort -u > custom_wordlist.txt
```

### 6. Application Analysis (Jason Haddix Method)

**Heat Map Priority Areas:**

1. **File Uploads** - Test for injection, XXE, SSRF, shell upload
2. **Content Types** - Filter Burp for multipart forms
3. **APIs** - Look for hidden methods, lack of auth
4. **Profile Sections** - Stored XSS, custom fields
5. **Integrations** - SSRF through third parties
6. **Error Pages** - Exotic injection points

**Analysis Questions:**
- How does the app pass data? (Params, API, Hybrid)
- Where does the app talk about users? (UID, UUID endpoints)
- Does the site have multi-tenancy or user levels?
- Does it have a unique threat model?
- How does the site handle XSS/CSRF?
- Has the site had past writeups/exploits?

### 7. Automated XSS Hunting

```bash
# ParamSpider for parameter extraction
python3 paramspider.py --domain target.com -o params.txt

# Filter with Gxss
cat params.txt | Gxss -p test

# Dalfox for XSS testing
cat params.txt | dalfox pipe --mining-dict params.txt -o xss_results.txt

# Alternative workflow
waybackurls target.com | grep "=" | qsreplace '"><script>alert(1)</script>' | while read url; do
    curl -s "$url" | grep -q 'alert(1)' && echo "$url"
done > potential_xss.txt
```

### 8. Vulnerability Scanning

```bash
# Nuclei comprehensive scan
nuclei -l hosts.txt -t ~/nuclei-templates/ -o nuclei_results.txt

# Check for common CVEs
nuclei -l hosts.txt -t cves/ -o cve_results.txt

# Web vulnerabilities
nuclei -l hosts.txt -t vulnerabilities/ -o vuln_results.txt
```

### 9. API Enumeration

**Wordlists for API fuzzing:**

```bash
# Enumerate API endpoints
ffuf -u https://target.com/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt

# Test API versions
ffuf -u https://target.com/api/v1/FUZZ -w api_wordlist.txt
ffuf -u https://target.com/api/v2/FUZZ -w api_wordlist.txt

# Check for hidden methods
for method in GET POST PUT DELETE PATCH; do
    curl -X $method https://target.com/api/users -v
done
```

### 10. Automated Recon Script

```bash
#!/bin/bash
domain=$1

if [[ -z $domain ]]; then
    echo "Usage: ./recon.sh <domain>"
    exit 1
fi

mkdir -p "$domain"

# Subdomain enumeration
echo "[*] Enumerating subdomains..."
subfinder -d "$domain" -silent > "$domain/subs.txt"

# Live host discovery
echo "[*] Finding live hosts..."
cat "$domain/subs.txt" | httpx -title -tech-detect -status-code > "$domain/live.txt"

# URL collection
echo "[*] Collecting URLs..."
cat "$domain/live.txt" | waybackurls > "$domain/urls.txt"

# Nuclei scanning
echo "[*] Running Nuclei..."
nuclei -l "$domain/live.txt" -o "$domain/nuclei.txt"

echo "[+] Recon complete!"
```

## Quick Reference

### Essential Tools

| Tool | Purpose |
|------|---------|
| Amass | Subdomain enumeration |
| Subfinder | Fast subdomain discovery |
| httpx/httprobe | Live host detection |
| ffuf | Content discovery |
| Nuclei | Vulnerability scanning |
| Burp Suite | Manual testing |
| Dalfox | XSS automation |
| waybackurls | Historical URL mining |

### Key API Endpoints to Check

```
/api/v1/users
/api/v1/admin
/api/v1/profile
/api/users/me
/api/config
/api/debug
/api/swagger
/api/graphql
```

### XSS Filter Testing

```html
<!-- Test encoding handling -->
<h1><img><table>
<script>
%3Cscript%3E
%253Cscript%253E
%26lt;script%26gt;
```

## Constraints

- Respect program scope boundaries
- Avoid DoS or fuzzing on production without permission
- Rate limit requests to avoid blocking
- Some tools may generate false positives
- API keys required for full functionality of some tools

## Examples

### Example 1: Quick Subdomain Recon

```bash
subfinder -d target.com | httpx -title | tee results.txt
```

### Example 2: XSS Hunting Pipeline

```bash
waybackurls target.com | grep "=" | qsreplace "test" | httpx -silent | dalfox pipe
```

### Example 3: Comprehensive Scan

```bash
# Full recon chain
amass enum -d target.com | httpx | nuclei -t ~/nuclei-templates/
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limited | Use proxy rotation, reduce concurrency |
| Too many results | Focus on specific technology stacks |
| False positives | Manually verify findings before reporting |
| Missing subdomains | Combine multiple enumeration sources |
| API key errors | Verify keys in config files |
| Tools not found | Install Go tools with `go install` |

---

# Red Team Tactics

> Adversary simulation principles based on MITRE ATT&CK framework.

---

## 1. MITRE ATT&CK Phases

### Attack Lifecycle

```
RECONNAISSANCE → INITIAL ACCESS → EXECUTION → PERSISTENCE
       ↓              ↓              ↓            ↓
   PRIVILEGE ESC → DEFENSE EVASION → CRED ACCESS → DISCOVERY
       ↓              ↓              ↓            ↓
LATERAL MOVEMENT → COLLECTION → C2 → EXFILTRATION → IMPACT
```

### Phase Objectives

| Phase | Objective |
|-------|-----------|
| **Recon** | Map attack surface |
| **Initial Access** | Get first foothold |
| **Execution** | Run code on target |
| **Persistence** | Survive reboots |
| **Privilege Escalation** | Get admin/root |
| **Defense Evasion** | Avoid detection |
| **Credential Access** | Harvest credentials |
| **Discovery** | Map internal network |
| **Lateral Movement** | Spread to other systems |
| **Collection** | Gather target data |
| **C2** | Maintain command channel |
| **Exfiltration** | Extract data |

---

## 2. Reconnaissance Principles

### Passive vs Active

| Type | Trade-off |
|------|-----------|
| **Passive** | No target contact, limited info |
| **Active** | Direct contact, more detection risk |

### Information Targets

| Category | Value |
|----------|-------|
| Technology stack | Attack vector selection |
| Employee info | Social engineering |
| Network ranges | Scanning scope |
| Third parties | Supply chain attack |

---

## 3. Initial Access Vectors

### Selection Criteria

| Vector | When to Use |
|--------|-------------|
| **Phishing** | Human target, email access |
| **Public exploits** | Vulnerable services exposed |
| **Valid credentials** | Leaked or cracked |
| **Supply chain** | Third-party access |

---

## 4. Privilege Escalation Principles

### Windows Targets

| Check | Opportunity |
|-------|-------------|
| Unquoted service paths | Write to path |
| Weak service permissions | Modify service |
| Token privileges | Abuse SeDebug, etc. |
| Stored credentials | Harvest |

### Linux Targets

| Check | Opportunity |
|-------|-------------|
| SUID binaries | Execute as owner |
| Sudo misconfiguration | Command execution |
| Kernel vulnerabilities | Kernel exploits |
| Cron jobs | Writable scripts |

---

## 5. Defense Evasion Principles

### Key Techniques

| Technique | Purpose |
|-----------|---------|
| LOLBins | Use legitimate tools |
| Obfuscation | Hide malicious code |
| Timestomping | Hide file modifications |
| Log clearing | Remove evidence |

### Operational Security

- Work during business hours
- Mimic legitimate traffic patterns
- Use encrypted channels
- Blend with normal behavior

---

## 6. Lateral Movement Principles

### Credential Types

| Type | Use |
|------|-----|
| Password | Standard auth |
| Hash | Pass-the-hash |
| Ticket | Pass-the-ticket |
| Certificate | Certificate auth |

### Movement Paths

- Admin shares
- Remote services (RDP, SSH, WinRM)
- Exploitation of internal services

---

## 7. Active Directory Attacks

### Attack Categories

| Attack | Target |
|--------|--------|
| Kerberoasting | Service account passwords |
| AS-REP Roasting | Accounts without pre-auth |
| DCSync | Domain credentials |
| Golden Ticket | Persistent domain access |

---

## 8. Reporting Principles

### Attack Narrative

Document the full attack chain:
1. How initial access was gained
2. What techniques were used
3. What objectives were achieved
4. Where detection failed

### Detection Gaps

For each successful technique:
- What should have detected it?
- Why didn't detection work?
- How to improve detection

---

## 9. Ethical Boundaries

### Always

- Stay within scope
- Minimize impact
- Report immediately if real threat found
- Document all actions

### Never

- Destroy production data
- Cause denial of service (unless scoped)
- Access beyond proof of concept
- Retain sensitive data

---

## 10. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Rush to exploitation | Follow methodology |
| Cause damage | Minimize impact |
| Skip reporting | Document everything |
| Ignore scope | Stay within boundaries |

---

> **Remember:** Red team simulates attackers to improve defenses, not to cause harm.

---
