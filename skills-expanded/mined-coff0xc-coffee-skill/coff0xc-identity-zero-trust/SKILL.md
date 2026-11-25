---
name: coff0xc-identity-zero-trust
description: "Use when the user requests identity, IAM, zero trust, AD/Active Directory, Kerberos, SSO/MFA, BloodHound, PAM, service accounts, permission/credential risk, identity paths, lateral-movement defense, access governance, or privileged-account convergence. Manual trigger: Use coff0xc-identity-zero-trust."
---

# coff0xc-identity-zero-trust

<!-- skill-id: cs-izt-5b0a7d2e -->

## Quick Rules (read this first for everyday tasks)
> **[Identity graph first]** First pin down principals, groups, roles, policies, sessions, devices, service accounts, and trust paths.
> **[Evidence gate]** Tie conclusions to configuration, logs, policies, BloodHound/graph paths, or code call sites.
> **[Fix priority]** Give least-privilege, MFA/session, segmented-access, audit, and rollback recommendations.
> **[Hard boundary]** Confirm first for IAM/AD writes, account disabling, key rotation, production permission changes, and lateral-movement validation.

Follow this section first for ordinary identity/zero-trust assessments; expand the full workflow only for real directory changes, exercises, or cross-environment governance.

## Capability
Permission-risk assessment capability for identity, access control, AD/Kerberos, IAM, and zero-trust governance. It helps answer "who can access what, why, where the risk is, and how to converge it."

## What It Can Deliver
- Identity/permission risk inventory and path explanations
- MFA/SSO/session/device posture assessment
- AD/Kerberos/IAM lateral-movement and privileged-account defense recommendations
- Least-privilege, PAM, conditional-access, and audit-verification plans

## What Input It Can Take
- IAM policies, AD/BloodHound output, SSO/MFA configuration
- Account/role/group/permission matrices, login logs, access anomalies
- Zero Trust policies, device posture, session policies

## Safe-Use Boundaries
- Read-only analysis and defensive recommendations for authorized environments by default
- Credential acquisition, hash dumping, unauthorized lateral movement, or privilege-escalation steps are not provided
- Production identity-policy changes, account disabling, and key rotation must be confirmed first
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Looks at identity, devices, sessions, resources, and audit trails together
- Distinguishes configuration weaknesses from genuinely reachable paths
- Outputs convergence order and verification methods

## Typical Usage
```text
Use coff0xc-identity-zero-trust to assess this AD domain's Kerberos, BloodHound paths, and service-account risks.
Use coff0xc-identity-zero-trust to map who can access what and give a least-privilege convergence plan.
Use coff0xc-identity-zero-trust to review IAM, SSO, MFA, and privileged account exposure.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
