---
name: encryption-strategy
description: Design encryption strategy with data-at-rest, data-in-transit, and key management. Outputs encryption standards, key rotation, and compliance requirements.
argument-hint: [data sensitivity, compliance requirements, key management]
allowed-tools: Read, Write, Bash
---

# Encryption Strategy

Design comprehensive encryption for sensitive data. Not ad-hoc crypto — systematic encryption-at-rest, in-transit, and enterprise key management.

## Process

1. **Classify data.** PII, PHI, payment data, secrets, public data.
2. **Choose encryption standards.** AES-256, RSA-2048, TLS 1.3.
3. **Design key management.** HSM, KMS, key rotation, backup.
4. **Encrypt at rest.** Database encryption, file encryption, disk encryption.
5. **Encrypt in transit.** TLS/HTTPS, VPN, encrypted message queues.
6. **Implement access controls.** Who can decrypt what, when.
7. **Ensure compliance.** PCI-DSS, HIPAA, GDPR encryption requirements.

## Output Format

### Encryption Strategy: [Organization]

**Standards:** AES-256-GCM, RSA-4096, TLS 1.3  
**Key Management:** AWS KMS with automatic rotation  
**Data at Rest:** Database TDE, S3 SSE-KMS  
**Data in Transit:** TLS 1.3 minimum, HSTS enabled  
**Compliance:** PCI-DSS, HIPAA, SOC 2

---

## Encryption Standards

| Algorithm | Use Case | Key Size | Notes |
|-----------|----------|----------|-------|
| **AES-256-GCM** | Data at rest | 256-bit | NIST approved, authenticated |
| **RSA-4096** | Key exchange | 4096-bit | Secure until 2030+ |
| **ChaCha20-Poly1305** | Mobile encryption | 256-bit | Fast on ARM processors |
| **SHA-256** | Hashing | 256-bit | Passwords (with salt), integrity |
| **PBKDF2** | Password derivation | 256-bit | 100,000+ iterations |
| **Argon2** | Password hashing | 256-bit | Modern, memory-hard |

**Avoid:**
- MD5, SHA-1 (broken)
- DES, 3DES (too small)
- RC4 (weak stream cipher)
- AES-ECB mode (patterns leak)

---

## Data Classification

```
┌──────────────────┐
│   Public Data    │ → No encryption required
└──────────────────┘   (marketing content, public docs)

┌──────────────────┐
│  Internal Data   │ → Encryption in transit
└──────────────────┘   (employee directory, policies)

┌──────────────────┐
│ Confidential Data│ → Encryption at rest + transit
└──────────────────┘   (financial reports, contracts)

┌──────────────────┐
│  Sensitive Data  │ → Encryption + strict access control
└──────────────────┘   (PII, passwords, API keys)

┌──────────────────┐
│ Regulated Data   │ → Encryption + audit + compliance
└──────────────────┘   (PHI, payment data, SSN)
```

---

## Encryption at Rest

### Database Encryption (TDE - Transparent Data Encryption)

**PostgreSQL:**
```sql
-- Enable encryption
ALTER SYSTEM SET data_encryption = on;

-- Create encrypted tablespace
CREATE TABLESPACE encrypted_space
  OWNER postgres
  LOCATION '/encrypted_data'
  ENCRYPTION = on;

-- Create table in encrypted tablespace
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255),
  ssn VARCHAR(11)  -- Encrypted automatically
) TABLESPACE encrypted_space;
```

**MySQL:**
```sql
-- Enable InnoDB encryption
SET GLOBAL innodb_encrypt_tables = ON;

-- Create encrypted table
CREATE TABLE credit_cards (
  id INT PRIMARY KEY,
  card_number VARCHAR(20),
  cvv VARCHAR(4)
) ENCRYPTION='Y';

-- Rotate master key
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

### Application-Level Encryption

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class DataEncryption:
    """Encrypt sensitive fields before storing"""
    
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext):
        """Encrypt data"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        
        return self.cipher.encrypt(plaintext)
    
    def decrypt(self, ciphertext):
        """Decrypt data"""
        return self.cipher.decrypt(ciphertext).decode()

# Generate key (store in KMS)
key = Fernet.generate_key()
enc = DataEncryption(key)

# Encrypt before storing
ssn = "123-45-6789"
encrypted_ssn = enc.encrypt(ssn)

# Store encrypted_ssn in database
db.execute("INSERT INTO users (ssn) VALUES (?)", (encrypted_ssn,))

# Decrypt when reading
row = db.execute("SELECT ssn FROM users WHERE id = 1").fetchone()
decrypted_ssn = enc.decrypt(row['ssn'])
```

### S3 Encryption

