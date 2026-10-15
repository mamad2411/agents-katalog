---
name: devops-security
description: "Seguridad DevOps (DevSecOps). Cubre Sigstore Cosign 3.0 para image signing, HashiCorp Vault para secrets management, Trivy para vulnerability scanning, RBAC en Kubernetes, network policies, y SBOM (Software Bill of Materials). Actívala al asegurar pipelines, gestionar secrets, o implementar supply chain security."
disable-model-invocation: true
---

# DevSecOps

Guía de seguridad en pipelines DevOps. Supply chain security, secretos, escaneo, RBAC.

---

## Supply Chain Security

```
Source Code → Build → Sign → Attest → Verify → Deploy
     │          │       │       │         │
     └──────────┴───────┴───────┴─────────┘
              Cada etapa verificada
```

---

## Cosign 3.0 — Image Signing

```bash
# Keyless signing con OIDC (GitHub Actions)
cosign sign ghcr.io/mi-org/miapp:${{ github.sha }}

# En CI (GitHub Actions)
- uses: sigstore/cosign-installer@v3
- run: cosign sign ${{ steps.meta.outputs.tags }}
  env:
    COSIGN_YES: true  # Non-interactive

# Verificar antes de deploy (admission controller o manual)
cosign verify \
  --certificate-identity "https://github.com/mi-org/miapp/.github/workflows/deploy.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  ghcr.io/mi-org/miapp:latest

# Firmar con key management (OpenBao)
cosign sign --key "openbao://transit/keys/cosign" ghcr.io/mi-org/miapp:latest
```

---

## HashiCorp Vault — Secrets Management

### Dynamic database credentials

```bash
# Configurar engine de PostgreSQL en Vault
vault secrets enable database

vault write database/config/miapp-db \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly,readwrite" \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/miapp" \
  username="vault_admin" \
  password="admin_password"

# Rotar credenciales automáticamente: role que genera creds temporales
vault write database/roles/readwrite \
  db_name=miapp-db \
  creation_statements="CREATE USER \"{{name}}\" WITH PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT ALL ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# La app obtiene credenciales dinámicas (se recrean cada 1h)
vault read database/creds/readwrite
```

### External Secrets Operator (Kubernetes)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: miapp-db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: miapp-db-secret
  data:
  - secretKey: DATABASE_URL
    remoteRef:
      key: database/creds/readwrite
      property: connection_string
```

---

## Trivy — Vulnerability Scanning

```yaml
# GitHub Actions: escanear imagen antes de push
- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/mi-org/miapp:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH
    exit-code: 1  # Fallar si hay CRITICAL o HIGH

# Escanear IaC
- name: Scan Terraform
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: config
    scan-ref: infra/
    severity: CRITICAL,HIGH
```

---

## Kubernetes RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: miapp-api
  namespace: miapp-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: miapp-prod
  name: miapp-api-role
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
  resourceNames: ["miapp-config", "miapp-secrets"]  # Restringir a recursos específicos
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: miapp-api-binding
  namespace: miapp-prod
subjects:
- kind: ServiceAccount
  name: miapp-api
roleRef:
  kind: Role
  name: miapp-api-role
  apiGroup: rbac.authorization.k8s.io
```

---

## Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: miapp-api-netpol
  namespace: miapp-prod
spec:
  podSelector:
    matchLabels:
      app: miapp-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx  # Solo desde ingress
    ports:
    - port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres  # Solo puede hablar con postgres
    ports:
    - port: 5432
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          app: redis
    ports:
    - port: 6379
```

---

## SBOM (Software Bill of Materials)

```bash
# Generar SBOM con Syft
syft ghcr.io/mi-org/miapp:latest -o spdx-json > miapp-sbom.json

# Adjuntar SBOM a la imagen
cosign attest --type spdx --predicate miapp-sbom.json ghcr.io/mi-org/miapp:latest

# Verificar SBOM
cosign verify-attestation --type spdx ghcr.io/mi-org/miapp:latest
```

---

## Checklist DevSecOps

- [ ] Imágenes firmadas con Cosign (keyless OIDC)
- [ ] Trivy scan en CI: fallar con CRITICAL/HIGH
- [ ] Secrets gestionados con Vault o External Secrets Operator
- [ ] ServiceAccount dedicado por app (no default)
- [ ] RBAC con mínimo privilegio (solo recursos necesarios)
- [ ] NetworkPolicy restringe tráfico entre pods
- [ ] SBOM generado y attestado en cada build
- [ ] Imágenes base escaneadas regularmente
- [ ] No secrets en código, Dockerfile, ni capas de imagen
- [ ] Admission controller que verifica firmas antes de deploy
