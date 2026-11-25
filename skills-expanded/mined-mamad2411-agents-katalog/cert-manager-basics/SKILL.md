---
name: cert-manager-basics
description: >
  cert-manager basics on owned Kubernetes clusters: install, Issuers/ClusterIssuers,
  Certificate CRDs, Secret targets, renewal, and troubleshooting Ready states. Use when
  cert-manager Certificate, ClusterIssuer, kubernetes TLS automation, or ACME issuer setup —
  pair challenge details with `cert-manager-http01-dns01`.
---

# Cert Manager Basics

## Scope And Authorization

- **In scope:** Kubernetes clusters and DNS/HTTP endpoints you operate.
- **Out of scope:** Issuing certificates for domains you do not control; abusing public ACME against third parties.
- ACME rate limits are real — use staging issuers for experiments.
- Pair with `cert-manager-http01-dns01`, ingress TLS, `code-quality-standards`.

## When To Use

- Automating TLS certificates inside Kubernetes with cert-manager.
- Creating Issuers for Let’s Encrypt, private CA, Vault, or self-signed.
- Debugging Certificate not Ready, Secret not created, renewal failures.
- Standardizing TLS secrets for Ingress/Gateway.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| HTTP-01 / DNS-01 challenge deep dive | `cert-manager-http01-dns01` |
| Certificate Transparency monitoring | `certificate-transparency-basics` |
| Expiry landing pages | `certificate-expiry-page` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Resource | Role |
| --- | --- |
| cert-manager controller | Reconciles CRDs, talks ACME/CA |
| Issuer / ClusterIssuer | How to obtain certs (namespaced vs cluster) |
| Certificate | Desired X.509 + Secret name |
| CertificateRequest / Order / Challenge | ACME machinery objects |
| Secret `kubernetes.io/tls` | tls.crt / tls.key for Ingress |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster version, ingress controller, domains, public vs private CA need.
2. Success: Certificate Ready=True; Secret mounted; auto-renew before expiry; runbook for failures.
3. Use ACME **staging** until green.

### 2. Install cert-manager

```bash
# Example official manifest/helm — pin version
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml
# or helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set crds.enabled=true --version v1.16.2
kubectl -n cert-manager get pods
kubectl get crd | rg cert-manager
```

1. Pin versions; review release notes.
2. Restrict who can create ClusterIssuers (RBAC).

### 3. Create an Issuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    email: sre@example.com
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: le-staging-account-key
    solvers:
      - http01:
          ingress:
            class: nginx
```

1. Production issuer uses production ACME URL after staging success.
2. Private PKI: `ca` issuer referencing a CA Secret; or Vault issuer.
3. Solver choice → see `cert-manager-http01-dns01`.

### 4. Request a Certificate

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: www-example
  namespace: app
spec:
  secretName: www-example-tls
  issuerRef:
    name: letsencrypt-staging
    kind: ClusterIssuer
  dnsNames:
    - www.example.com
    - example.com
```

```bash
kubectl -n app get certificate
kubectl -n app describe certificate www-example
kubectl -n app get secret www-example-tls
```

1. Ingress can auto-annotate for temporary certs (`cert-manager.io/cluster-issuer=...`) — understand ownership of Certificate objects.
2. Ensure DNS points to the cluster for HTTP-01.

### 5. Wire Ingress/Gateway

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: www
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts: [www.example.com]
      secretName: www-example-tls
  rules:
    - host: www.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port: { number: 80 }
```

### 6. Troubleshoot

```bash
kubectl -n app describe certificate www-example
kubectl -n app get certificaterequest,order,challenge
kubectl -n cert-manager logs deploy/cert-manager | tail
```

| Symptom | Checks |
| --- | --- |
| Challenge pending | DNS, ingress class, firewall 80, solver pods |
| Rate limited | Use staging; reduce re-issues |
| Secret empty | Certificate events; CSR failures |
| Renew fail | ACME account, DNS still valid, solver still works |
| Wrong issuer | issuerRef kind/name/namespace |

### 7. Operate and hand off

1. Monitor certificate expiry metrics (cert-manager metrics / blackbox).
2. Backup ACME account keys Secrets carefully.
3. Document prod vs staging issuers; RBAC for Certificate create.
4. Apply `code-quality-standards` to GitOps manifests.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Testing | Staging ACME first | Hammer production LE from CI loops |
| RBAC | Limit ClusterIssuer create | All devs edit cluster issuers |
| Secrets | TLS secrets namespaced least access | World-readable copies |
| Versions | Pinned cert-manager | Latest floating |
| Solvers | Correct class / DNS perms | Copy-paste wrong ingress class |
| Renew | Metrics + alerts | Discover expiry via users |

## Output Checklist

- [ ] cert-manager installed and pods healthy
- [ ] Staging issuer works end-to-end
- [ ] Production issuer created after success
- [ ] Certificate Ready and Secret present
- [ ] Ingress/Gateway serves valid TLS
- [ ] Renewal path understood
- [ ] Alerts on expiry/failure
- [ ] RBAC reviewed
- [ ] Challenge details per `cert-manager-http01-dns01`
- [ ] GitOps/`code-quality-standards` applied

## Rules

- Only issue for domains you control.
- Prefer staging until validation works.
- Protect ACME account private keys and TLS Secrets.
- Authorized clusters only.
- Challenge solver depth → `cert-manager-http01-dns01`.
