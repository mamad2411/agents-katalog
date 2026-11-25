---
name: couchbase-security-hardening
description: "Harden and audit Couchbase security posture for production deployments. Use whenever the user asks about TLS configuration, mTLS, certificate management, LDAP integration, SAML, PAM authentication, audit logging, audit log configuration, network isolation, firewall rules for Couchbase, RBAC design, least-privilege, password policy, account lockout (8.x), encryption at rest (DARE), KMIP key management, compliance (SOC2, HIPAA, PCI-DSS, FedRAMP), security hardening checklist, admin_encryption_*, admin_kmip_*, or 'how do I secure Couchbase for production.' Distinct from couchbase-mcp (calling the tools) and couchbase-app-integration (TLS in SDK clients). Use proactively for new production deployments, compliance reviews, security audits, and pre-certification hardening."
license: MIT
---

# Couchbase Security Hardening

A skill for *hardening* Couchbase deployments — TLS, RBAC, audit logging, encryption at rest, external authentication, network isolation, and compliance alignment.

Distinct from:
- `couchbase-mcp` — calling the security tools (`admin_user_*`, `admin_encryption_*`, etc.)
- `couchbase-app-integration` — TLS/mTLS configuration in SDK client code

## When this skill applies

- "How do I secure Couchbase for production?"
- "How do I set up TLS / enforce TLS-only connections?"
- "How do I integrate Couchbase with LDAP / Active Directory?"
- "How do I design RBAC for my team?"
- "What audit logging should I enable?"
- "How do I enable encryption at rest (DARE)?"
- "What's KMIP and when do I need it?"
- "How do I harden Couchbase for SOC2 / HIPAA / PCI?"
- "How do I configure password policy and account lockout?"

## Pick the right reference

| Question | Read |
|---|---|
| "TLS — enabling, certificate rotation, enforcing TLS-only, mTLS" | `references/tls.md` |
| "RBAC — role design, least-privilege, service accounts, group structure" | `references/rbac.md` |
| "External auth — LDAP, Active Directory, SAML, PAM" | `references/external-auth.md` |
| "Audit logging — what to enable, log rotation, SIEM integration" | `references/audit-logging.md` |
| "Encryption at rest — DARE, KMIP, key rotation" | `references/encryption-at-rest.md` |
| "Network hardening — ports, firewall rules, node-to-node TLS" | `references/network-hardening.md` |

## Security hardening checklist

Before going to production, verify all of these:

**Authentication & access:**
- [ ] Default `Administrator` password changed from the default
- [ ] All application connections use dedicated service accounts (not Administrator)
- [ ] All service accounts have minimum required roles only
- [ ] RBAC groups defined so roles are assigned via group, not per-user
- [ ] Password policy configured (min length ≥ 12, complexity, rotation)
- [ ] Account lockout enabled (8.x: `admin_user_lockout_settings`)
- [ ] External auth (LDAP/AD) configured if your organization requires centralized identity

**Network & encryption:**
- [ ] TLS enabled and TLS 1.2+ enforced (TLS 1.0 / 1.1 disabled)
- [ ] Node-to-node encryption enabled (cluster internal traffic)
- [ ] All client SDK connections use `couchbases://` (TLS)
- [ ] Ports restricted to Couchbase service ports only (see `network-hardening.md`)
- [ ] Cluster nodes on a private network, not directly internet-accessible
- [ ] Capella: allowed CIDRs configured; no 0.0.0.0/0

**Data protection:**
- [ ] Encryption at rest (DARE) enabled if required by compliance
- [ ] KMIP configured if your org requires external key management
- [ ] Backup encryption enabled (cbbackupmgr `--encrypted`)

**Audit & visibility:**
- [ ] Audit logging enabled
- [ ] `admin_loggedIn` and `admin_loggedOut` events captured
- [ ] `mutateDocument` events captured for sensitive collections
- [ ] Audit log rotation and retention configured
- [ ] Audit logs shipped to SIEM

## Quick tool map

| Task | Tool |
|---|---|
| Get current security settings | `admin_cluster_get_security_settings` |
| Update security settings (TLS, sessions) | `admin_cluster_update_security_settings` |
| Configure password policy | `admin_cluster_set_password_policy` |
| Get/update auto-failover (security adjacent) | `admin_cluster_get_auto_failover_settings` |
| User management | `admin_user_*` |
| Group management | `admin_group_*` |
| List roles | `admin_user_list_roles` |
| Check current user permissions | `admin_user_check_permissions` |
| Encryption settings (DARE) | `admin_encryption_get_settings`, `admin_encryption_update_settings` |
| KMIP configuration | `admin_kmip_*` |
| Audit log configuration | `admin_cluster_get_audit_config`, `admin_cluster_update_audit_config` |
| User lockout (8.x) | `admin_user_lock`, `admin_user_unlock`, `admin_user_get_lockout_settings` |

## Related skills

- `couchbase-mcp` — the actual security tools
- `couchbase-app-integration` — TLS/mTLS configuration in application SDK clients
- `couchbase-observability` — shipping audit logs and security metrics to monitoring systems
- `couchbase-backup-restore` — backup encryption configuration
