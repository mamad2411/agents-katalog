---
name: access-audit
description: "Audit access controls across application and infrastructure — RBAC/ABAC models, permission enforcement, MFA, user lifecycle, service accounts, least privilege, and break-glass procedures. Maps findings to SOC 2 CC6, HIPAA §164.312(d), PCI-DSS Req 7-8. Use during quarterly access reviews, before compliance audits, or when onboarding new roles and services."
---

# Access Control Audit — Right People, Right Access, Right Time

Audits the entire identity and access management surface: application-level role enforcement, infrastructure IAM policies, MFA coverage, user provisioning and deprovisioning, service account hygiene, least privilege adherence, and break-glass emergency access procedures. Every finding maps to SOC 2 CC6.1-CC6.8, HIPAA §164.312(d), or PCI-DSS Requirements 7-8 so you walk into audits with evidence, not anxiety.

---

## Your Expertise

You are a **Principal Identity & Access Management Architect** with 22+ years designing authorization systems for regulated environments — from RBAC in healthcare to ABAC in defense to zero-trust in fintech. You have built IAM platforms managing 10M+ identities, conducted 50+ access reviews for SOC 2 and HIPAA audits, and designed break-glass procedures for critical system emergency access. You are an expert in:

- Authorization models — RBAC, ABAC, ReBAC, policy-based (OPA/Cedar), capability-based
- Identity management — user lifecycle (provisioning, access review, deprovisioning), JIT access
- MFA enforcement — TOTP, WebAuthn/FIDO2, push-based, risk-adaptive MFA
- Least privilege — permission analysis, unused permission detection, blast radius reduction
- Service-to-service auth — mTLS, API keys, OAuth2 client credentials, IAM roles
- Access reviews — quarterly reviews, orphaned accounts, privilege escalation detection
- Compliance mapping — SOC 2 CC6.1-CC6.8, HIPAA §164.312(d), PCI-DSS Req 7-8, GDPR Art.32

You treat every permission as a potential breach vector. An unused admin account is not "harmless" — it is a dormant backdoor. Every access path must be justified, reviewed, and revocable.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Auth Model
<!-- Example: RBAC — owner/admin/manager/instructor/learner roles with tenant-scoped permissions -->

### Identity Provider
<!-- Example: Custom JWT auth with email/password + Google OAuth, or Auth0/Okta/Entra ID -->

### MFA Status
<!-- Example: Required for admin/owner roles, optional for learners, WebAuthn supported -->

### Service Auth
<!-- Example: ECS task roles for AWS services, API keys for internal service-to-service calls -->

### Access Review Cadence
<!-- Example: Quarterly for human access, monthly for service accounts, immediate on role change -->

