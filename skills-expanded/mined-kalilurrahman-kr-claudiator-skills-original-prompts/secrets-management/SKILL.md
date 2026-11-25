---
name: secrets-management
description: Design secrets management with Vault, AWS Secrets Manager, encrypted storage. Outputs rotation policies, access controls, and audit logging.
argument-hint: [infrastructure type, compliance requirements, rotation frequency]
allowed-tools: Read, Write, Bash
---

# Secrets Management

Design secure secrets management for applications. Not hardcoded credentials — centralized secret stores, encryption at rest/transit, rotation policies, and audit trails.

## Process

1. **Inventory secrets.** API keys, database passwords, certificates, encryption keys.
2. **Choose secret store.** Vault (self-hosted), AWS Secrets Manager, GCP Secret Manager.
3. **Define access policies.** Who/what can read which secrets.
4. **Enable encryption.** At rest (AES-256), in transit (TLS).
5. **Implement rotation.** Automatic rotation for databases, manual for API keys.
6. **Add auditing.** Log all secret access and changes.
7. **Inject at runtime.** Never commit secrets to git, load from secret store.

## Output Format

### Secrets Management: [Application]

**Secret Store:** HashiCorp Vault  
**Secrets:** 45 (DB creds, API keys, TLS certs)  
**Rotation:** Database passwords every 90 days  
**Access Control:** Role-based (RBAC)  
**Audit:** All access logged to SIEM

---

## Secret Store Comparison

| Feature | Vault | AWS Secrets Manager | Kubernetes Secrets |
|---------|-------|---------------------|-------------------|
| Cost | Self-hosted | $0.40/secret/month | Free |
| Rotation | ✅ Automatic | ✅ Automatic | ❌ Manual |
| Dynamic secrets | ✅ Yes | ❌ No | ❌ No |
| Encryption | ✅ Strong | ✅ Strong | ⚠️ Base64 default |
| Audit logs | ✅ Detailed | ✅ CloudTrail | ⚠️ Limited |
| Multi-cloud | ✅ Yes | ❌ AWS only | ✅ Yes |

**Recommendation:** Vault for multi-cloud, AWS Secrets Manager for AWS-only

---

## HashiCorp Vault

### Setup
```bash
# Start Vault server
vault server -dev -dev-root-token-id="root"

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Enable KV secrets engine
vault secrets enable -path=secret kv-v2
```

### Store Secret
```bash
# Write secret
vault kv put secret/database/postgres \
    username=dbuser \
    password=SuperSecret123

# Read secret
vault kv get secret/database/postgres

# Get JSON output
vault kv get -format=json secret/database/postgres | jq -r .data.data.password
```

### Dynamic Database Secrets
```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL
vault write database/config/postgresql \
    plugin_name=postgresql-database-plugin \
    allowed_roles="readonly,readwrite" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
    username="vault" \
    password="vault_password"

# Create role (readonly)
vault write database/roles/readonly \
    db_name=postgresql \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Generate dynamic credentials
vault read database/creds/readonly

Key                Value
---                -----
lease_id           database/creds/readonly/abc123
lease_duration     1h
lease_renewable    true
password           A1a-random-password
username           v-root-readonly-abc123
```

**Benefits:**
- Credentials auto-revoked after TTL
- No long-lived passwords
- Automatic rotation

---

## AWS Secrets Manager

### Create Secret
```python
import boto3
import json

client = boto3.client('secretsmanager')

# Store secret
response = client.create_secret(
    Name='prod/database/postgres',
    Description='Production PostgreSQL credentials',
    SecretString=json.dumps({
        'username': 'dbuser',
        'password': 'SuperSecret123',
        'host': 'postgres.example.com',
        'port': 5432
    })
)

print(f"Secret ARN: {response['ARN']}")
```

### Retrieve Secret
```python
def get_secret(secret_name):
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret

# Usage
db_creds = get_secret('prod/database/postgres')
db_password = db_creds['password']
```

### Automatic Rotation
```python
# Enable rotation (every 30 days)
client.rotate_secret(
    SecretId='prod/database/postgres',
    RotationLambdaARN='arn:aws:lambda:...:function:RotatePostgres',
    RotationRules={
        'AutomaticallyAfterDays': 30
    }
)
```

