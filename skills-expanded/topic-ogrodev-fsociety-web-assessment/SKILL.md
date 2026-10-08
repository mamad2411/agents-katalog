---
name: web-assessment
description: |
  This skill activates when the user mentions "XSS", "cross-site scripting", "reflected XSS",
  "stored XSS", "DOM XSS", "blind XSS", "SQL injection", "SQLi", "blind SQLi", "union injection",
  "error-based injection", "time-based injection", "stacked queries", "second-order injection",
  "SSRF", "server-side request forgery", "cloud metadata", "IMDS", "internal service access",
  "IDOR", "insecure direct object reference", "broken access control", "horizontal privilege",
  "vertical privilege", "BOLA", "BFLA", "object-level authorization",
  "LFI", "local file inclusion", "RFI", "remote file inclusion", "path traversal",
  "directory traversal", "file read", "arbitrary file read", "dot dot slash",
  "command injection", "OS command injection", "RCE", "remote code execution",
  "code injection", "code execution", "reverse shell", "web shell",
  "SSTI", "server-side template injection", "template injection", "Jinja2 injection",
  "Twig injection", "Freemarker injection", "Velocity injection", "Pebble injection",
  "XXE", "XML external entity", "XML injection", "DTD injection", "XML parser",
  "NoSQL injection", "NoSQLi", "MongoDB injection", "operator injection",
  "authentication bypass", "auth bypass", "login bypass", "password reset",
  "account takeover", "session fixation", "session hijacking", "JWT attack",
  "JWT forgery", "token manipulation", "brute force login", "credential stuffing",
  "web vulnerability", "web application testing", "web pentest", "web assessment",
  "injection testing", "parameter fuzzing", "input validation", "OWASP",
  "OWASP Top 10", "A01 broken access", "A03 injection",
  "API testing", "REST API", "GraphQL injection", "parameter tampering",
  "mass assignment", "rate limiting", "race condition", "TOCTOU",
  "open redirect", "CRLF injection", "HTTP header injection",
  "deserialization", "insecure deserialization", "object injection",
  "file upload", "unrestricted upload", "web shell upload",
  "CORS misconfiguration", "CSP bypass", "clickjacking",
  "subdomain takeover", "host header injection",
  "nuclei scan", "sqlmap", "dalfox", "ffuf", "burp", "web scanner",
  "vulnerability scanner", "web fuzzing", "parameter discovery",
  or discusses testing web application security, exploiting web vulnerabilities,
  or performing web application penetration testing.
version: 2.0.0
---

# Web Vulnerability Assessment

Systematic identification and exploitation of web application vulnerabilities. This skill provides structured workflows for every major web vulnerability class, routing you to the correct Hexstrike MCP tools and Kali tooling with proper parameters. Stop guessing at payloads and tool flags -- use the right tool for the right vuln class.

## Why Structured Web Assessment Matters

Web applications are the primary attack surface in most engagements. A single SQLi grants database access. An SSRF leaks cloud credentials. An SSTI yields RCE. Structured testing ensures you cover every class systematically instead of ad-hoc fuzzing. Every finding feeds the findings-tracker and chain-detector for automatic exploit chain discovery.

## Triage and Prioritization

Before testing anything, determine what you are dealing with. Target type dictates testing priority.

### Priority Matrix by Target Type

| Target Type | Test First | Test Second | Test Third |
|-------------|-----------|-------------|------------|
| **PHP app** | SQLi, LFI/RFI, SSTI (Twig), RCE, file upload | XSS, IDOR, auth bypass | SSRF, XXE |
| **Java/Spring** | SQLi, SSTI (Freemarker/Velocity), XXE, deserialization | SSRF, IDOR, auth bypass | XSS, NoSQLi |
| **Node.js/Express** | NoSQLi, SSTI (Pug/EJS), prototype pollution, RCE | SSRF, IDOR, auth bypass | XSS, SQLi |
| **Python/Django/Flask** | SSTI (Jinja2), SQLi, RCE, SSRF | IDOR, auth bypass | XSS, XXE |
| **Ruby on Rails** | SQLi, SSTI (ERB), deserialization, mass assignment | SSRF, IDOR, auth bypass | XSS, XXE |
| **API-only (REST)** | IDOR/BOLA, auth bypass, SQLi/NoSQLi, mass assignment | SSRF, rate limit bypass | injection via headers |
| **API-only (GraphQL)** | Introspection, query depth abuse, batching attacks | IDOR, auth bypass, injection | DoS via nested queries |
| **WordPress** | See waf-bypass + wordpress-hacking skills | SQLi via plugins, file upload | XSS, SSRF |
| **Cloud-hosted** | SSRF (IMDS), config leaks, auth bypass | SQLi/NoSQLi, IDOR | RCE, XSS |