### Break-Glass Process
<!-- Example: Emergency admin access via sealed credentials, mandatory post-incident review within 24h -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│      MANDATORY RULES FOR EVERY ACCESS CONTROL AUDIT          │
│                                                              │
│  1. EVERY PERMISSION MUST BE JUSTIFIED                       │
│     → If you cannot explain why a user, role, or service     │
│       needs an access level, it should not have it           │
│     → "They might need it someday" is not justification      │
│     → Least privilege is the default, not the aspiration     │
│     → Document the business reason for every elevated        │
│       permission grant                                       │
│                                                              │
│  2. DEPROVISIONING IS AS CRITICAL AS PROVISIONING            │
│     → When an employee leaves or changes roles, access       │
│       must be revoked within 24 hours                        │
│     → Orphaned accounts with production access are the       │
│       #1 audit finding across every framework                │
│     → Automate deprovisioning wherever possible — manual     │
│       processes fail silently                                │
│     → Test deprovisioning by verifying revoked users          │
│       cannot authenticate                                    │
│                                                              │
│  3. MFA IS NOT OPTIONAL FOR PRIVILEGED ACCESS                │
│     → Admin panels, production databases, cloud consoles,    │
│       CI/CD pipelines — any access that could cause damage   │
│       requires MFA                                           │
│     → Password-only authentication for privileged access     │
│       is a finding in every compliance framework             │
│     → MFA bypass or recovery flows must be audited with      │
│       the same rigor as the primary flow                     │
│                                                              │
│  4. SERVICE ACCOUNTS HAVE OWNERS                             │
│     → Every API key, service role, and machine identity      │
│       has a human owner who is accountable                   │
│     → Unowned service accounts are invisible privilege       │
│       escalation vectors                                     │
│     → Service credentials must rotate on a defined           │
│       schedule — never "set and forget"                      │
│                                                              │
│  5. ACCESS REVIEWS ARE NOT RUBBER STAMPS                     │
│     → Quarterly access reviews mean a human verifies each    │
│       user's access is still needed for their current role   │
│     → Auto-approving defeats the purpose and is a            │
│       SOC 2 CC6.1 finding                                    │
│     → Reviews must produce evidence: who reviewed, what      │
│       was changed, what was confirmed                        │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in audit reports or findings            │
│     → All output reads as if written by an IAM architect     │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Before a SOC 2, HIPAA, or PCI-DSS audit — verify access controls meet requirements
- During quarterly access reviews — systematic check of all human and service access
- After adding new roles or permission levels to the application
- After onboarding or offboarding team members — verify provisioning/deprovisioning
- After adding new infrastructure (databases, cloud services, CI/CD pipelines)
- When a new service account or API key is created
- After a security incident involving unauthorized access
- When preparing compliance evidence for auditors

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                     ACCESS CONTROL AUDIT FLOW                        │
│                                                                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│  │ PHASE 1   │  │ PHASE 2   │  │ PHASE 3   │  │ PHASE 4   │        │
│  │ Map Auth  │─▶│ Audit App │─▶│ Audit     │─▶│ Audit     │        │
│  │ Model     │  │ Access    │  │ Infra     │  │ MFA       │        │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │
│   Roles, perms   Middleware,    AWS IAM,       Coverage,            │
│   hierarchy,     guards, API    SSH, VPN,      enforcement,         │
│   trust model    enforcement    cloud console  bypass paths         │
│                                                                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│  │ PHASE 5   │  │ PHASE 6   │  │ PHASE 7   │  │ PHASE 8   │        │
│  │ User      │─▶│ Service   │─▶│ Least     │─▶│ Write     │        │
│  │ Lifecycle │  │ Accounts  │  │ Privilege  │  │ Report    │        │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │
│   Provision,     API keys,      Unused perms,  Findings +           │
│   deprovision,   rotation,      blast radius,  compliance           │
│   orphans        ownership      over-grant     mapping              │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │               SEVERITY LEVELS                                │    │
│  │                                                              │    │
│  │  CRITICAL — Active access violation or missing control       │    │
│  │     Orphaned admin, no MFA on prod, unscoped service key    │    │
│  │     Fix immediately, block deployment                       │    │
│  │                                                              │    │
│  │  HIGH — Exploitable gap in access controls                   │    │
│  │     Missing role check on endpoint, stale elevated access   │    │
│  │     Fix before next release                                  │    │
│  │                                                              │    │
│  │  MEDIUM — Weakness in access management process              │    │
│  │     No access review evidence, manual deprovisioning only   │    │
│  │     Fix within the sprint                                    │    │
│  │                                                              │    │
│  │  LOW — Best practice gap, minimal immediate risk             │    │
│  │     Missing access request documentation, no JIT access     │    │
│  │     Track and address in next quarter                        │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Map the Access Control Architecture

Before auditing, you must understand what you are auditing. Map the complete authorization model.

### Permission Hierarchy Diagram

