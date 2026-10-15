---
name: openssl-tls
description: OpenSSL commands for certificates, TLS debugging, and encryption. Use when user mentions "openssl", "ssl certificate", "tls", "self-signed cert", "certificate chain", "CSR", "private key", "cert expiry", "https debugging", "mTLS", "certificate authority", or any certificate/encryption task.
---

# OpenSSL & TLS

Certificates, TLS debugging, and encryption from the command line.

## Generate Self-Signed Certificate

### Quick (Dev/Local)

```bash
# One-liner: key + cert, valid 365 days
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=localhost"

# With SANs (needed for Chrome to accept it)
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# EC key instead of RSA
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 \
  -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=localhost"
```

## Generate CSR and Private Key

```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate CSR from existing key
openssl req -new -key server.key -out server.csr \
  -subj "/C=US/ST=California/L=SF/O=MyOrg/CN=example.com"

# Generate key + CSR in one step
openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr \
  -subj "/C=US/ST=California/L=SF/O=MyOrg/CN=example.com"

# CSR with SANs (create config file first)
cat > san.cnf <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req

[req_distinguished_name]
CN = example.com

[v3_req]
subjectAltName = DNS:example.com,DNS:www.example.com,DNS:api.example.com
EOF

openssl req -new -key server.key -out server.csr -config san.cnf

# Verify CSR contents
openssl req -in server.csr -noout -text
```

## View Certificate Details

```bash
# Full details
openssl x509 -in cert.pem -noout -text

# Just the subject and issuer
openssl x509 -in cert.pem -noout -subject -issuer

# Expiry dates
openssl x509 -in cert.pem -noout -dates

# SANs only
openssl x509 -in cert.pem -noout -ext subjectAltName

# Serial number
openssl x509 -in cert.pem -noout -serial

# Fingerprint
openssl x509 -in cert.pem -noout -fingerprint -sha256

# From a remote server
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -text
```

## Verify Certificate Chain

```bash
# Verify against system CA bundle
openssl verify cert.pem

# Verify against specific CA
openssl verify -CAfile ca.pem cert.pem

# Verify with intermediate chain
openssl verify -CAfile ca.pem -untrusted intermediate.pem cert.pem

# Show full chain from a server
openssl s_client -connect example.com:443 -servername example.com -showcerts </dev/null 2>/dev/null
```

## Test TLS Connection (s_client)

```bash
# Basic connection test
openssl s_client -connect example.com:443 -servername example.com </dev/null

# Show only cert summary
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates

# Force specific TLS version
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Test with client cert (mTLS)
openssl s_client -connect example.com:443 \
  -cert client.pem -key client-key.pem -CAfile ca.pem

# Check supported ciphers
openssl s_client -connect example.com:443 -cipher 'ECDHE-RSA-AES256-GCM-SHA384'

# STARTTLS for mail servers
openssl s_client -connect mail.example.com:587 -starttls smtp
openssl s_client -connect mail.example.com:993 -starttls imap
```

## Check Cert Expiry

```bash
# Local cert file
openssl x509 -in cert.pem -noout -enddate

# Remote server
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -enddate

# Days until expiry (Linux)
expiry=$(openssl x509 -in cert.pem -noout -enddate | cut -d= -f2)
echo $(( ($(date -d "$expiry" +%s) - $(date +%s)) / 86400 )) days remaining

# Days until expiry (macOS)
expiry=$(openssl x509 -in cert.pem -noout -enddate | cut -d= -f2)
echo $(( ($(date -j -f "%b %d %T %Y %Z" "$expiry" +%s) - $(date +%s)) / 86400 )) days remaining
```

## Convert Between Formats

```bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER to PEM
openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem

# PEM to PKCS12 (PFX) -- combines cert + key
openssl pkcs12 -export -out cert.pfx -inkey key.pem -in cert.pem
# With chain:
openssl pkcs12 -export -out cert.pfx -inkey key.pem -in cert.pem -certfile chain.pem

# PKCS12 to PEM (extract cert)
openssl pkcs12 -in cert.pfx -clcerts -nokeys -out cert.pem

# PKCS12 to PEM (extract key)
openssl pkcs12 -in cert.pfx -nocerts -nodes -out key.pem

# PKCS12 to PEM (everything)
openssl pkcs12 -in cert.pfx -out everything.pem -nodes

# Remove passphrase from key
openssl rsa -in encrypted.key -out decrypted.key

# Add passphrase to key
openssl rsa -in decrypted.key -aes256 -out encrypted.key
```