### Quick Stack Fingerprinting

Before deep testing, identify the stack:

```bash
# Broad fingerprinting with nuclei
nuclei_scan target="https://target.com" templates="technologies/" severity="info"

# Check response headers for framework hints
# X-Powered-By, Server, X-AspNet-Version, X-Generator, Set-Cookie names
```

Log stack information as target intel:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" tech-stack framework "Laravel 10" --source "response-headers"
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" defense waf "Cloudflare" --source "wafw00f"
```

## Testing Workflow

Follow this workflow for each target. Steps are ordered for maximum efficiency -- early findings inform later tests.

### Step 1 — Reconnaissance and Surface Mapping

Map the attack surface before testing individual vuln classes.

```bash
# Discover parameters and endpoints
ffuf -u "https://target.com/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -mc 200,301,302,403 -o recon.json

# Parameter discovery on known endpoints
paramspider -d target.com

# Technology detection
nuclei_scan target="https://target.com" templates="technologies/" severity="info"
```

If behind a WAF, detect it first:

```bash
wafw00f_scan target="https://target.com"
```

Log defenses:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" defense waf "Cloudflare" --source "wafw00f"
```

### Step 2 — Broad Vulnerability Scanning

Run automated scanners across all vuln classes to find low-hanging fruit.

```bash
# Nuclei with critical/high templates
nuclei_scan target="https://target.com" severity="critical,high,medium"

# Jaeles signature-based scanning
jaeles_vulnerability_scan target="https://target.com"

# AI-powered vulnerability assessment
ai_vulnerability_assessment target="https://target.com"
```

Load Hexstrike tools first:

```
ToolSearch → "+hexstrike nuclei" or "select:mcp__hexstrike-ai__nuclei_scan"
ToolSearch → "+hexstrike sqlmap" or "select:mcp__hexstrike-ai__sqlmap_scan"
ToolSearch → "+hexstrike dalfox" or "select:mcp__hexstrike-ai__dalfox_xss_scan"
```

### Step 3 — Targeted Vulnerability Testing

Based on scanner results and stack fingerprinting, test each relevant vuln class. Use the decision tree below to route to the correct reference.

### Step 4 — Chain Detection