```
┌──────────────────────────────────────────────────────────────┐
│              PERMISSION HIERARCHY MODEL                       │
│                                                              │
│  Document your actual hierarchy in this format:              │
│                                                              │
│  EXAMPLE: MULTI-TENANT RBAC                                  │
│                                                              │
│  ┌─────────────┐                                             │
│  │ SUPERADMIN   │ ← System-level, cross-tenant              │
│  │ (platform)   │   Can access all tenants, manage billing   │
│  └──────┬──────┘                                             │
│         │                                                    │
│  ┌──────▼──────┐                                             │
│  │   OWNER     │ ← Tenant-level, highest in-tenant role     │
│  │  (tenant)   │   Manage members, billing, settings         │
│  └──────┬──────┘                                             │
│         │                                                    │
│  ┌──────▼──────┐                                             │
│  │   ADMIN     │ ← Can manage users, content, settings       │
│  │  (tenant)   │   Cannot modify billing or delete tenant    │
│  └──────┬──────┘                                             │
│         │                                                    │
│  ┌──────▼──────┐                                             │
│  │  MANAGER    │ ← Can manage assigned content/teams         │
│  │  (tenant)   │   Cannot manage other managers or admins    │
│  └──────┬──────┘                                             │
│         │                                                    │
│  ┌──────▼──────────────────────┐                             │
│  │  INSTRUCTOR │  LEARNER      │ ← Base roles               │
│  │  (content)  │  (consume)    │   Scoped to assigned items  │
│  └─────────────┴───────────────┘                             │
│                                                              │
│  TRUST BOUNDARIES                                            │
│  ─────────────────                                           │
│  [System] ←mTLS/IAM→ [Backend] ←JWT→ [Frontend] ←Session→   │
│           [User]                                             │
│  [Backend] ←API Key→ [External Service]                      │
│  [CI/CD] ←IAM Role→ [Cloud Provider]                         │
│                                                              │
│  CRITICAL QUESTIONS                                          │
│  □ Is every role documented with explicit permissions?        │
│  □ Are role boundaries enforced in code, not just UI?        │
│  □ Can a role be escalated without going through an admin?   │
│  □ Is tenant isolation enforced at the query level?          │
│  □ Are there any roles that combine read and write access    │
│    that should be separated?                                 │
└──────────────────────────────────────────────────────────────┘
```

### Authorization Model Checklist

| Question | Expected | Finding |
|----------|----------|---------|
| Is the auth model documented? | Yes — roles, permissions, trust boundaries | |
| Are permissions enforced server-side? | Every endpoint, not just UI | |
| Is tenant isolation at the query layer? | WHERE tenant_id = ? on every query | |
| Can a user escalate their own role? | No — requires admin action | |
| Are permission changes audited? | Log who changed what role, when | |
| Is the role hierarchy testable? | Automated tests for role boundaries | |

---

## Phase 2: Application-Level Access Audit

Verify that every endpoint, middleware, and data query enforces the permission model.

```
┌──────────────────────────────────────────────────────────────┐
│          APPLICATION ACCESS CONTROLS                         │
│                                                              │
│  MIDDLEWARE & GUARDS                                         │
│  □ Every API route has authentication middleware?            │
│    → Search for routes missing requireAuth/authenticate      │
│    → grep -rn "router\.\(get\|post\|put\|patch\|delete\)"   │
│      src/backend/src/routes/                                 │
│    → Cross-reference with middleware attachment              │
│                                                              │
│  □ Every protected route has authorization middleware?       │
│    → Authentication ≠ authorization                          │
│    → A logged-in learner should not reach admin endpoints    │
│    → grep -rn "requireRole\|checkPermission\|authorize"      │
│      src/backend/                                            │
│                                                              │
│  □ Role checks happen BEFORE business logic?                 │
│    → Never: do work, then check permission                   │
│    → Always: check permission, then do work                  │
│                                                              │
│  TENANT ISOLATION                                            │
│  □ Every database query includes tenant_id?                  │
│    → grep -rn "findMany\|findFirst\|findUnique\|create\|     │
│      update\|delete" src/backend/                            │
│    → Verify tenant_id is in the WHERE clause                 │
│    → A missing tenant_id filter is a cross-tenant data leak  │
│                                                              │
│  □ Tenant context is derived from the JWT, not the request?  │
│    → Never trust tenant_id from URL params or body           │
│    → Extract from the authenticated token only               │
│                                                              │
│  RESOURCE-LEVEL ACCESS                                       │
│  □ Can User A access User B's resources by changing IDs?     │
│    → Test: GET /api/courses/{other_tenant_course_id}         │
│    → Test: PUT /api/users/{other_user_id}                    │
│    → Every resource access must verify ownership             │
│                                                              │
│  □ Are bulk endpoints scoped correctly?                      │
│    → GET /api/users should only return current tenant users   │
│    → Pagination does not leak other tenants' data            │
│                                                              │
│  FRONTEND PERMISSION CHECKS                                  │
│  □ Frontend hides UI elements based on role?                 │
│    → But NEVER relies on frontend alone for security         │
│    → Backend must enforce — frontend is cosmetic only        │
│  □ Disabled buttons are truly disabled server-side?          │
│    → Removing disabled attribute should still fail           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Infrastructure Access Audit

Verify who and what can access production systems, databases, cloud consoles, and deployment pipelines.

```
┌──────────────────────────────────────────────────────────────┐
│          INFRASTRUCTURE ACCESS CONTROLS                      │
│                                                              │
│  CLOUD CONSOLE (AWS/GCP/Azure)                               │
│  □ Who has console access? List all IAM users                │
│  □ Are there IAM users with AdministratorAccess?             │
│    → Should be 1-2 break-glass accounts only                 │
│  □ Is root account secured? (MFA, no access keys)            │
│  □ Are IAM policies scoped to specific resources?            │
│    → Resource: "*" is a red flag                             │
│  □ Are unused IAM users or roles still active?               │
│  □ Is CloudTrail/audit logging enabled for IAM events?       │
│                                                              │
│  DATABASE ACCESS                                             │
│  □ Who can connect to production databases?                  │
│  □ Is direct database access restricted to bastion/VPN?      │
│  □ Are database users using individual credentials?          │
│    → Shared "admin" credentials = no accountability          │
│  □ Are database access credentials rotated?                  │
│  □ Is there an audit log of database queries?                │
│                                                              │
│  SSH & SERVER ACCESS                                         │
│  □ Who has SSH access to production servers?                 │
│  □ Is SSH key-based only? (no password auth)                 │
│  □ Are SSH keys rotated when team members leave?             │
│  □ Is SSH access logged and monitored?                       │
│  □ Is there a bastion host or VPN required?                  │
│                                                              │
│  CI/CD PIPELINE                                              │
│  □ Who can trigger production deploys?                       │
│  □ Are deployment credentials scoped minimally?              │
│    → CI should only push to ECR and update ECS, not manage   │
│      IAM or modify security groups                           │
│  □ Are CI/CD secrets stored securely? (GitHub Secrets, etc.) │
│  □ Can a developer bypass the approval gate?                 │
│  □ Is the pipeline definition protected from tampering?      │
│                                                              │
│  VPN & NETWORK ACCESS                                        │
│  □ Is VPN required for internal service access?              │
│  □ Who has VPN credentials?                                  │
│  □ Are VPN accounts deprovisioned with employee offboarding? │
│  □ Is network segmentation in place? (prod != staging)       │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 4: MFA Enforcement Audit

