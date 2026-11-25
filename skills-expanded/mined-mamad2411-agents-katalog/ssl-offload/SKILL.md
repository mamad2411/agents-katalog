# Skill: SSL/TLS Offload & Certificate Management (`lb_ssl_offload`)

Design TLS termination strategies, certificate lifecycle management, and encryption-in-transit architectures for load-balanced workloads across Azure, AWS, and GCP.

---

## TLS Termination Models

| Model | TLS Terminates At | Backend Traffic | Use Case |
|---|---|---|---|
| **TLS offload** | Load balancer | HTTP (unencrypted) to backend | Simplest; backend doesn't need certs. Only acceptable if LB → backend is within a trusted network (same VNet/VPC). |
| **TLS re-encryption** | Load balancer + backend | HTTPS (re-encrypted) to backend | LB terminates and inspects, then opens new TLS session to backend. Common for WAF + L7 routing. |
| **TLS pass-through** | Backend server | Encrypted end-to-end | LB forwards TCP without decryption. Required for mTLS or when LB must not see plaintext. L4 only — no L7 routing. |

**Recommendation**: Use **TLS re-encryption** for most production L7 workloads. It enables WAF inspection and content-based routing while maintaining encryption to backends.

---

## Certificate Management Per Cloud

### Azure — Key Vault Integration

```bash
# Store certificate in Key Vault
az keyvault certificate import \
  --vault-name myKeyVault \
  --name my-cert \
  --file ./cert.pfx \
  --password "certpassword"

# Reference from Application Gateway v2
az network application-gateway ssl-cert create \
  --resource-group myRG \
  --gateway-name myAppGW \
  --name my-ssl-cert \
  --key-vault-secret-id "https://myKeyVault.vault.azure.net/secrets/my-cert"

# Front Door managed certificate (auto-provisioned and renewed)
az afd custom-domain create \
  --resource-group myRG \
  --profile-name myFD \
  --custom-domain-name myCustomDomain \
  --host-name www.contoso.com \
  --certificate-type ManagedCertificate
```

**Azure certificate options:**
- **Key Vault certificates**: Centralized, version-controlled, auto-renewal with supported CAs (DigiCert, GlobalSign). Application Gateway, Front Door, and API Management all integrate natively.
- **Managed certificates**: Front Door and App Service can auto-provision free certificates via DigiCert. Requires CNAME validation.
- **Uploaded certificates (PFX)**: For Application Gateway when Key Vault is not available. Manual renewal required.

**Key Vault best practices:**
- Enable **managed identity** on the LB resource with `GET` permission on Key Vault secrets/certificates.
- Enable **soft delete** and **purge protection** on Key Vault — accidental cert deletion takes down TLS.
- Set Key Vault certificate **auto-renewal** at 30 days before expiry.

### AWS — ACM (AWS Certificate Manager)

```bash
# Request a public certificate (free, auto-renewed)
aws acm request-certificate \
  --domain-name www.contoso.com \
  --subject-alternative-names "*.contoso.com" \
  --validation-method DNS

# Attach to ALB listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:us-east-1:123456789012:certificate/abc-123 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...

# NLB TLS listener (NLB terminates TLS)
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol TLS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=...
```

**ACM key points:**
- Public certificates are **free** and **auto-renewed** (managed by AWS).
- ACM certs can only be used with **integrated AWS services** (ALB, NLB, CloudFront, API Gateway) — they cannot be exported.
- For certificates needed on EC2/ECS instances (backend re-encryption), use **ACM Private CA** or import your own certificates.
- CloudFront requires certs in **us-east-1** region.

### GCP — Certificate Manager

```bash
# Create a Google-managed certificate (auto-provisioned, auto-renewed)
gcloud certificate-manager certificates create my-cert \
  --domains="www.contoso.com,contoso.com" \
  --type=MANAGED

# Create a certificate map and attach to LB
gcloud certificate-manager maps create my-cert-map
gcloud certificate-manager maps entries create my-entry \
  --map=my-cert-map \
  --certificates=my-cert \
  --hostname=www.contoso.com

# Attach certificate map to HTTPS proxy
gcloud compute target-https-proxies update my-https-proxy \
  --certificate-map=my-cert-map
```

**GCP options:**
- **Google-managed certificates**: Free, auto-renewed, DNS or LB authorization.
- **Self-managed certificates**: Upload your own PEM cert + key. Manual renewal.
- **Certificate Manager**: Central service for managing certificates across multiple LBs. Supports wildcard certs.

---

## TLS Version & Cipher Suite Policy

### Minimum TLS Version

**Always enforce TLS 1.2 as minimum.** TLS 1.0 and 1.1 are deprecated (RFC 8996).

```bash
# Azure Application Gateway — set minimum TLS version
az network application-gateway ssl-policy set \
  --resource-group myRG \
  --gateway-name myAppGW \
  --policy-type Predefined \
  --policy-name AppGwSslPolicy20220101S

# AWS ALB — security policy selection
aws elbv2 create-listener ... \
  --ssl-policy ELBSecurityPolicy-TLS13-1-2-2021-06

# GCP — SSL policy
gcloud compute ssl-policies create my-ssl-policy \
  --profile RESTRICTED \
  --min-tls-version 1.2
gcloud compute target-https-proxies update my-proxy \
  --ssl-policy my-ssl-policy
```

### Cipher Suite Recommendations

| Level | Profile | Ciphers Included |
|---|---|---|
| **Restricted** | TLS 1.2+ only, AEAD ciphers | AES-256-GCM, AES-128-GCM, CHACHA20-POLY1305 |
| **Modern** | TLS 1.2+, strong ciphers | Above + AES-CBC (for older clients) |
| **Compatible** | TLS 1.0+ (not recommended) | All ciphers including legacy RC4, 3DES |

Use **Restricted** profile unless you must support legacy clients (e.g., legacy IoT devices, Windows Server 2012).

---

## Common TLS Mistakes

1. **Certificate hostname mismatch** — SAN/CN must match the FQDN clients use to connect. Wildcard certs (`*.contoso.com`) don't cover the apex (`contoso.com`).
2. **Expired certificates** — automate renewal. Set alerts at 30, 14, and 7 days before expiry.
3. **Incomplete certificate chain** — always include intermediate CA certificates. Use `openssl s_client -connect host:443 -showcerts` to verify.
4. **Backend certs ignored** — when using TLS re-encryption, the LB must trust the backend certificate. Configure the trusted root CA on the LB.
5. **Mixed content** — after enabling HTTPS on the LB, ensure all backend responses use HTTPS URLs. Use `Strict-Transport-Security` (HSTS) headers.

**Analysis only — verify against vendor documentation before applying.**