After logging findings, run chain detection to discover multi-step exploit paths:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/chain-detector.js
```

The chain detector matches finding combinations into exploit chains. For example: SSRF + cloud metadata → credential theft, or SQLi + file write → RCE.

### Step 5 — Exploitation and Proof

For confirmed vulns, build proof-of-concept exploits. Document impact clearly for the report.

## Vulnerability Class Decision Tree

Use this to pick the right testing approach for each class. Each class has a dedicated reference document.

### Injection Vulnerabilities

| Class | Primary Tool | Reference | Vuln Type | Quick Indicator |
|-------|-------------|-----------|-----------|-----------------|
| **SQL Injection** | `sqlmap_scan` | `references/sqli-testing.md` | `sqli` | Error messages with SQL syntax, different responses for `' OR 1=1--` vs `' OR 1=2--` |
| **XSS** | `dalfox_xss_scan` | `references/xss-testing.md` | `xss` | Input reflected in response HTML without encoding |
| **SSTI** | `ai_generate_payload` | `references/ssti-testing.md` | `ssti` | `{{7*7}}` returns `49` in response |
| **XXE** | `http_repeater` | `references/xxe-testing.md` | `xxe` | XML content type accepted, DTD processing enabled |
| **NoSQL Injection** | `http_intruder` | `references/nosqli-testing.md` | `nosqli` | MongoDB-style parameters, JSON body injection |
| **Command Injection** | `ai_generate_payload` | `references/rce-testing.md` | `cmdi` | Time delay with `sleep` or `ping`, DNS callback |
| **RCE** | varies | `references/rce-testing.md` | `rce` | Direct code execution via any vector |

### Access Control Vulnerabilities

| Class | Primary Tool | Reference | Vuln Type | Quick Indicator |
|-------|-------------|-----------|-----------|-----------------|
| **IDOR** | `http_repeater` | `references/idor-testing.md` | `idor` | Sequential/guessable IDs in URLs or request bodies |
| **Auth Bypass** | `http_repeater` | `references/auth-testing.md` | `auth-bypass` | Missing auth checks on endpoints, JWT manipulation |

### Server-Side Vulnerabilities

| Class | Primary Tool | Reference | Vuln Type | Quick Indicator |
|-------|-------------|-----------|-----------|-----------------|
| **SSRF** | `http_repeater` | `references/ssrf-testing.md` | `ssrf` | URL parameters, redirect/callback fields, file import |
| **LFI/RFI** | `dotdotpwn_scan` | `references/ssrf-testing.md` | `lfi`/`rfi` | File path parameters, include functions, wrapper protocols |

## Tool Routing

### Hexstrike MCP Tools

| Tool | Best For | Load With |
|------|----------|-----------|
| `sqlmap_scan` | SQL injection detection + exploitation | `select:mcp__hexstrike-ai__sqlmap_scan` |
| `dalfox_xss_scan` | XSS scanning with DOM analysis + WAF bypass | `select:mcp__hexstrike-ai__dalfox_xss_scan` |
| `xsser_scan` | Focused XSS with encoding control | `select:mcp__hexstrike-ai__xsser_scan` |
| `nuclei_scan` | Broad vuln scanning with templates | `select:mcp__hexstrike-ai__nuclei_scan` |
| `jaeles_vulnerability_scan` | Signature-based web vuln scanning | `select:mcp__hexstrike-ai__jaeles_vulnerability_scan` |
| `dotdotpwn_scan` | Path traversal / LFI scanning | `select:mcp__hexstrike-ai__dotdotpwn_scan` |
| `ai_generate_payload` | Custom payload generation for any vuln type | `select:mcp__hexstrike-ai__ai_generate_payload` |
| `ai_vulnerability_assessment` | AI-powered vulnerability assessment | `select:mcp__hexstrike-ai__ai_vulnerability_assessment` |
| `advanced_payload_generation` | WAF-evasion-aware payloads | `select:mcp__hexstrike-ai__advanced_payload_generation` |
| `http_repeater` | Manual request replay and modification | `select:mcp__hexstrike-ai__http_repeater` |
| `http_intruder` | Parameter fuzzing and enumeration | `select:mcp__hexstrike-ai__http_intruder` |
| `wafw00f_scan` | WAF detection and fingerprinting | `select:mcp__hexstrike-ai__wafw00f_scan` |

### Kali CLI Tools

| Tool | Install | Best For |
|------|---------|----------|
| `sqlmap` | Pre-installed | SQLi exploitation (alternative to MCP) |
| `ffuf` | `apt install ffuf` | Directory/parameter fuzzing |
| `nuclei` | `go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` | Template-based scanning |
| `wfuzz` | Pre-installed | Web fuzzing with advanced filtering |
| `gobuster` | Pre-installed | Directory/DNS enumeration |
| `nikto` | Pre-installed | Web server scanner |
| `whatweb` | Pre-installed | Technology fingerprinting |
| `commix` | Pre-installed | Command injection exploitation |
| `tplmap` | `pip install tplmap` | SSTI exploitation |
| `xxeinjector` | GitHub | XXE exploitation |
| `nosqlmap` | `pip install nosqlmap` | NoSQL injection |
| `jwt_tool` | `pip install jwt_tool` | JWT testing and forgery |
| `hydra` | Pre-installed | Brute force authentication |
| `patator` | Pre-installed | Multi-protocol brute forcer |

## WAF Considerations

If a WAF is detected, adapt your approach:

1. Run `wafw00f_scan` to identify the specific WAF
2. Use `advanced_payload_generation` for evasion-aware payloads
3. Adjust scan speed and aggressiveness (see scan profile)
4. Consider the waf-bypass skill for detailed bypass strategies

WAF-specific tamper scripts for sqlmap:

| WAF | Tamper Scripts |
|-----|----------------|
| Cloudflare | `between,randomcase,space2comment` |
| ModSecurity | `space2comment,between,charencode` |
| AWS WAF | `space2comment,randomcase,percentage` |
| Imperva | `between,bluecoat,percentage` |
| Akamai | `space2comment,between,charencode,randomcase` |
| Generic | `apostrophemask,equaltolike,space2dash` |

## Recording Findings

Log every confirmed vulnerability immediately:

```bash
# Add a finding
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "<endpoint>" "<vuln-type>" "<param>" "<severity>" "<title>"