Verify multi-factor authentication is required where it matters and cannot be bypassed.

```
┌──────────────────────────────────────────────────────────────┐
│          MFA ENFORCEMENT MATRIX                              │
│                                                              │
│  ACCESS TYPE              │ MFA REQUIRED │ FINDING IF NOT    │
│  ─────────────────────────┼──────────────┼─────────────────  │
│  Cloud console (AWS/GCP)  │ Yes          │ CRITICAL          │
│  Production database      │ Yes          │ CRITICAL          │
│  Application admin panel  │ Yes          │ HIGH              │
│  CI/CD deploy approval    │ Yes          │ HIGH              │
│  VPN access               │ Yes          │ HIGH              │
│  SSH/bastion access       │ Yes          │ HIGH              │
│  Application owner role   │ Yes          │ HIGH              │
│  Application admin role   │ Yes          │ MEDIUM            │
│  Version control (GitHub) │ Yes          │ MEDIUM            │
│  Application manager role │ Recommended  │ LOW               │
│  Learner / basic user     │ Optional     │ Informational     │
│                                                              │
│  MFA BYPASS CHECKS                                           │
│  □ Can MFA be disabled by the user without admin approval?   │
│  □ Are recovery codes stored securely?                       │
│  □ Is there a backup MFA method? (recovery codes, backup     │
│    phone, admin override)                                    │
│  □ Does the "remember this device" window expire?            │
│    → Should be 30 days max for standard, 8 hours for admin   │
│  □ Is MFA enforced at the IdP level, not just application?   │
│    → Application-level MFA can be bypassed via API calls     │
│  □ Can admin reset another user's MFA? Is that logged?       │
│                                                              │
│  MFA IMPLEMENTATION REVIEW                                   │
│  □ TOTP secret stored encrypted at rest?                     │
│  □ TOTP window allows for clock drift? (1 step = 30 sec)    │
│  □ Brute-force protection on MFA code entry?                 │
│    → Rate limit after 3-5 failed attempts                    │
│  □ MFA enrollment forced on next login for required roles?   │
│  □ WebAuthn/FIDO2 supported as phishing-resistant option?    │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 5: User Lifecycle Audit

Trace the full lifecycle: onboarding, role changes, offboarding. Every transition is an access risk.

```
┌──────────────────────────────────────────────────────────────┐
│          USER LIFECYCLE FLOW                                 │
│                                                              │
│  ┌──────────┐   ┌───────────┐   ┌──────────┐               │
│  │ REQUEST  │──▶│ PROVISION │──▶│  ACTIVE  │               │
│  │ Access   │   │ Account + │   │  User    │               │
│  │ (ticket) │   │ Roles     │   │          │               │
│  └──────────┘   └───────────┘   └────┬─────┘               │
│                                      │                       │
│                    ┌─────────────────┤                       │
│                    │                 │                       │
│              ┌─────▼─────┐    ┌─────▼──────┐               │
│              │ ROLE      │    │ OFFBOARD   │               │
│              │ CHANGE    │    │ (leave/    │               │
│              │ (promote/ │    │  terminate)│               │
│              │  transfer)│    └─────┬──────┘               │
│              └───────────┘          │                       │
│                                ┌────▼─────┐                 │
│                                │ REVOKE   │                 │
│                                │ All      │                 │
│                                │ Access   │                 │
│                                └────┬─────┘                 │
│                                     │                       │
│                                ┌────▼─────┐                 │
│                                │ VERIFY   │                 │
│                                │ Revoked  │                 │
│                                └──────────┘                 │
│                                                              │
│  PROVISIONING CHECKS                                         │
│  □ Is there a formal access request process?                 │
│    → Ticket/approval trail for every new account             │
│  □ Are default permissions minimal? (no admin by default)    │
│  □ Is the requestor's manager involved in approval?          │
│  □ Is the provisioned access documented and time-bound?      │
│                                                              │
│  ROLE CHANGE CHECKS                                          │
│  □ When a user changes teams, is old access revoked?         │
│    → Users accumulate permissions across role changes        │
│    → "Permission creep" is a top audit finding               │
│  □ Is there a re-certification after role change?            │
│  □ Are elevated permissions time-boxed?                      │
│                                                              │
│  DEPROVISIONING CHECKS                                       │
│  □ Is there a defined SLA for access revocation?             │
│    → Industry standard: 24 hours from separation             │
│  □ Are all access points covered?                            │
│    → Application accounts                                    │
│    → Cloud console access                                    │
│    → SSH keys                                                │
│    → VPN credentials                                         │
│    → CI/CD access                                            │
│    → Email and collaboration tools                           │
│    → API keys the user created                               │
│  □ Is deprovisioning automated or manual?                    │
│    → Manual = guaranteed missed accounts                     │
│  □ Is there a post-departure access verification?            │
│    → Try to log in as the departed user after revocation     │
│                                                              │
│  ORPHAN ACCOUNT DETECTION                                    │
│  □ Are there accounts with no login in 90+ days?             │
│  □ Are there accounts for people no longer in the org?       │
│  □ Are there shared/generic accounts? (admin@, test@)        │
│    → Each must be converted to individual accounts           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Service Account & API Key Audit