## Create a Local CA (Dev/Testing)

```bash
# 1. Generate CA private key
openssl genrsa -out ca.key 4096

# 2. Create CA certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem \
  -subj "/C=US/ST=Dev/O=LocalCA/CN=Local Dev CA"

# 3. Generate server key
openssl genrsa -out server.key 2048

# 4. Create server CSR
openssl req -new -key server.key -out server.csr \
  -subj "/CN=myapp.local"

# 5. Sign server cert with CA (with SANs)
cat > server-ext.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment
subjectAltName = DNS:myapp.local,DNS:*.myapp.local,IP:127.0.0.1
EOF

openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial \
  -out server.crt -days 825 -sha256 -extfile server-ext.cnf

# 6. Trust the CA (macOS)
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca.pem

# 6. Trust the CA (Ubuntu/Debian)
sudo cp ca.pem /usr/local/share/ca-certificates/local-dev-ca.crt
sudo update-ca-certificates
```

## mTLS Setup Basics

```bash
# Generate client key + cert signed by same CA
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/CN=my-client"

cat > client-ext.cnf <<EOF
basicConstraints=CA:FALSE
keyUsage = digitalSignature
extendedKeyUsage = clientAuth
EOF

openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key -CAcreateserial \
  -out client.crt -days 365 -sha256 -extfile client-ext.cnf

# Test with curl
curl --cert client.crt --key client.key --cacert ca.pem https://myapp.local:8443

# Test with openssl
openssl s_client -connect myapp.local:8443 \
  -cert client.crt -key client.key -CAfile ca.pem
```

## Encrypt/Decrypt Files

```bash
# Symmetric encryption (AES-256-CBC, prompts for password)
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret.txt -out secret.enc
openssl enc -aes-256-cbc -d -pbkdf2 -in secret.enc -out secret.txt

# Encrypt with a key file
openssl rand -out filekey.bin 32
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret.txt -out secret.enc -pass file:filekey.bin
openssl enc -aes-256-cbc -d -pbkdf2 -in secret.enc -out secret.txt -pass file:filekey.bin

# Asymmetric: encrypt with public key, decrypt with private key
openssl rsautl -encrypt -inkey public.pem -pubin -in secret.txt -out secret.enc
openssl rsautl -decrypt -inkey private.pem -in secret.enc -out secret.txt
```

## Generate Random Passwords/Keys

```bash
# Random hex string (32 bytes = 64 hex chars)
openssl rand -hex 32

# Random base64 string
openssl rand -base64 32

# Random bytes to file (for encryption keys)
openssl rand -out keyfile.bin 32

# Quick password
openssl rand -base64 18
```

## Common Errors

### certificate verify failed

The client does not trust the server cert. Either the CA is missing from the trust store or the chain is incomplete.

```bash
# Check what CA the cert needs
openssl x509 -in cert.pem -noout -issuer

# Test with explicit CA
openssl s_client -connect host:443 -CAfile /path/to/ca-bundle.crt

# Quick workaround (not for prod)
curl -k https://...
# or
export NODE_TLS_REJECT_UNAUTHORIZED=0
```

### unable to get local issuer certificate

The intermediate certificate is missing. The server needs to send the full chain.

```bash
# See what chain the server sends
openssl s_client -connect host:443 -servername host -showcerts </dev/null 2>/dev/null

# If intermediate is missing, concatenate it
cat server.crt intermediate.crt > fullchain.crt
```

### certificate has expired

```bash
# Confirm expiry
echo | openssl s_client -connect host:443 2>/dev/null | openssl x509 -noout -dates
```

### certificate is not yet valid

System clock is wrong, or the cert's notBefore is in the future.

```bash
# Check cert validity window
openssl x509 -in cert.pem -noout -startdate -enddate

# Check system time
date -u
```

### handshake failure / no shared cipher

TLS version or cipher mismatch between client and server.

```bash
# Check what the server supports
openssl s_client -connect host:443 -tls1_2
openssl s_client -connect host:443 -tls1_3

# List available ciphers
openssl ciphers -v 'ALL'
```

### key values mismatch

The private key does not match the certificate.

```bash
# Compare modulus hashes -- they must match
openssl x509 -in cert.pem -noout -modulus | openssl md5
openssl rsa -in key.pem -noout -modulus | openssl md5
openssl req -in csr.pem -noout -modulus | openssl md5
```