```python
import boto3

s3 = boto3.client('s3')

# Server-Side Encryption with KMS
s3.put_object(
    Bucket='my-bucket',
    Key='sensitive-data.txt',
    Body=b'confidential information',
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId='arn:aws:kms:us-east-1:123456789:key/abc-123'
)

# Client-Side Encryption
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Encrypt on client
key = get_random_bytes(32)
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(b'sensitive data')

# Upload encrypted
s3.put_object(
    Bucket='my-bucket',
    Key='encrypted-data.bin',
    Body=ciphertext,
    Metadata={
        'encryption-key-id': 'key-123',  # Reference to KMS key
        'nonce': cipher.nonce.hex(),
        'tag': tag.hex()
    }
)
```

---

## Encryption in Transit

### TLS Configuration

**Nginx:**
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Certificates
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Protocols (TLS 1.3 only)
    ssl_protocols TLSv1.3;
    
    # Ciphers (strongest first)
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256';
    ssl_prefer_server_ciphers on;
    
    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Session resumption (performance)
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Database Connections (TLS)

```python
import psycopg2

# PostgreSQL with SSL
conn = psycopg2.connect(
    host="db.example.com",
    database="mydb",
    user="dbuser",
    password="password",
    sslmode="require",  # or "verify-full" for cert validation
    sslrootcert="/path/to/ca.crt",
    sslcert="/path/to/client.crt",
    sslkey="/path/to/client.key"
)
```

---

## Key Management

### AWS KMS

```python
import boto3
import base64

kms = boto3.client('kms')

# Create master key
response = kms.create_key(
    Description='Master encryption key',
    KeyUsage='ENCRYPT_DECRYPT',
    Origin='AWS_KMS'
)
key_id = response['KeyMetadata']['KeyId']

# Create alias
kms.create_alias(
    AliasName='alias/my-master-key',
    TargetKeyId=key_id
)

# Encrypt data
plaintext = b'sensitive data'
response = kms.encrypt(
    KeyId='alias/my-master-key',
    Plaintext=plaintext
)
ciphertext = response['CiphertextBlob']

# Decrypt data
response = kms.decrypt(
    CiphertextBlob=ciphertext
)
decrypted = response['Plaintext']

# Generate data key (envelope encryption)
response = kms.generate_data_key(
    KeyId='alias/my-master-key',
    KeySpec='AES_256'
)

plaintext_key = response['Plaintext']  # Use this to encrypt data
encrypted_key = response['CiphertextBlob']  # Store this with data
```

### Envelope Encryption

```
1. Generate data encryption key (DEK) from KMS
2. Encrypt data with DEK
3. Encrypt DEK with master key (from KMS)
4. Store encrypted data + encrypted DEK together
5. To decrypt: decrypt DEK with KMS, then decrypt data with DEK

Benefits:
- Fast (bulk encryption with DEK, not KMS API)
- Secure (DEK never stored plaintext)
- Key rotation (re-encrypt DEK, not all data)
```

```python
def envelope_encrypt(data, kms_key_id):
    """Encrypt data using envelope encryption"""
    
    # Generate data key
    response = kms.generate_data_key(
        KeyId=kms_key_id,
        KeySpec='AES_256'
    )
    
    plaintext_key = response['Plaintext']
    encrypted_key = response['CiphertextBlob']
    
    # Encrypt data with data key
    cipher = AESGCM(plaintext_key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, data, None)
    
    return {
        'ciphertext': ciphertext,
        'encrypted_key': encrypted_key,
        'nonce': nonce
    }

def envelope_decrypt(encrypted_data):
    """Decrypt data using envelope encryption"""
    
    # Decrypt data key with KMS
    response = kms.decrypt(
        CiphertextBlob=encrypted_data['encrypted_key']
    )
    plaintext_key = response['Plaintext']
    
    # Decrypt data with data key
    cipher = AESGCM(plaintext_key)
    plaintext = cipher.decrypt(
        encrypted_data['nonce'],
        encrypted_data['ciphertext'],
        None
    )
    
    return plaintext
```

---

## Key Rotation

### Automatic Rotation (AWS KMS)

```python
# Enable automatic rotation (every year)
kms.enable_key_rotation(KeyId=key_id)

# Check rotation status
response = kms.get_key_rotation_status(KeyId=key_id)
print(f"Rotation enabled: {response['KeyRotationEnabled']}")

# Note: Old ciphertexts still decryptable with old key versions
```

### Manual Rotation

```python
def rotate_encryption_key():
    """Rotate application-level encryption key"""
    
    # 1. Generate new key
    new_key = Fernet.generate_key()
    
    # 2. Store new key with version
    store_key(new_key, version=2)
    
    # 3. Re-encrypt all data
    for record in db.execute("SELECT id, encrypted_field FROM sensitive_data"):
        # Decrypt with old key
        old_cipher = Fernet(get_key(version=1))
        plaintext = old_cipher.decrypt(record['encrypted_field'])
        
        # Encrypt with new key
        new_cipher = Fernet(new_key)
        new_ciphertext = new_cipher.encrypt(plaintext)
        
        # Update record
        db.execute(
            "UPDATE sensitive_data SET encrypted_field = ?, key_version = 2 WHERE id = ?",
            (new_ciphertext, record['id'])
        )
    
    # 4. Mark old key as deprecated
    deprecate_key(version=1)
```