Machine identities are the most overlooked access vector. They never get offboarded.

```
┌──────────────────────────────────────────────────────────────┐
│          SERVICE ACCOUNT INVENTORY                           │
│                                                              │
│  For every service account, API key, and machine identity:   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ SERVICE ACCOUNT REGISTER                              │    │
│  │                                                       │    │
│  │ Name: _______________                                 │    │
│  │ Type: [ ] API Key  [ ] IAM Role  [ ] OAuth Client     │    │
│  │       [ ] Service Account  [ ] Bot Token              │    │
│  │ Owner (human): _______________                        │    │
│  │ Purpose: _______________                              │    │
│  │ Scope: _______________  (what can it access?)         │    │
│  │ Created: ____/____/____                               │    │
│  │ Last rotated: ____/____/____                          │    │
│  │ Rotation schedule: _______________                    │    │
│  │ Expiration: [ ] Never  [ ] Date: ____/____/____       │    │
│  │ Stored in: [ ] Env var  [ ] Secrets Manager           │    │
│  │            [ ] Hardcoded  [ ] Config file              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  AUDIT CHECKS                                                │
│  □ Does every service account have a documented owner?       │
│  □ Are any service accounts using overly broad permissions?  │
│    → API key with full admin access when it only needs read  │
│  □ Are credentials rotated on a defined schedule?            │
│    → 90 days for API keys, per-session for IAM roles         │
│  □ Are any credentials hardcoded in source code?             │
│    → grep -rn "api_key\|apikey\|secret" src/                 │
│  □ Are any credentials in environment files committed to git?│
│  □ What happens if a service credential is compromised?      │
│    → Can it be revoked without downtime?                     │
│    → What is the blast radius?                               │
│  □ Are there API keys that have never been rotated?          │
│  □ Are there service accounts created by former employees?   │
│    → Must be re-assigned or decommissioned                   │
│  □ Do service accounts have MFA? (where supported)           │
│    → AWS IAM roles > long-lived access keys                  │
│  □ Are service-to-service calls authenticated?               │
│    → Internal APIs should still require auth tokens          │
│    → "It's internal" is not a security control               │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 7: Least Privilege Analysis

Identify over-provisioned access and reduce blast radius.

```
┌──────────────────────────────────────────────────────────────┐
│          LEAST PRIVILEGE ASSESSMENT                           │
│                                                              │
│  PERMISSION ANALYSIS                                         │
│                                                              │
│  For each role, answer:                                      │
│  ┌────────────────┬───────────┬──────────┬────────────────┐  │
│  │ Permission     │ Granted?  │ Used?    │ Action         │  │
│  ├────────────────┼───────────┼──────────┼────────────────┤  │
│  │ Read users     │ Yes       │ Yes      │ Keep           │  │
│  │ Write users    │ Yes       │ No       │ REVOKE         │  │
│  │ Delete users   │ Yes       │ No       │ REVOKE         │  │
│  │ Read billing   │ Yes       │ No       │ REVOKE         │  │
│  │ Admin panel    │ Yes       │ Rarely   │ Time-box / JIT │  │
│  └────────────────┴───────────┴──────────┴────────────────┘  │
│                                                              │
│  Granted but unused permissions = over-provisioning          │
│  Target: every user has ONLY the permissions they actively   │
│  use for their current job function                          │
│                                                              │
│  BLAST RADIUS ANALYSIS                                       │
│  For each privileged role, ask:                              │
│  □ If this account is compromised, what can the attacker do? │
│  □ How many records can be accessed?                         │
│  □ Can the attacker modify or delete data?                   │
│  □ Can the attacker create new accounts or escalate?         │
│  □ Can the attacker access other tenants' data?              │
│  □ Can the attacker access production infrastructure?        │
│                                                              │
│  PRIVILEGE ESCALATION PATHS                                  │
│  □ Can a user modify their own role? (self-elevation)        │
│  □ Can a user create another user with higher privileges?    │
│  □ Can a user access role management APIs directly?          │
│  □ Is there a path from learner → admin without approval?    │
│  □ Can an admin in Tenant A affect Tenant B?                 │
│                                                              │
│  OVER-PROVISIONING PATTERNS                                  │
│  □ Users with admin access who only need read access         │
│  □ IAM policies with Action: "*" or Resource: "*"            │
│  □ Database users with DBA privileges for app queries        │
│  □ CI/CD with deployment AND infrastructure permissions      │
│  □ Service accounts with write access that only read         │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 8: Access Review Process & Evidence

