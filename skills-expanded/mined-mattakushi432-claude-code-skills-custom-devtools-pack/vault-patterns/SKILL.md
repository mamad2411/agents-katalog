---
name: vault-patterns
description: "When to activate: HashiCorp Vault, secrets engine, auth method, dynamic secrets, lease, agent sidecar, KV store, PKI, AppRole"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: devops
  language: devops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# HashiCorp Vault Patterns

## Core Concepts

```
Secrets Engines — plugins that store/generate/encrypt secrets
  kv-v2        — versioned key-value store
  database     — dynamic DB credentials (auto-rotated)
  pki          — certificate authority
  aws/gcp/azure — dynamic cloud credentials

Auth Methods — how clients prove identity
  kubernetes   — pod service account JWT
  approle      — CI/CD pipelines
  aws          — IAM role binding
  oidc         — SSO / human users

Policies — what a token can access
  path "secret/data/myapp/*" { capabilities = ["read"] }
```

## KV v2 — Static Secrets

```bash
# Enable
vault secrets enable -path=secret kv-v2

# Write
vault kv put secret/myapp/prod \
  db_password=$DB_PASSWORD \
  api_key=$API_KEY

# Read
vault kv get -field=db_password secret/myapp/prod

# List versions
vault kv metadata get secret/myapp/prod

# Read specific version
vault kv get -version=3 secret/myapp/prod
```

## Dynamic Database Credentials

```bash
# Enable
vault secrets enable database

# Configure connection
vault write database/config/mydb \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db:5432/mydb" \
  allowed_roles="readonly,readwrite" \
  username="vault" \
  password=$VAULT_DB_PASSWORD

# Create role (credentials expire in 1h)
vault write database/roles/readonly \
  db_name=mydb \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Generate credentials (app calls this)
vault read database/creds/readonly
# → username: v-readonly-Abc123, password: A1B2C3...
```

## Kubernetes Auth Method

```bash
# Enable
vault auth enable kubernetes

# Configure
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create role binding pod SA → vault policy
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=prod \
  policies=myapp-policy \
  ttl=1h
```

## Vault Agent Sidecar (Kubernetes)

```yaml
spec:
  serviceAccountName: myapp-sa
  volumes:
    - name: vault-secrets
      emptyDir: { medium: Memory }
  initContainers:
    - name: vault-agent-init
      image: hashicorp/vault:1.15
      args: [agent, -config=/vault/config/agent.hcl, -exit-after-auth]
      volumeMounts:
        - name: vault-secrets
          mountPath: /vault/secrets
  containers:
    - name: myapp
      volumeMounts:
        - name: vault-secrets
          mountPath: /vault/secrets
          readOnly: true
      env:
        - name: DB_PASSWORD
          value: /vault/secrets/db_password   # or use envconsul
```

```hcl
# agent.hcl
vault {
  address = "https://vault.vault.svc.cluster.local:8200"
}
auto_auth {
  method "kubernetes" {
    mount_path = "auth/kubernetes"
    config = { role = "myapp" }
  }
}
template {
  destination = "/vault/secrets/db_password"
  contents    = <<EOT
{{ with secret "database/creds/readonly" }}{{ .Data.password }}{{ end }}
EOT
}
```

## Policy Example

```hcl
# myapp-policy.hcl
path "secret/data/myapp/prod/*" {
  capabilities = ["read"]
}
path "database/creds/readonly" {
  capabilities = ["read"]
}
path "pki/issue/myapp" {
  capabilities = ["create", "update"]
}
```

```bash
vault policy write myapp myapp-policy.hcl
```

## Key Rules
- Never store long-lived static credentials — use dynamic secrets with short TTL
- Seal/unseal with auto-unseal (AWS KMS, GCP KMS) — never manual unseal in prod
- Enable audit logging: `vault audit enable file file_path=/var/log/vault/audit.log`
- Use `vault agent` sidecar to handle token renewal automatically
- Rotate the root token immediately after cluster init; use break-glass procedure instead
