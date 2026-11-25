---
name: crypto-patterns
description: "When to activate: encryption, hashing, bcrypt, argon2, AES, RSA, TLS, key management, cryptography, signing"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: security
  language: security
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Cryptography Patterns

## Password Hashing

```python
# Argon2id — current best practice (winner of Password Hashing Competition)
from passlib.hash import argon2
hashed = argon2.using(memory_cost=65536, time_cost=3, parallelism=4).hash(password)
verified = argon2.verify(password, hashed)

# bcrypt — widely supported, still acceptable
from passlib.hash import bcrypt
hashed = bcrypt.using(rounds=12).hash(password)

# NEVER: MD5, SHA1, SHA256 for passwords — fast hashes are wrong here
```

## Symmetric Encryption (AES-GCM)

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Key generation — store in secrets manager, not in code
key = AESGCM.generate_key(bit_length=256)  # 32 bytes

def encrypt(key: bytes, plaintext: bytes, aad: bytes = b"") -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce — never reuse with same key
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    return nonce + ciphertext  # prepend nonce for storage

def decrypt(key: bytes, data: bytes, aad: bytes = b"") -> bytes:
    aesgcm = AESGCM(key)
    nonce, ciphertext = data[:12], data[12:]
    return aesgcm.decrypt(nonce, ciphertext, aad)

# Fernet (simpler, includes HMAC + AES-CBC — fine for most cases)
from cryptography.fernet import Fernet, MultiFernet
key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"secret data")
data = f.decrypt(token)

# Key rotation with MultiFernet
old_key = Fernet(old_key_bytes)
new_key = Fernet(new_key_bytes)
mf = MultiFernet([new_key, old_key])  # tries new first, falls back to old
```

## Asymmetric Encryption and Signing

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generate RSA key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
public_key = private_key.public_key()

# Serialize
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")
)

# Sign with RSA-PSS
signature = private_key.sign(message, padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
), hashes.SHA256())

# Verify
public_key.verify(signature, message, padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
), hashes.SHA256())

# Ed25519 — faster, smaller keys, preferred for signing
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
private_key = Ed25519PrivateKey.generate()
signature = private_key.sign(message)
private_key.public_key().verify(signature, message)
```

## Secure Random and Hashing

```python
import secrets, hashlib, hmac

# Cryptographically secure random
token = secrets.token_urlsafe(32)     # URL-safe base64 token
hex_token = secrets.token_hex(32)     # hex string
random_bytes = secrets.token_bytes(32)

# Constant-time comparison (prevent timing attacks)
if not hmac.compare_digest(provided_token, stored_token):
    raise ValueError("Invalid token")

# HMAC for message integrity
mac = hmac.new(key, message, hashlib.sha256).digest()
# Verify
if not hmac.compare_digest(mac, provided_mac):
    raise ValueError("MAC verification failed")

# SHA-256 for content hashing (not for passwords!)
content_hash = hashlib.sha256(content).hexdigest()
```

## Key Management

```python
# AWS KMS — envelope encryption
import boto3
kms = boto3.client('kms')

# Generate data key (encrypt with CMK, use DEK locally)
key_response = kms.generate_data_key(KeyId='alias/my-key', KeySpec='AES_256')
plaintext_dek = key_response['Plaintext']      # use to encrypt data
encrypted_dek = key_response['CiphertextBlob'] # store alongside data

# To decrypt: call KMS to decrypt DEK, then decrypt data locally
plaintext_dek = kms.decrypt(CiphertextBlob=encrypted_dek)['Plaintext']

# HashiCorp Vault — transit secrets engine
import hvac
client = hvac.Client(url='https://vault.internal', token=os.environ['VAULT_TOKEN'])
encrypted = client.secrets.transit.encrypt_data('my-key',
    base64.b64encode(plaintext).decode())['data']['ciphertext']
decrypted = base64.b64decode(
    client.secrets.transit.decrypt_data('my-key', encrypted)['data']['plaintext'])
```

## TLS Configuration

```nginx
# nginx — strong TLS config
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
add_header Strict-Transport-Security "max-age=63072000" always;
```