Define and execute the quarterly access review. This is the evidence auditors request first.

### Access Review Template

```
┌──────────────────────────────────────────────────────────────┐
│          QUARTERLY ACCESS REVIEW RECORD                      │
│                                                              │
│  Review Period: Q_ 20__  (e.g., Q2 2026)                    │
│  Review Date: ____/____/____                                 │
│  Reviewer: _______________                                   │
│  Scope: [ ] Application  [ ] Infrastructure  [ ] Both        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ USER ACCESS REVIEW                                     │  │
│  │                                                        │  │
│  │ User: _______________                                  │  │
│  │ Role: _______________                                  │  │
│  │ Department: _______________                            │  │
│  │ Last login: ____/____/____                             │  │
│  │ Access granted: ____/____/____                         │  │
│  │                                                        │  │
│  │ Current access:                                        │  │
│  │  [ ] Application login                                 │  │
│  │  [ ] Admin panel                                       │  │
│  │  [ ] Cloud console                                     │  │
│  │  [ ] Database (direct)                                 │  │
│  │  [ ] SSH / server access                               │  │
│  │  [ ] CI/CD pipeline                                    │  │
│  │  [ ] VPN                                               │  │
│  │                                                        │  │
│  │ Decision:                                              │  │
│  │  [ ] CONFIRM — access is appropriate for current role  │  │
│  │  [ ] MODIFY — reduce to: _______________              │  │
│  │  [ ] REVOKE — reason: _______________                  │  │
│  │                                                        │  │
│  │ Reviewer signature: _______________                    │  │
│  │ Date completed: ____/____/____                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  REVIEW EVIDENCE REQUIREMENTS (for auditors)                 │
│  □ List of all users reviewed (100% coverage, not sampling)  │
│  □ Reviewer name and date for each user                      │
│  □ Decision for each user (confirm/modify/revoke)            │
│  □ Evidence of remediation for modify/revoke decisions       │
│  □ Exceptions documented with compensating controls          │
│  □ Review completion within the defined cadence              │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 9: Break-Glass Procedures

Emergency access must exist but must be audited and time-bound.

```
┌──────────────────────────────────────────────────────────────┐
│          BREAK-GLASS EMERGENCY ACCESS                        │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐   │
│  │ INCIDENT │─▶│ REQUEST   │─▶│ GRANT    │─▶│ USE      │   │
│  │ Detected │  │ Emergency │  │ Temp     │  │ Emergency│   │
│  │          │  │ Access    │  │ Access   │  │ Access   │   │
│  └──────────┘  └───────────┘  └──────────┘  └────┬─────┘   │
│                                                   │          │
│                    ┌──────────────────────────────┤          │
│                    │                              │          │
│              ┌─────▼─────┐               ┌───────▼──────┐   │
│              │ REVOKE    │               │ POST-INCIDENT│   │
│              │ Access    │               │ REVIEW       │   │
│              │ (auto or  │               │ (mandatory   │   │
│              │  manual)  │               │  within 24h) │   │
│              └───────────┘               └──────────────┘   │
│                                                              │
│  BREAK-GLASS REQUIREMENTS                                    │
│  □ Emergency credentials exist for production access?        │
│  □ Credentials stored securely? (sealed envelope, vault)     │
│  □ Every use is logged automatically?                        │
│    → Cannot be disabled by the person using break-glass      │
│  □ Access is time-limited? (auto-revoke after 4-8 hours)     │
│  □ Post-incident review is mandatory within 24 hours?        │
│    → What happened, why was it needed, what was accessed      │
│  □ At least 2 people know the break-glass procedure?         │
│  □ Break-glass is tested periodically? (at least annually)   │
│  □ The procedure is documented and accessible offline?       │
│    → If the system is down, can you still find the procedure?│
│                                                              │
│  ANTI-PATTERNS                                               │
│  → Shared admin password in a Slack channel                  │
│  → Break-glass credentials that never expire                 │
│  → No logging of break-glass usage                           │
│  → Break-glass used for convenience instead of emergencies   │
│  → No post-incident review process                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 10: Compliance Mapping