**Lambda rotation function:**
```python
import boto3
import psycopg2

def lambda_handler(event, context):
    secret_arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    
    if step == "createSecret":
        # Generate new password
        new_password = generate_secure_password()
        
        # Store as AWSPENDING version
        client.put_secret_value(
            SecretId=secret_arn,
            ClientRequestToken=token,
            SecretString=json.dumps({'password': new_password}),
            VersionStages=['AWSPENDING']
        )
    
    elif step == "setSecret":
        # Update database password
        pending = get_secret_version(secret_arn, 'AWSPENDING')
        current = get_secret_version(secret_arn, 'AWSCURRENT')
        
        conn = psycopg2.connect(
            user=current['username'],
            password=current['password'],
            host=current['host']
        )
        cursor = conn.cursor()
        cursor.execute(f"ALTER USER {current['username']} WITH PASSWORD '{pending['password']}'")
        conn.commit()
    
    elif step == "testSecret":
        # Test new password works
        pending = get_secret_version(secret_arn, 'AWSPENDING')
        conn = psycopg2.connect(
            user=pending['username'],
            password=pending['password'],
            host=pending['host']
        )
        conn.close()
    
    elif step == "finishSecret":
        # Promote AWSPENDING to AWSCURRENT
        client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token
        )
```

---

## Kubernetes Secrets

### Create Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
type: Opaque
data:
  username: ZGJ1c2Vy  # base64("dbuser")
  password: U3VwZXJTZWNyZXQxMjM=  # base64("SuperSecret123")
```

```bash
# Create from command line
kubectl create secret generic postgres-credentials \
    --from-literal=username=dbuser \
    --from-literal=password=SuperSecret123

# Create from file
kubectl create secret generic tls-cert \
    --from-file=tls.crt=./cert.pem \
    --from-file=tls.key=./key.pem
```

### Use in Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: postgres-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: postgres-credentials
          key: password
    
    # Or mount as files
    volumeMounts:
    - name: secrets
      mountPath: "/etc/secrets"
      readOnly: true
  
  volumes:
  - name: secrets
    secret:
      secretName: postgres-credentials
```

### Encrypt at Rest (KSMS)
```yaml
# kube-apiserver config
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml

# encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
      - identity: {}
```

---

## External Secrets Operator

### Sync from AWS Secrets Manager to K8s
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secretsmanager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: SecretStore
  target:
    name: postgres-credentials  # K8s Secret name
  data:
  - secretKey: username
    remoteRef:
      key: prod/database/postgres
      property: username
  - secretKey: password
    remoteRef:
      key: prod/database/postgres
      property: password
```

**Benefit:** Secrets stay in AWS, K8s syncs automatically

---

## Access Control

### Vault Policies
```hcl
# readonly.hcl
path "secret/data/database/*" {
  capabilities = ["read", "list"]
}

path "secret/data/api-keys/*" {
  capabilities = ["deny"]
}
```

```bash
# Create policy
vault policy write readonly readonly.hcl

# Create token with policy
vault token create -policy=readonly
```

### AppRole Authentication
```bash
# Enable AppRole
vault auth enable approle

# Create role
vault write auth/approle/role/my-app \
    secret_id_ttl=10m \
    token_ttl=20m \
    token_max_ttl=30m \
    policies=readonly

# Get role ID
vault read auth/approle/role/my-app/role-id

# Generate secret ID (one-time use)
vault write -f auth/approle/role/my-app/secret-id
```

```python
# App authenticates with AppRole
import hvac

client = hvac.Client(url='http://vault:8200')

response = client.auth.approle.login(
    role_id='role-id-here',
    secret_id='secret-id-here'
)

client.token = response['auth']['client_token']

# Read secret
secret = client.secrets.kv.v2.read_secret_version(path='database/postgres')
password = secret['data']['data']['password']
```

---

## Rotation Policies

### Database Password Rotation
```
Rotation Frequency: Every 90 days
Grace Period: 7 days (old password still works)
Notification: Email 14 days before expiration

Process:
1. Generate new password
2. Update database
3. Update secret store
4. Rolling restart of apps (pick up new password)
5. After grace period, revoke old password
```

### API Key Rotation
```
Rotation: On-demand (when compromised)
Dual keys: Primary + Secondary (allow zero-downtime rotation)

