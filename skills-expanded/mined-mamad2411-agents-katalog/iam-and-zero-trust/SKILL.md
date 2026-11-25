---
name: iam-and-zero-trust
description: Design identity and access for humans and workloads with zero-trust principles — federated SSO, MFA, short-lived credentials, just-in-time elevation, least privilege, and continuous verification. Use when designing authn/authz, hardening cloud accounts, or removing standing access.
source: self
date_added: 2026-04-30
---

# IAM & Zero Trust

Design identity and access so that no network is trusted, no credential is long-lived, and no privilege is permanent. Verify explicitly, every time.

## When to Use

- Designing authn/authz for a new app, API, or platform.
- Replacing VPN-based perimeter access with identity-aware proxies.
- Removing standing IAM users / long-lived API keys.
- Aligning with NIST SP 800-207 (Zero Trust Architecture), CISA ZT Maturity Model, or BeyondCorp.

## Zero-Trust Tenets (NIST SP 800-207, condensed)

1. All resources are protected, regardless of network location.
2. Access is per-session and per-resource, not "into a network".
3. Trust is computed dynamically from identity, device posture, and context.
4. Access is least-privileged and time-bound.
5. Everything is monitored; logs feed continuous improvement.
6. No implicit trust based on IP, VPN, or asset ownership.

## Identity Foundations

- **Single source of truth** for human identity (Okta, Entra ID, Google Workspace, JumpCloud). One identity per person, lifecycle tied to HR system.
- **Federation, not local accounts.** Apps and cloud accounts authenticate via SAML/OIDC against the IdP. No app-specific passwords.
- **Phishing-resistant MFA** — FIDO2 / WebAuthn / passkeys. SMS and TOTP only as fallback for low-risk users; never for admins.
- **Conditional access policies**: require compliant device, MFA, geo/risk-based step-up.
- **Group-based entitlements** with **Access Reviews** quarterly (or continuous via IGA tools).
- **Joiner-Mover-Leaver (JML)** automated; deprovisioning within minutes of HR termination.
- **Break-glass accounts**: 2-3, hardware-key-only, sealed credentials, alarmed on use.

## Workload Identity

- **No long-lived secrets in workloads.** Use platform identities:
  - AWS: IAM Roles via instance profile / ECS task role / Lambda role / IRSA on EKS / Roles Anywhere on-prem.
  - Azure: Managed Identities (system or user-assigned) and Workload Identity Federation.
  - GCP: Service-account impersonation + Workload Identity (GKE) and Workload Identity Federation.
  - Kubernetes-native: SPIFFE/SPIRE for cross-cluster, cross-cloud workload identity (X.509 SVIDs / JWT SVIDs).
- **CI/CD to cloud**: OIDC federation (GitHub Actions, GitLab, CircleCI -> AWS/Azure/GCP). Never store cloud keys in CI variables.
- **Service-to-service**: mTLS with short-lived certs (service mesh — Istio, Linkerd — or SPIRE), or signed OIDC tokens validated per call.

## Authorization Patterns

- **RBAC** as a baseline — roles map to job functions, not individuals.
- **ABAC / ReBAC** when policies depend on attributes (tenant, region, data classification) or relationships (owner, member). Tools: OPA/Rego, Cedar, Oso, OpenFGA, SpiceDB.
- **Policy as code** — versioned, tested, deployed via pipeline with rego/cedar unit tests.
- **Decision point centralized** (PDP), enforcement distributed (PEPs at each service).
- **Tenant isolation** is an authorization concern: every query and message scoped by tenant id, asserted by policy.
- **Deny by default**; explicit allow with the smallest scope.

## Privileged Access (Humans)

- **No standing admin.** Just-in-time elevation via PIM (Entra), AWS IAM Identity Center session policies, GCP IAM Conditions + temporary grants, or third-party PAM (CyberArk, Teleport, StrongDM, HashiCorp Boundary).
- Approval workflow for elevation; auto-expire (e.g., 1-4 hours).
- All admin actions logged with user, source, justification.
- Production access requires session recording for sensitive systems.
- Admin workstations isolated (PAW / SAW) for top-tier roles.

## Network: From VPN to Identity-Aware Proxy

- Replace flat VPN with **identity-aware access** to specific apps:
  - Cloudflare Access, Google IAP, Tailscale, Twingate, Zscaler ZPA, Teleport.
- Each request authenticates the user *and* the device, then authorizes per app.
- East-west traffic in K8s: **service mesh with mTLS + authorization policies** (Istio AuthorizationPolicy, Linkerd policies).
- Egress: explicit allow-lists from known service identities.

## Device Trust

- Inventory of all endpoints (MDM: Intune, Jamf, Kandji).
- **Compliance signals** (disk encryption, OS patch level, EDR running) feed conditional access.
- BYOD only with managed app boundary or strict access scope.

## Secrets Management

- Centralized vault (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager).
- **Dynamic secrets** for databases (Vault DB engine) — short-lived, per-session.
- Rotation automated; access audited; access path is machine identity, not a static token.
- Pre-commit + CI secret scanning (`gitleaks`, `trufflehog`); revoke on detection, don't just rotate.
- Never embed secrets in container images, env files in repos, or client-side code.

## Tokens & Sessions

- OAuth2 / OIDC for delegated access; short access-token lifetimes (5-15 min) + refresh tokens with rotation + reuse detection.
- DPoP or mTLS-bound tokens for high-sensitivity APIs.
- Session cookies: `Secure`, `HttpOnly`, `SameSite=Lax/Strict`, signed/encrypted server-side state.
- Bind sessions to device fingerprint where feasible; revoke on risk signals.

## Continuous Verification & Logging

- All authn/authz events to SIEM (Sentinel, Splunk, Elastic, Chronicle).
- Anomaly detection: impossible travel, unusual scope grants, privilege escalation chains.
- Periodic access reviews with auto-revoke for unused entitlements (>90 days unused).
- Red-team / purple-team identity attack paths quarterly.

## Anti-Patterns

- IAM users with `AdministratorAccess` for "the deploy pipeline".
- "Temporary" access that becomes permanent because nobody revokes it.
- MFA exemption for execs.
- Password rotation policies without phishing-resistant MFA — security theater.
- Service accounts shared across teams with passwords in a wiki.
- Network-based trust ("if you're in the VPN, you're in").
- Authorization in the UI only; APIs unprotected.
- Logs of admin actions kept in the same blast radius as the admins.
- Wildcard scopes (`*`, `roles/owner`, `Owner`) granted "to unblock".

## Quality Gates

- Zero long-lived cloud keys in CI/CD; OIDC federation in use.
- 100% phishing-resistant MFA on admins; >95% on all users.
- All workload-to-cloud auth via platform identities.
- Authorization decisions covered by policy-as-code with tests.
- Quarterly access review completed; unused access auto-revoked.
- SIEM alerts on identity anomalies route to on-call.
- Break-glass procedure tested annually.

## Maturity Roadmap

1. **Federate** all apps to one IdP; enforce MFA.
2. **Eliminate long-lived cloud keys** (OIDC + workload identity).
3. **Just-in-time elevation** for all admin roles.
4. **Identity-aware proxy** to retire flat VPN.
5. **Service mesh + policy as code** for east-west.
6. **Continuous access evaluation** with risk-based step-up and auto-revocation.

## References

- NIST SP 800-207: Zero Trust Architecture
- CISA Zero Trust Maturity Model 2.0
- Google BeyondCorp papers
- OWASP Authentication / Authorization Cheat Sheets
- "Zero Trust Networks" (Gilman, Barth)
- SPIFFE / SPIRE: https://spiffe.io/