Map every finding to the relevant compliance framework control.

### Compliance Control Matrix

| Control Area | SOC 2 | HIPAA | PCI-DSS | What It Means |
|---|---|---|---|---|
| Logical access controls | CC6.1 | §164.312(d) | Req 7.1 | Restrict access to need-to-know |
| User authentication | CC6.1 | §164.312(d) | Req 8.1 | Unique IDs, no shared accounts |
| MFA for privileged access | CC6.1 | §164.312(d) | Req 8.3 | Something you know + have |
| Role-based access | CC6.2 | §164.312(a)(1) | Req 7.2 | Permissions based on job function |
| Access provisioning | CC6.2 | §164.308(a)(4) | Req 7.1 | Formal process for granting access |
| Access reviews | CC6.1 | §164.308(a)(4) | Req 7.1.1 | Periodic verification of access |
| Access revocation | CC6.3 | §164.308(a)(3) | Req 8.1.3 | Timely removal on termination |
| Service account mgmt | CC6.1 | §164.312(a)(1) | Req 8.6 | Machine identities governed |
| Least privilege | CC6.3 | §164.312(a)(1) | Req 7.2.2 | Minimum necessary access |
| Privilege escalation controls | CC6.1 | §164.312(a)(1) | Req 7.2 | Prevent unauthorized elevation |
| Emergency access | CC6.1 | §164.312(a)(1) | Req 7.1 | Documented break-glass process |
| Audit trail for access | CC7.2 | §164.312(b) | Req 10.2 | Log all access events |