---

## Password Hashing

```python
import bcrypt
from argon2 import PasswordHasher

# Bcrypt (older, still secure)
password = b"user_password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# Verify
if bcrypt.checkpw(password, hashed):
    print("Password correct")

# Argon2 (modern, recommended)
ph = PasswordHasher()
hash = ph.hash("user_password")

# Verify
try:
    ph.verify(hash, "user_password")
    print("Password correct")
except:
    print("Invalid password")

# Check if rehash needed (parameters changed)
if ph.check_needs_rehash(hash):
    new_hash = ph.hash("user_password")
    update_user_password(new_hash)
```

**Parameters:**
```python
# Argon2 configuration
ph = PasswordHasher(
    time_cost=3,        # Number of iterations
    memory_cost=65536,  # Memory in KB (64 MB)
    parallelism=4,      # Number of threads
    hash_len=32,        # Hash output length
    salt_len=16         # Salt length
)
```

---

## Certificate Management

### Let's Encrypt (Automated)

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d example.com -d www.example.com

# Auto-renewal (runs daily)
certbot renew --dry-run

# Renewal hook (reload nginx)
certbot renew --deploy-hook "systemctl reload nginx"
```

### Certificate Pinning (Mobile Apps)

```swift
// iOS certificate pinning
class NetworkManager {
    func pinCertificate(challenge: URLAuthenticationChallenge) -> URLSession.AuthChallengeDisposition {
        guard let serverTrust = challenge.protectionSpace.serverTrust,
              let certificate = SecTrustGetCertificateAtIndex(serverTrust, 0) else {
            return .cancelAuthenticationChallenge
        }
        
        let remoteCertData = SecCertificateCopyData(certificate) as Data
        let localCertData = loadCertificateFromBundle()
        
        if remoteCertData == localCertData {
            return .useCredential
        } else {
            return .cancelAuthenticationChallenge
        }
    }
}
```

---

## Compliance Requirements

### PCI-DSS (Payment Card Industry)
- Encrypt cardholder data at rest (AES-256)
- TLS 1.2+ for transmission
- Key rotation every year
- Access logs for encrypted data

### HIPAA (Health Insurance)
- Encrypt PHI (Protected Health Information)
- Encryption algorithm documented
- Access controls on decryption keys
- Business associate agreements

### GDPR (General Data Protection Regulation)
- Encryption recommended (not mandatory)
- "Pseudonymization and encryption" as safeguard
- Breach notification within 72 hours
- Data portability in encrypted format

---

## Monitoring & Auditing

```python
from prometheus_client import Counter

# Metrics
encryption_operations = Counter(
    'encryption_operations_total',
    'Total encryption/decryption operations',
    ['operation', 'status']  # encrypt/decrypt, success/failure
)

key_rotations = Counter(
    'key_rotations_total',
    'Total key rotations',
    ['key_id']
)

# Log all decryption attempts
def decrypt_with_audit(ciphertext, user_id):
    try:
        plaintext = decrypt(ciphertext)
        
        encryption_operations.labels(operation='decrypt', status='success').inc()
        
        audit_log.info({
            'action': 'decrypt',
            'user_id': user_id,
            'timestamp': datetime.now(),
            'success': True
        })
        
        return plaintext
    
    except Exception as e:
        encryption_operations.labels(operation='decrypt', status='failure').inc()
        
        audit_log.warning({
            'action': 'decrypt',
            'user_id': user_id,
            'error': str(e),
            'success': False
        })
        
        raise
```

## Rules

- AES-256-GCM for data at rest — authenticated encryption prevents tampering.
- TLS 1.3 minimum for data in transit — TLS 1.0/1.1 deprecated, 1.2 acceptable but upgrading.
- Envelope encryption for large data — encrypt data with DEK, encrypt DEK with master key.
- KMS for key management, not application code — centralized, auditable, hardware-backed.
- Rotate keys annually minimum — compromised keys limited exposure window.
- Argon2 or bcrypt for passwords — memory-hard, resistant to GPU cracking.
- Never roll your own crypto — use audited libraries (OpenSSL, cryptography.io, NaCl).
- Encrypt PII, payment data, and secrets always — regulatory requirement and security best practice.
- Certificate pinning for mobile apps — prevent man-in-the-middle with fake certificates.
- Audit all decryption operations — who decrypted what and when for compliance.
