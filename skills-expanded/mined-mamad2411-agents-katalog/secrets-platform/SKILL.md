---
name: secrets-platform
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: secrets management platform, secret rotation automation, secret access auditing, secret sprawl prevention, vault architecture, secrets lifecycle, dynamic secret generation, secret injection pattern, secrets governance, secret scanning platform, certificate management, secrets policy enforcement
compose: secrets-rotation
---

# Skill — Secrets Platform

## When this skill activates

This skill activates when the user is designing or implementing a centralized secrets management platform. This includes secret rotation automation, access auditing, secret sprawl prevention, Vault architecture, secrets lifecycle management, dynamic secret generation, secret injection patterns, secrets governance, secret scanning, certificate management, and secrets policy enforcement.

## Mandatory actions when this skill is active

### Before writing any code

1. Audit current secret storage locations: code repos, config files, environment variables, CI/CD systems, container images, config management tools. Quantify secret sprawl.
2. Identify secret types: API keys, database credentials, TLS certificates, OAuth tokens, encryption keys, SSH keys. Each type has different rotation requirements.
3. Define secret access policies: which teams/services can access which secrets. Use principle of least privilege (default deny, explicit allow).
4. Establish secret rotation requirements: compliance mandates (PCI DSS, SOC 2), blast radius reduction, credential age limits.
5. Assess current secret rotation toil: how many hours per month spent manually rotating secrets.

### During implementation

- **Centralized Secret Store:** Use HashiCorp Vault, AWS Secrets Manager, or GCP Secret Manager. Never store secrets in code, config files, or environment variables. Secrets should be encrypted at rest and in transit.
- **Secret Rotation Automation:** Automate rotation for database credentials, API keys, and TLS certificates. High-sensitivity secrets (production database) rotate every 30 days. Low-sensitivity (dev sandbox API keys) rotate every 90 days. Rotation should be zero-downtime (dual-write during rotation window).
- **Dynamic Secret Generation:** For databases, generate short-lived credentials on-demand (Vault database secrets engine). Credentials should expire after 1-8 hours. Reduces blast radius if credentials leak.
- **Secret Injection Patterns:** Inject secrets at runtime, not build time. Use init containers (Kubernetes), sidecar containers (Vault Agent), or secret CSI drivers. Secrets should never be in container images.
- **Access Auditing:** Log every secret access (who, what, when, from where). Audit logs must be immutable and retained for 1+ year. Alert on unusual access patterns (access from new IP, high-frequency access, access to secrets outside normal scope).
- **Secret Sprawl Prevention:** Use secret scanning in CI/CD (Trufflehog, GitGuardian, GitHub Secret Scanning). Block commits containing secrets. Scan existing repos and remediate found secrets (rotate + remove from history).
- **Certificate Management:** Automate TLS certificate issuance (Let's Encrypt, cert-manager) and renewal (30 days before expiry). Track certificate expiration dates and alert 60 days before expiry.
- **Secrets Policy Enforcement:** Use policy-as-code (OPA, Vault policies) to enforce: maximum credential age, minimum rotation frequency, required encryption strength, allowed access patterns. Policies should fail-closed (deny by default).
- **Emergency Access (Break-Glass):** Provide mechanism for emergency access to secrets when automation fails. Requires: approval workflow, audit trail, automatic expiration (4-8 hours), post-incident review.

### After implementation

- Verify all production secrets are migrated to centralized secret store (zero secrets in code/config).
- Confirm secret rotation is automated and zero-downtime for critical credentials.
- Validate secret injection happens at runtime with no secrets in container images.
- Ensure access auditing logs every secret access with retention of 1+ year.
- Check that secret scanning blocks commits containing secrets in CI/CD.

## Self-check before task completion

- [ ] All production secrets are stored in centralized secret store (Vault, Secrets Manager).
- [ ] Secret rotation is automated for credentials and certificates with zero-downtime.
- [ ] Dynamic secrets are used for databases with 1-8 hour expiration.
- [ ] Secret injection happens at runtime via init containers, sidecars, or CSI drivers.
- [ ] Access auditing logs every secret access with immutable logs retained for 1+ year.
- [ ] Secret scanning is enabled in CI/CD and blocks commits containing secrets.
- [ ] Certificate management automates issuance and renewal with alerts 60 days before expiry.
- [ ] Secrets policy enforcement uses policy-as-code and fails closed (deny by default).
- [ ] Emergency access (break-glass) requires approval, audit trail, and auto-expiration.
