---
name: mongodb-analyze-security
description: Analyze self-managed MongoDB authentication, authorization, RBAC, internal keyfile or x.509 authentication, LDAP/AD integration where licensed/configured, TLS, and least-privilege access. Use for security architecture or access failures.
---

# Analyze Security

1. Identify MongoDB edition/version, authentication mechanisms, users/roles, and internal member authentication.
2. Inspect RBAC assignments and least-privilege requirements.
3. For replica/sharded clusters, inspect keyfile or x.509 internal authentication as configured.
4. Inspect TLS settings and certificate validity/trust.
5. Evaluate LDAP/AD integration only when supported and actually deployed.
6. Never expose passwords, keyfiles, private keys, or credentials.

## Output
- Authentication Model
- RBAC Findings
- Internal Auth/TLS Findings
- Failure Layer
- Recommended Action
