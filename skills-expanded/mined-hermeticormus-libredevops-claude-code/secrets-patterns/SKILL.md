---
name: secrets-patterns
description: "Secret management patterns: Vault Agent Injector sidecars, External Secrets Operator with Vault or with AWS Secrets Manager and IRSA, Sealed Secrets for GitOps, and secret rotation without downtime. Use when getting secrets into Kubernetes workloads safely or rotating them."
---

# Secret Management Patterns

Vault dynamic secrets, External Secrets Operator, SOPS encryption, and zero-downtime rotation.

## Vault Agent Injector (Kubernetes Sidecar)

```yaml
# Pod annotation: Vault Agent injects secrets into pod's filesystem
# No Kubernetes Secret created -- credentials never touch etcd
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api
  namespace: production
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "payment-api"
        vault.hashicorp.com/agent-inject-secret-db-creds: "database/creds/app-readwrite"
        vault.hashicorp.com/agent-inject-template-db-creds: |
          {{- with secret "database/creds/app-readwrite" -}}
          export DB_USERNAME="{{ .Data.username }}"
          export DB_PASSWORD="{{ .Data.password }}"
          export DATABASE_URL="postgresql://{{ .Data.username }}:{{ .Data.password }}@postgres.internal:5432/myapp"
          {{- end }}
        # Renew credentials before expiry (app gets refreshed creds without restart)
        vault.hashicorp.com/agent-inject-secret-app-config: "secret/data/production/payment-api"
        vault.hashicorp.com/agent-inject-template-app-config: |
          {{- with secret "secret/data/production/payment-api" -}}
          {{ .Data.data | toJSON }}
          {{- end }}
    spec:
      serviceAccountName: payment-api
      containers:
        - name: app
          image: registry.example.com/payment-api:v1.0.0
          command: ["/bin/sh", "-c", "source /vault/secrets/db-creds && exec ./payment-api"]
```

## External Secrets Operator with Vault

```yaml
# SecretStore: Vault backend
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.internal:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "payment-api"
          serviceAccountRef:
            name: payment-api

---
# ExternalSecret: database dynamic creds from Vault
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-dynamic-creds
  namespace: production
spec:
  refreshInterval: 45m   # Rotate before 1h TTL expires
  secretStoreRef:
    name: vault
    kind: SecretStore
  target:
    name: db-creds
    # Restart pods when secret refreshes (pick up new DB creds)
    template:
      metadata:
        annotations:
          reloader.stakater.com/match: "true"
  data:
    - secretKey: username
      remoteRef:
        key: database/creds/app-readwrite
        property: username
    - secretKey: password
      remoteRef:
        key: database/creds/app-readwrite
        property: password
```

## Sealed Secrets (GitOps-Safe Kubernetes Secrets)

```bash
# Install Sealed Secrets controller
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm upgrade --install sealed-secrets sealed-secrets/sealed-secrets \
  -n kube-system \
  --set fullnameOverride=sealed-secrets-controller

# Fetch the public key (safe to commit)
kubeseal --fetch-cert > sealed-secrets-cert.pem

# Create a SealedSecret from a regular Secret
kubectl create secret generic my-secret \
  --from-literal=API_KEY=super-secret-value \
  --dry-run=client -o yaml | \
  kubeseal \
    --cert sealed-secrets-cert.pem \
    --format yaml > my-secret-sealed.yaml

# Commit the sealed secret to Git (it's encrypted)
git add my-secret-sealed.yaml
git commit -m "feat: add API key sealed secret"

# The controller decrypts it in the cluster automatically
kubectl get secret my-secret -n production  # Regular K8s Secret appears
```

## AWS Secrets Manager with ESO and IRSA

```hcl
# Terraform: IRSA for External Secrets Operator
data "aws_iam_policy_document" "eso_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [module.eks.oidc_provider_arn]
    }
    condition {
      test     = "StringEquals"
      variable = "${module.eks.oidc_provider}:sub"
      values   = ["system:serviceaccount:external-secrets:external-secrets-sa"]
    }
  }
}

resource "aws_iam_role" "eso" {
  name               = "external-secrets-role"
  assume_role_policy = data.aws_iam_policy_document.eso_assume_role.json
}

resource "aws_iam_role_policy" "eso" {
  role = aws_iam_role.eso.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      # Limit to production secrets only
      Resource = "arn:aws:secretsmanager:us-east-1:${data.aws_caller_identity.current.account_id}:secret:production/*"
    }]
  })
}
```

## Secret Rotation Without Downtime

```python
# Pattern: DB connection pool that reconnects on auth failure
# Works with Vault dynamic creds or AWS Secrets Manager rotation

import boto3
import psycopg2
from psycopg2 import pool
import json

class RotatingConnectionPool:
    def __init__(self, secret_name: str, region: str):
        self.secret_name = secret_name
        self.region = region
        self._pool = None
        self._refresh_pool()

    def _get_credentials(self):
        client = boto3.client('secretsmanager', region_name=self.region)
        secret = client.get_secret_value(SecretId=self.secret_name)
        return json.loads(secret['SecretString'])

    def _refresh_pool(self):
        creds = self._get_credentials()
        self._pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=2, maxconn=10,
            host=creds['host'], database=creds['dbname'],
            user=creds['username'], password=creds['password']
        )

    def get_connection(self):
        try:
            return self._pool.getconn()
        except psycopg2.OperationalError as e:
            # Auth error = credentials rotated, refresh and retry
            if "authentication failed" in str(e):
                self._pool.closeall()
                self._refresh_pool()
                return self._pool.getconn()
            raise
```