Process:
1. Generate secondary key
2. Deploy apps with secondary key
3. Verify traffic on secondary
4. Revoke primary key
5. Promote secondary → primary
```

---

## Audit Logging

### Vault Audit
```bash
# Enable file audit
vault audit enable file file_path=/vault/logs/audit.log

# Audit log entry (JSON)
{
  "time": "2024-03-21T10:30:00Z",
  "type": "request",
  "auth": {
    "client_token": "abc123",
    "policies": ["readonly"]
  },
  "request": {
    "operation": "read",
    "path": "secret/data/database/postgres"
  },
  "response": {
    "data": {
      "username": "dbuser"
      // password redacted in logs
    }
  }
}
```

### Send to SIEM
```bash
# Fluentd to ElasticSearch
<source>
  @type tail
  path /vault/logs/audit.log
  format json
</source>

<match **>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name vault-audit
</match>
```

---

## Injection Patterns

### Environment Variables (12-Factor App)
```python
import os

DATABASE_URL = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']
```

**Kubernetes:**
```yaml
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: url
```

### Files (Mounted Volumes)
```python
# Read from /etc/secrets/db-password
with open('/etc/secrets/db-password') as f:
    db_password = f.read().strip()
```

### Vault Agent Sidecar
```yaml
# Pod with Vault agent
spec:
  initContainers:
  - name: vault-agent
    image: vault:1.12
    command:
      - vault
      - agent
      - -config=/vault/config/agent.hcl
    volumeMounts:
    - name: vault-config
      mountPath: /vault/config
    - name: secrets
      mountPath: /vault/secrets
  
  containers:
  - name: app
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
```

---

## Encryption

### Encrypt Secret Before Storing
```python
from cryptography.fernet import Fernet

# Generate key (store in KMS)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
secret = "my-secret-password"
encrypted = cipher.encrypt(secret.encode())

# Decrypt
decrypted = cipher.decrypt(encrypted).decode()
```

### Envelope Encryption (KMS)
```
1. Generate data encryption key (DEK)
2. Encrypt secret with DEK
3. Encrypt DEK with master key (stored in KMS)
4. Store encrypted secret + encrypted DEK

To decrypt:
1. Decrypt DEK using KMS
2. Decrypt secret using DEK
```

```python
import boto3

kms = boto3.client('kms')

# Generate data key
response = kms.generate_data_key(
    KeyId='arn:aws:kms:...:key/abc123',
    KeySpec='AES_256'
)

plaintext_key = response['Plaintext']
encrypted_key = response['CiphertextBlob']

# Encrypt secret with plaintext key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
cipher = Cipher(algorithms.AES(plaintext_key), modes.GCM(iv))
encrypted_secret = cipher.encryptor().update(secret) + cipher.encryptor().finalize()

# Store: encrypted_secret + encrypted_key

# Decrypt:
response = kms.decrypt(CiphertextBlob=encrypted_key)
plaintext_key = response['Plaintext']
# Use plaintext_key to decrypt secret
```

---

## Anti-Patterns

### ❌ Hardcoded Secrets
```python
DATABASE_URL = "postgresql://user:password123@db:5432/mydb"  # WRONG!
```

### ❌ Secrets in Git
```bash
# .env file committed to git
API_KEY=sk-abc123  # WRONG!
```

### ❌ Secrets in Docker Images
```dockerfile
ENV API_KEY=sk-abc123  # WRONG! Visible in image layers
```

### ✅ Correct: Runtime Injection
```dockerfile
# No secrets in Dockerfile
FROM python:3.11
COPY app.py .
CMD ["python", "app.py"]

# Pass secrets at runtime
docker run -e API_KEY=$API_KEY myapp
```

## Rules

- Never commit secrets to version control — use .gitignore, pre-commit hooks to prevent.
- Rotate secrets regularly — database passwords every 90 days, API keys on compromise.
- Use secret stores, not environment files — centralized management, audit logs.
- Encrypt secrets at rest and in transit — AES-256, TLS required.
- Grant least privilege access — applications only access secrets they need.
- Audit all secret access — log who read what when for compliance.
- Dynamic secrets preferred over static — auto-revoked credentials reduce exposure window.
- Secrets injected at runtime, never baked into images — Docker layers are immutable.
- Use service accounts/IAM roles over API keys — authentication without managing credentials.
- Test secret rotation in staging — broken rotation causes production outages.
