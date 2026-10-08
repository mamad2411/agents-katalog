---
name: "multi-tenant-saas-readiness"
description: "Review multi-tenant SaaS production readiness for tenant isolation, auth tenancy, trusted host routing, provisioning, impersonation, DNS, CORS, rate limits, audit logging, and cross-tenant tests. Use before launching or hardening a tenant-subdomain, organization-scoped, or customer-workspace SaaS product."
---

# Multi-Tenant SaaS Readiness

Assess whether a multi-tenant product can safely run in production without
tenant data leaks, auth bypasses, or unrecoverable operator gaps.

## Workflow

1. Identify tenant boundaries: org/workspace records, domain mapping, tenant ids,
   membership tables, role models, and privileged system-admin paths.
2. Trace tenant resolution from request entry to data access. Confirm the
   effective tenant comes from a trusted boundary, not client-controlled input.
3. Review auth tenancy: token tenant id, session cookie scope, provider tenant
   selection, custom claims, role/status checks, and production bypass removal.
4. Inspect provisioning and lifecycle flows: tenant creation, default roles,
   invites, first sign-in binding, suspension, domain verification, and teardown.
5. Check operator controls: impersonation, audit logs, request ids, safe entity
   ids, rate limits, CORS, DNS, and production support runbooks.
6. Require focused tests or smoke checks for cross-tenant denial, host/token
   mismatch, impersonation auditability, and production auth configuration.

## Readiness Gates

- Tenant-scoped data access is enforced server-side or at the database/security
  rule layer for every sensitive object.
- Tenant host or domain routing fails closed when headers are missing,
  untrusted, mismatched, or ambiguous.
- Auth tokens, session cookies, and tenant provider configuration agree on the
  same tenant before privileged reads or writes.
- Super-admin and impersonation flows are explicit, time-limited, auditable, and
  unavailable to normal tenant users.
- Production disables mock users, local auth bypasses, tenant override headers,
  and demo seed paths unless they are separately protected.
- CORS, rate limits, secret ownership, DNS, and authorized auth domains match
  the production tenant model.

## Findings

Promote a finding when there is concrete evidence of tenant confusion, unsafe
fallbacks, missing tests for critical boundaries, or production configuration
that could route users into the wrong tenant.

Do not require a specific cloud provider or identity provider. Map the checks to
the product's chosen stack.

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Severity rubric: `../_shared-project-ops/references/severity-rubric.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
