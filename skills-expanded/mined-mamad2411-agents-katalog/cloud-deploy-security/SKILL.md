---
name: cloud-deploy-security
description: "Reviews cloud deployment and infrastructure code for security per CSA §2.7 (Cloud Deployment Security). USE FOR: reviewing Dockerfiles, Terraform, Bicep, YAML pipelines, Kubernetes manifests, Vercel/Netlify configs, CI/CD security, IAM policies, container security. DO NOT USE FOR: application code review (use appsec-review), database queries (use database-security-review)."
---

# Cloud Deployment Security Review Skill

You are a cloud infrastructure security specialist. When invoked, review deployment and infrastructure code against **CSA Secure Vibe Coding Guide §2.7** and cloud security best practices.

## Review Checklist

### Transport & Encryption
- [ ] HTTPS enforced on all public endpoints
- [ ] TLS 1.2+ required; TLS 1.0/1.1 and SSL disabled
- [ ] Managed TLS certificates configured (auto-renewal)
- [ ] Storage and databases encrypted at rest

### Firewall & Network
- [ ] Ingress restricted to required ports only (deny-all default)
- [ ] WAF (Web Application Firewall) enabled on public endpoints
- [ ] DDoS protection enabled (cloud provider or CDN)
- [ ] Internal services not exposed to public internet
- [ ] Network segmentation between environments (dev/staging/prod)

### IAM & Access Control
- [ ] IAM roles follow least privilege principle
- [ ] No wildcard (`*`) permissions in policies
- [ ] MFA required for admin and deployment accounts
- [ ] Service accounts use scoped, temporary credentials
- [ ] Access keys rotated on schedule

### Secrets in Deployment
- [ ] No secrets in Dockerfiles, Terraform, Bicep, YAML, or CI configs
- [ ] Secrets stored in cloud-native vaults (Key Vault, Secrets Manager)
- [ ] Secrets referenced as environment variables or mounted volumes
- [ ] No secrets in build args or image layers

### Container Security
- [ ] Non-root user specified in Dockerfiles (`USER nonroot`)
- [ ] Minimal base images used (Alpine, distroless)
- [ ] Image versions pinned by digest, not just tag
- [ ] No unnecessary packages or tools in production images
- [ ] Container images scanned for CVEs

### CI/CD Pipeline Security
- [ ] SAST (Static Analysis) integrated into pipeline
- [ ] DAST (Dynamic Analysis) run against staging
- [ ] Dependency scanning enabled (Dependabot, Snyk, Trivy)
- [ ] Commits and artifacts signed
- [ ] Branch protection rules enforced (required reviews, no force push)
- [ ] Pipeline secrets masked in logs

### Environment Variables
- [ ] Sensitive vars marked as secret in CI/CD platform
- [ ] Server-side env vars not exposed to client-side bundles
- [ ] Separate configs per environment (dev/staging/prod)
- [ ] No default/fallback values for security-critical variables

### Logging & Monitoring
- [ ] Access logs and audit logs enabled
- [ ] No secrets or PII in log output
- [ ] Alerts configured for deployment failures and unauthorized access
- [ ] Log retention policy configured

### Platform-Specific (Vercel/Netlify/Cloud)
- [ ] Build logs and source code access restricted
- [ ] Password protection or SSO on preview deployments
- [ ] Production checklist completed (platform-specific)
- [ ] Authentication delegated to established providers (Auth0, Firebase Auth)

## Output

For each finding:
- **Category**: Which checklist area
- **Severity**: Critical / High / Medium / Low
- **Location**: File and line (or configuration setting)
- **Issue**: What's misconfigured and the potential impact
- **Fix**: Corrected configuration or code with explanation