# Examples
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "/api/users?id=1" sqli "id" CRITICAL "Union-based SQL injection in user lookup"

node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "/search" xss "q" MEDIUM "Reflected XSS in search parameter"

node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "/api/profile/123" idor "id" HIGH "Horizontal IDOR in user profile endpoint"
```

### Severity Classification for Web Vulns

| Severity | Criteria | Examples |
|----------|----------|----------|
| `CRITICAL` | Direct RCE, full database access, admin account takeover, cloud credential theft | SQLi with data extraction, SSTI→RCE, SSRF→IMDS, command injection |
| `HIGH` | Significant data access, account compromise, privilege escalation | Blind SQLi, stored XSS on admin panel, IDOR exposing PII, auth bypass |
| `MEDIUM` | Limited data access, requires interaction, partial impact | Reflected XSS, CSRF, information disclosure, IDOR on non-sensitive data |
| `LOW` | Minimal direct impact, defense-in-depth issue | Missing security headers, verbose errors, directory listing |
| `INFO` | Informational, no direct exploit | Technology disclosure, version information, default pages |

### Log Techniques

Record every tool/technique used for coverage tracking:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  "sqlmap" "target.com/api/users" "union-based-sqli" "success" \
  --report "reports/sqlmap_users.json" \
  --notes "MySQL 5.7, 3 databases found"
```

## OPSEC and Scan Profile Integration

Adapt testing intensity to the current scan profile:

| Profile | Approach | Timing |
|---------|----------|--------|
| `loud` | Full automation, parallel scans, no delays | No restrictions |
| `normal` | Sequential scans, standard timing | Default tool settings |
| `stealth` | Manual testing preferred, careful automation | 2-5s between requests |
| `paranoid` | Manual only, single requests, full Tor/VPN | 10-30s between requests, rotate IPs |

Check current profile:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/scan-profile.js show
```

## References

| Reference | Coverage |
|-----------|----------|
| `references/sqli-testing.md` | SQL injection: detection, exploitation, WAF bypass, DBMS-specific techniques, blind methods, second-order |
| `references/xss-testing.md` | XSS: reflected, stored, DOM, blind, payload contexts, WAF evasion, CSP bypass, exploitation |
| `references/ssrf-testing.md` | SSRF: cloud metadata, protocol smuggling, filter bypass, blind SSRF, chaining, LFI/RFI |
| `references/idor-testing.md` | IDOR: horizontal/vertical, BOLA/BFLA, UUID bypass, mass assignment, GraphQL IDOR, API testing |
| `references/ssti-testing.md` | SSTI: template engine detection, Jinja2/Twig/Freemarker/Velocity/Pebble exploitation, sandbox escape, RCE |
| `references/xxe-testing.md` | XXE: classic/blind/error-based, OOB exfiltration, SSRF via XXE, file read, RCE, parser-specific attacks |
| `references/rce-testing.md` | RCE: command injection, code injection, deserialization, file upload, SSTI→RCE, chained RCE |
| `references/nosqli-testing.md` | NoSQLi: MongoDB operator injection, auth bypass, data extraction, blind NoSQLi, aggregation abuse |
| `references/auth-testing.md` | Auth: login bypass, JWT attacks, session management, password reset, 2FA bypass, OAuth flaws, brute force |