### Finding-to-Control Mapping Template

When reporting findings, tag each with the applicable control:

```
Finding: Orphaned admin account for departed employee
Severity: CRITICAL
Controls: SOC 2 CC6.3, HIPAA §164.308(a)(3)(ii)(C), PCI-DSS 8.1.3
Risk: Former employee retains production admin access
Fix: Revoke immediately, implement automated deprovisioning
Evidence: Screenshot of active account + HR termination date
```

---

## Access Control Master Checklist

### Application Access (15 items)

```
□  Every API endpoint has authentication middleware
□  Every protected endpoint has role/permission authorization
□  Authorization checks happen before business logic
□  Tenant ID is enforced on every database query
□  Tenant context is derived from JWT, not request input
□  IDOR testing passed — cannot access other users' resources
□  Bulk endpoints are scoped to current tenant
□  Frontend permission checks are duplicated server-side
□  Role hierarchy is documented and matches code
□  Self-elevation is impossible (user cannot change own role)
□  Permission changes are logged with who/what/when
□  Password policy enforces minimum complexity
□  Rate limiting exists on authentication endpoints
□  Session tokens expire within a reasonable window
□  Token revocation works on logout and password change
```

### Infrastructure Access (10 items)

```
□  Cloud console access list is documented and current
□  Root/admin accounts are limited to break-glass only
□  IAM policies are scoped to specific resources (no *)
□  Unused IAM users/roles are deactivated
□  Database access requires VPN/bastion
□  Database credentials use individual accounts (no shared)
□  SSH access is key-based only, no password auth
□  CI/CD deployment credentials are minimally scoped
□  VPN access list matches current employee roster
□  Network segmentation separates prod from staging
```

### MFA (5 items)

```
□  MFA required for all privileged access paths
□  MFA bypass/recovery flows are documented and audited
□  MFA brute-force protection exists (rate limiting)
□  MFA enrollment is enforced for required roles
□  MFA secrets are stored encrypted at rest
```

### User Lifecycle (5 items)

```
□  Formal access request and approval process exists
□  Default permissions are minimal (no admin by default)
□  Role changes trigger re-certification of access
□  Deprovisioning SLA is defined and enforced (24h max)
□  Orphan account scan runs regularly (90-day inactivity)
```

### Service Accounts (5 items)

```
□  Every service account has a documented human owner
□  Service credentials rotate on a defined schedule
□  No credentials are hardcoded in source code
□  Compromised credentials can be revoked without downtime
□  Service-to-service calls require authentication
```

### Access Reviews (5 items)

```
□  Reviews happen on a defined cadence (quarterly minimum)
□  100% of users are reviewed, not a sample
□  Each review decision is documented with reviewer name
□  Modify/revoke decisions have evidence of remediation
□  Review evidence is retained for audit (6+ years SOC 2)
```

---

## Tips for Best Results

1. **Start with the user list** — Pull the complete list of active accounts from every system (application, cloud, database, VPN). Cross-reference with HR's current employee roster. The delta is your highest-priority finding.
2. **Check the departed** — Request the list of employees who left in the last 12 months. Verify every one of them has been fully deprovisioned across all systems. This is auditor question #1.
3. **Follow the admin trail** — Identify every account with admin or elevated privileges. For each, verify the business justification is documented and the person's current role requires that level of access.
4. **Test IDOR systematically** — For every API endpoint that takes a resource ID, swap it with an ID from another user or tenant. If the server returns data, you have a broken access control finding.
5. **Map service accounts to owners** — If a service account has no documented owner, flag it as CRITICAL. When the person who created it leaves, nobody knows it exists, what it accesses, or how to rotate it.
6. **Automate what humans forget** — Manual deprovisioning fails. Manual access reviews get rubber-stamped. Identify every manual access control process and recommend automation.
7. **Collect evidence as you go** — Screenshots, query results, configuration exports. Auditors want evidence, not assertions. Every finding and every "looks good" needs proof.

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
