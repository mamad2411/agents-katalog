---
name: enterprise-web
description: Enterprise web application assessment across SSO, role matrix, admin console, tenant isolation, and integration boundaries. Covers scope partitioning, identity-provider-aware recon, privilege-tier enumeration, business-logic mapping, and safe validation within enterprise constraints.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, role-matrix, integration-map]
---

# Enterprise web assessment

Use this skill to assess authorized internal or internet-facing enterprise web applications. Enterprise apps differ from single-tenant SaaS: identity providers (IdP), role hierarchies, admin consoles, tenant boundaries, integration surfaces, and compliance-constrained environments all change the threat model. This skill structures assessment around those differences while keeping every active step gated.

## Required inputs

- Target list with environment labels (production, staging, dev, DR, admin).
- Scope file with explicit tenant, role, and integration boundaries.
- Identity-provider context when SSO is in use: IdP type (Entra ID, Okta, Ping, Keycloak, Auth0), protocol (SAML, OIDC, WS-Fed), and whether IdP itself is in scope.
- Test accounts per role tier (at minimum: unauthenticated, low-privilege user, elevated user). Never use production admin accounts without explicit written approval.
- List of known third-party integrations, embedded widgets, iframes, and backend-to-backend API calls visible in the application.
- Authorization cache valid for all in-scope hosts.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every host, subdomain, admin panel, and integration endpoint before contact.
3. Use `pentest_agent_check_authorization` before any active request.
4. Use `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. Use `pentest_agent_execute_tool` for all active execution with timeout, rate-limit, approval, and output policy enforcement.
6. Use `pentest_agent_append_evidence` for role matrices, integration maps, header audit results, and per-endpoint observations.

## Workflow

### Phase 1 — Environment partitioning and scope validation

Map the full attack surface before sending a single request.

- Identify every environment listed in scope: production, staging, UAT, QA, dev, DR, admin, and internal tooling subdomains.
- For each environment, determine the identity boundary: shared IdP or separate tenant, shared session store or isolated, shared backend APIs or independent.
- Flag environments where SSO session cookies issued by the IdP grant access across multiple in-scope hosts. This cross-environment session trust is a key enterprise risk.
- Confirm that staging, dev, and pre-production environments are explicitly in scope. Enterprise apps often share backend infrastructure across environments; testing one may affect another.
- Document the environment map with `pentest_agent_append_evidence` before active testing.

### Phase 2 — Identity-provider and authentication surface

Understand the authentication flow before testing application logic.

- Identify every login flow: primary SSO, direct login fallback, API-key paths, service-account endpoints, and legacy authentication endpoints.
- Map redirect URIs, SAML assertion consumers, and OIDC callback URLs to confirm they are constrained.
- Check whether the IdP exposes a tenant selection or organization-switching endpoint reachable after authentication. Cross-tenant access in multi-tenant IdPs is a common enterprise finding.
- Inspect session cookie attributes across environments: Domain scope, Path, Secure, HttpOnly, SameSite. A cookie scoped to `.example.com` that is valid across prod, staging, and admin is a lateral-movement enabler.
- If the application supports direct username/password in addition to SSO, verify whether MFA is enforced on the direct path. Enterprise SSO often bypasses app-level MFA controls.

### Phase 3 — Role matrix enumeration

Map every privilege tier and test horizontal/vertical access boundaries.

- Enumerate all known roles from documentation, JWT claims, SAML attributes, or API responses. Common enterprise tiers: anonymous, authenticated user, manager, org-admin, system-admin, support-agent, auditor/read-only, API service account.
- For each role, collect a session token (or API key). If some roles are unavailable, document the gap.
- Test every enumerated API endpoint and UI route against every role token. A support-agent token accessing a system-admin endpoint is a vertical-privilege-escalation candidate.
- Test tenant-scoped endpoints for cross-tenant access: replace tenant IDs, org slugs, or workspace UUIDs in requests while holding a different tenant's token.
- Document the full role-to-endpoint matrix.

### Phase 4 — Admin console and management-plane assessment

Admin consoles in enterprise apps often run on separate hosts with weaker controls.

- Locate admin interfaces: dedicated subdomains (`admin.example.com`), path-prefixed consoles (`/admin`, `/management`), and hidden management APIs consumed by internal tooling.
- Check whether admin consoles enforce the same authentication and authorization policy as the main application. Common gaps: admin host accepts lower-privilege session cookies, admin API trusts internal network origin, or admin console skips MFA.
- Enumerate management-plane capabilities: user provisioning, role assignment, tenant creation, billing modification, configuration export, audit-log access.
- Test whether a low-privilege user's token can reach admin endpoints. Even a 403 is informational; a 200 with data is critical.
- Document admin surface with `pentest_agent_append_evidence`.

### Phase 5 — Integration and supply-chain surface

Enterprise apps embed third-party widgets, analytics, support chat, payment iframes, SSO integrations, and backend-to-backend API calls.

- Map every external origin loaded by the application: scripts, iframes, stylesheets, fonts, images, and XHR/fetch targets. Use browser DevTools or catalog tools like `httpx` with `-tech-detect`.
- For each integration, identify whether it receives session tokens, user data, or tenant context via URL parameters, POST bodies, or Referer headers.
- Check CSP and frame-ancestors directives for gaps that allow untrusted origins to embed or read application pages.
- Test whether integrations can be abused for data exfiltration: a chat widget that echoes URL parameters, an analytics beacon that receives PII in the page title, or a support iframe that leaks the parent origin.
- Document the integration map and trust boundaries.

### Phase 6 — Business-logic and workflow review

Enterprise workflows span multiple steps, roles, and approval chains. Test the gaps between steps.

- Map critical business workflows: user provisioning, role changes, financial transactions, data export, configuration changes, and tenant creation.
- For each workflow, identify state-transition points where authorization is checked. Common gaps: the first step checks permission but subsequent steps do not, or the API allows skipping intermediate steps.
- Test workflow state manipulation: replay a completed step, skip an approval step, or modify the workflow state identifier in the request.
- Test bulk operations and CSV export functions for authorization bypass and excessive data exposure.
- Test notification and email triggers for injection, spoofing, and data leakage.

## Decision points

- Environment scope: if staging and production share an IdP, coordinate with the security contact before testing authentication flows that could affect production sessions.
- Role token collection: if obtaining tokens for all roles is infeasible, prioritize unauthenticated, low-privilege, and the most sensitive admin role.
- Integration testing: if a third-party integration is out of scope, still document it but do not send active requests to the external origin.
- Workflow depth: if a workflow spans out-of-scope systems, stop at the scope boundary and document the architectural risk.
- Admin console coverage: if the admin console is a COTS product, shift from custom-logic testing to configuration and access-control review.

## Prohibited behavior

No testing against production admin accounts without explicit written authorization. No modifying production user data, roles, or configurations. No inviting real users, triggering real notifications, or altering billing state. No accessing customer data belonging to other tenants. No credential attacks against the IdP unless the IdP is explicitly in scope and approved. No denial-of-service against shared enterprise infrastructure. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop active testing on a host or endpoint if: the target is outside authorized scope, the authorization cache has expired, a WAF or rate limiter signals blocking, you encounter production user data or PII, an action would modify production state, the environment label conflicts with the authorization (e.g., production in scope but only staging authorized), or user consent is revoked.

## Evidence

For each phase, append evidence records via `pentest_agent_append_evidence`:
- Environment partition map with identity boundaries.
- Role-to-endpoint access matrix (redacted tokens, only status codes and response-size deltas).
- Admin console inventory with authentication-policy notes.
- Integration map: origin, data received, trust relationship.
- Workflow state diagrams and identified authorization gaps.

Never store session tokens, cookies, passwords, PII, customer data, integration secrets, IdP metadata containing keys, or raw response bodies containing user content.

## Report handoff

Generate findings via `pentest_agent_record_finding` for each confirmed authorization gap, cross-tenant access, admin-console bypass, or workflow flaw. Render the final report with `pentest_agent_render_report` using a template appropriate to the engagement mode. Include the environment map, role matrix summary, integration trust diagram, and prioritized remediation recommendations grouped by risk tier.
